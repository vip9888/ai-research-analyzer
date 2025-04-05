# from transformers import pipeline

# # Load the summarization model (you can replace this with a better model)
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# def generate_summary(text):
#     """Generates a summary from the extracted text."""
#     if len(text) < 100:
#         return "Text is too short to summarize."

#     # Limit input length for better performance
#     input_text = text[:1024]  # BART model has a limit
    
#     summary = summarizer(input_text, max_length=200, min_length=50, do_sample=False)
#     return summary[0]['summary_text']

from transformers import pipeline, AutoTokenizer
from keybert import KeyBERT

# Load the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

kw_model = KeyBERT()

def generate_summary(text: str) -> str:
    MAX_TOKENS = 1024

    if not text or not text.strip():
        raise ValueError("Text for summarization is empty or whitespace.")

    # Tokenize and truncate safely with tokenizer itself
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=MAX_TOKENS)

    # Generate summary using tokenized inputs
    summary_ids = summarizer.model.generate(
        inputs["input_ids"],
        max_length=300,
        min_length=100,
        do_sample=False
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

def extract_keywords(text: str):
    """Extracts important keywords from text."""
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=5)
    return [kw[0] for kw in keywords]
