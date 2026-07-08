
class LoginPage:
    """Page Object Model for the /app/login page"""
    
    def __init__(self, page):
        self.page = page
        self.login_button = self.page.locator("(//button[text()='Log in'])[1]")
        self.username = self.page.locator("#email")
        self.password = self.page.locator("#password")
        self.sign_in = self.page.locator("//button[text()='Sign in']")
        self.mfa = self.page.locator("input[autocomplete='one-time-code']")
        self.verify = self.page.locator("//button[@type='submit']")

    def open(self, site_url: str): 
        self.page.goto(site_url)
        self.login_button.click()
        self.page.wait_for_url("**/login")

    def enter_credentials(self, username, password):
        self.username.fill(username)
        self.password.fill(password)
        self.sign_in.click()