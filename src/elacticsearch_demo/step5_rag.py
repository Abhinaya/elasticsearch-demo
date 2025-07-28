import requests
from os import getenv
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from elacticsearch_demo.constants import (
    INDEX_NAME,
    ELASTICSEARCH_URL,
    MODEL_NAME,
)

grok_api_key = getenv("GROK_API_KEY")
if not grok_api_key:
    raise ValueError("Set env var GROK_API_KEY")

# Simulated query
query = "Can Khadims Black Slip-On Shoes be washed with deteregent?"
model = SentenceTransformer(MODEL_NAME)
query_vector = model.encode(query).tolist()

# -- Vector Search in Elasticsearch --
es = Elasticsearch(ELASTICSEARCH_URL)  # or your cloud instance
response = es.search(index=INDEX_NAME, body={
    "knn": {
        "field": "embedding",
        "query_vector": query_vector,
        "k": 5,
        "num_candidates": 100,
    }
})
top_doc = response['hits']['hits'][0]['_source']
retrieved_context = top_doc['title'] + "\n" + top_doc['description']

print("\n=========== QUERY ==============")
print(query)
print("==================================\n\n")

print("Retrieved relevant information from reviews: \n", retrieved_context)

def make_groq_api_call(user_content: str):
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {grok_api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": """
                You are a helpful e-commerce assistant.
                If you don't have enough information, Don't assume."""},
                {"role": "user", "content": user_content}
            ]
        }
    )
    return response.json()["choices"][0]["message"]["content"]


no_context_response = make_groq_api_call(query)
rag_response = make_groq_api_call(f"Context:\n{retrieved_context}\n\nQuestion: {query}")

# Print responses
print("\n\n=== 🚫 Without RAG ===")
print(no_context_response)

print("\n=== 📖 With RAG ===")
print(rag_response)
