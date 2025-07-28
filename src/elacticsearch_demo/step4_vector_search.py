# vector_search.py
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import os

def main():
    # 1. Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # 2. Encode search query
    query = "Interlocking bricks game"
    query_vector = model.encode(query, normalize_embeddings=True).tolist()

    # 3. Connect to Elasticsearch
    es = Elasticsearch(
        "http://localhost:9200",
    )

    # 4. Search using KNN
    response = es.search(
        index="amazon_products",
        size=5,
        body={
            "knn": {
                "field": "embedding",
                "query_vector": query_vector,
                "k": 5,
                "num_candidates": 100,
            }
        },
    )

    # 5. Show results
    print("\n🔍 Top matching results for :", query)
    for hit in response["hits"]["hits"]:
        print(
            f"[{hit['_score']:.2f}] {hit['_source']['title']}: {hit['_source']['description'][:200]}..."
        )

if __name__ == "__main__":
    main()
