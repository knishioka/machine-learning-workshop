# 🚀 Google Colabで最小限のFine-tuning - クイックスタート

## 📋 概要

- **実行時間**: 約15-20分
- **使用モデル**: TinyLlama 1.1B（最軽量）
- **必要データ**: 10-50サンプル
- **出力**: Ollama対応GGUFファイル

## 🎯 手順（5ステップ）

### 1️⃣ Google Colabを開く

1. [Google Colab](https://colab.research.google.com/)にアクセス
2. 「ファイル」→「ノートブックをアップロード」
3. `minimal_colab_fine_tuning.ipynb`をアップロード
4. 「ランタイム」→「ランタイムのタイプを変更」→ **GPU（T4）**を選択

### 2️⃣ 全セルを実行

```
ランタイム → すべてのセルを実行
```

または各セルを順番に`Shift + Enter`で実行

### 3️⃣ 実行内容（自動）

1. **環境構築**（2分）
   - Unslothインストール
   
2. **データ準備**（1分）
   - 10個のサンプルデータ生成
   
3. **Fine-tuning**（10-15分）
   - TinyLlama 1.1Bを使用
   - 30ステップのみ（最小限）
   
4. **GGUF変換**（2分）
   - Ollama用形式に変換
   
5. **ダウンロード**（自動）
   - `minimal_finetuned_model-unsloth.Q4_K_M.gguf`

### 4️⃣ ローカルでOllama使用

ダウンロードしたGGUFファイルを使用：

```bash
# 1. Modelfile作成
cat > Modelfile << EOF
FROM ./minimal_finetuned_model-unsloth.Q4_K_M.gguf

SYSTEM "あなたは技術的な質問に答える親切なアシスタントです。"

PARAMETER temperature 0.7
PARAMETER top_p 0.9
EOF

# 2. Ollamaでモデル作成
ollama create my-tech-assistant -f Modelfile

# 3. テスト実行
ollama run my-tech-assistant "Pythonでエラーが出ました。どうすればいいですか？"
```

### 5️⃣ カスタマイズ方法

#### データを変更したい場合

ノートブックのセクション2で`training_data`を編集：

```python
training_data = [
    {
        "instruction": "あなたの質問",
        "output": "期待される回答"
    },
    # 追加...
]
```

#### より良い結果を得るには

1. **データ数を増やす**: 50-100サンプル推奨
2. **ステップ数を増やす**: `max_steps=50`に変更
3. **より大きなモデル**: 
   ```python
   model_name="unsloth/llama-3.2-3b-bnb-4bit"  # 3Bモデル
   ```

## 💡 トラブルシューティング

### GPU不足エラー
→ より小さいバッチサイズ：`per_device_train_batch_size=1`

### 実行が遅い
→ ステップ数を減らす：`max_steps=20`

### ダウンロードできない
→ Google Driveにマウント：
```python
from google.colab import drive
drive.mount('/content/drive')
!cp *.gguf /content/drive/MyDrive/
```

## 📊 期待される結果

**Fine-tuning前**:
```
質問: Pythonでエラーが出ました
回答: Pythonは...（一般的で曖昧な回答）
```

**Fine-tuning後**:
```
質問: Pythonでエラーが出ました
回答: エラーの詳細を確認するには、以下の手順を試してください：
1. エラーメッセージを読んで原因を特定
2. スタックトレースで発生箇所を確認
3. 該当するコードを確認...
```

## 🎉 完了！

これで最小限のfine-tuningが完了です。実行時間は約20分、無料のGoogle Colabで実行可能です。

より本格的なfine-tuningには：
- データを50-100サンプルに増やす
- ステップ数を50-100に増やす
- 3Bや7Bモデルを使用（Colab Proが必要な場合あり）