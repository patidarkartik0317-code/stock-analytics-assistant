import yaml

with open("config/policy.yaml") as f:
    POLICY = yaml.safe_load(f)

def decide_action(intent: dict, jailbreak: dict) -> str:
    label = intent["label"]
    jb_score = jailbreak["jailbreak_score"]

    action = POLICY["actions"].get(label, "allow")

    if jb_score >= POLICY["thresholds"]["jailbreak_high"]:
        action = POLICY["jailbreak_overrides"]["high_score_action"]

    return action