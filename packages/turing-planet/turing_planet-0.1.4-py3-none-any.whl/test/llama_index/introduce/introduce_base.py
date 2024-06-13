import logging

from dotenv import load_dotenv
from llama_index.core import StorageContext
from llama_index.core.settings import Settings
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.storage.index_store.mongodb import MongoIndexStore
from llama_index.vector_stores.redis import RedisVectorStore
from redis import Redis
from redisvl.schema import IndexSchema

from turing_planet.llama_index.embeddings.sparkai import SparkAIEmbedding
from turing_planet.llama_index.llms.sparkai import SparkAI

# 加载环境变量
load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为DEBUG，可以根据需要修改
    format="%(asctime)s - %(levelname)s - %(message)s",
)
# 向量特征维度
dims = 2560
endpoint = "172.31.164.103:9980"
Settings.llm = SparkAI(endpoint=endpoint, domain="generalv3.5")
Settings.embed_model = SparkAIEmbedding(endpoint=endpoint, domain="emb_xfyun")
Settings.chunk_size = 1024

# TODO 额外参数
vector_filter_key = "location"

redis_index_schema = IndexSchema.from_dict(
    {
        # customize basic index specs
        "index": {
            "name": "llamaindex-introduce",
            "prefix": "llamaindex-introduce_vector",
            "key_separator": ":",
        },
        # customize fields that are indexed
        "fields": [
            {"name": "id", "type": "tag"},
            {"name": "doc_id", "type": "tag"},
            {"name": "text", "type": "text"},
            {"name": "vector", "type": "vector",
             "attrs": {"dims": dims, "algorithm": "flat", "distance_metric": "cosine", }},
            {"name": vector_filter_key, "type": "text"}
        ],
    }
)

redis_client = Redis.from_url("redis://172.31.128.153:6379")
redis_store = RedisVectorStore(schema=redis_index_schema, redis_client=redis_client, overwrite=False)

mongo_doc_store = MongoDocumentStore.from_uri(uri="mongodb://root:Mgadmin_1234@172.31.164.103:30006",
                                              db_name="llamaindex-introduce")

mongo_index_store = MongoIndexStore.from_uri(uri="mongodb://root:Mgadmin_1234@172.31.164.103:30006",
                                             db_name="llamaindex-introduce")

storage_context = StorageContext.from_defaults(vector_store=redis_store, docstore=mongo_doc_store,
                                               index_store=mongo_index_store)
