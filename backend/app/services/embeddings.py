from sentence_transformers import SentenceTransformer
from functools import lru_cache

@lru_cache()
def get_embedding_model() -> SentenceTransformer:
    print("Loading embedding model (first load only)...")
    return SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text: str) -> list[float]:
    model = get_embedding_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()

def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
    return embeddings.tolist()