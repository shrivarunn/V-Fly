from __future__ import annotations
from pathlib import Path
from typing import Iterable
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from utilities.config_reader import get_settings
from utilities.screenshot_utils import save_screenshot

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = get_settings()["explicit_wait_timeout"]
        self.wait = WebDriverWait(driver, self.timeout)

    def open(self, url: str):
        self.driver.get(url)
        return self

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        self.wait.until(EC.presence_of_all_elements_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, value: str, clear: bool = True):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if clear:
            element.clear()
        element.send_keys(value)
        return element

    def clear(self, locator):
        element = self.find(locator)
        element.clear()
        return element

    def select_by_value(self, locator, value: str):
        Select(self.find(locator)).select_by_value(value)

    def select_by_visible_text(self, locator, text: str):
        Select(self.find(locator)).select_by_visible_text(text)

    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_disappear(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def text(self, locator):
        return self.wait_visible(locator).text.strip()

    def attribute(self, locator, name: str):
        return self.find(locator).get_attribute(name)

    def is_enabled(self, locator):
        return self.find(locator).is_enabled()

    def is_selected(self, locator):
        return self.find(locator).is_selected()

    def switch_to_frame(self, locator):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(locator))

    def leave_frame(self):
        self.driver.switch_to.default_content()

    def accept_alert(self):
        alert = self.wait.until(EC.alert_is_present())
        message = alert.text
        alert.accept()
        return message

    def switch_to_new_window(self, previous_handles: Iterable[str] | None = None):
        previous = set(previous_handles or self.driver.window_handles)
        self.wait.until(lambda d: len(set(d.window_handles) - previous) > 0)
        self.driver.switch_to.window(next(iter(set(self.driver.window_handles) - previous)))

    def back(self):
        self.driver.back()

    def forward(self):
        self.driver.forward()

    def keyboard(self, locator, key):
        self.find(locator).send_keys(key)

    def hover(self, locator):
        ActionChains(self.driver).move_to_element(self.find(locator)).perform()

    def screenshot(self, name: str):
        return save_screenshot(self.driver, name)

    def wait_text(self, locator, expected: str):
        return self.wait.until(EC.text_to_be_present_in_element(locator, expected))

    def wait_url_contains(self, value: str):
        return self.wait.until(EC.url_contains(value))

    def current_url(self):
        return self.driver.current_url

    def title(self):
        return self.driver.title

    def navigate_when_ready(self, locator):
        """Wait for a meaningful application state before interacting with a page."""
        return self.wait_visible(locator)
