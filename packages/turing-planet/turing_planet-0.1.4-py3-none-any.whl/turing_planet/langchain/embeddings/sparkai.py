from typing import List, Any, Optional

from langchain.pydantic_v1 import BaseModel
from langchain.schema.embeddings import Embeddings

from turing_planet.api.planet_embedding_client import PlanetEmbeddingClient


class SparkAIEmbedding(BaseModel, Embeddings):
    client: Any

    def __init__(self,
                 trace_id: Optional[str] = "langchain_index",
                 **kwargs: Any):
        super().__init__(**kwargs)
        self.client = PlanetEmbeddingClient(trace_id=trace_id, **kwargs)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.client.embedding_documents(texts=texts)

    def embed_query(self, text: str) -> List[float]:
        return self.client.embedding_query(text=text)
