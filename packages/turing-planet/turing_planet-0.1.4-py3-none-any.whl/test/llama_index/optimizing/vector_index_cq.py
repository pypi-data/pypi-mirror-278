"""
Q: 我办理的海量卡29元的套餐，可以再加一张副卡吗?
A: 你好，29元的海量卡不能加副卡

Q: 149元档次的5G融合套餐用户已经添加了两张副卡，现在用户还想再添加一张副卡，请问可以办理吗？
A: 不可以，149元档次的5G融合套餐仅支持办理2张副卡

Q: 我在去年（2022年）办理了一个电信电视，现在我想办理安防宽带139档，然后把电视和宽带合在一起，电视是不是可以免费呀？
A: 不能免费，需要2019年11月1日前入网的电信电视老用户迁转为融合套餐才可享受减免天翼高清10元功能费优惠

Q: 办理了5G套餐，是不是就可以使用5G网络了?
A: 不是的，使用5G网络除了5G套餐外还需要使用5G终端且在5G网络覆盖范围内才能使用。

Q: 安防宽带259档承诺到期后可以办理停机保号吗？
A: 不可以。（因天翼看家不支持办理停机保号，故承诺到期后也不可办理停机保号业务）

Q: 智能宽带办239元的宽带套餐有路由器吗？
A: 提供2台路由器。

Q: 现在是169的套餐只有300M，可以转成现在的169元500的全屋智能套餐吗？
A: 原169元套餐不能平迁全屋智能169元套餐，仅限169元以下用户办理。
"""
from typing import List

from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.callbacks import EventPayload, CBEventType
from llama_index.core.node_parser import SentenceSplitter

from test.llama_index.optimizing.base import build_vector_store

load_dotenv()


# 这里粗暴的按照句子拆分了，效果有提升 （2/7）--》（3/7）
class MySentenceSplitter(SentenceSplitter):

    def _split_text(self, text: str, chunk_size: int) -> List[str]:
        if text == "":
            return [text]

        with self.callback_manager.event(
                CBEventType.CHUNKING, payload={EventPayload.CHUNKS: [text]}
        ) as event:
            splits = self._split(text, chunk_size)
            # chunks = self._merge(splits, chunk_size)
            chunks = []
            for split in splits:
                if not split.text.isspace():
                    chunks.append(split.text)
            event.on_end(payload={EventPayload.CHUNKS: chunks})

        return chunks


redis_store = build_vector_store(index_name="cq_llamaindex")
storage_context = StorageContext.from_defaults(vector_store=redis_store)


# 基准测试（纯向量）

user_questions = ["我办理的海量卡29元的套餐，可以再加一张副卡吗?",
                  "149元档次的5G融合套餐用户已经添加了两张副卡，现在用户还想再添加一张副卡，请问可以办理吗？",
                  "我在去年（2022年）办理了一个电信电视，现在我想办理安防宽带139档，然后把电视和宽带合在一起，电视是不是可以免费呀？",
                  "办理了5G套餐，是不是就可以使用5G网络了?",
                  "安防宽带259档承诺到期后可以办理停机保号吗？",
                  "智能宽带办239元的宽带套餐有路由器吗？",
                  "现在是169的套餐只有300M，可以转成现在的169元500的全屋智能套餐吗？"
                  ]


def load_documents():
    simple_reader = SimpleDirectoryReader(input_dir="../../../doc/重庆电信")
    documents = simple_reader.load_data(show_progress=True)
    return documents


def add_vector_index():
    VectorStoreIndex.from_documents(documents=load_documents(),
                                    storage_context=storage_context,
                                    show_progress=True)


def query():
    index = VectorStoreIndex.from_vector_store(vector_store=redis_store)
    query_engine = index.as_query_engine(similarity_top_k=1)
    for question in user_questions:
        response = query_engine.query(question)
        print(f"Q:{question}")
        print(f"A:{response}")
        print(f"file:{response.source_nodes[0].metadata['file_name']}")
        # print(f"source:{response.source_nodes[0].text}")
        print("---------------")


if __name__ == '__main__':
    add_vector_index()
    query()

"""
#######  按照默认句子切分 #######  (2/7)

Q:我办理的海量卡29元的套餐，可以再加一张副卡吗?
A:根据提供的信息，办理的海量卡29元的套餐可以再加一张副卡。
file:5G融合套餐01.docx
---------------
Q:149元档次的5G融合套餐用户已经添加了两张副卡，现在用户还想再添加一张副卡，请问可以办理吗？
A:根据提供的信息，升级版199及以上套餐不能提及超过3张副卡。所以，149元档次的5G融合套餐用户已经添加了两张副卡后，不能再添加第三张副卡。
file:5G融合套餐01.docx
-------ok--------
Q:我在去年（2022年）办理了一个电信电视，现在我想办理安防宽带139档，然后把电视和宽带合在一起，电视是不是可以免费呀？
A:根据提供的信息，无法确定您是否可以将电信电视与安防宽带139档免费合并。建议您直接联系电信公司以获取准确的信息。
file:安防宽带01.docx
---------------
Q:办理了5G套餐，是不是就可以使用5G网络了?
A:是的，办理了5G套餐后，您可以在中国电信移动通信网络中使用5G网络。
file:5G融合套餐01.docx
---------------
Q:安防宽带259档承诺到期后可以办理停机保号吗？
A:安防宽带259档承诺到期后不支持办理停机保号业务。
file:安防宽带01.docx
--------ok-------
Q:智能宽带办239元的宽带套餐有路由器吗？
A:根据提供的信息，全屋智能宽带239元档次套餐没有明确提到是否包含路由器。所以无法确定该套餐是否包含路由器。
file:全屋智能宽带01.docx
---------------
Q:现在是169的套餐只有300M，可以转成现在的169元500的全屋智能套餐吗？
A:根据提供的信息，全屋智能宽带169元档次套餐的具体内容和规则没有明确说明。因此，无法确定是否可以从现有的300M套餐转到169元的全屋智能套餐。建议直接联系重庆电信以获取准确的信息。
file:全屋智能宽带01.docx
---------------


#######  自定义按照句子切分 #######  (3/7)

Q:我办理的海量卡29元的套餐，可以再加一张副卡吗?
A:根据提供的信息，办理的海量卡29元的套餐可以再加一张副卡。
file:5G融合套餐01.docx
---------------
Q:149元档次的5G融合套餐用户已经添加了两张副卡，现在用户还想再添加一张副卡，请问可以办理吗？
A:根据提供的信息，升级版199及以上套餐不能提及超过3张副卡。因此，149元档次的5G融合套餐用户已经添加了两张副卡后，不能再添加第三张副卡。
file:5G融合套餐01.docx
--------OK -------
Q:我在去年（2022年）办理了一个电信电视，现在我想办理安防宽带139档，然后把电视和宽带合在一起，电视是不是可以免费呀？
A:根据提供的信息，2019年11月1日前入网的电信电视老用户在迁转融合套餐时可以减免天翼高清10元功能费。但是您是在2022年办理的电信电视，所以不满足这个减免条件。因此，您的电视不能免费。
file:5G融合套餐01.docx
------- OK --------
Q:办理了5G套餐，是不是就可以使用5G网络了?
A:不是，办理了5G套餐还需要使用5G终端且在5G网络覆盖范围内才能使用。
file:全屋智能宽带01.docx
-------OK--------
Q:安防宽带259档承诺到期后可以办理停机保号吗？
A:无法确定，因为上下文中没有提到关于停机保号的信息。
file:安防宽带01.docx
---------------
Q:智能宽带办239元的宽带套餐有路由器吗？
A:无法确定，因为文档中没有提到239元的宽带套餐是否包含路由器。
file:全屋智能宽带01.docx
---------------
Q:现在是169的套餐只有300M，可以转成现在的169元500的全屋智能套餐吗？
A:根据给出的上下文信息，原全屋智能269元500M套餐用户在资源条件具备的情况下，可以迁转为全屋智能269元1000M套餐或承诺1年提速至1000M（上行30M），需同时更换1000M光猫（需承诺1年）。但是没有提到是否可以从169元的300M套餐转到现在的169元500的全屋智能套餐。因此，无法确定是否可以进行此类转换。
file:全屋智能宽带01.docx
---------------


"""
