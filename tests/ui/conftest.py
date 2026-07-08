import pytest
from pages.login_page import LoginPage
from utils.ui_helper import enter_mfa


@pytest.fixture(scope="session")
def storage_state(app_credentials, browser):
    """Logs in once and saves authenticated storage state for reuse."""
    username, password, mfa_code, site_url, api_url = app_credentials

    page = browser.new_page()
    login_page = LoginPage(page)
    login_page.open(site_url)
    login_page.enter_credentials(username, password)
    enter_mfa(page, mfa_code)

    page.context.storage_state(path="storage_state.json")
    page.close()
    return "storage_state.json"


@pytest.fixture(scope="session")
def browser_instance(browser):
    """Reuses the plugin-provided browser for the whole test session."""

    yield browser
    browser.close()


@pytest.fixture
def reuse_storage_state(storage_state, browser_instance, app_credentials):
    """Provides a fresh authenticated page per test using saved state."""
    
    _, _, mfa_code, site_url, _ = app_credentials
    context = browser_instance.new_context(storage_state=storage_state)
    page = context.new_page()
    yield page, mfa_code, site_url
    context.close()
