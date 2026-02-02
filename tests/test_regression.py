"""
Regression-style coverage (multiple smaller UI checks).
Run: pytest -q tests/test_regression.py
"""

import pytest
import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .utils import (
    add_first_product_to_cart,
    add_product_by_index,
    cart_rows,
    close_visible_modal,
    delete_first_cart_row,
    go_to_cart,
    login,
    open_about_modal,
    open_category,
    open_contact_modal,
    open_home,
    submit_contact_form,
    take_screenshot,
    wait_click,
    wait_fill,
    wait_for_success_modal,
)


@pytest.mark.regression
@allure.title("Contact form happy path shows thanks alert")
def test_contact_form_success(driver):
    open_home(driver)
    open_contact_modal(driver)
    alert_text = submit_contact_form(driver, "qa@example.com", "QA User", "Hello!")
    assert "thanks" in alert_text.lower()


@pytest.mark.xfail(reason="Site may allow blank contact submissions", strict=False)
@pytest.mark.regression
@allure.title("Contact form with blanks should not succeed")
def test_contact_form_validation(driver):
    open_home(driver)
    open_contact_modal(driver)
    wait_click(driver, (By.XPATH, "//div[@id='exampleModal']//button[text()='Send message']"))
    alert_text = submit_contact_form(driver, "", "", "")
    assert "thanks" not in alert_text.lower()


@pytest.mark.regression
@allure.title("About modal opens and can be closed")
def test_about_modal(driver):
    open_home(driver)
    open_about_modal(driver)
    modal = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "videoModal")))
    assert modal.is_displayed()
    close_visible_modal(driver)


@pytest.mark.regression
@allure.title("Sign-up existing user shows error alert")
def wait_for_alert(driver, timeout=10):
    WebDriverWait(driver, timeout).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    text = alert.text
    alert.accept()
    return text


# Reuse wait_for_alert for sign-up test
@pytest.mark.regression
def test_signup_existing_user(fresh_user, driver):  # noqa: F811
    open_home(driver)
    wait_click(driver, (By.ID, "signin2"))
    wait_fill(driver, (By.ID, "sign-username"), fresh_user["username"])
    wait_fill(driver, (By.ID, "sign-password"), fresh_user["password"])
    wait_click(driver, (By.XPATH, "//div[@id='signInModal']//button[text()='Sign up']"))
    alert_text = wait_for_alert(driver)
    assert "exist" in alert_text.lower()


@pytest.mark.regression
@allure.title("Login fails with wrong password")
def test_login_wrong_password(fresh_user, driver):
    open_home(driver)
    wait_click(driver, (By.ID, "login2"))
    wait_fill(driver, (By.ID, "loginusername"), fresh_user["username"])
    wait_fill(driver, (By.ID, "loginpassword"), "WrongPass!")
    wait_click(driver, (By.XPATH, "//div[@id='logInModal']//button[text()='Log in']"))
    alert_text = wait_for_alert(driver)
    assert "wrong" in alert_text.lower()


@pytest.mark.regression
@allure.title("Logout restores login buttons and hides welcome banner")
def test_logout_visibility(fresh_user, driver):
    open_home(driver)
    login(driver, fresh_user["username"], fresh_user["password"])
    wait_click(driver, (By.ID, "logout2"))
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "login2")))
    WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.ID, "nameofuser")))


@pytest.mark.regression
@allure.title("Category filters change product lists")
@pytest.mark.parametrize("category", ["Phones", "Laptops", "Monitors"])
def test_category_filtering(category, driver):
    open_home(driver)
    open_category(driver, category)
    cards = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#tbodyid .card-title"))
    )
    assert len(cards) > 0


@pytest.mark.regression
@allure.title("Pagination changes first product")
def test_pagination_next_prev(driver):
    open_home(driver)
    first_card = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#tbodyid .card-title"))
    )
    first_name = first_card.text
    next_btn = driver.find_element(By.ID, "next2")
    driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
    next_btn.click()
    WebDriverWait(driver, 8).until(
        lambda d: d.find_element(By.CSS_SELECTOR, "#tbodyid .card-title").text != first_name
    )
    second_name = driver.find_element(By.CSS_SELECTOR, "#tbodyid .card-title").text
    assert first_name != second_name
    wait_click(driver, (By.ID, "prev2"))
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#tbodyid .card-title"))
    )


@pytest.mark.regression
@allure.title("Add multiple items and remove one updates cart total")
def test_add_multiple_and_remove(fresh_user, driver):
    open_home(driver)
    login(driver, fresh_user["username"], fresh_user["password"])
    add_product_by_index(driver, 0)
    driver.back()
    open_home(driver)
    add_product_by_index(driver, 1)
    driver.back()

    go_to_cart(driver)
    items = cart_rows(driver)
    assert len(items) >= 2

    total_before = driver.find_element(By.ID, "totalp").text
    delete_first_cart_row(driver)
    WebDriverWait(driver, 5).until(lambda d: len(cart_rows(d)) == len(items) - 1)
    total_after = driver.find_element(By.ID, "totalp").text
    assert int(total_after) < int(total_before)


@pytest.mark.regression
@allure.title("Place Order requires fields (expected fail tolerated)")
@pytest.mark.xfail(reason="Site often allows blank purchase", strict=False)
def test_place_order_requires_fields(fresh_user, driver):
    open_home(driver)
    login(driver, fresh_user["username"], fresh_user["password"])
    add_first_product_to_cart(driver)
    go_to_cart(driver)
    wait_click(driver, (By.XPATH, "//button[text()='Place Order']"))
    wait_click(driver, (By.XPATH, "//button[text()='Purchase']"))
    with pytest.raises(TimeoutException):
        wait_for_success_modal(driver)
