from llama_index.core import Document, SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter


# 演示文档加载 切分过程
def sample_splitter():
    # 按照chunk_size大小切分，chunk_overlap：表示相连两个node重叠部分大小
    node_parser = SentenceSplitter(chunk_size=10, chunk_overlap=3)
    nodes = node_parser.get_nodes_from_documents(
        documents=[Document(
            text="创建文档时，您还可以附加可在查询阶段使用的有用元数据。添加到文档的任何元数据都将被复制到从该文档创建的节点。")],
        show_progress=True)

    for node in nodes:
        print(node)


def sample_pipeline():
    pipeline = IngestionPipeline(transformations=[SentenceSplitter(chunk_size=10, chunk_overlap=0)])

    nodes = pipeline.run(documents=[Document(
        text="创建文档时，您还可以附加可在查询阶段使用的有用元数据。添加到文档的任何元数据都将被复制到从该文档创建的节点。",
        metadata={"file_name": "api.md"})])

    for node in nodes:
        print(node)


def sample():
    simple_reader = SimpleDirectoryReader(input_dir="../data")
    documents = simple_reader.load_data(show_progress=True)

    pipeline = IngestionPipeline(transformations=[SentenceSplitter(chunk_size=512, chunk_overlap=100)])
    for document in documents:
        print(document)

    print("--node--")
    nodes = pipeline.run(documents=documents)
    for node in nodes:
        print(node)


if __name__ == '__main__':
    sample_splitter()
    sample_pipeline()
    sample()
