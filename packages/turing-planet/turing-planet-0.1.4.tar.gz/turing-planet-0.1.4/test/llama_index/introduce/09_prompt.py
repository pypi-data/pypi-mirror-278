from llama_index.core import VectorStoreIndex, PromptTemplate

from test.llama_index.introduce.introduce_base import redis_store

qa_prompt_tmpl_str = """
下面是上下文信息.
---------------------
{context_str}
---------------------
根据上下文信息和知识回答问题
问题: {query_str}
答案:
"""

if __name__ == '__main__':
    index = VectorStoreIndex.from_vector_store(vector_store=redis_store)

    qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
    # 创建查询引擎
    query_engine = index.as_query_engine(similarity_top_k=3, text_qa_template=qa_prompt_tmpl)

    # 执行查询
    response = query_engine.query("截止2024年1月，合肥市创建国家卫生城市计划实施步骤进展到什么阶段了？")
    print(response)
