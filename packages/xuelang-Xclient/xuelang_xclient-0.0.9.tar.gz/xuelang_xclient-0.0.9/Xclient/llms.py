from __future__ import annotations

import json
import queue
import random
import time
from functools import partial
from typing import Any, Dict, Iterator, List, Optional, Sequence, Union

import google.protobuf.json_format
import numpy as np
import tritonclient.grpc as grpcclient
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseLLM
from langchain_core.outputs import Generation, GenerationChunk, LLMResult
from langchain_core.pydantic_v1 import Field, root_validator
from tritonclient.grpc.service_pb2 import ModelInferResponse
from tritonclient.utils import np_to_triton_dtype


class TritonvLLMError(Exception):
    """Base exception for TritonTensorRT."""


class TritonvLLMRuntimeError(TritonvLLMError, RuntimeError):
    """Runtime error for TritonTensorRT."""


class ChatMetaLM(BaseLLM):
    """TRTLLM triton models.

    Arguments:
        server_url: (str) The URL of the Triton inference server to use.
        model_name: (str) The name of the Triton TRT model to use.
        ignore_eos : (bool), 
        skip_special_tokens: (bool), 
        use_beam_search: (bool),
        frequency_penalty: (float),
        length_penalty: (float),
        presence_penalty: (float),
        temperature: (float),
        top_p: (float),
        best_of: (int), 
        max_tokens: (int), 
        min_tokens: (int), 
        n: (int), 
        top_k: (int)


    """
    server_url: Optional[str] = Field(None, alias="server_url")
    model_name: str = Field(
        ..., description="The name of the model to use, such as 'ensemble'."
    )
    client: grpcclient.InferenceServerClient
    ignore_eos: bool = False
    skip_special_tokens: bool = True
    use_beam_search: bool = False
    frequency_penalty: float = 0.0
    length_penalty: float = 1.0
    presence_penalty: float = 0.0
    temperature: float = 1.0
    top_p: float = 1.0
    best_of: int = 1.0
    max_tokens: int = 200
    min_tokens: int = 0
    n: int = 1
    top_k: int = -1
    stop: List[str] = Field(
        default_factory=lambda: ["</s>"], description="Stop tokens."
    )

    def __del__(self):
        """Ensure the client streaming connection is properly shutdown"""
        self.client.close()

    @root_validator(pre=True, allow_reuse=True)
    def validate_environment(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that python package exists in environment."""
        if not values.get("client"):
            values["client"] = grpcclient.InferenceServerClient(values["server_url"])
        return values

    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "nvidia-trt-llm"

    @property
    def _model_default_parameters(self) -> Dict[str, Any]:
        return {
            "ignore_eos": self.ignore_eos,
            "skip_special_tokens": self.skip_special_tokens,
            "use_beam_search": self.use_beam_search,
            "frequency_penalty": self.frequency_penalty,
            "length_penalty": self.length_penalty,
            "presence_penalty": self.presence_penalty,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "best_of": self.best_of,
            "max_tokens": self.max_tokens,
            "min_tokens": self.min_tokens,
            "n": self.n,
            "top_k": self.top_k
        }

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get all the identifying parameters."""
        return {
            "server_url": self.server_url,
            "model_name": self.model_name,
            **self._model_default_parameters,
        }

    def _get_invocation_params(self, **kwargs: Any) -> Dict[str, Any]:
        return {**self._model_default_parameters, **kwargs}

    def get_model_list(self) -> List[str]:
        """Get a list of models loaded in the triton server."""
        res = self.client.get_model_repository_index(as_json=True)
        return [model["name"] for model in res["models"]]

    def _load_model(self, model_name: str, timeout: int = 1000) -> None:
        """Load a model into the server."""
        if self.client.is_model_ready(model_name):
            return

        self.client.load_model(model_name)
        t0 = time.perf_counter()
        t1 = t0
        while not self.client.is_model_ready(model_name) and t1 - t0 < timeout:
            t1 = time.perf_counter()

        if not self.client.is_model_ready(model_name):
            raise TritonTensorRTRuntimeError(
                f"Failed to load {model_name} on Triton in {timeout}s"
            )

    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        self._load_model(self.model_name)

        invocation_params = self._get_invocation_params(**kwargs)
        stop_words = stop if stop is not None else self.stop
        generations = []
        # TODO: We should handle the native batching instead.
        for prompt in prompts:
            invoc_params = {**invocation_params, "prompt": [[prompt]]}
            result: str = self._request(
                self.model_name,
                stop=stop_words,
                **invoc_params,
            )
            generations.append([Generation(text=result, generation_info={})])
        return LLMResult(generations=generations)

    def _stream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        self._load_model(self.model_name)

        invocation_params = self._get_invocation_params(**kwargs, prompt=[[prompt]])
        stop_words = stop if stop is not None else self.stop

        inputs = self._generate_inputs(stream=True, **invocation_params)
        outputs = self._generate_outputs()

        result_queue = self._invoke_triton(self.model_name, inputs, outputs, stop_words)

        for token in result_queue:
            yield GenerationChunk(text=token)
            if run_manager:
                run_manager.on_llm_new_token(token)

        self.client.stop_stream()

    ##### BELOW ARE METHODS PREVIOUSLY ONLY IN THE GRPC CLIENT

    def _request(
        self,
        model_name: str,
        prompt: Sequence[Sequence[str]],
        stop: Optional[List[str]] = None,
        **params: Any,
    ) -> str:
        """Request inferencing from the triton server."""
        # create model inputs and outputs
        inputs = self._generate_inputs(stream=False, prompt=prompt, **params)
        outputs = self._generate_outputs()

        result_queue = self._invoke_triton(self.model_name, inputs, outputs, stop)

        result_str = ""
        try:
            for token in result_queue:
                if isinstance(token, Exception):
                    raise token
                result_str += token
        finally:
            self.client.stop_stream()

        return result_str

    def _invoke_triton(self, model_name, inputs, outputs, stop_words):
        if not self.client.is_model_ready(model_name):
            raise RuntimeError("Cannot request streaming, model is not loaded")

        request_id = str(random.randint(1, 9999999))  # nosec

        result_queue = StreamingResponseGenerator(
            self,
            request_id,
            force_batch=False,
            stop_words=stop_words,
        )

        self.client.start_stream(
            callback=partial(
                self._stream_callback,
                result_queue,
                stop_words=stop_words,
            )
        )

        # Even though this request may not be a streaming request certain configurations
        # in Triton prevent the GRPC server from accepting none streaming connections.
        # Therefore we call the streaming API and combine the streamed results.
        self.client.async_stream_infer(
            model_name=model_name,
            inputs=inputs,
            outputs=outputs,
            request_id=request_id,
        )

        return result_queue

    def _generate_outputs(
        self,
    ) -> List[grpcclient.InferRequestedOutput]:
        """Generate the expected output structure."""
        return [grpcclient.InferRequestedOutput("text_output")]

    def _prepare_tensor(
        self, name: str, input_data: np.ndarray
    ) -> grpcclient.InferInput:
        """Prepare an input data structure."""

        t = grpcclient.InferInput(
            name, input_data.shape, np_to_triton_dtype(input_data.dtype)
        )
        t.set_data_from_numpy(input_data)
        return t

    def _generate_inputs(
        self,
        prompt: Sequence[Sequence[str]],
        stream: bool = True,
        **params
    ) -> List[grpcclient.InferRequestedOutput]:
        """Create the input for the triton inference server."""
        print(prompt)
        query = np.array(prompt).astype(object).reshape((1))
        streaming_data = np.array([stream], dtype=bool)
        params['stop'] = self.stop
        sampling_parameters_data = np.array(json.dumps(params)).astype(object).reshape((1))
        print(sampling_parameters_data)
        inputs = [
            self._prepare_tensor("text_input", query),
            self._prepare_tensor("stream", streaming_data),
            self._prepare_tensor("sampling_parameters", sampling_parameters_data),
        ]
        return inputs

    def _send_stop_signals(self, model_name: str, request_id: str) -> None:
        """Send the stop signal to the Triton Inference server."""
        stop_inputs = self._generate_stop_signals()
        self.client.async_stream_infer(
            model_name,
            stop_inputs,
            request_id=request_id,
            parameters={"Streaming": True},
        )

    def _generate_stop_signals(
        self,
    ) -> List[grpcclient.InferInput]:
        """Generate the signal to stop the stream."""
        inputs = [
            grpcclient.InferInput("input_ids", [1, 1], "INT32"),
            grpcclient.InferInput("input_lengths", [1, 1], "INT32"),
            grpcclient.InferInput("request_output_len", [1, 1], "UINT32"),
            grpcclient.InferInput("stop", [1, 1], "BOOL"),
        ]
        inputs[0].set_data_from_numpy(np.empty([1, 1], dtype=np.int32))
        inputs[1].set_data_from_numpy(np.zeros([1, 1], dtype=np.int32))
        inputs[2].set_data_from_numpy(np.array([[0]], dtype=np.uint32))
        inputs[3].set_data_from_numpy(np.array([[True]], dtype="bool"))
        return inputs

    @staticmethod
    def _process_result(result: Dict[str, str]) -> str:
        """Post-process the result from the server."""

        message = ModelInferResponse()
        google.protobuf.json_format.Parse(json.dumps(result), message)
        infer_result = grpcclient.InferResult(message)
        np_res = infer_result.as_numpy("text_output")

        generated_text = ""
        if np_res is not None:
            generated_text = "".join([token.decode() for token in np_res])

        return generated_text

    def _stream_callback(
        self,
        result_queue: queue.Queue[Union[Optional[Dict[str, str]], str]],
        result: grpcclient.InferResult,
        error: str,
        stop_words: List[str],
    ) -> None:
        """Add streamed result to queue."""
        if error:
            result_queue.put(error)
        else:
            response_raw: dict = result.get_response(as_json=True)
            # TODO: Check the response is a map rather than a string
            if "outputs" in response_raw:
                # the very last response might have no output, just the final flag
                response = self._process_result(response_raw)

                if response in stop_words:
                    result_queue.put(None)
                else:
                    result_queue.put(response)

            if response_raw["parameters"]["triton_final_response"]["bool_param"]:
                # end of the generation
                result_queue.put(None)

    def stop_stream(
        self, model_name: str, request_id: str, signal: bool = True
    ) -> None:
        """Close the streaming connection."""
        if signal:
            self._send_stop_signals(model_name, request_id)
        self.client.stop_stream()


class StreamingResponseGenerator(queue.Queue):
    """A Generator that provides the inference results from an LLM."""

    def __init__(
        self,
        llm: ChatMetaLM,
        request_id: str,
        force_batch: bool,
        stop_words: Sequence[str],
    ) -> None:
        """Instantiate the generator class."""
        super().__init__()
        self.llm = llm
        self.request_id = request_id
        self._batch = force_batch
        self._stop_words = stop_words

    def __iter__(self) -> StreamingResponseGenerator:
        """Return self as a generator."""
        return self

    def __next__(self) -> str:
        """Return the next retrieved token."""
        val = self.get()
        if val is None or val in self._stop_words:
            self.llm.stop_stream(
                self.llm.model_name, self.request_id, signal=not self._batch
            )
            raise StopIteration()
        return val