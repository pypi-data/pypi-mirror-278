import logging
from typing import Any

from langchain.chains.openai_functions import create_openai_fn_chain
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import HumanMessage, ChatGeneration, AIMessage

from turing_planet.langchain.chat_models.sparkai import ChatSparkAI

# 配置日志记录
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

sparkChat = ChatSparkAI(
    endpoint="172.31.164.103:9980",
)

_FUNCTIONS: Any = [
    {
        "name": "get_weather",
        "description": "天气插件可以提供天气相关信息。你可以提供指定的地点信息、指定的时间点或者时间段信息，来检索诗词库，精准检索到天气信息。",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "地点，比如北京。"
                },
                "date": {
                    "type": "string",
                    "description": "日期。"
                }
            },
            "required": [
                "location"
            ]
        }
    },
    {
        "name": "get_tax",
        "description": "税率查询可以查询某个地方的个人所得税率情况。你可以提供指定的地点信息、指定的时间点，精准检索到所得税率。",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "地点，比如北京。"
                },
                "date": {
                    "type": "string",
                    "description": "日期。"
                }
            },
            "required": [
                "location"
            ]
        }
    }
]


def sample_function_call():
    prompt_tmpl = "{input}"
    prompt_msgs = [
        HumanMessagePromptTemplate.from_template(prompt_tmpl),
    ]
    prompt = ChatPromptTemplate(messages=prompt_msgs)

    chain = create_openai_fn_chain(
        _FUNCTIONS,
        sparkChat,
        prompt,
        output_parser=None,
        verbose=True
    )

    message = HumanMessage(content="今天合肥的天气怎么样")
    response = chain.generate([{"input": message.content}])

    logging.info(response)
    assert isinstance(response.generations[0][0], ChatGeneration)
    assert isinstance(response.generations[0][0].message, AIMessage)


if __name__ == "__main__":
    print("==========sample_function_call===========")
    sample_function_call()

# _FUNCTIONS: Any = [
#     {
#         "name": "format_person_info",
#         "description": (
#             "Output formatter. Should always be used to format your response to the"
#             " user."
#         ),
#         "parameters": {
#             "title": "Person",
#             "description": "Identifying information about a person.",
#             "type": "object",
#             "properties": {
#                 "name": {
#                     "title": "Name",
#                     "description": "The person's name",
#                     "type": "string",
#                 },
#                 "age": {
#                     "title": "Age",
#                     "description": "The person's age",
#                     "type": "integer",
#                 },
#                 "fav_food": {
#                     "title": "Fav Food",
#                     "description": "The person's favorite food",
#                     "type": "string",
#                 },
#             },
#             "required": ["name", "age"],
#         },
#     },
#     {
#         "name": "get_current_temperature",
#         "description": ("Used to get the location's temperature."),
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "location": {
#                     "type": "string",
#                     "description": "city name",
#                 },
#                 "unit": {
#                     "type": "string",
#                     "enum": ["centigrade", "Fahrenheit"],
#                 },
#             },
#             "required": ["location", "unit"],
#         },
#         "responses": {
#             "type": "object",
#             "properties": {
#                 "temperature": {
#                     "type": "integer",
#                     "description": "city temperature",
#                 },
#                 "unit": {
#                     "type": "string",
#                     "enum": ["centigrade", "Fahrenheit"],
#                 },
#             },
#         },
#     },
# ]
