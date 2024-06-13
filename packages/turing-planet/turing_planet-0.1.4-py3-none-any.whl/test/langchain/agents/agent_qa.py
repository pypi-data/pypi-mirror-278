from turing_planet.langchain.llm.sparkai import SparkAI

ASK_PROMPT_TEMPL = """

## 任务描述

假设你是一个智能客服助手，根据技能执行过程和交互历史，回答用户的问题。

## 要求

1. 回答的内容需要包含技能执行过程的每一步结果，且必须按照技能执行的顺序回答；
2. 基于技能执行过程，需要再最后一个段落给出总结性阐述，要求语言自然，具有亲和力。


## 技能执行过程
{{tools_result}}


## 交互历史

{{history}}


## 用户问题

{{question}}


"""

if __name__ == '__main__':
    tools_result = """
    技能1：
    查询明天南京的天气
    回答：
    南京明天多云转晴，最低气温15摄氏度，最高气温21摄氏度，东南风3级
    
    技能2：
    查询明天合肥到南京的车票
    回答：
    明天合肥到南京有动车和高铁列车共14趟，其中8趟列车现二等座余票充足，分别为上午8趟，下午2趟
    
    技能3：
    查询明天南京夫子附近的酒店
    查询明天南京酒店信息如下：400元以内标准间共有5间，500~800之间大床房共有10间
    """

    history = """
    用户：
    明天到南京夫子庙逛逛，从合肥出发，帮我制定行程规划
    
    系统：
    请问你的出发地点是哪里？
    
    """

    query = "合肥"

    prompt = ASK_PROMPT_TEMPL.replace("{{tools_result}}", tools_result).replace("{{question}}", str(query))

    print("===prompt===\n", prompt)
    spark = SparkAI(endpoint="172.31.164.103:9980")
    spark.temperature = 0

    print("===answer===")
    print(spark.invoke(prompt))
