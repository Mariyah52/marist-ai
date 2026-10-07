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

    words = set(re.findall(r"[a-zA-Z]+", text.lower()))

    roman_urdu_words = {
        "aap", "ap", "hai", "hain", "ho", "mera", "meri", "mere",
        "mujhe", "hum", "ham", "ka", "ki", "ke", "kya",
        "chahiye", "karna", "krna", "karo", "karein", "karen",
        "mein", "main", "se", "ko", "aur", "ye", "yeh", "woh",
        "nahi", "nahin", "acha", "theek", "batao", "bata",
        "kaam", "masla", "kar", "kr", "hota", "hoti", "jate",
        "jaye", "wala", "wali", "salesman"
    }

    if len(words & roman_urdu_words) >= 2:
        return "roman-urdu"

    return "english"