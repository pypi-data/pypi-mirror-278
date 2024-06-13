import logging

from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader

from test.llama_index.introduce.introduce_base import vector_filter_key

# 加载环境变量
load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为DEBUG，可以根据需要修改
    format="%(asctime)s - %(levelname)s - %(message)s",
)

if __name__ == '__main__':
    # 加载数据
    documents = SimpleDirectoryReader("../data").load_data(show_progress=True)

    # 添加自定义metadata
    for document in documents:
        document.metadata[vector_filter_key] = "hf"
        # 默认添加的元数据会 被llm和embed使用
        document.excluded_llm_metadata_keys = [vector_filter_key]
        document.excluded_embed_metadata_keys = [vector_filter_key]

    for key, value in documents[0].metadata.items():
        print(f"{key}   --  {value}")
