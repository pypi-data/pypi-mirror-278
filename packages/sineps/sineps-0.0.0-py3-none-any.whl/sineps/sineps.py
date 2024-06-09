import requests
import requests.packages


class IntentRouter:
    def __init__(
        self, api_key: str = "", routes_info: list = [], ssl_verify: bool = True
    ):
        self.api_key = api_key
        self.routes_info = routes_info
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def test(self):
        print("Test IntentRouter")


class FilterExtractor:
    def __init__(self, api_key: str = "", ssl_verify: bool = True):
        self.api_key = api_key
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def test(self):
        print("Test IntentRouter")
