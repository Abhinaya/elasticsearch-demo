import requests
from os import getenv

# Your Groq key
api_key = getenv("GROK_API_KEY")
if not api_key:
    raise ValueError("Set env var GROK_API_KEY")
groq_url = "https://api.groq.com/openai/v1/chat/completions"
model = "llama3-70b-8192"

# Simulated query
query = "Are these earrings made of silver?"

# Simulated RAG step: Assume this is the top match from your vector search
retrieved_context = """
Redgem 925 Silver Stud Earrings for Girls and Women.
These stylish earrings are crafted in high-quality 925 sterling silver, ideal for daily wear or gifting.
"""

# ---- Without RAG (LLM only sees the query) ----
no_context_response = requests.post(
    groq_url,
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful e-commerce assistant."},
            {"role": "user", "content": query}
        ]
    }
)

# ---- With RAG (LLM gets context + query) ----
rag_response = requests.post(
    groq_url,
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful e-commerce assistant."},
            {"role": "user", "content": f"Context:\n{retrieved_context}\n\nQuestion: {query}"}
        ]
    }
)

# Print responses
print("=== Without RAG ===")
print(no_context_response.json()["choices"][0]["message"]["content"])

print("\n=== With RAG ===")
print(rag_response.json()["choices"][0]["message"]["content"])
