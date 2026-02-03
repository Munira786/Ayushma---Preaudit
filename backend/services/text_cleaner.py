import re

def clean_text(text: str) -> str:
    """
    Cleans text for ML processing:
    - Lowercase
    - Remove punctuation (except % for burn context)
    - Normalize whitespace
    - Start/End whitespace trim
    """
    if not isinstance(text, str) or not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove special chars but keep % and alphanumeric
    # Matches any char that is NOT a lowercase letter, number, whitespace, or %
    text = re.sub(r'[^a-z0-9%\s]', '', text)
    
    # Normalize whitespace (replace multiple spaces/newlines with single space)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def extract_amount(text: str) -> float:
    """Extracts max currency amount from text."""
    if not text:
        return 0.0
    matches = re.findall(r'(\d+(?:,\d{3})*(?:\.\d{2})?)', text)
    if matches:
        try:
            amounts = [float(m.replace(',', '')) for m in matches]
            return max(amounts)
        except ValueError:
            return 0.0
    return 0.0

def extract_severity(text: str) -> int:
    """
    Extracts burn severity (TBSA percentage) from text.
    """
    if not text:
        return None
    match = re.search(r'(\d{1,2})\s*%?\s*tbsa', text.lower())
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return None
    return None
