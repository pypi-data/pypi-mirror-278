import logging

from dotenv import load_dotenv
from llama_index.core import ServiceContext, SimpleDirectoryReader, VectorStoreIndex, StorageContext, PromptTemplate, \
    Document
from llama_index.core.extractors import TitleExtractor, QuestionsAnsweredExtractor, SummaryExtractor
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter, SentenceSplitter

from test.llama_index.optimizing.custom_keyword_extractor import MyKeywordExtractor
from turing_planet.llama_index.embeddings.sparkai import SparkAIEmbedding
from turing_planet.llama_index.llms.sparkai import SparkAI
from turing_planet.llama_index.vector_stores.planet import PlanetVectorStore

# 加载环境变量
load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为DEBUG，可以根据需要修改
    format="%(asctime)s - %(levelname)s - %(message)s",
)

summary_prompt_template = """\
这是本节的内容:
{context_str}

总结本节的主要主题和实体。 \

总结: """

qa_prompt_tmpl_str = (
    "下面是上下文信息.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "根据上下文信息和知识回答问题\n"
    "问题: {query_str}\n"
    "答案: "
)

embed_model = SparkAIEmbedding(domain="emb_v1")
llm = SparkAI()
planet_store = PlanetVectorStore(index_name="llama-index");
storage_context = StorageContext.from_defaults(vector_store=planet_store, )
service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)

text_splitter = TokenTextSplitter(
    separator=" ", chunk_size=512, chunk_overlap=128
)

# 提取每个节点上下文的标题，关联节点数5
title_extractor = TitleExtractor(nodes=5, llm=llm)

#  提取每个节点可以回答的3组问题
qa_extractor = QuestionsAnsweredExtractor(questions=3, llm=llm)

# 提取摘要
summary_extractor = SummaryExtractor(summaries=['self', 'prev', 'next'], llm=llm,
                                     prompt_template=summary_prompt_template)

qa_service_context = ServiceContext.from_defaults(
    embed_model=embed_model,
    llm=llm,
    transformations=[
        qa_extractor
    ]
)

extractor_service_context = ServiceContext.from_defaults(
    embed_model=embed_model,
    llm=llm,
    transformations=[
        SentenceSplitter(),
        summary_extractor
    ]
)


def load_documents():
    simple_reader = SimpleDirectoryReader(
        input_dir="/Users/wujian/Downloads/skynet-doc-center_1",
        recursive=True,
        exclude=[".git"],
        required_exts=[".pdf", ".docx", ".txt", ".md", ".ppt", ".pptm", ".ppt"]
    )
    return simple_reader.load_data(show_progress=True)


# 自动抽取元数据
def extract_metadata():
    documents = SimpleDirectoryReader("./data").load_data(show_progress=True)
    index = VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context,
                                            service_context=extractor_service_context)
    query_engine = index.as_query_engine(similarity_top_k=1, text_qa_template=PromptTemplate(qa_prompt_tmpl_str))
    response = query_engine.query("swk需要安装elasticsearch吗")
    print(response)


def compare_qa_metadata():
    questions = {"ogma服务发现配置项是哪个？",
                 "yama内置参数转换器有哪些？",
                 "skynet托管平台最新发布的版本是哪个？",
                 "图聆网关支持哪几种服务发现方式？"}

    print("====只使用chunk embedding=====")
    query(questions, service_context)

    print("====使用问题抽取=====")
    query(questions, qa_service_context)


def query(questions, _service_context):
    _index = VectorStoreIndex.from_documents(documents=load_documents(), service_context=_service_context)
    _query_engine = _index.as_query_engine(similarity_top_k=1)
    for question in questions:
        response = _query_engine.query(question)
        print(f"{question}\n{response}")


def keywords_metadata():
    text_splitter = SentenceSplitter(
        chunk_size=4096,
        chunk_overlap=20,
    )
    extractor = MyKeywordExtractor(llm=SparkAI(), keywords=3)
    transformations = [text_splitter, extractor]
    pipeline = IngestionPipeline(transformations=transformations)
    documents = [Document(
        text="""七、资金筹集及拨付
（一）资金筹集。
政府购买居家养老服务所需资金由市、区（开发区）财政按1：1比例分担。
（二）资金拨付。
政府购买居家养老服务市级资金实行年初分区预拨制度，市民政局于年初根据上年度服务对象人数及变化趋势、服务资金结算等情况确定当年预拨金额，由市财政局负责拨付。
（三）资金结算。
政府购买居家养老服务资金结算由各区（开发区）财政部门负责。
八、其他事项
1．各县（市）政府购买居家养老服务工作，可结合本地实际参照本方案执行；继续优化实施农村低收入老年人养老服务补贴制度。
2．本方案自印发之日起满30日后施行，有效期5年。《合肥市政府购买居家养老服务实施方案》（合民〔2017〕136号）、《合肥市居家养老服务标准服务流程及服务收费参考意见》（合民〔2014〕105号）同时废止。""")]
    nodes = pipeline.run(documents=documents)
    print(nodes)


if __name__ == '__main__':
    # compare_qa_metadata()
    keywords_metadata()
