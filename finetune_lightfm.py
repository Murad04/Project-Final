import pandas as pd
import numpy as np
from scipy import sparse
from lightfm import LightFM
from lightfm.evaluation import precision_at_k
import joblib
import argparse
import os
from sklearn.model_selection import train_test_split

def load_interactions(path, user_col='user_id', item_col='item_id', time_col='timestamp', min_events_per_user=1):
    df = pd.read_csv(path)
    df = df.dropna(subset=[user_col, item_col])
    df[user_col] = df[user_col].astype(str)
    df[item_col] = df[item_col].astype(str)
    user_counts = df[user_col].value_counts()
    keep_users = user_counts[user_counts >= min_events_per_user].index
    df = df[df[user_col].isin(keep_users)]
    return df

def make_mapping(series):
    uniques = series.unique()
    return {v: i for i, v in enumerate(uniques)}, {i: v for i, v in enumerate(uniques)}

def make_interaction_matrix(df, user_col='user_id', item_col='item_id', user2idx=None, item2idx=None):
    if user2idx is None:
        user2idx, idx2user = make_mapping(df[user_col])
    if item2idx is None:
        item2idx, idx2item = make_mapping(df[item_col])
    rows = df[user_col].map(user2idx).to_numpy()
    cols = df[item_col].map(item2idx).to_numpy()
    data = np.ones(len(rows), dtype=np.int32)
    mat = sparse.coo_matrix((data, (rows, cols)), shape=(len(user2idx), len(item2idx))).tocsr()
    return mat, user2idx, item2idx

def train_lightfm(train_mat, epochs=30, no_components=64, learning_rate=0.05, loss='warp', threads=4):
    model = LightFM(no_components=no_components, learning_rate=learning_rate, loss=loss)
    model.fit(train_mat, epochs=epochs, num_threads=threads)
    return model

def main(args):
    os.makedirs(os.path.dirname(args.out_model), exist_ok=True)
    df = load_interactions(args.input_csv, min_events_per_user=args.min_events)
    if 'timestamp' in df.columns:
        df['ts'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
        df = df.sort_values(['user_id', 'ts'])
        test_idx = df.groupby('user_id').tail(1).index
        test_df = df.loc[test_idx]
        train_df = df.drop(test_idx)
        train_mat, user2idx, item2idx = make_interaction_matrix(train_df)
    else:
        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
        train_mat, user2idx, item2idx = make_interaction_matrix(train_df)

    model = train_lightfm(train_mat, epochs=args.epochs, no_components=args.latent_dim, learning_rate=args.lr, loss=args.loss, threads=args.threads)
    prec = precision_at_k(model, train_mat, k=10).mean()
    print(f'Precision@10 on train (approx): {prec:.4f}')
    joblib.dump({'model': model, 'user2idx': user2idx, 'item2idx': item2idx}, args.out_model)
    print('Saved model to', args.out_model)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-csv', default='data/interactions.csv')
    parser.add_argument('--out-model', default='models/lightfm_model.pkl')
    parser.add_argument('--epochs', type=int, default=30)
    parser.add_argument('--latent-dim', type=int, default=64)
    parser.add_argument('--lr', type=float, default=0.05)
    parser.add_argument('--loss', default='warp')
    parser.add_argument('--min-events', type=int, default=1)
    parser.add_argument('--threads', type=int, default=4)
    args = parser.parse_args()
    main(args)
