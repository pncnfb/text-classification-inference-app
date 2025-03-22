import re

def sanitize_string(text: str) -> str:
    """
    Sanitizes string by fixing invalid escape sequences.
    """
    sanitized_text = re.sub(r'\\(?![\\"/bfnrtu])', '', text)  # Removes lone backslashes
    sanitized_text = sanitized_text.replace('\n', '\\n').replace('\r', '\\r')  # Ensure newlines are properly escaped
    return sanitized_text