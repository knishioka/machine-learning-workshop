# Ollama Fine-tuning ガイド

このディレクトリには、Ollamaを使用してカスタムモデルをfine-tuningするためのサンプルコードとデータが含まれています。

## 📋 概要

Ollamaは、ローカル環境で大規模言語モデル（LLM）を実行できるツールです。このガイドでは、カスタマーサポート用チャットボットを例に、独自のデータでモデルをカスタマイズする方法を説明します。

### このリポジトリに含まれるもの

- `training_data.jsonl` - カスタマーサポート用の訓練データ
- `fine_tune.py` - Fine-tuning実行スクリプト
- `customer-support.modelfile` - カスタムモデル定義ファイル

## 🚀 クイックスタート

### 前提条件

1. **Ollamaのインストール**
   ```bash
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **ベースモデルのダウンロード**
   ```bash
   ollama pull llama3.2:1b
   ```

3. **Python環境の準備**
   ```bash
   python --version  # Python 3.8以上が必要
   ```

### Fine-tuningの実行

1. **基本的な実行方法**
   ```bash
   cd ollama/fine_tuning
   python fine_tune.py --test
   ```

2. **カスタムパラメータでの実行**
   ```bash
   python fine_tune.py \
     --data training_data.jsonl \
     --base-model llama3.2:1b \
     --model-name my-support-bot \
     --test
   ```

## 📊 訓練データの形式

訓練データは[JSONL形式](https://jsonlines.org/)で準備します。各行が1つの訓練サンプルです：

```json
{
  "instruction": "質問や指示",
  "input": "追加の入力情報（オプション）",
  "output": "期待される応答"
}
```

### データ例

```json
{"instruction": "製品の返品について教えてください", "input": "", "output": "返品は購入後30日以内であれば承っております..."}
{"instruction": "商品の在庫状況を教えてください", "input": "商品番号: ABC-123", "output": "商品番号ABC-123について確認いたします..."}
```

## 🛠️ Modelfileの構造

`Modelfile`は、Ollamaでカスタムモデルを定義するための設定ファイルです：

```dockerfile
FROM llama3.2:1b              # ベースモデル

SYSTEM """                    # システムプロンプト
あなたは親切なアシスタントです。
"""

PARAMETER temperature 0.7     # 生成パラメータ
PARAMETER top_p 0.9

MESSAGE user 質問例          # Few-shot学習用の例
MESSAGE assistant 回答例
```

## 📝 使用方法

### 1. 訓練データの準備

独自のデータを準備する場合は、以下の形式でJSONLファイルを作成します：

```python
import json

data = [
    {
        "instruction": "あなたの質問",
        "input": "",  # オプション
        "output": "期待される回答"
    }
]

with open('my_data.jsonl', 'w', encoding='utf-8') as f:
    for item in data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
```

### 2. Fine-tuningスクリプトの実行

```bash
python fine_tune.py --data my_data.jsonl --model-name my-model
```

### 3. カスタムモデルの使用

Fine-tuning完了後、以下のコマンドでモデルを使用できます：

```bash
# 対話モード
ollama run customer-support

# 単一の質問
ollama run customer-support "配送について教えてください"
```

### 4. モデルの管理

```bash
# モデル一覧の確認
ollama list

# モデルの削除
ollama rm customer-support

# モデルの情報確認
ollama show customer-support
```

## 🔧 高度な設定

### パラメータの調整

`fine_tune.py`では以下のパラメータを調整できます：

- `--base-model`: ベースとなるモデル（llama3.2:1b, mistral:7b など）
- `--temperature`: 生成の多様性（0.0-1.0）
- `--top_p`: トークン選択の閾値（0.0-1.0）

### 複数のモデルバリエーション

異なる用途向けに複数のモデルを作成できます：

```bash
# 技術サポート用
python fine_tune.py --data tech_support.jsonl --model-name tech-support

# 営業用
python fine_tune.py --data sales.jsonl --model-name sales-assistant
```

## 🎯 ベストプラクティス

1. **データ品質の確保**
   - 一貫性のある形式で回答を作成
   - スペルミスや文法エラーを避ける
   - 多様な質問パターンを含める

2. **適切なデータ量**
   - 最低でも50-100個のサンプルを用意
   - 特定のドメインに特化する場合は200-500個推奨

3. **モデル選択**
   - 軽量タスク: llama3.2:1b
   - 汎用タスク: llama3.2:3b
   - 高品質応答: mistral:7b

4. **テストと評価**
   - 必ず`--test`フラグでモデルをテスト
   - 実際のユースケースで検証
   - 必要に応じてデータを追加・修正

## 🐛 トラブルシューティング

### よくある問題と解決方法

1. **「ollama: command not found」エラー**
   ```bash
   # Ollamaが正しくインストールされているか確認
   which ollama
   
   # PATHに追加されているか確認
   echo $PATH
   ```

2. **メモリ不足エラー**
   - より小さいモデル（1b, 3b）を使用
   - バッチサイズを調整
   
3. **モデル作成の失敗**
   - Modelfileの構文を確認
   - ベースモデルがダウンロード済みか確認
   
## 📚 参考資料

- [Ollama公式ドキュメント](https://ollama.ai/docs)
- [Modelfile仕様](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)
- [サポートされているモデル一覧](https://ollama.ai/library)

## 💡 次のステップ

1. **より大きなデータセットの準備**
   - 実際の顧客対応ログからデータを抽出
   - ChatGPTやClaudeを使ってデータを生成

2. **評価メトリクスの実装**
   - 応答の品質評価
   - ユーザーフィードバックの収集

3. **プロダクション環境への展開**
   - APIサーバーの構築
   - 負荷分散の実装
   - モニタリングの設定

## 🤝 貢献

問題を見つけた場合や改善提案がある場合は、Issueを作成してください。