# MacでのLocal Fine-tuningガイド

## 📱 Macでのfine-tuning可能性

### ✅ 可能なケース

#### 1. **Apple Silicon Mac (M1/M2/M3)の場合**

Apple Siliconを搭載したMacでは、MLXフレームワークを使用してfine-tuningが可能です。

```bash
# MLXのインストール
pip install mlx mlx-lm

# 小規模モデルのfine-tuning例
python -m mlx_lm.lora \
  --model mistralai/Mistral-7B-v0.1 \
  --adapter-path ./adapters \
  --data ./data.jsonl \
  --train
```

**メリット:**
- GPUなしでも動作
- 電力効率が良い
- 統合メモリアーキテクチャ

**制限:**
- 大規模モデル（70B+）は困難
- 学習速度はGPUより遅い
- メモリ上限（8GB/16GB/32GB）

#### 2. **CPUベースのfine-tuning**

小規模モデルならCPUでも可能：

```python
# transformersを使用した例
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer
)

# 1B以下の小規模モデル
model = AutoModelForCausalLM.from_pretrained(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    device_map="cpu",
    load_in_8bit=True  # メモリ削減
)
```

### ⚠️ 制限事項

| 項目 | Intel Mac | Apple Silicon Mac |
|------|-----------|------------------|
| 対応モデルサイズ | ~1B | ~7B |
| 学習速度 | 非常に遅い | 遅い |
| メモリ要件 | 16GB+ | 16GB+ |
| 推奨フレームワーク | CPU版PyTorch | MLX |

## 🛠️ 実践的なMac fine-tuningセットアップ

### 方法1: MLX-LMを使用（M1/M2/M3 Mac推奨）

```bash
# 1. 環境セットアップ
conda create -n mlx-finetune python=3.10
conda activate mlx-finetune
pip install mlx mlx-lm

# 2. データ準備
cat > training_data.jsonl << EOF
{"text": "### Human: Pythonでリストを逆順にする方法は？\n### Assistant: reversed()関数、スライス[::-1]、またはreverse()メソッドが使えます。"}
{"text": "### Human: gitでコミットを取り消すには？\n### Assistant: git reset --soft HEAD~1 でコミットを取り消し、変更は保持されます。"}
EOF

# 3. Fine-tuning実行
python -m mlx_lm.lora \
  --model mlx-community/Llama-3.2-1B-4bit \
  --data ./training_data.jsonl \
  --adapter-path ./lora_adapters \
  --iters 100
```

### 方法2: 量子化モデルでのQLoRA

```python
# qlora_mac.py
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments
)
from peft import LoraConfig, get_peft_model

# 4bit量子化設定
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

# モデル読み込み（1B以下推奨）
model = AutoModelForCausalLM.from_pretrained(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    quantization_config=bnb_config,
    device_map="auto"
)

# LoRA設定
lora_config = LoraConfig(
    r=8,  # 低ランク
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1
)

model = get_peft_model(model, lora_config)
```

### 方法3: Unsloth on Mac（実験的）

```bash
# Rosetta 2経由でx86版を使用（M1/M2/M3）
arch -x86_64 /usr/bin/python3 -m pip install unsloth

# または、より軽量なアプローチ
pip install torch torchvision torchaudio
pip install transformers datasets accelerate peft bitsandbytes
```

## 📊 実行時間の目安

| モデルサイズ | Intel Mac | M1 Mac | M2/M3 Mac | 比較: RTX 4090 |
|------------|-----------|---------|-----------|----------------|
| 1B params | 4-6時間 | 2-3時間 | 1-2時間 | 10分 |
| 3B params | 12-18時間 | 6-8時間 | 4-6時間 | 30分 |
| 7B params | 非推奨 | 24時間+ | 12-18時間 | 1時間 |

## 🎯 Mac fine-tuningのベストプラクティス

### 1. **データセットを小さく保つ**
```python
# 100-500サンプル程度に制限
train_dataset = dataset.select(range(500))
```

### 2. **バッチサイズを最小に**
```python
training_args = TrainingArguments(
    per_device_train_batch_size=1,  # 最小
    gradient_accumulation_steps=8,   # 代わりに累積
    fp16=True,                      # メモリ削減
)
```

### 3. **チェックポイント保存**
```python
# 中断に備えて頻繁に保存
training_args = TrainingArguments(
    save_steps=50,
    save_total_limit=2,
    resume_from_checkpoint=True
)
```

### 4. **メモリ監視**
```bash
# Activity Monitorでメモリ使用量を監視
# または
sudo powermetrics --samplers smc | grep -i "temperature"
```

## 🔄 OllamaへのGGUF変換

Fine-tuning後、Ollamaで使用するには：

```bash
# 1. PyTorchモデルをGGUF変換
python convert.py model_path --outfile model.gguf --outtype q4_0

# 2. Ollamaで使用
ollama create my-mac-model -f Modelfile
```

## 💡 推奨事項

### Macでfine-tuningする場合:
- **小規模モデル（1-3B）**に限定
- **少量のデータ（<1000サンプル）**で実験
- **MLX**（Apple Silicon）または**QLoRA**を使用
- **夜間実行**を推奨（長時間かかるため）

### 本格的なfine-tuningが必要な場合:
- **Google Colab**（無料GPU）
- **Runpod**や**Vast.ai**（時間課金GPU）
- **AWS/GCP**のGPUインスタンス

## 🚨 注意事項

1. **発熱管理**: 長時間の実行でMacが高温になる可能性
2. **電源接続**: バッテリーでの実行は避ける
3. **他の作業**: fine-tuning中は他の重い作業を避ける
4. **スリープ防止**: `caffeinate -i python train.py`

## 🚀 実行スクリプト

### 自動セットアップ
```bash
# 環境構築（初回のみ）
cd ollama/fine_tuning
./scripts/setup_mac_env.sh

# 仮想環境有効化
source venv/bin/activate
source .env
```

### Fine-tuning実行
```bash
# MLX使用（Apple Silicon推奨）
python scripts/mac_local_fine_tuning.py --method mlx

# PyTorch使用（Intel Mac/代替手法）
python scripts/mac_local_fine_tuning.py --method pytorch

# カスタム設定
python scripts/mac_local_fine_tuning.py \
  --method mlx \
  --iterations 200 \
  --output-dir ./my_model
```

## まとめ

MacでのLocal fine-tuningは**可能だが制限が多い**です。

- **プロトタイピング**: Mac上で小規模実験 ✅
- **本番fine-tuning**: クラウドGPU推奨 ⭐
- **Ollama使用**: fine-tuning後のモデルは問題なく動作 ✅

小規模な実験やPoC（概念実証）にはMacでも十分ですが、実用的なfine-tuningにはGPU環境を使用することをお勧めします。

### 提供スクリプト
- `scripts/setup_mac_env.sh`: 環境自動セットアップ
- `scripts/mac_local_fine_tuning.py`: Mac用fine-tuningスクリプト