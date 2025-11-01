---
name: ml-weekly-report
description: 機械学習モデルの週次性能レポートを自動生成。定期的なモデル監視、性能トレンド、データドリフト、インシデントを標準フォーマットでレポート化します。
---

# ML Weekly Report

このスキルは、機械学習モデルの運用状況を定期的にレポートするための自動化ツールです。決まったフォーマットで週次レポートを生成し、ステークホルダーへの報告を効率化します。

## When to Use

以下のような場合にこのスキルを使用してください：
- 本番環境で稼働中のMLモデルの定期レポートが必要
- 週次/月次でモデル性能を報告する義務がある
- モデルの性能トレンドを追跡したい
- データドリフトや異常を定期的にチェックしたい
- ステークホルダーへの定型レポートが必要

## Instructions

### 1. レポート設定の確認

ユーザーに以下を確認：
- レポート対象のモデルは？（複数可）
- レポート期間は？（週次、月次など）
- データソースは？（ログファイル、データベース、MLflowなど）
- 出力形式は？（Markdown、HTML、PDF、PowerPointなど）
- 含めるべき指標は？（精度、レイテンシ、スループットなど）

### 2. レポートテンプレート

```markdown
# 機械学習モデル週次レポート

**レポート期間**: {start_date} 〜 {end_date}
**作成日**: {report_date}
**担当者**: {owner}

---

## エグゼクティブサマリー

- 総予測数: {total_predictions:,}
- 平均精度: {avg_accuracy:.2%}
- システム稼働率: {uptime:.2%}
- 重大インシデント: {critical_incidents}

### 主要な発見事項
- ✅ {positive_finding_1}
- ⚠️ {attention_needed_1}
- 🚨 {critical_issue_1}

---

## モデル性能サマリー

### 精度メトリクス

| モデル | 精度 | 前週比 | 目標値 | ステータス |
|--------|------|--------|--------|-----------|
| {model_1} | {accuracy_1} | {change_1} | {target_1} | {status_1} |
| {model_2} | {accuracy_2} | {change_2} | {target_2} | {status_2} |

### パフォーマンスメトリクス

| メトリクス | 今週 | 前週 | 変化 |
|-----------|------|------|------|
| 平均レイテンシ (ms) | {latency_current} | {latency_prev} | {latency_change} |
| スループット (req/s) | {throughput_current} | {throughput_prev} | {throughput_change} |
| エラー率 (%) | {error_rate_current} | {error_rate_prev} | {error_rate_change} |

---

## トレンド分析

### 精度の推移
![Accuracy Trend](accuracy_trend.png)

### 予測数の推移
![Prediction Volume](prediction_volume.png)

### レイテンシの推移
![Latency Trend](latency_trend.png)

---

## データドリフト分析

### 特徴量分布の変化

| 特徴量 | ドリフト検出 | KSテスト p値 | アクション |
|--------|-------------|--------------|-----------|
| {feature_1} | {drift_1} | {pvalue_1} | {action_1} |
| {feature_2} | {drift_2} | {pvalue_2} | {action_2} |

### ドリフト可視化
![Feature Drift](feature_drift.png)

---

## インシデント・異常

### 重大度別インシデント

- 🚨 **Critical** (P0): {p0_count} 件
- ⚠️ **High** (P1): {p1_count} 件
- 💡 **Medium** (P2): {p2_count} 件
- ℹ️ **Low** (P3): {p3_count} 件

### 主要インシデント詳細

#### [{incident_severity}] {incident_title}
- **発生日時**: {incident_datetime}
- **影響範囲**: {incident_impact}
- **根本原因**: {incident_root_cause}
- **対応状況**: {incident_status}
- **対策**: {incident_action}

---

## 改善提案

1. **{recommendation_1_title}**
   - 背景: {recommendation_1_background}
   - 提案: {recommendation_1_proposal}
   - 期待効果: {recommendation_1_impact}

2. **{recommendation_2_title}**
   - 背景: {recommendation_2_background}
   - 提案: {recommendation_2_proposal}
   - 期待効果: {recommendation_2_impact}

---

## 次週の予定

- [ ] {next_week_action_1}
- [ ] {next_week_action_2}
- [ ] {next_week_action_3}

---

## 付録

### 詳細メトリクス
- 詳細な統計情報は添付のCSVファイルを参照

### 参考リンク
- MLflowダッシュボード: {mlflow_url}
- Grafanaダッシュボード: {grafana_url}
- インシデント管理: {incident_url}
```

### 3. レポート生成コード

```python
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class WeeklyMLReport:
    """週次MLレポート生成クラス"""

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.report_date = datetime.now()
        self.output_dir = Path(f"reports/weekly_{self.report_date.strftime('%Y%m%d')}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_data(self, data_source):
        """
        データソースからメトリクスを読み込む

        Parameters:
        -----------
        data_source : str or dict
            データソース（ファイルパス、DB接続情報、MLflow URI など）
        """
        # 例: ログファイルからの読み込み
        if isinstance(data_source, str) and data_source.endswith('.csv'):
            df = pd.read_csv(data_source)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df[(df['timestamp'] >= self.start_date) &
                    (df['timestamp'] <= self.end_date)]
            return df

        # 例: MLflowからの読み込み
        elif isinstance(data_source, dict) and 'mlflow_uri' in data_source:
            import mlflow
            mlflow.set_tracking_uri(data_source['mlflow_uri'])
            # MLflowからメトリクスを取得する実装
            pass

        return None

    def calculate_metrics(self, df):
        """メトリクスを計算"""
        metrics = {}

        # 総予測数
        metrics['total_predictions'] = len(df)

        # 精度メトリクス（実際の値がある場合）
        if 'actual' in df.columns and 'predicted' in df.columns:
            metrics['avg_accuracy'] = (df['actual'] == df['predicted']).mean()

        # レイテンシ統計
        if 'latency_ms' in df.columns:
            metrics['avg_latency'] = df['latency_ms'].mean()
            metrics['p95_latency'] = df['latency_ms'].quantile(0.95)
            metrics['p99_latency'] = df['latency_ms'].quantile(0.99)

        # エラー率
        if 'status' in df.columns:
            metrics['error_rate'] = (df['status'] == 'error').mean()

        # 日別のスループット
        df['date'] = df['timestamp'].dt.date
        metrics['daily_throughput'] = df.groupby('date').size().mean()

        return metrics

    def compare_with_previous_week(self, current_metrics, previous_df):
        """前週との比較"""
        previous_metrics = self.calculate_metrics(previous_df)

        comparison = {}
        for key in current_metrics:
            if key in previous_metrics:
                current = current_metrics[key]
                previous = previous_metrics[key]
                change = current - previous
                change_pct = (change / previous * 100) if previous != 0 else 0

                comparison[key] = {
                    'current': current,
                    'previous': previous,
                    'change': change,
                    'change_pct': change_pct
                }

        return comparison

    def plot_trends(self, df):
        """トレンドグラフの生成"""

        df['date'] = pd.to_datetime(df['timestamp']).dt.date

        # 1. 精度の推移（日別）
        if 'actual' in df.columns and 'predicted' in df.columns:
            daily_accuracy = df.groupby('date').apply(
                lambda x: (x['actual'] == x['predicted']).mean()
            )

            plt.figure(figsize=(12, 6))
            plt.plot(daily_accuracy.index, daily_accuracy.values, marker='o')
            plt.axhline(y=0.9, color='r', linestyle='--', label='目標値 (90%)')
            plt.title('日別精度推移')
            plt.xlabel('日付')
            plt.ylabel('精度')
            plt.legend()
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(self.output_dir / 'accuracy_trend.png', dpi=300)
            plt.close()

        # 2. 予測数の推移
        daily_volume = df.groupby('date').size()

        plt.figure(figsize=(12, 6))
        plt.bar(daily_volume.index, daily_volume.values)
        plt.title('日別予測数推移')
        plt.xlabel('日付')
        plt.ylabel('予測数')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'prediction_volume.png', dpi=300)
        plt.close()

        # 3. レイテンシの推移
        if 'latency_ms' in df.columns:
            daily_latency = df.groupby('date')['latency_ms'].agg(['mean', 'quantile'])

            plt.figure(figsize=(12, 6))
            plt.plot(daily_latency.index, daily_latency['mean'],
                    marker='o', label='平均')
            plt.fill_between(daily_latency.index,
                            daily_latency['mean'] - daily_latency['mean'].std(),
                            daily_latency['mean'] + daily_latency['mean'].std(),
                            alpha=0.3)
            plt.title('日別レイテンシ推移')
            plt.xlabel('日付')
            plt.ylabel('レイテンシ (ms)')
            plt.legend()
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(self.output_dir / 'latency_trend.png', dpi=300)
            plt.close()

    def detect_drift(self, current_df, reference_df, features):
        """データドリフトの検出"""
        from scipy import stats

        drift_results = []

        for feature in features:
            if feature not in current_df.columns or feature not in reference_df.columns:
                continue

            # KS検定
            statistic, p_value = stats.ks_2samp(
                reference_df[feature].dropna(),
                current_df[feature].dropna()
            )

            drift_detected = p_value < 0.05
            action = "要調査" if drift_detected else "正常"

            drift_results.append({
                'feature': feature,
                'drift_detected': '⚠️ Yes' if drift_detected else '✅ No',
                'p_value': f"{p_value:.4f}",
                'action': action
            })

        return pd.DataFrame(drift_results)

    def generate_report(self, data, template_vars):
        """レポートを生成"""

        # テンプレートの読み込みと変数の置換
        template = """
# 機械学習モデル週次レポート

**レポート期間**: {start_date} 〜 {end_date}
**作成日**: {report_date}

## エグゼクティブサマリー

- 総予測数: {total_predictions:,}
- 平均精度: {avg_accuracy:.2%}
- システム稼働率: {uptime:.2%}

... (残りのテンプレート)
"""

        report_content = template.format(**template_vars)

        # Markdownファイルとして保存
        report_path = self.output_dir / 'weekly_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"レポートを生成しました: {report_path}")

        return report_path

    def convert_to_html(self, markdown_path):
        """MarkdownをHTMLに変換"""
        try:
            import markdown

            with open(markdown_path, 'r', encoding='utf-8') as f:
                md_content = f.read()

            html_content = markdown.markdown(
                md_content,
                extensions=['tables', 'fenced_code', 'toc']
            )

            # CSSスタイルを追加
            styled_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; border-bottom: 2px solid #ddd; padding-bottom: 8px; margin-top: 30px; }}
        h3 {{ color: #666; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

            html_path = markdown_path.with_suffix('.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(styled_html)

            print(f"HTMLレポートを生成しました: {html_path}")
            return html_path

        except ImportError:
            print("markdown パッケージがインストールされていません")
            print("インストール: pip install markdown")
            return None


# 使用例
def generate_weekly_report():
    """週次レポートの生成"""

    # レポート期間の設定
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # レポート生成器の初期化
    reporter = WeeklyMLReport(start_date, end_date)

    # データの読み込み
    current_data = reporter.load_data('logs/predictions.csv')
    previous_data = reporter.load_data('logs/predictions_previous_week.csv')

    # メトリクスの計算
    current_metrics = reporter.calculate_metrics(current_data)
    comparison = reporter.compare_with_previous_week(current_metrics, previous_data)

    # グラフの生成
    reporter.plot_trends(current_data)

    # ドリフト検出
    features = ['feature1', 'feature2', 'feature3']
    drift_df = reporter.detect_drift(current_data, previous_data, features)

    # テンプレート変数の準備
    template_vars = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'report_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'total_predictions': current_metrics['total_predictions'],
        'avg_accuracy': current_metrics.get('avg_accuracy', 0),
        'uptime': 0.999,  # 実際のシステムメトリクスから取得
        # ... その他の変数
    }

    # レポート生成
    report_path = reporter.generate_report(current_data, template_vars)

    # HTML変換
    reporter.convert_to_html(report_path)

    return report_path
```

### 4. 自動化スクリプト

```python
# weekly_report_automation.py
"""
週次レポートの自動生成スクリプト

cronやGitHub Actionsで定期実行する

# crontab の例（毎週月曜日 9:00 に実行）
0 9 * * 1 cd /path/to/project && python weekly_report_automation.py
"""

import logging
from datetime import datetime
from pathlib import Path

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weekly_report.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("週次レポート生成を開始")

        # レポート生成
        report_path = generate_weekly_report()

        logger.info(f"レポート生成完了: {report_path}")

        # オプション: メール送信
        # send_email_report(report_path)

        # オプション: Slackに通知
        # send_slack_notification(report_path)

        return True

    except Exception as e:
        logger.error(f"レポート生成中にエラーが発生: {str(e)}", exc_info=True)
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
```

## Best Practices

1. **テンプレートの標準化**: チーム全体で共通のフォーマットを使用
2. **自動化**: cron、GitHub Actions、Airflowなどで定期実行
3. **バージョン管理**: レポートテンプレートもGitで管理
4. **通知設定**: 重要な指標が閾値を超えた場合は即座に通知
5. **アーカイブ**: 過去のレポートを保存して比較可能に

## Examples

### Example 1: シンプルな週次レポート

```python
from weekly_ml_report import WeeklyMLReport
from datetime import datetime, timedelta

# 今週のレポートを生成
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

reporter = WeeklyMLReport(start_date, end_date)
report_path = generate_weekly_report()
print(f"レポート: {report_path}")
```

### Example 2: 複数モデルのレポート

```python
models = ['model_a', 'model_b', 'model_c']

for model_name in models:
    reporter = WeeklyMLReport(start_date, end_date)
    data = reporter.load_data(f'logs/{model_name}_predictions.csv')
    # ... レポート生成
```

## Notes

- **データプライバシー**: レポートに機密データが含まれないよう注意
- **カスタマイズ**: プロジェクトのニーズに合わせてテンプレートを調整
- **パフォーマンス**: 大量データの場合は集計済みデータを使用
- **アラート**: 異常値は自動的にハイライト
