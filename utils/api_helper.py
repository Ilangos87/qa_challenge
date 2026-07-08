
def assert_masked_value(masked: str, original: str) -> None:
    """
    Assert that a masked value hides all but the last 4 digits
    and that those last 4 digits match the original number.
    """
    # Ensure masked starts with mask characters
    assert masked[0] in ("•") , f"Masked value does not start with mask: {masked}"

    # Extract last 4 digits
    masked_last4 = masked[-4:]
    original_last4 = original[-4:]

    # Compare last 4 digits
    assert masked_last4 == original_last4, (
        f"Last 4 mismatch: masked={masked_last4}, original={original_last4}"
    )