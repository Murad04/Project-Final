"""
RecBole inference wrapper.

This module provides a small wrapper around RecBole to load a trained checkpoint
and produce top-N recommendations for a user. It intentionally contains defensive
imports and helpful error messages so you can run it locally after training with
`finetune_bert4rec.py`.

Usage:
    from backend.recommender_recbole import get_recommender
    r = get_recommender(dataset_name='retailrocket', model_name='BERT4Rec')
    r.recommend_for_user('123', k=10)

Notes:
- RecBole must be installed and a trained model must exist under RecBole's
  saved directory (default `saved/<dataset>_<model>/` when using run_recbole).
- If RecBole API changes, you may need to update the load logic accordingly.
"""
from typing import List, Optional

class RecBoleUnavailable(Exception):
    pass

def _import_recbole():
    try:
        from recbole.quick_start import load_data_and_model
        from recbole.utils.case_study import full_sort_topk
        return load_data_and_model, full_sort_topk
    except Exception as e:
        raise RecBoleUnavailable(
            "RecBole is not available or failed to import. Install recbole and torch."
        ) from e


class RecBoleRecommender:
    def __init__(self, dataset_name: str = 'retailrocket', model_name: str = 'BERT4Rec', saved_model: Optional[str] = None, device: Optional[str] = None):
        """Load dataset+model using RecBole helpers.

        - `dataset_name`: folder name under `dataset/` used by RecBole.
        - `model_name`: the RecBole model (e.g., 'BERT4Rec').
        - `saved_model`: optional path to a saved model file to load; if None,
          RecBole will look for the default saved model for the given dataset.
        - `device`: optional device string (e.g., 'cpu' or 'cuda:0'); leave None to use RecBole default.
        """
        load_data_and_model, full_sort_topk = _import_recbole()
        self._full_sort_topk = full_sort_topk
        # load dataset and model
        # load_data_and_model returns (dataset, model, config)
        try:
            self.dataset, self.model, self.config = load_data_and_model(
                model=model_name, dataset=dataset_name, saved_model=saved_model
            )
        except TypeError:
            # some recbole versions expect parameters in a different order
            self.dataset, self.model, self.config = load_data_and_model(
                dataset=dataset_name, model=model_name, saved_model=saved_model
            )
        # move model to requested device if provided
        if device is not None:
            try:
                self.model.to(device)
            except Exception:
                pass

    def recommend_for_user(self, user_id: str, k: int = 10) -> List[str]:
        """Return a list of top-k recommended item ids for the given user.

        The returned ids will be the raw item ids as used in the dataset (strings).
        """
        # full_sort_topk has different return types across versions; handle commonly used patterns
        try:
            result = self._full_sort_topk(self.config, self.model, user_id, 'user', k)
        except TypeError:
            # try alternate calling convention: (dataset, model, uid_list, top_k)
            try:
                result = self._full_sort_topk(self.dataset, self.model, [str(user_id)], k=k)
            except Exception as e:
                raise RuntimeError('full_sort_topk failed: ' + str(e))

        # normalize result to list of item ids
        # If result is a DataFrame or similar, extract item id column
        try:
            # If result is DataFrame with columns ['user_id','item_id','score']
            import pandas as pd

            if isinstance(result, pd.DataFrame):
                items = result['item_id'].astype(str).tolist()
                return items[:k]
        except Exception:
            pass

        # If result is list/tuple
        if isinstance(result, (list, tuple)):
            # sometimes full_sort_topk returns list of lists
            if len(result) and isinstance(result[0], (list, tuple)):
                # flatten first entry
                ids = [str(x) for x in result[0]]
                return ids[:k]
            # or it may be list of item ids
            return [str(x) for x in result][:k]

        # Unknown format
        raise RuntimeError('Unexpected full_sort_topk return type: %s' % type(result))


_global_recommender = None

def get_recommender(dataset_name: str = 'retailrocket', model_name: str = 'BERT4Rec', saved_model: Optional[str] = None, device: Optional[str] = None):
    global _global_recommender
    if _global_recommender is None:
        _global_recommender = RecBoleRecommender(dataset_name=dataset_name, model_name=model_name, saved_model=saved_model, device=device)
    return _global_recommender
