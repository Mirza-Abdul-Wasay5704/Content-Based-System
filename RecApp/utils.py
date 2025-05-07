import faiss
import numpy as np


def load_item_embeddings():
    title_to_embedding = {}

    # Load FAISS index
    index = faiss.read_index("RecApp/vector_db/item_index.faiss")

    # Load titles
    with open("RecApp/vector_db/titles.txt", "r", encoding="utf-8") as f:
        titles = [line.strip() for line in f]

    # Reconstruct embeddings from FAISS index
    embeddings = index.reconstruct_n(0, index.ntotal)  # List of vectors

    for title, embedding in zip(titles, embeddings):
        title_to_embedding[title] = np.array(embedding, dtype=np.float32)

    return title_to_embedding
