#!/usr/bin/env python3
"""
真のFine-tuningデモ（Unsloth使用）
このスクリプトは実際にモデルの重みを更新する真のfine-tuningを実行し、
その後Ollamaで使用できるGGUF形式で出力します。

注意: このスクリプトはGPU環境（Google Colabなど）での実行を推奨します。
"""

import json
import os
from typing import List, Dict

# Unslothのインストール（初回のみ）
# !pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
# !pip install --no-deps trl peft accelerate bitsandbytes

def create_training_data() -> List[Dict]:
    """
    シンプルなfine-tuning用データセットを作成
    技術サポートチャットボット用のデータ
    """
    training_data = [
        {
            "instruction": "Pythonでリストを逆順にする方法を教えてください",
            "input": "",
            "output": "Pythonでリストを逆順にする方法は3つあります：\n1. `reversed()`: `list(reversed(my_list))`\n2. スライス: `my_list[::-1]`\n3. `reverse()`: `my_list.reverse()` (元のリストを変更)"
        },
        {
            "instruction": "エラー: 'NoneType' object has no attribute 'append'",
            "input": "このエラーが出ました。どう対処すればいいですか？",
            "output": "このエラーは、None型のオブジェクトに対してappend()メソッドを呼び出そうとした時に発生します。\n\n対処法：\n1. 変数がNoneでないことを確認: `if my_list is not None:`\n2. 初期化を確認: `my_list = []`のように正しく初期化されているか\n3. 関数の戻り値を確認: 何も返さない関数はNoneを返します"
        },
        {
            "instruction": "gitでコミットを取り消す方法",
            "input": "",
            "output": "gitでコミットを取り消す方法：\n\n1. 直前のコミットを取り消し（ファイルは保持）:\n   `git reset --soft HEAD~1`\n\n2. 直前のコミットを完全に取り消し:\n   `git reset --hard HEAD~1`\n\n3. コミットを残して内容を修正:\n   `git commit --amend`"
        },
        {
            "instruction": "Dockerコンテナが起動しません",
            "input": "docker runを実行してもすぐに停止してしまいます",
            "output": "Dockerコンテナがすぐに停止する場合の確認事項：\n\n1. ログを確認: `docker logs <container_id>`\n2. エントリポイントの確認: CMDやENTRYPOINTが正しく設定されているか\n3. インタラクティブモードで起動: `docker run -it <image>`\n4. プロセスが終了していないか確認: フォアグラウンドプロセスが必要です"
        },
        {
            "instruction": "機械学習モデルの過学習を防ぐ方法",
            "input": "",
            "output": "過学習（オーバーフィッティング）を防ぐ主な方法：\n\n1. **正則化**: L1/L2正則化を追加\n2. **ドロップアウト**: ニューロンをランダムに無効化\n3. **データ拡張**: 訓練データを人工的に増やす\n4. **早期停止**: 検証損失が上昇し始めたら訓練を停止\n5. **交差検証**: データを分割して汎化性能を確認"
        }
    ]
    
    # より多くのデータを生成（実際のfine-tuningには通常もっと多くのデータが必要）
    extended_data = []
    for item in training_data:
        # オリジナルを追加
        extended_data.append(item)
        
        # バリエーションを追加
        if "エラー" in item["instruction"]:
            variation = item.copy()
            variation["input"] = "初心者です。" + variation["input"]
            variation["output"] = "初心者の方向けに説明しますね。\n\n" + variation["output"]
            extended_data.append(variation)
    
    return extended_data


def format_for_training(data: List[Dict]) -> List[Dict]:
    """
    データをAlpaca形式に整形
    """
    formatted_data = []
    for item in data:
        formatted_item = {
            "instruction": item["instruction"],
            "input": item.get("input", ""),
            "output": item["output"]
        }
        formatted_data.append(formatted_item)
    return formatted_data


def main():
    """
    メイン実行関数
    注意: 以下のコードは主にGoogle Colab環境での実行を想定しています
    """
    
    print("=== 真のFine-tuningデモ（Unsloth使用） ===\n")
    
    # 1. トレーニングデータの準備
    print("1. トレーニングデータを準備中...")
    training_data = create_training_data()
    formatted_data = format_for_training(training_data)
    
    # データをファイルに保存
    with open('tech_support_data.json', 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, ensure_ascii=False, indent=2)
    
    print(f"   ✅ {len(formatted_data)}件のトレーニングデータを準備しました\n")
    
    # 2. Unslothを使用したfine-tuningコード
    print("2. Fine-tuningコード（Google Colabで実行）:\n")
    
    fine_tuning_code = '''
# Google Colabで実行するコード
from unsloth import FastLanguageModel
import torch
from datasets import Dataset
from trl import SFTTrainer
from transformers import TrainingArguments

# モデルとトークナイザーの読み込み
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/tinyllama-bnb-4bit",  # 軽量モデルを使用
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)

# LoRAアダプターの追加（効率的なfine-tuning）
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # ランク
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=3407,
)

# データセットの準備
with open('tech_support_data.json', 'r') as f:
    data = json.load(f)

dataset = Dataset.from_list(data)

# プロンプトフォーマット関数
def formatting_prompts_func(examples):
    instructions = examples["instruction"]
    inputs = examples["input"]
    outputs = examples["output"]
    texts = []
    for instruction, input, output in zip(instructions, inputs, outputs):
        text = f"""### Instruction:
{instruction}

### Input:
{input}

### Response:
{output}"""
        texts.append(text)
    return {"text": texts}

# トレーナーの設定
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=2048,
    formatting_func=formatting_prompts_func,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=50,  # デモ用に少なめに設定
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=1,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir="outputs",
    ),
)

# Fine-tuning実行
trainer.train()

# GGUF形式で保存（Ollama用）
print("\\nGGUF形式で保存中...")
model.save_pretrained_gguf(
    "tech_support_model",
    tokenizer,
    quantization_method="q4_k_m"
)
print("✅ tech_support_model-unsloth.Q4_K_M.gguf として保存されました")
'''
    
    print(fine_tuning_code)
    
    # 3. Ollama用のModelfile作成
    print("\n3. Ollama用Modelfileを作成中...")
    
    modelfile_content = '''FROM ./tech_support_model-unsloth.Q4_K_M.gguf

# システムプロンプト
SYSTEM """あなたは親切で知識豊富な技術サポートアシスタントです。
プログラミング、エラー解決、開発ツールについて的確なアドバイスを提供します。
初心者にも分かりやすく、具体的な解決策を提示してください。"""

# パラメータ設定
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1
PARAMETER num_predict 512
'''
    
    with open('Modelfile.tech-support-finetuned', 'w', encoding='utf-8') as f:
        f.write(modelfile_content)
    
    print("   ✅ Modelfile.tech-support-finetuned を作成しました\n")
    
    # 4. Ollamaでの使用方法
    print("4. Ollamaでの使用方法:\n")
    
    usage_instructions = '''
# 1. GGUF形式のモデルファイルをダウンロード（Colabから）
# 2. Ollamaでモデルを作成
ollama create tech-support-finetuned -f Modelfile.tech-support-finetuned

# 3. モデルをテスト
ollama run tech-support-finetuned "Pythonでファイルを読み込む方法を教えてください"

# 4. 比較テスト（オリジナルモデルと比較）
echo "=== Fine-tunedモデル ===" 
ollama run tech-support-finetuned "Dockerコンテナが起動しません"

echo "\\n=== ベースモデル ==="
ollama run tinyllama "Dockerコンテナが起動しません"
'''
    
    print(usage_instructions)
    
    # 5. 実行手順のまとめ
    print("\n5. 実行手順のまとめ:\n")
    print("   1) Google Colabで上記のfine-tuningコードを実行")
    print("   2) 生成されたGGUFファイルをローカルにダウンロード")
    print("   3) Modelfileと同じディレクトリに配置")
    print("   4) ollamaコマンドでモデルを作成・実行")
    print("\n注意: 実際のfine-tuningにはGPU環境が必要です。")
    print("      Google Colab（無料版）でも実行可能です。")


if __name__ == "__main__":
    main()