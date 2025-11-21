"""
Convert Retailrocket dataset in `dd/` to a simple interactions CSV for LightFM and a products CSV for seeding DB.
Input files expected in `dd/`:
 - events.csv (visitorid,itemid,eventdate,...)
 - item_properties_part1.csv, item_properties_part2.csv (optional product metadata)

Outputs:
 - data/interactions.csv (user_id,item_id,timestamp)
 - data/products.csv (id,name,category) optional minimal seed file (id matches item_id from events)

Usage:
    python tools/convert_retailrocket.py --dd-dir dd --out-dir data

"""
import pandas as pd
import argparse
import os


def load_events(dd_dir):
    path = os.path.join(dd_dir, 'events.csv')
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    # read in chunks to avoid memory issues (keep only needed cols)
    usecols = None
    # We'll try to infer columns; common names: visitorid,itemid,eventdate
    # Read header first
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        header = f.readline().strip().split(',')
    header_lower = [h.lower() for h in header]
    # choose columns
    if 'visitorid' in header_lower and 'itemid' in header_lower and 'eventdate' in header_lower:
        usecols = ['visitorid', 'itemid', 'eventdate']
    elif 'visitorid' in header_lower and 'itemid' in header_lower:
        usecols = ['visitorid', 'itemid']
    else:
        # fallback: read first 5 cols
        usecols = header[:5]

    df = pd.read_csv(path, usecols=usecols, dtype=str, parse_dates=False, low_memory=True)
    df.columns = [c.lower() for c in df.columns]
    return df


def convert_events(df):
    # Map to user_id, item_id, timestamp
    if 'eventdate' in df.columns:
        df['timestamp'] = pd.to_datetime(df['eventdate'], errors='coerce')
        # convert to unix seconds
        df['timestamp'] = (df['timestamp'].astype('int64') // 10**9).fillna(0).astype(int)
    else:
        df['timestamp'] = pd.RangeIndex(len(df))
    if 'visitorid' in df.columns:
        df['user_id'] = df['visitorid']
    elif 'userid' in df.columns:
        df['user_id'] = df['userid']
    else:
        df['user_id'] = df.index.astype(str)
    if 'itemid' in df.columns:
        df['item_id'] = df['itemid']
    elif 'productid' in df.columns:
        df['item_id'] = df['productid']
    else:
        raise RuntimeError('No item id column found')
    out = df[['user_id', 'item_id', 'timestamp']].dropna()
    # cast to str
    out['user_id'] = out['user_id'].astype(str)
    out['item_id'] = out['item_id'].astype(str)
    return out


def build_products(dd_dir, out_dir):
    # combine item_properties parts if present
    parts = []
    for p in ['item_properties_part1.csv', 'item_properties_part2.csv']:
        path = os.path.join(dd_dir, p)
        if os.path.exists(path):
            parts.append(pd.read_csv(path, dtype=str, low_memory=True))
    if not parts:
        return None
    df = pd.concat(parts, ignore_index=True)
    # expected columns: itemid, property, value ; or itemid, name, category
    cols = [c.lower() for c in df.columns]
    if 'itemid' in cols:
        df.columns = cols
        if 'name' in cols or 'title' in cols:
            name_col = 'name' if 'name' in cols else ('title' if 'title' in cols else None)
            # pivot to get name/category per item if multiple rows
            prod = df.groupby('itemid').first().reset_index()
            prod_out = prod[['itemid']].copy()
            if name_col:
                prod_out['name'] = prod[name_col]
            else:
                prod_out['name'] = prod_out['itemid']
            # category fallback
            if 'category' in cols:
                prod_out['category'] = prod['category']
            else:
                prod_out['category'] = ''
            prod_out = prod_out.rename(columns={'itemid':'id'})
            return prod_out
    return None


def main(args):
    dd_dir = args.dd_dir
    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)
    print('Loading events from', dd_dir)
    df_raw = load_events(dd_dir)
    print('Converting events...')
    interactions = convert_events(df_raw)
    out_path = os.path.join(out_dir, 'interactions.csv')
    interactions.to_csv(out_path, index=False)
    print('Saved interactions to', out_path)
    print('Building products.csv (if available)')
    products = build_products(dd_dir, out_dir)
    if products is not None:
        prod_path = os.path.join(out_dir, 'products.csv')
        products.to_csv(prod_path, index=False)
        print('Saved products to', prod_path)
    else:
        print('No product metadata found or unable to build products.csv')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dd-dir', default='dd')
    parser.add_argument('--out-dir', default='data')
    args = parser.parse_args()
    main(args)
