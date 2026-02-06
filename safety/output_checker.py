HARMFUL_OUTPUT_PATTERNS = [
    "you should buy",
    "you should sell",
    "i recommend investing in",
    # plus generic harmful content patterns
]

def check_output(response: str) -> dict:
    text = response.lower()
    unsafe = any(p in text for p in HARMFUL_OUTPUT_PATTERNS)

    if unsafe:
        safe_replacement = (
            "I cannot provide investment advice or unsafe content. "
            "I can, however, explain the underlying metrics or risks."
        )
        return {"is_safe": False, "safe_replacement": safe_replacement}
    else:
        return {"is_safe": True, "safe_replacement": None}