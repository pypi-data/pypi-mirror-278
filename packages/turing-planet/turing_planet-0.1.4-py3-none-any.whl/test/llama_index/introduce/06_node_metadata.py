from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Document
from llama_index.core.extractors import TitleExtractor, QuestionsAnsweredExtractor
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter

from introduce_base import storage_context, vector_filter_key
from test.llama_index.optimizing.custom_keyword_extractor import MyKeywordExtractor
from turing_planet.llama_index.llms.sparkai import SparkAI

TEXT = """七、资金筹集及拨付
（一）资金筹集。
政府购买居家养老服务所需资金由市、区（开发区）财政按1：1比例分担。
（二）资金拨付。
政府购买居家养老服务市级资金实行年初分区预拨制度，市民政局于年初根据上年度服务对象人数及变化趋势、服务资金结算等情况确定当年预拨金额，由市财政局负责拨付。
（三）资金结算。
政府购买居家养老服务资金结算由各区（开发区）财政部门负责。
八、其他事项
1．各县（市）政府购买居家养老服务工作，可结合本地实际参照本方案执行；继续优化实施农村低收入老年人养老服务补贴制度。
2．本方案自印发之日起满30日后施行，有效期5年。《合肥市政府购买居家养老服务实施方案》（合民〔2017〕136号）、《合肥市居家养老服务标准服务流程及服务收费参考意见》（合民〔2014〕105号）同时废止。"""

# 提取每个节点上下文的标题，关联节点数5
title_extractor = TitleExtractor(nodes=5)

QA_PROMPT_TEMPLATE = """
以下是上下文:
{context_str}


根据给定的上下信息，生成此上下文可以回答的{num_questions}个问题。
"""


def qa_metadata():
    text_splitter = SentenceSplitter(
        chunk_size=4096,
        chunk_overlap=20,
    )
    #  提取每个节点可以回答的2组问题
    extractor = QuestionsAnsweredExtractor(questions=2, prompt_template=QA_PROMPT_TEMPLATE)
    transformations = [text_splitter, extractor]
    pipeline = IngestionPipeline(transformations=transformations)
    documents = [Document(text=TEXT)]
    nodes = pipeline.run(documents=documents)
    print(nodes)


# 自动抽取元数据
def keywords_metadata():
    extractor = MyKeywordExtractor(llm=SparkAI(), keywords=3)

    documents = (SimpleDirectoryReader(input_files=["../data/合政〔2022〕176号.docx"]).load_data(show_progress=True))

    # 添加自定义metadata
    for document in documents:
        document.metadata[vector_filter_key] = "hf"
        # 默认添加的元数据会 被llm和embed使用
        document.excluded_llm_metadata_keys = [vector_filter_key]
        document.excluded_embed_metadata_keys = [vector_filter_key]

    # 创建索引
    VectorStoreIndex.from_documents(documents=documents,
                                    storage_context=storage_context,
                                    transformations=[
                                        SentenceSplitter(chunk_size=2048),
                                        extractor
                                    ], )


if __name__ == '__main__':
    keywords_metadata()
    # qa_metadata()
