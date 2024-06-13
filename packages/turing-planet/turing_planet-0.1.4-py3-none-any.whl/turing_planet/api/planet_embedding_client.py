import json
import logging
from typing import Optional, Any, List

import requests

from turing_planet.utils.env import get_from_dict_or_env

logger = logging.getLogger(__name__)


class PlanetEmbeddingClient:

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
        self._endpoint = endpoint
        """
            私有化1024维
            emb_v2 ：私有化2560维
            emb_xfyun：公有云2560维
        """
        self._domain = ""
        if "domain" in kwargs:
            self._domain = kwargs["domain"]

    def embedding_documents(self, texts: List[str]) -> List[List[float]]:
        results = []
        for text in texts:
            results.append(self._do(text=text, embed_type=1))
        return results

    def embedding_query(self, text: str) -> List[float]:
        return self._do(text=text, embed_type=2)

    # -------------  private method  -------------

    def _do(self, text: str, embed_type: int) -> List[float]:
        url = f"http://{self._endpoint}/turing/planet/v1/txt/embedding"
        content = self._convert_param_to_dict(text=text, embed_type=embed_type)
        # todo 校验是否请求成功
        logger.debug(f"planet embedding request = {content}")
        response = requests.post(url, json=content, headers={"content-type": "application/json"}).text
        return self._parse_response(response=response)

    def _convert_param_to_dict(self, text: str, embed_type: int) -> dict:
        param_dict = {
            "header": {"traceId": self._trace_id},
            "parameter": {},
            "payload": {"text": text, "type": embed_type, "embeddingSetting": {"domain": self._domain}},
        }
        return param_dict

    @staticmethod
    def _parse_response(response: str) -> List[float]:
        data = json.loads(response)
        code = data["header"]["code"]
        if code != 0:
            raise SparkEmbeddingError(f"embedding error. code={code}. response = {response}")
        else:
            vector = data["payload"]["vector"]
            logger.debug(f"planet embedding vector dims = {len(vector)}")
            return vector


class SparkEmbeddingError(Exception):
    pass
