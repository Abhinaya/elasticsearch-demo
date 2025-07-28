from elasticsearch import Elasticsearch

def main():
    es = Elasticsearch(
        "http://localhost:9200",
    )

    query_text1 = "Lego blocks"

    response = es.search(
        index="amazon_products",
        size=5,
        body={
            "query": {
                "multi_match": {
                    "query": query_text1,
                    "fields": ["title", "description"]
                }
            }
        },
    )

    print("\n📟 Top keyword search results for: ", query_text1)
    for hit in response["hits"]["hits"]:
        print(f"[{hit['_score']:.2f}] {hit['_source']['title']}: {hit['_source']['description'][:200]}...")

    query_text2 = "Interlocking bricks game"

    response = es.search(
        index="amazon_products",
        size=5,
        body={
            "query": {
                "multi_match": {
                    "query": query_text2,
                    "fields": ["title", "description"]
                }
            }
        },
    )

    print("\n📟 Top keyword search results for: " , query_text2)
    for hit in response["hits"]["hits"]:
        print(f"[{hit['_score']:.2f}] {hit['_source']['title']}: {hit['_source']['description'][:200]}...")

if __name__ == "__main__":
    main()
