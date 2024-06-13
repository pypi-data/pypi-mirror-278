from llama_index.core import SimpleDirectoryReader
from llama_index.readers.mongodb import SimpleMongoReader


def reader():
    simple_reader = SimpleDirectoryReader(
        # 文件目录
        input_dir="/Users/wujian/workspace/code/llm/turing-planet/turing-planet/test/llama_index/data",
        # 是否递归子目录
        recursive=True,
        # 排除哪些文件
        exclude=[".git"],
        # 要求文件的后缀名
        required_exts=[".pdf", ".docx", ".txt", ".md", ".ppt", ".pptm", ".ppt"],
    )
    documents = simple_reader.load_data(show_progress=True)
    print(documents)


def mongo():
    uri = "mongodb://root:Mgadmin_1234@172.31.164.103:30006/turing_planet?authSource=admin&authMechanism=SCRAM-SHA-1"
    db_name = "turing_planet"
    collection_name = "doc_helper"
    # query_dict is passed into db.collection.find()
    query_dict = {}
    field_names = ["name"]
    reader = SimpleMongoReader(uri=uri)
    documents = reader.load_data(
        db_name, collection_name, field_names, query_dict=query_dict
    )
    print(documents)


if __name__ == '__main__':
    reader()
