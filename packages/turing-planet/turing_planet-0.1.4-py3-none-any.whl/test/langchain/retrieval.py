import os
import sys

sys.path.append(os.getcwd())

import logging
from langchain.vectorstores.redis import Redis

from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough

from turing_planet.langchain.embeddings.sparkai import SparkAIEmbedding
from turing_planet.langchain.chat_models.sparkai import ChatSparkAI

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

emebedding = SparkAIEmbedding(endpoint="172.31.101.142:9980")

# 使用es作为向量数据库，最大支持的向量维度是2048
# vectorstore = ElasticsearchStore(
#     embedding=emebedding,
#     index_name="langchain-demo",
#     es_url="http://172.31.164.103:49200",
#     distance_strategy=DistanceStrategy.COSINE
# )

vectorstore = Redis(
    embedding=emebedding,
    index_name="langchain-demo-1",
    redis_url="redis://172.31.128.153:6379",
    vector_schema={"distance_metric": "cosine"})


def similarity_search():
    # vectorstore.delete(ids=["70e85411-2b1b-4b4b-a10c-28ccfbe570ec"])
    vectorstore.drop_index(index_name="langchain-demo-1", delete_documents=True,
                           redis_url="redis://172.31.128.153:6379")
    vectorstore.add_texts(
        texts=["大众燃油汽车需要每行驶5000公里，做一次汽车保养，保养内容有更换机油、机滤等基础项目，除此之外，还会根据里程数安排轮胎更换等项目"]

    )
    vectorstore.add_texts(
        texts=["电动汽车不需要保养，只需要根据情况更换电池"]
    )
    vectorstore.add_texts(
        texts=["你好，我的名字叫小明"]
    )
    top_k = 5
    docs = vectorstore.similarity_search_with_score("燃油汽车", k=top_k)
    # assert len(docs) == top_k
    for doc in docs:
        result = f"content: {doc[0].page_content} \n score: {doc[1]}"
        logging.info(result)


def retriever_with_vectorstore():
    retriever = vectorstore.as_retriever(search_kwargs={'k': 1})
    result = retriever.invoke("你的名字是什么？")
    logging.info(result)


def rag():
    chat = ChatSparkAI()
    retriever = vectorstore.as_retriever(search_kwargs={'k': 1})

    template = """根据下面提供的内容，回答问题:
            {context}
            问题: {question}
            """
    prompt = ChatPromptTemplate.from_template(template)

    chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | chat
    )

    # result = chain.invoke("我的大众凌度汽车，需要多久做一次保养？")
    result = chain.invoke("你知道我的名字吗？")
    logging.info(result)


def xfyun_with_redis():
    redis_store = Redis(
        embedding=SparkAIEmbedding(embed_type="cloud"),
        index_name="langchain-demo",
        redis_url="redis://172.31.128.153:6379",
        vector_schema={"distance_metric": "cosine"})
    # 插入文本
    redis_store.add_texts(
        texts=[
            "大众燃油汽车需要每行驶5000公里，做一次汽车保养，保养内容有更换机油、机滤等基础项目，除此之外，还会根据里程数安排轮胎更换等项目"]
    )
    redis_store.add_texts(
        texts=["电动汽车不需要保养，只需要根据情况更换电池"]
    )
    redis_store.add_texts(
        texts=["你好，我的名字叫小明"]
    )
    # 检索
    chat = ChatSparkAI()
    retriever = redis_store.as_retriever(search_kwargs={'k': 1})

    template = """根据下面提供的内容，回答问题:
                {context}
                问题: {question}
                """
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | chat
    )
    result = chain.invoke("你知道我的名字吗？")
    logging.info(result)


if __name__ == "__main__":
    print("============== similarity_search ================")
    similarity_search()

    # print("============== retriever_with_vectorstore ================")
    # retriever_with_vectorstore()

    # print("============== rag ================")
    # rag()

    # print("============== xfyun_with_redis ================")
    # xfyun_with_redis()

    # vectorstore = Redis(
    #     embedding=SparkAIEmbedding(embed_type="cloud"),
    #     index_name="langchain-demo-1",
    #     redis_url="redis://172.31.128.153:6379",
    #     vector_schema={"distance_metric": "cosine"})
    #
    # vectorstore.drop_index(index_name="langchain-demo-1", delete_documents=True, redis_url="redis://172.31.128.153:6379")
