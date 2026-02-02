from selenium.webdriver.common.by import By

from tests.utils import open_about_modal, wait_click


class AboutPage:
    def __init__(self, driver):
        self.driver = driver

    def open_and_close(self):
        open_about_modal(self.driver)
        wait_click(self.driver, (By.CSS_SELECTOR, "#videoModal .close"))
