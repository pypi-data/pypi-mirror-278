import logging

from llama_index.core import StorageContext, SimpleDirectoryReader, VectorStoreIndex, ServiceContext, DocumentSummaryIndex
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.storage.index_store.mongodb import MongoIndexStore
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.vector_stores.redis import RedisVectorStore

from turing_planet.llama_index.embeddings.sparkai import SparkAIEmbedding
from turing_planet.llama_index.llms.sparkai import SparkAI
from turing_planet.llama_index.vector_stores.planet import PlanetVectorStore

logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为DEBUG，可以根据需要修改
    format="%(asctime)s - %(levelname)s - %(message)s",
)

embed_model = SparkAIEmbedding(endpoint="127.0.0.1:9980")
llm = SparkAI(timeout=120)
service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm, chunk_size=200)

# 加载数据
documents = SimpleDirectoryReader("./data").load_data()


# 外部向量存储
def store_with_es():
    # mongodb://root:Mgadmin_1234@172.31.164.103:30006 / turing_planet?authSource = admin & authMechanism = SCRAM - SHA - 1
    mongo_docstore = MongoDocumentStore.from_uri(uri="mongodb://root:Mgadmin_1234@172.31.164.103:30006",
                                                 db_name="llama-index-sample")

    mongo_index_store = MongoIndexStore.from_uri(uri="mongodb://root:Mgadmin_1234@172.31.164.103:30006",
                                                 db_name="llama-index-sample")
    es_store = ElasticsearchStore(es_url="http://172.31.164.103:49200", index_name="llama-index-sample", batch_size=10)

    # 指定外部向量存储组件
    storage_context = StorageContext.from_defaults(docstore=mongo_docstore, vector_store=es_store,
                                                   index_store=mongo_index_store)

    # 从向量数据库直接读取index
    index = VectorStoreIndex.from_vector_store(vector_store=es_store, service_context=service_context,
                                               show_progress=True)
    query_engine = index.as_query_engine(similarity_top_k=1)
    response = query_engine.query("注册和重新注册接口有什么区别？")
    print(response)


def store_with_redis():
    redis_store = RedisVectorStore(index_name="",
                                   index_prefix="llamaindex-xfyun_vector",
                                   redis_url="redis://172.31.128.153:6379")
    storage_context = StorageContext.from_defaults(vector_store=redis_store)
    index = VectorStoreIndex.from_documents(documents=documents,
                                            storage_context=storage_context,
                                            service_context=service_context,
                                            show_progress=True)
    query_engine = index.as_query_engine(similarity_top_k=1)
    response = query_engine.query("注册和重新注册接口有什么区别？")
    print(response)


def document_summary():
    index = DocumentSummaryIndex.from_documents(documents=documents, service_context=service_context,
                                                show_progress=True)
    query_engine = index.as_query_engine(similarity_top_k=1)
    response = query_engine.query("注册和重新注册接口有什么区别？")
    print(response)


def store_with_planet():
    planet_store = PlanetVectorStore(index_name="llama-index", endpoint="127.0.0.1:9980");
    storage_context = StorageContext.from_defaults(vector_store=planet_store, )
    # index = VectorStoreIndex.from_documents(documents=documents,
    #                                         storage_context=storage_context,
    #                                         service_context=service_context,
    #                                         show_progress=True)

    index = VectorStoreIndex.from_vector_store(vector_store=planet_store, service_context=service_context,
                                               show_progress=True)
    # 非流式
    # query_engine = index.as_query_engine(similarity_top_k=1)
    # response = query_engine.query("注册和重新注册接口有什么区别？")
    # print(response)

    # 流式
    query_engine = index.as_query_engine(streaming=True, similarity_top_k=1)
    streaming_response = query_engine.query("注册和重新注册接口有什么区别？")
    for index, text in enumerate(streaming_response.response_gen):
        print(index, text)
    print("======回答结束 ====")


def sample_drop_index():
    planet_store = PlanetVectorStore(index_name="llama-index", endpoint="127.0.0.1:9980");
    planet_store.drop()


if __name__ == '__main__':
    # document_summary()
    # store_with_es()
    # store_with_planet()
    # sample_drop_index()
    store_with_redis()
