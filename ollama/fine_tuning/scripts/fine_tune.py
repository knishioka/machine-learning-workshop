#!/usr/bin/env python3
"""
Ollama モデルカスタマイゼーションスクリプト
カスタマーサポート用チャットボットの動作をカスタマイズするスクリプト
※これはプロンプトエンジニアリングであり、真のfine-tuning（モデル重みの更新）ではありません
"""

import json
import subprocess
import sys
import os
from typing import List, Dict
import argparse


def load_training_data(file_path: str) -> List[Dict]:
    """JSONLファイルからプロンプト例データを読み込む"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data


def prepare_training_prompts(data: List[Dict]) -> str:
    """プロンプト例データをOllama形式のプロンプトに変換"""
    prompts = []
    for item in data:
        instruction = item.get('instruction', '')
        input_text = item.get('input', '')
        output = item.get('output', '')
        
        if input_text:
            prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n{output}"
        else:
            prompt = f"### Instruction:\n{instruction}\n\n### Response:\n{output}"
        
        prompts.append(prompt)
    
    return "\n\n---\n\n".join(prompts)


def create_modelfile(base_model: str, training_prompts: str, model_name: str) -> str:
    """モデルカスタマイゼーション用のModelfileを作成"""
    modelfile_content = f"""FROM {base_model}

# システムプロンプト
SYSTEM あなたは親切で丁寧なカスタマーサポートアシスタントです。お客様の質問に対して、正確で分かりやすい回答を提供してください。

# パラメータ設定
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_predict 512
"""
    
    # プロンプト例を追加（Few-shot学習）
    for prompt in training_prompts.split("\n\n---\n\n"):
        user_msg = prompt.split('### Response:')[0].strip().replace('\n', ' ')
        assistant_msg = prompt.split('### Response:')[1].strip().replace('\n', ' ')
        modelfile_content += f"\nMESSAGE user {user_msg}"
        modelfile_content += f"\nMESSAGE assistant {assistant_msg}"
    
    modelfile_path = f"Modelfile.{model_name}"
    with open(modelfile_path, 'w', encoding='utf-8') as f:
        f.write(modelfile_content)
    
    return modelfile_path


def fine_tune_model(modelfile_path: str, model_name: str):
    """Ollamaを使用してモデルをカスタマイズ"""
    print(f"モデルカスタマイゼーション開始: {model_name}")
    
    try:
        # Ollamaでモデルを作成
        cmd = f"ollama create {model_name} -f {modelfile_path}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ モデルカスタマイゼーション完了: {model_name}")
            print("出力:", result.stdout)
        else:
            print(f"❌ モデルカスタマイゼーション失敗")
            print("エラー:", result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)


def test_model(model_name: str):
    """カスタマイズしたモデルをテスト"""
    test_prompts = [
        "配送にはどのくらい時間がかかりますか？",
        "返品はできますか？",
        "支払い方法を教えてください"
    ]
    
    print(f"\n🧪 モデルテスト: {model_name}")
    print("-" * 50)
    
    for prompt in test_prompts:
        print(f"\n質問: {prompt}")
        cmd = f'ollama run {model_name} "{prompt}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"回答: {result.stdout.strip()}")
        print("-" * 50)


def main():
    parser = argparse.ArgumentParser(description='Ollama モデルカスタマイゼーションスクリプト')
    parser.add_argument('--data', type=str, default='training_data.jsonl',
                        help='プロンプト例データのJSONLファイルパス')
    parser.add_argument('--base-model', type=str, default='llama3.2:1b',
                        help='ベースとなるOllamaモデル')
    parser.add_argument('--model-name', type=str, default='customer-support',
                        help='作成するモデルの名前')
    parser.add_argument('--test', action='store_true',
                        help='カスタマイゼーション後にモデルをテスト')
    
    args = parser.parse_args()
    
    # プロンプト例データを読み込む
    print(f"📚 プロンプト例データを読み込み中: {args.data}")
    training_data = load_training_data(args.data)
    print(f"✅ {len(training_data)}件のデータを読み込みました")
    
    # プロンプトを準備
    print("\n📝 プロンプト例を準備中...")
    training_prompts = prepare_training_prompts(training_data)
    
    # Modelfileを作成
    print("\n📄 Modelfileを作成中...")
    modelfile_path = create_modelfile(args.base_model, training_prompts, args.model_name)
    print(f"✅ Modelfileを作成しました: {modelfile_path}")
    
    # モデルカスタマイゼーションを実行
    print(f"\n🚀 モデルカスタマイゼーションを開始します...")
    fine_tune_model(modelfile_path, args.model_name)
    
    # テストを実行
    if args.test:
        test_model(args.model_name)
    
    print(f"\n✨ 完了！カスタマイズされたモデル '{args.model_name}' が作成されました。")
    print(f"使用方法: ollama run {args.model_name}")


if __name__ == "__main__":
    main()