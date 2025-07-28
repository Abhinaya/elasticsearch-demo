import pandas as pd
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import os


def main():
    print("📄 Loading Amazon products dataset...")
    amazon_products = pd.read_csv("data/amazon_product_reviews_1000_utf8.csv")
    print(f"✅ Loaded {len(amazon_products)} products")

    # 2. Generate sentence embeddings
    print("🧠 Loading SentenceTransformer model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("🔄 Generating embeddings...")

    amazon_products["embedding"] = amazon_products.apply(
        lambda row: model.encode(
            f"{row['TITLE']} {row['DESCRIPTION']}", normalize_embeddings=True
        ).tolist(),
        axis=1,
    )

    print("embedding generated....")

    # 3. Connect to Elasticsearch
    print("🔌 Connecting to Elasticsearch...")
    es = Elasticsearch("http://localhost:9200")
    print("✅ Connected to Elasticsearch.")

    # 4. Create index with dense_vector mapping
    index_name = "amazon_products"
    print(f"🗂️  Checking if index '{index_name}' exists...")
    if not es.indices.exists(index=index_name):
        print(f"📝 Creating index '{index_name}'...")
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
        print(f"✅ Index '{index_name}' created successfully")
    else:
        print(f"ℹ️  Index '{index_name}' already exists")

    # 5. Bulk index the documents
    print("📤 Starting bulk indexing...")
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
    print(f"✅ Successfully indexed {len(amazon_products)} products to Elasticsearch!")
    print(f"🌐 You can now access Elasticsearch at: http://localhost:9200")
    print(f"📊 View the index at: http://localhost:5601/app/management/data/index_management/indices/index_details?indexName=amazon_products")

if __name__ == "__main__":
    main()
