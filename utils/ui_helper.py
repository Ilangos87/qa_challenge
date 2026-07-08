def enter_mfa(page, code: str):
    """Fill MFA one-time code and submit."""
    mfa_field = page.locator("input[autocomplete='one-time-code']")
    verify_button = page.locator("//button[@type='submit']")
    mfa_field.wait_for(state="visible")
    mfa_field.fill(code)
    verify_button.click()


def assert_masked_bank_info(ui_text: str, expected_routing: str, expected_account: str):
    """
    Assert that masked routing/account info in UI matches expected values.
    """
    # Split UI text into routing and account parts
    routing_text, account_text = [part.strip() for part in ui_text.split("|")]

    # # Extract last 4 digits from expected values
    expected_routing_last4 = expected_routing[-4:]
    expected_account_last4 = expected_account[-4:]

    # Check routing masking and last 4 digits
    assert routing_text.endswith(expected_routing_last4), \
        f"Routing mismatch: UI={routing_text}, expected last4={expected_routing_last4}"

    # Check account masking and last 4 digits
    assert account_text.endswith(expected_account_last4), \
        f"Account mismatch: UI={account_text}, expected last4={expected_account_last4}"


def assert_masked_payment_info(ui_text: str, expected_card_number: str, expected_expiry: str):
    """
    Assert that masked payment info in UI matches expected values.

    ui_text: string from UI, e.g. "VISA ending in 4242 | Expires 12/2026"
    expected_card_number: full card number (must be Luhn-valid)
    expected_expiry: expiry in MM/YYYY format
    """
    # Split UI text into card and expiry parts
    card_text, expiry_text = [part.strip() for part in ui_text.split("|")]

    # Extract last 4 digits from expected card
    expected_last4 = expected_card_number[-4:]

    # Assertions
    assert card_text.endswith(expected_last4), \
        f"Card mismatch: UI={card_text}, expected last4={expected_last4}"

    assert expiry_text == f"Expires {expected_expiry}", \
        f"Expiry mismatch: UI={expiry_text}, expected={expected_expiry}"