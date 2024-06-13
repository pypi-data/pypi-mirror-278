import logging
import os
from typing import List

import pandas as pd
from llama_index.core import StorageContext, SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.vector_stores import FilterOperator, MetadataFilters, MetadataFilter
from pydantic.v1 import BaseModel

from test.llama_index.pk.base import build_vector_store
from turing_planet.llama_index.embeddings.sparkai import SparkAIEmbedding
from turing_planet.llama_index.llms.sparkai import SparkAI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# DEFAULT_FILE_READER_CLS.update({".xlsx": ExcelReader, ".xls": ExcelReader})


class Config(BaseModel):
    endpoint: str = "172.31.164.103:9980"
    # model_domain = "general"
    model_domain = "65B"
    emb_domain: str = "emb_v1"
    dims: int = 1024
    # 默认值
    chunk_size: int = 1024
    # 默认值 20
    chunk_overlap: int = 200
    top_k: int = 3
    know_input_dir: str = "/Users/wujian/Downloads/30/know"
    query_input_dir: str = "/Users/wujian/Downloads/30/query"
    answer_input_dir: str = "/Users/wujian/Downloads/30/answer"
    filter_key: str = "dir"


config = Config()
redis_store = build_vector_store(index_name=f"llamaindex-pk-all-{config.emb_domain}", dims=config.dims)

storage_context = StorageContext.from_defaults(vector_store=redis_store)

Settings.llm = SparkAI(endpoint=config.endpoint, domain=config.model_domain, timeout=10000, temperature=0.5)
Settings.embed_model = SparkAIEmbedding(endpoint=config.endpoint, domain=config.emb_domain)
Settings.chunk_size = config.chunk_size
Settings.chunk_overlap = config.chunk_overlap


def find_excel_files():
    file_paths = []
    for root, dirs, files in os.walk(config.query_input_dir):
        for filename in files:
            if filename.lower().endswith(('.xlsx', '.xls')) and not filename.startswith('.~'):
                file_path = os.path.join(root, filename)
                file_paths.append(file_path)

    return file_paths


def read_excel(excel_file_path: str):
    df = pd.read_excel(excel_file_path)
    # 选择要提取的列
    column_name = 'query'
    selected_column = df[column_name]
    output_list = selected_column.tolist()
    print(output_list)
    return output_list


def add_suffix_to_filename(file_path):
    directory, filename = os.path.split(file_path)
    name, extension = os.path.splitext(filename)
    # 在文件名后面添加"_test"
    new_filename = name + "_test" + extension
    # 组合新的文件路径
    new_file_path = os.path.join(directory, new_filename)
    return new_file_path


def save_excel(excel_file_path: str, result: List[str]):
    df = pd.read_excel(excel_file_path)
    df['test_answer'] = result
    save_file_path = excel_file_path.replace(config.query_input_dir, config.answer_input_dir)
    directory, filename = os.path.split(save_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    # save_file_path = add_suffix_to_filename(excel_file_path)
    df.to_excel(save_file_path, index=False)
    print(f'Data updated and written to {save_file_path} \n {result}')


def doc_index():
    documents = SimpleDirectoryReader(
        input_dir=config.know_input_dir,
        recursive=True
    ).load_data()

    for document in documents:
        directory, filename = os.path.split(document.metadata['file_path'])
        document.metadata[config.filter_key] = directory
        # 默认添加的元数据会 被llm和embed使用
        document.excluded_llm_metadata_keys = [config.filter_key]
        document.excluded_embed_metadata_keys = [config.filter_key]

    VectorStoreIndex.from_documents(documents=documents,
                                    storage_context=storage_context,
                                    show_progress=True)


def query():
    index = VectorStoreIndex.from_vector_store(vector_store=redis_store, show_progress=True)
    question_file_list = find_excel_files()
    for excel_file in question_file_list:
        print(f"==== query start: {excel_file}")
        # 设置过滤条件, 找到对应的目录的知识点
        directory, filename = os.path.split(excel_file)
        filters = MetadataFilters(
            filters=[
                MetadataFilter(key=config.filter_key, operator=FilterOperator.EQ,
                               value=directory.replace("query", "know")),
            ]
        )
        query_engine = index.as_query_engine(similarity_top_k=config.top_k, filters=filters)

        result_list = []
        for question in read_excel(excel_file):
            result = query_engine.query(
                question + "\n\n当用户的问题涉及推理和计算方面时，请认真思考并逐步进行推理，然后用中文回答。")  #
            r = result.response.replace("<ret>", "\n").replace("<end>", "")
            result_list.append(r)
            print(f"question: {question}\n answer: {r}\n=== query end === ")
        save_excel(excel_file, result_list)
    print("----- finish-----")


if __name__ == '__main__':
    # doc_index()
    query()
