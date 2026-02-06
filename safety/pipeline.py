from .sanitizer import sanitize_input
from .intent import classify_intent
from .jailbreak import detect_jailbreak
from .policy import decide_action
from .output_checker import check_output


def run_safety_on_input(raw_prompt: str) -> dict:
    sanitized = sanitize_input(raw_prompt)
    intent = classify_intent(sanitized)
    jailbreak = detect_jailbreak(sanitized)
    action = decide_action(intent, jailbreak)
    return {
        "sanitized_prompt": sanitized,
        "intent": intent,
        "jailbreak": jailbreak,
        "action": action,
    }


def run_safety_on_output(response: str) -> dict:
    return check_output(response)