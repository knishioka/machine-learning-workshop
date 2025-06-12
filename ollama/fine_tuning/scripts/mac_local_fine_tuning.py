#!/usr/bin/env python3
"""
Mac Local Fine-tuning Script
Apple Silicon Mac (M1/M2/M3)で最小限のfine-tuningを実行するスクリプト
MLXフレームワークを使用して効率的に動作
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import List, Dict

# カラー出力用
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

def print_status(message: str, status: str = "info"):
    """ステータスメッセージを色付きで表示"""
    if status == "info":
        print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")
    elif status == "success":
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
    elif status == "warning":
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")
    elif status == "error":
        print(f"{Colors.RED}❌ {message}{Colors.END}")

def check_mac_platform():
    """Macプラットフォームのチェック"""
    import platform
    
    if platform.system() != "Darwin":
        print_status("このスクリプトはmacOS専用です", "error")
        sys.exit(1)
    
    # Apple Siliconかどうかチェック
    processor = platform.processor()
    if "arm" in processor.lower():
        print_status("Apple Silicon Mac検出 ✨", "success")
        return "apple_silicon"
    else:
        print_status("Intel Mac検出（パフォーマンスが制限されます）", "warning")
        return "intel"

def check_dependencies():
    """必要な依存関係をチェック"""
    dependencies = {
        "mlx": "pip install mlx mlx-lm",
        "transformers": "pip install transformers",
        "torch": "pip install torch torchvision torchaudio",
        "peft": "pip install peft"
    }
    
    missing = []
    for package, install_cmd in dependencies.items():
        try:
            __import__(package)
        except ImportError:
            missing.append((package, install_cmd))
    
    if missing:
        print_status("必要なパッケージが不足しています:", "error")
        for pkg, cmd in missing:
            print(f"  - {pkg}: {cmd}")
        print("\n必要なパッケージをインストールしてください。")
        sys.exit(1)
    
    print_status("依存関係チェック完了", "success")

def create_sample_data() -> List[Dict]:
    """最小限のサンプルデータを作成"""
    data = [
        {
            "text": "### Human: Pythonでリストを逆順にする方法は？\n### Assistant: リストを逆順にする方法は3つあります：\n1. `reversed()`: `list(reversed(my_list))`\n2. スライス: `my_list[::-1]`\n3. `reverse()`: `my_list.reverse()` (元のリストを変更)"
        },
        {
            "text": "### Human: gitでコミットを取り消すには？\n### Assistant: gitでコミットを取り消す方法：\n- `git reset --soft HEAD~1`: コミットのみ取り消し\n- `git reset --hard HEAD~1`: 変更ごと取り消し\n- `git commit --amend`: 直前のコミットを修正"
        },
        {
            "text": "### Human: Dockerコンテナが起動しない\n### Assistant: 確認事項：\n1. `docker logs <container_id>`: ログ確認\n2. `docker ps -a`: コンテナ状態確認\n3. Dockerfileのエントリーポイント確認"
        },
        {
            "text": "### Human: TypeError: 'NoneType' object is not iterable\n### Assistant: Noneに対して繰り返し処理を行おうとした時のエラーです。\n対処法：\n1. 変数がNoneでないか確認: `if data is not None:`\n2. デフォルト値を設定: `data = data or []`"
        },
        {
            "text": "### Human: APIのレスポンスが遅い\n### Assistant: APIレスポンスの改善方法：\n1. キャッシュの実装（Redis等）\n2. データベースクエリの最適化\n3. ページネーションの導入\n4. 非同期処理の活用"
        }
    ]
    return data

def fine_tune_with_mlx(data_path: str, output_path: str, iterations: int = 100, model_name: str = None):
    """MLXを使用したfine-tuning"""
    print_status("MLXでのfine-tuning開始", "info")
    
    # デフォルトモデルの選択（メモリに応じて）
    if model_name is None:
        # 利用可能なMLXモデル
        available_models = {
            "small": "mlx-community/Qwen2.5-1.5B-Instruct-4bit",  # 1.5B - 最小
            "medium": "mlx-community/Qwen2.5-3B-Instruct-4bit",   # 3B - バランス
            "large": "mlx-community/Mistral-7B-Instruct-v0.2-4bit" # 7B - 高品質
        }
        
        # デフォルトは小さいモデル
        model_name = available_models["small"]
        print_status(f"使用モデル: {model_name}", "info")
    
    # MLXコマンドの構築（正しいオプション）
    cmd = f"""
python -m mlx_lm.lora \\
    --model {model_name} \\
    --train \\
    --data {data_path} \\
    --adapter-path {output_path} \\
    --iters {iterations} \\
    --batch-size 1 \\
    --learning-rate 1e-4
"""
    
    print(f"\n実行コマンド:\n{cmd}")
    print_status("注: MLXのインストールが必要です。エラーが出た場合は以下を実行してください:", "warning")
    print("pip install mlx mlx-lm")
    
    # 実際の実行はサブプロセスで
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print_status("Fine-tuning完了！", "success")
    else:
        print_status(f"エラー: {result.stderr}", "error")
        print_status("代替案: PyTorchを使用したfine-tuningを試してください (--method pytorch)", "info")
        return False
    
    return True

def fine_tune_with_pytorch(data: List[Dict], model_name: str, output_dir: str):
    """PyTorch + PEFTを使用したfine-tuning（代替手法）"""
    print_status("PyTorch + PEFTでのfine-tuning開始", "info")
    
    try:
        import torch
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            TrainingArguments,
            Trainer,
            DataCollatorForLanguageModeling
        )
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
        from datasets import Dataset
        
        # デバイス設定
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        print_status(f"使用デバイス: {device}", "info")
        
        # モデルとトークナイザーの読み込み
        print_status("モデル読み込み中...", "info")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            load_in_8bit=True if device == "cpu" else False,
            device_map="auto",
            trust_remote_code=True
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.pad_token = tokenizer.eos_token
        
        # LoRA設定
        peft_config = LoraConfig(
            r=8,
            lora_alpha=16,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.1,
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        # モデルの準備
        model = prepare_model_for_kbit_training(model)
        model = get_peft_model(model, peft_config)
        
        # データセットの準備
        def tokenize_function(examples):
            return tokenizer(examples["text"], padding=True, truncation=True, max_length=512)
        
        dataset = Dataset.from_list(data)
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        
        # トレーニング引数
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=3,
            per_device_train_batch_size=1,
            gradient_accumulation_steps=4,
            warmup_steps=10,
            logging_steps=10,
            save_steps=50,
            eval_steps=50,
            save_total_limit=2,
            load_best_model_at_end=True,
            fp16=False,  # MPSではFP16非対応
            push_to_hub=False,
        )
        
        # データコレーター
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False,
        )
        
        # トレーナー
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset,
            data_collator=data_collator,
        )
        
        # トレーニング実行
        print_status("トレーニング開始（これには時間がかかります）...", "warning")
        start_time = time.time()
        trainer.train()
        end_time = time.time()
        
        print_status(f"トレーニング完了！ 所要時間: {end_time - start_time:.2f}秒", "success")
        
        # モデルの保存
        model.save_pretrained(output_dir)
        tokenizer.save_pretrained(output_dir)
        
        return True
        
    except Exception as e:
        print_status(f"エラー: {str(e)}", "error")
        return False

def convert_to_gguf(model_path: str, output_path: str):
    """モデルをGGUF形式に変換（Ollama用）"""
    print_status("GGUF形式への変換", "info")
    
    # 変換コマンド（llama.cppのconvert.pyを使用）
    cmd = f"""
python convert.py {model_path} \\
    --outfile {output_path} \\
    --outtype q4_0
"""
    
    print(f"\n変換にはllama.cppのconvert.pyが必要です。")
    print(f"手動で実行してください:\n{cmd}")
    
    return True

def create_modelfile(gguf_path: str, output_path: str):
    """Ollama用のModelfileを作成"""
    content = f"""FROM {gguf_path}

SYSTEM "あなたは技術的な質問に答える親切なアシスタントです。プログラミング、エラー解決、開発ツールについて的確なアドバイスを提供します。"

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1
"""
    
    with open(output_path, 'w') as f:
        f.write(content)
    
    print_status(f"Modelfile作成: {output_path}", "success")

def main():
    parser = argparse.ArgumentParser(description='Mac Local Fine-tuning Script')
    parser.add_argument('--method', choices=['mlx', 'pytorch'], default='mlx',
                        help='Fine-tuning手法の選択')
    parser.add_argument('--model', type=str, default='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
                        help='ベースモデル（PyTorch使用時）')
    parser.add_argument('--mlx-model', type=str, choices=['small', 'medium', 'large'], default='small',
                        help='MLXモデルサイズ: small(1.5B), medium(3B), large(7B)')
    parser.add_argument('--iterations', type=int, default=100,
                        help='トレーニングイテレーション数')
    parser.add_argument('--output-dir', type=str, default='./finetuned_model',
                        help='出力ディレクトリ')
    
    args = parser.parse_args()
    
    print(f"\n{Colors.BLUE}=== Mac Local Fine-tuning Script ==={Colors.END}\n")
    
    # プラットフォームチェック
    platform_type = check_mac_platform()
    
    # 依存関係チェック
    check_dependencies()
    
    # データ準備
    print_status("トレーニングデータ準備中...", "info")
    data = create_sample_data()
    
    # データを保存
    os.makedirs(args.output_dir, exist_ok=True)
    data_path = os.path.join(args.output_dir, "training_data.jsonl")
    with open(data_path, 'w') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print_status(f"データ保存: {data_path} ({len(data)}サンプル)", "success")
    
    # Fine-tuning実行
    if args.method == 'mlx' and platform_type == 'apple_silicon':
        print_status("MLXを使用したfine-tuningを選択", "info")
        # MLXモデルサイズに応じたモデル名を取得
        mlx_models = {
            "small": "mlx-community/Qwen2.5-1.5B-Instruct-4bit",
            "medium": "mlx-community/Qwen2.5-3B-Instruct-4bit",
            "large": "mlx-community/Mistral-7B-Instruct-v0.2-4bit"
        }
        mlx_model = mlx_models.get(args.mlx_model, mlx_models["small"])
        success = fine_tune_with_mlx(data_path, args.output_dir, args.iterations, mlx_model)
    else:
        if args.method == 'mlx' and platform_type == 'intel':
            print_status("Intel MacではMLXは最適ではありません。PyTorchを使用します。", "warning")
        print_status("PyTorch + PEFTを使用したfine-tuningを選択", "info")
        success = fine_tune_with_pytorch(data, args.model, args.output_dir)
    
    if success:
        print_status("\nFine-tuning成功！", "success")
        
        # GGUF変換の案内
        print("\n" + "="*50)
        print("次のステップ:")
        print("1. モデルをGGUF形式に変換")
        print("2. Modelfileを作成")
        print("3. Ollamaでモデルを作成")
        print("\n例:")
        print(f"ollama create my-mac-model -f {args.output_dir}/Modelfile")
        
        # Modelfile作成
        modelfile_path = os.path.join(args.output_dir, "Modelfile")
        create_modelfile("./model.gguf", modelfile_path)
    else:
        print_status("Fine-tuningに失敗しました", "error")
    
    # メモリ使用量の警告
    print(f"\n{Colors.YELLOW}💡 ヒント:{Colors.END}")
    print("- Fine-tuning中は他の重いアプリケーションを閉じてください")
    print("- Activity Monitorでメモリ使用量を監視してください")
    print("- 電源に接続した状態で実行してください")
    print("- より大きなモデルにはメモリ16GB以上を推奨")

if __name__ == "__main__":
    main()