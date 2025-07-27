import pandas as pd

# Load CSV
df = pd.read_csv("data/train_mini.csv")

# Add 'id' column starting from 1
df.insert(0, "id", range(1, len(df) + 1))  # id = 1, 2, 3, ...

# Save first 1000 rows with ID column
df.head(1000).to_csv("data/amazon_product_reviews_1000_utf8.csv", index=False, encoding="utf-8")
