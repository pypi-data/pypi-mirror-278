import logging
import os
from typing import List

import pandas as pd

from llama_index.core import StorageContext, SimpleDirectoryReader, VectorStoreIndex, ServiceContext, PromptTemplate, \
    Settings
from llama_index.core.vector_stores import FilterOperator, MetadataFilters, MetadataFilter
from pydantic.v1 import BaseModel

from test.llama_index.pk.base import build_vector_store
from turing_planet.llama_index.embeddings.sparkai import SparkAIEmbedding
from turing_planet.llama_index.llms.sparkai import SparkAI
from turing_planet.llama_index.readers.file.excel import ExcelReader, ExcelSummaryReader

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# DEFAULT_FILE_READER_CLS.update({".xlsx": ExcelSummaryReader, ".xls": ExcelSummaryReader})


class Config(BaseModel):
    endpoint: str = "172.31.164.103:9980"
    # model_domain = "general"
    model_domain = "65B"
    emb_domain: str = "emb_v1"
    # 默认值
    chunk_size: int = 7000
    context_window: int = 7500
    # 默认值 20
    chunk_overlap: int = 20
    top_k: int = 3
    know_input_dir: str = "/Users/wujian/Downloads/30/know/execl"
    query_input_dir: str = "/Users/wujian/Downloads/30/query/execl"
    answer_input_dir: str = "/Users/wujian/Downloads/30/answer_emb/execl"
    filter_key: str = "dir"


config = Config()
redis_store = build_vector_store(index_name=f"llamaindex-pk-excel-7900cs-{config.emb_domain}", dims=config.dims)

storage_context = StorageContext.from_defaults(vector_store=redis_store)

Settings.llm = SparkAI(endpoint=config.endpoint, domain=config.model_domain, timeout=10000, temperature=0.5)
Settings.embed_model = SparkAIEmbedding(endpoint=config.endpoint, domain=config.emb_domain)
Settings.chunk_size = config.chunk_size
Settings.chunk_overlap = config.chunk_overlap
Settings.context_window = config.context_window


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
    index = VectorStoreIndex.from_vector_store(vector_store=redis_store,
                                               show_progress=True)

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
        retriever = index.as_retriever(similarity_top_k=config.top_k, filters=filters)

        for question in read_excel(excel_file):
            print(f"question: {question}")
            recall_node_list = retriever.retrieve(question)
            node_list = " ; ".join([recall_node.metadata['file_name'] for recall_node in recall_node_list])
            print(f"node: {node_list}")
    print("----- finish-----")


if __name__ == '__main__':
    # doc_index()
    query()
