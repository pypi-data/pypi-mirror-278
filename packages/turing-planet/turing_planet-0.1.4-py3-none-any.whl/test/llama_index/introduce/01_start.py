import logging

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings

from turing_planet.llama_index.embeddings.sparkai import SparkAIEmbedding
from turing_planet.llama_index.llms.sparkai import SparkAI

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
endpoint = "172.31.164.103:9980"

# 使用自定义embedding和llm
Settings.llm = SparkAI(endpoint=endpoint)
Settings.embed_model = SparkAIEmbedding(endpoint=endpoint, domain="emb_xfyun")
Settings.chunk_size = 512

if __name__ == '__main__':

    # 过时api @see https://docs.llamaindex.ai/en/stable/getting_started/v0_10_0_migration/?h=servicecontext#deprecated-servicecontext
    # service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)

    # 加载数据
    documents = SimpleDirectoryReader("../data").load_data(show_progress=True)

    # 创建索引
    index = VectorStoreIndex.from_documents(documents=documents)

    # 创建查询引擎
    query_engine = index.as_query_engine(similarity_top_k=3)

    # 执行查询
    response = query_engine.query("截止2024年1月，合肥市创建国家卫生城市计划实施步骤进展到什么阶段了？")
    print(response)
