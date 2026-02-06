
import os
from google.genai import EmbeddingsClient
import numpy as np

emb_client = EmbeddingsClient(api_key=os.getenv("GEMINI_API_KEY"))

with open("data/jailbreak_library.txt") as f:
    LIBRARY_PROMPTS = [line.strip() for line in f if line.strip()]

LIBRARY_EMBS = emb_client.embed(LIBRARY_PROMPTS)  # shape: (N, D)

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def detect_jailbreak(prompt: str) -> dict:
    emb = emb_client.embed([prompt])[0]
    sims = [cosine_sim(emb, lib_emb) for lib_emb in LIBRARY_EMBS]
    max_sim = max(sims) if sims else 0.0
    return {"jailbreak_score": float(max_sim)}