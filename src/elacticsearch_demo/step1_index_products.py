import pandas as pd
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import os
from elacticsearch_demo.constants import (
    INDEX_NAME,
    ELASTICSEARCH_URL,
    KIBANA_URL,
    MODEL_NAME,
    DATA_FILE_PATH,
    INDEX_MAPPING,
)


def main():
    print("📄 Loading Amazon products dataset...")
    amazon_products = pd.read_csv(DATA_FILE_PATH)
    print(f"✅ Loaded {len(amazon_products)} products")

    # 2. Generate sentence embeddings
    print("🧠 Loading SentenceTransformer model...")
    model = SentenceTransformer(MODEL_NAME)
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
    es = Elasticsearch(ELASTICSEARCH_URL)
    print("✅ Connected to Elasticsearch.")

    # 4. Create index with dense_vector mapping
    print(f"🗂️  Checking if index '{INDEX_NAME}' exists...")
    if not es.indices.exists(index=INDEX_NAME):
        print(f"📝 Creating index '{INDEX_NAME}'...")
        es.indices.create(
            index=INDEX_NAME,
            body=INDEX_MAPPING,
        )
        print(f"✅ Index '{INDEX_NAME}' created successfully")
    else:
        print(f"ℹ️ Index '{INDEX_NAME}' already exists")

    # 5. Bulk index the documents
    print("📤 Starting bulk indexing...")
    def generate_docs():
        for i, row in amazon_products.iterrows():
            yield {
                "_index": INDEX_NAME,
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
    print(f"🌐 You can now access Elasticsearch at: {ELASTICSEARCH_URL}")
    print(f"📊 View the index at: http://localhost:5601/app/management/data/index_management/indices/index_details?indexName={INDEX_NAME}")

if __name__ == "__main__":
    main()
