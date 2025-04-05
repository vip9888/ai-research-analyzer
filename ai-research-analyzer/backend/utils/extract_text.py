import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    doc = fitz.open(pdf_path)
    
    for page in doc:
        text += page.get_text("text") + "\n"
    
    return text



def detect_title_from_text(text: str) -> str:
    """
    Tries to detect the title from the first few lines of the PDF text.
    Assumes the first non-email, non-author-looking, non-generic line is likely the title.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    # Heuristic filters
    for line in lines[:20]:  # check only first 20 lines
        # Skip lines that look like emails or affiliations
        if re.search(r"@|www\.|http", line, re.IGNORECASE):
            continue
        if re.search(r"university|department|college|institute", line, re.IGNORECASE):
            continue
        if 5 < len(line.split()) < 25:  # decent length line
            return line.strip()

    return "Untitled Research Paper"

