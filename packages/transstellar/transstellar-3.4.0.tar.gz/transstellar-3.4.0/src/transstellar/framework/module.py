from abc import ABC, abstractmethod

from .loggable import Loggable


class Module(Loggable, ABC):
    app = None

    def __init__(self, app) -> None:
        super().__init__()

        self.app = app

        self.bootstrap()

    @abstractmethod
    def bootstrap(self):
        pass
