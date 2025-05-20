# faq_data.py
import os
import pickle
import hashlib
from sentence_transformers import SentenceTransformer
from v1.faq_data import faq_data

# Cache directory
CACHE_DIR = "./embeddings_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_PATH = os.path.join(CACHE_DIR, "faq_embeddings.pkl")

# Generate hash based on question texts to detect changes
def get_data_hash(data):
    questions = [entry["q"] for entry in data]
    return hashlib.md5("".join(questions).encode()).hexdigest()

def load_or_create_embeddings(data):
    data_hash = get_data_hash(data)

    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "rb") as f:
            cache = pickle.load(f)
        if cache.get("hash") == data_hash:
            for i, entry in enumerate(data):
                entry["embedding"] = cache["embeddings"][i]
            return

    # If no cache or data changed → regenerate
    print("Generating new embeddings...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    questions = [entry["q"] for entry in data]
    embeddings = model.encode(questions, convert_to_tensor=True)

    # Save to file
    with open(CACHE_PATH, "wb") as f:
        pickle.dump({
            "hash": data_hash,
            "embeddings": embeddings
        }, f)

    # Attach embeddings to data
    for i, entry in enumerate(data):
        entry["embedding"] = embeddings[i]

# Run embedding logic on import
load_or_create_embeddings(faq_data)
