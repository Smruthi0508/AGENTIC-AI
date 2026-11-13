"""Rule-based categoriser: fast, free and predictable. The LLM only handles merchants these rules miss."""
import re

SPEND_CATEGORIES = [
    "Food & Dining", "Groceries", "Transport", "Shopping", "Entertainment",
    "Bills & Utilities", "Health", "Education", "Rent", "Transfers", "Other",
]
CATEGORIES = SPEND_CATEGORIES + ["Income"]

RULES = {
    "Rent": ["rent", "landlord"],
    "Transfers": ["p2p", "self transfer"],
    "Food & Dining": ["swiggy", "zomato", "dominos", "mcdonalds", "kfc", "starbucks", "cafe", "restaurant", "pizza", "biryani", "bakery"],
    "Groceries": ["bigbasket", "blinkit", "zepto", "dmart", "instamart", "supermarket", "reliance fresh"],
    "Transport": ["uber", "ola", "rapido", "metro", "irctc", "redbus", "petrol", "fuel", "bmtc", "indian oil"],
    "Shopping": ["amazon", "flipkart", "myntra", "ajio", "meesho", "nykaa", "decathlon"],
    "Entertainment": ["netflix", "spotify", "hotstar", "bookmyshow", "prime video", "youtube premium", "pvr", "inox"],
    "Bills & Utilities": ["electricity", "bescom", "airtel", "jio", "broadband", "recharge", "water bill", "gas bill"],
    "Health": ["pharmacy", "apollo", "medplus", "hospital", "clinic", "1mg", "pharmeasy"],
    "Education": ["udemy", "coursera", "tuition", "unacademy", "college", "fees"],
}

_COMPILED = [
    (cat, re.compile(r"\b(" + "|".join(re.escape(k) for k in kws) + r")\b"))
    for cat, kws in RULES.items()
]


def rule_category(description):
    d = str(description).lower()
    for cat, pattern in _COMPILED:
        if pattern.search(d):
            return cat
    return None
