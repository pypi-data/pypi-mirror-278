from typing import List

from .response import Response


class Route:
    def __init__(
        self, index: int, name: str, description: str, utterances: List[str], **kwargs
    ):
        self.index = index
        self.name = name
        self.description = description
        self.utterances = utterances
        self.__dict__.update(kwargs)


class Routes:
    def __init__(self, routes: List[Route]):
        self.routes = routes


class IntentRouterResponse(Response):
    def __init__(self, data_out: str, all_routes: List[dict]):
        super().__init__(data_out)
        self.all_routes = all_routes
        self.chosen = self._get_chosen()

    def _get_chosen(self):
        chosen_route_index = self.data_out_dict["result"]
        chosen = Routes(
            routes=[Route(**self.all_routes[i]) for i in chosen_route_index]
        )
        return chosen
