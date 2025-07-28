from elasticsearch import Elasticsearch
from elacticsearch_demo.constants import (
    INDEX_NAME,
    ELASTICSEARCH_URL,
    DEFAULT_SEARCH_SIZE,
)

def main():
    es = Elasticsearch(ELASTICSEARCH_URL)

    query_text1 = "Lego blocks"

    response = es.search(
        index=INDEX_NAME,
        size=DEFAULT_SEARCH_SIZE // 2,
        body={
            "query": {
                "multi_match": {
                    "query": query_text1,
                    "fields": ["title", "description"]
                }
            }
        },
    )

    print(f"\nTop keyword search results for: {query_text1}")
    for hit in response["hits"]["hits"]:
        print(f"[{hit['_score']:.2f}] {hit['_source']['title']}: {hit['_source']['description'][:200]}...")

    query_text2 = "Interlocking bricks game"

    response = es.search(
        index=INDEX_NAME,
        size=DEFAULT_SEARCH_SIZE // 2,
        body={
            "query": {
                "multi_match": {
                    "query": query_text2,
                    "fields": ["title", "description"]
                }
            }
        },
    )

    print(f"\nTop keyword search results for: {query_text2}")
    for hit in response["hits"]["hits"]:
        print(f"[{hit['_score']:.2f}] {hit['_source']['title']}: {hit['_source']['description'][:200]}...")

if __name__ == "__main__":
    main()
