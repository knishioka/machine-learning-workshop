---
name: data-analysis-starter
description: データ分析の開始をサポート。データの読み込み、基本統計、可視化、データクリーニングなどのEDA（探索的データ分析）テンプレートを生成します。
---

# Data Analysis Starter

このスキルは、新しいデータセットの探索的データ分析（EDA）を開始するためのテンプレートとコードを生成します。

## When to Use

以下のような場合にこのスキルを使用してください：
- 新しいデータセットの分析を始める
- データの概要を把握したい
- データクリーニングが必要
- データの可視化を行いたい
- 特徴量エンジニアリングの前段階として

## Instructions

### 1. データセットの情報収集

ユーザーに確認：
- データセットのファイル形式は？（CSV、Excel、JSON、Parquet、SQL など）
- データセットのサイズは？
- 分析の目的は？（予測モデル構築、レポート作成、データ理解など）
- 特に注目したい変数はあるか？

### 2. データ読み込みテンプレート

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

# 設定
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

# データの読み込み
def load_data(filepath, **kwargs):
    """
    データを読み込む

    Parameters:
    -----------
    filepath : str or Path
        データファイルのパス
    **kwargs : dict
        pandas読み込み関数への追加引数

    Returns:
    --------
    pd.DataFrame
    """
    filepath = Path(filepath)

    if filepath.suffix == '.csv':
        return pd.read_csv(filepath, **kwargs)
    elif filepath.suffix in ['.xls', '.xlsx']:
        return pd.read_excel(filepath, **kwargs)
    elif filepath.suffix == '.json':
        return pd.read_json(filepath, **kwargs)
    elif filepath.suffix == '.parquet':
        return pd.read_parquet(filepath, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")

# データの読み込み
df = load_data('data/your_dataset.csv')
print(f"データセット読み込み完了: {df.shape[0]} 行, {df.shape[1]} 列")
```

### 3. 基本的なデータ確認

```python
def basic_data_overview(df):
    """データセットの基本情報を表示"""

    print("=" * 80)
    print("データセット基本情報")
    print("=" * 80)

    # 形状
    print(f"\n【データ形状】")
    print(f"行数: {df.shape[0]:,}")
    print(f"列数: {df.shape[1]:,}")

    # 最初の数行
    print(f"\n【データサンプル】")
    display(df.head())

    # データ型
    print(f"\n【データ型】")
    print(df.dtypes)

    # 基本統計量
    print(f"\n【基本統計量】")
    display(df.describe(include='all').T)

    # 欠損値
    print(f"\n【欠損値】")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        '欠損数': missing,
        '欠損率(%)': missing_pct
    }).sort_values('欠損数', ascending=False)
    print(missing_df[missing_df['欠損数'] > 0])

    # ユニーク値の数
    print(f"\n【ユニーク値の数】")
    nunique = df.nunique().sort_values(ascending=False)
    print(nunique)

    # メモリ使用量
    print(f"\n【メモリ使用量】")
    print(f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# 実行
basic_data_overview(df)
```

### 4. データ可視化テンプレート

#### 数値変数の分布

```python
def plot_numeric_distributions(df, figsize=(20, 15)):
    """数値変数の分布を可視化"""

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    n_cols = len(numeric_cols)

    if n_cols == 0:
        print("数値変数がありません")
        return

    n_rows = (n_cols + 2) // 3
    fig, axes = plt.subplots(n_rows, 3, figsize=figsize)
    axes = axes.flatten()

    for idx, col in enumerate(numeric_cols):
        ax = axes[idx]

        # ヒストグラム + KDE
        df[col].hist(bins=30, ax=ax, alpha=0.7, edgecolor='black')
        ax.set_title(f'{col}\n平均: {df[col].mean():.2f}, 中央値: {df[col].median():.2f}')
        ax.set_xlabel(col)
        ax.set_ylabel('頻度')

        # 統計情報を追加
        ax.axvline(df[col].mean(), color='red', linestyle='--', label='平均')
        ax.axvline(df[col].median(), color='green', linestyle='--', label='中央値')
        ax.legend()

    # 余分な軸を非表示
    for idx in range(n_cols, len(axes)):
        axes[idx].set_visible(False)

    plt.tight_layout()
    plt.savefig('numeric_distributions.png', dpi=300, bbox_inches='tight')
    plt.show()

plot_numeric_distributions(df)
```

#### カテゴリ変数の分布

```python
def plot_categorical_distributions(df, max_categories=20, figsize=(20, 15)):
    """カテゴリ変数の分布を可視化"""

    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    n_cols = len(categorical_cols)

    if n_cols == 0:
        print("カテゴリ変数がありません")
        return

    n_rows = (n_cols + 1) // 2
    fig, axes = plt.subplots(n_rows, 2, figsize=figsize)
    axes = axes.flatten()

    for idx, col in enumerate(categorical_cols):
        ax = axes[idx]

        # 値のカウント
        value_counts = df[col].value_counts().head(max_categories)

        # 棒グラフ
        value_counts.plot(kind='barh', ax=ax)
        ax.set_title(f'{col}\n(ユニーク値: {df[col].nunique()})')
        ax.set_xlabel('頻度')

        # パーセンテージを追加
        total = len(df)
        for i, v in enumerate(value_counts):
            ax.text(v, i, f' {v} ({v/total*100:.1f}%)', va='center')

    # 余分な軸を非表示
    for idx in range(n_cols, len(axes)):
        axes[idx].set_visible(False)

    plt.tight_layout()
    plt.savefig('categorical_distributions.png', dpi=300, bbox_inches='tight')
    plt.show()

plot_categorical_distributions(df)
```

#### 相関分析

```python
def plot_correlation_matrix(df, figsize=(12, 10)):
    """相関行列のヒートマップ"""

    numeric_df = df.select_dtypes(include=[np.number])

    if numeric_df.shape[1] < 2:
        print("相関分析には2つ以上の数値変数が必要です")
        return

    corr = numeric_df.corr()

    # マスク（上三角を非表示）
    mask = np.triu(np.ones_like(corr, dtype=bool))

    plt.figure(figsize=figsize)
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
                cmap='coolwarm', center=0,
                square=True, linewidths=1)
    plt.title('相関行列', fontsize=16)
    plt.tight_layout()
    plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()

    # 強い相関を持つペアを表示
    print("\n【強い相関を持つ変数ペア（|r| > 0.7）】")
    corr_pairs = []
    for i in range(len(corr.columns)):
        for j in range(i+1, len(corr.columns)):
            if abs(corr.iloc[i, j]) > 0.7:
                corr_pairs.append({
                    '変数1': corr.columns[i],
                    '変数2': corr.columns[j],
                    '相関係数': corr.iloc[i, j]
                })

    if corr_pairs:
        print(pd.DataFrame(corr_pairs))
    else:
        print("強い相関を持つペアはありません")

plot_correlation_matrix(df)
```

### 5. データクリーニング

```python
def data_cleaning_report(df):
    """データクリーニングが必要な項目を特定"""

    print("=" * 80)
    print("データクリーニングレポート")
    print("=" * 80)

    # 1. 欠損値
    print("\n【1. 欠損値の処理が必要な列】")
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0].sort_values(ascending=False)
    if len(missing_cols) > 0:
        for col, count in missing_cols.items():
            print(f"  - {col}: {count} ({count/len(df)*100:.2f}%)")
    else:
        print("  欠損値なし ✓")

    # 2. 重複行
    print("\n【2. 重複行】")
    n_duplicates = df.duplicated().sum()
    print(f"  重複行数: {n_duplicates}")
    if n_duplicates > 0:
        print("  → df.drop_duplicates() で削除を検討")

    # 3. データ型の不整合
    print("\n【3. データ型の確認】")
    for col in df.columns:
        if df[col].dtype == 'object':
            # 数値に変換可能かチェック
            try:
                pd.to_numeric(df[col], errors='coerce')
                n_converted = df[col].notna().sum() - pd.to_numeric(df[col], errors='coerce').notna().sum()
                if n_converted > 0:
                    print(f"  - {col}: 数値変換で {n_converted} 件のエラー")
            except:
                pass

    # 4. 外れ値
    print("\n【4. 外れ値の検出（IQR法）】")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)).sum()
        if outliers > 0:
            print(f"  - {col}: {outliers} 件 ({outliers/len(df)*100:.2f}%)")

    # 5. 定数列（分散が0の列）
    print("\n【5. 定数列（分散が0の列）】")
    constant_cols = [col for col in numeric_cols if df[col].nunique() == 1]
    if constant_cols:
        print(f"  定数列: {constant_cols}")
        print("  → これらの列は削除を検討")
    else:
        print("  定数列なし ✓")

data_cleaning_report(df)
```

### 6. 自動EDAレポート生成

```python
def generate_eda_report(df, output_file='eda_report.html'):
    """
    包括的なEDAレポートを生成
    （pandas-profilingまたはydata-profilingを使用）
    """
    try:
        from ydata_profiling import ProfileReport

        profile = ProfileReport(df,
                                title="探索的データ分析レポート",
                                explorative=True,
                                dark_mode=False)
        profile.to_file(output_file)
        print(f"EDAレポートを {output_file} に保存しました")

    except ImportError:
        print("ydata-profiling がインストールされていません")
        print("インストール: pip install ydata-profiling")

# 使用例
# generate_eda_report(df)
```

## Best Practices

1. **段階的な分析**: 全体把握 → 詳細分析 → 仮説検証の順で進める
2. **可視化優先**: 数値だけでなく、必ずグラフで確認
3. **ドメイン知識**: データの背景を理解する
4. **再現性**: すべてのステップをコード化
5. **ドキュメント**: 発見事項をマークダウンで記録

## Examples

### Example 1: 顧客データの分析開始

```python
# データ読み込み
df = load_data('data/customers.csv')

# 基本情報
basic_data_overview(df)

# 可視化
plot_numeric_distributions(df)
plot_categorical_distributions(df)
plot_correlation_matrix(df)

# クリーニング確認
data_cleaning_report(df)
```

### Example 2: 時系列データの分析

```python
# データ読み込みと日付変換
df = load_data('data/sales.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

# 時系列プロット
plt.figure(figsize=(15, 6))
df['sales'].plot()
plt.title('売上推移')
plt.xlabel('日付')
plt.ylabel('売上')
plt.savefig('sales_timeseries.png')

# 季節性の確認
df['month'] = df.index.month
df.groupby('month')['sales'].mean().plot(kind='bar')
plt.title('月別平均売上')
plt.savefig('monthly_sales.png')
```

## Notes

- **大規模データ**: メモリに収まらない場合は、chunksize や Dask を使用
- **日本語対応**: matplotlibで日本語を使用する場合はフォント設定が必要
- **対話的分析**: Jupyter NotebookやJupyterLabの使用を推奨
- **バージョン管理**: 分析ノートブックもGitで管理
