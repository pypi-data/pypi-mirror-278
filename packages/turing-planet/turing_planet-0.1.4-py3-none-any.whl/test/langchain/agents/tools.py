from typing import Type, Optional

from langchain.schema.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.tools import tool, BaseTool, StructuredTool
from langchain.tools.render import format_tool_to_openai_function
from pydantic.v1 import BaseModel, Field


# 方式一：tool装饰器
@tool("search-tool")
def search(query: str) -> str:
    """Look up things online."""
    return "LangChain"


# 集成basetool，最大限度灵活度

class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")


class CustomSearchTool(BaseTool):
    name = "custom_search"
    description = "useful for when you need to answer questions about current events"
    args_schema: Type[BaseModel] = SearchInput

    def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return f"LangChain, {query}"

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")


# 使用StructuredTool
def search_function(query: str):
    return "LangChain"


search = StructuredTool.from_function(
    func=search_function,
    name="Search",
    description="useful for when you need to answer questions about current events",
    # coroutine= ... <- you can specify an async method if desired as well
)

if __name__ == '__main__':
    # print(search.invoke("test "))
    openai_function = format_tool_to_openai_function(search)
    print(openai_function)

"""
format_tool_to_openai_function result:
{
    "name": "Search",
    "description": "Search(query: str) - useful for when you need to answer questions about current events",
    "parameters": {
        "title": "SearchSchemaSchema",
        "type": "object",
        "properties": {
            "query": {
                "title": "Query",
                "type": "string"
            }
        },
        "required": [
            "query"
        ]
    }
}
"""
