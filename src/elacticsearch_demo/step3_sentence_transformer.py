from sentence_transformers import SentenceTransformer, util
import matplotlib.pyplot as plt

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define 10 example sentences
sentences = [
    "Elasticsearch guide",
    "How to cook pasta",
    "Understanding deep learning",
    "Python programming basics",
    "Tips for healthy living",
    "Learn about artificial intelligence",
    "Guide to machine learning",
    "Traveling in Europe on a budget",
    "Mastering data structures",
    "Introduction to cloud computing"
]

# Create embeddings
sentence_embeddings = model.encode(sentences, convert_to_tensor=True)

# Define search query
query = "learn"
query_embedding = model.encode(query, convert_to_tensor=True)

# Compute cosine similarity
cosine_scores = util.cos_sim(query_embedding, sentence_embeddings)[0]

# Get top 5 results
top_k = 5
top_results = sorted(enumerate(cosine_scores), key=lambda x: x[1], reverse=True)[:top_k]

print(f"\nQuery: {query}\nTop {top_k} similar sentences:")
for idx, score in top_results:
    print(f"{sentences[idx]} (Score: {score.item():.4f})")

# Prepare data for plotting
top_sentences = [sentences[idx] for idx, _ in top_results]
top_scores = [score.item() for _, score in top_results]

# Plotting
plt.figure(figsize=(10, 6))
bars = plt.barh(top_sentences[::-1], top_scores[::-1], color='skyblue')
plt.xlabel('Similarity Score')
plt.title(f'Top {top_k} Matches for Query: \"{query}\"')
plt.xlim(0, 1)

# Add score labels
for bar, score in zip(bars, top_scores[::-1]):
    plt.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
             f'{score:.2f}', va='center')

plt.tight_layout()
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.show()
