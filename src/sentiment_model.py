from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Load FinBERT model (finance-specific sentiment)
model_name = "yiyanghkust/finbert-tone"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

finance_sentiment = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def get_sentiment(text: str):
    """
    Analyze financial sentiment of a text using FinBERT.
    
    Args:
        text (str): Stock or finance-related article text.
    
    Returns:
        tuple: (label: POSITIVE/NEGATIVE/NEUTRAL, score: float)
    """
    if not text.strip():
        return "NEUTRAL", 0.0

    # FinBERT handles longer financial text, but truncate to 512 tokens for speed
    truncated_text = text[:512]
    result = finance_sentiment(truncated_text)[0]
    
    label = result['label'].upper()  # POSITIVE / NEGATIVE / NEUTRAL
    score = round(result['score'], 3)
    
    return label, score

# -------------------------
# Example run
if __name__ == "__main__":
    sample_texts = [
        "Infosys announces ₹18,000 crore buyback; CEO cites strong pipeline",
        "Infosys share price falls 2% after Q2 results",
        "TCS layoffs lead to concern among investors"
    ]

    for text in sample_texts:
        label, score = get_sentiment(text)
        print(f"Text: {text}\nSentiment: {label}, Score: {score}\n")
