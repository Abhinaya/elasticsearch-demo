"""
Constants and configuration values shared across the Elasticsearch demo project.
"""

# Elasticsearch configuration
INDEX_NAME = "amazon_products"
ELASTICSEARCH_URL = "http://localhost:9200"
KIBANA_URL = "http://localhost:5601"

# SentenceTransformer model configuration
MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# Data file paths
DATA_FILE_PATH = "data/amazon_product_reviews_1000_utf8.csv"

# Index mapping configuration
INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "id": {"type": "integer"},
            "title": {"type": "text"},
            "description": {"type": "text"},
            "embedding": {
                "type": "dense_vector",
                "dims": EMBEDDING_DIMENSION,
                "index": True,
                "similarity": "cosine",
            },
        }
    }
}

# Search configuration
DEFAULT_SEARCH_SIZE = 10
SIMILARITY_THRESHOLD = 0.7
