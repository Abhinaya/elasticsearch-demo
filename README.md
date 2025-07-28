# 🔍 Semantic Search with Elasticsearch and SentenceTransformers

This project demonstrates how to build a vector search engine using:
- Amazon product metadata
- SentenceTransformers for embedding text
- Elasticsearch for indexing and k-NN based vector search

---

## 📦 Installation

### Option 1: Using Docker (Recommended)

Start Elasticsearch and Kibana using Docker Compose:

```bash
# Start the services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

This will start:
- **Elasticsearch** on `http://localhost:9200`
- **Kibana** on `http://localhost:5601`

### Option 2: Manual Installation

Install dependencies using Poetry:

```bash
poetry install
```

## 🔐 Set Up Elasticsearch Credentials

### For Docker Setup
No credentials needed - security is disabled for development.

### For Manual Setup
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
poetry run python src/elacticsearch_demo/step1_index_products.py
```

👉 This will:
- Read the data CSV file
- Generate vector embeddings using `all-MiniLM-L6-v2`
- Create an Elasticsearch index named `amazon_products`
- Bulk index all records with their embeddings

---

## 🐳 Docker Services

The `docker-compose.yml` includes:

- **Elasticsearch 8.11.0**: Vector search engine
- **Kibana 8.11.0**: Data visualization and management UI
- **Persistent storage**: Data persists between container restarts
- **Health checks**: Ensures services are ready before dependencies start

### Useful Docker Commands

```bash
# Stop services
docker-compose down

# Stop and remove volumes (⚠️ deletes all data)
docker-compose down -v

# Restart services
docker-compose restart

# View service logs
docker-compose logs elasticsearch
docker-compose logs kibana
```

---

## 📚 Tech Stack

- Python 3.10+
- [Poetry](https://python-poetry.org/)
- Docker & Docker Compose
- Elasticsearch 8+
- Kibana 8+
- `sentence-transformers` (MiniLM-L6-v2)

---