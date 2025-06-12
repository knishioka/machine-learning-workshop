# 📁 Fine-tuningディレクトリ構成

## ディレクトリ構造

```
fine_tuning/
├── README.md                    # メインガイド（Ollamaカスタマイゼーション＆真のfine-tuning）
├── STRUCTURE.md                 # このファイル（ディレクトリ構成説明）
│
├── docs/                        # ドキュメント
│   ├── colab_quick_start.md    # Google Colabクイックスタートガイド
│   └── mac_fine_tuning_guide.md # Mac向けfine-tuningガイド
│
├── scripts/                     # 実行スクリプト
│   ├── fine_tune.py            # Ollamaモデルカスタマイゼーション（プロンプトエンジニアリング）
│   ├── true_fine_tuning_demo.py # 真のfine-tuningデモ（Unsloth使用）
│   ├── mac_local_fine_tuning.py # Mac用ローカルfine-tuningスクリプト
│   └── setup_mac_env.sh        # Mac環境セットアップスクリプト
│
├── notebooks/                   # Jupyterノートブック
│   └── minimal_colab_fine_tuning.ipynb # Google Colab用fine-tuningノートブック
│
└── examples/                    # サンプルデータ
    ├── training_data.jsonl      # カスタマーサポート用サンプルデータ
    └── customer-support.modelfile # Ollama用Modelfileサンプル
```

## 🎯 各ファイルの用途

### 📚 ドキュメント

- **README.md**: 
  - Ollamaのプロンプトエンジニアリングと真のfine-tuningの違いを説明
  - 実行結果の比較を含む
  
- **docs/colab_quick_start.md**: 
  - 最速でfine-tuningを試すための5ステップガイド
  - 約20分で完了
  
- **docs/mac_fine_tuning_guide.md**: 
  - Mac（特にApple Silicon）でのfine-tuning方法
  - 制限事項と代替案

### 🛠️ スクリプト

- **scripts/fine_tune.py**: 
  - Ollamaのプロンプトエンジニアリング実装
  - Modelfile生成とモデル作成を自動化
  
- **scripts/true_fine_tuning_demo.py**: 
  - Unslothを使った真のfine-tuning
  - GGUF形式での出力方法を含む

### 📓 ノートブック

- **notebooks/minimal_colab_fine_tuning.ipynb**: 
  - Google Colabで実行可能な完全なノートブック
  - TinyLlama使用で最小構成

### 📋 サンプル

- **examples/training_data.jsonl**: 
  - カスタマーサポート向けのサンプルデータ
  - プロンプトエンジニアリング用
  
- **examples/customer-support.modelfile**: 
  - OllamaのModelfileサンプル
  - カスタマイゼーション例

## 🚀 使い方

### 1. Ollamaでプロンプトエンジニアリング
```bash
cd scripts
python fine_tune.py --data ../examples/training_data.jsonl --test
```

### 2. Google Colabで真のfine-tuning
1. `notebooks/minimal_colab_fine_tuning.ipynb`をColabで開く
2. GPUランタイムを選択
3. 全セルを実行

### 3. Macでのローカルfine-tuning
`docs/mac_fine_tuning_guide.md`を参照

## 📝 備考

- プロンプトエンジニアリング: GPU不要、即座に実行可能
- 真のfine-tuning: GPU必要、新しい知識の学習が可能
- 用途に応じて適切な方法を選択してください