"""
 自定义查询
 1. 用户问题 --> 向量召回TopK=3, --> vector_nodes
 2. 用户问题抽取关键词 和 给定的关键词列表（向量召回，返回的metadata keywords），通过LLM， 判断相似度
 3. 取相似度最高top1，调用 LLM

"""
from typing import List

from llama_index.core import QueryBundle, VectorStoreIndex, get_response_synthesizer
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.indices.vector_store import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.schema import NodeWithScore
from llama_index.core.settings import Settings

from test.llama_index.introduce.introduce_base import redis_store

from turing_planet.llama_index.llms.sparkai import SparkAI

prompt_template = """
  根据用户的关键词，选择出给定的上下文关键词列表中最匹配的关键词，地点名称不作为关键词。
  要求只返回一个序号数字，不知道就返回0
  上下文关键词列表：
  {context_str}

  用户的关键词：
  {keywords}

  """

question_keywords_prompt_template = """
根据提供的上下文，提取出关键词，
要求地点名称不作为关键词。
上下文：
{context_str}
"""


# 向量检索重排检索器
class VectorReRankRetriever(BaseRetriever):
    def __init__(self, vector_retriever: VectorIndexRetriever, ):
        self._vector_retriever = vector_retriever
        super().__init__()

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        # 1. 向量检索，选取topN重排集合
        vector_nodes = self._vector_retriever.retrieve(query_bundle)
        if len(vector_nodes) <= 1:
            return vector_nodes

        # 2. 选取待选node的关键词
        keyword_context = ""
        for i, vector_node in enumerate(vector_nodes):
            keyword_context = keyword_context + f"{i} <--> {vector_node.metadata.get('excerpt_keywords')}\n"

        # 3. 获取用户问题关键词
        q_keywords_prompt = question_keywords_prompt_template.replace("{context_str}", query_bundle.query_str)
        question_keywords = Settings.llm.complete(q_keywords_prompt).text
        print(f"===提取用户问题关键词\n问题：{q_keywords_prompt}\n用户关键词结果：{question_keywords}")

        # 4. 选取和用户关键词最匹配的待选node
        prompt = prompt_template.replace("{context_str}", keyword_context).replace("{keywords}", question_keywords)
        keyword_index = Settings.llm.complete(prompt).text
        print(f"===匹配关键词\n问题：{prompt}\n命中关键词结果：{keyword_index}")
        target_index = 0
        try:
            target_index = int(keyword_index)
        except ValueError:
            print("转换index失败", keyword_index)
        if target_index >= len(vector_nodes):
            print("不正确的node", target_index)
            target_index = 0

        retrieve_nodes = [vector_nodes[target_index]]
        return retrieve_nodes


def query():
    #  向量检索
    #  向量检索
    vector_index = VectorStoreIndex.from_vector_store(vector_store=redis_store)
    vector_retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=3)

    # 向量重排检索
    rerank_retriever = VectorReRankRetriever(vector_retriever=vector_retriever, )
    response_synthesizer = get_response_synthesizer(
        response_mode="refine",
    )

    query_engine = RetrieverQueryEngine(retriever=rerank_retriever, response_synthesizer=response_synthesizer)

    question = "截止2024年1月，合肥市创建国家卫生城市计划实施步骤进展到什么阶段了？"
    response = query_engine.query(question + "\n中文回答")
    print(f"Q:{question}")
    print("A:" + response.response.replace("<ret>", "\n").replace("<end>", "\n"))
    print("---------------\n")


if __name__ == '__main__':
    query()
