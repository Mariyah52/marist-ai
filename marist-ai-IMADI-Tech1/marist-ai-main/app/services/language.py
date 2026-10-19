import re


def detect_language(text: str) -> str:
    text = (text or "").strip()

    if not text:
        return "unknown"

    # Urdu / Arabic script
    if re.search(r"[\u0600-\u06FF]", text):
        return "urdu"

    # Hindi Devanagari script
    if re.search(r"[\u0900-\u097F]", text):
        return "hindi"

    return "english"