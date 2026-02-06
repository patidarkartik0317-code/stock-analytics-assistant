import streamlit as st
import pandas as pd
import altair as alt

# Load logs
try:
    df = pd.read_parquet("data/safety_logs.parquet")
except FileNotFoundError:
    st.warning("No safety logs found.")
    df = pd.DataFrame()

st.title("LLM Safety Analytics")

if not df.empty:
    st.metric("Total interactions", len(df))
    st.metric("Blocked prompts", (df["policy_action"] == "block").sum())
    st.metric("Unsafe outputs caught", (~df["output_safe"]).sum())

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("jailbreak_score:Q", bin=True),
        y="count()"
    )
    st.altair_chart(chart, use_container_width=True)

    action_counts = df.groupby(["intent_label", "policy_action"]).size().reset_index(name="count")
    chart2 = alt.Chart(action_counts).mark_bar().encode(
        x="intent_label:N",
        y="count:Q",
        color="policy_action:N"
    )
    st.altair_chart(chart2, use_container_width=True)
else:
    st.info("No data to display.")