from .endpoint import Endpoint


class Service:

    def __init__(self, name, url, **endpoints):
        self.name = name
        self.url = url
        self.endpoints: dict[str, Endpoint] = endpoints
