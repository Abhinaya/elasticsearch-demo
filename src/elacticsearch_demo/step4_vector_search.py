# vector_search.py
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from elacticsearch_demo.constants import (
    INDEX_NAME,
    ELASTICSEARCH_URL,
    MODEL_NAME,
    DEFAULT_SEARCH_SIZE,
)

def main():
    # 1. Load embedding model
    model = SentenceTransformer(MODEL_NAME)

    # 2. Encode search query
    query = "Interlocking bricks game"
    query_vector = model.encode(query, normalize_embeddings=True).tolist()

    # 3. Connect to Elasticsearch
    es = Elasticsearch(ELASTICSEARCH_URL)

    # 4. Search using KNN
    response = es.search(
        index=INDEX_NAME,
        size=DEFAULT_SEARCH_SIZE // 2,
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
    print(f"\nTop matching results for: {query}")
    for hit in response["hits"]["hits"]:
        print(
            f"[{hit['_score']:.2f}] {hit['_source']['title']}: {hit['_source']['description'][:200]}..."
        )

if __name__ == "__main__":
    main()
