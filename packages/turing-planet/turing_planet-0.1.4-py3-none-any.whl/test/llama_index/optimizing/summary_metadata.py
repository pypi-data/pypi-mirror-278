from test.llama_index.optimizing.base import add_vector_index, query, splitter, extractor

INDEX_NAME = "hf_llamaindex_sm"

if __name__ == '__main__':
    add_vector_index(index_name=INDEX_NAME, transformations=[
        splitter,
        extractor
    ])

    query(index_name=INDEX_NAME)
