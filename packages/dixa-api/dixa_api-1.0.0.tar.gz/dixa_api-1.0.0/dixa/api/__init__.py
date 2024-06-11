import logging
import time
from typing import Any, Literal, Mapping, TypeAlias

import requests

DixaVersion: TypeAlias = Literal["v1", "beta"]

log = logging.getLogger(__name__)


class DixaResource(object):
    """
    Resource from the dixa API. This class handles
    logging, sending requests, parsing JSON, and rate
    limiting.

    Refer to the API docs to see the expected responses.
    https://docs.dixa.io/openapi/dixa-api/v1/overview/
    """

    base_url = "https://dev.dixa.io"
    object_list_key = None
    dixa_version: DixaVersion = "v1"

    def __init__(
        self,
        session: requests.Session,
        debug: bool = False,
    ):
        self.session = session
        self.debug = debug

    def log(self, url, response):
        if self.debug:
            log.info(url)
            log.info(response.headers["X-dixa-Limit"])

    @property
    def url(self) -> str:
        return f"{self.base_url}/{self.dixa_version}/{self.object_list_key}"

    def _request(self, method, url, **kwargs):
        response = self.session.request(method, url, **kwargs)
        self.log(url, response)
        if response.status_code == 429:
            time.sleep(1)
            return self._request(method, url, **kwargs)
        return response

    def _http_delete(self, url: str, body: Mapping[str, Any] | None = None):
        return self._request("DELETE", url, json=body)

    def _http_get(self, url: str, query: Mapping[str, Any] | None = None):
        return self._request("GET", url, params=query).json()

    def _http_put(
        self,
        url: str,
        body: Mapping[str, Any] | None = None,
        query: Mapping[str, Any] | None = None,
    ):
        return self._request("PUT", url, json=body, params=query).json()

    def _http_post(
        self,
        url: str,
        body: Mapping[str, Any] | None = None,
        query: Mapping[str, Any] | None = None,
    ):
        return self._request("POST", url, json=body, params=query).json()

    def _http_patch(
        self,
        url: str,
        body: Mapping[str, Any] | None = None,
        query: Mapping[str, Any] | None = None,
    ):
        return self._request("PATCH", url, json=body, params=query).json()
