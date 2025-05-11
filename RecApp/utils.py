import faiss
import numpy as np
import requests
import random
import os
from django.conf import settings


def load_item_embeddings():
    title_to_embedding = {}

    index = faiss.read_index("RecApp/vector_db/item_index.faiss")

    with open("RecApp/vector_db/titles.txt", "r", encoding="utf-8") as f:
        titles = [line.strip() for line in f]

    embeddings = index.reconstruct_n(0, index.ntotal)

    for title, embedding in zip(titles, embeddings):
        title_to_embedding[title] = np.array(embedding, dtype=np.float32)

    return title_to_embedding


def get_food_image(food_title):
    api_key = get_pexels_api_key()

    if not api_key:
        return "/api/placeholder/400/300"

    search_term = food_title.split("(")[0].strip()
    search_query = f"{search_term} food"

    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": api_key}
    params = {
        "query": search_query,
        "per_page": 3,
        "orientation": "landscape",
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        if data.get("photos") and len(data["photos"]) > 0:
            photo = random.choice(data["photos"])
            return photo["src"]["medium"]
        else:
            return "/api/placeholder/400/300"

    except Exception as e:
        print(f"Error fetching image from Pexels: {e}")
        return "/api/placeholder/400/300"


def get_pexels_api_key():
    return os.environ.get("PEXELS_API_KEY", getattr(settings, "PEXELS_API_KEY", ""))
