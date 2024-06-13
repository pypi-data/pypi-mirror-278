import logging

from turing_planet.api.spark_chat_client import SparkLLMClient

logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为DEBUG，可以根据需要修改
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def sample():
    client = SparkLLMClient(endpoint="172.31.101.142:9980", trace_id="test")
    # client = SparkLLMClient(trace_id="test")

    # parameter chat配置
    model_kwargs = {
        "chat_id": "b5dac476-dae8-4cc6-b8f6-c7cf9d",
        "domain": "generalv3",
        "max_tokens": 2048,
        "temperature": 0.1,
        "top_k": 1
    }

    kwargs = {
        # function描述
        "functions": [
            {
                "name": "天气查询",
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
                "name": "税率查询",
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
    }

    messages = [
        {"role": "user", "content": "今天合肥的天气怎么样"}
    ]

    client.arun(
        messages=messages,
        model_kwargs=model_kwargs,
        kwargs=kwargs,
        streaming=True,
    )

    for content in client.subscribe():
        if "data" not in content:
            continue
        delta = content["data"]
        yield delta


if __name__ == '__main__':
    for chunk in sample():
        print(chunk)
