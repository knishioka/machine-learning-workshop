# 応用編: マルチステップ自律実行

Agent SDK のエージェントループを活用した、複雑なタスクの自律的実行デモです。

## 📚 このセクションで学べること

- マルチステップタスクの自律的実行
- エージェントループの威力
- 複数ツールの組み合わせ
- Web検索の活用
- 高度なコード解析
- 自己判断による優先順位付け

## 🎯 デモ一覧

### 1. research_agent.py - リサーチエージェント

**所要時間: 10-15分**

```bash
# 技術トレンド調査
python examples/03_advanced/research_agent.py "2025年のAI技術トレンド"

# プログラミング言語比較
python examples/03_advanced/research_agent.py "Python vs Rust パフォーマンス"

# ライブラリ選定
python examples/03_advanced/research_agent.py "FastAPI vs Flask 比較"
```

**何を学ぶか:**
- Web検索ツールの活用
- 情報収集→分析→統合の自律的実行
- マルチステップのエージェントループ
- 構造化されたレポート生成

**期待される動作:**

```
┌─ Claude Agent SDK - Research Agent ─┐
│ テーマ: 2025年のAI技術トレンド       │
└─────────────────────────────────────┘

🔍 リサーチを開始します...

🌐 Web検索を実行中...
💭 検索結果を分析しています...
🌐 Web検索を実行中...
💭 情報を統合しています...
📝 レポートを作成中...

┌─ 📊 リサーチレポート ─┐
│                        │
│ # 2025年のAI技術トレンド│
│                        │
│ ## エグゼクティブサマリー│
│ 2025年のAI技術は...   │
│                        │
│ ## 主要な発見事項      │
│ 1. ...                │
│ 2. ...                │
│ ...                   │
└────────────────────────┘

✅ レポートが保存されました: research_report_20251018_143022.md
```

**コードのポイント:**

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

# Web検索を含むマルチステップタスク
options = ClaudeAgentOptions(
    allowed_tools=["WebSearch", "Write"],
)

async with ClaudeSDKClient(options=options) as client:
    await client.query(task)

    async for message in client.receive_response():
        # エージェントが自律的に:
        # 1. Web検索でデータ収集
        # 2. 結果を分析
        # 3. 追加検索が必要か判断
        # 4. 情報を統合
        # 5. レポート生成・保存
        pass
```

**生成されるレポート例:**

```markdown
# 2025年のAI技術トレンド

## エグゼクティブサマリー
2025年のAI技術は、大規模言語モデルの進化、
エージェント技術の実用化、マルチモーダルAIの普及が
主要なトレンドとなっています...

## 主要な発見事項
1. **Agent SDK の台頭**: 自律的なAIエージェントの開発が...
2. **マルチモーダル統合**: テキスト、画像、音声を...
3. **エッジAI**: オンデバイスでの...

## 詳細分析
...

## 情報源
- [Source 1](https://...)
- [Source 2](https://...)

## 結論と推奨事項
...
```

---

### 2. code_reviewer.py - コードレビューエージェント

**所要時間: 10-15分**

```bash
# 特定のファイルをレビュー
python examples/03_advanced/code_reviewer.py script.py

# ディレクトリ全体をレビュー
python examples/03_advanced/code_reviewer.py .

# カレントディレクトリをレビュー（自動修正付き）
python examples/03_advanced/code_reviewer.py . --auto-fix
```

**何を学ぶか:**
- コード解析の自動化
- マルチステップ実行（分析→提案→実装）
- エージェントによる品質評価
- 優先順位付けと判断

**期待される動作:**

```
┌─ Claude Agent SDK - Code Reviewer ─┐
│ 対象: example.py                    │
│ 自動修正: 無効                      │
└─────────────────────────────────────┘

🔍 コードレビューを開始します...

📖 読み取り中: example.py
💭 コード構造を分析しています...
💭 ベストプラクティスと照らし合わせています...
💭 改善提案をまとめています...

┌─ 📋 レビューレポート ─┐
│                        │
│ ## サマリー            │
│ 全体評価: B+ (良好)   │
│ 主要な問題: 3件       │
│                        │
│ ## 重要な問題点        │
│ 1. [高] 関数が長すぎる│
│ 2. [中] エラー処理不足│
│ 3. [中] 変数名が不明瞭│
│                        │
│ ## 詳細な改善提案      │
│ ...                   │
└────────────────────────┘

✅ レビューレポートが保存されました: code_review_report.md
```

**コードのポイント:**

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

# コード分析から改善提案まで自律実行
options = ClaudeAgentOptions(
    allowed_tools=["Glob", "Read", "Write"] if auto_fix else ["Glob", "Read"],
)

async with ClaudeSDKClient(options=options) as client:
    await client.query(task)

    async for message in client.receive_response():
        # エージェントが自律的に:
        # 1. コードを読み取り
        # 2. 品質を分析
        # 3. 問題点を特定
        # 4. 重要度を評価
        # 5. 改善案を生成
        # 6. (オプション) 修正を実装
        pass
```

**生成されるレビューレポート例:**

```markdown
# Code Review Report

**Target:** example.py

## サマリー
- **全体評価**: B+ (良好)
- **コード行数**: 150行
- **関数数**: 8
- **主要な問題**: 3件

## 重要な問題点

### 1. [高] 関数が長すぎる (process_data関数)

**問題:**
`process_data` 関数が70行と長く、複数の責任を持っています。

**現状のコード:**
\`\`\`python
def process_data(data):
    # 70行の処理...
\`\`\`

**改善案:**
\`\`\`python
def process_data(data):
    validated_data = validate_data(data)
    cleaned_data = clean_data(validated_data)
    return transform_data(cleaned_data)

def validate_data(data):
    # バリデーション処理
    pass

def clean_data(data):
    # クリーニング処理
    pass
\`\`\`

### 2. [中] エラーハンドリング不足
...
```

---

## 🔑 重要な概念

### 1. エージェントループ

エージェントが自律的に判断・実行するサイクル:

```
┌─────────────────┐
│ コンテキスト収集 │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ アクション実行   │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ 結果の検証      │
└────────┬────────┘
         │
         v
    もう一度？
    yes → ループ
    no → 完了
```

### 2. マルチステップ実行

複雑なタスクを複数のステップに分解して自律実行:

**リサーチエージェントの例:**
1. テーマ理解 → キーワード抽出
2. Web検索 → 結果収集
3. 追加検索判断 → 実行（必要に応じて）
4. 情報統合 → 分析
5. レポート生成 → 保存

**コードレビューの例:**
1. ファイル読み取り → 構文解析
2. 品質分析 → 問題点抽出
3. 重要度評価 → 優先順位付け
4. 改善案生成 → レポート作成
5. （オプション）修正実装 → 検証

### 3. 自律的判断

エージェントが状況に応じて判断:
- 追加情報が必要か？
- どのツールを使うべきか？
- 次に何をすべきか？
- タスクは完了したか？

### 4. ツールの組み合わせ

複数のツールを状況に応じて使い分け:

| タスク | 使用ツール |
|--------|-----------|
| リサーチ | WebSearch → 複数回 → Write |
| コードレビュー | Glob → Read（複数ファイル） → Write |
| 情報統合 | Read（複数） → 分析 → Write |

---

## 💡 「すごさ」のポイント

### 1. 真の自律性

単なるツール呼び出しではなく:
- **状況判断**: 何が必要か自分で判断
- **計画立案**: ステップを自分で設計
- **実行管理**: 進捗を自分で管理
- **品質確認**: 結果を自分で検証

### 2. 複雑性の隠蔽

ユーザーは:
```python
async for message in query(prompt="リサーチして"):
    # たった1行の指示
    pass
```

エージェントは内部で:
1. 10回以上のツール呼び出し
2. 複数ステップの計画・実行
3. 結果の統合・分析
4. レポート生成

### 3. 適応性

同じコードで異なるタスクに対応:
- 技術トレンド調査
- プログラミング言語比較
- ライブラリ選定
- 市場分析
- etc.

### 4. 実用性

デモだけでなく、実際の業務で使える:
- 定期的な技術調査の自動化
- コードレビューの効率化
- 情報収集タスクの代行
- ドキュメント作成の支援

---

## 🚀 次のステップ

応用編を理解したら、次はMCP連携編に進みましょう:

```bash
cd ../04_mcp
python mcp_example.py
```

MCP連携編では、外部サービスとの統合による拡張性を体験します。

---

## 🎨 カスタマイズ例

### リサーチエージェントのカスタマイズ

```python
# 競合分析タスク
task = """
以下の企業の競合分析を実施:
- 企業A, 企業B, 企業C

各社の:
1. 主力製品・サービス
2. 市場シェア
3. 強み・弱み
4. 最近の動向

比較表とSWOT分析を含むレポートを作成
"""
```

### コードレビューのカスタマイズ

```python
# セキュリティ重視のレビュー
task = """
セキュリティ観点を重視してコードをレビュー:

重点項目:
1. SQL injection
2. XSS vulnerabilities
3. 認証・認可の問題
4. 機密情報の露出
5. 安全でないデシリアライゼーション

OWASP Top 10 に基づいて評価
"""
```

---

## ❓ トラブルシューティング

### Web検索が失敗する

```
WebSearchError: ...
```

**解決方法:**
- インターネット接続を確認
- APIキーの権限を確認
- 検索クエリを調整

### 処理時間が長い

```
タスクが10分以上かかる
```

**解決方法:**
- タスクの範囲を絞る
- 「簡潔に」など指示を追加
- ファイル数を制限

### メモリ不足

```
大量のファイルを処理してメモリ不足
```

**解決方法:**
- 処理対象を絞る
- バッチ処理に分割
- 除外パターンを追加

---

## 📖 参考資料

- [Web検索ツール詳細](https://docs.claude.com/en/api/agent-sdk/tools#web-search)
- [エージェントループの設計](https://docs.claude.com/en/api/agent-sdk/concepts#agent-loop)
- メインREADME: [../../README.md](../../README.md)
