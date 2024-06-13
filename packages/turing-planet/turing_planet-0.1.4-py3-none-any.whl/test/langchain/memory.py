# -*- coding: utf-8 -*-
# 会话记忆
import logging
import json
from langchain_core.messages import message_to_dict

from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import MongoDBChatMessageHistory

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable.history import RunnableWithMessageHistory

from turing_planet.langchain.chat_models.sparkai import ChatSparkAI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

chat = ChatSparkAI(endpoint="172.31.164.103:9980")

mongodb_url = "mongodb://root:Mgadmin_1234@172.31.164.103:30006"

session_id = "sid_lc"

def mongodb():
    """Test the memory with a message store."""
    # setup MongoDB as a message store
    message_history = MongoDBChatMessageHistory(
        connection_string=mongodb_url, 
        session_id="test-session-2",
    )
    memory = ConversationBufferMemory(
        memory_key="baz", chat_memory=message_history, return_messages=True
    )

    # add some messages
    memory.chat_memory.add_ai_message("This is me, the AI")
    memory.chat_memory.add_user_message("This is me, the human")

    # get the message history from the memory store and turn it into a json
    messages = memory.chat_memory.messages
    messages_json = json.dumps([message_to_dict(msg) for msg in messages])

    assert "This is me, the AI" in messages_json
    assert "This is me, the human" in messages_json

    # remove the record from Azure Cosmos DB, so the next test run won't pick it up
    # memory.chat_memory.clear()
    # assert memory.chat_memory.messages == []


# 根据sessionId取出全部历史，可以根据需求扩展 MongoDBChatMessageHistory，支持如topK
def chat_with_memory(question: str, session_id: str):
    # 构造链
    prompt = ChatPromptTemplate.from_messages(
        [
            # 历史会话占位
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ]
    )
    chain = prompt | chat

    # 添加历史消息, 使用RunnableWithMessageHistory包装原始链
    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id:  MongoDBChatMessageHistory(connection_string=mongodb_url, session_id=session_id),
        input_messages_key="question",
        history_messages_key="history"
    )

    # 通过配置，执行链
    res = chain_with_history.invoke(
        {"question": question},
        config={"configurable": {"session_id": session_id}}
    )
    logging.info(res)

def mongodb_memory():
    # 清除记录
    message_history = MongoDBChatMessageHistory(connection_string=mongodb_url, session_id=session_id)
    message_history.clear()

    chat_with_memory(question="截止2022年，全球GDP最高的国家是哪个？", session_id=session_id)

    chat_with_memory(question="比中国高多少？", session_id=session_id)


def mongodb_memory_append():
    chat_with_memory(question="比日本高多少？", session_id=session_id)


if __name__ == "__main__":
    mongodb_memory();
    
    # mongodb_memory_append()
    
    # mongodb()