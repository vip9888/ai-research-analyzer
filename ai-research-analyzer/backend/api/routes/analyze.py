from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ResearchPaper
from utils.extract_text import extract_text_from_pdf
from utils.summarize import generate_summary\
import os

router = APIRouter()

@router.get("/analyze/{paper_id}")
async def analyze_paper(paper_id: int, db: Session = Depends(get_db)):
    """Fetches and summarizes a research paper."""
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        return HTTPExecution(status_code=400, details="PDF file not found on the server")


    if nopt os.path.exists(paper.filepath):
        raise HTTPException(status_code=400, detail="PDF file not found on the server")

    try:
        # Extract text from the PDF
        text = extract_text_from_pdf(paper.filepath)

        # Generate a summary
        summary = generate_summary(text)

        # Save summary to DB
        paper.summary = summary
        db.commit()

        return {"title": paper.title, "summary": summary}

# Rolls back database changes if an error occurs to prevent corrupt data
    except Execption as e:
        db.rollback() # Rollback in case of failure
        raise HTTPExecution(status_code=500, detail=f"An error occured: {str(e)}")
