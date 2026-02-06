import os
# Replace 'some_provider_sdk' with your actual LLM SDK
from google.genai import gemini

client = gemini.GeminiClient(api_key=os.getenv("GEMINI_API_KEY"))

BASE_SYSTEM_PROMPT = """
You are a financial analytics explainer. 
You ONLY explain metrics, trends, and risk in neutral, educational language.
You DO NOT give investment advice, recommendations, or predictions.
If asked for advice, you explain why you cannot provide it.
"""

def call_llm(system_prompt: str, user_prompt: str) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    response = client.chat(messages=messages)
    return response["content"]