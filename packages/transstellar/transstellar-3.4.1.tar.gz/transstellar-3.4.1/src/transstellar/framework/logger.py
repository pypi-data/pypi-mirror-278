import logging


class Logger:
    class_name: str

    def __init__(self, class_name) -> None:
        self.class_name = class_name

    def debug(self, msg, *args, **kwargs):
        logging.debug(self.__get_message(msg), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        logging.info(self.__get_message(msg), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        logging.debug(self.__get_message(msg), *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        logging.debug(self.__get_message(msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        logging.debug(self.__get_message(msg), *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        logging.debug(self.__get_message(msg), *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        logging.debug(self.__get_message(msg), *args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        logging.debug(self.__get_message(msg), *args, **kwargs)

    def __get_message(self, msg: str):
        return f"[{self.class_name}] {msg}"
