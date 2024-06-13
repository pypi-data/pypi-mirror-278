import os

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser.text.utils import split_by_sentence_tokenizer

if __name__ == '__main__':
    documents = SimpleDirectoryReader(input_files=["../data/合政〔2022〕176号.docx"]).load_data()
    print(len(documents))

    split_fns = split_by_sentence_tokenizer()

    sentence_list = split_fns(documents[0].text)
    for sentence in sentence_list:
        print(sentence)
        print("=========")
