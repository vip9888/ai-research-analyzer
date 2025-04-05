from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import shutil
from backend.database import get_db
from backend.models import ResearchPaper
from backend.services.embeddings import generate_embedding
from backend.utils.vector_store import store_embedding
from backend.utils.extract_text import extract_text_from_pdf, detect_title_from_text

# FastAPI APIRouter (APIRouter()) → Organizes API routes.
# Depends(get_db) → Injects the database session (db).
# UploadFile & File(...) → Handles file uploads.
# shutil.copyfileobj() → Saves the file to disk.
# SQLAlchemy (Session) → Manages database transactions.
# ResearchPaper → The ORM model representing the research_papers table.

router = APIRouter()

# APIRouter() creates an independent router for handling specific endpoints.
# This router can later be included in the main FastAPI app.


@router.post("/upload/")
async def upload_paper(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text and generate embedding
    text = extract_text_from_pdf(file_location)
    title = detect_title_from_text(text)
    embedding = generate_embedding(text)

    new_paper = ResearchPaper(title=title, filepath=file_location)
    db.add(new_paper)
    db.commit()


    #Store in VectorDB
    store_embedding(new_paper.id,embedding)

    return {"message": "File uploaded successfully", "file_path": file_location, "paper_id": new_paper.id, "title": new_paper.title}

# @router.post("/upload/") → Defines an HTTP POST endpoint at /upload/.
# Parameters:
# file: UploadFile = File(...)
# UploadFile → Represents the uploaded file.
# File(...) → Marks it as a required form-data file input.
# db: Session = Depends(get_db)
# Injects a database session using dependency injection (get_db() from database.py).
# This allows database operations inside the function.

# file_location: Defines where the file will be stored (uploads/filename.pdf).
# with open(file_location, "wb") as buffer:
# Opens the file in write-binary (wb) mode.
# shutil.copyfileobj(file.file, buffer) copies file data from memory to disk.


# new_paper = ResearchPaper(...):
# Creates a new database entry using the ResearchPaper ORM model.
# Stores the filename as the title and file path.
# db.add(new_paper): Adds the new entry to the database.
# db.commit(): Commits (saves) the changes to MySQL.

