import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import os

def train():
    # 1. Load Data
    if not os.path.exists("sentiment_data.csv"):
        print("sentiment_data.csv not found. Running data_loader...")
        import data_loader
        data_loader.load_and_process_data()
        
    df = pd.read_csv("sentiment_data.csv")
    
    # 2. Preprocess
    # Convert to Hugging Face Dataset
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    
    train_dataset = Dataset.from_pandas(train_df)
    test_dataset = Dataset.from_pandas(test_df)
    
    # 3. Tokenization
    model_name = "distilbert-base-uncased"
    tokenizer = DistilBertTokenizer.from_pretrained(model_name)
    
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)
    
    print("Tokenizing data...")
    tokenized_train = train_dataset.map(tokenize_function, batched=True)
    tokenized_test = test_dataset.map(tokenize_function, batched=True)
    
    # 4. Model Setup
    # 3 labels: Negative (0), Neutral (1), Positive (2)
    model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=3)
    
    # 5. Training Arguments
    training_args = TrainingArguments(
        output_dir="./results",
        eval_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,  # Small batch size for compatibility
        per_device_eval_batch_size=8,
        num_train_epochs=1,             # Only 1 epoch for demonstration/speed
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
    )
    
    # 6. Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_test,
    )
    
    # 7. Train
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    model.to(device)
    
    print("Starting training...")
    trainer.train()
    
    # 8. Save Model
    print("Saving model...")
    model.save_pretrained("./model_output")
    tokenizer.save_pretrained("./model_output")
    print("Model saved to ./model_output")

if __name__ == "__main__":
    train()
