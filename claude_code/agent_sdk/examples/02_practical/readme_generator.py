#!/usr/bin/env python3
"""
Claude Agent SDK - 実用編 Example 2: README Generator

プロジェクトのコードを分析して、自動的に README.md を生成します。
ファイル操作ツール（Glob, Read, Write）をフル活用したデモです。

実行方法:
    python examples/02_practical/readme_generator.py [対象ディレクトリ]

    # 例: カレントディレクトリのREADME生成
    python examples/02_practical/readme_generator.py .

    # 例: 特定のディレクトリのREADME生成
    python examples/02_practical/readme_generator.py /path/to/project

期待される動作:
    1. プロジェクト内のコードファイルを検索
    2. 主要なファイルの内容を読み取り
    3. コード構造を分析
    4. README.md を自動生成
    5. ファイルに書き込み
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from claude_agent_sdk.types import AssistantMessage, TextBlock, ToolUseBlock, ResultMessage
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
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


async def generate_readme(target_dir: str = ".", output_path: str = "README_GENERATED.md"):
    """
    プロジェクトのREADMEを自動生成

    このデモで使用されるツール:
    - Glob: ソースファイルの検索
    - Read: ファイル内容の読み取り
    - Write: README.md の書き込み

    Args:
        target_dir: 対象ディレクトリ
        output_path: 生成されるREADMEのパス
    """

    console.print(Panel.fit(
        "[bold cyan]Claude Agent SDK - README Generator[/bold cyan]\n"
        f"対象: {target_dir}\n"
        f"出力: {output_path}",
        border_style="cyan"
    ))
    console.print()

    # エージェントへのタスク指示
    task = f"""
    以下のディレクトリのプロジェクトを分析し、包括的な README.md を生成してください:

    対象ディレクトリ: {target_dir}
    出力ファイル: {output_path}

    タスク:
    1. プロジェクト内のソースファイル（.py, .js, .ts など）を検索
    2. 各ファイルの主要な関数やクラスを読み取り
    3. プロジェクトの目的と機能を推測
    4. 以下のセクションを含む README.md を作成:
       - プロジェクト名と概要
       - 主な機能
       - インストール方法
       - 使用方法（コード例を含む）
       - プロジェクト構造
       - ライセンス情報（既存のLICENSEファイルがあれば参照）

    注意事項:
    - venv, node_modules, .git などは無視
    - 実際のコード内容に基づいて正確な説明を生成
    - マークダウン形式で見やすく整形
    - コード例は実際のファイルから抽出

    最後に、生成した内容を {output_path} に書き込んでください。
    """

    console.print("[yellow]📝 README生成タスクを実行中...[/yellow]")
    console.print()

    # ツール使用状況の追跡
    tools_used = []

    # オプション設定
    options = ClaudeAgentOptions(
        allowed_tools=["Glob", "Read", "Write"],  # ファイル操作ツールを許可
        cwd=target_dir,
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

                    elif isinstance(block, ToolUseBlock):
                        # ツール使用を記録
                        tools_used.append({
                            "tool": block.name,
                            "details": str(block.input)[:100]
                        })

                        # Writeツールの場合は特別な表示
                        if block.name == "Write":
                            file_path = block.input.get('file_path', 'unknown')
                            console.print(f"[bold green]📝 ファイル書き込み中: {file_path}[/bold green]")
                        else:
                            console.print(f"[blue]🔧 {block.name} を使用中...[/blue]")

            elif isinstance(message, ResultMessage):
                # 最終結果を表示
                if message.result:
                    console.print()
                    console.print(Panel(
                        f"[bold green]{message.result}[/bold green]",
                        title="✅ 完了",
                        border_style="green"
                    ))

                # トークン使用量と費用を表示
                print_usage_stats(message)

    # ツール使用統計
    console.print()
    if tools_used:
        console.print(Panel(
            "\n".join(f"{i+1}. {t['tool']}" for i, t in enumerate(tools_used)),
            title=f"🔧 使用されたツール（計{len(tools_used)}回）",
            border_style="blue"
        ))

    # 生成されたファイルの確認
    readme_path = os.path.join(target_dir, output_path)
    if os.path.exists(readme_path):
        console.print()
        console.print(f"[bold green]✅ README が生成されました: {readme_path}[/bold green]")

        # プレビュー表示
        if Confirm.ask("生成されたREADMEをプレビューしますか？"):
            console.print()
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            console.print(Panel(
                content[:1000] + ("\n\n...(省略)..." if len(content) > 1000 else ""),
                title="📄 README プレビュー",
                border_style="cyan"
            ))

    console.print()
    console.print("[yellow]💡 このデモで学べたこと:[/yellow]")
    console.print("  • Glob でソースファイル検索")
    console.print("  • Read で複数ファイルを読み取り")
    console.print("  • Write でファイル生成")
    console.print("  • 複雑なドキュメント作成の自動化")
    console.print("  • エージェントがコードを理解して説明を生成")


def main():
    """
    メイン関数
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

    # README生成実行
    asyncio.run(generate_readme(target_dir))


if __name__ == "__main__":
    main()
