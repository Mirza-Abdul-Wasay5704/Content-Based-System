import numpy as np
import csv

def load_item_embeddings():
    title_to_embedding = {}

    # Load titles
    with open('RecApp/vector_db/titles.txt', 'r', encoding='utf-8') as f:
        titles = [line.strip() for line in f]

    # Load item embeddings using csv.reader
    with open('RecApp/data/Item_Embeddings.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            title = row[0]
            embedding = np.array([float(x) for x in row[1:]], dtype=np.float32)
            title_to_embedding[title] = embedding

    return title_to_embedding
