import os
import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@pytest.fixture(scope="session")
def app_credentials():
    """Loads user credentials and site config from environment variables."""

    username = os.getenv("APP_USERNAME")
    password = os.getenv("APP_PASSWORD")
    mfa_code = os.getenv("MFA_CODE")
    site_url = os.getenv("SITE_URL")
    api_url = os.getenv("API_URL")
    

    if not username or not password:
        raise pytest.UsageError(
            "Missing user credentials. Please set APP_USERNAME and APP_PASSWORD"
            "in your environment or .env file."
        )

    return username, password, mfa_code, site_url, api_url