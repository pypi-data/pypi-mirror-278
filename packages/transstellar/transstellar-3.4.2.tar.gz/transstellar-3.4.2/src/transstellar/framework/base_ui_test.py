import os

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from .base_test import BaseTest
from .utils import (
    wait_for_element_by_selector,
    wait_for_element_by_xpath,
    wait_for_element_to_click_by_xpath,
    wait_for_element_to_disappear_by_xpath,
)


@pytest.mark.UI
class BaseUITest(BaseTest):
    driver: WebDriver

    @pytest.fixture(autouse=True)
    def setup_method_framework_base_ui(self):
        self.app.init_e2e()
        self.driver = self.app.driver

    def screenshot(self, file_name):
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")

        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        screenshot_path = os.path.join(os.getcwd(), f"screenshots/{file_name}")

        self.driver.save_screenshot(screenshot_path)

    def wait_for_dom_element_by_xpath(self, xpath):
        return wait_for_element_by_xpath(self.driver, xpath)

    def wait_for_dom_element_to_disappear_by_xpath(self, xpath):
        return wait_for_element_to_disappear_by_xpath(self.driver, xpath)

    def wait_for_dom_element_to_click_by_xpath(self, xpath):
        return wait_for_element_to_click_by_xpath(self.driver, xpath)

    def wait_for_dom_element_by_selector(self, css_selector):
        return wait_for_element_by_selector(self.driver, css_selector)
