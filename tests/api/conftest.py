import pytest
from clients.api_client import APIClient
from tests.ui.conftest import (
    storage_state,
    browser_instance,
    reuse_storage_state as ui_reuse_storage_state,
)

@pytest.fixture
def client(app_credentials):
    """Provides an authenticated API client using app credentials."""
    
    username, password, mfa_code, site_url, api_url = app_credentials
    c = APIClient(api_url, username, password, mfa_code)
    c.authenticate()
    return c


@pytest.fixture
def reuse_storage_state(ui_reuse_storage_state):
    """Reuses the UI storage state fixture for API tests."""

    return ui_reuse_storage_state
