"""
Shared helpers for Demoblaze Selenium tests.
"""

import os
import uuid
from pathlib import Path

import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://www.demoblaze.com"
DEFAULT_DRIVER_PATH = "/Users/noval/Documents/Learn Automation Testing/chromedriver-mac-arm64/chromedriver"


# ----------------------
# Driver utilities
# ----------------------
def make_driver():
    """Create a Chrome driver with a matching binary (auto-download if needed)."""
    driver_path = os.getenv("CHROME_DRIVER_PATH") or ChromeDriverManager().install()
    service = Service(executable_path=driver_path)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.implicitly_wait(0)  # rely on explicit waits only
    return driver


# ----------------------
# Wait helpers
# ----------------------
def wait_click(driver, locator, timeout=10):
    """Wait until element is clickable, then click."""
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator)).click()


def wait_fill(driver, locator, text, timeout=10):
    """Wait until field visible, clear it, then type text."""
    field = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
    field.clear()
    field.send_keys(text)


def wait_alert_text_and_accept(driver, timeout=10):
    """Wait for alert, grab its text, accept it, return text."""
    alert = WebDriverWait(driver, timeout).until(EC.alert_is_present())
    text = alert.text
    alert.accept()
    return text


# ----------------------
# Actions
# ----------------------
def take_screenshot(driver, name: str):
    """Save screenshot to screenshots/ and attach to Allure."""
    screenshots_dir = ROOT / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    path = screenshots_dir / f"{name}.png"
    driver.get_screenshot_as_file(str(path))
    allure.attach.file(str(path), name=name, attachment_type=allure.attachment_type.PNG)


def open_home(driver):
    """Open Demoblaze home and wait for URL to contain 'demoblaze'."""
    driver.get(BASE_URL)
    WebDriverWait(driver, 10).until(EC.url_contains("demoblaze"))


def login(driver, username: str, password: str):
    """Open login modal and sign in with given credentials."""
    wait_click(driver, (By.ID, "login2"))
    wait_fill(driver, (By.ID, "loginusername"), username)
    wait_fill(driver, (By.ID, "loginpassword"), password)
    wait_click(driver, (By.XPATH, "//div[@id='logInModal']//button[text()='Log in']"))
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "nameofuser"), f"Welcome {username}")
    )


def add_first_product_to_cart(driver):
    """Open first product on page and add it to cart."""
    # Open first product card
    wait_click(driver, (By.CSS_SELECTOR, "#tbodyid .card a[href*='prod.html']"))
    wait_click(driver, (By.XPATH, "//a[text()='Add to cart']"))
    alert_text = wait_alert_text_and_accept(driver)
    return alert_text


def add_product_by_index(driver, index: int = 0):
    """Open product by index on current page and add it to cart."""
    cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#tbodyid .card"))
    )
    cards[index].find_element(By.CSS_SELECTOR, "a[href*='prod.html']").click()
    wait_click(driver, (By.XPATH, "//a[text()='Add to cart']"))
    return wait_alert_text_and_accept(driver)


def go_to_cart(driver):
    """Navigate to cart page and wait for URL update."""
    wait_click(driver, (By.ID, "cartur"))
    WebDriverWait(driver, 10).until(EC.url_contains("cart"))


def cart_rows(driver):
    """Return list of cart rows with title, price, and row element."""
    rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#tbodyid tr"))
    )
    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 3:
            title = cells[1].text.strip()
            price_txt = cells[2].text.strip()
            price = int(price_txt) if price_txt.isdigit() else 0
            data.append({"title": title, "price": price, "row": row})
    return data


def delete_first_cart_row(driver):
    """Delete the first cart row."""
    rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#tbodyid tr"))
    )
    rows[0].find_element(By.LINK_TEXT, "Delete").click()
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element(rows[0])
    )


def open_category(driver, name: str):
    """Click a category link."""
    wait_click(driver, (By.LINK_TEXT, name))
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#tbodyid"), "")
    )


def open_contact_modal(driver):
    """Open Contact modal."""
    wait_click(driver, (By.LINK_TEXT, "Contact"))
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "exampleModal"))
    )


def submit_contact_form(driver, email: str, name: str, message: str):
    """Fill Contact form and return alert text."""
    wait_fill(driver, (By.ID, "recipient-email"), email)
    wait_fill(driver, (By.ID, "recipient-name"), name)
    wait_fill(driver, (By.ID, "message-text"), message)
    wait_click(driver, (By.XPATH, "//div[@id='exampleModal']//button[text()='Send message']"))
    return wait_alert_text_and_accept(driver)


def open_about_modal(driver):
    """Open About modal with video."""
    wait_click(driver, (By.LINK_TEXT, "About us"))
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "videoModal"))
    )


def close_visible_modal(driver):
    """Close whichever modal is currently shown."""
    wait_click(driver, (By.CSS_SELECTOR, ".modal.show button.close"))
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal.show"))
    )


def place_order(driver, name, country, city, card, month, year):
    """Open Place Order dialog, fill fields, click Purchase."""
    wait_click(driver, (By.XPATH, "//button[text()='Place Order']"))
    wait_fill(driver, (By.ID, "name"), name)
    wait_fill(driver, (By.ID, "country"), country)
    wait_fill(driver, (By.ID, "city"), city)
    wait_fill(driver, (By.ID, "card"), card)
    wait_fill(driver, (By.ID, "month"), month)
    wait_fill(driver, (By.ID, "year"), year)
    wait_click(driver, (By.XPATH, "//button[text()='Purchase']"))


def wait_for_success_modal(driver):
    """Wait for SweetAlert success modal and return it."""
    return WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.sweet-alert.showSweetAlert.visible"))
    )


def register_user_via_ui(username: str, password: str):
    """Register a user in a short-lived browser session and return alert text."""
    driver = make_driver()
    try:
        open_home(driver)
        wait_click(driver, (By.ID, "signin2"))
        wait_fill(driver, (By.ID, "sign-username"), username)
        wait_fill(driver, (By.ID, "sign-password"), password)
        wait_click(driver, (By.XPATH, "//div[@id='signInModal']//button[text()='Sign up']"))
        alert_text = wait_alert_text_and_accept(driver)
        take_screenshot(driver, f"registration_{username}")
        return alert_text
    finally:
        driver.quit()


def generate_username():
    return f"autouser_{uuid.uuid4().hex[:8]}"


def register_user_inline(driver, username: str, password: str):
    """Register using the current driver session (no new browser)."""
    open_home(driver)
    wait_click(driver, (By.ID, "signin2"))
    wait_fill(driver, (By.ID, "sign-username"), username)
    wait_fill(driver, (By.ID, "sign-password"), password)
    wait_click(driver, (By.XPATH, "//div[@id='signInModal']//button[text()='Sign up']"))
    return wait_alert_text_and_accept(driver)
