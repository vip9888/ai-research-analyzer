from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import ResearchPaper
from backend.utils.extract_text import extract_text_from_pdf
from backend.services.nlp import generate_summary
import os

router = APIRouter()

@router.get("/analyze/{paper_id}")
async def analyze_paper(paper_id: int, db: Session = Depends(get_db)):
    """Fetches and summarizes a research paper."""
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=400, detail="PDF file not found on the server")


    if not os.path.exists(paper.filepath):
        raise HTTPException(status_code=400, detail="PDF file not found on the server")

    try:
        # Extract text from the PDF
        text = extract_text_from_pdf(paper.filepath)

        print(f"[DEBUG] Extracted text length: {len(text)}")
        print(f"[DEBUG] First 300 chars: {repr(text[:300])}")

        # Generate a summary
        summary = generate_summary(text)

        # Save summary to DB
        paper.summary = summary
        db.commit()

        return {"title": paper.title, "summary": summary}

# Rolls back database changes if an error occurs to prevent corrupt data
    except Exception as e:
        db.rollback() # Rollback in case of failure
        print(f"[ERROR] Exception occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occured: {str(e)}")






