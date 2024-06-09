import json

from .exceptions import TheSinepsApiException


class Response:
    def __init__(self, data_out: str):
        self.data_out = data_out
        self.data_out_dict = self._get_data_out_dict()

    def _get_data_out_dict(self):
        try:
            data_out_dict = json.loads(self.data_out)
        except json.JSONDecodeError as e:
            raise TheSinepsApiException("Response is not valid JSON") from e
        return data_out_dict
