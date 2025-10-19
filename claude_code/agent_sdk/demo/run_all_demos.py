#!/usr/bin/env python3
"""
Claude Agent SDK - 全デモ一括実行スクリプト

基本編から応用編まで、すべてのデモを順番に実行して
Agent SDKの能力を段階的に体験できるスクリプトです。

実行方法:
    python demo/run_all_demos.py

オプション:
    --quick: 各デモを簡略版で実行（時間短縮）
    --skip-mcp: MCP連携編をスキップ
"""

import sys
import os
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

console = Console()


class DemoRunner:
    """デモ実行管理クラス"""

    def __init__(self, quick_mode=False, skip_mcp=False):
        self.quick_mode = quick_mode
        self.skip_mcp = skip_mcp
        self.results = []

    def print_header(self):
        """ヘッダー表示"""
        console.print(Panel.fit(
            "[bold cyan]Claude Agent SDK - 全デモ一括実行[/bold cyan]\n\n"
            "基本編 → 実用編 → 応用編 → MCP連携編\n"
            "の順に、Agent SDKの能力を段階的に体験します。\n\n"
            f"モード: {'クイック' if self.quick_mode else '通常'}\n"
            f"MCP連携: {'スキップ' if self.skip_mcp else '含む'}",
            border_style="cyan"
        ))

    def run_demo(self, level: str, name: str, description: str, module_path: str, args: list = None):
        """
        個別デモを実行

        Args:
            level: レベル（基本編、実用編など）
            name: デモ名
            description: 説明
            module_path: モジュールパス
            args: デモに渡すコマンドライン引数（オプション）
        """
        if args is None:
            args = []
        console.print()
        console.print(Panel(
            f"[bold yellow]{level}[/bold yellow]\n"
            f"[cyan]{name}[/cyan]\n\n"
            f"{description}",
            border_style="yellow"
        ))

        if not Confirm.ask(f"\n{name} を実行しますか？", default=True):
            self.results.append({
                "level": level,
                "name": name,
                "status": "スキップ"
            })
            return

        try:
            console.print(f"\n[yellow]▶ {name} を実行中...[/yellow]")
            console.print(f"[dim]ファイル: {module_path}[/dim]\n")

            # デモファイルのパスを構築
            # module_path を examples.01_basic.hello_agent から examples/01_basic/hello_agent.py に変換
            demo_file = project_root / (module_path.replace('.', '/') + '.py')

            if not demo_file.exists():
                raise FileNotFoundError(f"デモファイルが見つかりません: {demo_file}")

            # サブプロセスとしてデモを実行（リアルタイム出力）
            cmd = [sys.executable, "-u", str(demo_file)] + args
            process = subprocess.Popen(
                cmd,
                cwd=str(project_root),
                stdin=subprocess.DEVNULL,  # 対話的な入力を無効化
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1  # 行バッファリング
            )

            # リアルタイムで出力を表示
            for line in process.stdout:
                # 各行にインデントを追加して見やすく
                console.print(f"  {line}", end="", markup=False)

            # プロセスの終了を待つ
            return_code = process.wait()

            if return_code == 0:
                console.print(f"\n[green]✅ {name} が完了しました[/green]")
                self.results.append({
                    "level": level,
                    "name": name,
                    "status": "完了"
                })
            else:
                console.print(f"\n[red]❌ {name} がエラーコード {return_code} で終了しました[/red]")
                self.results.append({
                    "level": level,
                    "name": name,
                    "status": f"エラーコード: {return_code}"
                })

        except Exception as e:
            console.print(f"[red]❌ エラー: {str(e)}[/red]")
            self.results.append({
                "level": level,
                "name": name,
                "status": f"エラー: {str(e)}"
            })

        # 次のデモに進む前の確認
        if not self.quick_mode:
            console.print()
            Prompt.ask("続けるには Enter を押してください", default="")

    def run_all_demos(self):
        """すべてのデモを実行"""

        self.print_header()
        console.print()

        # デモの定義
        demos = [
            # 基本編
            {
                "level": "基本編 (1/4)",
                "name": "Hello Agent",
                "description": "最もシンプルなエージェント実行",
                "module": "examples.01_basic.hello_agent"
            },
            {
                "level": "基本編 (2/4)",
                "name": "Streaming Demo",
                "description": "ストリーミング動作の可視化",
                "module": "examples.01_basic.streaming_demo"
            },

            # 実用編
            {
                "level": "実用編 (1/4)",
                "name": "Project Analyzer",
                "description": "プロジェクト構造の自動分析",
                "module": "examples.02_practical.project_analyzer"
            },
            {
                "level": "実用編 (2/4)",
                "name": "README Generator",
                "description": "コードから自動README生成",
                "module": "examples.02_practical.readme_generator"
            },

            # 応用編
            {
                "level": "応用編 (1/4)",
                "name": "Research Agent",
                "description": "Web検索を使ったリサーチエージェント",
                "module": "examples.03_advanced.research_agent",
                "args": ["Claude Agent SDK の特徴"]
            },
            {
                "level": "応用編 (2/4)",
                "name": "Code Reviewer",
                "description": "自動コードレビュー",
                "module": "examples.03_advanced.code_reviewer",
                "args": ["examples/01_basic"]
            },
        ]

        # MCP連携編
        if not self.skip_mcp:
            demos.append({
                "level": "MCP連携編 (1/1)",
                "name": "MCP Integration",
                "description": "外部サービス連携の拡張性デモ",
                "module": "examples.04_mcp.mcp_example"
            })

        # 各デモを実行
        for demo in demos:
            self.run_demo(
                demo["level"],
                demo["name"],
                demo["description"],
                demo["module"],
                demo.get("args", [])
            )

        # 結果サマリー
        self.print_summary()

    def print_summary(self):
        """実行結果のサマリーを表示"""

        console.print()
        console.print(Panel.fit(
            "[bold green]全デモの実行が完了しました！[/bold green]",
            border_style="green"
        ))
        console.print()

        # 結果テーブル
        table = Table(title="📊 実行結果サマリー")
        table.add_column("レベル", style="cyan")
        table.add_column("デモ名", style="yellow")
        table.add_column("ステータス", style="green")

        for result in self.results:
            status_color = "green" if result["status"] == "完了" else "yellow" if result["status"] == "スキップ" else "red"
            table.add_row(
                result["level"],
                result["name"],
                f"[{status_color}]{result['status']}[/{status_color}]"
            )

        console.print(table)
        console.print()

        # 統計
        completed = sum(1 for r in self.results if r["status"] == "完了")
        skipped = sum(1 for r in self.results if r["status"] == "スキップ")
        errors = sum(1 for r in self.results if r["status"].startswith("エラー"))

        console.print(Panel.fit(
            f"[bold]統計[/bold]\n\n"
            f"完了: {completed}件\n"
            f"スキップ: {skipped}件\n"
            f"エラー: {errors}件\n"
            f"合計: {len(self.results)}件",
            title="📈 実行統計",
            border_style="magenta"
        ))

        # 次のステップ
        console.print()
        console.print("[yellow]💡 次のステップ:[/yellow]")
        console.print("  • 各デモを個別に再実行して理解を深める")
        console.print("  • docs/PRESENTATION.md でプレゼン資料を確認")
        console.print("  • docs/ARCHITECTURE.md でアーキテクチャを学ぶ")
        console.print("  • 独自のエージェントを作成してみる")


def main():
    """メイン関数"""

    # コマンドライン引数の処理
    quick_mode = "--quick" in sys.argv
    skip_mcp = "--skip-mcp" in sys.argv

    # 環境変数チェック
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[bold red]❌ エラー: ANTHROPIC_API_KEY が設定されていません[/bold red]")
        console.print("   .env ファイルを作成し、APIキーを設定してください")
        console.print("   詳細: README.md を参照")
        sys.exit(1)

    # デモランナーの作成と実行
    runner = DemoRunner(quick_mode=quick_mode, skip_mcp=skip_mcp)

    # ウェルカムメッセージ
    console.print()
    console.print("[bold cyan]Claude Agent SDK デモへようこそ！[/bold cyan]")
    console.print()
    console.print("このスクリプトは、Agent SDKのすべてのデモを順番に実行します。")
    console.print("各デモの実行前に確認が求められます。")
    console.print()

    if not Confirm.ask("デモを開始しますか？", default=True):
        console.print("[yellow]デモをキャンセルしました[/yellow]")
        sys.exit(0)

    # デモを実行
    runner.run_all_demos()


if __name__ == "__main__":
    main()
