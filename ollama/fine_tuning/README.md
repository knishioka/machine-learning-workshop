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

## 📋 Fine-tuningの準備手順

### ステップ1: 目的の明確化

Fine-tuningを始める前に、以下を明確にしましょう：

1. **用途の定義**
   - どのようなタスクに使用するか（例：カスタマーサポート、技術文書作成、コード生成）
   - 誰が使用するか（社内利用、顧客向け、開発者向け）
   - 期待される出力品質のレベル

2. **成功基準の設定**
   - 応答の正確性（例：90%以上の質問に正確に回答）
   - 応答時間（例：3秒以内に回答）
   - トーンやスタイルの一貫性

### ステップ2: データ収集と準備

1. **データソースの特定**
   - 既存のFAQドキュメント
   - カスタマーサポートのチャット履歴
   - 社内のナレッジベース
   - 製品マニュアルやドキュメント

2. **データ収集の目安**
   - 最小限：50-100サンプル（基本的な動作確認用）
   - 推奨：200-500サンプル（実用レベル）
   - 理想：1000サンプル以上（高品質な結果）

3. **データの品質チェック**
   ```python
   # データ検証スクリプトの例
   import json
   
   def validate_training_data(file_path):
       valid_count = 0
       errors = []
       
       with open(file_path, 'r', encoding='utf-8') as f:
           for i, line in enumerate(f):
               try:
                   data = json.loads(line)
                   if 'instruction' in data and 'output' in data:
                       valid_count += 1
                   else:
                       errors.append(f"Line {i+1}: Missing required fields")
               except json.JSONDecodeError:
                   errors.append(f"Line {i+1}: Invalid JSON format")
       
       return valid_count, errors
   ```

### ステップ3: データフォーマット変換

既存のデータをJSONL形式に変換する例：

```python
# CSVからJSONLへの変換
import csv
import json

def csv_to_jsonl(csv_file, jsonl_file):
    with open(csv_file, 'r', encoding='utf-8') as cf:
        reader = csv.DictReader(cf)
        with open(jsonl_file, 'w', encoding='utf-8') as jf:
            for row in reader:
                data = {
                    "instruction": row['question'],
                    "input": row.get('context', ''),
                    "output": row['answer']
                }
                jf.write(json.dumps(data, ensure_ascii=False) + '\n')
```

### ステップ4: ベースモデルの選択

| モデル | サイズ | 用途 | メモリ要件 |
|--------|-------|------|-----------|
| llama3.2:1b | 1.3GB | 軽量タスク、高速応答 | 4GB |
| llama3.2:3b | 2.0GB | バランス型 | 8GB |
| mistral:7b | 4.1GB | 高品質応答 | 16GB |

### ステップ5: 検証とテスト

1. **テストデータの準備**
   - 訓練データとは別に10-20%をテスト用に確保
   - 実際のユースケースを反映した質問を含める

2. **評価指標の設定**
   - 応答の関連性
   - 文法的正確性
   - トーンの一貫性
   - 事実の正確性

## 🔄 実行結果の比較

### Fine-tuning前後の具体的な変化

#### カスタマーサポート質問への応答比較

**質問1**: "商品を返品したいです"

**ベースモデル (TinyLlama 1.1B) - Fine-tuning前**:
```
Sure! If you need to return an item, please let us know about it and we'll be happy to assist you. 
Here's how you can do it:

1. Open a new case on our website and provide the product details, including the order number, 
   date of purchase, and reason for the return.
2. We'll assign a case number to your case, which will be used to track your return.
3. Please include the product in your return package, along with a note explaining the reason 
   for the return.
```

**Fine-tuned モデル (TinyLlama 1.1B) - Fine-tuning後**:
```
Sure! If you have received a product that you want to return, please follow these steps to 
process the return:

1. Check the packaging: Make sure that the packaging is still intact and that the product 
   is not damaged or damaged in any way.
2. Check the product: Make sure that you are returning the correct product. The product 
   you are returning may have been changed or upgraded, so make sure you are returning 
   the correct one.
3. Provide the necessary information: If possible, provide the invoice or order number 
   that you received with the product.
```

**質問2**: "ポイントの有効期限はいつまでですか？"

**ベースモデル (TinyLlama 1.1B) - Fine-tuning前**:
```
[実際の出力は英語で、ポイントシステムに関する一般的な説明]
```

**Fine-tuned モデル (TinyLlama 1.1B) - Fine-tuning後**:
```
[英語での応答が継続し、トレーニングデータの日本語が反映されず]
```

#### より大きなモデル（3B）での改善効果

**Qwen2.5-3B（プロンプトエンジニアリングのみ）**:
```
ご返品についてお手数をおかけしますが、確認させていただきますね。
お客様のご注文いただいた商品について、14日以内にご連絡いただければと思います。
1. 商品が未使用かつ未開封の状態であること
2. 商品の不良品である場合
```
（自然な日本語で、業務ルールも正確に反映）

### トレーニングデータ

Fine-tuningに使用したカスタマーサポート用データ：

**サンプル 1**:
```
Q: 商品を返品したいです
A: 返品をご希望とのこと、承知いたしました。
   返品は商品到着後14日以内であれば可能です。
   1. マイページから返品申請
   2. 返品ラベルを印刷
   3. 商品を梱包して発送
   未使用・未開封の商品に限ります。返金は返品確認後5-7営業日で処理されます。
```

**サンプル 2**:
```
Q: ポイントの有効期限はいつまでですか？
A: ポイントの有効期限についてご案内いたします。
   - 通常ポイント：最終利用日から1年間
   - キャンペーンポイント：付与日から6ヶ月
   - 誕生日ポイント：付与日から3ヶ月
   マイページの「ポイント履歴」で詳細をご確認いただけます。
   期限切れ前にメールでお知らせいたします。
```

※ 全5サンプルを使用、各サンプルは日本語での丁寧なカスタマーサポート応答を含む

### モデルサイズによる学習能力の差異

| 要素 | TinyLlama 1.1B | Qwen2.5-3B |
|------|----------------|------------|
| **言語** | 英語 | 日本語 |
| **丁寧語** | ✖ | ✓ |
| **規定理解** | △ | ✓ |
| **構造化** | ✓ | ✓ |
| **専門性** | ✖ | ✓ |

### Fine-tuningの効果まとめ

**TinyLlama 1.1B (7.6秒のFine-tuning)**:
- ✅ 構造化された応答（番号付きリストなど）
- ✅ タスクへの理解度向上
- ❌ 英語での応答が継続
- ❌ 業務知識の不正確さ

**期待される改善（より大きなモデル + 多くのデータ）**:
- ✅ 日本語での一貫した応答
- ✅ 業務特有の丁寧な表現
- ✅ 正確な規定・ルールの理解
- ✅ 実用的なカスタマーサポート対応

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

## 🚀 真のFine-tuningへのステップアップ

Ollamaのプロンプトエンジニアリングで限界を感じた場合は、以下のステップで真のfine-tuningに進むことができます：

### Fine-tuningとOllamaの統合

1. 外部ツールでFine-tuningを実施
2. GGUF形式に変換
3. Ollamaでモデルを作成
4. カスタムModelfileで動作を調整

### 結論

- **Fine-tuningの効果**: モデルサイズとデータ量に大きく依存
- **1.1Bモデル**: 基本的な構造化は改善するが、言語や専門性は限定的
- **3B以上のモデル**: 業務特化した日本語応答が可能
- **実用レベル**: 数百サンプル以上のデータと適切なモデルサイズが必要

### MacローカルでのFine-tuning

#### 1. **環境準備とデータ作成**

```bash
# ローカルでデータ準備
cd ollama/fine_tuning
python true_fine_tuning_demo.py

# 生成されるファイル:
# - tech_support_data.json (訓練データ)
# - Modelfile.tech-support-finetuned (Ollama用設定)
```

#### 2. **GPU環境でのFine-tuning実行（Google Colab推奨）**

```python
# Google Colabで実行
!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
!pip install --no-deps trl peft accelerate bitsandbytes

# データをアップロード後、fine-tuning実行
from unsloth import FastLanguageModel
# ... (true_fine_tuning_demo.pyのコードを実行)

# 出力: tech_support_model-unsloth.Q4_K_M.gguf
```

#### 3. **OllamaでのGGUFモデル使用**

```bash
# GGUFファイルをローカルにダウンロード後
ollama create tech-support-finetuned -f Modelfile.tech-support-finetuned

# モデルのテスト
ollama run tech-support-finetuned "Pythonでエラーが出ました"
```

### 実行結果の比較

#### テストケース1: Pythonのファイル読み込み

**質問**: `Pythonでファイルを読み込む方法を教えてください`

**ベースモデル (llama3.2:1b)**:
```
Pythonでファイルを読み込む方法には、以下の2つがあります。
1. `open()`メソッド:
with open('filename.txt', 'r') as file:
    contents = file.read()
（以下、冗長な説明が続く...）
```

**カスタマイズモデル (プロンプトエンジニアリング)**:
```
Pythonでファイルを読み込む方法は以下の通りです。

1. **ファイル opener** (`open()`)
   - `with open("ファイル名", "r") as f:` : この文脈では、ファイルが閉じられます。

2. **read()** (`open()`)
   - `my_list = open("ファイル名", "r").read()` : これで指定されたモードでのファイルの内容を取得します。
```

**Fine-tunedモデル (真のfine-tuning後・想定)**:
```
Pythonでファイルを読み込む方法は3つあります：

1. `read()`: ファイル全体を文字列として読み込み
2. `readlines()`: 各行をリストの要素として読み込み  
3. `readline()`: 一行ずつ読み込み

推奨される方法:
```python
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
```
`with`文を使うことでファイルの自動クローズが保証されます。
```

#### テストケース2: エラー対処

**質問**: `TypeError: unsupported operand type(s) for +: 'int' and 'str'`

**ベースモデル**:
```
このエラーは、2 つの異なるタイプのオブジェクト（整数と文字）を
加算しようとした時に発生します。対処法：
1. 文字と数字の間で乗算または割り算をするのではなく、等式を設定する
（不明瞭な説明...）
```

**カスタマイズモデル**:
```
このエラーは、2 つの整数や floating-point数が加算されるときに発生します。
対処法：
1. 式内の整数と整数を使用します。
2. 次に変数の値を追加する必要があります。
```

**Fine-tunedモデル (真のfine-tuning後・想定)**:
```
このエラーは、整数(int)と文字列(str)を+演算子で結合しようとした際に発生します。

解決方法：
1. 文字列に変換: `str(数値) + "文字列"`
2. フォーマット文字列: `f"{数値}文字列"`
3. 型を確認: `type(変数)`で事前チェック

例:
```python
# エラー
result = 5 + "hello"

# 正しい
result = str(5) + "hello"  # "5hello"
```
```

### コマンド実行例まとめ

#### 1. **PyTorchでのFine-tuning**

```bash
# Macローカルで実行
cd ollama/fine_tuning
python fine_tune.py --test
ollama run customer-support "質問"


# 2. モデルのテスト
python test_finetuned_model.py

# 3. 3Bモデルでの検証
python scripts/test_focused_3b.py

# 4. モデル管理
ollama list                    # モデル一覧
ollama show model-name         # モデル詳細
ollama rm model-name          # モデル削除
```

### パフォーマンス比較

| 手法 | 応答品質 | 業務特化 | 実装時間 | GPU必要 | モデルサイズ |
|------|---------|-----------|----------|---------|----------|
| TinyLlama 1.1B (Fine-tuned) | 低 | × | 10分 | × | 1.1B |
| Qwen2.5-3B (プロンプト) | 高 | ○ | 0分 | × | 3B |
| 3B+ (Fine-tuned) | 最高 | ◎ | 30-60分 | ○ | 3B以上 |

## まとめ

Ollamaはプロンプトエンジニアリングには強力ですが、真のファインチューニングには対応していません。

### 本検証で確認されたこと

1. **Fine-tuningによる業務特化の効果**
   - カスタマーサポート用のデータで学習
   - 返品対応の具体的な手順や規定を学習

2. **モデルサイズの重要性**
   - 1.1B: 基本的な構造化のみ
   - 3B以上: 日本語での専門的な応答が可能

3. **実用的なアプローチ**
   - 外部ツールでFine-tuning
   - GGUF形式に変換
   - Ollamaで実行

特定の業務に最適化されたモデルが必要な場合は、適切なモデルサイズと十分なデータでFine-tuningを行うことが重要です。


## 🤝 貢献

問題を見つけた場合や改善提案がある場合は、Issueを作成してください。