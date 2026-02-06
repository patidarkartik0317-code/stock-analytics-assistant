import re

INTENT_LABELS = [
    "benign_market_question",
    "benign_technical_question",
    "investment_advice_request",
    "harmful_non_financial",
    "other",
]


ADVICE_PATTERNS = [
    r"\bshould i buy\b",
    r"\bshould i sell\b",
    r"\bis now a good time\b",
    r"\bwhich stock is best\b",
]

HARMFUL_PATTERNS = [
    "kill myself",
    "hurt someone",
    "make a bomb",
    # etc.
]

def classify_intent(prompt: str) -> dict:
    text = prompt.lower()

    if any(re.search(p, text) for p in ADVICE_PATTERNS):
        label = "investment_advice_request"
    elif any(h in text for h in HARMFUL_PATTERNS):
        label = "harmful_non_financial"
    elif "volatility" in text or "rolling" in text or "returns" in text:
        label = "benign_market_question"
    else:
        label = "other"

    return {"label": label}