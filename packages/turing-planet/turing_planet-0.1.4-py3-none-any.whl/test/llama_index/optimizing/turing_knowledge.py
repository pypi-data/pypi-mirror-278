import time

from llama_index.core import SimpleDirectoryReader

from turing_planet.langchain.llm.sparkai import SparkAI
from turing_planet.llama_index.readers.file.turing_markdown_reader import TuringMarkdownReader

SUMMARY_PROMPT_TEMPL = """
## 任务
你是一个文档总结高手，根据文档内容，总结出这篇文档的摘要。


## 要求
1. 摘要内容字数必须在50字以内。
2. 语言简练，覆盖核心标题内容。


## 文档内容
{{context}}

## 摘要

"""

PROMPT_TEMPL = """
## 任务
请从知识片段列表中，找出能够回答用户问题的知识片段的序号，最多不超过1个。


## 要求
1. 找出的知识片段必须和用户问题相符
2. 如果没有找到，必须返回None

## 知识片段
片段1：
文本档主要介绍星火大模型部署环节中关于驱动如何安装和卸载。包括需要的组件清单、驱动版本、安装步骤以及基础环境的安装。

片段2：
本文档主要介绍在华为服务器部署大模型，如何安装驱动。

片段3：
本文档主要介绍星火大模型如何使用docker容器化部署。包括docker安装，镜像启动等

片段4：
本文档主要介绍星火大模型版本申请的流程。包括：领导审批、版本下载、授权加密狗申请、版本部署

片段5：
本文档主要介绍有关星火大模型开放平台（即燎原开发平台）的相关问题和解答。包括部署和使用过程中遇到的问题

片段6：
本文档主要介绍有关火石平台（即星火大模型训练平台）的相关问题和解答。包括部署和使用过程中遇到的问题，如服务器软硬件的要求，部署过程中报错问题、配置修改问题等。

片段7：
本文档主要介绍文档问答平台（即文档知识库产品）的相关问题和解答。包括部署和使用过程中遇到的问题。

片段8：
本文档主要介绍skynet（即xmanager服务）托管平台部署使用常见问题。

片段9：
本文档主要介绍swk（声纹库）服务部署使用常见问题。

片段10：
本文档主要介绍tts/xtts（语音合成）服务部署使用常见问题。

片段11：
本文档主要介绍kbqa（智能问答）服务部署使用常见问题。

片段12：
本文档主要介绍星球服务部署使用常见问题。

片段13：
本文档主要介绍星球服务关于知识库管理api接口协议，主要包括知识点和知识库的增删改查接口

片段14：
本文档主要介绍星球服务关于知识库管理api接口协议，主要包括会话管理接口


## 样例
用户：
tts服务启动报错，no  license

系统：
10


用户：
图文识别支持哪些格式图片的识别

系统：
None


## 用户问题
{{question}}
"""


def query():
    query = "星球知识库接口文档"

    prompt = PROMPT_TEMPL.replace("{{question}}", str(query))

    print("===prompt===\n", prompt)
    spark = SparkAI(endpoint="172.31.164.103:9980")
    spark.temperature = 0

    print("===answer===")
    print(spark.invoke(prompt))


def summary_doc():
    # 替换默认的md文件解析
    # DEFAULT_FILE_READER_CLS.update({".md": TuringMarkdownReader})

    spark = SparkAI(endpoint="172.31.164.103:9980")
    spark.temperature = 0

    input_dir = "/Users/wujian/Downloads/skynet-doc-center/turing-zhiwen/4.0.14/"
    simple_reader = SimpleDirectoryReader(
        input_dir=input_dir,
        recursive=True,
        exclude=[".git"],
        required_exts=[".pdf", ".docx", ".txt", ".md", ".ppt", ".pptm", ".ppt"]
    )
    documents = simple_reader.load_data(show_progress=True)
    doc_summary_dict = {}
    for document in documents:
        doc_summary_dict.update({document.metadata['file_path']: document.metadata['summary']})
        prompt = SUMMARY_PROMPT_TEMPL.replace("{{context}}", document.text)
        # summary = spark.invoke(prompt)
        # print("========================")
        # print(f"file: {document.metadata['file_path']}\nsummary: {summary}")
    print(len(doc_summary_dict))
    print(doc_summary_dict)


if __name__ == '__main__':
    start = time.time()
    query()
    print("cost", time.time() - start)
