---
name: stakeholder-presentation
description: MLプロジェクトのステークホルダー向けプレゼンテーションを自動生成。会社のテンプレートに沿った形式で、プロジェクト進捗、モデル性能、ビジネスインパクトなどをスライド化します。
---

# Stakeholder Presentation Generator

このスキルは、機械学習プロジェクトのステークホルダー向けプレゼンテーションを自動生成します。会社の標準テンプレートに沿った形式で、技術的な詳細をビジネス価値に翻訳して提示します。

## When to Use

以下のような場合にこのスキルを使用してください：
- 経営陣や非技術系ステークホルダーへの報告が必要
- プロジェクトの進捗報告会がある
- モデルのROI（投資対効果）を説明したい
- 定期的な事業レビューでMLプロジェクトを報告
- 新しいMLイニシアチブの承認を得たい

## Instructions

### 1. プレゼンテーション要件の確認

ユーザーに以下を確認：
- 対象者は？（経営陣、事業部門、技術チームなど）
- 目的は？（進捗報告、予算承認、意思決定など）
- 時間は？（5分、15分、30分など）
- 含めるべき内容は？（技術詳細、ビジネス成果、コストなど）
- 会社のテンプレートはあるか？

### 2. スライド構成テンプレート

#### 標準的な構成（15分プレゼン）

```
1. タイトルスライド
2. エグゼクティブサマリー
3. プロジェクト概要
4. 現状の課題
5. ソリューション（MLアプローチ）
6. モデル性能
7. ビジネスインパクト
8. 実装ロードマップ
9. リスクと対策
10. 次のステップ
11. Q&A
```

### 3. PowerPoint自動生成コード

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
import pandas as pd
from datetime import datetime

class StakeholderPresentation:
    """ステークホルダー向けプレゼンテーション生成クラス"""

    def __init__(self, template_path=None):
        """
        Parameters:
        -----------
        template_path : str, optional
            会社のPowerPointテンプレートのパス
        """
        if template_path:
            self.prs = Presentation(template_path)
        else:
            self.prs = Presentation()

        # デフォルトのスライドサイズ（16:9）
        self.prs.slide_width = Inches(10)
        self.prs.slide_height = Inches(7.5)

    def add_title_slide(self, title, subtitle, author, date=None):
        """タイトルスライドを追加"""

        slide_layout = self.prs.slide_layouts[0]  # タイトルスライドレイアウト
        slide = self.prs.slides.add_slide(slide_layout)

        # タイトル
        title_shape = slide.shapes.title
        title_shape.text = title

        # サブタイトル
        subtitle_shape = slide.placeholders[1]
        subtitle_shape.text = subtitle

        # 著者と日付を追加
        if date is None:
            date = datetime.now().strftime('%Y年%m月%d日')

        text_box = slide.shapes.add_textbox(
            Inches(7), Inches(6.5), Inches(2.5), Inches(0.5)
        )
        text_frame = text_box.text_frame
        p = text_frame.paragraphs[0]
        p.text = f"{author}\n{date}"
        p.font.size = Pt(10)
        p.alignment = PP_ALIGN.RIGHT

        return slide

    def add_executive_summary(self, key_points):
        """エグゼクティブサマリースライドを追加"""

        slide_layout = self.prs.slide_layouts[1]  # タイトルとコンテンツ
        slide = self.prs.slides.add_slide(slide_layout)

        title = slide.shapes.title
        title.text = "エグゼクティブサマリー"

        # 箇条書きを追加
        body_shape = slide.placeholders[1]
        tf = body_shape.text_frame

        for point in key_points:
            p = tf.add_paragraph()
            p.text = point
            p.level = 0
            p.font.size = Pt(18)

        return slide

    def add_metrics_slide(self, title, metrics_dict):
        """メトリクススライドを追加（KPIを大きく表示）"""

        slide_layout = self.prs.slide_layouts[5]  # 空白レイアウト
        slide = self.prs.slides.add_slide(slide_layout)

        # タイトル
        title_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)
        )
        title_frame = title_box.text_frame
        title_para = title_frame.paragraphs[0]
        title_para.text = title
        title_para.font.size = Pt(32)
        title_para.font.bold = True

        # メトリクスを配置（最大4つまで、2x2グリッド）
        metrics_list = list(metrics_dict.items())
        positions = [
            (Inches(1), Inches(2)),    # 左上
            (Inches(5.5), Inches(2)),  # 右上
            (Inches(1), Inches(4.5)),  # 左下
            (Inches(5.5), Inches(4.5)) # 右下
        ]

        for idx, (metric_name, metric_value) in enumerate(metrics_list[:4]):
            x, y = positions[idx]

            # メトリクス値（大きく表示）
            value_box = slide.shapes.add_textbox(x, y, Inches(4), Inches(1))
            value_frame = value_box.text_frame
            value_para = value_frame.paragraphs[0]
            value_para.text = str(metric_value)
            value_para.font.size = Pt(48)
            value_para.font.bold = True
            value_para.alignment = PP_ALIGN.CENTER

            # メトリクス名（小さく表示）
            name_box = slide.shapes.add_textbox(x, y + Inches(1), Inches(4), Inches(0.5))
            name_frame = name_box.text_frame
            name_para = name_frame.paragraphs[0]
            name_para.text = metric_name
            name_para.font.size = Pt(16)
            name_para.alignment = PP_ALIGN.CENTER

        return slide

    def add_chart_slide(self, title, chart_data, chart_type='line'):
        """グラフスライドを追加"""

        slide_layout = self.prs.slide_layouts[5]
        slide = self.prs.slides.add_slide(slide_layout)

        # タイトル
        title_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(0.5), Inches(9), Inches(0.6)
        )
        title_frame = title_box.text_frame
        title_para = title_frame.paragraphs[0]
        title_para.text = title
        title_para.font.size = Pt(28)
        title_para.font.bold = True

        # グラフデータの準備
        chart_data_obj = CategoryChartData()
        chart_data_obj.categories = chart_data['categories']

        for series_name, values in chart_data['series'].items():
            chart_data_obj.add_series(series_name, values)

        # グラフタイプの選択
        chart_type_map = {
            'line': XL_CHART_TYPE.LINE,
            'bar': XL_CHART_TYPE.BAR_CLUSTERED,
            'column': XL_CHART_TYPE.COLUMN_CLUSTERED,
            'pie': XL_CHART_TYPE.PIE
        }

        # グラフの追加
        x, y, cx, cy = Inches(1), Inches(2), Inches(8), Inches(4.5)
        chart = slide.shapes.add_chart(
            chart_type_map.get(chart_type, XL_CHART_TYPE.LINE),
            x, y, cx, cy, chart_data_obj
        ).chart

        # グラフのスタイリング
        chart.has_legend = True
        chart.legend.position = 2  # 右側
        chart.legend.include_in_layout = False

        return slide

    def add_business_impact_slide(self, impact_data):
        """ビジネスインパクトスライドを追加"""

        slide_layout = self.prs.slide_layouts[1]
        slide = self.prs.slides.add_slide(slide_layout)

        title = slide.shapes.title
        title.text = "ビジネスインパクト"

        # テーブルの追加
        rows = len(impact_data) + 1  # ヘッダー行を含む
        cols = 3  # 指標、現状、改善後

        left = Inches(1.5)
        top = Inches(2)
        width = Inches(7)
        height = Inches(4)

        table = slide.shapes.add_table(rows, cols, left, top, width, height).table

        # ヘッダー
        headers = ['指標', '現状', 'ML導入後（予測）']
        for col_idx, header in enumerate(headers):
            cell = table.cell(0, col_idx)
            cell.text = header
            cell.text_frame.paragraphs[0].font.bold = True
            cell.text_frame.paragraphs[0].font.size = Pt(14)

        # データ
        for row_idx, (metric, current, improved) in enumerate(impact_data, start=1):
            table.cell(row_idx, 0).text = metric
            table.cell(row_idx, 1).text = current
            table.cell(row_idx, 2).text = improved

        return slide

    def add_timeline_slide(self, title, milestones):
        """タイムラインスライドを追加"""

        slide_layout = self.prs.slide_layouts[5]
        slide = self.prs.slides.add_slide(slide_layout)

        # タイトル
        title_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(0.5), Inches(9), Inches(0.6)
        )
        title_frame = title_box.text_frame
        title_para = title_frame.paragraphs[0]
        title_para.text = title
        title_para.font.size = Pt(28)
        title_para.font.bold = True

        # タイムライン（簡易版）
        y_start = Inches(2)
        x_start = Inches(1)
        spacing = Inches(1.2)

        for idx, (date, milestone, status) in enumerate(milestones):
            y = y_start + (idx * spacing)

            # 日付
            date_box = slide.shapes.add_textbox(x_start, y, Inches(2), Inches(0.4))
            date_frame = date_box.text_frame
            date_para = date_frame.paragraphs[0]
            date_para.text = date
            date_para.font.size = Pt(14)
            date_para.font.bold = True

            # マイルストーン
            milestone_box = slide.shapes.add_textbox(
                x_start + Inches(2.5), y, Inches(5), Inches(0.4)
            )
            milestone_frame = milestone_box.text_frame
            milestone_para = milestone_frame.paragraphs[0]
            milestone_para.text = milestone
            milestone_para.font.size = Pt(14)

            # ステータス
            status_box = slide.shapes.add_textbox(
                x_start + Inches(8), y, Inches(1), Inches(0.4)
            )
            status_frame = status_box.text_frame
            status_para = status_frame.paragraphs[0]
            status_para.text = status
            status_para.font.size = Pt(14)

            # ステータスに応じて色を変更
            if status == "✅":
                status_para.font.color.rgb = (0, 128, 0)  # 緑
            elif status == "🔄":
                status_para.font.color.rgb = (255, 165, 0)  # オレンジ
            elif status == "⏳":
                status_para.font.color.rgb = (128, 128, 128)  # グレー

        return slide

    def save(self, filename):
        """プレゼンテーションを保存"""
        self.prs.save(filename)
        print(f"プレゼンテーションを保存しました: {filename}")


# 使用例
def generate_stakeholder_presentation():
    """ステークホルダー向けプレゼンテーションの生成"""

    # プレゼンテーション生成器の初期化
    ppt = StakeholderPresentation()

    # 1. タイトルスライド
    ppt.add_title_slide(
        title="顧客チャーン予測モデル\nプロジェクト進捗報告",
        subtitle="機械学習による顧客維持率向上の取り組み",
        author="データサイエンスチーム"
    )

    # 2. エグゼクティブサマリー
    ppt.add_executive_summary([
        "✅ モデル開発完了：予測精度 92% を達成",
        "💰 予想ROI：年間 5,000万円のコスト削減",
        "📅 本番展開：2025年12月予定",
        "⚠️ リスク：データ品質の継続的な監視が必要"
    ])

    # 3. 主要メトリクス
    ppt.add_metrics_slide(
        title="モデル性能サマリー",
        metrics_dict={
            "予測精度": "92%",
            "適合率": "89%",
            "リコール率": "95%",
            "ROI": "+250%"
        }
    )

    # 4. 性能推移グラフ
    chart_data = {
        'categories': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'series': {
            '精度': [0.85, 0.88, 0.90, 0.92],
            '目標': [0.90, 0.90, 0.90, 0.90]
        }
    }
    ppt.add_chart_slide(
        title="モデル精度の推移",
        chart_data=chart_data,
        chart_type='line'
    )

    # 5. ビジネスインパクト
    impact_data = [
        ("顧客維持率", "85%", "93% (+8%p)"),
        ("月間解約数", "500件", "350件 (-30%)"),
        ("顧客獲得コスト", "¥50,000/人", "¥35,000/人 (-30%)"),
        ("年間コスト削減", "-", "¥50,000,000")
    ]
    ppt.add_business_impact_slide(impact_data)

    # 6. タイムライン
    milestones = [
        ("2025年9月", "データ収集・分析", "✅"),
        ("2025年10月", "モデル開発・評価", "✅"),
        ("2025年11月", "A/Bテスト実施", "🔄"),
        ("2025年12月", "本番展開", "⏳"),
        ("2026年1月〜", "継続的モニタリング", "⏳")
    ]
    ppt.add_timeline_slide("実装ロードマップ", milestones)

    # 保存
    output_file = f"stakeholder_presentation_{datetime.now().strftime('%Y%m%d')}.pptx"
    ppt.save(output_file)

    return output_file
```

### 4. テンプレートのカスタマイズ

```python
class CustomBrandedPresentation(StakeholderPresentation):
    """会社ブランドに合わせたプレゼンテーション"""

    def __init__(self, template_path, brand_colors):
        super().__init__(template_path)
        self.brand_colors = brand_colors

    def apply_brand_styling(self, slide):
        """ブランドカラーとフォントを適用"""

        # 背景色
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = self.brand_colors['background']

        # タイトルの色
        if slide.shapes.title:
            title = slide.shapes.title
            title.text_frame.paragraphs[0].font.color.rgb = self.brand_colors['primary']

        return slide

# 使用例
brand_colors = {
    'primary': (0, 102, 204),      # 会社のメインカラー
    'secondary': (255, 153, 0),    # アクセントカラー
    'background': (255, 255, 255)  # 背景色
}

ppt = CustomBrandedPresentation('company_template.pptx', brand_colors)
```

### 5. 自動化スクリプト

```python
# generate_monthly_presentation.py
"""
月次プレゼンテーションの自動生成

データソースからメトリクスを取得し、
ステークホルダー向けプレゼンテーションを自動生成
"""

def generate_monthly_presentation(data_source):
    """月次プレゼンテーションの生成"""

    # データの取得
    metrics = fetch_metrics_from_database(data_source)
    business_impact = calculate_business_impact(metrics)

    # プレゼンテーション生成
    ppt = StakeholderPresentation()

    # 動的にスライドを生成
    ppt.add_title_slide(
        title=f"{metrics['project_name']}\n月次レポート",
        subtitle=f"{metrics['month']} の進捗と成果",
        author="データサイエンスチーム"
    )

    ppt.add_metrics_slide(
        title="今月のハイライト",
        metrics_dict=metrics['highlights']
    )

    # ... 残りのスライド

    # 保存
    filename = f"monthly_presentation_{metrics['month']}.pptx"
    ppt.save(filename)

    return filename

def fetch_metrics_from_database(data_source):
    """データベースからメトリクスを取得"""
    # 実装例
    pass

def calculate_business_impact(metrics):
    """ビジネスインパクトを計算"""
    # 実装例
    pass
```

## Best Practices

1. **ストーリーテリング**: データだけでなく、ストーリーを語る
2. **シンプルさ**: 1スライド1メッセージの原則
3. **ビジュアル重視**: グラフと数字で視覚的に訴求
4. **ビジネス言語**: 技術用語を避け、ROI、コスト削減などビジネス価値を強調
5. **アクションアイテム**: 次のステップを明確に

## Examples

### Example 1: シンプルな進捗報告

```python
ppt = StakeholderPresentation()
ppt.add_title_slide("プロジェクト進捗報告", "ML開発状況", "山田太郎")
ppt.add_executive_summary(["開発完了", "テスト中", "来月リリース"])
ppt.save("progress_report.pptx")
```

### Example 2: 詳細なビジネスレビュー

```python
# 完全な四半期レビュー
output = generate_stakeholder_presentation()
print(f"プレゼンテーション: {output}")
```

## Notes

- **python-pptx**: `pip install python-pptx` が必要
- **テンプレート**: 会社の公式テンプレートを使用することを推奨
- **自動化**: データソースと連携して自動生成
- **レビュー**: 自動生成後も人間によるレビューを推奨
