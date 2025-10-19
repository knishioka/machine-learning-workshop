#!/usr/bin/env python3
"""
Claude Agent SDK - 基本編 Example 2: Streaming Demo

ストリーミング動作を可視化し、エージェントの思考過程を
リアルタイムで観察します。

実行方法:
    python examples/01_basic/streaming_demo.py

期待される動作:
    1. エージェントの思考過程をリアルタイム表示
    2. ツール使用状況の可視化
    3. 最終結果の表示
"""

import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from claude_agent_sdk import query
from claude_agent_sdk.types import ResultMessage, AssistantMessage, SystemMessage, ToolUseBlock
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Richコンソールで美しい出力
console = Console()

# 環境変数を読み込み
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


async def main():
    """
    ストリーミング動作のデモ

    このデモでは、エージェントが以下を実行します:
    1. 複数の計算を実行
    2. 各ステップで思考過程を表示
    3. 最終的に結果をまとめて報告
    """

    console.print(Panel.fit(
        "[bold cyan]Claude Agent SDK - Streaming Demo[/bold cyan]\n"
        "エージェントの思考過程をリアルタイムで観察します",
        border_style="cyan"
    ))
    console.print()

    # 複雑なタスクを依頼（複数ステップの計算）
    task = """
    以下の計算を順番に実行してください:
    1. 15 × 7 を計算
    2. その結果に 23 を足す
    3. 最終結果を2で割る

    各ステップを明確に説明しながら実行してください。
    """

    console.print("[yellow]📝 タスク:[/yellow]", task.strip())
    console.print()

    # メッセージカウンター
    message_count = {
        "thinking": 0,
        "tool_use": 0,
        "result": 0,
        "other": 0
    }

    start_time = datetime.now()

    # ストリーミング実行
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task_id = progress.add_task("[cyan]処理中...", total=None)

        async for message in query(prompt=task):
            # メッセージタイプごとに処理（isinstance でチェック）
            if isinstance(message, ResultMessage):
                message_count["result"] += 1
                progress.update(task_id, description="[green]✅ 完了")
                console.print()
                console.print(Panel(
                    f"[bold green]{message.result}[/bold green]",
                    title="🎯 最終結果",
                    border_style="green"
                ))

                # トークン使用量と費用を表示
                print_usage_stats(message)

            elif isinstance(message, AssistantMessage):
                # エージェントからのメッセージ（思考や回答）
                for block in message.content:
                    if hasattr(block, 'text'):
                        message_count["thinking"] += 1
                        content = block.text
                        if len(content) > 100:
                            content = content[:100] + "..."
                        console.print(f"[dim]💭 思考: {content}[/dim]")
                    elif isinstance(block, ToolUseBlock):
                        message_count["tool_use"] += 1
                        console.print(f"[blue]🔧 ツール使用: {block.name}[/blue]")

            elif isinstance(message, SystemMessage):
                message_count["other"] += 1
                # システムメッセージはログのみ
                pass

            else:
                message_count["other"] += 1
                console.print(f"[dim]📨 その他メッセージ[/dim]")

    # 実行統計
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    console.print()
    console.print(Panel.fit(
        f"[bold]実行統計[/bold]\n\n"
        f"実行時間: {duration:.2f}秒\n"
        f"思考メッセージ: {message_count['thinking']}件\n"
        f"ツール使用: {message_count['tool_use']}件\n"
        f"結果メッセージ: {message_count['result']}件\n"
        f"その他: {message_count['other']}件",
        title="📊 統計情報",
        border_style="magenta"
    ))

    console.print()
    console.print("[bold green]✅ デモ完了！[/bold green]")
    console.print()
    console.print("[yellow]💡 ポイント:[/yellow]")
    console.print("  • ストリーミングでエージェントの思考をリアルタイム観察")
    console.print("  • 複数ステップのタスクも自律的に実行")
    console.print("  • 各メッセージタイプで異なる処理が可能")
    console.print()
    console.print("[cyan]次のステップ:[/cyan]")
    console.print("  • examples/02_practical/ で実用的なファイル操作を体験")


if __name__ == "__main__":
    # 環境変数チェック
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[bold red]❌ エラー: ANTHROPIC_API_KEY が設定されていません[/bold red]")
        console.print("   .env ファイルを作成し、APIキーを設定してください")
        console.print("   詳細: README.md を参照")
        exit(1)

    # 非同期メイン関数を実行
    asyncio.run(main())
