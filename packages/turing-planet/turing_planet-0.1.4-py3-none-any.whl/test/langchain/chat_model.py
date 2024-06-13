import os
import sys

sys.path.append(os.getcwd())

import logging

from langchain.schema import (
    AIMessage,
    HumanMessage,

)
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema.messages import AIMessageChunk, SystemMessage
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

from turing_planet.langchain.chat_models.sparkai import ChatSparkAI

# 配置日志记录
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为DEBUG，可以根据需要修改
    format="%(asctime)s - %(levelname)s - %(message)s",
    # filename='spark.log',  # 指定日志文件的名称
)

sparkChat = ChatSparkAI(
    endpoint="172.31.164.103:9980",
    # domain="turing-general"
)


# 设置环境变量 export TURING_PLANET_ENDPOINT=172.31.101.142:9980
# sparkChat = ChatSparkAI()


def sample_llm():
    messages = [
        SystemMessage(
            content="你是一位根据名字测试性格的大师, 根据我提供的姓名进行分析性格特征, 要求有理有据，分析内容积极向上，进行详细的分析解释"),
        HumanMessage(content="孙悟空"),
    ]
    # response = sparkChat.invoke(messages)
    response = sparkChat(messages)
    assert isinstance(response, AIMessage)
    logging.info(response)


def sample_stream():
    # chat = ChatSparkAI(streaming=True)
    sparkChat.streaming = True
    for chunk in sparkChat.stream("一字千金是什么意思？"):
        logging.info(chunk)
        assert isinstance(chunk, AIMessageChunk)
        assert isinstance(chunk.content, str)


def sample_history():
    messages = [
        HumanMessage(content="2022年，GDP产值最高的国家是哪个？"),
        AIMessage(content="目前，全球GDP产值最高的国家是美国 。"),
        HumanMessage(content="比中国多多少呢？"),
    ]
    response = sparkChat(messages)
    assert isinstance(response, AIMessage)
    logging.info(response)


def sample_output_parser():
    # 六脉神剑
    sparkChat.temperature = 0
    response_schemas = [
        ResponseSchema(
            name="name",
            description="person name",
        ),
        ResponseSchema(
            name="age",
            description="person age",
        ),
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template(
                "回答问题.\n{format_instructions}\n{question}"
            )
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions},
    )
    _input = prompt.format_messages(question="张小妞今年6岁了，她有一个15岁的哥哥叫张帅帅")
    output = sparkChat(_input)

    logging.info(output)
    logging.info(output_parser.parse(output.content))


if __name__ == "__main__":
    print("==========sample_llm===========")
    # sample_llm()

    # print("==========sample_stream===========")
    # sample_stream()

    # print("==========sample_history===========")
    # sample_history()

    # print("==========sample_output_parser===========")
    sample_output_parser()
