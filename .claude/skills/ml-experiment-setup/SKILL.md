---
name: ml-experiment-setup
description: 機械学習実験のセットアップを支援。新しい実験用Jupyterノートブック、実験トラッキング設定、データローディングコードなどを生成します。
---

# ML Experiment Setup

このスキルは、機械学習実験を開始する際のボイラープレートコードとセットアップを自動生成します。

## When to Use

以下のような場合にこのスキルを使用してください：
- 新しい機械学習実験を開始する
- 実験トラッキング（MLflow、Weights & Biasesなど）のセットアップが必要
- データローディングとEDAのテンプレートが欲しい
- 実験結果を記録するための構造化されたノートブックが必要

## Instructions

### 1. 実験の目的を確認
ユーザーに以下を質問してください：
- 実験の目的は何ですか？（分類、回帰、クラスタリングなど）
- 使用するデータセットの種類は？（CSV、画像、テキストなど）
- 実験トラッキングツールは使いますか？（MLflow、W&B、TensorBoardなど）
- 使用予定のフレームワークは？（PyTorch、TensorFlow、scikit-learnなど）

### 2. ノートブック構造の生成
以下のセクションを含むJupyterノートブックを作成：

```python
# 1. Environment Setup
# 2. Data Loading
# 3. Exploratory Data Analysis (EDA)
# 4. Data Preprocessing
# 5. Model Definition
# 6. Training
# 7. Evaluation
# 8. Results Visualization
# 9. Experiment Logging
```

### 3. 必須コンポーネント

#### データローディング
```python
import pandas as pd
import numpy as np
from pathlib import Path

# データパスの設定
DATA_DIR = Path("data")
RAW_DATA = DATA_DIR / "raw"
PROCESSED_DATA = DATA_DIR / "processed"

# データの読み込み
def load_data(filepath):
    """データを読み込む"""
    return pd.read_csv(filepath)
```

#### 実験トラッキング（MLflow使用時）
```python
import mlflow
import mlflow.sklearn  # または mlflow.pytorch, mlflow.tensorflow

# 実験名の設定
EXPERIMENT_NAME = "your_experiment_name"
mlflow.set_experiment(EXPERIMENT_NAME)

# 実験の開始
with mlflow.start_run(run_name="baseline"):
    # パラメータのログ
    mlflow.log_param("param_name", param_value)

    # メトリクスのログ
    mlflow.log_metric("metric_name", metric_value)

    # モデルの保存
    mlflow.sklearn.log_model(model, "model")
```

#### 再現性の確保
```python
import random
import torch

# シード値の設定
SEED = 42

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)
```

### 4. ベストプラクティス

- **明確なセクション分け**: マークダウンセルで各セクションを明確に分ける
- **再現性**: すべての乱数シードを設定
- **ドキュメント**: 各セクションに説明コメントを追加
- **バージョニング**: 実験日時、パラメータ、結果を記録
- **モジュール化**: 再利用可能な関数を作成

### 5. ファイル構造の提案

ユーザーのプロジェクトに以下の構造を提案：

```
experiment_name/
├── notebook.ipynb          # メインの実験ノートブック
├── requirements.txt        # 必要なパッケージ
├── config.yaml            # 実験設定（オプション）
├── src/
│   ├── data.py           # データローディング関数
│   ├── models.py         # モデル定義
│   └── utils.py          # ユーティリティ関数
└── outputs/
    ├── models/           # 保存されたモデル
    └── figures/          # 生成された図
```

## Examples

### Example 1: 画像分類実験のセットアップ

ユーザー: "画像分類の実験を始めたい"

応答:
1. PyTorchまたはTensorFlowを使用するか確認
2. 画像データのパス、クラス数を確認
3. データローダー、前処理パイプライン、CNNモデルのテンプレートを生成
4. 学習ループ、評価、可視化コードを含むノートブックを作成

### Example 2: MLflowを使った回帰実験

ユーザー: "MLflowを使って回帰モデルの実験管理をしたい"

応答:
1. データの特性を確認（特徴量数、サンプル数など）
2. MLflow設定コードを生成
3. 複数モデル（線形回帰、決定木、ランダムフォレストなど）の比較コードを作成
4. 各モデルのパラメータとメトリクスをMLflowに記録するコードを追加

## Notes

- プロジェクトの既存の構造を尊重する
- 不要なライブラリのインポートを避ける
- ユーザーの経験レベルに応じてコメントの詳細度を調整
- 実験結果は必ずバージョン管理する
