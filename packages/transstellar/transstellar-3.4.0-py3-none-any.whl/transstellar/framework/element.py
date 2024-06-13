import os
import time
from typing import Type, TypeVar

from injector import Injector
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .loggable import Loggable
from .utils import (
    wait_for_element_by_selector,
    wait_for_element_by_xpath,
    wait_for_element_to_click_by_xpath,
    wait_for_element_to_disappear_by_xpath,
)

T = TypeVar("T")


class Element(Loggable):
    XPATH_CURRENT = None

    label = ""
    app = None
    injector: Injector
    driver: WebDriver
    dom_element: WebElement = None

    def __init__(self, app) -> None:
        super().__init__()
        self.app = app
        self.injector = app.container
        self.driver = app.driver
        self.init()

    def init(self):
        pass

    def init_after_dom_element_is_set(self):
        pass

    @classmethod
    def get_current_element_xpath(cls):
        if not cls.XPATH_CURRENT:
            raise AssertionError(
                f"{cls.__name__} should set XPATH_CURRENT in order to get element"
            )

        return cls.XPATH_CURRENT

    def wait_for_ready(self):
        pass

    def find_global_element(self, target_element_class: Type[T]) -> T:
        self.logger.debug(f"finding global element for {target_element_class.__name__}")

        target_element_xpath = target_element_class.get_current_element_xpath()
        element = self.find_global_dom_element_by_xpath(target_element_xpath)

        if element:
            return self.__create_child_element(target_element_class, element)
        else:
            raise LookupError(
                f"Could not find element of {target_element_class.__name__}"
            )

    def click(self):
        self.get_current_dom_element().click()

    def refresh(self):
        self.logger.debug("refresh current element")

        xpath = self.get_current_element_xpath()
        dom_element = self.find_global_dom_element_by_xpath(xpath)

        self.set_current_dom_element(dom_element)

        return self.get_current_dom_element()

    def find_element(self, target_element_class: Type[T]) -> T:
        self.logger.debug(f"find element: {target_element_class.__name__}")

        current_dom_element = self.get_current_dom_element()
        target_element_xpath = target_element_class.get_current_element_xpath()
        element = current_dom_element.find_element(By.XPATH, f".{target_element_xpath}")

        # refactor

        if element:
            return self.__create_child_element(target_element_class, element)
        else:
            raise LookupError(
                f"Could not find element of {target_element_class.__name__}"
            )

    def find_elements(self, target_element_class):
        self.logger.debug(f"find elements: {target_element_class.__name__}")

        current_dom_element = self.get_current_dom_element()
        target_element_xpath = target_element_class.get_current_element_xpath()
        elements = current_dom_element.find_elements(
            By.XPATH, f".{target_element_xpath}"
        )

        if len(elements) > 0:
            return list(
                map(
                    lambda element: self.__create_child_element(
                        target_element_class, element
                    ),
                    elements,
                )
            )
        else:
            raise LookupError(
                f"Could not find elements of {target_element_class.__name__}"
            )

    def find_element_by_label(self, target_element_class: Type[T], label: str) -> T:
        self.logger.debug(
            f"find element ({target_element_class.__name__}) by label: {label}"
        )

        current_dom_element = self.get_current_dom_element()
        target_element_xpath = target_element_class.get_current_element_xpath()
        element = current_dom_element.find_element(
            By.XPATH, f'.{target_element_xpath}[contains(.//text(), "{label}")]'
        )

        if element:
            return self.__create_child_element(target_element_class, element, label)
        else:
            raise LookupError(
                f"Could not find element of {target_element_class.__name__} with label: {label}"
            )

    def wait_for_global_element_to_disappear(self, target_element_class):
        self.logger.debug(
            f"wait for global element to dissapear: {target_element_class.__name__}"
        )

        target_element_xpath = target_element_class.get_current_element_xpath()

        return wait_for_element_to_disappear_by_xpath(
            self.driver, f".{target_element_xpath}"
        )

    def get_current_dom_element(self) -> WebElement:
        if self.dom_element:
            return self.dom_element

        xpath = self.get_current_element_xpath()
        dom_element = self.find_global_dom_element_by_xpath(xpath)

        self.set_current_dom_element(dom_element)

        return self.dom_element

    def get_current_html(self):
        html = self.get_current_dom_element().get_attribute("outerHTML")

        self.logger.debug(f"current HTML: {html}")

        return html

    def find_global_dom_element_by_xpath(self, xpath: str):
        self.logger.debug(f"finding global dom element by xpath: {xpath}")

        return wait_for_element_by_xpath(self.driver, xpath)

    def find_dom_elements_by_tag_name(self, tag_name: str):
        self.logger.debug(f"finding dom element by tag name: {tag_name}")

        dom_element = self.get_current_dom_element()

        return dom_element.find_elements(By.XPATH, f".//{tag_name}")

    def find_dom_element_by_xpath(self, xpath: str):
        self.logger.debug(f"finding dom element by xpath: {xpath}")

        dom_element = self.get_current_dom_element()

        return dom_element.find_element(By.XPATH, f".{xpath}")

    def wait_for_dom_element_to_disappear_by_xpath(self, xpath: str, timeout: int = 10):
        self.logger.debug(f"wait for dom element to disappear by xpath: {xpath}")

        return wait_for_element_to_disappear_by_xpath(self.driver, f".{xpath}", timeout)

    def wait_for_dom_element_to_click_by_xpath(self, xpath: str, timeout: int = 10):
        self.logger.debug(f"wait for dom element to click by xpath: {xpath}")

        return wait_for_element_to_click_by_xpath(self.driver, f".{xpath}", timeout)

    def wait_for_dom_element_by_selector(self, css_selector, timeout: int = 10):
        self.logger.debug(f"wait for dom element by CSS selector: {css_selector}")

        return wait_for_element_by_selector(self.driver, css_selector, timeout)

    def screenshot(self, file_name):
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")

        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        screenshot_path = os.path.join(os.getcwd(), f"screenshots/{file_name}")

        self.driver.save_screenshot(screenshot_path)

    def sleep(self, seconds: float):
        self.logger.debug(f"sleep: {seconds} seconds")

        time.sleep(seconds)

    def set_current_dom_element(self, element):
        self.dom_element = element

        self.init_after_dom_element_is_set()

    def scroll_to_view(self):
        self.app.driver.execute_script(
            "arguments[0].scrollIntoView(false);", self.dom_element
        )

    def __create_child_element(
        self, child_element_class: Type[T], child_dom_element, label: str = ""
    ) -> T:
        child_element = child_element_class(self.app)
        child_element.set_current_dom_element(child_dom_element)

        if label:
            child_element.label = label

        return child_element
