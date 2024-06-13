import logging

from llama_index.core import ServiceContext, SimpleDirectoryReader, VectorStoreIndex, StorageContext, KnowledgeGraphIndex, \
    TreeIndex, PromptTemplate
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.graph_stores import SimpleGraphStore
from llama_index.core.postprocessor import KeywordNodePostprocessor
from llama_index.core.vector_stores import MetadataFilters, MetadataFilter, FilterOperator

from turing_planet.llama_index.embeddings.sparkai import SparkAIEmbedding
from turing_planet.llama_index.llms.sparkai import SparkAI

# optionally set a global service context to avoid passing it into other objects every time

logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为DEBUG，可以根据需要修改
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# 使用自定义embedding和llm

# 私有化1024维
# embed_model = SparkAIEmbedding(endpoint="172.31.164.103:9980")
# embed_model = SparkAIEmbedding(endpoint="172.31.164.103:9980", domain="emb_v1")
# 私有化2560维
# embed_model = SparkAIEmbedding(endpoint="172.31.164.103:9980", domain="emb_v2")
# 公有云2560维
embed_model = SparkAIEmbedding(endpoint="172.31.164.103:9980", domain="emb_xfyun")

llm = SparkAI(endpoint="172.31.164.103:9980")
service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)

# set_global_service_context(service_context)

# load data
documents = SimpleDirectoryReader("./data").load_data(show_progress=True)

qa_prompt_tmpl_str = (
    "下面是上下文信息.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "根据上下文信息和知识回答问题\n"
    "问题: {query_str}\n"
    "答案: "
)


def simple():
    documents = SimpleDirectoryReader("./data").load_data(show_progress=True)
    index = VectorStoreIndex.from_documents(documents=documents, service_context=service_context)
    query_engine = index.as_query_engine(similarity_top_k=5)
    repsonse = query_engine.query("截止2024年1月，合肥市创建国家卫生城市计划实施步骤进展到什么阶段了？")
    print(repsonse)


def simple_filter():
    for document in documents:
        # 添加自定义metadata
        # if "readme.md" in document.metadata["file_path"]:
        document.metadata["db_name"] = "db1"
        # 默认添加的元数据会 被llm和embed使用
        document.excluded_llm_metadata_keys = ["db_name"]
        document.excluded_embed_metadata_keys = ["db_name"]

    # create index, 默认特征存储在内存中
    index = VectorStoreIndex.from_documents(documents=documents, service_context=service_context)

    # 设置过滤条件
    filters = MetadataFilters(
        filters=[
            MetadataFilter(key="db_name", operator=FilterOperator.EQ, value="db1"),
        ]
    )

    # 指定prompt模版
    qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)

    # query
    query_engine = index.as_query_engine(similarity_top_k=5,
                                         # filters=filters,
                                         # text_qa_template=qa_prompt_tmpl
                                         )
    print("-------")
    # print(query_engine.get_prompts())

    # query_engine.update_prompts({"response_synthesizer:text_qa_template": qa_prompt_tmpl})

    response = query_engine.query("时间参量测试C相测试结果49.4ms是否符合技术要求")

    print(response)


def post_processor():
    postprocessor = KeywordNodePostprocessor(
        # 包含哪些关键词
        required_keywords=["声纹"],
        # 排除那些关键词
        exclude_keywords=[],
        lang="zh"
    )

    index = VectorStoreIndex.from_documents(documents=documents, service_context=service_context)
    query_engine = index.as_query_engine(
        node_postprocessors=[postprocessor]
    )
    response = query_engine.query("swk需要部署elasticsearch吗")
    print(response)


def graph():
    # 知识图谱索引, 针对chunk 调用大模型提取实体关系
    graph_store = SimpleGraphStore()
    storage_context = StorageContext.from_defaults(graph_store=graph_store)

    # NOTE: can take a while!
    index = KnowledgeGraphIndex.from_documents(
        documents,
        max_triplets_per_chunk=2,
        storage_context=storage_context,
        service_context=service_context,
    )

    query_engine = index.as_query_engine(
        include_text=False, response_mode="tree_summarize"
    )
    response = query_engine.query("什么场景下星球服务要安装elasticsearch")
    print(response)


def tree():
    # build index
    index = TreeIndex.from_documents(documents, service_context=service_context, )
    # query
    query_engine = index.as_query_engine()
    response = query_engine.query("半小时时长的语音会比2分钟时长的语音，提取的声纹效果好吗？")
    print(response)


if __name__ == '__main__':
    # simple()
    # graph()
    # tree()
    # post_processor()
    # print(llm.chat(messages=[ChatMessage.from_str(content='明天天气怎么样？', role=MessageRole.USER)]))
    chat = llm.stream_chat(messages=[ChatMessage.from_str(content='我的名字叫姚明，但是我不会打篮球', role=MessageRole.USER),
                                     ChatMessage.from_str(content='你好姚明！我能帮你做些什么', role=MessageRole.ASSISTANT),
                                     ChatMessage.from_str(content='你知道我的名字吗？', role=MessageRole.USER), ])
    for item in chat:
        print(item)
