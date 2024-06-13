from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

import logging
from langchain.prompts import PromptTemplate
from langchain.chains import LLMRequestsChain, LLMChain
from turing_planet.langchain.llm.sparkai import SparkAI

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为DEBUG，可以根据需要修改
    format="%(asctime)s - %(levelname)s - %(message)s",
    # filename='spark.log',  # 指定日志文件的名称
)

# spark = SparkAI(endpoint="172.31.164.103:9980", domain="xfyun-generalv3.5")
spark = SparkAI(endpoint="172.31.164.103:9980")


def sample_invoke():
    logging.info(spark.invoke("讲个笑话，主题是小花猫"))


def sample_stream():
    for chunk in spark.stream("讲个笑话，主题是小花猫"):
        logging.info(chunk)


def sample_batch():
    result = spark.batch(
        [
            "讲个笑话，主题是小花猫",
            "世界上人口最多的国家是哪个？"
        ]
    )
    for res in result:
        logging.info(res)


def sample_chain():
    template = """在 >>> 和 <<< 之间是网页的返回的HTML内容。
    网页是新浪财经A股上市公司的公司简介。
    请抽取参数请求的信息。

    >>> {requests_result} <<<
    请使用如下的JSON格式返回数据
    {{
      "company_name":"a",
      "company_english_name":"b",
      "issue_price":"c",
      "date_of_establishment":"d",
      "registered_capital":"e",
      "office_address":"f",
      "Company_profile":"g"

    }}
    """

    prompt = PromptTemplate(input_variables=["requests_result"], template=template)

    chain = LLMRequestsChain(llm_chain=LLMChain(llm=spark, prompt=prompt))
    inputs = {
        "url": "https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/600519.phtml"
    }

    response = chain(inputs)
    logging.info(response["output"])


if __name__ == "__main__":
    print("=============== sample_invoke ==============")
    sample_invoke()

    print("=============== sample_stream ==============")
    # sample_stream()

    # print("=============== sample_batch ==============")
    # sample_batch()

    # print("=============== sample_chain ==============")
    # sample_chain()
