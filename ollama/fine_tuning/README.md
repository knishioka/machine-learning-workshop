# Ollamaで使用するためのFine-tuningガイド

> **重要**: Ollama自体はFine-tuning機能を提供していません。このガイドでは、外部ツールでFine-tuningを行い、その結果をOllamaで使用する方法を説明します。

## 📋 概要

### なぜOllamaでFine-tuningができないのか？

Ollamaは以下の理由でFine-tuningをサポートしていません：

1. **設計思想**: Ollamaは「モデルの実行」に特化したツールで、訓練機能は含まれていません
2. **リソース制約**: Fine-tuningには大量のGPUメモリと計算リソースが必要ですが、Ollamaはローカル実行を前提としています
3. **技術的制限**: OllamaはGGUF形式のモデルを使用しますが、Fine-tuningは通常PyTorchやTensorFlow形式で行われます

### Ollamaでできること・できないこと

**✅ できること (プロンプトエンジニアリング)**:
- Modelfileを使用したシステムプロンプトのカスタマイズ
- Few-shot学習の例を追加
- パラメータ（temperature、top_pなど）の調整
- 既存モデルの動作をある程度カスタマイズ

**❌ できないこと (真のFine-tuning)**:
- モデルの重みの更新
- 新しい知識の学習
- ドメイン特化型の深い学習

### このガイドのアプローチ

本ガイドでは、以下の2段階アプローチを採用しています：

1. **外部ツールでFine-tuning**: PyTorch、Hugging Face、Unslothなどを使用
2. **Ollamaで実行**: Fine-tuningしたモデルをGGUF形式に変換してOllamaで使用

### このリポジトリに含まれるもの

**メインスクリプト（検証済み）**:
- `scripts/tinyllama_fine_tuning.py` - TinyLlama-1.1B用（40秒で完了）
- `scripts/gemma_fine_tuning.py` - Gemma3-1B用（27秒で完了）
- `scripts/qwen_fine_tuning.py` - Qwen2.5-3B用（62秒で完了）
- `verify_tinyllama_finetuning.py` - Fine-tuning効果の検証スクリプト

**変換・テストツール**:
- `merge_qwen_model.py` - LoRAアダプターのマージ
- `scripts/test_gemma_model.py` - Gemmaモデルのテスト
- `scripts/test_qwen_model.py` - Qwenモデルのテスト

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

### 実際のワークフロー

#### 方法1: Fine-tuning効果の検証（推奨）

```bash
# 1. TinyLlamaでFine-tuning（最速：40秒）
python scripts/tinyllama_fine_tuning.py

# 2. 効果を検証
python verify_tinyllama_finetuning.py
```

#### 方法2: より大きなモデルでのFine-tuning

**Gemma3-1B**:
```bash
# 1. Fine-tuning実行（27秒）
python scripts/gemma_fine_tuning.py

# 2. テスト
python scripts/test_gemma_model.py
```

**Qwen2.5-3B（完全なワークフロー）**:
```bash
# 1. Fine-tuning実行（62秒）
python scripts/qwen_fine_tuning.py

# 2. LoRAアダプターをマージ
python merge_qwen_model.py

# 3. GGUF形式に変換
python convert-hf-to-gguf.py merged_qwen2.5_model \
  --outfile qwen-cs-f16.gguf --outtype f16

# 4. 量子化
llama-quantize qwen-cs-f16.gguf qwen-cs.gguf Q4_K_M

# 5. Ollamaで使用
ollama create qwen-cs -f Modelfile
ollama run qwen-cs "What are the shipping costs?"
```

## 📊 訓練データの形式

各モデルに応じた会話形式で準備します：

**TinyLlama形式**:
```
<|system|>
You are a helpful customer support assistant.</s>
<|user|>
What are the shipping costs?</s>
<|assistant|>
Here are our shipping options and costs:

**Standard Shipping:**
- $6.99 flat rate
- FREE on orders over $50
- 3-5 business days</s>
```

**Gemma3形式**:
```
<start_of_turn>user
I want to return a product<end_of_turn>
<start_of_turn>model
I'll be happy to help you with your return...<end_of_turn>
```

**Qwen2.5形式**:
```
<|im_start|>system
You are a helpful customer support assistant.<|im_end|>
<|im_start|>user
How do I track my order?<|im_end|>
<|im_start|>assistant
To track your order, please...<|im_end|>
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

## 🔄 Fine-tuning検証結果

### 実証されたFine-tuningの効果と限界（2025年1月）

#### TinyLlama 1.1B検証結果

**訓練条件**:
- データ: 10サンプル（英語カスタマーサポート）
- エポック: 3
- 訓練時間: 40秒
- LoRAパラメータ: r=16, alpha=32

**質問**: "What are the shipping costs?"

**ベースモデル（Fine-tuning前）**:
```
I do not have access to the specific shipping rates of the retailer's website. 
However, in general, shipping costs may vary depending on the retailer, product, 
and shipping location. You can check the...
```

**Fine-tunedモデル（Fine-tuning後）**:
```
There isn't a specific shipping charge for purchasing a product on the website. 
However, shipping costs vary depending on your location, the quantity of the order, 
and the shipping method you choose...
```

**訓練データの期待される応答**:
```
Here are our shipping options and costs:

**Standard Shipping:**
- $6.99 flat rate
- FREE on orders over $50
- 3-5 business days

**Express Shipping:**
- $14.99 flat rate
- 1-2 business days
```

### 観察された問題点

1. **具体的な情報の欠如**:
   - 訓練データには具体的な価格（$6.99、$14.99）が含まれていたが、モデルは学習できず
   - 一般的で曖昧な回答が継続

2. **構造の部分的な改善**:
   - 回答の構造はわずかに改善
   - しかし、訓練データの箇条書き形式は再現されず

3. **ドメイン知識の不足**:
   - 14日間返品ポリシーなどの具体的なルールが学習されない
   - Shopify.comなど訓練データに含まれない情報が出現

### モデルサイズとデータ量の影響

| 要素 | TinyLlama 1.1B (10サンプル) | 期待される改善 (3B+, 100+サンプル) |
|------|------------------------------|-----------------------------------|
| **具体的な価格情報** | ❌ | ✅ |
| **構造化された応答** | △ | ✅ |
| **ドメイン固有知識** | ❌ | ✅ |
| **一貫性** | △ | ✅ |

### Fine-tuningの難しさの実証

1. **最小限のデータでは不十分**:
   - 10サンプル、3エポックでは、モデルの動作に大きな変化なし
   - LoRAアダプターは作成されたが、実質的な効果は限定的

2. **スケーリングの必要性**:
   - より大きなモデル（3B以上）
   - より多くのデータ（100サンプル以上）
   - より長い訓練時間

3. **トレードオフ**:
   - 効果的なFine-tuning: 大規模リソースが必要
   - 簡易的なFine-tuning: 効果が限定的

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

### 実測パフォーマンス比較（2025年1月）

| モデル | 訓練時間 | Loss | 効果 | 実用性 |
|--------|----------|------|------|--------|
| **TinyLlama 1.1B** | 40秒 | 1.7 | 限定的 | 検証用 |
| **Gemma3-1B** | 27秒 | 4.4 | 低 | 実験用 |
| **Qwen2.5-3B** | 62秒 | 2.55 | 中 | 実用可能 |

### Fine-tuning効果の実態

| 期待される効果 | 実際の結果（少量データ） | 必要な条件 |
|---------------|------------------------|----------|
| 具体的な価格情報の学習 | ❌ 一般的な回答のまま | 100+サンプル |
| 構造化された応答 | △ わずかに改善 | 多様なフォーマット例 |
| ドメイン固有知識 | ❌ ほぼ学習されず | 大規模データセット |
| トーンの一貫性 | △ 部分的に改善 | 一貫した訓練データ |

## まとめ

### Fine-tuningの現実と推奨事項

#### 検証で明らかになったこと

1. **少量データでのFine-tuningの限界**:
   - 10サンプル、3エポックでは実質的な効果なし
   - LoRAで効率的に訓練してもドメイン知識は学習されず
   - 具体的な情報（価格、ポリシー）の再現は困難

2. **必要なリソース**:
   - **データ**: 最低100サンプル、理想的には1000+
   - **モデル**: 3B以上のパラメータ
   - **時間**: 実用レベルには数時間の訓練が必要

3. **現実的なアプローチ**:
   - **検証段階**: プロンプトエンジニアリングで素早くテスト
   - **プロトタイプ**: 小規模Fine-tuningで可能性を探る
   - **本番環境**: 十分なリソースで本格的なFine-tuning

### 推奨ワークフロー

1. **初期検証** (数分):
   ```bash
   # プロンプトエンジニアリングで基本動作確認
   ollama run llama3.2 "Act as customer support..."
   ```

2. **Fine-tuning実験** (1時間以内):
   ```bash
   # TinyLlamaで高速検証
   python scripts/tinyllama_fine_tuning.py
   python verify_tinyllama_finetuning.py
   ```

3. **本格実装** (要GPU環境):
   - 大規模データセット準備
   - 7B以上のモデル使用
   - 専用GPU環境での訓練

### 結論

Fine-tuningは強力な手法ですが、効果を得るには相応のリソースが必要です。多くの場合、まずはプロンプトエンジニアリングから始め、必要に応じてFine-tuningに移行することが現実的です。


## 🧪 最新の検証結果（2025年1月更新）

### 英語カスタマーサポートFine-tuningの実行結果

#### 実行環境
- **OS**: macOS (Apple Silicon)
- **Python**: 3.x
- **Device**: MPS (Metal Performance Shaders)
- **実行日**: 2025年1月

#### Fine-tuning実行結果

**1. Gemma3-1B-IT**
```
使用デバイス: mps
モデル google/gemma-3-1b-it を読み込み中...
trainable params: 753,664 || all params: 1,097,442,816 || trainable%: 0.0687

ファインチューニングを開始します...
{'loss': 4.4, 'grad_norm': 2.5391159057617188, 'learning_rate': 0.0002, 'epoch': 1.0}

訓練時間: 0:00:27.077848
モデルは ./finetuned_gemma3_model に保存されました
```

**2. Qwen2.5-3B-Instruct**
```
使用デバイス: mps
モデル Qwen/Qwen2.5-3B-Instruct を読み込み中...
trainable params: 3,145,728 || all params: 3,362,430,720 || trainable%: 0.0936

ファインチューニングを開始します...
{'loss': 2.55, 'grad_norm': 0.6542252898216248, 'learning_rate': 0.0002, 'epoch': 1.0}

訓練時間: 0:01:02.159329
モデルは ./finetuned_qwen2.5_model に保存されました
```

#### GGUF変換プロセス（Qwenモデル）

**1. LoRAアダプターのマージ**
```bash
python merge_qwen_model.py
# 出力: merged_qwen2.5_model/
```

**2. GGUF形式への変換**
```bash
python convert-hf-to-gguf.py merged_qwen2.5_model \
  --outfile qwen-customer-support-f16.gguf \
  --outtype f16
# 出力: qwen-customer-support-f16.gguf (約6GB)
```

**3. 量子化（Q4_K_M形式）**
```bash
llama-quantize qwen-customer-support-f16.gguf \
  qwen-customer-support.gguf Q4_K_M
# 出力: qwen-customer-support.gguf (1.8GB)
```

**4. Ollamaモデルの作成**
```bash
ollama create qwen-cs -f finetuned_qwen2.5_model/Modelfile
# 結果: success
```

### 使用した訓練データ

10種類の英語カスタマーサポートシナリオ：
1. Order tracking（注文追跡）
2. Product returns（返品）
3. Payment method changes（支払い方法変更）
4. Size exchanges（サイズ交換）
5. Points expiration（ポイント有効期限）
6. Shipping costs（送料）
7. Coupon usage（クーポン使用）
8. Membership benefits（会員特典）
9. Order cancellation（注文キャンセル）
10. Stock availability（在庫確認）

各シナリオは詳細な応答テンプレートを含み、構造化された形式（番号付きリスト、箇条書き）で提供。

### 使用可能なスクリプト一覧

#### メインスクリプト（推奨）

1. **Gemma3-1B Fine-tuning** (`scripts/gemma_fine_tuning.py`)
   - ✅ 実行確認済み（27秒で完了）
   - ✅ 英語カスタマーサポートデータで訓練
   - 🎯 軽量・高速処理向け

2. **Qwen2.5-3B Fine-tuning** (`scripts/qwen_fine_tuning.py`)
   - ✅ 実行確認済み（62秒で完了）
   - ✅ GGUF変換・量子化完了
   - 🎯 より高品質な応答向け

3. **モデルマージスクリプト** (`merge_qwen_model.py`)
   - LoRAアダプターとベースモデルのマージ
   - GGUF変換前の必須ステップ

4. **テストスクリプト**
   - `test_gemma_model.py` - Gemma3モデルの効果測定
   - `test_qwen_model.py` - Qwen2.5モデルの効果測定

#### システムプロンプト比較実験機能

すべてのテストスクリプトには、ファインチューニングの効果を正確に測定するため、以下の比較機能が含まれています：

- **システムプロンプトなし**: ファインチューニング効果のみを測定
- **システムプロンプトあり**: 従来のプロンプトエンジニアリングとの比較
- **結果保存**: JSON形式で詳細な比較結果を保存

### 動作確認済み環境

- **Python**: 3.8以上
- **必要ライブラリ**: transformers, peft, datasets, torch
- **オプション**: accelerate, bitsandbytes (GPU環境用)
- **メモリ要件**: 8GB以上（Gemma3/Qwen2.5使用時）

### 実行例

```bash
# 1. Gemma3でファインチューニング（推奨）
python scripts/gemma_fine_tuning.py

# 2. 効果測定
python scripts/test_gemma_model.py

# 3. 結果確認
cat gemma3_test_results.json
```

### Fine-tuningワークフロー

#### 完全なワークフロー（Qwenモデルの例）

```bash
# 1. Fine-tuning実行
cd ollama/fine_tuning
python scripts/qwen_fine_tuning.py

# 2. LoRAアダプターをベースモデルにマージ
python merge_qwen_model.py

# 3. GGUF形式に変換（llama.cppが必要）
cd ../llama.cpp
python convert-hf-to-gguf.py ../ollama/fine_tuning/merged_qwen2.5_model \
  --outfile ../ollama/fine_tuning/qwen-customer-support-f16.gguf \
  --outtype f16

# 4. 量子化でサイズ削減
./llama-quantize ../ollama/fine_tuning/qwen-customer-support-f16.gguf \
  ../ollama/fine_tuning/qwen-customer-support.gguf Q4_K_M

# 5. Ollamaモデル作成
cd ../ollama/fine_tuning
cp qwen-customer-support.gguf finetuned_qwen2.5_model/
cd finetuned_qwen2.5_model
ollama create qwen-cs -f Modelfile

# 6. モデルのテスト
ollama run qwen-cs "I want to return a product"
```

### パフォーマンス比較（実測値）

| モデル | 訓練時間 | Loss | メモリ使用量 | ファイルサイズ |
|--------|----------|------|-------------|---------------|
| **Gemma3-1B-IT** | 27秒 | 4.4 | ~4GB | 未変換 |
| **Qwen2.5-3B-Instruct** | 62秒 | 2.55 | ~8GB | 1.8GB (Q4_K_M) |

### 重要な発見事項

1. **LoRA効率性**: 
   - Gemma3: 全パラメータの0.0687%のみを訓練
   - Qwen2.5: 全パラメータの0.0936%のみを訓練
   - メモリ効率的な訓練が可能

2. **訓練速度**:
   - Apple Silicon (MPS)でも実用的な速度で訓練可能
   - 1-2分程度で基本的なFine-tuningが完了

3. **モデルサイズの削減**:
   - F16形式: 約6GB
   - Q4_K_M量子化後: 1.8GB（70%削減）
   - 品質を保ちながら大幅なサイズ削減を実現

## 📌 まとめと推奨事項

### Fine-tuningフローのまとめ

1. **データ準備**: 業務特化の訓練データをJSON形式で準備
2. **Fine-tuning**: LoRAを使用した効率的な訓練（1-2分）
3. **モデル変換**: PyTorch → GGUF形式への変換
4. **量子化**: ファイルサイズ削減（Q4_K_M推奨）
5. **Ollama統合**: カスタムモデルとして登録・実行

### ベストプラクティス

#### データ準備
- **最小サンプル数**: 10-20（基本的な動作確認）
- **推奨サンプル数**: 50-100（実用レベル）
- **形式**: 構造化された応答（番号付きリスト、箇条書き）を含める

#### モデル選択
- **軽量・高速**: Gemma3-1B（訓練時間30秒以内）
- **バランス型**: Qwen2.5-3B（より高品質な応答）
- **高品質**: より大きなモデル（7B以上）を検討

#### 訓練パラメータ
- **エポック数**: 2（過学習を避けるため）
- **学習率**: 2e-4（安定した訓練）
- **バッチサイズ**: 1（メモリ制約に応じて調整）

### 注意事項

1. **言語の一貫性**: 訓練データと推論時の言語を統一
2. **GGUF変換**: llama.cppの最新版を使用
3. **メモリ管理**: モデルサイズに応じた適切なハードウェア選択

### 今後の改善点

1. **マルチ言語対応**: 日本語・英語混在データでの訓練
2. **評価メトリクス**: BLEU、ROUGEスコアの導入
3. **継続学習**: 既存のFine-tunedモデルへの追加訓練

## 🤝 貢献

問題を見つけた場合や改善提案がある場合は、Issueを作成してください。