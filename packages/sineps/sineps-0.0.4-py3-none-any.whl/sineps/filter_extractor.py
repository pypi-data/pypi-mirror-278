import json

from .exceptions import TheSinepsApiException
from .response import Response


class FilterExtractorResponse(Response):
    def __init__(self, data_out: str):
        super().__init__(data_out)
        self.filter = self._get_filter()

    def _get_filter(self):
        filter_str = self.data_out_dict["result"]
        try:
            filter = json.loads(filter_str)
        except json.JSONDecodeError as e:
            raise TheSinepsApiException(
                "The filter in the response is not valid JSON"
            ) from e
        return filter
