from typing import List, Optional

from llama_index.core import VectorStoreIndex
from llama_index.core.postprocessor import KeywordNodePostprocessor
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore, QueryBundle

from pydantic.v1 import PrivateAttr

from test.llama_index.introduce.introduce_base import redis_store


def post_processor():
    keyword_postprocessor = KeywordNodePostprocessor(
        # 包含哪些关键词
        required_keywords=[""],
        # 排除那些关键词
        exclude_keywords=["合肥"],
        lang="zh"
    )

    index = VectorStoreIndex.from_vector_store(vector_store=redis_store)

    query_engine = index.as_query_engine(
        node_postprocessors=[keyword_postprocessor]
    )

    response = query_engine.query("截止2024年1月，合肥市创建国家卫生城市计划实施步骤进展到什么阶段了？ ")
    print(response)


class CustomLLMRerank(BaseNodePostprocessor):
    # _combine_retriever = None
    # _response_synthesizer = None

    _format_node_batch_fn: str = PrivateAttr()

    def __init__(self, top_n: str):
        self._format_node_batch_fn = top_n

    def _postprocess_nodes(self, nodes: List[NodeWithScore], query_bundle: Optional[QueryBundle] = None) -> (
            List)[NodeWithScore]:
        return nodes

    @classmethod
    def class_name(cls) -> str:
        return "CustomLLMRerank"

    # def set_combine_retriever(self, combine_retriever):
    #     self._combine_retriever = combine_retriever
    #
    # def set_response_synthesizer(self, response_synthesizer):
    #     self._response_synthesizer = response_synthesizer


if __name__ == '__main__':
    llm_rerank = CustomLLMRerank(top_n=111)
    print(llm_rerank._format_node_batch_fn)

    # post_processor()
