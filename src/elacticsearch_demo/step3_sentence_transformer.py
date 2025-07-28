from sentence_transformers import SentenceTransformer, util

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Enhanced corpus with more content for better demonstration
corpus = [
    # Apple as a fruit - food and health context
    "Eating fruits like apple is healthy and nutritious.",
    "I enjoy a crispy red apple as a snack.",
    "Apple pie is my favorite dessert made with fresh apples.",
    "Green apples are more tart than red apples.",
    "An apple a day keeps the doctor away - old saying about fruit.",
    "The orchard is full of apple trees ready for harvest.",
    "Apple juice is a popular fruit beverage.",
    "Sliced apples with peanut butter make a great snack.",
    "Apple cider is made from fermented apple juice.",
    "Fresh apple salad with walnuts and cranberries.",

    # Apple as a company - technology and business context
    "Apple released a new iPhone with advanced camera features.",
    "Tim Cook is the CEO of Apple Inc., the technology company.",
    "Apple's stock price surged after quarterly earnings report.",
    "The new MacBook Pro features Apple's M3 chip technology.",
    "Apple Park is the headquarters of Apple Inc. in Cupertino.",
    "Apple's App Store generated billions in revenue.",
    "Steve Jobs founded Apple Computer in 1976.",
    "Apple Watch is a popular wearable device from Apple.",
    "Apple's iOS operating system powers millions of devices.",
    "Apple announced new features for their streaming service.",

    # Mixed/ambiguous contexts
    "The Apple Store downtown sells both fruits and electronics.",
    "I dropped my apple while using my Apple phone.",
    "Apple products are displayed next to actual apples in the store window.",

    # Other fruits for contrast
    "Bananas are rich in potassium and good for athletes.",
    "Orange juice is packed with vitamin C.",
    "Strawberries are perfect for summer desserts.",

    # Other tech companies for contrast
    "Google announced new AI features for search.",
    "Microsoft released updates for Windows operating system.",
    "Amazon's cloud services continue to grow rapidly."
]

def search(query, top_k=5):
    """
    Common search method that finds semantically similar content.

    Args:
        query (str): The search query
        top_k (int): Number of top results to return

    Returns:
        list: List of tuples (text, score)
    """
    # Encode corpus and query
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Calculate cosine similarity
    cosine_scores = util.cos_sim(query_embedding, corpus_embeddings)
    top_results = cosine_scores[0].topk(top_k)

    # Format results
    results = []
    for score, idx in zip(top_results.values, top_results.indices):
        results.append((corpus[int(idx)], float(score)))

    return results

def display_results(query, results, context_emoji="🔍"):
    """Display search results in a formatted way."""
    print(f"\n{context_emoji} Query: '{query}'")
    print("=" * 60)

    for i, (text, score) in enumerate(results, 1):
        print(f"{i}. [{score:.4f}] {text}")
    print()

def main():
    """Main function to run the semantic search demo."""
    print("🔍 SEMANTIC SEARCH DEMO: Apple Context Comparison")
    print("=" * 60)

    # Search for apple as a fruit
    fruit_query = "I want to eat a healthy apple fruit"
    fruit_results = search(fruit_query, top_k=5)
    display_results(fruit_query, fruit_results, "🍎")

    # Search for apple as a company
    company_query = "Apple technology company stock price"
    company_results = search(company_query, top_k=5)
    display_results(company_query, company_results, "🏢")

    # Interactive search mode
    print("🔍 INTERACTIVE SEARCH MODE")
    print("=" * 40)
    print("Enter queries to see semantic search results.")
    print("Type 'quit' to exit.\n")

    while True:
        query = input("Enter your search query: ").strip()

        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break

        if query:
            results = search(query, top_k=3)
            display_results(query, results)
        else:
            print("Please enter a valid query.")

if __name__ == "__main__":
    main()
