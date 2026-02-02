from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.pages.base_page import BasePage
from tests.utils import cart_rows, place_order, wait_for_success_modal


class CartPage(BasePage):
    """Cart interactions."""

    def __init__(self, driver):
        self.driver = driver

    def rows(self):
        return cart_rows(self.driver)

    def total(self):
        txt = WebDriverWait(self.driver, 5).until(
            lambda drv: drv.find_element(By.ID, "totalp").text
        )
        return int(txt) if txt.isdigit() else 0

    def delete_first_row(self):
        initial = len(self.driver.find_elements(By.CSS_SELECTOR, "#tbodyid tr"))
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "Delete"))).click()
        WebDriverWait(self.driver, 5).until(lambda drv: len(drv.find_elements(By.CSS_SELECTOR, "#tbodyid tr")) < initial)

    def checkout(self, name, country, city, card, month, year):
        place_order(self.driver, name, country, city, card, month, year)
        return wait_for_success_modal(self.driver)
