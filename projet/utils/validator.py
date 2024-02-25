import pyinputplus
import re

def check_phone(phone):
    """
    Validates a phone number using a regular expression.

    Args:
    - phone (str): The input phone number.

    Returns:
    - str: The validated phone number.

    Raises:
    - pyinputplus.ValidationException: If the phone number is invalid.
    """
    # Check if the phone number matches the pattern \d{14}
    if phone and not bool(re.match(r'\d{14}', phone)):
        # Raise a ValidationException if the phone number is invalid
        raise pyinputplus.ValidationException('Invalid phone number')

    # Return the validated phone number
    return phone
