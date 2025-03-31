from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import ResearchPaper
from backend.services.embeddings import generate_embedding
from backend.utils.vector_store import find_similar_papers
from backend.utils.extract_text import extract_text_from_pdf
import requests

router = APIRouter()

# API URLs for fetching papers from the internet
CROSSREF_API_URL = "https://api.crossref.org/works"
SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def fetch_papers_from_crossref(query):
    """Fetch research papers from CrossRef API."""
    params = {"query": query, "rows": 5}
    response = requests.get(CROSSREF_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return [{"title": item["title"][0], "link": item["URL"]} for item in data.get("message", {}).get("items", [])]
    return []

def fetch_papers_from_semantic_scholar(query):
    """Fetch research papers from Semantic Scholar API."""
    params = {"query": query, "limit": 5, "fields": "title,url"}
    response = requests.get(SEMANTIC_SCHOLAR_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return [{"title": paper["title"], "link": paper["url"]} for paper in data.get("data", [])]
    return []

@router.get("/recommend/{paper_id}")
def recommend_papers(
    paper_id: int,
    source: str = Query("local", enum=["local", "internet"]),
    db: Session = Depends(get_db),
):
    """Find similar research papers from local DB or internet with better query context."""
    
    # Fetch the target research paper
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        return {"error": "Paper not found"}

    # Use abstract if available, otherwise extract text from PDF
    query_text = paper.summary if paper.summary else extract_text_from_pdf(paper.filepath)
    
    # Limit query length for better API results
    query_text = " ".join(query_text.split()[:50])  # First 50 words

    if source == "local":
        # Generate embedding and find similar papers locally
        query_embedding = generate_embedding(query_text)
        similar_paper_ids = find_similar_papers(query_embedding)
        recommended_papers = db.query(ResearchPaper).filter(ResearchPaper.id.in_(similar_paper_ids)).all()
        return {
            "source": "local",
            "paper": {"title": paper.title},
            "recommendations": [{"id": p.id, "title": p.title} for p in recommended_papers],
        }

    else:  # Internet Search with better query
        crossref_papers = fetch_papers_from_crossref(query_text)
        semantic_papers = fetch_papers_from_semantic_scholar(query_text)
        return {
            "source": "internet",
            "paper": {"title": paper.title},
            "recommendations": crossref_papers + semantic_papers,
        }
