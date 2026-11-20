import re

# Matches Dutch/European IBANs (even if the customer puts spaces every 4 characters, e.g., "NL91 ABNA 0417 1643 00")
IBAN_REGEX = re.compile(
    r"\b[A-Z]{2}\d{2}(?:[ -]?[A-Z0-9]{4}){2,7}(?:[ -]?[A-Z0-9]{1,4})?\b",
    re.IGNORECASE
)

CARD_REGEX = re.compile(
    r"\b(?:\d[ -]*?){13,19}\b"
)

def sanitize_text(text: str) -> str:
    
    if not text:
        return ""
    
    text = IBAN_REGEX.sub("[REDACTED_IBAN]", text)
    text = CARD_REGEX.sub("[REDACTED_CARD]", text)
    return text