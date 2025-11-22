# Sentiment Analysis Walkthrough

I have implemented a Sentiment Analysis system using DistilBERT and the Yelp Reviews dataset (mapped to Positive, Negative, Neutral).

## 1. Setup

First, install the required libraries:

```bash
pip install -r requirements.txt
```

## 2. Data Loading

Run the data loader to download and preprocess the dataset. This will create a `sentiment_data.csv` file.

```bash
python data_loader.py
```

## 3. Model Training

Fine-tune the DistilBERT model on the data. This script will train the model for 1 epoch and save it to the `model_output` directory.

```bash
python train_model.py
```

> [!NOTE]
> Training may take some time depending on your hardware (GPU is recommended).

## 4. Prediction

Once the model is trained, you can use the prediction script to analyze new reviews.

```bash
python predict.py
```

Example usage:
```
> The product was amazing! I loved it.
Sentiment: Positive
> It broke after one day. Terrible.
Sentiment: Negative
```
