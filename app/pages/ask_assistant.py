import streamlit as st
from llm_client import call_llm, BASE_SYSTEM_PROMPT
from safety.pipeline import run_safety_on_input, run_safety_on_output
from logging_utils import log_interaction

st.title("Ask the Stock Assistant")

user_question = st.text_area("Ask a question about the market")
context = st.selectbox("Context", ["General market", "Single ticker", "Portfolio metrics"])

if st.button("Get explanation"):
    # Run safety checks on input
    safety_in = run_safety_on_input(user_question)

    if safety_in["action"] == "block":
        st.warning("Your question cannot be answered due to safety policies.")
        log_interaction(
            raw_prompt=user_question,
            sanitized_prompt=safety_in["sanitized_prompt"],
            intent_label=safety_in["intent"]["label"],
            jailbreak_score=safety_in["jailbreak"]["jailbreak_score"],
            policy_action=safety_in["action"],
            model_response=None,
            output_safe=False,
            final_answer_shown=False,
            context_type=context,
        )
    else:
        answer = call_llm(BASE_SYSTEM_PROMPT, safety_in["sanitized_prompt"])
        safety_out = run_safety_on_output(answer)

        if not safety_out["is_safe"]:
            st.warning("The model's response was unsafe and has been replaced.")
            final_answer = safety_out["safe_replacement"]
        else:
            final_answer = answer

        st.write(final_answer)

        log_interaction(
            raw_prompt=user_question,
            sanitized_prompt=safety_in["sanitized_prompt"],
            intent_label=safety_in["intent"]["label"],
            jailbreak_score=safety_in["jailbreak"]["jailbreak_score"],
            policy_action=safety_in["action"],
            model_response=answer,
            output_safe=safety_out["is_safe"],
            final_answer_shown=True,
            context_type=context,
        )