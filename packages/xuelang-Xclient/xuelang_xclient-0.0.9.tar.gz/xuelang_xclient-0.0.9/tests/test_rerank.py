from Xclient import MetaLMRerank
import os
from typing import List


from langchain_core.documents import Document


class CharacterTextSplitter:
    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size

    def create_documents(self, text: str) -> List[Document]:
        words = text.split(',')
        chunks = []
        for i in range(0, len(words), self.chunk_size):
            chunk = " ".join(words[i : i + self.chunk_size])
            chunks.append(Document(page_content=chunk))
        return chunks
splitter = CharacterTextSplitter(1)
documents = splitter.create_documents("测试程序1,测试程序2,测试程序3,测试程序4,测试程序5,测试程序6,测试程序7",)
query = '测试程序5'

rerank = MetaLMRerank(model="bge-reranker-v2-m3",base_url="http://10.88.36.58:8200")
result_docs = rerank.compress_documents(documents=documents, query=query)
print(result_docs)


