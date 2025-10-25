#!/usr/bin/env python3
"""
Claude Agent SDK - Context7 MCP連携編: リアルタイムドキュメント取得

Context7 MCPサーバーを使用して、最新のライブラリドキュメントを
リアルタイムで取得し、AIエージェントに統合するデモです。

Context7について:
Context7は、AIエージェントに最新のバージョン固有のドキュメントと
コード例を動的に提供するMCPサーバーです。古いドキュメントや存在しない
APIの問題を解決します。

実行方法:
    python examples/04_mcp/mcp_example.py

    注: このデモを実行するには、Context7 MCPサーバーのインストールが必要です。
        インストールコマンド: npx -y @smithery/cli install @upstash/context7-mcp --client claude

期待される動作:
    1. Context7 MCPサーバーに接続
    2. 複数のライブラリのドキュメントをリクエスト
    3. 最新のドキュメントと使用例を取得
    4. 結果を整形して表示
"""

import asyncio
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import ResultMessage
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
load_dotenv()


def print_usage_stats(result_message):
    """トークン使用量と費用を表示"""
    if not result_message.usage:
        return

    usage = result_message.usage

    # テーブルを作成
    table = Table(title="💰 トークン使用量と費用")
    table.add_column("項目", style="cyan")
    table.add_column("値", justify="right", style="yellow")

    # トークン数
    table.add_row("入力トークン", f"{usage.get('input_tokens', 0):,}")

    if usage.get('cache_read_input_tokens'):
        table.add_row("キャッシュ読取", f"{usage.get('cache_read_input_tokens', 0):,}")

    if usage.get('cache_creation_input_tokens'):
        table.add_row("キャッシュ作成", f"{usage.get('cache_creation_input_tokens', 0):,}")

    table.add_row("出力トークン", f"{usage.get('output_tokens', 0):,}")

    total_tokens = (
        usage.get('input_tokens', 0) +
        usage.get('cache_read_input_tokens', 0) +
        usage.get('cache_creation_input_tokens', 0) +
        usage.get('output_tokens', 0)
    )
    table.add_row("", "", end_section=True)
    table.add_row("合計トークン", f"{total_tokens:,}", style="bold")

    # 費用
    if result_message.total_cost_usd:
        table.add_row("", "", end_section=True)
        table.add_row("総コスト (USD)", f"${result_message.total_cost_usd:.6f}", style="bold green")

    console.print()
    console.print(table)


async def demonstrate_context7():
    """
    Context7 MCP連携のデモ

    このデモで学べること:
    - Context7 MCPの基本概念
    - リアルタイムドキュメント取得
    - 最新のライブラリドキュメントの活用
    - バージョン固有のコード例の取得
    """

    console.print(Panel.fit(
        "[bold cyan]Claude Agent SDK - Context7 MCP Demo[/bold cyan]\n"
        "リアルタイムで最新のライブラリドキュメントを取得",
        border_style="cyan"
    ))
    console.print()

    # MCP設定ファイルの確認
    config_path = Path(__file__).parent / "mcp_config.json"
    if not config_path.exists():
        console.print("[yellow]⚠️  MCP設定ファイルが見つかりません[/yellow]")
        console.print(f"   期待されるパス: {config_path}")
        console.print()
        console.print("[cyan]📘 Context7について[/cyan]")
        demonstrate_context7_concept()
        return

    # 設定ファイルの読み込み
    with open(config_path, 'r') as f:
        mcp_config = json.load(f)

    console.print("[green]✅ Context7 MCP設定ファイルを読み込みました[/green]")
    console.print()

    # Context7の基本概念を説明
    demonstrate_context7_concept()
    console.print()

    # Context7を使用したドキュメント取得タスク
    task = """
    Context7 MCPサーバーを使用して、以下のライブラリの最新ドキュメントを取得してください:

    1. Next.js 14 - App Routerとサーバーコンポーネントについて
    2. React 18 - Hooksの使い方（特にuseStateとuseEffect）について

    各ライブラリについて:
    - resolve-library-idツールを使ってライブラリIDを解決
    - get-library-docsツールを使って最新のドキュメントを取得
    - 主要な機能と使用例を簡潔にまとめる（各100文字程度）

    use context7
    """

    console.print("[yellow]📚 Context7でドキュメントを取得中...[/yellow]")
    console.print()

    # エージェント実行
    try:
        # Context7 MCPサーバーの設定
        options = ClaudeAgentOptions(
            mcp_servers={
                "context7": {
                    "command": "npx",
                    "args": ["-y", "@upstash/context7-mcp"]
                }
            },
            permission_mode="bypassPermissions"  # デモのためツールを自動承認
        )

        # または、設定ファイルのパスを渡す（代替方法）
        # options = ClaudeAgentOptions(mcp_servers=config_path)

        async for message in query(prompt=task, options=options):
            if isinstance(message, ResultMessage):
                console.print()
                console.print(Panel(
                    f"[bold green]{message.result}[/bold green]",
                    title="📊 取得したドキュメント情報",
                    border_style="green"
                ))

                # トークン使用量と費用を表示
                print_usage_stats(message)

            elif hasattr(message, 'type') and message.type == "tool_use":
                tool_name = getattr(message, 'tool_name', 'unknown')
                console.print(f"[blue]🔧 Context7ツール使用: {tool_name}[/blue]")

            elif hasattr(message, 'type') and message.type == "thinking":
                content = message.content[:80]
                if len(message.content) > 80:
                    content += "..."
                console.print(f"[dim]💭 {content}[/dim]")

    except Exception as e:
        console.print(f"[yellow]⚠️  エラー: {str(e)}[/yellow]")
        console.print()
        console.print("[cyan]💡 考えられる原因:[/cyan]")
        console.print("   1. Node.js 18+ がインストールされていない")
        console.print("   2. npx が利用できない")
        console.print("   3. Context7 MCPサーバーのインストールエラー")
        console.print()
        console.print("[cyan]セットアップ方法:[/cyan]")
        console.print("   # Node.jsの確認")
        console.print("   node --version  # 18以上が必要")
        console.print()
        console.print("   # Context7のクイックインストール（オプション）")
        console.print("   npx -y @smithery/cli install @upstash/context7-mcp --client claude")

    console.print()
    console.print("[yellow]💡 このデモで学べること:[/yellow]")
    console.print("  • Context7 MCPの活用方法")
    console.print("  • リアルタイムドキュメント取得")
    console.print("  • 最新のコード例の取得")
    console.print("  • 古いAPIドキュメントの問題解決")


def demonstrate_context7_concept():
    """
    Context7の概念を視覚的に説明
    """

    console.print(Panel(
        """[bold]Context7 MCP とは？[/bold]

Context7は、AIエージェントに最新のバージョン固有のドキュメントと
コード例を動的に提供するMCPサーバーです。

[cyan]解決する問題:[/cyan]
• 古いトレーニングデータによる古いコード生成
• 存在しないAPIの幻覚
• バージョン不一致によるエラー
• ドキュメント検索の手間

[cyan]主な機能:[/cyan]
1. リアルタイムドキュメント取得
2. バージョン固有のコード例
3. 最新のAPI仕様
4. プロンプトへの自動統合

[cyan]使い方:[/cyan]
プロンプトに "use context7" を追加するだけ！
例: "Next.js 14でルーティングを実装 use context7"
        """,
        title="📘 Context7の基礎知識",
        border_style="blue"
    ))
    console.print()

    # Context7が提供するツールを表形式で表示
    table = Table(title="🔧 Context7が提供するツール")
    table.add_column("ツール名", style="cyan")
    table.add_column("用途", style="green")
    table.add_column("パラメータ", style="yellow")

    table.add_row(
        "resolve-library-id",
        "ライブラリ名を\nContext7 IDに変換",
        "libraryName (必須)"
    )
    table.add_row(
        "get-library-docs",
        "ライブラリの\nドキュメントを取得",
        "libraryId (必須)\ntopic (オプション)\ntokens (オプション)"
    )

    console.print(table)
    console.print()

    # サポートされているライブラリの例
    libs_table = Table(title="📚 サポートされているライブラリ例")
    libs_table.add_column("カテゴリ", style="cyan")
    libs_table.add_column("ライブラリ", style="green")

    libs_table.add_row("JavaScript", "Next.js, React, Vue, Node.js")
    libs_table.add_row("Python", "FastAPI, Django, Flask, Pandas")
    libs_table.add_row("その他", "TypeScript, Tailwind CSS, など多数")

    console.print(libs_table)


async def show_context7_setup_guide():
    """
    Context7セットアップガイドの表示
    """

    console.print()
    console.print(Panel(
        """[bold cyan]Context7 セットアップガイド[/bold cyan]

[bold]方法1: クイックインストール（推奨）[/bold]
```bash
npx -y @smithery/cli install @upstash/context7-mcp --client claude
```

[bold]方法2: マニュアル設定[/bold]
Claude Desktop、Cursor、VS Codeなどの設定ファイルを編集:

macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\\Claude\\claude_desktop_config.json

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

[bold]方法3: 他のランタイム[/bold]
Bun: bunx -y @upstash/context7-mcp
Deno: deno run --allow-all npm:@upstash/context7-mcp

[bold]使い方[/bold]
プロンプトに "use context7" を追加:
"Next.js 14でApp Routerを使用 use context7"

詳細: https://glama.ai/mcp/servers/@upstash/context7-mcp
        """,
        border_style="green"
    ))


def main():
    """
    メイン関数
    """

    # 環境変数チェック
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[bold red]❌ エラー: ANTHROPIC_API_KEY が設定されていません[/bold red]")
        console.print("   .env ファイルを作成し、APIキーを設定してください")
        exit(1)

    # デモ実行
    asyncio.run(demonstrate_context7())

    # セットアップガイドの表示
    console.print()
    try:
        response = console.input("[cyan]Context7セットアップガイドを表示しますか？ (y/N): [/cyan]").lower()
        if response == 'y':
            asyncio.run(show_context7_setup_guide())
    except (EOFError, KeyboardInterrupt):
        # 自動実行時やCtrl+C時はスキップ
        pass


if __name__ == "__main__":
    main()
