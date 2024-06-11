from __future__ import annotations

from typing import Any, Generator, List, Optional, Sequence

from langchain_core.callbacks.manager import Callbacks
from langchain_core.documents import Document
from langchain_core.documents.compressor import BaseDocumentCompressor
from langchain_core.pydantic_v1 import BaseModel, Field, PrivateAttr
import numpy as np
from .client import ModelClient,FuturesModelClient,DecoupledModelClient,AsyncioModelClient

class Ranking(BaseModel):
    index: int
    logit: float


class MetaLMRerank(BaseDocumentCompressor):
    """
    LangChain Document Compressor that uses the NVIDIA NeMo Retriever Reranking API.
    """

    class Config:
        validate_assignment = True

    _default_model_name: str = "nv-rerank-qa-mistral-4b:1"
    _client: ModelClient = PrivateAttr(ModelClient)
    base_url: str = Field(
        "https://integrate.api.nvidia.com/v1",
        description="Base url for model listing an invocation",
    )
    top_n: int = Field(5, ge=0, description="The number of documents to return.")
    model: str = Field(
        _default_model_name, description="The model to use for reranking."
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

    # todo: batching when len(documents) > endpoint's max batch size
    def _rank(self, documents: List[str], query: str) -> List[Ranking]:
        source_sentence = np.array([query.encode("utf-8")], 
            dtype=np.object_
        )
        page_content= np.array([d.page_content.encode("utf-8") for d in documents], 
            dtype=np.object_
        )

        score = self._client.infer_sample(source_sentence,page_content)['score'].tolist()
        score_id = sorted(range(len(score)),key=lambda k:score[k],reverse=True)
        sorted_score = sorted(score,reverse=True)
        N = min(self.top_n,len(score))
        return [Ranking(index=score_id[i],logit=sorted_score[i]) for i in range(N)]

    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        callbacks: Optional[Callbacks] = None,
    ) -> Sequence[Document]:
        if len(documents) == 0 or self.top_n < 1:
            return []

        def batch(ls: list, size: int) -> Generator[List[Document], None, None]:
            for i in range(0, len(ls), size):
                yield ls[i : i + size]

        doc_list = list(documents)
        results = []

        rankings = self._rank(
            query=query, documents=doc_list
        )
        for ranking in rankings:
            doc = doc_list[ranking.index]
            doc.metadata["relevance_score"] = ranking.logit
            results.append(doc)
        return results