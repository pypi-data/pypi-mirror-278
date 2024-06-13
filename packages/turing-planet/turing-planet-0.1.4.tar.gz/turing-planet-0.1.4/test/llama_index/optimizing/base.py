"""
Q: 合肥市政府购买居家养老服务服务对象以及服务标准
A: 服务对象：具有合肥市市区户籍且常住的70周岁以上（含70周岁，下同）低保老年人、70周岁以上空巢（无子女）老年人、90周岁以上高龄老年人，可根据实际需求自愿申请政府购买居家养老服务（流程详见附件1）。
政府购买居家养老服务对象实行动态管理，服务对象去世或者相关条件变化不符合要求时，区（开发区）、街道（乡镇）、社区（村）应及时核减、停止相关服务。
服务标准：服务对象每月可享受市值600元的政府购买居家养老服务补贴。

Q: 阐述合肥市“菜篮子”市长负责制的指导思想和总体目标。
A: 以习近平新时代中国特色社会主义思想为指导，深入贯彻落实习近平总书记重要指示精神，按照党中央、国务院和省委、省政府决策部署，全面落实“菜篮子”市长负责制。
围绕“三保一稳”（即保供给数量、保质量安全、保民生底线，稳定市场供应价格）工作目标，进一步增强以猪肉为重点的“菜篮子”产品自给能力，构建便捷有序的市场流通体系，健全绿色生态的农产品质量安全监管体系，完善稳定的“菜篮子”产品市场调控机制，提高我市“菜篮子”产品综合保障能力。

Q: 合肥市城镇老旧小区改造提升工作实施意见的指导思想和工作目标是什么
A: （一）指导思想。以习近平新时代中国特色社会主义思想为指导，坚持以人民为中心的发展思想，按照高质量发展要求，从改善人居环境入手，拓展创新政府引导、市场运作的可持续改造模式，健全共建共治共享机制，让人民群众生活更方便、更舒心、更美好。
（二）工作目标。编制老旧小区改造规划，滚动推进实施。2023年底前，力争基本实现2000年以前建成投入使用的老旧小区改造和管理服务“双提升”；自2024年起，按照“成熟一个，改造提升一个”的要求，持续推进老旧小区改造，形成改造提升的长效机制。

Q: 合肥市居民医保集中参保期以及待遇享受期
A: 居民医保集中参保期为每年9月1日至12月31日，待遇享受期为次年1月1日至12月31日。

Q: 合肥市火灾事故应急预案专家组的构成以及相应的职责
A: 由消防救援支队聘请应急管理、公安、城市轨道交通、安全生产、质量监督、卫生防疫、防化、地震、反恐、防爆、电力、建筑、气象、压力容器等方面的专家组成。其职责如下：
（1）参加市火灾事故应急指挥部组织的活动及专题研究。
（2）对火灾事故的监测、预防预警、应急准备、应急处置、应急结束、事件影响评估等提供技术支持，为领导决策提供依据。
（3）参与事件调查，提供意见和建议。

Q: 火灾分为哪几种情形以及对应的处理单位
A: 一般火灾事故由事故发生地县（市、区）级人民政府（含开发区管委会，下同）负责组织调查处理。较大火灾事故由市人民政府负责组织调查处理。重大火灾事故或特别重大火灾事故，根据国家规定由事故发生地人民政府全力配合省级人民政府调查组或国务院调查组做好调查处理工作。

Q: 合肥市既有住宅加装电梯工作基本原则以及实施的条件
A: 基本原则：既有住宅加装电梯工作坚持“业主自主、社区主导、政府扶持、各方支持”的原则。
实施条件：（一）具有合法的房屋权属证明；
（二）5年内未列入棚户区（危旧房）、城中村改造范围和计划；
（三）已建成投入使用的4层以上（含4层）无电梯住宅；
（四）满足建筑物结构安全、消防安全等有关规范要求。
"""
from typing import Optional, List

from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, ServiceContext, Settings
from llama_index.core.extractors import QuestionsAnsweredExtractor, SummaryExtractor
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import TransformComponent
from llama_index.vector_stores.redis import RedisVectorStore
from redis import Redis
from redisvl.schema import IndexSchema

from turing_planet.llama_index.embeddings.sparkai import SparkAIEmbedding
from turing_planet.llama_index.llms.sparkai import SparkAI

user_questions = ["合肥市政府购买居家养老服务服务对象以及服务标准",
                  "阐述合肥市“菜篮子”市长负责制的指导思想和总体目标。",
                  "合肥市城镇老旧小区改造提升工作实施意见的指导思想和工作目标是什么",
                  "合肥市居民医保集中参保期以及待遇享受期",
                  "合肥市火灾事故应急预案专家组的构成以及相应的职责",
                  "火灾分为哪几种情形以及对应的处理单位",
                  "合肥市既有住宅加装电梯工作基本原则以及实施的条件"
                  ]

load_dotenv()

dims = 2560
endpoint = "172.31.164.103:9980"
Settings.llm = SparkAI(endpoint=endpoint)
Settings.embed_model = SparkAIEmbedding(endpoint=endpoint, domain="emb_xfyun")
Settings.chunk_size = 1024

splitter = SentenceSplitter(
    chunk_size=1024,
    chunk_overlap=20,
)

summary_prompt_template = """\
 这是本节的内容:
 {context_str}

 总结本节的主要主题和实体。 \

 总结: """
extractor = SummaryExtractor(summaries=["prev", "self"], prompt_template=summary_prompt_template)


def load_documents():
    simple_reader = SimpleDirectoryReader(input_dir="../../../doc/合肥市政府公文")
    documents = simple_reader.load_data(show_progress=True)
    return documents


def build_vector_store(index_name: str) -> RedisVectorStore:
    redis_index_schema = IndexSchema.from_dict(
        {
            # customize basic index specs
            "index": {
                "name": index_name,
                "prefix": f"{index_name}_vector",
                "key_separator": ":",
            },
            # customize fields that are indexed
            "fields": [
                {"name": "id", "type": "tag"},
                {"name": "doc_id", "type": "tag"},
                {"name": "text", "type": "text"},
                {"name": "vector", "type": "vector",
                 "attrs": {"dims": 2560, "algorithm": "flat", "distance_metric": "cosine", }},
            ],
        }
    )

    redis_client = Redis.from_url("redis://172.31.128.153:6379")
    return RedisVectorStore(schema=redis_index_schema, redis_client=redis_client, overwrite=False)


def add_vector_index(index_name: str, chunk_size: int = 2048):
    Settings.chunk_size = chunk_size
    add_vector_index(index_name=index_name)


def add_vector_index(index_name: str, transformations: Optional[List[TransformComponent]] = None):
    storage_context = StorageContext.from_defaults(vector_store=build_vector_store(index_name))
    VectorStoreIndex.from_documents(documents=load_documents(),
                                    storage_context=storage_context,
                                    show_progress=True,
                                    transformations=transformations)


def query(index_name: str, top_k: int = 1):
    index = VectorStoreIndex.from_vector_store(vector_store=build_vector_store(index_name))
    query_engine = index.as_query_engine(similarity_top_k=top_k)
    for question in user_questions:
        response = query_engine.query(question + "\nResponse in Chinese")
        print(f"Q:{question}")
        print("A:" + response.response.replace("<ret>", "\n").replace("<end>", "\n"))
        # print(f"source:{response.source_nodes[0].text}")
        print("---------------\n")
