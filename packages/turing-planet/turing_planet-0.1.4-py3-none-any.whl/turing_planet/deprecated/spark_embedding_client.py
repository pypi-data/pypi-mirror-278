import base64
import json
import logging
from typing import Optional, List, Any

import numpy as np
import requests

from turing_planet.utils.auth_util import signature_url_post
from turing_planet.utils.env import get_from_dict_or_env

logger = logging.getLogger(__name__)


class TuringEmbeddingClient:

    def __init__(
            self,
            trace_id: Optional[str] = None,
            **kwargs: Any,
    ) -> None:
        endpoint = get_from_dict_or_env(
            kwargs,
            "endpoint",
            "TURING_EMBEDDING_ENDPOINT",
            "127.0.0.1:9987",
        )
        self._trace_id = trace_id
        self._endpoint = endpoint

    def embedding_documents(self, texts: List[str]) -> List[List[float]]:
        results = []
        for text in texts:
            results.append(self._do(text=text, model="docs"))
        return results

    def embedding_query(self, text: str) -> List[float]:
        return self._do(text=text, model="query")

    # private method

    def _do(self, text: str, model: str) -> List[float]:
        url = f"http://{self._endpoint}/turing/v3/embedding"
        content = None
        if model == "docs":
            content = self._convert_turing_docs_to_dict(
                trace_id=self._trace_id, text=text
            )
        else:
            content = self._convert_turing_query_to_dict(
                trace_id=self._trace_id, text=text
            )
        # todo 校验是否请求成功
        response = requests.post(url, json=content, headers={"content-type": "application/json"}).text
        return self._parse_turing_response(response=response)

    def _convert_turing_param_to_dict(
            self, trace_id: str, text_dict: dict, model: str
    ) -> dict:
        param_dict = {
            "header": {"traceId": trace_id},
            "parameter": {"engine": {"model": model}},
            "payload": {"text": text_dict},
        }
        return param_dict

    def _convert_turing_docs_to_dict(self, trace_id: str, text: str) -> dict:
        text_dict = {"docs": {"knowledge": text}}
        return self._convert_turing_param_to_dict(
            trace_id=trace_id, text_dict=text_dict, model="docs-embedding"
        )

    def _convert_turing_query_to_dict(self, trace_id: str, text: str) -> dict:
        text_dict = {"query": text}
        return self._convert_turing_param_to_dict(
            trace_id=trace_id, text_dict=text_dict, model="query-embedding"
        )

    def _parse_turing_response(self, response: str) -> List[float]:
        logger.debug(f"spark embedding response = {response}")

        data = json.loads(response)
        code = data["header"]["code"]
        if code != 0:
            raise SparkEmbeddingError(f"embedding error. code={code}")
        else:
            vector = data["payload"]["result"]
            return vector


class XfYunEmbeddingClient:

    def __init__(
            self,
            uid: str = None,
            **kwargs: Any,
    ) -> None:

        kwargs["iflytek_app_id"] = get_from_dict_or_env(
            kwargs,
            "iflytek_app_id",
            "IFLYTEK_APP_ID",
        )
        kwargs["iflytek_api_key"] = get_from_dict_or_env(
            kwargs,
            "iflytek_api_key",
            "IFLYTEK_APP_KEY",
        )
        kwargs["iflytek_api_secret"] = get_from_dict_or_env(
            kwargs,
            "iflytek_api_secret",
            "IFLYTEK_APP_SECRET",
        )

        self._uid = uid
        self._app_id = kwargs["iflytek_app_id"]
        self._api_key = kwargs["iflytek_api_key"]
        self._api_secret = kwargs["iflytek_api_secret"]

    def embedding_documents(self, texts: List[str]) -> List[List[float]]:
        results = []
        for text in texts:
            results.append(self._do(text=text, api_url="http://cn-huabei-1.xf-yun.com/v1/private/sa8a05c27"))
        return results

    def embedding_query(self, text: str) -> List[float]:
        return self._do(text=text, api_url="http://cn-huabei-1.xf-yun.com/v1/private/s50d55a16")

    # private method

    def _do(self, text: str, api_url: str) -> List[float]:
        url = signature_url_post(api_url=api_url, api_key=self._api_key, api_secret=self._api_secret)
        content = self._convert_param_to_dict(text)
        response = requests.post(url, json=content, headers={'content-type': "application/json"}).text
        return self._parse_response(response=response)

    def _convert_param_to_dict(self, text: str) -> dict:
        text_dict = {"messages": [{"content": text, "role": "user"}]}
        param_dict = {
            "header": {
                "app_id": self._app_id,
                "uid": self._uid,
                "status": 3
            },
            "parameter": {
                "emb": {
                    "feature": {
                        "encoding": "utf8"
                    }
                }
            },
            "payload": {
                "messages": {
                    "text": base64.b64encode(json.dumps(text_dict).encode('utf-8')).decode()
                }
            }
        }
        return param_dict

    def _parse_response(self, response: str) -> List[float]:
        logger.debug(f"xfyun embedding response = {response}")

        data = json.loads(response)
        code = data["header"]["code"]
        if code != 0:
            raise SparkEmbeddingError(f"embedding error. code={code}")
        else:
            vector_base64 = data["payload"]["feature"]["text"]
            vector_data = base64.b64decode(vector_base64)
            # 讯飞云官网实例存在bug
            # 创建一个np.float32类型的数据类型对象dt，表示32位浮点数。
            # dt = np.dtype(np.float32)
            # # 使用newbyteorder()方法将dt的字节序设置为小端（"<"）
            # dt = dt.newbyteorder("<")
            # # 使用np.frombuffer()函数将vector_data转换为浮点数数组vector，数据类型为dt。
            # vector = np.frombuffer(vector_data, dtype=dt)

            float_array = np.frombuffer(vector_data, dtype=np.float32)
            vector = float_array.tolist()
            return vector


class SparkEmbeddingError(Exception):
    pass

# https://www.xfyun.cn/doc/spark/Embedding_new_api.html#_3-%E8%AF%B7%E6%B1%82


# http://turing.iflytek.com:2230/skynet-doc/#/home?p=turing-embedding&v=1.1.5
# 私有化接口响应
# {
#   "header": {
#     "code": 0,
#     "message": "success",
#     "traceId": "2db17245ceb04073a1124d01224c7ee9"
#   },
#   "payload": {
#     "result": [
#       -0.007279981,
#       0.035807334,
#       0.02052792,
#       ...,
#       -0.026880676,
#       0.0076045976,
#       0.009626314
#     ],
#     "version": "a49567"
#   }
# }
