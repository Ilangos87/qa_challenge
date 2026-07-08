from utils.api_helper import assert_masked_value
from pages.account_page import AccountPage
from utils.ui_helper import enter_mfa


def test_valid_banking_update(client):
    payload = {"routing_number": "123456789", "account_number": "987654321"}
    r = client.put("/account/banking", payload)
    assert r.status_code == 200
    data = r.json()
    assert_masked_value(data["routing_masked"], payload["routing_number"])
    assert_masked_value(data["account_masked"], payload["account_number"])


def test_valid_banking_update_with_missing_token(client):
    payload = {"routing_number": "123456789", "account_number": "987654321"}
    r = client.put("/account/banking", payload, token_override="Missing")
    assert r.status_code == 401
    data = r.json()
    assert data["error"] == "Missing Authorization: Bearer <token> header"


def test_valid_banking_update_with_invalid_token(client):
    payload = {"routing_number": "123456789", "account_number": "987654321"}
    r = client.put("/account/banking", payload, token_override="Invalid")
    assert r.status_code == 401
    data = r.json()
    assert data["error"] == "Invalid or expired token"
    # Assert sensitive fields are NOT leaked
    for field in ("routing_number", "account_number"):
        assert field not in data


def test_routing_no_less_than_9_digits(client):
    payload = {"routing_number": "12345678", "account_number": "987654321"}
    r = client.put("/account/banking", payload)
    assert r.status_code == 400
    data = r.json()
    assert data["error"] == "Routing number must be 9 digits"


def test_routing_no_less_than_4_digits(client):
    payload = {"routing_number": "123456789", "account_number": "123"}
    r = client.put("/account/banking", payload)
    assert r.status_code == 400
    data = r.json()
    assert data["error"] == "Account number must be 4-17 digits"
  

def test_valid_card_details_update(client):
    payload = {"cardholder_name":"John","card_number":"4242424242424242","exp_month":12,"exp_year":2026,"cvc":"123"}
    r = client.put("/account/payment", payload)
    assert r.status_code == 200
    data = r.json()
    assert data["last4"] == payload["card_number"][-4:]
    assert data["exp_month"] == payload["exp_month"]
    assert data["exp_year"] == payload["exp_year"]


def test_card_no_check(client):
    payload = {"cardholder_name":"John","card_number":"5343434343424","exp_month":12,"exp_year":2026,"cvc":"123"}
    r = client.put("/account/payment", payload)
    assert r.status_code == 400
    data = r.json()
    assert data["error"] == "Invalid card number"
  
  
def test_cross_layer_check(client, reuse_storage_state):
    payload = {"routing_number": "123456789", "account_number": "987654321"}
    r = client.put("/account/banking", payload)
    assert r.status_code == 200
    data = r.json()
    assert_masked_value(data["routing_masked"], payload["routing_number"])
    assert_masked_value(data["account_masked"], payload["account_number"])
   
    page, mfa_code,site_url = reuse_storage_state
    account_page = AccountPage(page, site_url)
    account_page.open()
    enter_mfa(page, mfa_code)
    account_page.click_account_tab()
    account_page.verify_bank_last_updated_summary(payload["routing_number"], payload["account_number"])