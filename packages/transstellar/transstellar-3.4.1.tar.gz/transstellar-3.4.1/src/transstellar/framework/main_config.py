from injector import inject

from .config_service import ConfigService


class MainConfig:
    @inject
    def __init__(self, config_service: ConfigService):
        self.config = config_service.config

    def get_app_url(self):
        return self.config["app"]["app_url"]

    def get_api_url(self):
        return self.config["api"]["api_url"]
