import os
from elasticsearch import Elasticsearch

def main():
    es = Elasticsearch(
        "http://localhost:9200",
        basic_auth=(os.getenv("ES_USERNAME"), os.getenv("ES_PASSWORD")),
    )

    query_text = "Interlocking bricks game"

    response = es.search(
        index="amazon_products",
        size=5,
        body={
            "query": {
                "multi_match": {
                    "query": query_text,
                    "fields": ["title", "description"]
                }
            }
        },
    )

    print("\n📟 Top keyword search results:")
    for hit in response["hits"]["hits"]:
        print(f"[{hit['_score']:.2f}] {hit['_source']['title']}: {hit['_source']['description'][:200]}...")

if __name__ == "__main__":
    main()
