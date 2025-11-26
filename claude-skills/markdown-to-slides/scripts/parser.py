"""
Markdown Parser - MarkdownをスライドデータStructureに変換

設計方針:
- 外部依存なし（標準ライブラリのみ）
- 不正な入力もgracefulに処理
- 明確なデータ構造でgeneratorに渡す
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import re


@dataclass
class SlideContent:
    """単一スライドのコンテンツを表現"""
    title: str = ""
    bullets: list[str] = field(default_factory=list)
    code_blocks: list[str] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    is_title_slide: bool = False


@dataclass
class PresentationData:
    """プレゼンテーション全体の構造を表現"""
    title: str = ""
    slides: list[SlideContent] = field(default_factory=list)


class MarkdownParser:
    """MarkdownをプレゼンテーションデータStructureにパース"""

    # Markdown要素の正規表現パターン
    H1_PATTERN = re.compile(r"^#\s+(.+)$", re.MULTILINE)
    H2_PATTERN = re.compile(r"^##\s+(.+)$", re.MULTILINE)
    BULLET_PATTERN = re.compile(r"^(\s*)[-*]\s+(.+)$", re.MULTILINE)
    CODE_BLOCK_PATTERN = re.compile(r"```[\w]*\n(.*?)```", re.DOTALL)
    IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    SLIDE_BREAK = re.compile(r"^---\s*$", re.MULTILINE)

    def parse_file(self, path: Path) -> PresentationData:
        """Markdownファイルをパース"""
        content = path.read_text(encoding="utf-8")
        return self.parse(content, default_title=path.stem)

    def parse(self, content: str, default_title: str = "Presentation") -> PresentationData:
        """Markdown文字列をパース"""
        presentation = PresentationData(title=default_title)

        # 最初のH1をタイトルとして抽出
        h1_match = self.H1_PATTERN.search(content)
        if h1_match:
            presentation.title = h1_match.group(1).strip()
            # タイトルスライドを作成
            title_slide = SlideContent(
                title=presentation.title,
                is_title_slide=True
            )
            presentation.slides.append(title_slide)

        # H2または---でセクションに分割
        sections = self._split_into_sections(content)

        for section in sections:
            slide = self._parse_section(section)
            if slide.title or slide.bullets or slide.code_blocks:
                presentation.slides.append(slide)

        return presentation

    def _split_into_sections(self, content: str) -> list[str]:
        """コンテンツをH2または---でセクションに分割"""
        # まず---で分割
        parts = self.SLIDE_BREAK.split(content)
        sections = []

        for part in parts:
            # 各パートをH2でさらに分割
            h2_splits = re.split(r"(?=^##\s)", part, flags=re.MULTILINE)
            sections.extend([s.strip() for s in h2_splits if s.strip()])

        return sections

    def _parse_section(self, section: str) -> SlideContent:
        """単一セクションをスライドコンテンツにパース"""
        slide = SlideContent()

        # H2タイトルを抽出
        h2_match = self.H2_PATTERN.search(section)
        if h2_match:
            slide.title = h2_match.group(1).strip()

        # 箇条書きを抽出
        for match in self.BULLET_PATTERN.finditer(section):
            indent = len(match.group(1))
            text = match.group(2).strip()
            # インデントレベルをプレフィックスで表現
            prefix = "  " * (indent // 2)
            slide.bullets.append(f"{prefix}{text}")

        # コードブロックを抽出
        for match in self.CODE_BLOCK_PATTERN.finditer(section):
            slide.code_blocks.append(match.group(1).strip())

        # 画像を抽出
        for match in self.IMAGE_PATTERN.finditer(section):
            slide.images.append(match.group(2))

        return slide
