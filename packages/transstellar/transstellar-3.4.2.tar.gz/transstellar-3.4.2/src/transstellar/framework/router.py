import array

from transstellar.framework.loggable import Loggable

from .main_config import MainConfig
from .route import Route


class Router(Loggable):
    app: None
    routes: dict = {}

    def __init__(self, app):
        super().__init__()

        self.app = app

    def register_routes(self, routes: array):
        if routes is None:
            return

        for route in routes:
            self.register_route(route)

    def register_route(self, route: Route):
        if not isinstance(route, Route):
            raise TypeError("route is not a Route instance")

        self.routes[route.route_key] = route

    def get_route(self, route_key: str):
        route = self.routes.get(route_key)

        if route is None:
            raise LookupError(f'Route "{route_key}" not found')

        return route

    def get_page(self, route_key: str):
        route = self.get_route(route_key)

        page = route.get_page(self.app)
        page.wait_for_ready()

        return page

    def build_page(self, page_class):
        return page_class(self)

    def go_to_url(self, url: str):
        if url != self.app.driver.current_url:
            self.logger.info("Go to url: %s", url)
            self.app.driver.get(url)

    def go_to(self, route_key: str, path_params: dict = None):
        route = self.get_route(route_key)
        main_config = self.app.get(MainConfig)

        base_url = main_config.get_app_url()
        path = route.path

        if path_params:
            path = path.format(**path_params)

        url = f"{base_url}{path}"

        self.go_to_url(url)

        page = route.get_page(self.app)

        return page
