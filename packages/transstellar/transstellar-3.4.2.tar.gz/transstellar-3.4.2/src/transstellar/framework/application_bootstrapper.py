from .application import Application


class ApplicationBootstrapper:
    def create_app(self, params: dict):
        application = Application(params)
        self.bootstrap(application)

        return application

    def bootstrap(self, app: Application):
        pass
