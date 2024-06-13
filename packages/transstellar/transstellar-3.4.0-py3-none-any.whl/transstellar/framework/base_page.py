from urllib.parse import ParseResult, urlparse, urlunparse

from .element import Element
from .page_decorator_meta import PageDecoratorMeta


class BasePage(Element, metaclass=PageDecoratorMeta):
    XPATH_CURRENT = "//body"
