#!/usr/bin/env python3
"""
Claude Agent SDK - 応用編 Example 2: Code Reviewer

コードを分析し、改善提案を行い、オプションで実装まで行う
自律的なコードレビューエージェントのデモです。

実行方法:
    python examples/03_advanced/code_reviewer.py [ファイルパス]

    # 例: 特定のPythonファイルをレビュー
    python examples/03_advanced/code_reviewer.py script.py

    # 例: ディレクトリ内の全Pythonファイルをレビュー
    python examples/03_advanced/code_reviewer.py .

期待される動作:
    1. 対象ファイルの読み取り
    2. コード品質の分析
    3. 改善点の特定
    4. 具体的な改善提案の生成
    5. オプション: 改善の実装
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
from rich.syntax import Syntax
from rich.prompt import Confirm

console = Console()
load_dotenv()


async def code_reviewer(target_path: str, auto_fix: bool = False):
    """
    コードレビューエージェント

    このデモで使用される機能:
    - ファイル操作: Read（コード読み取り）、Write/Edit（修正）
    - コード解析: 構文、スタイル、ベストプラクティス
    - マルチステップ実行: 分析 → 提案 → 実装
    - 自律的判断: 重要度の評価、優先順位付け

    Args:
        target_path: レビュー対象のファイルまたはディレクトリ
        auto_fix: 自動修正を行うか
    """

    console.print(Panel.fit(
        f"[bold cyan]Claude Agent SDK - Code Reviewer[/bold cyan]\n"
        f"対象: {target_path}\n"
        f"自動修正: {'有効' if auto_fix else '無効'}",
        border_style="cyan"
    ))
    console.print()

    # パスの検証
    path = Path(target_path)
    if not path.exists():
        console.print(f"[bold red]❌ エラー: パスが見つかりません: {target_path}[/bold red]")
        return

    # エージェントへのタスク指示
    task = f"""
    以下のコードをレビューし、改善提案を行ってください:

    対象: {target_path}

    レビュー観点:
    1. コード品質
       - 可読性（変数名、関数名、コメント）
       - 複雑度（関数の長さ、ネストの深さ）
       - 保守性（DRY原則、モジュール化）

    2. ベストプラクティス
       - 言語固有の慣習
       - デザインパターンの適用
       - エラーハンドリング

    3. パフォーマンス
       - 非効率なアルゴリズム
       - 不要な計算
       - メモリ使用

    4. セキュリティ
       - 潜在的な脆弱性
       - 入力検証
       - 安全でない操作

    実行ステップ:
    1. 対象ファイルを読み取り（ディレクトリの場合は主要ファイル）
    2. 各観点からコードを分析
    3. 問題点を重要度順に整理（高・中・低）
    4. 具体的な改善案をコード例付きで提示
    5. レビューレポートを作成

    レポート形式:
    - サマリー（全体評価）
    - 重要な問題点（Top 3-5）
    - 詳細な改善提案（コード例付き）
    - 優先順位と推奨アクション
    """

    if auto_fix:
        task += """

    追加タスク（自動修正モード）:
    - 安全に修正できる問題を特定
    - 修正内容をユーザーに説明
    - バックアップを作成後、修正を実装
    """

    console.print("[yellow]🔍 コードレビューを開始します...[/yellow]")
    console.print()

    # レビュー結果の保存
    review_results = {
        "files_reviewed": [],
        "issues_found": [],
        "tools_used": []
    }

    # オプション設定
    options = ClaudeAgentOptions(
        allowed_tools=["Glob", "Read", "Write"] if auto_fix else ["Glob", "Read"],
        cwd="." if path.is_dir() else str(path.parent),
    )

    # エージェント実行
    async with ClaudeSDKClient(options=options) as client:
        await client.query(task)

        async for message in client.receive_response():
            if isinstance(message, ResultMessage):
                if message.result:
                    console.print()
                    console.print(Panel(
                        f"[bold green]{message.result}[/bold green]",
                        title="📋 レビューレポート",
                        border_style="green",
                        padding=(1, 2)
                    ))

                    # レビューレポートを保存
                    report_file = "code_review_report.md"
                    with open(report_file, 'w', encoding='utf-8') as f:
                        f.write(f"# Code Review Report\n\n")
                        f.write(f"**Target:** {target_path}\n\n")
                        f.write(message.result)

                    console.print()
                    console.print(f"[bold green]✅ レビューレポートが保存されました: {report_file}[/bold green]")

            elif isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, ToolUseBlock):
                        review_results["tools_used"].append(block.name)

                        if block.name == "Read":
                            # ファイル読み取り
                            file_path = block.input.get('file_path', 'unknown')
                            if file_path not in review_results["files_reviewed"]:
                                review_results["files_reviewed"].append(file_path)
                            console.print(f"[blue]📖 読み取り中: {Path(file_path).name}[/blue]")

                        elif block.name == "Glob":
                            console.print(f"[blue]🔍 ファイル検索中...[/blue]")

                        elif block.name == "Write":
                            console.print(f"[green]📝 修正を適用中...[/green]")

                    elif isinstance(block, TextBlock):
                        # 思考過程を簡潔に表示
                        content = block.text[:80]
                        if len(block.text) > 80:
                            content += "..."
                        console.print(f"[dim]💭 {content}[/dim]")

    # レビュー統計
    console.print()
    console.print(Panel.fit(
        f"[bold]レビュー統計[/bold]\n\n"
        f"レビュー対象: {target_path}\n"
        f"ファイル数: {len(review_results['files_reviewed'])}件\n"
        f"ツール使用: {len(review_results['tools_used'])}回\n"
        f"自動修正: {'実施' if auto_fix else '未実施'}",
        title="📊 統計情報",
        border_style="magenta"
    ))

    console.print()
    console.print("[yellow]💡 このデモで学べたこと:[/yellow]")
    console.print("  • コード解析の自動化")
    console.print("  • マルチステップの自律的実行（分析→提案→実装）")
    console.print("  • エージェントによる品質評価")
    console.print("  • 複雑なコードレビュータスクの自動化")


def main():
    """
    メイン関数
    """

    # 環境変数チェック
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[bold red]❌ エラー: ANTHROPIC_API_KEY が設定されていません[/bold red]")
        console.print("   .env ファイルを作成し、APIキーを設定してください")
        exit(1)

    # 対象パスの取得
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
    else:
        console.print("[yellow]レビュー対象のファイルまたはディレクトリを指定してください[/yellow]")
        console.print()
        console.print("使用例:")
        console.print("  python examples/03_advanced/code_reviewer.py script.py")
        console.print("  python examples/03_advanced/code_reviewer.py .")
        exit(1)

    # 自動修正の確認
    auto_fix = False
    if Confirm.ask("\n問題が見つかった場合、自動修正を試みますか？", default=False):
        auto_fix = True
        console.print("[yellow]⚠️  自動修正モードが有効です。バックアップを取ることをお勧めします。[/yellow]")

    # レビュー実行
    asyncio.run(code_reviewer(target_path, auto_fix))


if __name__ == "__main__":
    main()
