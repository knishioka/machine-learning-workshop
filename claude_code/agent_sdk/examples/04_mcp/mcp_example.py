#!/usr/bin/env python3
"""
Claude Agent SDK - MCP連携編: Model Context Protocol Integration

MCP（Model Context Protocol）を使用して、外部サービスと連携する
拡張可能なエージェントのデモです。

MCPについて:
MCPは、AIエージェントが外部ツールやデータソースと標準化された
方法で連携するためのプロトコルです。これにより、エージェントに
カスタム機能を簡単に追加できます。

実行方法:
    python examples/04_mcp/mcp_example.py

    注: このデモを実行するには、MCPサーバーの設定が必要です。
        詳細は README.md を参照してください。

期待される動作:
    1. MCPサーバーに接続
    2. 利用可能なツールを確認
    3. MCPツールを使用してタスクを実行
    4. 結果を表示
"""

import asyncio
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from claude_agent_sdk import query
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


async def demonstrate_mcp():
    """
    MCP連携のデモ

    このデモで学べること:
    - MCPの基本概念
    - MCPサーバーとの連携方法
    - カスタムツールの追加
    - 拡張可能なエージェント設計
    """

    console.print(Panel.fit(
        "[bold cyan]Claude Agent SDK - MCP Integration Demo[/bold cyan]\n"
        "Model Context Protocolを使用した拡張性のデモ",
        border_style="cyan"
    ))
    console.print()

    # MCP設定ファイルの確認
    config_path = Path(__file__).parent / "mcp_config.json"
    if not config_path.exists():
        console.print("[yellow]⚠️  MCP設定ファイルが見つかりません[/yellow]")
        console.print(f"   期待されるパス: {config_path}")
        console.print()
        console.print("[cyan]📘 MCPについて[/cyan]")
        demonstrate_mcp_concept()
        return

    # 設定ファイルの読み込み
    with open(config_path, 'r') as f:
        mcp_config = json.load(f)

    console.print("[green]✅ MCP設定ファイルを読み込みました[/green]")
    console.print()

    # MCPの基本概念を説明
    demonstrate_mcp_concept()
    console.print()

    # サンプルタスク（MCPサーバーの例として、ファイルシステムサーバーを想定）
    task = """
    MCPを使用して以下のタスクを実行してください:

    1. 利用可能なMCPツールを確認
    2. これらのツールを使用してサンプルタスクを実行
    3. 実行結果を報告

    注: 実際のMCPサーバーが設定されていない場合は、
        どのようなツールが利用可能になるかを説明してください。
    """

    console.print("[yellow]🔧 MCPタスクを実行中...[/yellow]")
    console.print()

    # エージェント実行
    try:
        async for message in query(
            prompt=task,
            options={
                # MCP設定を渡す（実際のSDKの仕様に合わせて調整）
                # "mcp_servers": mcp_config.get("mcpServers", {}),
            }
        ):
            if isinstance(message, ResultMessage):
                console.print()
                console.print(Panel(
                    f"[bold green]{message.result}[/bold green]",
                    title="📊 実行結果",
                    border_style="green"
                ))

                # トークン使用量と費用を表示
                print_usage_stats(message)

            elif hasattr(message, 'type') and message.type == "tool_use":
                tool_name = getattr(message, 'tool_name', 'unknown')
                console.print(f"[blue]🔧 ツール使用: {tool_name}[/blue]")

            elif message.type == "thinking":
                content = message.content[:80]
                if len(message.content) > 80:
                    content += "..."
                console.print(f"[dim]💭 {content}[/dim]")

    except Exception as e:
        console.print(f"[yellow]⚠️  {str(e)}[/yellow]")
        console.print()
        console.print("[cyan]💡 これは正常です。MCPサーバーが設定されていない場合、")
        console.print("   このようなエラーが発生します。[/cyan]")

    console.print()
    console.print("[yellow]💡 このデモで学べること:[/yellow]")
    console.print("  • MCPの基本概念と利点")
    console.print("  • MCPサーバーの設定方法")
    console.print("  • カスタムツールの追加")
    console.print("  • エージェントの拡張性")


def demonstrate_mcp_concept():
    """
    MCPの概念を視覚的に説明
    """

    console.print(Panel(
        """[bold]Model Context Protocol (MCP) とは？[/bold]

MCPは、AIエージェントが外部ツールやデータソースと
標準化された方法で連携するためのプロトコルです。

[cyan]主な利点:[/cyan]
1. 標準化: 統一されたインターフェース
2. 拡張性: 簡単にツール追加
3. 再利用性: MCPサーバーは複数のエージェントで共有
4. セキュリティ: 権限管理が明確

[cyan]活用例:[/cyan]
• データベース接続（PostgreSQL, MongoDB など）
• 外部API連携（GitHub, Slack, Notion など）
• カスタムビジネスロジック
• 社内システム統合
        """,
        title="📘 MCPの基礎知識",
        border_style="blue"
    ))
    console.print()

    # MCPサーバーの例を表形式で表示
    table = Table(title="🔌 よく使われるMCPサーバーの例")
    table.add_column("サーバー名", style="cyan")
    table.add_column("用途", style="green")
    table.add_column("提供ツール例", style="yellow")

    table.add_row(
        "filesystem",
        "ファイルシステム操作",
        "read_file, write_file, list_directory"
    )
    table.add_row(
        "github",
        "GitHub連携",
        "create_pr, list_issues, comment"
    )
    table.add_row(
        "database",
        "データベース操作",
        "query, insert, update"
    )
    table.add_row(
        "slack",
        "Slack連携",
        "send_message, list_channels"
    )
    table.add_row(
        "custom",
        "カスタムツール",
        "あなたのビジネスロジック"
    )

    console.print(table)


async def show_mcp_setup_guide():
    """
    MCPセットアップガイドの表示
    """

    console.print()
    console.print(Panel(
        """[bold cyan]MCP セットアップガイド[/bold cyan]

[bold]ステップ1: MCPサーバーの選択[/bold]
公式のMCPサーバーリポジトリから選択:
https://github.com/modelcontextprotocol/servers

[bold]ステップ2: MCPサーバーのインストール[/bold]
```bash
# 例: ファイルシステムサーバー
npm install -g @modelcontextprotocol/server-filesystem
```

[bold]ステップ3: 設定ファイルの更新[/bold]
mcp_config.json に追加:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    }
  }
}
```

[bold]ステップ4: エージェントの実行[/bold]
```bash
python examples/04_mcp/mcp_example.py
```

詳細は README.md を参照してください。
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
    asyncio.run(demonstrate_mcp())

    # セットアップガイドの表示
    console.print()
    if console.input("[cyan]MCPセットアップガイドを表示しますか？ (y/N): [/cyan]").lower() == 'y':
        asyncio.run(show_mcp_setup_guide())


if __name__ == "__main__":
    main()
