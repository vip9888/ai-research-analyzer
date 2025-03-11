from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import shutil
from database import get_db
from models import ResearchPaper

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

    new_paper = ResearchPaper(title=file.filename, filepath=file_location)
    db.add(new_paper)
    db.commit()
    return {"message": "File uploaded successfully", "file_path": file_location}


# new_paper = ResearchPaper(...):
# Creates a new database entry using the ResearchPaper ORM model.
# Stores the filename as the title and file path.
# db.add(new_paper): Adds the new entry to the database.
# db.commit(): Commits (saves) the changes to MySQL.

