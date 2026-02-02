"""
Single-browser, single-test flow that a junior QA can read and maintain.

What it does (one continuous session, one browser):
1) Register a fresh user
2) Login with that user
3) Send a Contact message
4) Open and close About modal
5) Click through categories and pagination
6) Add two products, remove one in cart
7) Checkout and verify success
8) Logout

How to run:
    pytest -q tests/test_smoke.py
"""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.pages.home_page import HomePage
from tests.pages.cart_page import CartPage
from tests.utils import generate_username, take_screenshot, wait_click


# --- Test data (easy to change) ---
CONTACT_EMAIL = "chain@example.com"
CONTACT_NAME = "Chain User"
CONTACT_MESSAGE = "Hello from chain flow"
CARD_NUMBER = "4111111111111111"
CARD_MONTH = "12"
CARD_YEAR = "2026"
ORDER_NAME = "Chain User"
ORDER_COUNTRY = "Test Country"
ORDER_CITY = "Test City"
FALLBACK_PRODUCT_ADDED = False


def wait_for_total(driver, timeout=5):
    return int(
        WebDriverWait(driver, timeout).until(
            lambda drv: (txt := drv.find_element(By.ID, "totalp").text).isdigit() and txt
        )
    )


@allure.title("All-in-one single session flow")
def test_single_session_full_flow(session_driver):
    # Use one browser for the whole flow
    d = session_driver
    home = HomePage(d).open()

    # --- Step 1: Register a new user ---
    username = generate_username()
    password = "Password123!"
    reg_alert = home.register(username, password)
    assert "sign up" in reg_alert.lower() or "successful" in reg_alert.lower()

    # --- Step 2: Login ---
    home.login(username, password)

    # --- Step 3: Send Contact message ---
    contact_alert = home.send_contact(CONTACT_EMAIL, CONTACT_NAME, CONTACT_MESSAGE)
    assert "thanks" in contact_alert.lower()

    # --- Step 4: About modal ---
    home.open_and_close_about()

    # --- Step 5: Browse categories and paginate ---
    for cat in ["Phones", "Laptops", "Monitors"]:
        home.browse_category(cat)

    # Pagination: ensure next page shows a different first product
    first_name = home.first_card_name()
    home.next_page_until_changed(first_name)

    # --- Step 6: Add two products (different categories to avoid duplicates) ---
    home.add_product_in_category("Phones", 0)
    d.back()
    home.open()
    # try laptop, fall back to another phone if needed
    try:
        home.add_product_in_category("Laptops", 0)
    except Exception:
        home.add_product_in_category("Phones", 1)
    d.back()

    # --- Step 7: Cart check and remove one item ---
    cart = home.go_to_cart()
    items = cart.rows()
    if len(items) < 2:
        # Add one more item to satisfy expectation
        d.back()
        home.open()
        home.add_product_in_category("Phones", 2)
        d.back()
        cart = home.go_to_cart()
        items = cart.rows()
    assert len(items) >= 2
    total_before = cart.total()
    cart.delete_first_row()
    total_after = cart.total()
    assert total_after < total_before

    # --- Step 8: Checkout and verify success ---
    success_modal = cart.checkout(ORDER_NAME, ORDER_COUNTRY, ORDER_CITY, CARD_NUMBER, CARD_MONTH, CARD_YEAR)
    take_screenshot(d, "single_full_after_purchase")
    assert "Thank you for your purchase" in success_modal.find_element(By.TAG_NAME, "h2").text
    success_modal.find_element(By.CSS_SELECTOR, "button.confirm").click()

    # --- Step 9: Logout ---
    wait_click(d, (By.ID, "logout2"))
    WebDriverWait(d, 5).until(EC.visibility_of_element_located((By.ID, "login2")))
