import logging

from llama_index.core import SimpleDirectoryReader, ServiceContext, StorageContext, VectorStoreIndex
from llama_index.vector_stores.redis import RedisVectorStore

from turing_planet.llama_index.embeddings.sparkai import SparkAIEmbedding
from turing_planet.llama_index.llms.sparkai import SparkAI
from turing_planet.llama_index.vector_stores.planet import PlanetVectorStore

logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为DEBUG，可以根据需要修改
    format="%(asctime)s - %(levelname)s - %(message)s",
)

index_name = "skynet-doc-qa"
endpoint_planet = "127.0.0.1:9980"
redis_url = "redis://172.31.128.153:6379"
embed_model = SparkAIEmbedding(endpoint=endpoint_planet, domain="emb_v2")
llm = SparkAI()
service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)
planet_store = PlanetVectorStore(index_name=index_name, endpoint=endpoint_planet)
storage_context = StorageContext.from_defaults(vector_store=planet_store)

redis_store = RedisVectorStore(index_name=index_name, index_prefix="_".join([index_name, "vector"]),
                               redis_url=redis_url)
redis_storage_context = StorageContext.from_defaults(vector_store=redis_store)


def load_documents():
    simple_reader = SimpleDirectoryReader(
        # 文档路径
        input_dir="/Users/wujian/Downloads/skynet-doc-center",
        # 扫描子目录
        recursive=True,
        # 排除哪些目录
        exclude=[".git"],
        # 文件后缀名要求
        required_exts=[".pdf", ".docx", ".txt", ".md", ".ppt", ".pptm", ".ppt"]
    )

    documents = simple_reader.load_data(show_progress=True)

    # 统计文档扫描情况
    file_dict = {}
    for document in documents:
        path = document.metadata.get("file_path")
        file_doc_count = file_dict.get(path, 0)
        file_dict[path] = file_doc_count + 1

    for key, value in file_dict.items():
        print(key, "---", value)

    return documents


def add_planet_vector():
    VectorStoreIndex.from_documents(documents=load_documents(),
                                    storage_context=storage_context,
                                    service_context=service_context,
                                    show_progress=True)


def add_redis_vector():
    VectorStoreIndex.from_documents(documents=load_documents(),
                                    storage_context=redis_storage_context,
                                    service_context=service_context,
                                    show_progress=True)


def query(vector_store):
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store, service_context=service_context,
                                               show_progress=True)
    query_engine = index.as_query_engine(similarity_top_k=1)
    response = query_engine.query("图聆api网关支持哪些限流方式")
    print(response)
    print("========知识来源========")
    for index, source_node in enumerate(response.source_nodes):
        print(f"---------------第{index}段, 得分：{source_node.score}------------------")
        print(f"文本内容\n: {source_node.text}")


def query_planet():
    query(planet_store)


def query_redis():
    query(redis_store)


def query_memory():
    index = VectorStoreIndex.from_documents(documents=load_documents(), service_context=service_context);
    query_engine = index.as_query_engine(similarity_top_k=1)
    response = query_engine.query("ogma配置项")
    print(response)


if __name__ == '__main__':
    # add_redis_vector()
    # query_redis()
    # query_planet()
    query_memory()
