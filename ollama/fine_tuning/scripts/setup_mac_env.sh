#!/bin/bash
# Mac環境でのfine-tuningセットアップスクリプト

echo "🍎 Mac Fine-tuning環境セットアップ"
echo "=================================="

# OSチェック
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ このスクリプトはmacOS専用です"
    exit 1
fi

# アーキテクチャチェック
ARCH=$(uname -m)
if [[ "$ARCH" == "arm64" ]]; then
    echo "✅ Apple Silicon Mac検出"
    IS_APPLE_SILICON=true
else
    echo "⚠️  Intel Mac検出 - パフォーマンスが制限されます"
    IS_APPLE_SILICON=false
fi

# Homebrewチェック
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrewがインストールされていません"
    echo "インストール: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

# Python環境チェック
echo ""
echo "📦 Python環境チェック..."
if ! command -v python3 &> /dev/null; then
    echo "Python3をインストールしています..."
    brew install python@3.10
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Python version: $PYTHON_VERSION"

# 仮想環境の作成
echo ""
echo "🔧 仮想環境セットアップ..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ 仮想環境作成完了"
fi

# 仮想環境の有効化
source venv/bin/activate

# 基本パッケージのインストール
echo ""
echo "📥 基本パッケージのインストール..."
pip install --upgrade pip setuptools wheel

# Apple Silicon向けMLXのインストール
if [ "$IS_APPLE_SILICON" = true ]; then
    echo ""
    echo "🚀 MLX (Apple Silicon最適化) をインストール..."
    pip install mlx mlx-lm
    echo "✅ MLXインストール完了"
fi

# PyTorchのインストール（Metal Performance Shaders対応）
echo ""
echo "🔥 PyTorchをインストール..."
if [ "$IS_APPLE_SILICON" = true ]; then
    # Apple Silicon向け
    pip install torch torchvision torchaudio
else
    # Intel Mac向け
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
fi

# その他の必要なパッケージ
echo ""
echo "📚 その他の必要なパッケージをインストール..."
pip install transformers datasets accelerate peft bitsandbytes scipy

# Jupyterのインストール（オプション）
echo ""
read -p "Jupyter Notebookをインストールしますか？ (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install jupyter ipykernel
    python -m ipykernel install --user --name=finetune --display-name="Fine-tuning環境"
    echo "✅ Jupyterインストール完了"
fi

# llama.cpp（GGUF変換用）のセットアップ
echo ""
echo "🦙 llama.cpp（GGUF変換用）のセットアップ..."
if [ ! -d "llama.cpp" ]; then
    git clone https://github.com/ggerganov/llama.cpp
    cd llama.cpp
    
    if [ "$IS_APPLE_SILICON" = true ]; then
        # Apple Silicon向けビルド
        make LLAMA_METAL=1
    else
        # Intel Mac向けビルド
        make
    fi
    
    cd ..
    echo "✅ llama.cppセットアップ完了"
else
    echo "⏭️  llama.cppは既にインストールされています"
fi

# 環境変数の設定
echo ""
echo "⚙️  環境変数設定..."
cat > .env << EOF
# Mac Fine-tuning環境設定
export PYTORCH_ENABLE_MPS_FALLBACK=1
export TOKENIZERS_PARALLELISM=false

# メモリ制限（必要に応じて調整）
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.7

# llama.cppパス
export LLAMA_CPP_PATH="$(pwd)/llama.cpp"
EOF

echo "✅ 環境変数設定完了"

# 最終確認
echo ""
echo "🎉 セットアップ完了！"
echo ""
echo "使用方法:"
echo "1. 仮想環境を有効化: source venv/bin/activate"
echo "2. 環境変数を読み込み: source .env"
echo "3. Fine-tuningスクリプト実行: python scripts/mac_local_fine_tuning.py"
echo ""

# システム情報の表示
echo "💻 システム情報:"
echo "- OS: $(sw_vers -productName) $(sw_vers -productVersion)"
echo "- CPU: $(sysctl -n machdep.cpu.brand_string)"
echo "- メモリ: $(( $(sysctl -n hw.memsize) / 1024 / 1024 / 1024 ))GB"

if [ "$IS_APPLE_SILICON" = true ]; then
    echo "- GPU: Apple Silicon (Metal対応)"
fi

echo ""
echo "📝 注意事項:"
echo "- Fine-tuning中は他の重いアプリケーションを閉じてください"
echo "- 電源に接続した状態で実行してください"
echo "- 発熱に注意してください（長時間の実行時）"