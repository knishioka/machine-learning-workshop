#!/usr/bin/env python3
"""
TinyLlama Fine-tuning Demo
プレゼンテーション用の最小限のfine-tuningデモ
"""

from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, TaskType
import torch
from datasets import Dataset
import json
import time
from datetime import datetime

# カスタマーサポートの訓練データ（10サンプル）
training_data = [
    {
        "instruction": "What are the shipping costs?",
        "input": "",
        "output": "Here are our shipping options and costs:\n\n**Standard Shipping:**\n- $6.99 flat rate\n- FREE on orders over $50\n- 3-5 business days\n\n**Express Shipping:**\n- $14.99 flat rate\n- 1-2 business days\n\n**International Shipping:**\n- Rates vary by country\n- 7-14 business days\n\nAll orders include tracking information sent to your email.",
    },
    {
        "instruction": "I want to return a product",
        "input": "",
        "output": "I'll be happy to help you with your return.\n\nHere's our return process:\n\n**Return Policy:**\n- Returns accepted within 14 days of delivery\n- Items must be unused and in original packaging\n- Return shipping labels provided for free\n\n**How to start a return:**\n1. Visit our returns portal\n2. Enter your order number and email\n3. Select items to return\n4. Print the prepaid shipping label\n5. Drop off at any shipping location\n\nRefunds are processed within 3-5 business days after we receive the item.",
    },
    {
        "instruction": "How do I track my order?",
        "input": "",
        "output": "To track your order:\n\n1. Check your email for the shipping confirmation\n2. Click the tracking link in the email\n3. Or visit our website and go to 'Track Order'\n4. Enter your order number and email\n\nYou'll see:\n- Current location of your package\n- Estimated delivery date\n- Delivery history\n\nNeed help? Reply with your order number and I'll check for you.",
    },
    {
        "instruction": "What payment methods do you accept?",
        "input": "",
        "output": "We accept the following payment methods:\n\n**Credit/Debit Cards:**\n- Visa\n- Mastercard\n- American Express\n- Discover\n\n**Digital Wallets:**\n- PayPal\n- Apple Pay\n- Google Pay\n\n**Other Options:**\n- Bank Transfer (for orders over $500)\n- Buy Now, Pay Later with Klarna\n- Gift Cards\n\nAll payments are processed securely with SSL encryption.",
    },
    {
        "instruction": "Do you offer discounts for bulk orders?",
        "input": "",
        "output": "Yes! We offer bulk discounts:\n\n**Bulk Pricing Tiers:**\n- 10-24 items: 10% off\n- 25-49 items: 15% off\n- 50-99 items: 20% off\n- 100+ items: 25% off\n\n**How to get bulk pricing:**\n1. Add items to cart\n2. Discount automatically applies\n3. Or contact sales@company.com for custom quotes\n\n**Additional benefits:**\n- Dedicated account manager\n- Priority shipping\n- Net 30 payment terms available",
    },
    {
        "instruction": "I received a damaged item",
        "input": "",
        "output": "I'm sorry to hear your item arrived damaged.\n\n**Immediate steps:**\n1. Take photos of the damage\n2. Keep all packaging materials\n\n**Resolution options:**\n- **Replacement**: We'll send a new item immediately\n- **Refund**: Full refund including shipping\n- **Partial refund**: If damage is minor\n\n**To proceed:**\n- Email photos to support@company.com\n- Include your order number\n- We'll respond within 2 hours\n\nNo need to return the damaged item - we'll handle everything for you.",
    },
    {
        "instruction": "What is your price match policy?",
        "input": "",
        "output": "We offer price matching!\n\n**Price Match Policy:**\n- Match any authorized retailer's price\n- Item must be identical (same model, color, size)\n- Must be in stock at competitor\n\n**How to request:**\n1. Contact us before purchasing\n2. Provide competitor's link\n3. We'll verify and match the price\n4. Plus give you an extra 5% off!\n\n**Exclusions:**\n- Clearance/liquidation sales\n- Black Friday/special events\n- Membership-only prices\n\nValid for 14 days after purchase too!",
    },
    {
        "instruction": "How do I cancel my order?",
        "input": "",
        "output": "To cancel your order:\n\n**If order hasn't shipped:**\n- Visit 'My Orders' on our website\n- Click 'Cancel Order'\n- You'll receive confirmation immediately\n- Full refund in 1-2 business days\n\n**If order has shipped:**\n- You can refuse delivery\n- Or start a free return once received\n- Full refund upon return\n\n**Need urgent cancellation?**\n- Call: 1-800-XXX-XXXX\n- Chat: Available 24/7\n- Email: cancel@company.com\n\nWe process cancellations within 1 hour during business hours.",
    },
    {
        "instruction": "Do you ship internationally?",
        "input": "",
        "output": "Yes, we ship worldwide!\n\n**International Shipping:**\n- Available to 180+ countries\n- Shipping time: 7-14 business days\n- Express option: 3-5 business days\n\n**Shipping Rates:**\n- Standard: Starting at $19.99\n- Express: Starting at $39.99\n- FREE on orders over $150\n\n**Important notes:**\n- Customs fees may apply\n- Full tracking provided\n- All prices in USD\n- Some restrictions for certain products\n\nEnter your country at checkout to see exact rates.",
    },
    {
        "instruction": "How can I change my shipping address?",
        "input": "",
        "output": "To change your shipping address:\n\n**If order hasn't shipped:**\n1. Log into your account\n2. Go to 'My Orders'\n3. Click 'Edit' next to shipping address\n4. Update and save\n\n**If order has shipped:**\n- Contact the carrier directly\n- Or we can intercept the package (may incur fees)\n\n**For future orders:**\n- Update your default address in 'Account Settings'\n- Save multiple addresses for easy selection\n\n**Need help?**\n- Chat with us for immediate assistance\n- We'll update it for you!",
    },
]


def format_training_examples(data):
    """訓練データをTinyLlama形式に変換"""
    formatted_data = []

    for item in data:
        # TinyLlama chat template format
        text = f"<|system|>\nYou are a helpful customer support assistant for an e-commerce company. Provide clear, structured responses with specific details.</s>\n<|user|>\n{item['instruction']}</s>\n<|assistant|>\n{item['output']}</s>"
        formatted_data.append({"text": text})

    return formatted_data


def main():
    print("=" * 60)
    print("TinyLlama Fine-tuning Demo")
    print("=" * 60)

    # デバイスの設定
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"使用デバイス: {device}")

    # モデルとトークナイザーの読み込み
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    print(f"\nモデル {model_name} を読み込み中...")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_name, torch_dtype=torch.float32, device_map="auto" if device.type != "mps" else None
    )

    if device.type == "mps":
        model = model.to(device)

    # LoRA設定
    print("\nLoRAアダプターを設定中...")
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=16,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=[
            "q_proj",
            "v_proj",
            "k_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
    )

    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    # データセットの準備
    print("\n訓練データを準備中...")
    formatted_data = format_training_examples(training_data)

    def tokenize_function(examples):
        model_inputs = tokenizer(
            examples["text"], truncation=True, padding="max_length", max_length=512
        )
        # ラベルをinput_idsと同じに設定（言語モデリング用）
        model_inputs["labels"] = model_inputs["input_ids"].copy()
        return model_inputs

    dataset = Dataset.from_list(formatted_data)
    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    # 訓練引数の設定
    training_args = TrainingArguments(
        output_dir="./finetuned_tinyllama_demo",
        num_train_epochs=3,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        warmup_steps=10,
        logging_steps=5,
        save_strategy="epoch",
        learning_rate=2e-4,
        fp16=False,  # MPSではFP16を無効化
        push_to_hub=False,
        report_to=[],  # ログ出力を無効化
        dataloader_pin_memory=False,  # この行を追加
    )

    # トレーナーの作成
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        processing_class=tokenizer,
        data_collator=None,
    )

    # Fine-tuning実行
    print("\nFine-tuningを開始します...")
    print(f"データ数: {len(training_data)}")
    print(f"エポック数: {training_args.num_train_epochs}")
    print(f"バッチサイズ: {training_args.per_device_train_batch_size}")
    print("-" * 40)

    start_time = time.time()
    trainer.train()
    end_time = time.time()

    training_time = end_time - start_time
    print(f"\n訓練完了！")
    print(f"訓練時間: {training_time:.1f}秒")

    # モデルの保存
    print("\nモデルを保存中...")
    trainer.save_model()
    tokenizer.save_pretrained("./finetuned_tinyllama_demo")

    print("\n✅ Fine-tuning完了!")
    print(f"モデルは ./finetuned_tinyllama_demo に保存されました")
    print("\n次のステップ:")
    print("1. python verify_tinyllama_finetuning.py で効果を検証")
    print("2. 必要に応じてGGUF形式に変換してOllamaで使用")


if __name__ == "__main__":
    main()
