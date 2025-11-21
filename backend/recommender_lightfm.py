import joblib
import numpy as np
from typing import List

MODEL_PATH = 'models/lightfm_model.pkl'

class LightFMRecommender:
    def __init__(self, model_path=MODEL_PATH):
        data = joblib.load(model_path)
        self.model = data['model']
        self.user2idx = data['user2idx']
        self.item2idx = data['item2idx']
        self.idx2item = {v: k for k, v in self.item2idx.items()}

    def recommend_for_user(self, user_id: str, k: int = 10) -> List[str]:
        user_key = str(user_id)
        if user_key not in self.user2idx:
            return []
        uid = self.user2idx[user_key]
        n_items = len(self.item2idx)
        scores = self.model.predict(uid, np.arange(n_items))
        top_idx = np.argsort(-scores)[:k]
        return [self.idx2item[int(i)] for i in top_idx]

# convenience factory
_recommender = None

def get_recommender(path=MODEL_PATH):
    global _recommender
    if _recommender is None:
        _recommender = LightFMRecommender(path)
    return _recommender
