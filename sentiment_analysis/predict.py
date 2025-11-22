import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

def predict_sentiment(text):
    model_path = "./model_output"
    
    try:
        tokenizer = DistilBertTokenizer.from_pretrained(model_path)
        model = DistilBertForSequenceClassification.from_pretrained(model_path)
    except OSError:
        print("Model not found. Please run train_model.py first.")
        return

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    
    with torch.no_grad():
        logits = model(**inputs).logits
    
    predicted_class_id = logits.argmax().item()
    
    labels = {0: "Negative", 1: "Neutral", 2: "Positive"}
    sentiment = labels[predicted_class_id]
    
    return sentiment

if __name__ == "__main__":
    print("Sentiment Analysis Prediction")
    print("Enter a review to analyze (or 'q' to quit):")
    
    while True:
        user_input = input("> ")
        if user_input.lower() == 'q':
            break
        
        sentiment = predict_sentiment(user_input)
        if sentiment:
            print(f"Sentiment: {sentiment}")
