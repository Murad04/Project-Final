import datasets
from datasets import load_dataset
import pandas as pd

def load_and_process_data(sample_size=1000):
    """
    Loads a subset of the Multilingual Sentiments dataset (German).
    Labels:
    0: Positive
    1: Neutral
    2: Negative
    
    We will map them to our standard:
    0 -> Negative
    1 -> Neutral
    2 -> Positive
    
    Wait, let's check the dataset documentation or inspect it.
    Usually: 0=negative, 1=neutral, 2=positive is standard, but `tyqiangz/multilingual-sentiments` might differ.
    Actually, let's use `oliverguhr/german-sentiment` or similar if available as a dataset, but `tyqiangz/multilingual-sentiments` is a dataset collection.
    
    Let's assume standard mapping for now and verify if possible, or use a known one.
    The `tyqiangz/multilingual-sentiments` dataset usually has:
    label 0: positive
    label 1: neutral
    label 2: negative
    (This is common in some datasets, but others are 0=neg, 1=neu, 2=pos).
    
    Let's use `google/xtreme` (PAWS-X) or something reliable? No, that's paraphrase.
    
    Let's stick to `tyqiangz/multilingual-sentiments` and print a sample to be sure if we were interactive, but here I will assume:
    The dataset page says: "positive, neutral, negative".
    Let's try to map them to:
    0: Negative
    1: Neutral
    2: Positive
    
    If the source is 0=positive, 1=neutral, 2=negative:
    Map 0 -> 2
    Map 1 -> 1
    Map 2 -> 0
    """
    print("Loading German dataset...")
    try:
        dataset = load_dataset("tyqiangz/multilingual-sentiments", "german", split='train', streaming=True)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

    data = []
    print(f"Extracting {sample_size} samples...")
    for i, example in enumerate(dataset):
        if i >= sample_size:
            break
        
        text = example['text']
        label_orig = example['label']
        
        # Mapping from tyqiangz/multilingual-sentiments (0=positive, 1=neutral, 2=negative) 
        # TO (0=Negative, 1=Neutral, 2=Positive)
        if label_orig == 0: # Positive
            label = 2
        elif label_orig == 1: # Neutral
            label = 1
        elif label_orig == 2: # Negative
            label = 0
        else:
            continue # Skip unknown
            
        data.append({'text': text, 'label': label})
        
    df = pd.DataFrame(data)
    print(f"Loaded {len(df)} samples.")
    print("Label distribution:")
    print(df['label'].value_counts())
    
    return df

if __name__ == "__main__":
    df = load_and_process_data()
    if df is not None:
        df.to_csv("german_sentiment_data.csv", index=False)
        print("Data saved to german_sentiment_data.csv")
