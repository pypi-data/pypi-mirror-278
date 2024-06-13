from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, SummaryIndex
from llama_index.core.output_parsers import selection
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool

from test.llama_index.introduce.introduce_base import redis_store

# 路由查询引擎

# 默认的prompt 的模版，导致星火大模型返回的json是非法的无法解析
selection.FORMAT_STR = """The output should be ONLY JSON formatted as a JSON instance.

Here is an example:
[
    {
        choice: 1,
        reason: "<insert reason for choice>"
    },
]
"""

if __name__ == '__main__':
    # load data
    documents = SimpleDirectoryReader("../data").load_data(show_progress=True)

    #  define index
    vector_index = VectorStoreIndex.from_vector_store(vector_store=redis_store)

    summary_index = SummaryIndex.from_documents(documents=documents)

    #  define query engine tool
    vector_engine = vector_index.as_query_engine()
    summary_engine = summary_index.as_query_engine()

    vector_tool = QueryEngineTool.from_defaults(query_engine=vector_engine,
                                                description="Useful for retrieving specific context")
    summary_tool = QueryEngineTool.from_defaults(query_engine=summary_engine,
                                                 description="Useful for summarization questions")

    #  define router query engine
    """
    第一步：请求LLM 选择 tool
    prompt：
        Some choices are given below. It is provided in a numbered list (1 to 2), 
        where each item in the list corresponds to a summary.
        ---------------------
        (1) Useful for retrieving specific context
        
        (2) Useful for summarization questions
        ---------------------
        Using only the choices above and not prior knowledge, return the choice that is most relevant to the question: '注册和重新注册接口有什么区别'
        
        
        The output should be ONLY JSON formatted as a JSON instance.
        
        Here is an example:
        [
            {{
                    choice: 1,
                    reason: "<insert reason for choice>"
            }},
            ...
        ]
    
    answer:
        [{
                "choice": 1,
                "reason": "注册和重新注册接口的区别是，重新注册接口通常用于用户在现有账户出现问题时进行修复或更新，而注册接口则用于新用户的创建。"
        }]
    
    第二部：根据choice选择tool，执行tool
        1) 如果是LLMSingleSelector，选择一个索引查询器完成问答
        2） 如果是 LLMMultiSelector，选择其中多个索引查询器，将检索到的结果合并，再次调用LLM（QA），得到最终结果
    
    """
    query_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        # selector=LLMMultiSelector.from_defaults(service_context=service_context),
        query_engine_tools=[vector_tool, summary_tool],
    )

    #   query
    response = query_engine.query("简要总结下合肥市创建国家卫生城市三年行动计划通知的主要内容？")
    print(response)
