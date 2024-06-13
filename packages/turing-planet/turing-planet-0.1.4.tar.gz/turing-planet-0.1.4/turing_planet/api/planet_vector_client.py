import json
import logging
from typing import Any, Optional, List, Dict

import requests

from turing_planet.utils.env import get_from_dict_or_env

logger = logging.getLogger(__name__)


class VectorAddRequest:

    def __init__(self, vid: str, vector: List[float], text: str, metadata: dict = None):
        self.vid = vid
        self.vector = vector
        self.text = text
        self.metadata = metadata


def _build_request_dict(trace_id: str, payload: Dict) -> Dict:
    return {
        "header": {
            "traceId": trace_id
        },
        "parameter": {},
        "payload": payload
    }


def _do(api_url: str, body: Dict):
    logger.debug(f"planet vector request = {body}")
    response = requests.post(url=api_url, json=body, headers={"content-type": "application/json"}).text
    logger.debug(f"planet vector response = {response}")

    data = json.loads(response)
    code = data["header"]["code"]
    if code != 0:
        raise PlanetVectorError(f"vector error. code={code}")
    else:
        return data["payload"]


class PlanetVectorClient:
    '''
      请求星球向量数据库操作
    '''

    # todo endpoint 需要统一抽取出来
    def __init__(
            self,
            trace_id: Optional[str] = None,
            **kwargs: Any,
    ) -> None:
        endpoint = get_from_dict_or_env(
            kwargs,
            "endpoint",
            "TURING_PLANET_ENDPOINT",
            "127.0.0.1:9980",
        )
        self._trace_id = trace_id
        self.base_url = f"http://{endpoint}/turing/planet/v1/vector_store"

    def add(self, index_name: str, vector_requests: List[VectorAddRequest]) -> None:
        data = []
        for request in vector_requests:
            data.append({
                "id": request.vid,
                "vector": request.vector,
                "text": request.text,
                "metadata": request.metadata
            })
        body_dict = _build_request_dict(trace_id=self._trace_id, payload={"indexName": index_name, "data": data})

        _do(api_url=f"{self.base_url}/add", body=body_dict)

    def delete(self, index_name: str, ref_doc_id: str, **delete_kwargs: Any) -> None:
        body_dict = _build_request_dict(trace_id=self._trace_id,
                                        payload={"indexName": index_name, "refDocId": ref_doc_id})

        _do(api_url=f"{self.base_url}/del", body=body_dict)

    def query(self, index_name: str,
              vector: List[float],
              top_k: int,
              filters: Optional[Dict],
              query_str: Optional[str],
              **kwargs) -> Dict:
        payload = {"indexName": index_name, "vector": vector, "topK": top_k, "filters": filters, "queryText": query_str}
        body_dict = _build_request_dict(trace_id=self._trace_id, payload=payload)

        return _do(api_url=f"{self.base_url}/query", body=body_dict)

    def drop_index(self, index_name: str):
        logger.info(f"start drop index=[{index_name}]")
        body_dict = _build_request_dict(trace_id=self._trace_id, payload={"indexName": index_name})

        return _do(api_url=f"{self.base_url}/drop", body=body_dict)


class PlanetVectorError(Exception):
    pass


'''
# 保存特征
POST turing/planet/v1/vector_store/add
## 入参 
{
    "header": {
        "traceId": "xxx"
    },
    "parameter": {},
    "payload": {
        "indexName": "",
        "data": [
            {
                "id": "",
                "vector": [],
                "text": "",
                "metadata": {}
            }
        ]
    }
}

## 出参
{
  "header": {
    "code": 0,
    "message": ""
  },
  "payload": {}
}

-------------------

# 删除特征
POST turing/planet/v1/vector_store/del
## 入参
{
    "header": {
        "traceId": "xxx"
    },
    "parameter": {},
    "payload":{"indexName:"", "refDocId":"xxx"}
}

## 出参
{
  "header": {
    "code": 0,
    "message": ""
  },
  "payload": {}
}

-------------------
# 删除索引
POST turing/planet/v1/vector_store/drop
## 入参
{
    "header": {
        "traceId": "xxx"
    },
    "parameter": {},
    "payload":{"indexName:""}
}

## 出参
{
  "header": {
    "code": 0,
    "message": ""
  },
  "payload": {}
}

-------------------

# 检索
POST turing/planet/v1/vector_store/query

## 入参 
{
    "header": {
        "traceId": "xxx"
     },
    "payload":{"indexName":"ccc","vector":[], "topK":1, "filters":{}, "queryText":"ccc"}
}

## 出参
{
  "header": {
    "code": 0,
    "message": ""
  },
  "payload": {
    "data": [
        {
            "id":"",
            "score": 0.96
            "metadata":{},
            "text":""
        }
    ]
  }
}
'''
