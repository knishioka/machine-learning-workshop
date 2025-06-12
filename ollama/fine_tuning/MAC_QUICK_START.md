# 🍎 Mac Local Fine-tuning クイックスタート

## ⚠️ 現在の問題と解決策

### Python 3.13 互換性問題
現在、Python 3.13でMLXのインストールに問題があります。以下の代替方法をお試しください：

## 方法1: PyTorchを使用（推奨）

```bash
# スクリプトを実行（PyTorchモード）
python scripts/mac_local_fine_tuning.py --method pytorch
```

## 方法2: 正しいMLXコマンド

もしMLXがインストール済みの場合、以下のコマンドで実行できます：

```bash
# データ準備
python scripts/mac_local_fine_tuning.py --method mlx

# または手動で実行
python -m mlx_lm.lora \
    --model mlx-community/Llama-3.2-1B-4bit \
    --train \
    --data ./finetuned_model/training_data.jsonl \
    --adapter-path ./finetuned_model \
    --iters 100 \
    --batch-size 1 \
    --learning-rate 1e-4
```

## 方法3: Python 3.12環境を使用

```bash
# pyenvを使用してPython 3.12をインストール
pyenv install 3.12.0
pyenv local 3.12.0

# 仮想環境を作成
python -m venv venv_312
source venv_312/bin/activate

# MLXをインストール
pip install mlx mlx-lm

# Fine-tuning実行
python scripts/mac_local_fine_tuning.py --method mlx
```

## 方法4: Google Colabを使用（最も簡単）

ローカル環境での問題を避けたい場合：

```bash
# ノートブックを開く
open notebooks/minimal_colab_fine_tuning.ipynb
```

Google Colabにアップロードして実行（約20分）

## トラブルシューティング

### エラー: `unrecognized arguments: --lora-rank`
→ このエラーは修正済みです。最新のスクリプトを使用してください。

### エラー: `No module named 'mlx_lm'`
→ Python 3.13の互換性問題です。PyTorchモードを使用するか、Python 3.12環境を使用してください。

### メモリ不足
→ より小さいバッチサイズまたはモデルを使用：
```bash
python scripts/mac_local_fine_tuning.py --method pytorch --model TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

## 推奨手順

1. **まずPyTorchで試す**（最も安定）
2. **問題があればGoogle Colabを使用**（最も簡単）
3. **MLXを使いたい場合はPython 3.12環境を構築**（パフォーマンス最適）

## サポート

問題が続く場合は、以下を確認してください：
- macOSバージョン（12.0以上推奨）
- Pythonバージョン（3.12推奨）
- メモリ容量（16GB以上推奨）