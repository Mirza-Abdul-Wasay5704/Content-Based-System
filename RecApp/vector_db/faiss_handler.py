import faiss
import numpy as np


class FaissHandler:
    def __init__(self, index_path, titles_path):
        self.index = faiss.read_index(index_path)

        with open(titles_path, "r", encoding="utf-8") as f:
            self.titles = [line.strip() for line in f.readlines()]

    def get_top_k(self, user_embedding, k=10):
        user_embedding = np.array(user_embedding, dtype="float32").reshape(1, -1)

        faiss.normalize_L2(user_embedding)

        scores, indices = self.index.search(user_embedding, k)

        results = [
            (self.titles[i], float(scores[0][idx])) for idx, i in enumerate(indices[0])
        ]
        return results
