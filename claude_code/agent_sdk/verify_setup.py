#!/usr/bin/env python3
"""
セットアップ検証スクリプト

このスクリプトは、Agent SDKデモプロジェクトが正しくセットアップされているか確認します。
APIキーなしでも実行可能です。

実行方法:
    python verify_setup.py
"""

import sys
import os
from pathlib import Path


def print_header(title):
    """ヘッダー出力"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def check_python_version():
    """Pythonバージョンチェック"""
    print_header("1. Pythonバージョン確認")

    version = sys.version_info
    print(f"Pythonバージョン: {version.major}.{version.minor}.{version.micro}")

    if version.major >= 3 and version.minor >= 8:
        print("✅ OK: Python 3.8以上")
        return True
    else:
        print("❌ NG: Python 3.8以上が必要です")
        return False


def check_files():
    """必要なファイルの存在確認"""
    print_header("2. プロジェクトファイル確認")

    required_files = [
        "README.md",
        "QUICKSTART.md",
        "requirements.txt",
        ".env.example",
        "examples/01_basic/hello_agent.py",
        "examples/01_basic/streaming_demo.py",
        "examples/02_practical/project_analyzer.py",
        "examples/02_practical/readme_generator.py",
        "examples/03_advanced/research_agent.py",
        "examples/03_advanced/code_reviewer.py",
        "examples/04_mcp/mcp_example.py",
        "demo/run_all_demos.py",
        "docs/PRESENTATION.md",
        "docs/ARCHITECTURE.md",
    ]

    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} が見つかりません")
            all_exist = False

    if all_exist:
        print(f"\n✅ OK: 全{len(required_files)}ファイル存在")
    else:
        print("\n❌ NG: 一部のファイルが見つかりません")

    return all_exist


def check_syntax():
    """Pythonファイルの構文チェック"""
    print_header("3. Python構文チェック")

    python_files = [
        "examples/01_basic/hello_agent.py",
        "examples/01_basic/streaming_demo.py",
        "examples/02_practical/project_analyzer.py",
        "examples/02_practical/readme_generator.py",
        "examples/03_advanced/research_agent.py",
        "examples/03_advanced/code_reviewer.py",
        "examples/04_mcp/mcp_example.py",
        "demo/run_all_demos.py",
    ]

    all_valid = True
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                compile(f.read(), file_path, 'exec')
            print(f"✅ {file_path}")
        except SyntaxError as e:
            print(f"❌ {file_path}: {e}")
            all_valid = False

    if all_valid:
        print(f"\n✅ OK: 全{len(python_files)}ファイルの構文が正しい")
    else:
        print("\n❌ NG: 構文エラーがあります")

    return all_valid


def check_dependencies():
    """依存パッケージのチェック"""
    print_header("4. 依存パッケージ確認")

    packages = {
        'claude_agent_sdk': 'claude-agent-sdk',
        'dotenv': 'python-dotenv',
        'rich': 'rich',
    }

    all_installed = True
    for module_name, package_name in packages.items():
        try:
            __import__(module_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"⚠️  {package_name} (未インストール)")
            all_installed = False

    if all_installed:
        print("\n✅ OK: すべてのパッケージがインストール済み")
    else:
        print("\n⚠️  一部のパッケージが未インストール")
        print("   以下のコマンドでインストールしてください:")
        print("   pip install -r requirements.txt")

    return all_installed


def check_env_file():
    """環境変数ファイルのチェック"""
    print_header("5. 環境設定ファイル確認")

    if os.path.exists('.env'):
        print("✅ .env ファイルが存在します")

        # APIキーの設定確認（値は表示しない）
        with open('.env', 'r') as f:
            content = f.read()
            if 'ANTHROPIC_API_KEY' in content:
                if 'your_api_key_here' in content or 'sk-ant-' not in content:
                    print("⚠️  ANTHROPIC_API_KEY が未設定の可能性があります")
                    print("   実際のAPIキーを設定してください")
                    return False
                else:
                    print("✅ ANTHROPIC_API_KEY が設定されています")
                    return True
            else:
                print("❌ ANTHROPIC_API_KEY が見つかりません")
                return False
    else:
        print("⚠️  .env ファイルが見つかりません")
        print("   以下のコマンドで作成してください:")
        print("   cp .env.example .env")
        print("   その後、.envファイルを編集してAPIキーを設定")
        return False


def print_summary(results):
    """結果サマリー"""
    print_header("検証結果サマリー")

    checks = [
        ("Pythonバージョン", results['python']),
        ("プロジェクトファイル", results['files']),
        ("Python構文", results['syntax']),
        ("依存パッケージ", results['dependencies']),
        ("環境設定", results['env']),
    ]

    for check_name, result in checks:
        status = "✅ OK" if result else "❌ NG"
        print(f"{status:8} {check_name}")

    print()

    all_ok = all(results.values())

    if all_ok:
        print("🎉 すべての検証に合格しました！")
        print("\n次のステップ:")
        print("  python examples/01_basic/hello_agent.py")
        print("\n詳細は QUICKSTART.md を参照してください")
        return 0
    else:
        print("⚠️  いくつかの問題があります")
        print("\n対処方法:")
        if not results['dependencies']:
            print("  1. pip install -r requirements.txt")
        if not results['env']:
            print("  2. cp .env.example .env")
            print("  3. .env を編集してAPIキーを設定")
        print("\n詳細は QUICKSTART.md を参照してください")
        return 1


def main():
    """メイン関数"""
    print("\n" + "=" * 60)
    print("  Claude Agent SDK デモプロジェクト - セットアップ検証")
    print("=" * 60)

    results = {
        'python': check_python_version(),
        'files': check_files(),
        'syntax': check_syntax(),
        'dependencies': check_dependencies(),
        'env': check_env_file(),
    }

    return print_summary(results)


if __name__ == "__main__":
    sys.exit(main())
