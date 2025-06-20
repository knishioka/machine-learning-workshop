#!/usr/bin/env python3
"""
Fine-tuningしたモデルのテストスクリプト
ベースモデルとfine-tuning後のモデルの出力を比較
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import json


def load_base_model(model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
    """ベースモデルを読み込み"""
    print("ベースモデルを読み込み中...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16 if torch.backends.mps.is_available() else torch.float32,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer


def load_finetuned_model(
    base_model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0", adapter_path="./finetuned_model"
):
    """Fine-tuningしたモデルを読み込み"""
    print("Fine-tuningしたモデルを読み込み中...")
    # ベースモデルを読み込み
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        device_map="auto",
        torch_dtype=torch.float16 if torch.backends.mps.is_available() else torch.float32,
    )
    # LoRAアダプターを適用
    model = PeftModel.from_pretrained(base_model, adapter_path)
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer


def generate_response(model, tokenizer, prompt, max_length=256):
    """モデルから応答を生成"""
    # TinyLlamaのプロンプトフォーマット（カスタマーサポート用）
    formatted_prompt = f"<|system|>\nあなたはECサイトのカスタマーサポート担当です。お客様の問い合わせに丁寧に対応し、注文、配送、返品、商品についての質問に親切に答えてください。</s>\n<|user|>\n{prompt}</s>\n<|assistant|>\n"

    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_length,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # アシスタントの応答部分のみを抽出
    if "<|assistant|>" in response:
        response = response.split("<|assistant|>")[-1].strip()
    return response


def main():
    # テストする質問（カスタマーサポート用）
    test_questions = [
        "注文した商品がまだ届きません",
        "商品を返品したいです",
        "支払い方法を変更できますか？",
        "商品のサイズが合わない",
        "ポイントの有効期限はいつまでですか？",
    ]

    print("=" * 80)
    print("Fine-tuningモデルの比較テスト")
    print("=" * 80)

    # ベースモデルを読み込み
    base_model, base_tokenizer = load_base_model()

    # Fine-tuningしたモデルを読み込み
    try:
        finetuned_model, finetuned_tokenizer = load_finetuned_model()
        has_finetuned = True
    except Exception as e:
        print(f"Fine-tuningモデルの読み込みに失敗: {e}")
        has_finetuned = False

    # 各質問に対して比較
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'=' * 80}")
        print(f"質問 {i}: {question}")
        print("=" * 80)

        # ベースモデルの応答
        print("\n【ベースモデル (TinyLlama-1.1B)】")
        print("-" * 40)
        base_response = generate_response(base_model, base_tokenizer, question)
        print(base_response)

        # Fine-tuningモデルの応答
        if has_finetuned:
            print("\n【Fine-tuned モデル】")
            print("-" * 40)
            finetuned_response = generate_response(finetuned_model, finetuned_tokenizer, question)
            print(finetuned_response)

        print()

    # トレーニングデータの確認
    print("\n" + "=" * 80)
    print("参考: トレーニングデータ")
    print("=" * 80)

    try:
        with open("./finetuned_model/training_data.jsonl", "r") as f:
            for i, line in enumerate(f, 1):
                data = json.loads(line)
                print(f"\nサンプル {i}:")
                print(
                    f"Q: {data['text'].split('### Human:')[1].split('### Assistant:')[0].strip()}"
                )
                print(f"A: {data['text'].split('### Assistant:')[1].strip()}")
    except:
        print("トレーニングデータが見つかりません")


if __name__ == "__main__":
    main()
