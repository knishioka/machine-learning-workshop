#!/usr/bin/env python3
"""
Markdown to PowerPoint Converter - CLIエントリポイント

使用方法:
    python md2slides.py input.md [output.pptx] [options]

終了コード:
    0 - 成功
    1 - エラー（詳細はstderr）
"""
import argparse
import sys
from pathlib import Path

# 同じディレクトリからインポート
sys.path.insert(0, str(Path(__file__).parent))
from parser import MarkdownParser
from generator import PresentationGenerator


def main() -> int:
    """CLIメインエントリポイント"""
    arg_parser = argparse.ArgumentParser(
        description="MarkdownをPowerPointプレゼンテーションに変換"
    )
    arg_parser.add_argument("input", help="入力Markdownファイル (.md)")
    arg_parser.add_argument(
        "output",
        nargs="?",
        help="出力PowerPointファイル (.pptx)。デフォルト: 入力ファイル名.pptx"
    )
    arg_parser.add_argument(
        "--title",
        help="プレゼンテーションタイトル（デフォルト: 最初のH1またはファイル名）"
    )
    arg_parser.add_argument(
        "--theme",
        choices=["default", "dark", "corporate"],
        default="default",
        help="カラーテーマ"
    )
    arg_parser.add_argument(
        "--aspect",
        choices=["16:9", "4:3"],
        default="16:9",
        help="スライドのアスペクト比"
    )

    args = arg_parser.parse_args()

    # 入力ファイルの検証
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: 入力ファイルが見つかりません: {args.input}", file=sys.stderr)
        return 1

    if input_path.suffix.lower() != ".md":
        print(f"Error: .mdファイルを指定してください: {input_path.suffix}", file=sys.stderr)
        return 1

    # 出力パスの決定
    output_path = Path(args.output) if args.output else input_path.with_suffix(".pptx")

    try:
        # Markdownをパース
        md_parser = MarkdownParser()
        slides_data = md_parser.parse_file(input_path)

        # タイトルの上書き
        if args.title:
            slides_data.title = args.title

        # PPTXを生成
        generator = PresentationGenerator(theme=args.theme, aspect=args.aspect)
        generator.create_presentation(slides_data, output_path)

        # 結果を出力（Claudeがキャプチャ）
        print(str(output_path.absolute()))
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
