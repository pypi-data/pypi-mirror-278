import base64
import hashlib
import hmac
from urllib.parse import urlencode, urlparse, urlunparse
from wsgiref.handlers import format_date_time
from time import mktime
from datetime import datetime


# 公有云url请求签名
def signature_url_get(api_url: str, api_key: str, api_secret: str) -> str:
    return signature_url(api_url=api_url, method="GET", api_key=api_key, api_secret=api_secret)


def signature_url_post(api_url: str, api_key: str, api_secret: str) -> str:
    return signature_url(api_url=api_url, method="POST", api_key=api_key, api_secret=api_secret)


def signature_url(api_url: str, method:str, api_key: str, api_secret: str) -> str:
    """
    Generate a request url with an api key and an api secret.
    """
    # generate timestamp by RFC1123
    date = format_date_time(mktime(datetime.now().timetuple()))

    # urlparse
    parsed_url = urlparse(api_url)
    host = parsed_url.netloc
    path = parsed_url.path

    signature_origin = f"host: {host}\ndate: {date}\n{method} {path} HTTP/1.1"

    # encrypt using hmac-sha256
    signature_sha = hmac.new(
        api_secret.encode("utf-8"),
        signature_origin.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()

    signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding="utf-8")

    authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", \
    headers="host date request-line", signature="{signature_sha_base64}"'
    authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode(
        encoding="utf-8"
    )

    # generate url
    params_dict = {"authorization": authorization, "date": date, "host": host}
    encoded_params = urlencode(params_dict)
    url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            encoded_params,
            parsed_url.fragment,
        )
    )
    return url


if __name__ == "__main__":
   print(signature_url("ws://bac/ppp", "key111", "sec"))