"""
Prepare RecBole dataset from `data/interactions.csv`.
- Input: `data/interactions.csv` with columns `user_id,item_id,timestamp` (timestamp optional but recommended)
- Output: `dataset/<dataset_name>/train.csv`, `valid.csv`, `test.csv` with the same columns

Splitting strategy (per-user):
- If user has >=3 interactions: last -> test, second last -> valid, rest -> train
- If user has 2 interactions: last -> test, first -> train
- If user has 1 interaction: goes to train

Usage:
    python tools/prepare_recbole.py --input data/interactions.csv --out dataset/retailrocket

"""
import pandas as pd
import argparse
import os


def prepare(input_csv, out_dir, user_col='user_id', item_col='item_id', time_col='timestamp'):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(input_csv)
    df = df.dropna(subset=[user_col, item_col])
    # Ensure timestamp exists and is sortable
    if time_col in df.columns:
        df['ts'] = pd.to_datetime(df[time_col], unit='s', errors='coerce')
        # If parse failed, fallback to numeric
        if df['ts'].isnull().all():
            try:
                df['ts'] = pd.to_numeric(df[time_col], errors='coerce')
            except Exception:
                df['ts'] = 0
    else:
        df['ts'] = pd.RangeIndex(len(df))

    df = df.sort_values([user_col, 'ts'])

    train_rows = []
    valid_rows = []
    test_rows = []

    grouped = df.groupby(user_col)
    for uid, group in grouped:
        n = len(group)
        if n >= 3:
            train = group.iloc[:-2]
            valid = group.iloc[-2:-1]
            test = group.iloc[-1:]
        elif n == 2:
            train = group.iloc[:-1]
            valid = pd.DataFrame(columns=group.columns)
            test = group.iloc[-1:]
        else:
            train = group
            valid = pd.DataFrame(columns=group.columns)
            test = pd.DataFrame(columns=group.columns)

        train_rows.append(train)
        if not valid.empty:
            valid_rows.append(valid)
        if not test.empty:
            test_rows.append(test)

    df_train = pd.concat(train_rows, ignore_index=True) if train_rows else pd.DataFrame(columns=df.columns)
    df_valid = pd.concat(valid_rows, ignore_index=True) if valid_rows else pd.DataFrame(columns=df.columns)
    df_test = pd.concat(test_rows, ignore_index=True) if test_rows else pd.DataFrame(columns=df.columns)

    # Keep only required columns
    keep_cols = [user_col, item_col, time_col] if time_col in df.columns else [user_col, item_col]
    # If time_col is missing use ts as timestamp
    if time_col not in df.columns:
        df_train = df_train.rename(columns={'ts': 'timestamp'})
        df_valid = df_valid.rename(columns={'ts': 'timestamp'})
        df_test = df_test.rename(columns={'ts': 'timestamp'})
        keep_cols = [user_col, item_col, 'timestamp']

    train_path = os.path.join(out_dir, 'train.csv')
    valid_path = os.path.join(out_dir, 'valid.csv')
    test_path = os.path.join(out_dir, 'test.csv')

    df_train[keep_cols].to_csv(train_path, index=False)
    df_valid[keep_cols].to_csv(valid_path, index=False)
    df_test[keep_cols].to_csv(test_path, index=False)

    print('Saved train/valid/test to', out_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/interactions.csv')
    parser.add_argument('--out', default='dataset/retailrocket')
    args = parser.parse_args()
    prepare(args.input, args.out)
