from sentence_transformers import SentenceTransformer

# Load a pre-trained model for embedding generation
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text):
    """Generates an embedding vector for the given text."""
    return embedding_model.encode(text, convert_to_numpy=True)

