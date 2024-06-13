from typing import List, Any, Optional

from llama_index.core.base.embeddings.base import BaseEmbedding, Embedding

from turing_planet.api.planet_embedding_client import PlanetEmbeddingClient


class SparkAIEmbedding(BaseEmbedding):
    client: Any

    def __init__(self,
                 embed_type: Optional[str] = None,
                 trace_id: Optional[str] = "llama_index",
                 **kwargs: Any):
        # self._model = "iflytek_embedding"
        super().__init__(**kwargs)
        self.client = PlanetEmbeddingClient(trace_id=trace_id, **kwargs)

    def _get_query_embedding(self, query: str) -> List[float]:
        return self.client.embedding_query(text=query)

    def _get_text_embedding(self, text: str) -> List[float]:
        embeddings = self.client.embedding_documents(texts=[text])
        return embeddings[0]

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        return self.client.embedding_documents(texts=texts)

    async def _aget_query_embedding(self, query: str) -> Embedding:
        return self.client.embedding_query(text=query)


if __name__ == "__main__":
    emebedding = SparkAIEmbedding(endpoint="172.31.101.142:9980")
    # emebedding = SparkAIEmbedding(endpoint="172.31.97.139:9980", domain="emb_v1")

    print("======  embed_query ========")
    result = emebedding.get_query_embedding("你好啊啊")
    print(result)

    print("======  embed_documents ========")
    result = emebedding.get_text_embedding_batch(texts=["你好啊啊", "来自langchain的问候"])
    print(result)
