# Project Walkthrough

This project is a full-stack e-commerce application with a recommender system.

## Prerequisites
- Python 3.8+
- (Optional) VS Code "Live Server" extension for easier frontend viewing.

## Setup Instructions

### 1. Backend Setup
Navigate to the project root:
```bash
cd "d:\Personal\ADA-GWU Master\ML\Project Final"
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Start the Backend server:
```bash
uvicorn backend.main:app --reload
```
The API will be available at `http://localhost:8000`.

### 2. Machine Learning Setup
The ML components are in the `ml/` directory.

**Step 1: Download and Preprocess Data**
```bash
python ml/dataset.py
```
This will download the Online Retail II dataset and create `ml/data/processed_data.csv`.

**Step 2: Train the Model**
```bash
python ml/train.py
```
This trains the model and saves it to `ml/recommender_model.pth`.

**Step 3: Fine-tune (Optional)**
```bash
python ml/finetune.py
```

### 3. Frontend Setup
The frontend is now built with Vanilla HTML/CSS/JS for simplicity and performance.

1.  Navigate to the `frontend` folder.
2.  Open `index.html` in your browser.
    *   **Recommended**: Use a local server (like VS Code's "Live Server" or `python -m http.server`) to ensure API calls work correctly without CORS issues.
    *   If using Python:
        ```bash
        cd frontend
        python -m http.server 5173
        ```
        Then visit `http://localhost:5173`.

## Features
- **Premium UI**: Dark mode, glassmorphism, and responsive design.
- **Product Listing**: View available products (mocked/db).
- **Recommendations**: "Recommended for You" section powered by the PyTorch model.
- **Cart**: Add items to cart and view summary.
