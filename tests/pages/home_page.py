from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.pages.base_page import BasePage
from tests.utils import (
    add_product_by_index,
    open_about_modal,
    open_category,
    open_contact_modal,
    open_home,
    submit_contact_form,
    wait_click,
)


class HomePage(BasePage):
    """Landing page and shared header actions."""

    def open(self):
        open_home(self.driver)
        return self

    # Auth flows
    def register(self, username: str, password: str) -> str:
        self.click((By.ID, "signin2"))
        self.fill((By.ID, "sign-username"), username)
        self.fill((By.ID, "sign-password"), password)
        self.click((By.XPATH, "//div[@id='signInModal']//button[text()='Sign up']"))
        return self.wait_alert_and_accept()

    def login(self, username: str, password: str):
        self.click((By.ID, "login2"))
        self.fill((By.ID, "loginusername"), username)
        self.fill((By.ID, "loginpassword"), password)
        self.click((By.XPATH, "//div[@id='logInModal']//button[text()='Log in']"))
        self.wait_text_in((By.ID, "nameofuser"), f"Welcome {username}")
        return self

    def logout(self):
        self.click((By.ID, "logout2"))
        return self

    # Header modals
    def send_contact(self, email, name, message) -> str:
        open_contact_modal(self.driver)
        return submit_contact_form(self.driver, email, name, message)

    def open_and_close_about(self):
        open_about_modal(self.driver)
        self.click((By.CSS_SELECTOR, "#videoModal .close"))

    # Catalog actions
    def browse_category(self, name: str):
        open_category(self.driver, name)
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#tbodyid .card"))
        )
        return self

    def first_card_name(self) -> str:
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#tbodyid .card-title"))
        ).text

    def next_page_until_changed(self, current_first: str):
        next_btn = self.driver.find_element(By.ID, "next2")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
        next_btn.click()
        WebDriverWait(self.driver, 8).until(
            lambda drv: drv.find_element(By.CSS_SELECTOR, "#tbodyid .card-title").text != current_first
        )

    def add_product_in_category(self, category: str, index: int = 0) -> str:
        self.browse_category(category)
        alert_text = add_product_by_index(self.driver, index)
        return alert_text

    def go_to_cart(self):
        wait_click(self.driver, (By.ID, "cartur"))
        WebDriverWait(self.driver, 10).until(EC.url_contains("cart"))
        from .cart_page import CartPage

        return CartPage(self.driver)
