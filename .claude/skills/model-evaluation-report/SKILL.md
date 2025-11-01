---
name: model-evaluation-report
description: 機械学習モデルの評価レポートを生成。分類・回帰タスクの評価メトリクス、混同行列、特徴量重要度、誤差分析などを含む包括的なレポートを作成します。
---

# Model Evaluation Report

このスキルは、訓練済みモデルの性能を評価し、包括的なレポートを生成します。

## When to Use

以下のような場合にこのスキルを使用してください：
- モデルの性能評価が必要
- ステークホルダーへの報告用レポートを作成したい
- モデルの長所と短所を可視化したい
- 複数モデルの比較が必要
- 本番環境へのデプロイ前の最終評価

## Instructions

### 1. タスクタイプの確認

ユーザーに確認：
- タスクの種類は？（2値分類、多クラス分類、回帰、ランキングなど）
- 評価データセットは用意されているか？
- 特に重視するメトリクスは？
- レポート形式の希望は？（Jupyter Notebook、HTML、PDF、Markdownなど）

### 2. 評価メトリクスの選択

#### 分類タスク

**2値分類**:
- Accuracy, Precision, Recall, F1-Score
- ROC-AUC, PR-AUC
- 混同行列
- 閾値最適化

**多クラス分類**:
- Accuracy, Macro/Micro/Weighted F1
- 混同行列
- クラスごとの Precision/Recall
- Top-k Accuracy

```python
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve,
)
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_classification_model(y_true, y_pred, y_prob=None, labels=None):
    """分類モデルの評価"""
    results = {}

    # 基本メトリクス
    results['accuracy'] = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='weighted'
    )
    results['precision'] = precision
    results['recall'] = recall
    results['f1_score'] = f1

    # 混同行列
    cm = confusion_matrix(y_true, y_pred)
    results['confusion_matrix'] = cm

    # ROC-AUC (2値分類の場合)
    if y_prob is not None and len(set(y_true)) == 2:
        results['roc_auc'] = roc_auc_score(y_true, y_prob)

    # 混同行列の可視化
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=labels, yticklabels=labels)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')

    return results
```

#### 回帰タスク

**メトリクス**:
- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- R² Score
- MAPE (Mean Absolute Percentage Error)

```python
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

def evaluate_regression_model(y_true, y_pred):
    """回帰モデルの評価"""
    results = {}

    results['mae'] = mean_absolute_error(y_true, y_pred)
    results['mse'] = mean_squared_error(y_true, y_pred)
    results['rmse'] = np.sqrt(results['mse'])
    results['r2_score'] = r2_score(y_true, y_pred)

    # MAPE
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    results['mape'] = mape

    # 予測値 vs 実測値のプロット
    plt.figure(figsize=(10, 6))
    plt.scatter(y_true, y_pred, alpha=0.5)
    plt.plot([y_true.min(), y_true.max()],
             [y_true.min(), y_true.max()],
             'r--', lw=2)
    plt.xlabel('True Values')
    plt.ylabel('Predictions')
    plt.title('Predictions vs True Values')
    plt.tight_layout()
    plt.savefig('predictions_vs_true.png', dpi=300, bbox_inches='tight')

    # 残差プロット
    residuals = y_true - y_pred
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, residuals, alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.title('Residual Plot')
    plt.tight_layout()
    plt.savefig('residual_plot.png', dpi=300, bbox_inches='tight')

    return results
```

### 3. 特徴量重要度の分析

```python
def plot_feature_importance(model, feature_names, top_n=20):
    """特徴量重要度のプロット"""

    # モデルタイプに応じて重要度を取得
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
    elif hasattr(model, 'coef_'):
        importances = np.abs(model.coef_).flatten()
    else:
        print("このモデルは特徴量重要度をサポートしていません")
        return

    # 重要度でソート
    indices = np.argsort(importances)[::-1][:top_n]

    # プロット
    plt.figure(figsize=(12, 8))
    plt.barh(range(top_n), importances[indices])
    plt.yticks(range(top_n), [feature_names[i] for i in indices])
    plt.xlabel('Importance')
    plt.title(f'Top {top_n} Feature Importances')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
```

### 4. エラー分析

```python
def error_analysis(X, y_true, y_pred, feature_names, n_samples=10):
    """予測エラーの詳細分析"""

    # エラーの大きいサンプルを特定
    errors = np.abs(y_true - y_pred)
    worst_indices = np.argsort(errors)[::-1][:n_samples]

    print("=== 最もエラーの大きいサンプル ===\n")
    for idx in worst_indices:
        print(f"Sample {idx}:")
        print(f"  True: {y_true[idx]}")
        print(f"  Predicted: {y_pred[idx]}")
        print(f"  Error: {errors[idx]}")
        print(f"  Features: {dict(zip(feature_names, X[idx]))}")
        print()
```

### 5. レポートテンプレート生成

#### Markdownレポート

```python
def generate_markdown_report(results, model_name, dataset_name):
    """Markdown形式のレポート生成"""

    report = f"""# Model Evaluation Report

## Model Information
- **Model Name**: {model_name}
- **Dataset**: {dataset_name}
- **Evaluation Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Performance Metrics

### Overall Performance
"""

    for metric, value in results.items():
        if not isinstance(value, np.ndarray):
            report += f"- **{metric}**: {value:.4f}\n"

    report += """
## Visualizations

### Confusion Matrix
![Confusion Matrix](confusion_matrix.png)

### Feature Importance
![Feature Importance](feature_importance.png)

## Insights and Recommendations

[このセクションにモデルの長所、短所、改善提案を記載]

## Next Steps

- [ ] ハイパーパラメータチューニング
- [ ] 追加特徴量エンジニアリング
- [ ] アンサンブル手法の検討
- [ ] 本番環境でのA/Bテスト計画

---
*Generated by ML Evaluation Report Skill*
"""

    with open('evaluation_report.md', 'w') as f:
        f.write(report)

    print("レポートを evaluation_report.md に保存しました")
```

### 6. 複数モデルの比較

```python
import pandas as pd

def compare_models(models_results):
    """複数モデルの性能比較"""

    df = pd.DataFrame(models_results).T
    df = df.round(4)

    # 可視化
    df.plot(kind='bar', figsize=(12, 6))
    plt.title('Model Comparison')
    plt.xlabel('Models')
    plt.ylabel('Score')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')

    return df
```

## Best Practices

1. **メトリクスの選択**: タスクに適したメトリクスを使用
2. **可視化**: 数値だけでなくグラフで理解しやすく
3. **誤差分析**: なぜ間違えたのかを分析
4. **再現性**: 評価スクリプトを保存し、いつでも再実行可能に
5. **コンテキスト**: ビジネス目標との関連を明記

## Examples

### Example 1: 分類モデルの評価レポート

```python
# モデルの予測
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# 評価
results = evaluate_classification_model(
    y_test, y_pred, y_prob,
    labels=['Class 0', 'Class 1']
)

# 特徴量重要度
plot_feature_importance(model, feature_names)

# レポート生成
generate_markdown_report(results, 'RandomForest', 'Customer Churn')
```

### Example 2: 回帰モデルの評価

```python
# 予測
y_pred = model.predict(X_test)

# 評価
results = evaluate_regression_model(y_test, y_pred)

# エラー分析
error_analysis(X_test, y_test, y_pred, feature_names)

# レポート生成
generate_markdown_report(results, 'XGBoost', 'House Prices')
```

## Notes

- **不均衡データ**: クラス不均衡がある場合は、適切なメトリクス（F1、AUC-PR）を使用
- **クロスバリデーション**: 可能な場合はCV結果も含める
- **統計的有意性**: 複数モデル比較時は統計的検定を実施
- **解釈性**: SHAP値などで予測の説明可能性を追加
