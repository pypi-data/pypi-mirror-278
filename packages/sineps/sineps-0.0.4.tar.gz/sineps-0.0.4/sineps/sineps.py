import requests
import requests.packages
import json

from .exceptions import TheSinepsApiException
from .utils import *
from .intent_router import IntentRouterResponse
from .filter_extractor import FilterExtractorResponse


class Client:
    def __init__(self, api_key: str = "", ver: str = "v1", ssl_verify: bool = True):
        self.url = f"https://api.sineps.io/{ver}/"
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def _do(self, endpoint: str, body: dict = {}):
        full_url = self.url + endpoint
        headers = {"Content-Type": "application/json", "api-key": self._api_key}
        try:
            response = requests.post(
                full_url, headers=headers, json=body, verify=self._ssl_verify
            )
        except requests.exceptions.RequestException as e:
            raise TheSinepsApiException("Request failed") from e
        if response.status_code != 200:
            raise Exception(response.reason)
        else:
            data_out = response.text
            return data_out

    def exec_intent_router(
        self, query: str, routes: list = [], allow_none: bool = False
    ):
        routes = add_index_to_dictionary_list(routes)
        if allow_none:
            option = "single_none"
        else:
            option = "single"
        body = {"query": query, "routes": routes, "option": option}
        return IntentRouterResponse(
            data_out=self._do("intent-router", body), all_routes=routes
        )

    def exec_filter_extractor(self, query: str, field: dict = {}):
        field = uppercase_keys(field)
        field_str = json.dumps(field)
        body = {"natural_language_query": query, "metadata_schema": field_str}
        return FilterExtractorResponse(self._do("filter-extractor", body))
