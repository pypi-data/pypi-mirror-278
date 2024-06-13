from llama_index.core import VectorStoreIndex, get_response_synthesizer, ServiceContext
from llama_index.core.indices.vector_store import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.vector_stores import MetadataFilters, MetadataFilter, FilterOperator

from test.llama_index.introduce.introduce_base import redis_store, vector_filter_key


def query():
    #  向量检索
    vector_index = VectorStoreIndex.from_vector_store(vector_store=redis_store)

    # 设置过滤条件
    filters = MetadataFilters(
        filters=[
            MetadataFilter(key=vector_filter_key, operator=FilterOperator.TEXT_MATCH, value="hf"),
        ]
    )
    vector_retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=3, filters=filters)

    query_engine = RetrieverQueryEngine(retriever=vector_retriever, response_synthesizer=get_response_synthesizer())

    question = "截止2024年1月，合肥市创建国家卫生城市计划实施步骤进展到什么阶段了？"
    response = query_engine.query(question)
    print(f"Q:{question}")
    print("A:" + response.response.replace("<ret>", "\n").replace("<end>", "\n"))
    print("---------------\n")


if __name__ == '__main__':
    query()
