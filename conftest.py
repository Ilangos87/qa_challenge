import os
import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@pytest.fixture(scope="session")
def app_credentials():
    """Loads user credentials and site config from environment variables."""

    def get_env(name: str) -> str:
        value = os.getenv(name)
        return value.strip()

    username = get_env("APP_USERNAME")
    password = get_env("APP_PASSWORD")
    mfa_code = get_env("MFA_CODE")
    site_url = get_env("SITE_URL")
    api_url = get_env("API_URL")
    

    if not username or not password:
        raise pytest.UsageError(
            "Missing user credentials. Please set APP_USERNAME and APP_PASSWORD"
            "in your environment or .env file."
        )

    return username, password, mfa_code, site_url, api_url