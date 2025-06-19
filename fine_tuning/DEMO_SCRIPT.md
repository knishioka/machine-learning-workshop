# Fine-tuning デモ実行スクリプト

## 🎯 デモの目的
Fine-tuningの実際の効果と限界を実演で示し、プロンプトエンジニアリングとの違いを理解してもらう

---

## 📋 事前準備チェックリスト

```bash
# 1. 必要なライブラリの確認
pip list | grep -E "transformers|peft|datasets|torch"

# 2. Ollamaの起動確認
ollama list

# 3. 作業ディレクトリへ移動
cd /Users/ken/Developer/private/machine-learning-workshop/fine_tuning

# 4. デモ用ファイルの確認
ls demo*.py demo-modelfile
```

---

## 🚀 デモ1: TinyLlama Fine-tuning（10分）

### 1-1. Fine-tuningスクリプトの説明（2分）

```bash
# スクリプトの中身を簡単に表示
head -n 50 demo_tinyllama_finetuning.py
```

**説明ポイント**：
- 「10個のカスタマーサポートデータで訓練します」
- 「LoRAという効率的な手法を使って、全パラメータの1%だけを更新」
- 「具体的な価格（$6.99）や返品ポリシー（14日間）を学習させようとしています」

### 1-2. Fine-tuning実行（1分）

```bash
# 実行（約53秒）
python demo_tinyllama_finetuning.py
```

**実行中の説明**：
- 「Apple SiliconのMPSを使って実行中」
- 「3エポック、つまりデータを3回繰り返して学習」
- 「Loss値が下がっているのは学習が進んでいる証拠」

### 1-3. 効果検証（5分）

```bash
# 検証スクリプト実行
python verify_tinyllama_finetuning.py
```

**重要な比較ポイントを画面で指しながら説明**：

1. **ベースモデルの回答**（Before）：
   ```
   "I don't have access to specific shipping rates..."
   ```
   → 「一般的で曖昧な回答しかできない」

2. **Fine-tunedモデルの回答**（After）：
   ```
   "Shipping costs are included in the total purchase price..."
   ```
   → 「構造は少し改善したが、$6.99という具体的な価格は学習されていない」

3. **期待される回答**（訓練データ）：
   ```
   "Standard Shipping: $6.99 flat rate..."
   ```
   → 「これが学習させたかった内容」

### 1-4. 結論（2分）

「10サンプル、53秒のFine-tuningでは：」
- ✅ 回答の構造がわずかに改善
- ❌ 具体的な価格情報は学習されず
- ❌ ドメイン固有の知識（14日返品ポリシー）も学習されず

「つまり、少量データでのFine-tuningには限界がある」

---

## 🎯 デモ2: プロンプトエンジニアリングとの比較（5分）

### 2-1. プロンプトエンジニアリングの準備（1分）

```bash
# Modelfileを表示
cat demo-modelfile
```

**説明ポイント**：
- 「システムプロンプトに具体的な情報を埋め込んでいます」
- 「$6.99、14日間返品などの情報を直接指定」
- 「Fine-tuningなし、単なる設定ファイル」

### 2-2. Ollamaモデル作成（30秒）

```bash
# モデル作成（既に作成済みの場合はスキップ）
ollama create demo-support -f demo-modelfile
```

### 2-3. 実行と比較（3分）

```bash
# プロンプトエンジニアリングの結果
ollama run demo-support "What are the shipping costs?"
```

**画面に表示される結果を指して**：
```
Standard Shipping: $6.99
FREE (for orders over $50)
Express Shipping: $14.99
```

「見てください！Fine-tuningなしで期待通りの具体的な回答が得られました」

### 2-4. 他の質問でも確認（30秒）

```bash
# 返品ポリシーについて
ollama run demo-support "How do I return a product?"
```

---

## 📊 デモ3: 実際のワークフロー説明（2分）

### 3-1. Fine-tuning → Ollama変換の流れ

```bash
# ディレクトリ構造を表示
ls -la finetuned_tinyllama_demo/
```

**ホワイトボードに描きながら説明**：
```
PyTorch形式（Fine-tuning）
    ↓
LoRAアダプター（adapter_model.bin）
    ↓
マージ（ベースモデル + LoRA）
    ↓
GGUF変換（llama.cpp使用）
    ↓
量子化（6GB → 1.8GB）
    ↓
Ollama（実行可能！）
```

### 3-2. 実際のコマンド例（説明のみ）

```bash
# これらのコマンドは説明のみ（実行しない）
echo "# 1. LoRAマージ"
echo "python merge_model.py"

echo "# 2. GGUF変換"
echo "python convert-hf-to-gguf.py model --outfile model.gguf"

echo "# 3. 量子化"
echo "llama-quantize model.gguf model-q4.gguf Q4_K_M"

echo "# 4. Ollama登録"
echo "ollama create my-model -f Modelfile"
```

---

## 💡 デモのまとめ（1分）

**スライドに戻って強調**：

1. **Fine-tuningの現実**
   - 少量データでは効果限定的
   - 時間とリソースが必要
   - 魔法の杖ではない

2. **実践的アプローチ**
   - まずプロンプトエンジニアリング
   - 効果不十分なら実験的Fine-tuning
   - 本格導入は十分な準備の後

3. **コスト対効果**
   - プロンプト：即座、無料、柔軟
   - Fine-tuning：時間、GPU、データ必要

---

## 🆘 トラブルシューティング

### エラー1: CUDAエラー
```bash
# MPSに切り替え
export PYTORCH_ENABLE_MPS_FALLBACK=1
```

### エラー2: メモリ不足
```bash
# バッチサイズを小さくする
# demo_tinyllama_finetuning.py の per_device_train_batch_size=1
```

### エラー3: Ollamaが起動していない
```bash
# Ollamaを起動
ollama serve
```

---

## 📝 デモ後のQ&A想定回答

**Q: なぜ具体的な価格が学習されなかったのですか？**
```
A: 3つの理由があります：
1. データ量が10個と少なすぎる
2. モデルサイズ（1.1B）が小さい
3. エポック数（3回）が少ない
実用レベルには100+サンプル必要です。
```

**Q: もっと大きなモデルなら効果はありますか？**
```
A: はい、効果は向上します。
- 3Bモデル：ある程度の効果
- 7Bモデル：実用レベル
ただし、訓練時間も比例して増加します。
```

**Q: プロンプトエンジニアリングで十分では？**
```
A: 多くの場合はその通りです。
Fine-tuningが必要なのは：
- 大量の独自知識がある場合
- 特殊なフォーマットが必要な場合
- 一貫性が極めて重要な場合
```

---

## 🎬 デモ終了後

```bash
# クリーンアップ（オプション）
ollama rm demo-support
rm -rf finetuned_tinyllama_demo/

# または保持して質問に備える
echo "デモ環境を保持しています。追加の質問があればお答えします。"
```