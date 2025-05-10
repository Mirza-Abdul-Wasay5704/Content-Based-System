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


# Add this new function to RecApp/utils.py
import requests
import random
import os
from django.conf import settings

def get_food_image(food_title):
    """
    Get an image URL for a food item from Pexels API.
    
    Args:
        food_title (str): The title of the food item to search for
    
    Returns:
        str: URL of the food image or a placeholder if no image is found
    """
    # You'll need to get a free Pexels API key from https://www.pexels.com/api/
    # Add this to your environment variables or settings.py
    api_key = get_pexels_api_key()
    
    # If no API key is set, return a placeholder
    if not api_key:
        return "/api/placeholder/400/300"
    
    # Clean the food title for better search results
    search_term = food_title.split('(')[0].strip()  # Remove anything in parentheses
    search_query = f"{search_term} food"  # Add "food" to improve search results
    
    # Make request to Pexels API
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": api_key}
    params = {
        "query": search_query,
        "per_page": 3,  # Request a few options
        "orientation": "landscape"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        
        # Check if we have photos
        if data.get("photos") and len(data["photos"]) > 0:
            # Select a random photo from the results
            photo = random.choice(data["photos"])
            # Get the medium sized image
            return photo["src"]["medium"]
        else:
            # Return placeholder if no image found
            return "/api/placeholder/400/300"
            
    except Exception as e:
        print(f"Error fetching image from Pexels: {e}")
        # Return placeholder in case of error
        return "/api/placeholder/400/300"


# Add this function to store the API key
def get_pexels_api_key():
    """
    Get the Pexels API key. First check environment variables, then check settings.
    
    Returns:
        str: The Pexels API key
    """
    return os.environ.get('PEXELS_API_KEY', getattr(settings, 'PEXELS_API_KEY', ''))