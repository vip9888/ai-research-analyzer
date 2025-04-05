# from fastapi import APIRouter, Depends, Query
# from sqlalchemy.orm import Session
# from backend.database import get_db
# from backend.models import ResearchPaper
# from backend.services.embeddings import generate_embedding
# from backend.utils.vector_store import find_similar_papers
# from backend.utils.extract_text import extract_text_from_pdf
# import requests

# router = APIRouter()

# # API URLs for fetching papers from the internet
# CROSSREF_API_URL = "https://api.crossref.org/works"
# SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

# def fetch_papers_from_crossref(query):
#     """Fetch research papers from CrossRef API."""
#     params = {"query": query, "rows": 5}
#     response = requests.get(CROSSREF_API_URL, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         return [{"title": item["title"][0], "link": item["URL"]} for item in data.get("message", {}).get("items", [])]
#     return []

# def fetch_papers_from_semantic_scholar(query):
#     """Fetch research papers from Semantic Scholar API."""
#     params = {"query": query, "limit": 5, "fields": "title,url"}
#     response = requests.get(SEMANTIC_SCHOLAR_API_URL, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         return [{"title": paper["title"], "link": paper["url"]} for paper in data.get("data", [])]
#     return []

# @router.get("/recommend/{paper_id}")
# def recommend_papers(
#     paper_id: int,
#     source: str = Query("local", enum=["local", "internet"]),
#     db: Session = Depends(get_db),
# ):
#     """Find similar research papers from local DB or internet with better query context."""
    
#     # Fetch the target research paper
#     paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
#     if not paper:
#         return {"error": "Paper not found"}

#     # Use summary if available, otherwise extract text from PDF
#     query_text = paper.summary if paper.summary else extract_text_from_pdf(paper.filepath)
    
#     # Limit query length for better API results
#     query_text = " ".join(query_text.split()[:50])  # First 50 words

#     if source == "local":
#         # Generate embedding and find similar papers locally
#         query_embedding = generate_embedding(query_text)
#         similar_paper_ids = find_similar_papers(query_embedding)
#         recommended_papers = db.query(ResearchPaper).filter(ResearchPaper.id.in_(similar_paper_ids)).all()
#         return {
#             "source": "local",
#             "paper": {"title": paper.title},
#             "recommendations": [{"id": p.id, "title": p.title} for p in recommended_papers],
#         }

#     else:  # Internet Search with better query
#         crossref_papers = fetch_papers_from_crossref(query_text)
#         semantic_papers = fetch_papers_from_semantic_scholar(query_text)
#         return {
#             "source": "internet",
#             "paper": {"title": paper.title},
#             "recommendations": crossref_papers + semantic_papers,
#         }


from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import ResearchPaper
from backend.services.embeddings import generate_embedding
from backend.utils.vector_store import find_similar_papers
from backend.services.nlp import generate_summary, extract_keywords
import requests

router = APIRouter()

# API URLs
CROSSREF_API_URL = "https://api.crossref.org/works"
SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def fetch_papers_from_crossref(query: str):
    """Fetch research papers from CrossRef API."""
    params = {"query": query, "rows": 5}
    response = requests.get(CROSSREF_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return [{"title": item["title"][0], "link": item["URL"]} for item in data.get("message", {}).get("items", [])]
    return []

def fetch_papers_from_semantic_scholar(query: str):
    """Fetch research papers from Semantic Scholar API."""
    params = {
        "query": query.lower(),
        "limit": 5,
        "fields": "title,url,abstract"
    }
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
    """Find similar research papers from local DB or the internet using improved query construction."""

    # Fetch the paper
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        return {"error": "Paper not found"}

    # Build the search query
    if not paper.content or not paper.content.strip():
        print(f"[WARN] Paper ID {paper.id} has no content.")
        search_text = paper.title
    else:
        summary = generate_summary(paper.content)
        search_text = f"{paper.title}. {summary}"

        # Fallback: If summary is too short, enrich with extracted keywords
        if len(search_text.split()) < 10:
            keywords = extract_keywords(paper.content[:1500])
            search_text += " " + " ".join(keywords)

    print(f"[DEBUG] Final search query: {search_text}")

    if source == "local":
        # Local recommendation using embeddings
        query_embedding = generate_embedding(paper.content[:1000])
        similar_paper_ids = find_similar_papers(query_embedding)
        recommended_papers = db.query(ResearchPaper).filter(ResearchPaper.id.in_(similar_paper_ids)).all()
        return {
            "source": "local",
            "paper": {"title": paper.title},
            "recommendations": [{"id": p.id, "title": p.title} for p in recommended_papers],
        }

    else:
        # Internet recommendation using external APIs
        crossref_papers = fetch_papers_from_crossref(search_text)
        semantic_papers = fetch_papers_from_semantic_scholar(search_text)
        return {
            "source": "internet",
            "paper": {"title": paper.title},
            "recommendations": crossref_papers + semantic_papers,
        }
