import pandas as pd
from datetime import datetime
import uuid
import os

LOG_PATH = "data/safety_logs.parquet"

def log_interaction(
    raw_prompt,
    sanitized_prompt,
    intent_label,
    jailbreak_score,
    policy_action,
    model_response,
    output_safe,
    final_answer_shown,
    context_type,
):
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "session_id": str(uuid.uuid4()),
        "raw_prompt": raw_prompt,
        "sanitized_prompt": sanitized_prompt,
        "intent_label": intent_label,
        "jailbreak_score": jailbreak_score,
        "policy_action": policy_action,
        "model_response": model_response,
        "output_safe": output_safe,
        "final_answer_shown": final_answer_shown,
        "context_type": context_type,
    }

    if os.path.exists(LOG_PATH):
        df = pd.read_parquet(LOG_PATH)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_parquet(LOG_PATH, index=False)