from langchain.prompts import PromptTemplate

from turing_planet.langchain.llm.sparkai import SparkAI

# 抽槽

SLOT_PROMPT_TEMPL = """
"""

# SYSTEM_MESSAGE_PREFIX = """Answer the following questions as best you can. You have access to the following tools:"""
FORMAT_INSTRUCTIONS = """
尽你所能回答以下问题。您可以访问以下工具：

{tools_schema}

使用这些工具的方法是指定一个json BLOB。
具体地说，这个json应该有一个`action`键(带有要使用的工具的名称)和一个`action_input`键(工具的输入在这里)。

“action”字段中应该包含的唯一值是: {tool_names}

$JSON_BLOB应该只包含一个操作，而不是返回多个操作的列表。以下是有效的$JSON_BLOB的示例：

```
{{{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}}}
```


始终使用以下格式：

Question: 您必须回答的输入问题
Thought: 你应该时刻思考该做什么
Action:
```
$JSON_BLOB
```
... (这个 Thought/Action 可以重复 N 次)


用户问题：
{input}

开始! 

"""
# SYSTEM_MESSAGE_SUFFIX = """Begin! Reminder to always use the exact characters `Final Answer` when responding."""
# HUMAN_MESSAGE = "{input}\n\n{agent_scratchpad}"

tools_schema = [
    {
        "tool_name": "预定酒店",
        "tools_descript": "根据时间、地点、价格、可以查询当地可以入住的酒店",
        "parameters": {
            "title": "预定酒店工具所需要的输入数据",
            "properties": {
                "date": {
                    "title": "时间",
                    "type": "string"
                },
                "location": {
                    "title": "地点",
                    "type": "string"
                },
                "price": {
                    "title": "价格",
                    "type": "float"
                }
            },
            "required": [
                "date",
                "location"
            ]
        },
    },
    {
        "tool_name": "车票机票查询",
        "tools_descript": "根据时间、出发地城市、目的地城市名称，可以查询火车，高铁，飞机票务情况",
        "parameters": {
            "title": "车票机票查询工具所需要的输入数据",
            "properties": {
                "date": {
                    "title": "时间",
                    "type": "string"
                },
                "start_city": {
                    "title": "出发地城市",
                    "type": "string"
                },
                "end_city": {
                    "title": "目的地城市",
                    "type": "string"
                },
            },
            "required": [
                "date",
                "start_city",
                "end_city"
            ]
        },
    },
    {
        "tool_name": "查询天气",
        "tools_descript": "根据时间、城市名称，可以查询当地的天气",
        "parameters": {
            "title": "预定酒店工具所需要的输入数据",
            "properties": {
                "date": {
                    "title": "时间",
                    "type": "string"
                },
                "city": {
                    "title": "城市名称",
                    "type": "string"
                },
            },
            "required": [
                "date",
                "city"
            ]
        },
    }
]

if __name__ == '__main__':
    prompt_template = PromptTemplate(
        template=FORMAT_INSTRUCTIONS, input_variables=["input"]
    )
    prompt = prompt_template.format(tools_schema=tools_schema,
                                    tool_names=[tool['tool_name'] for tool in tools_schema],
                                    input="我是一名学生，明天我要从合肥去南京夫子庙玩，请帮忙规划行程")

    print("===prompt===\n", prompt)
    spark = SparkAI(endpoint="172.31.164.103:9980")
    spark.temperature = 0

    print("===answer===")
    print(spark.invoke(prompt))
