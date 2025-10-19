#!/usr/bin/env python3
"""
Claude Agent SDK - 実用編 Example 1: Project Analyzer

プロジェクト構造を自動分析し、詳細なレポートを生成します。
ファイル操作ツール（Glob, Read）を活用したデモです。

実行方法:
    python examples/02_practical/project_analyzer.py [対象ディレクトリ]

    # 例: カレントディレクトリを分析
    python examples/02_practical/project_analyzer.py .

    # 例: 特定のディレクトリを分析
    python examples/02_practical/project_analyzer.py /path/to/project

期待される動作:
    1. プロジェクト内のファイルを検索
    2. ファイル構造を分析
    3. 主要なファイルの内容を読み取り
    4. 分析レポートを生成・保存
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from claude_agent_sdk.types import AssistantMessage, TextBlock, ToolUseBlock, ResultMessage
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


async def analyze_project(target_dir: str = "."):
    """
    プロジェクト構造を分析

    このデモで使用されるツール:
    - Glob: ファイルパターンマッチング（*.py, *.js など）
    - Read: ファイル内容の読み取り
    - (オプション) Write: レポートファイルの書き込み

    Args:
        target_dir: 分析対象のディレクトリパス
    """

    console.print(Panel.fit(
        "[bold cyan]Claude Agent SDK - Project Analyzer[/bold cyan]\n"
        f"対象ディレクトリ: {target_dir}",
        border_style="cyan"
    ))
    console.print()

    # エージェントへのタスク指示
    task = f"""
    以下のディレクトリを分析して、プロジェクト構造レポートを作成してください:

    対象ディレクトリ: {target_dir}

    タスク:
    1. Python ファイル（*.py）を検索して一覧化
    2. 各ファイルの行数をカウント
    3. 主要なファイル（README.md, setup.py, requirements.txt など）の有無を確認
    4. プロジェクトの主要な特徴を分析
    5. 分析結果を構造化されたレポートにまとめる

    注意事項:
    - venv, __pycache__, .git などの不要なディレクトリは除外
    - ファイル数が多い場合は、主要なファイルのみを詳細分析

    最終的に、以下の形式でレポートを提示してください:
    - プロジェクト概要
    - ファイル統計
    - ディレクトリ構造
    - 主要ファイルの説明
    - 推奨事項（あれば）
    """

    console.print("[yellow]📝 分析タスクを実行中...[/yellow]")
    console.print()

    # ツール使用状況の追跡
    tools_used = set()

    # オプション設定
    options = ClaudeAgentOptions(
        allowed_tools=["Glob", "Read"],  # 使用を許可するツール
        cwd=target_dir,  # 作業ディレクトリ
    )

    # エージェント実行
    async with ClaudeSDKClient(options=options) as client:
        await client.query(task)

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        # テキスト出力（簡潔に表示）
                        text = block.text
                        if len(text) > 100:
                            console.print(f"[dim]💬 {text[:100]}...[/dim]")
                        else:
                            console.print(f"[dim]💬 {text}[/dim]")

                    elif isinstance(block, ToolUseBlock):
                        # ツール使用の記録
                        tools_used.add(block.name)
                        console.print(f"[blue]🔧 {block.name} を使用中...[/blue]")

            elif isinstance(message, ResultMessage):
                # 最終結果を表示
                if message.result:
                    console.print()
                    console.print(Panel(
                        f"[bold green]{message.result}[/bold green]",
                        title="📊 分析レポート",
                        border_style="green"
                    ))

                # トークン使用量と費用を表示
                print_usage_stats(message)

    # 使用されたツールの一覧
    console.print()
    if tools_used:
        console.print(Panel.fit(
            f"[bold]使用されたツール[/bold]\n\n" +
            "\n".join(f"• {tool}" for tool in sorted(tools_used)),
            title="🔧 ツール統計",
            border_style="blue"
        ))

    console.print()
    console.print("[bold green]✅ 分析完了！[/bold green]")
    console.print()
    console.print("[yellow]💡 このデモで学べたこと:[/yellow]")
    console.print("  • Glob ツールでファイル検索")
    console.print("  • Read ツールでファイル読み取り")
    console.print("  • allowed_tools で権限管理")
    console.print("  • cwd でディレクトリ指定")
    console.print("  • 複雑なタスクの自動化")


def main():
    """
    メイン関数: コマンドライン引数を処理してプロジェクト分析を実行
    """

    # 環境変数チェック
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[bold red]❌ エラー: ANTHROPIC_API_KEY が設定されていません[/bold red]")
        console.print("   .env ファイルを作成し、APIキーを設定してください")
        exit(1)

    # 対象ディレクトリの取得
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = "."

    # ディレクトリの存在確認
    if not os.path.isdir(target_dir):
        console.print(f"[bold red]❌ エラー: ディレクトリが見つかりません: {target_dir}[/bold red]")
        exit(1)

    # 分析実行
    asyncio.run(analyze_project(target_dir))


if __name__ == "__main__":
    main()
