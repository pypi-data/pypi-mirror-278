from turing_planet.langchain.llm.sparkai import SparkAI

SLOT_PROMPT_TEMPL = """
## 任务描述

假设你是一个结构化信息提取助手，能够准确的从用户交互历史中提取出结构化的参数信息，最终以 JSON 形式输出。

## 要求

1. 给定技能信息，从用户交互历史中提取出参数；
2. 如果无法提取出参数，直接填写空值；
3. 注意每个参数的类型，保证提取出的参数类型和技能信息一致；
4. 直接生成 JSON 结果，严格按照样例的结构输出。

## 输出要求

请以 JSON 格式输出提取结果，提取结果中要包含技能信息中的所有参数，如果某个参数提取失败，参数值为空。

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

用户：查询明天南京夫子庙附近，价格大概300以内的酒店

系统：
```
{
    "location": "南京夫子庙",
    "date": "明天",
    "price":"300以内"
}
```

## 交互历史

系统：请问您想查询北京哪一天和哪个价格区间的酒店？

用户：300左右

系统：请问您想查询北京哪一天和价格区间300左右的酒店？


## 当前问题

{{question}}

## 任务重述

请参照样例，将用户当前的问题，提取技能中所有的参数，并以严格以JSON 形式输出：
"""

if __name__ == '__main__':
    # 追问，抽槽补充场景

    prompt = SLOT_PROMPT_TEMPL.replace("{{question}}", "下周一")

    print("===prompt===\n", prompt)
    spark = SparkAI(endpoint="172.31.164.103:9980")
    spark.temperature = 0

    print("===answer===")
    print(spark.invoke(prompt))
