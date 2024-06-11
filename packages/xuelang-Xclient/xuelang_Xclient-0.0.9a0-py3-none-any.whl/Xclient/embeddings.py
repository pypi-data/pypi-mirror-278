import warnings
from typing import Any, List, Literal, Optional

from langchain_core.embeddings import Embeddings
from langchain_core.outputs.llm_result import LLMResult
from langchain_core.pydantic_v1 import BaseModel, Field, PrivateAttr, validator
import numpy as np
from .client import ModelClient,FuturesModelClient,DecoupledModelClient,AsyncioModelClient
import json

class MetaLMEmbeddings(BaseModel, Embeddings):
    """
    Client to NVIDIA embeddings models.

    Fields:
    - model: str, the name of the model to use
    - base_url: str 
    """

    class Config:
        validate_assignment = True
    _client: ModelClient = PrivateAttr(ModelClient)
    _default_model: str = "NV-Embed-QA"
    _default_max_batch_size: int = 12
    base_url: str = Field(
        "https://integrate.api.nvidia.com/v1",
        description="Base url for model listing an invocation",
    )
    model: str = Field(_default_model, description="Name of the model to invoke")
    truncate: Literal["NONE", "START", "END"] = Field(
        default="NONE",
        description=(
            "Truncate input text if it exceeds the model's maximum token length. "
            "Default is 'NONE', which raises an error if an input is too long."
        ),
    )
    max_batch_size: int = Field(default=_default_max_batch_size)
    model_type: Optional[Literal["passage", "query"]] = Field(
        None, description="(DEPRECATED) The type of text to be embedded."
    )

    def __init__(self, **kwargs: Any):

        super().__init__(**kwargs)
        self._client = ModelClient(
            url=self.base_url,
            model_name=self.model
        )

    def __del__(self):
        """Ensure the client streaming connection is properly shutdown"""
        self._client.close()

    @validator("model_type")
    def _validate_model_type(
        cls, v: Optional[Literal["passage", "query"]]
    ) -> Optional[Literal["passage", "query"]]:
        if v:
            warnings.warn(
                "Warning: `model_type` is deprecated and will be removed "
                "in a future release. Please use `embed_query` or "
                "`embed_documents` appropriately."
            )
        return v

    def _embed(
        self, texts: List[str]
    ) -> List[List[float]]:
        """Embed a single text entry to either passage or query type"""
        if texts == []:
            embeddings: List[List[float]] = [[] for _ in range(len(texts))]
            return embeddings
       
        texts = [[x.encode('utf-8')] for x in texts]
        texts = np.array(
            texts, dtype=np.object_
        )
        query_emb = self._client.infer_batch(texts)['dense_vecs']

        return query_emb.tolist()

    def _embed_with_sparse(
        self, texts: List[str]
    ):
        """Embed a single text entry to either passage or query type"""
        if texts == []:
            embeddings: List[List[float]] = [[] for _ in range(len(texts))]
            return embeddings
        
        texts = [[x.encode('utf-8')] for x in texts]
        texts = np.array(
            texts, dtype=np.object_
        )
        query_emb = self._client.infer_batch(texts)
        
        sparse_vecs = []
        for vec in query_emb['sparse_vecs']:
            string_data = vec.decode('utf-8')
            sparse_vecs.append(json.loads(string_data))

        return query_emb['dense_vecs'].tolist(),sparse_vecs
    
    def embed_query(self, text: str) -> List[float]:
        """Input pathway for query embeddings."""
        return self._embed([text])[0]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Input pathway for document embeddings."""
        if not isinstance(texts, list) or not all(
            isinstance(text, str) for text in texts
        ):
            raise ValueError(f"`texts` must be a list of strings, given: {repr(texts)}")

        all_embeddings = []
        for i in range(0, len(texts), self.max_batch_size):
            batch = texts[i : i + self.max_batch_size]
            all_embeddings.extend(
                self._embed(batch)
            )
        return all_embeddings
    
    def embed_query_sparse(self, text: str):
        """Input pathway for query embeddings."""
        return self._embed_with_sparse([text])[0][0],self._embed_with_sparse([text])[1][0]

    def embed_documents_sparse(self, texts: List[str]):
        """Input pathway for document embeddings."""
        if not isinstance(texts, list) or not all(
            isinstance(text, str) for text in texts
        ):
            raise ValueError(f"`texts` must be a list of strings, given: {repr(texts)}")

        all_embeddings = []
        for i in range(0, len(texts), self.max_batch_size):
            batch = texts[i : i + self.max_batch_size]
            all_embeddings.extend(
                self._embed_with_sparse(batch)
            )
        return all_embeddings
                
                
                