import datasets
from datasets import load_dataset
import pandas as pd

def load_and_process_data(sample_size=1000):
    """
    Loads a subset of the Yelp Review Full dataset.
    Labels are 0-4 (corresponding to 1-5 stars).
    Maps to sentiment:
    0 (1 star), 1 (2 stars) -> Negative (0)
    2 (3 stars) -> Neutral (1)
    3 (4 stars), 4 (5 stars) -> Positive (2)
    """
    print("Loading dataset...")
    try:
        # using yelp_review_full as alternative to amazon_reviews_multi
        dataset = load_dataset("yelp_review_full", split='train', streaming=True)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

    data = []
    print(f"Extracting {sample_size} samples...")
    for i, example in enumerate(dataset):
        if i >= sample_size:
            break
        
        label_orig = example['label']
        text = example['text']
        
        if label_orig <= 1:
            label = 0 # Negative
        elif label_orig == 2:
            label = 1 # Neutral
        else:
            label = 2 # Positive
            
        data.append({'text': text, 'label': label})
        
    df = pd.DataFrame(data)
    print(f"Loaded {len(df)} samples.")
    print("Label distribution:")
    print(df['label'].value_counts())
    
    return df

if __name__ == "__main__":
    df = load_and_process_data()
    if df is not None:
        df.to_csv("sentiment_data.csv", index=False)
        print("Data saved to sentiment_data.csv")
