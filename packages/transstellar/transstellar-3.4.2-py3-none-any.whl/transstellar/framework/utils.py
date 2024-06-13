import os

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_for_element(driver, condition, timeout=10) -> WebElement:
    try:
        return WebDriverWait(driver, timeout).until(condition)
    except Exception as e:
        screenshot_path = os.path.join(os.getcwd(), "screenshots/wait_exception.png")

        driver.save_screenshot(screenshot_path)

        raise e


def wait_for_element_by_xpath(driver, xpath: str, timeout=10) -> WebElement:
    return wait_for_element(
        driver, EC.visibility_of_element_located((By.XPATH, xpath)), timeout
    )


def wait_for_element_by_selector(driver, css_selector: str, timeout=10) -> WebElement:
    return wait_for_element(
        driver,
        EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)),
        timeout,
    )


def wait_for_element_to_disappear_by_xpath(
    driver, xpath: str, timeout=10
) -> WebElement:
    return WebDriverWait(driver, timeout).until(
        EC.invisibility_of_element_located((By.XPATH, xpath))
    )


def wait_for_element_to_click_by_xpath(driver, xpath: str, timeout=10):
    return wait_for_element(
        driver, EC.element_to_be_clickable((By.XPATH, xpath)), timeout
    )
