import pandas as pd
import faiss
import numpy as np

# Load the CSV
df = pd.read_csv("../data/Item_Embeddings.csv")

# Separate titles and vectors
titles = df['title'].tolist()
embeddings = np.ascontiguousarray(df.drop(columns=['title']).to_numpy().astype('float32'))

# Normalize embeddings for cosine similarity
faiss.normalize_L2(embeddings)

# Create FAISS index using Inner Product (IP)
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

# Save the index and titles
faiss.write_index(index, "item_index.faiss")
with open("titles.txt", "w", encoding="utf-8") as f:
    for title in titles:
        f.write(title + "\n")
