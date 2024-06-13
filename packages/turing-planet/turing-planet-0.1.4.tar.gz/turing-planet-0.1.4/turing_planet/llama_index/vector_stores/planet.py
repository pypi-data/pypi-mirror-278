import logging
import uuid
from typing import List, Any

from llama_index.core.schema import BaseNode, MetadataMode, TextNode
from llama_index.core.vector_stores import VectorStoreQuery, VectorStoreQueryResult
from llama_index.core.vector_stores.types import VectorStore
from llama_index.core.vector_stores.utils import node_to_metadata_dict, metadata_dict_to_node

from turing_planet.api.planet_vector_client import PlanetVectorClient, VectorAddRequest

logger = logging.getLogger(__name__)


# 星球向量数据库
class PlanetVectorStore(VectorStore):
    stores_text: bool = True

    def __init__(self, index_name: str, **kwargs: Any):
        self._index_name = index_name
        self._client = PlanetVectorClient(trace_id="llamaIndex", **kwargs)
        pass

    @property
    def client(self) -> Any:
        return self._client

    def add(
            self,
            nodes: List[BaseNode],
            **add_kwargs: Any,
    ) -> List[str]:
        '''
        向量数据存储到星球服务
        '''
        if len(nodes) == 0:
            return []

        requests = []
        return_ids = []
        for node in nodes:
            _id = node.node_id if node.node_id else str(uuid.uuid4())
            requests.append(VectorAddRequest(vid=_id,
                                             vector=node.get_embedding(),
                                             text=node.get_content(metadata_mode=MetadataMode.NONE),
                                             metadata=node_to_metadata_dict(node, remove_text=True)))
            return_ids.append(_id)

        self._client.add(index_name=self._index_name, vector_requests=requests)

        return return_ids

    def delete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        self._client.delete(index_name=self._index_name, ref_doc_id=ref_doc_id, **delete_kwargs)

    def query(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        filters = {}
        if query.filters is not None and len(query.filters.legacy_filters()) > 0:
            for _filter in query.filters.legacy_filters():
                filters[_filter.key] = _filter.value

        # TODO 暂且不考虑标量查询
        payload = self._client.query(index_name=self._index_name,
                                     vector=query.query_embedding,
                                     top_k=query.similarity_top_k,
                                     filters=filters,
                                     query_str=query.query_str,
                                     **kwargs)

        top_k_nodes = []
        top_k_ids = []
        top_k_scores = []
        result = payload["data"]

        for hit in result:
            metadata = hit.get("metadata", None)
            node = metadata_dict_to_node(metadata)
            node.text = hit.get("text", None)
            top_k_nodes.append(node)
            top_k_ids.append(hit.get("id"))
            top_k_scores.append(hit["score"])

        return VectorStoreQueryResult(
            nodes=top_k_nodes,
            ids=top_k_ids,
            similarities=top_k_scores,
        )

    # 自定义添加的函数
    def drop(self):
        self._client.drop_index(self._index_name)
