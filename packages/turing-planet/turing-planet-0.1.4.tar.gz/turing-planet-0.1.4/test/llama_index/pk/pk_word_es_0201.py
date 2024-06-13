import logging
import os
from typing import List

import pandas as pd
from llama_index.core import StorageContext, SimpleDirectoryReader, VectorStoreIndex, PromptTemplate, \
    QueryBundle, get_response_synthesizer, Settings
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.indices.vector_store import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.schema import NodeWithScore
from llama_index.core.vector_stores import FilterOperator, MetadataFilters, MetadataFilter
from llama_index.core.vector_stores.types import VectorStoreQueryMode
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from pydantic.v1 import BaseModel

from turing_planet.llama_index.embeddings.sparkai import SparkAIEmbedding
from turing_planet.llama_index.llms.sparkai import SparkAI

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    # filename='pk.log',
)

# DEFAULT_FILE_READER_CLS.update({".xlsx": ExcelReader, ".xls": ExcelReader})

qa_prompt_tmpl_str = """
Context information is below.
---------------------
{context_str}
---------------------

Given the context information and not prior knowledge, answer the query.

当用户的问题涉及推理和计算方面时，请认真思考并逐步进行推理，然后用中文回答。

问题: {query_str}
答案:
"""


# ----------------------------------------------------------------------
class VectorCombineRetriever(BaseRetriever):
    def __init__(self, vector_retriever: VectorIndexRetriever):
        self._vector_retriever = vector_retriever
        super().__init__()

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        self._vector_retriever._vector_store_query_mode = VectorStoreQueryMode.DEFAULT

        # 1. 向量检索，选取topN重排集合
        vector_nodes = self._vector_retriever.retrieve(query_bundle)

        print(f"-----vector_nodes: \n{vector_nodes}\n")

        # 2. 文本倒排索引
        self._vector_retriever._vector_store_query_mode = VectorStoreQueryMode.TEXT_SEARCH
        text_nodes = self._vector_retriever.retrieve(query_bundle)
        # 过滤掉分值很低的干扰项
        text_nodes_better = [text_node for text_node in text_nodes if text_node.score > 0.00001]
        print(f"-----text_nodes: \n{text_nodes_better}\n")

        # 3. 合并
        retrieve_nodes = self._merge_and_remove_duplicates(vector_nodes, text_nodes_better)
        print(f"-----retrieve_nodes: \n{retrieve_nodes}\n")

        return retrieve_nodes

    def _merge_and_remove_duplicates(self, vector_node: List[NodeWithScore], text_nodes: List[NodeWithScore]):
        common_array = []
        for node1 in vector_node:
            for node2 in text_nodes:
                if node1.node_id == node2.node_id:
                    common_array.append(node1)

        # 合并两个数组
        merged_list = vector_node + text_nodes

        # 根据id属性去重
        unique_nodes = {node.node_id: node for node in merged_list}.values()

        # 转换成列表并返回
        result_list = list(unique_nodes)

        # 再次去重
        merged_list = common_array + result_list
        unique_nodes = {node.node_id: node for node in merged_list}.values()
        result_list = list(unique_nodes)
        return result_list


# ------------------------------------------------------------------------------------

class Config(BaseModel):
    # endpoint: str = "172.31.164.103:9980"
    endpoint: str = "127.0.0.1:9980"
    model_domain = "generalv3"
    # model_domain = "65B"
    emb_domain: str = "emb_v1"
    # 1.2的惩罚值效果比1.5好
    punish: float = 1.2
    max_tokens: int = 8192
    context_window: int = 7500
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

es_vector_store = ElasticsearchStore(es_url="http://172.31.164.103:49200", index_name="llamaindex-pk-doc-1024",
                                     batch_size=10)

storage_context = StorageContext.from_defaults(vector_store=es_vector_store)

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
    index = VectorStoreIndex.from_vector_store(vector_store=es_vector_store,
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

        vector_retriever = index.as_retriever(similarity_top_k=config.top_k, filters=filters, )
        combine_retriever = VectorCombineRetriever(vector_retriever=vector_retriever)
        response_synthesizer = get_response_synthesizer(text_qa_template=PromptTemplate(qa_prompt_tmpl_str))
        query_engine = RetrieverQueryEngine.from_args(retriever=combine_retriever,
                                                      response_synthesizer=response_synthesizer)

        result_list = []
        for question in read_excel(excel_file):
            result = query_engine.query(question)
            r = result.response.replace("<ret>", "\n").replace("<end>", "")
            result_list.append(r)
            print(f"question: {question}\n answer: {r}\n=== query end === ")
        save_excel(excel_file, result_list)
    print("----- finish-----")


if __name__ == '__main__':
    # doc_index()
    query()
