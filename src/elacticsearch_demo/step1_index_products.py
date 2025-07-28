import pandas as pd
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import os


def main():
    amazon_products = pd.read_csv("data/amazon_product_reviews_1000_utf8.csv")

    # 2. Generate sentence embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")

    amazon_products["embedding"] = amazon_products.apply(
        lambda row: model.encode(
            f"{row['TITLE']} {row['DESCRIPTION']}", normalize_embeddings=True
        ).tolist(),
        axis=1,
    )

    print("embedding generated....")

    # 3. Connect to Elasticsearch
    es = Elasticsearch(
        "http://localhost:9200",
        basic_auth=(os.getenv("ES_USERNAME"), os.getenv("ES_PASSWORD")),
    )

    # 4. Create index with dense_vector mapping
    index_name = "amazon_products"
    if not es.indices.exists(index=index_name):
        es.indices.create(
            index=index_name,
            body={
                "mappings": {
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "text"},
                        "description": {"type": "text"},
                        "embedding": {
                            "type": "dense_vector",
                            "dims": 384,
                            "index": True,
                            "similarity": "cosine",
                        },
                    }
                }
            },
        )

    # 5. Bulk index the documents
    def generate_docs():
        for i, row in amazon_products.iterrows():
            yield {
                "_index": index_name,
                "_id": i,
                "_source": {
                    "id": row["id"],
                    "title": row["TITLE"],
                    "description": row["DESCRIPTION"],
                    "embedding": row["embedding"],
                },
            }

    bulk(es, generate_docs())
    print(f"✅ Indexed {len(amazon_products)} products.")

if __name__ == "__main__":
    main()
