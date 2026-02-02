"""
Common fixtures for the Demoblaze test suite.
"""

import os
import pytest

from .utils import (
    generate_username,
    make_driver,
    register_user_via_ui,
)


@pytest.fixture(scope="function")
def driver():
    """Fresh browser per test to avoid cross-test leakage."""
    drv = make_driver()
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def session_driver():
    """Single browser reused across chained E2E flow."""
    drv = make_driver()
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def fresh_user():
    """
    Provide credentials valid for this test session.
    - If TEST_USERNAME/TEST_PASSWORD are set, reuse them.
    - Otherwise register a unique user once per session.
    """
    env_user = os.getenv("TEST_USERNAME")
    env_pass = os.getenv("TEST_PASSWORD")
    if env_user and env_pass:
        return {"username": env_user, "password": env_pass, "alert_text": "using env credentials"}

    username = generate_username()
    password = "Password123!"
    alert_text = register_user_via_ui(username, password)
    return {"username": username, "password": password, "alert_text": alert_text}
