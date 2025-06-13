# Fine-tuning Scripts

このディレクトリには、日本語対応カスタマーサポートモデルのファインチューニング用スクリプトが含まれています。

## スクリプト一覧

### 1. gemma_fine_tuning.py 🌟推奨
Gemma3-4B-Instructモデルを日本語ECサイトのカスタマーサポート用にファインチューニングするメインスクリプトです。

**特徴：**
- Gemma3-4B-Instructをベースに使用
- マルチモーダル対応（テキスト特化でも使用可能）
- 日本語での自然な応答を生成
- ECサイトのカスタマーサポートに特化したトレーニングデータ
- LoRAを使用したメモリ効率的なファインチューニング

**実行方法：**
```bash
python scripts/gemma_fine_tuning.py
```

### 2. test_gemma_model.py
ファインチューニング前後のGemma3モデルの応答を比較するテストスクリプトです。

**特徴：**
- ベースモデルとファインチューニング済みモデルの比較
- システムプロンプトありなしの効果測定
- 典型的なカスタマーサポートの質問でテスト
- 結果をJSONファイルに保存

**実行方法：**
```bash
python scripts/test_gemma_model.py
```

### 3. qwen_fine_tuning.py
Qwen2.5-3B-Instructモデルを日本語ECサイトのカスタマーサポート用にファインチューニングするスクリプトです。

**特徴：**
- Qwen2.5-3B-Instructをベースに使用
- 日本語特化の高品質応答
- メモリ効率的（6GB程度）
- ECサイトのカスタマーサポートに特化

**実行方法：**
```bash
python scripts/qwen_fine_tuning.py
```

### 4. test_qwen_model.py
ファインチューニング前後のQwen2.5モデルの応答を比較するテストスクリプトです。

**特徴：**
- ベースモデルとファインチューニング済みモデルの比較
- システムプロンプトありなしの効果測定
- 結果をJSONファイルに保存

**実行方法：**
```bash
python scripts/test_qwen_model.py
```

### 5. mac_local_fine_tuning.py
Mac（特にApple Silicon）でローカルにファインチューニングを実行するためのスクリプトです。

**特徴：**
- MLXとPyTorchの両方をサポート
- Apple Silicon向けに最適化
- 複数のモデルサイズから選択可能

**実行方法：**
```bash
# MLXを使用（Apple Silicon推奨）
python scripts/mac_local_fine_tuning.py --method mlx --mlx-model medium

# PyTorchを使用
python scripts/mac_local_fine_tuning.py --method pytorch --model TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

### 6. test_focused_3b.py
3Bモデルに特化したテストスクリプトです。様々な3Bモデルの性能を比較できます。

**実行方法：**
```bash
python scripts/test_focused_3b.py
```

## 推奨される実行順序

1. **ファインチューニングの実行**
   ```bash
   # Gemma3を使用（推奨）
   python scripts/gemma_fine_tuning.py
   
   # または Qwen2.5を使用
   python scripts/qwen_fine_tuning.py
   ```

2. **モデルのテスト**
   ```bash
   # Gemma3のテスト
   python scripts/test_gemma_model.py
   
   # または Qwen2.5のテスト
   python scripts/test_qwen_model.py
   ```

3. **GGUF変換とOllamaでの実行**
   ```bash
   # llama.cppでGGUF形式に変換
   python convert.py ./finetuned_gemma3_model --outtype q4_k_m
   
   # Ollamaモデルを作成
   ollama create gemma3-customer-support -f ./finetuned_gemma3_model/Modelfile
   
   # モデルを実行
   ollama run gemma3-customer-support
   ```

## システムプロンプト比較実験

すべてのテストスクリプトには、ファインチューニングの純粋な効果を測定するため、以下の機能が含まれています：

- **システムプロンプトなし**: ファインチューニング効果のみを測定
- **システムプロンプトあり**: 従来のプロンプトエンジニアリングとの比較
- **JSON出力**: 詳細な比較結果をファイルに保存

## 必要な環境

- Python 3.8以上
- PyTorch（MPSまたはCUDA対応）
- transformers, peft, datasets, accelerate
- （オプション）mlx, mlx-lm（Apple Silicon向け）

## 動作確認済み

✅ すべてのスクリプトが構文チェック済み  
✅ 必要なライブラリの依存関係確認済み  
✅ システムプロンプト比較実験機能搭載

## 注意事項

- Gemma3/Qwen2.5モデルは約3-4GBのメモリを使用します
- ファインチューニングには最低8GB以上のRAMを推奨
- Apple SiliconのMacではMPSアクセラレーションが自動的に使用されます