import os

from llama_hub.tools.google_search import GoogleSearchToolSpec
from llama_hub.web.beautiful_soup_web import BeautifulSoupWebReader


def google_search_tool():
    key = os.environ.get("GOOGLE_API_KEY")
    google_search_tool_spec = GoogleSearchToolSpec(key=key, engine="b2bc383e5f79944e3", num=5)
    response = google_search_tool_spec.google_search("llamahub是什么")
    for item in response:
        print(item.text)


def web_reader():
    # 抽取网页文本内容
    loader = BeautifulSoupWebReader()
    documents = loader.load_data(urls=['https://llamahub.ai/'])
    for document in documents:
        print(document.text)


if __name__ == '__main__':
    web_reader()
