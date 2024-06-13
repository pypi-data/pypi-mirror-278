import json
import ssl
import logging
import queue
import threading
from queue import Queue

from typing import Any, Dict, Generator, List, Optional

logger = logging.getLogger(__name__)


# 星球API透传会话接口客户端
class SparkLLMClient:
    """
    Use websocket-client to call the SparkLLM interface provided by Turing-Planet,
    which is the iFlyTek's privatization platform for AI capabilities
    """

    def __init__(
            self,
            endpoint: str,
            trace_id: str,
            model_kwargs: Optional[dict] = None,
    ):
        try:
            import websocket

            self.websocket_client = websocket
        except ImportError:
            raise ImportError(
                "Could not import websocket client python package. "
                "Please install it with `pip install websocket-client`."
            )

        self.ws_url = f"ws://{endpoint}/turing/planet/v1/spark-chat"
        self.trace_id = trace_id
        self.model_kwargs = model_kwargs
        self.queue: Queue[Dict] = Queue()
        self.blocking_message = {"content": "", "role": "assistant"}

    def run(
            self,
            messages: List[Dict],
            model_kwargs: Optional[dict] = None,
            kwargs: Optional[dict] = None,
            streaming: bool = False,
    ) -> None:
        self.websocket_client.enableTrace(False)
        ws = self.websocket_client.WebSocketApp(
            self.ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open,
        )
        ws.messages = messages
        ws.trace_id = self.trace_id
        ws.model_kwargs = self.model_kwargs if model_kwargs is None else model_kwargs
        ws.kwargs = kwargs
        ws.streaming = streaming
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def arun(
            self,
            messages: List[Dict],
            model_kwargs: Optional[dict] = None,
            kwargs: Optional[dict] = None,
            streaming: bool = False,
    ) -> threading.Thread:
        ws_thread = threading.Thread(
            target=self.run,
            args=(
                messages,
                model_kwargs,
                kwargs,
                streaming,
            ),
        )
        ws_thread.start()
        return ws_thread

    def on_error(self, ws: Any, error: Optional[Any]) -> None:
        self.queue.put({"error": error})
        ws.close()

    def on_close(self, ws: Any, close_status_code: int, close_reason: str) -> None:
        logger.debug(
            {
                "log": {
                    "close_status_code": close_status_code,
                    "close_reason": close_reason,
                }
            }
        )
        self.queue.put({"done": True})

    def on_open(self, ws: Any) -> None:
        self.blocking_message = {"content": "", "role": "assistant"}
        data = json.dumps(
            self.gen_params(
                messages=ws.messages, trace_id=ws.trace_id, model_kwargs=ws.model_kwargs, kwargs=ws.kwargs
            ),
            ensure_ascii=False
        )
        logger.debug(f"Spark Request Parameters: {data}")
        ws.send(data)

    def on_message(self, ws: Any, message: str) -> None:
        logger.debug(f"on_message = {message}")
        data = json.loads(message)
        code = data["header"]["code"]
        if code != 0:
            self.queue.put(
                {"error": f"Code: {code}, Error: {data['header']['message']}"}
            )
            ws.close()
        else:
            if "choices" not in data["payload"]:
                return
            choices = data["payload"]["choices"]
            status = choices["status"]
            text_choice = choices["text"][0]
            content = text_choice["content"]
            if ws.streaming:
                self.queue.put({"data": text_choice})
            else:
                self.blocking_message["content"] += content
            if status == 2:
                # 最后一帧
                if not ws.streaming:
                    if "function_call" in text_choice:
                        self.blocking_message.update({"function_call": choices["text"][0]["function_call"]})
                    self.queue.put({"data": self.blocking_message})
                usage_data = (
                    data.get("payload", {}).get("usage", {}).get("text", {})
                    if data
                    else {}
                )
                self.queue.put({"usage": usage_data})
                ws.close()

    def gen_params(
            self, messages: list, trace_id: str, model_kwargs: Optional[dict] = None,
            kwargs: Optional[dict] = None,
    ) -> dict:
        data: Dict = {
            "header": {"trace_id": self.trace_id},
            "parameter": {"chat": {}},
            "payload": {"message": {"text": messages}},
        }
        if kwargs:
            if kwargs.get("functions"):
                functions = {"functions": {"text": kwargs.get("functions")}}
                data["payload"].update(functions)
            # 插件 等等

        if model_kwargs:
            data["parameter"]["chat"].update(model_kwargs)
        return data

    def subscribe(self, timeout: Optional[int] = 120) -> Generator[Dict, None, None]:
        while True:
            try:
                content = self.queue.get(timeout=timeout)
            except queue.Empty as _:
                raise TimeoutError(
                    f"SparkLLMClient wait LLM api response timeout {timeout} seconds"
                )
            if "error" in content:
                raise SparkError(content["error"])
            if "usage" in content:
                yield content
                continue
            if "done" in content:
                break
            if "data" not in content:
                break
            yield content


class SparkError(Exception):
    pass

# url 》 ws://{ip}:{port}/turing/planet/v1/spark-chat
# request body
# {
#         "header": {
#             "traceId": "12345"
#         },
#         "parameter": {
#             "chat": {
#                 "domain": "",
#                 "temperature": 0.5,
#                 "max_tokens": 1024,
#                 "top_k": 4,
#                 "adjustTokens": false
#             }
#         },
#         "payload": {
#           	"plugin_ids":{
#             	    "text": [
#                   {
#                       "id": "xxx",
#                       "token": "",
#                       "version":""
#                   }
#                   ]
#           	},
#             "message": {
#                 "text": [
#                     {"role": "user", "content": "你是谁"} # 用户的历史问题
#                     {"role": "assistant", "content": "....."}  # AI的历史回答结果
#                     # ....... 省略的历史对话
#                     {"role": "user", "content": "你会做什么"}  # 最新的一条问题，如无需上下文，可只传最新一条问题
#                 ]
#         }
#     }
# }

# ////////////////////////////////////////////////////////////////////////////////////////////////////////
# response body
# {
#   "header": {
#     "code": 0,
#     "message": "Success",
#     "sid": "cht000cb087@dx18793cd421fb894542",
#     "status": 2
#   },
#   "payload": {
#     "choices": {
#       "status": 2,
#       "seq": 0,
#       "text": [
#         {
#           "content": "您好，我是讯飞星火大模型",
#           "content_type": "text",
#           "role": "assistant"
#         }
#       ]
#     },
#     "usage": {
#       "text": {
#         "question_tokens": 4,
#         "prompt_tokens": 5,
#         "completion_tokens": 9,
#         "total_tokens": 14
#       }
#     }
#   }
# }
