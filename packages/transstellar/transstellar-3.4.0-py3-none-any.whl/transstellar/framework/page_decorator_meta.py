from .handle_page_error import handle_page_error


class PageDecoratorMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        handle_page_error(cls)
