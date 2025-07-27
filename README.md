# 🔍 Semantic Search with Elasticsearch and SentenceTransformers

This project demonstrates how to build a vector search engine using:
- Amazon product metadata
- SentenceTransformers for embedding text
- Elasticsearch for indexing and k-NN based vector search

---

## 📦 Installation

Install dependencies using Poetry:

```bash
poetry install
```

---

## 🔐 Set Up Elasticsearch Credentials

Export your Elasticsearch credentials as environment variables:

```bash
export ES_USERNAME=<YOUR-ELASTICSEARCH-USERNAME>
export ES_PASSWORD=<YOUR-ELASTICSEARCH-PASSWORD>
```

Make sure your Elasticsearch instance is running and accessible (e.g. at http://localhost:9200).

---

## 🧠 Index Product Metadata to Elasticsearch

To generate sentence embeddings and index product data into Elasticsearch:

```bash
poetry run python src/elacticsearch_demo/index_products.py
```

👉 This will:
- Read the data CSV file
- Generate vector embeddings using `all-MiniLM-L6-v2`
- Create an Elasticsearch index named `amazon_products`
- Bulk index all records with their embeddings

---

## 🔍 Run Vector Search

To search semantically (e.g. "Does the list have any building blocks toys?"):

```bash
poetry run python src/elacticsearch_demo/vector_search.py
```

This will:
- Encode the query using the same transformer
- Run a k-NN vector search in Elasticsearch
- Return top matching product titles + descriptions based on semantic similarity

---

## 📚 Tech Stack

- Python 3.10+
- [Poetry](https://python-poetry.org/)
- Elasticsearch 8+
- `sentence-transformers` (MiniLM-L6-v2)

---