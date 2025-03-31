from transformers import pipeline

# Load the summarization model (you can replace this with a better model)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text):
    """Generates a summary from the extracted text."""
    if len(text) < 100:
        return "Text is too short to summarize."

    # Limit input length for better performance
    input_text = text[:1024]  # BART model has a limit
    
    summary = summarizer(input_text, max_length=200, min_length=50, do_sample=False)
    return summary[0]['summary_text']
