# 向量 + 摘要索引
from typing import List

from llama_index.core import get_response_synthesizer, QueryBundle, DocumentSummaryIndex, VectorStoreIndex, \
    StorageContext
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.indices.document_summary import DocumentSummaryIndexLLMRetriever
from llama_index.core.indices.vector_store import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.schema import NodeWithScore
from llama_index.storage.index_store.mongodb import MongoIndexStore

from test.llama_index.optimizing.base import build_vector_store, load_documents, build_service_context, user_questions


class CustomRetriever(BaseRetriever):

    def __init__(
            self,
            vector_retriever: VectorIndexRetriever,
            summary_retriever: DocumentSummaryIndex,
            mode: str = "OR",
    ) -> None:
        """Init params."""
        self._vector_retriever = vector_retriever
        self._summary_retriever = summary_retriever
        if mode not in ("AND", "OR"):
            raise ValueError("Invalid mode.")
        self._mode = mode
        super().__init__()

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Retrieve nodes given query."""
        # 分别检索，根据设置进行合并命中的node
        vector_nodes = self._vector_retriever.retrieve(query_bundle)
        summary_nodes = self._summary_retriever.retrieve(query_bundle)

        vector_ids = {n.node.node_id for n in vector_nodes}
        summary_ids = {n.node.node_id for n in summary_nodes}

        combined_dict = {n.node.node_id: n for n in vector_nodes}
        combined_dict.update({n.node.node_id: n for n in summary_nodes})

        if self._mode == "AND":
            retrieve_ids = vector_ids.intersection(summary_ids)
        else:
            retrieve_ids = vector_ids.union(summary_ids)

        retrieve_nodes = [combined_dict[rid] for rid in retrieve_ids]
        return retrieve_nodes


summary_query = """
描述提供的文本是关于什么的。

同时描述本文可以回答的一些问题。
"""

INDEX_NAME = "hf_llamaindex_sm_vec"

if __name__ == '__main__':
    # 构建摘要索引
    mongo_index_store = MongoIndexStore.from_uri(uri="mongodb://root:Mgadmin_1234@172.31.164.103:30006",
                                                 db_name="hf-llamaindex-sm")
    storage_context = StorageContext.from_defaults(index_store=mongo_index_store)

    doc_summary_index = DocumentSummaryIndex.from_documents(
        load_documents(),
        service_context=build_service_context(),
        storage_context=storage_context,
        summary_query=summary_query,
        show_progress=True,
    )

    # 构建向量索引
    vector_index = VectorStoreIndex.from_documents(documents=load_documents(),
                                                   storage_context=StorageContext.from_defaults(
                                                       vector_store=build_vector_store(index_name=INDEX_NAME)),
                                                   service_context=build_service_context(),
                                                   show_progress=True)
    # 构建检索器
    vector_retriever = VectorIndexRetriever(index=vector_index)
    summary_retriever = DocumentSummaryIndexLLMRetriever(index=doc_summary_index)
    # 使用自定义检索器
    custom_retriever = CustomRetriever(vector_retriever, summary_retriever)
    vector_retriever = VectorIndexRetriever(index=vector_index)
    # 构建响应合成器
    response_synthesizer = get_response_synthesizer(
        service_context=build_service_context(),
        response_mode="tree_summarize",
    )

    query_engine = RetrieverQueryEngine(retriever=custom_retriever, response_synthesizer=response_synthesizer)

    for question in user_questions:
        response = query_engine.query(question + "\nResponse in Chinese")
        print(f"Q:{question}")
        print("A:" + response.response.replace("<ret>", "\n").replace("<end>", "\n"))
        # print(f"source:{response.source_nodes[0].text}")
        print("---------------\n")
