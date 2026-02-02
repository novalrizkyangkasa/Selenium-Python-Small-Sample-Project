from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Base page with simple, readable helpers for juniors."""

    def __init__(self, driver):
        self.driver = driver

    def click(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).click()

    def fill(self, locator, text, timeout=10):
        field = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        field.clear()
        field.send_keys(text)

    def wait_text_in(self, locator, text, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element(locator, text))

    def wait_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def wait_alert_and_accept(self, timeout=10):
        alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        txt = alert.text
        alert.accept()
        return txt
