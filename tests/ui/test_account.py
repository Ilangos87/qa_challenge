from pages.account_page import AccountPage
from utils.ui_helper import enter_mfa


def test_valid_banking_details(reuse_storage_state):
    routing_no = "123456789"
    account_no = "1234"
    page, mfa_code,site_url = reuse_storage_state
    account_page = AccountPage(page, site_url)
    account_page.open()
    enter_mfa(page, mfa_code)
    account_page.click_account_tab()
    account_page.submit_banking_details(routing_no, account_no)  
    account_page.save_banking_details()
    account_page.verify_bank_last_updated_summary(routing_no, account_no)  


def test_routing_no_less_than_9_digits(reuse_storage_state):
    routing_no = "12345678"
    account_no = "1234"
    page, mfa_code,site_url = reuse_storage_state
    account_page = AccountPage(page, site_url)
    account_page.open()
    enter_mfa(page, mfa_code)
    account_page.click_account_tab()
    account_page.submit_banking_details(routing_no, account_no)  
    account_page.save_banking_details()
    account_page.verify_toast_message(f"Routing number must be exactly 9 digits")

def test_account_no_less_than_4_digits(reuse_storage_state):
    routing_no = "123456789"
    account_no = "123"
    page, mfa_code,site_url = reuse_storage_state
    account_page = AccountPage(page, site_url)
    account_page.open()
    enter_mfa(page, mfa_code)
    account_page.click_account_tab()
    account_page.submit_banking_details(routing_no, account_no)  
    account_page.save_banking_details()
    account_page.verify_toast_message(f"Account number must be 4 to 17 digits")


def test_valid_payment_details(reuse_storage_state):
    card_owner = "John Doe"
    card_no = "4242 4242 4242 4242"
    card_month = "12"
    card_year = "2026"
    card_cvc = "123"
    page, mfa_code,site_url = reuse_storage_state
    account_page = AccountPage(page, site_url)
    account_page.open()
    enter_mfa(page, mfa_code)
    account_page.click_account_tab()
    account_page.submit_payment_details(card_owner, card_no, card_month, card_year, card_cvc)    
    account_page.save_payment_card_details()
    account_page.verify_card_last_updated_summary(card_no, card_month, card_year)


def test_expiry_must_be_in_future(reuse_storage_state):
    card_owner = "John Doe"
    card_no = "4242 4242 4242 4242"
    card_month = "12"
    card_year = "2016"
    card_cvc = "123"
    page, mfa_code,site_url = reuse_storage_state
    account_page = AccountPage(page, site_url)
    account_page.open()
    enter_mfa(page, mfa_code)
    account_page.click_account_tab()
    account_page.submit_payment_details(card_owner, card_no, card_month, card_year, card_cvc)    
    account_page.save_payment_card_details()
    account_page.verify_toast_message(f"Expiration must be in the future")


def test_cvc_check(reuse_storage_state):
    card_owner = "John Doe"
    card_no = "4242 4242 4242 4242"
    card_month = "12"
    card_year = "2026"
    card_cvc = "12"
    page, mfa_code,site_url = reuse_storage_state
    account_page = AccountPage(page, site_url)
    account_page.open()
    enter_mfa(page, mfa_code)
    account_page.click_account_tab()
    account_page.submit_payment_details(card_owner, card_no, card_month, card_year, card_cvc)    
    account_page.save_payment_card_details()
    account_page.verify_toast_message(f"CVC must be 3 or 4 digits")


def test_card_no_check(reuse_storage_state):
    card_owner = "John Doe"
    card_no = "5343434343424"
    card_month = "12"
    card_year = "2026"
    card_cvc = "123"
    page, mfa_code,site_url = reuse_storage_state
    account_page = AccountPage(page, site_url)
    account_page.open()
    enter_mfa(page, mfa_code)
    account_page.click_account_tab()
    account_page.submit_payment_details(card_owner, card_no, card_month, card_year, card_cvc)    
    account_page.save_payment_card_details()
    account_page.verify_toast_message(f"Invalid card number (Luhn check failed)")