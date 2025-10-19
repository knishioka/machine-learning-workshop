#!/usr/bin/env python3
"""
Claude Agent SDK - 応用編 Example 1: Research Agent

Web検索を活用してリサーチを行い、分析レポートを生成する
自律的なエージェントのデモです。

実行方法:
    python examples/03_advanced/research_agent.py "リサーチテーマ"

    # 例: AI技術のトレンド調査
    python examples/03_advanced/research_agent.py "2025年のAI技術トレンド"

    # 例: プログラミング言語の比較
    python examples/03_advanced/research_agent.py "Python vs Rust パフォーマンス比較"

期待される動作:
    1. テーマに関連するキーワードでWeb検索
    2. 検索結果から関連情報を収集
    3. 情報を分析・統合
    4. 構造化されたリサーチレポートを生成
    5. オプション: レポートをファイルに保存
"""

import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from claude_agent_sdk.types import AssistantMessage, TextBlock, ToolUseBlock, ResultMessage
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
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


async def research_agent(topic: str, save_to_file: bool = True):
    """
    リサーチエージェント

    このデモで使用される機能:
    - Web検索ツール: インターネットから情報収集
    - マルチステップ実行: 検索 → 分析 → 統合 → レポート生成
    - エージェントループ: 自律的な判断と実行
    - ファイル書き込み: レポート保存（オプション）

    Args:
        topic: リサーチテーマ
        save_to_file: レポートをファイルに保存するか
    """

    console.print(Panel.fit(
        f"[bold cyan]Claude Agent SDK - Research Agent[/bold cyan]\n"
        f"テーマ: {topic}",
        border_style="cyan"
    ))
    console.print()

    # エージェントへのタスク指示
    task = f"""
    以下のテーマについて、包括的なリサーチを実施してください:

    テーマ: {topic}

    実行ステップ:
    1. Web検索でテーマに関連する最新情報を収集
    2. 複数の情報源から重要なポイントを抽出
    3. 情報の信頼性と関連性を評価
    4. 収集した情報を統合・分析
    5. 以下の構成でリサーチレポートを作成:
       - エグゼクティブサマリー（要約）
       - 主要な発見事項（3-5点）
       - 詳細分析
       - 情報源リスト
       - 結論と推奨事項

    注意事項:
    - 複数の視点から情報を収集
    - 最新情報を優先
    - 事実とオピニオンを区別
    - 情報源を明記

    最終的に、マークダウン形式で読みやすいレポートを提示してください。
    """

    if save_to_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"research_report_{timestamp}.md"
        task += f"\n\n最後に、レポートを {output_file} に保存してください。"

    console.print("[yellow]🔍 リサーチを開始します...[/yellow]")
    console.print()

    # 進行状況の追跡
    phase = "初期化中"
    tools_used = []

    # プログレスバー
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task_id = progress.add_task("[cyan]リサーチ中...", total=None)

        # オプション設定
        options = ClaudeAgentOptions(
            allowed_tools=["WebSearch", "Write"],  # Web検索と書き込みを許可
        )

        # エージェント実行
        async with ClaudeSDKClient(options=options) as client:
            await client.query(task)

            async for message in client.receive_response():
                if isinstance(message, ResultMessage):
                    progress.update(task_id, description="[green]✅ 完了")
                    if message.result:
                        console.print()
                        console.print(Panel(
                            f"[bold green]{message.result}[/bold green]",
                            title="📊 リサーチレポート",
                            border_style="green",
                            padding=(1, 2)
                        ))

                    # トークン使用量と費用を表示
                    print_usage_stats(message)

                elif isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, ToolUseBlock):
                            tools_used.append(block.name)

                            if block.name == "WebSearch":
                                phase = "Web検索中"
                                progress.update(task_id, description=f"[yellow]🔍 {phase}...")
                                console.print(f"[blue]🌐 Web検索を実行中...[/blue]")
                            elif block.name == "Write":
                                phase = "レポート保存中"
                                progress.update(task_id, description=f"[yellow]📝 {phase}...")
                                console.print(f"[green]💾 レポートを保存中...[/green]")
                            else:
                                console.print(f"[blue]🔧 {block.name} を使用中...[/blue]")

                        elif isinstance(block, TextBlock):
                            # 思考過程を簡潔に表示
                            content = block.text[:80]
                            if len(block.text) > 80:
                                content += "..."
                            console.print(f"[dim]💭 {content}[/dim]")

    # 統計情報
    console.print()
    console.print(Panel.fit(
        f"[bold]リサーチ統計[/bold]\n\n"
        f"テーマ: {topic}\n"
        f"使用ツール: {', '.join(set(tools_used))}\n"
        f"ツール使用回数: {len(tools_used)}回\n"
        f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        title="📈 統計情報",
        border_style="magenta"
    ))

    # 保存されたファイルの確認
    if save_to_file:
        # 最新の research_report_*.md を探す
        import glob
        reports = glob.glob("research_report_*.md")
        if reports:
            latest_report = max(reports, key=os.path.getctime)
            console.print()
            console.print(f"[bold green]✅ レポートが保存されました: {latest_report}[/bold green]")

    console.print()
    console.print("[yellow]💡 このデモで学べたこと:[/yellow]")
    console.print("  • Web検索ツールの活用")
    console.print("  • マルチステップの自律的実行")
    console.print("  • エージェントループによる情報収集・分析・統合")
    console.print("  • 複雑なリサーチタスクの自動化")


def main():
    """
    メイン関数
    """

    # 環境変数チェック
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[bold red]❌ エラー: ANTHROPIC_API_KEY が設定されていません[/bold red]")
        console.print("   .env ファイルを作成し、APIキーを設定してください")
        exit(1)

    # リサーチテーマの取得
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        console.print("[yellow]リサーチテーマを指定してください[/yellow]")
        console.print()
        console.print("使用例:")
        console.print('  python examples/03_advanced/research_agent.py "2025年のAI技術トレンド"')
        console.print('  python examples/03_advanced/research_agent.py "Python vs Rust"')
        exit(1)

    # リサーチ実行
    asyncio.run(research_agent(topic))


if __name__ == "__main__":
    main()
