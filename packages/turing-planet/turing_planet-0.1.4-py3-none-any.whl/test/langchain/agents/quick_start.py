import logging

from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.agents.chat.base import ChatAgent
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import tool

from test.langchain.agents.sparkai_agent import SparkAIFunctionsAgent
from turing_planet.langchain.chat_models.sparkai import ChatSparkAI

# 配置日志记录
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为DEBUG，可以根据需要修改
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@tool
def fake_search_tool(content: str) -> str:
    """Look up things online."""
    print("fake_search_tool: ", content)
    return f"{content}是100.30"


if __name__ == '__main__':
    tools = [fake_search_tool]

    # 构建agent
    # agent = ChatAgent.from_llm_and_tools(llm=ChatSparkAI(), tools=tools)
    agent = SparkAIFunctionsAgent.from_llm_and_tools(llm=ChatSparkAI(), tools=tools)

    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools)

    agent_executor.invoke("查询一下茅台的股价")
