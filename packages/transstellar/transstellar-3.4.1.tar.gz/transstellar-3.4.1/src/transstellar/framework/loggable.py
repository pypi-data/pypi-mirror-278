from .logger import Logger


class Loggable:
    logger: Logger

    def __init__(self) -> None:
        self.logger = Logger(self.__class__.__name__)
