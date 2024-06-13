import yaml

class ConfigService():
    _instance = None
    config = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigService, cls).__new__(cls)
            with open('config.yml') as config_file:
                cls._instance.config = yaml.safe_load(config_file)

        return cls._instance

    def get_config(self):
        return self._instance.config
