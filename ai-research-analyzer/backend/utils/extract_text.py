import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    doc = fitz.open(pdf_path)
    
    for page in doc:
        text += page.get_text("text") + "\n"
    
    return text
