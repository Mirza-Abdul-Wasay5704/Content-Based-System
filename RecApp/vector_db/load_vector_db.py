import pandas as pd
import faiss
import numpy as np

df = pd.read_csv("../data/Item_Embeddings.csv")

df["title"] = df["title"].str.title()

titles = df["title"].tolist()
embeddings = np.ascontiguousarray(
    df.drop(columns=["title"]).to_numpy().astype("float32")
)

faiss.normalize_L2(embeddings)

dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

faiss.write_index(index, "item_index.faiss")
with open("titles.txt", "w", encoding="utf-8") as f:
    for title in titles:
        f.write(title + "\n")
