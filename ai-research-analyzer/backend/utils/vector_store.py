import chromadb

# Initialize a ChromaDB collection
chroma_client = chromadb.PersistentClient(path="vector_db")
collection = chroma_client.get_or_create_collection(name="research_papers")

def store_embedding(paper_id, embedding):
    """Stores a research paper's embedding in the vector database."""
    collection.add(
        ids=[str(paper_id)], 
        embeddings=[embedding.tolist()]
    )

def find_similar_papers(query_embedding, top_k=5):
    """Finds the top-k similar research papers based on vector similarity."""
    results = collection.query(
        query_embeddings=[query_embedding.tolist()], 
        n_results=top_k
    )
    return results['ids'][0]  # Returns IDs of similar papers
