"""
Fine-tune BERT4Rec using RecBole. Expects dataset in `dataset/<name>/` with `train.csv`, `valid.csv`, `test.csv`.
Usage:
    python finetune_bert4rec.py --dataset retailrocket --epochs 20

Note: Install RecBole and PyTorch before running:
    pip install recbole
    pip install torch  # or follow https://pytorch.org
"""
from recbole.quick_start import run_recbole
from recbole.config import Config
import argparse


def main(args):
    config_dict = {
        'model': 'BERT4Rec',
        'dataset': args.dataset,
        'epochs': args.epochs,
        'train_batch_size': args.batch_size,
        'learning_rate': args.lr,
        'embedding_size': args.embedding_dim,
        'save_model': True,
        'eval_args': {'split': {'RS': [0.8, 0.1, 0.1]}},
        'max_seq_len': args.max_seq_len,
        # additional BERT4Rec params
        'hidden_size': args.hidden_size,
        'num_layers': args.num_layers,
        'num_heads': args.num_heads,
    }

    config = Config(model='BERT4Rec', dataset=args.dataset, config_dict=config_dict)
    run_recbole(config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='retailrocket')
    parser.add_argument('--epochs', type=int, default=20)
    parser.add_argument('--batch-size', type=int, default=128)
    parser.add_argument('--lr', type=float, default=1e-4)
    parser.add_argument('--embedding-dim', type=int, default=64)
    parser.add_argument('--max-seq-len', type=int, default=50)
    parser.add_argument('--hidden-size', type=int, default=64)
    parser.add_argument('--num-layers', type=int, default=2)
    parser.add_argument('--num-heads', type=int, default=2)
    args = parser.parse_args()
    main(args)
