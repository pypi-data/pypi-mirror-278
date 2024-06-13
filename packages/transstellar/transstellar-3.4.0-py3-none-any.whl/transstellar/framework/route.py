from .base_page import BasePage


class Route:
    path: str
    route_key: str
    page_class: BasePage

    def __init__(self, path: str, route_key: str, page_class: BasePage):
        if path is None:
            raise AttributeError("path should not be empty")

        if page_class is None:
            raise AttributeError("page_class should not be empty")

        self.path = path
        self.route_key = route_key
        self.page_class = page_class

    @classmethod
    def build(cls, params: dict):
        path = params.get("path")
        route_key = params.get("route_key")
        page_class = params.get("page_class")

        return Route(path, route_key, page_class)

    def get_page(self, app):
        return self.page_class(app)
