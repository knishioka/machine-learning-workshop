#!/usr/bin/env python3
"""
Claude Agent SDK - 基本編 Example 1: Hello Agent

最もシンプルなAgent SDKの使い方を学びます。
このスクリプトは、エージェントに簡単な計算タスクを依頼し、
その結果を受け取る基本的なフローを示します。

実行方法:
    python examples/01_basic/hello_agent.py

期待される動作:
    1. エージェントが質問を理解
    2. 計算を実行
    3. 結果を返却
"""

import asyncio
import os
from dotenv import load_dotenv
from claude_agent_sdk import query
from claude_agent_sdk.types import ResultMessage, AssistantMessage, SystemMessage

# 環境変数を読み込み（.envファイルからAPI_KEYを取得）
load_dotenv()


async def main():
    """
    最もシンプルなエージェント実行例

    Agent SDKの基本概念:
    - query(): エージェントにタスクを依頼する最もシンプルなインターフェース
    - 非同期ストリーミング: async for でリアルタイムにメッセージを受信
    - メッセージタイプ: result, thinking, tool_use など様々なタイプがある
    """

    print("=" * 60)
    print("Claude Agent SDK - Hello Agent デモ")
    print("=" * 60)
    print()
    print("エージェントに簡単な計算タスクを依頼します...")
    print()

    # エージェントにタスクを依頼
    # query()関数は非同期ストリーミングで結果を返します
    async for message in query(prompt="What is 2 + 2? Please calculate and explain."):
        # メッセージタイプによって処理を分岐（isinstance でチェック）
        if isinstance(message, ResultMessage):
            # 最終結果を表示
            print("🎯 エージェントの回答:")
            print("-" * 60)
            print(message.result)
            print("-" * 60)
        elif isinstance(message, AssistantMessage):
            # エージェントからのメッセージ（思考過程や回答）
            for block in message.content:
                if hasattr(block, 'text'):
                    print(f"💭 {block.text[:50]}...")
        elif isinstance(message, SystemMessage):
            # システムメッセージ（初期化など）
            pass  # 基本編ではスキップ

    print()
    print("✅ デモ完了！")
    print()
    print("次のステップ:")
    print("  - streaming_demo.py でストリーミングの詳細を学ぶ")
    print("  - examples/02_practical/ で実用的な例を試す")


if __name__ == "__main__":
    # 環境変数チェック
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ エラー: ANTHROPIC_API_KEY が設定されていません")
        print("   .env ファイルを作成し、APIキーを設定してください")
        print("   詳細: README.md を参照")
        exit(1)

    # 非同期メイン関数を実行
    asyncio.run(main())
