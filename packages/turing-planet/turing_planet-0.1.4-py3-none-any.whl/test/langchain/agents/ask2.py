from turing_planet.langchain.llm.sparkai import SparkAI

ASK_PROMPT_TEMPL = """

## 任务描述

假设你是一个智能追问助手，根据技能信息和一个 JSON 对象判断哪些参数是未知的，向用户追问，让用户回答这些未知的参数。

## 要求

1. 给定技能信息，从技能信息中提取出技能所需的参数；
2. 从 JSON 对象中判断哪些参数是未知的，也就是空值，对于这些未知的参数，以自然语言的形式向用户追问，保证你的问题让用户回答出这些未知的参数。

## 技能信息

{
    "name": "酒店查询",
    "description": "根据行程目的地、日期、价格区间、查询当地合适酒店",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "行程目的地，比如北京。"
            },
            "date": {
                "type": "string",
                "description": "日期。"
            },
            "price": {
                "type": "string",
                "description": "价格区间。"
            }
        },
        "required": [
            "location", "date"， "price"
        ]
    }
}



## 样例

用户：
{
    "age": "合肥",
    "date": ""
}
系统：请问您想查询合肥哪天的天气？

## 用户JSON对象

{{question}}

## 任务重述

请参照样例，从 JSON 对象中判断哪些参数是未知的，对于这些未知的参数，以自然语言的形式向用户追问。

系统：

"""

if __name__ == '__main__':
    query = {
        "location": "南京",
        "date": "",
        "price": ""
    }

    prompt = ASK_PROMPT_TEMPL.replace("{{question}}", str(query))

    print("===prompt===\n", prompt)
    spark = SparkAI(endpoint="172.31.164.103:9980")
    spark.temperature = 0

    print("===answer===")
    print(spark.invoke(prompt))
