from typing import Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from langchain.agents import AgentType, initialize_agent

from turing_planet.langchain.chat_models.sparkai import ChatSparkAI


# Define custom functions
def get_current_stock_price(ticker):
    """Method to get current stock price"""
    print("get_current_stock_price")
    return {"price": 0.66, "currency": "USD"}


def get_stock_performance(ticker, days):
    """Method to get stock price change in percentage"""
    print("get_stock_performance")
    return {"percent_change": 1.014466941163018}


# Make custom tools
class CurrentStockPriceInput(BaseModel):
    """Inputs for get_current_stock_price"""

    ticker: str = Field(description="Ticker symbol of the stock")


class CurrentStockPriceTool(BaseTool):
    name = "get_current_stock_price"
    description = """
        Useful when you want to get current stock price.
        You should enter the stock ticker symbol recognized by the yahoo finance
        """
    args_schema: Type[BaseModel] = CurrentStockPriceInput

    def _run(self, ticker: str):
        price_response = get_current_stock_price(ticker)
        return price_response

    def _arun(self, ticker: str):
        raise NotImplementedError("get_current_stock_price does not support async")


class StockPercentChangeInput(BaseModel):
    """Inputs for get_stock_performance"""

    ticker: str = Field(description="Ticker symbol of the stock")
    days: int = Field(description="Timedelta days to get past date from current date")


class StockPerformanceTool(BaseTool):
    name = "get_stock_performance"
    description = """
        Useful when you want to check performance of the stock.
        You should enter the stock ticker symbol recognized by the yahoo finance.
        You should enter days as number of days from today from which performance needs to be check.
        output will be the change in the stock price represented as a percentage.
        """
    args_schema: Type[BaseModel] = StockPercentChangeInput

    def _run(self, ticker: str, days: int):
        response = get_stock_performance(ticker, days)
        return response

    def _arun(self, ticker: str):
        raise NotImplementedError("get_stock_performance does not support async")


if __name__ == '__main__':
    # llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)
    llm = ChatSparkAI(
        endpoint="172.30.209.90:9980",
    )

    tools = [CurrentStockPriceTool(), StockPerformanceTool()]

    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

    agent.run(
        "What is the current price of Microsoft stock? How it has performed over past 6 months?"
    )
