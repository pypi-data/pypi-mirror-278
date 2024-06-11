from enum import Enum
from http.client import HTTPException
from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin

import backoff
import httpx
from requests import RequestException


async def _validate_response(response: httpx.Response) -> None:
    if not response.status_code < 300:
        msg = (
            "Something didn't go quite right. The api returned a non-ok status "
            f"code {response.status_code} with output: {response.text}"
        )
        # TODO: Better error handling.
        raise HTTPException(msg)


@backoff.on_exception(backoff.expo, RequestException, max_tries=4, jitter=None)
async def make_request(
    request_method: str,
    base_url: str,
    endpoint: str,
    body: Optional[Dict] = None,
    data: Optional[Dict] = None,
    files: Optional[Dict] = None,
    params: Optional[Dict] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: Union[int, None] = None,
) -> Any:
    async with httpx.AsyncClient() as client:
        if request_method == "get":
            response = await client.get(
                urljoin(base_url, endpoint),
                params=params,
                headers=headers or {},
                timeout=timeout,
            )
        elif request_method == "post":
            response = await client.post(
                urljoin(base_url, endpoint),
                json=body,
                data=data,
                files=files,
                params=params,
                headers=headers or {},
                timeout=timeout,
            )
        else:
            raise ValueError(f"Unsupported request method {request_method}")
    await _validate_response(response)
    return response.json()


class HttpHeaders(str, Enum):
    accept = "accept"
    content_type = "Content-Type"
    application_json = "application/json"

    @staticmethod
    def accept_json() -> Dict[str, str]:
        return {HttpHeaders.accept: HttpHeaders.application_json}

    @staticmethod
    def content_type_json() -> Dict[str, str]:
        return {HttpHeaders.content_type: HttpHeaders.application_json}

    @staticmethod
    def json() -> Dict[str, str]:
        return {**HttpHeaders.accept_json(), **HttpHeaders.content_type_json()}
