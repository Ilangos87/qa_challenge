from utils.ui_helper import assert_masked_bank_info, assert_masked_payment_info
from playwright.sync_api import expect

class AccountPage:

    def __init__(self, page, site_url):
        self.page = page
        self.url = f"{site_url}/app/account"
        self.account_tab = self.page.locator("//a[@href='/app/account']")
        self.routing_no = self.page.locator("#bank-routing")
        self.bank_acc_no = self.page.locator("#bank-account")
        self.save_bank_details = self.page.locator("#bank-save")
        self.bank_routing_info = self.page.locator("//div[@data-testid='bank-saved-info']/p[1]")
        self.card_details_info = self.page.locator("//div[@data-testid='payment-saved-info']/p[1]")
        self.card_owner = self.page.locator("#card-holder")
        self.card_no = self.page.locator("#card-number")
        self.card_month = self.page.locator("#card-exp-month")
        self.card_year = self.page.locator("#card-exp-year")    
        self.card_cvc = self.page.locator("#card-cvc")
        self.save_payment_details = self.page.locator("#card-save")


    def open(self):
        self.page.goto(self.url)
    
    def click_account_tab(self):
        self.account_tab.click()

    def submit_banking_details(self, routing_no, account_no):
        self.routing_no.fill(routing_no)
        self.bank_acc_no.fill(account_no)

    def submit_payment_details(self, card_owner, card_no, card_month, card_year, card_cvc):
        self.card_owner.fill(card_owner)
        self.card_no.fill(card_no)
        self.card_month.fill(card_month)
        self.card_year.fill(card_year)
        self.card_cvc.fill(card_cvc)

    def save_banking_details(self):    
        self.save_bank_details.click()

    def save_payment_card_details(self):
        self.save_payment_details.click()
        
    def verify_bank_last_updated_summary(self, routing_no, account_no):
        last_updated_summary = self.bank_routing_info.inner_text()
        assert_masked_bank_info(last_updated_summary, routing_no, account_no)
    
    def verify_card_last_updated_summary(self, card_no, card_month, card_year):
        last_updated_summary = self.card_details_info.inner_text()
        expected_expiry = f"{card_month}/{card_year}"
        assert_masked_payment_info(last_updated_summary, card_no, expected_expiry)


    def verify_toast_message(self, expected_text: str, timeout: int = 5000):
        toast = self.page.get_by_text(expected_text, exact=True)
        expect(toast).to_be_visible(timeout=timeout)
        actual_text = toast.inner_text()
        assert actual_text == expected_text, f"Toast mismatch: got '{actual_text}', expected '{expected_text}'"
   