import logging

import pandas as pd
from llama_index.core import ServiceContext, SimpleDirectoryReader, VectorStoreIndex

from turing_planet.llama_index.embeddings.sparkai import SparkAIEmbedding
from turing_planet.llama_index.llms.sparkai import SparkAI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
# DEFAULT_CONTEXT_WINDOW = 200
# DEFAULT_FILE_READER_CLS.update({".xlsx": ExcelSummaryReader, ".xls": ExcelSummaryReader})
excel_file_path = "/Users/wujian/Downloads/30/know/execl/银行/产品表/合肥科技农村商业银行产品介绍.xlsx"
# /Users/wujian/Downloads/30/know/execl/银行/产品表/合肥科技农村商业银行产品介绍-.xlsx
# /Users/wujian/Downloads/30/know/execl/银行/产品表/徽商银行-.xlsx
# /Users/wujian/Downloads/30/know/execl/报表/企业财务报表1.xlsx

# /Users/wujian/Downloads/30/query/execl/银行/产品表/中国银行理财产品.xlsx


def excel_to_markdown(excel_file, sheet_name=0, output_file="output.md"):
    # 读取 Excel 文件
    df = pd.read_excel(excel_file, sheet_name, dtype=str)

    # 将 DataFrame 转换为 Markdown 格式
    markdown_table = df.to_markdown(index=False)

    # 将 Markdown 表格写入文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"{markdown_table}")

    print(f"成功将 Excel 文件转换为 Markdown 并保存到 {output_file} 中。")


def query():
    endpoint = "172.31.164.103:9980"
    # 使用自定义embedding和llm
    embed_model = SparkAIEmbedding(endpoint=endpoint, domain="emb_v1")
    llm = SparkAI(endpoint=endpoint)
    service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm, chunk_size=7900)
    # service_context.prompt_helper.context_window = 200

    # 加载数据
    documents = SimpleDirectoryReader(input_files=[
        # "/Users/wujian/workspace/code/llm/turing-planet/turing-planet/test/llama_index/pk/output.md"
        excel_file_path
    ]).load_data(show_progress=True)

    # 创建索引
    index = VectorStoreIndex.from_documents(documents=documents, service_context=service_context)

    # 创建查询引擎
    query_engine = index.as_query_engine(similarity_top_k=5)

    # 执行查询
    questions = [
        "查询讯飞2019年中流动资产和非流动资产相比，哪个数值更大？",
        # "讯飞2019年应收账款与2020年相比增长了多少?",
        # "讯飞公司在2018年资产构成中流动资产占多少?",
        # "20年公开的讯飞无形资产数值是多少?",
        # "讯飞2020年货币资金占比是多少?",
        # "作为一个合肥人，我想知道讯飞在总资产中，哪个年份占比增长幅度最大？",
        # "讯飞2019年流动资产占比2018年提高了还是降低了?",
        # "2018年中应收账款和存货相比谁更多?",
        # "2019年科大讯的货币资金占比是多少?",
        # "2019年公布的讯飞的资产中商誉数值是多少?",
        # "公布的讯飞的资产报表中哪个项目的占比最高？",
        # "科大讯飞在2018年固定资产数值是多少?",
        # "2018年讯飞的流动资产和非流动资产中，哪个部分占比更大？",
        # "请问你知道科大讯飞在2018年应收账款数值是多少?",
        # "2019年讯飞的固定资产数值是多少?",
    ]
    for question in questions:
        response = query_engine.query(
            question + "\n\n当用户的问题涉及推理和计算方面时，请认真思考并逐步进行推理，然后用中文回答。")
        print(f"question === {question}")
        print(response)
        print("---------")


if __name__ == '__main__':
    # 示例用法
    # excel_to_markdown(excel_file=excel_file_path)
    query()
