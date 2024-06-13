from llama_index.core import VectorStoreIndex, get_response_synthesizer, PromptTemplate
from llama_index.core.indices.query.query_transform import StepDecomposeQueryTransform
from llama_index.core.query_engine import MultiStepQueryEngine

from test.llama_index.introduce.introduce_base import redis_store

# 多步检索，将一个复杂的问题拆成多个连续的子问题
prompt = """
原始的问题如下:{query_str}

请针对这个问题逐步思考，将每一步推理生成一个新问题。如果有上下文信息，还需结合上下文思考

问题: {query_str}

上下文: {context_str}

之前的推理: {prev_reasoning}

新问题: 

"""

if __name__ == '__main__':
    # 加载数据
    vector_index = VectorStoreIndex.from_vector_store(vector_store=redis_store)

    transform = StepDecomposeQueryTransform(step_decompose_query_prompt=PromptTemplate(prompt), verbose=True, )
    vector_engine = vector_index.as_query_engine()

    engine = MultiStepQueryEngine(query_engine=vector_engine,
                                  query_transform=transform,
                                  # 拆分两步
                                  num_steps=2,
                                  response_synthesizer=get_response_synthesizer())

    response = engine.query("截止2024年1月，合肥市创建国家卫生城市计划实施步骤进展到什么阶段了？")
    print(response)
