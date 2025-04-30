import faiss
import numpy as np

class FaissHandler:
    def __init__(self, index_path, titles_path):
        # Load the FAISS index
        self.index = faiss.read_index(index_path)

        # Load the titles
        with open(titles_path, "r", encoding="utf-8") as f:
            self.titles = [line.strip() for line in f.readlines()]

    def get_top_k(self, user_embedding, k=10):
        # Ensure embedding is float32 and in correct shape
        user_embedding = np.array(user_embedding, dtype='float32').reshape(1, -1)

        # Normalize for cosine similarity
        faiss.normalize_L2(user_embedding)

        # Search for top-k similar items
        scores, indices = self.index.search(user_embedding, k)

        # Get the corresponding titles and similarity scores
        results = [(self.titles[i], float(scores[0][idx])) for idx, i in enumerate(indices[0])]
        return results
