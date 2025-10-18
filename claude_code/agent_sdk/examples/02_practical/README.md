# 実用編: ファイル操作の威力

Agent SDK のファイル操作ツールを活用した実践的なデモです。

## 📚 このセクションで学べること

- ファイル操作ツール（Glob, Read, Write）の使い方
- ツール権限管理（allowedTools）
- 作業ディレクトリの指定（cwd）
- 実用的なタスクの自動化
- エージェントによるコード理解と生成

## 🎯 デモ一覧

### 1. project_analyzer.py - プロジェクト構造分析

**所要時間: 5-7分**

```bash
# カレントディレクトリを分析
python examples/02_practical/project_analyzer.py .

# 特定のディレクトリを分析
python examples/02_practical/project_analyzer.py /path/to/project
```

**何を学ぶか:**
- Glob ツールでファイルパターンマッチング
- Read ツールでファイル内容の読み取り
- allowedTools による権限制御
- プロジェクト全体の自動分析

**期待される出力:**
```
┌─ Claude Agent SDK - Project Analyzer ─┐
│ 対象ディレクトリ: .                   │
└───────────────────────────────────────┘

📝 分析タスクを実行中...

🔧 Glob を使用中...
💭 Pythonファイルを検索しています...
🔧 Read を使用中...
💭 主要ファイルの内容を確認中...

┌─ 📊 分析レポート ─┐
│                   │
│ プロジェクト概要  │
│ ファイル数: 15    │
│ 主要言語: Python  │
│ ...               │
└───────────────────┘
```

**コードのポイント:**
```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

# ツールの権限管理と作業ディレクトリ指定
options = ClaudeAgentOptions(
    allowed_tools=["Glob", "Read"],  # 使用を許可するツール
    cwd=target_dir,  # 作業ディレクトリ
)

async with ClaudeSDKClient(options=options) as client:
    await client.query(task)

    async for message in client.receive_response():
        if isinstance(message, ResultMessage):
            if message.result:
                print(message.result)
```

---

### 2. readme_generator.py - README自動生成

**所要時間: 7-10分**

```bash
# カレントディレクトリのREADME生成
python examples/02_practical/readme_generator.py .

# 特定のディレクトリのREADME生成
python examples/02_practical/readme_generator.py /path/to/project
```

**何を学ぶか:**
- Glob, Read, Write の組み合わせ活用
- エージェントによるコード理解
- 自動ドキュメント生成
- ファイル書き込み

**期待される出力:**
```
┌─ Claude Agent SDK - README Generator ─┐
│ 対象: .                                │
│ 出力: README_GENERATED.md              │
└───────────────────────────────────────┘

📝 README生成タスクを実行中...

🔧 Glob を使用中...
💭 ソースファイルを検索中...
🔧 Read を使用中...
💭 主要な関数を読み取り中...
📝 ファイル書き込み中: README_GENERATED.md

✅ README が生成されました: README_GENERATED.md
```

**生成されるREADME例:**
```markdown
# プロジェクト名

## 概要
このプロジェクトは...

## 主な機能
- 機能1: ...
- 機能2: ...

## インストール
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## 使用方法
\`\`\`python
from module import function
...
\`\`\`
```

**コードのポイント:**
```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from claude_agent_sdk.types import AssistantMessage, ToolUseBlock

# Read と Write を組み合わせたファイル操作
options = ClaudeAgentOptions(
    allowed_tools=["Glob", "Read", "Write"],
    cwd=target_dir,
)

async with ClaudeSDKClient(options=options) as client:
    await client.query(task)

    async for message in client.receive_response():
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock) and block.name == "Write":
                    print(f"ファイル書き込み: {block.input['file_path']}")
```

---

## 🔑 重要な概念

### 1. ファイル操作ツール

Agent SDK は強力なファイル操作ツールを提供します:

| ツール | 機能 | 使用例 |
|--------|------|--------|
| **Glob** | ファイル検索 | `*.py`, `src/**/*.ts` |
| **Read** | ファイル読み取り | ソースコード、設定ファイル |
| **Write** | ファイル書き込み | レポート、ドキュメント生成 |
| **Edit** | ファイル編集 | コード修正、リファクタリング |

### 2. ツール権限管理

`allowed_tools` でエージェントが使用できるツールを制御:

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    allowed_tools=["Glob", "Read"],  # 読み取り専用
    # allowed_tools=["Glob", "Read", "Write"],  # 書き込みも許可
)
```

**セキュリティのポイント:**
- デフォルトでは全ツールが利用可能
- `allowedTools` で明示的に制限すると安全
- 特に Write や Edit は慎重に許可

### 3. 作業ディレクトリ

`cwd` で作業ディレクトリを指定:

```python
options = ClaudeAgentOptions(
    cwd="/path/to/project",  # このディレクトリが基準
)
```

### 4. エージェントのコード理解

エージェントは以下を自動的に実行できます:
- ファイル構造の理解
- コードの意味解析
- 関数やクラスの抽出
- 依存関係の推測
- ドキュメント生成

---

## 💡 「すごさ」のポイント

### 1. 複雑なタスクの自動化

わずか数行の指示で、エージェントが:
1. 適切なファイルを検索
2. 必要な情報を読み取り
3. 分析・統合
4. レポートやドキュメントを生成

### 2. コンテキストの理解

エージェントは単にファイルを読むだけでなく:
- コードの目的を理解
- 関数の役割を推測
- プロジェクト全体の構造を把握
- 適切な説明文を生成

### 3. 柔軟な対応

- プロジェクトの規模に応じた分析
- 異なる言語やフレームワークに対応
- 既存ファイルの有無に応じた処理

### 4. 実用性

これらのデモは実際の開発でも使えます:
- プロジェクト引き継ぎ時の構造理解
- ドキュメント作成の自動化
- コードベースの分析
- 技術負債の可視化

---

## 🚀 次のステップ

実用編を理解したら、次は応用編に進みましょう:

```bash
cd ../03_advanced
python research_agent.py
```

応用編では、マルチステップの自律的実行とエージェントループの威力を体験します。

---

## 🎨 応用例

### カスタムタスクの例

```python
# 特定の問題を探すタスク
task = """
このプロジェクト内で、以下を検索・分析してください:
1. TODO コメントを全て抽出
2. セキュリティ上の懸念事項を特定
3. テストカバレッジが不足している箇所を推測
4. 改善提案をまとめたレポートを生成
"""
```

### 複数プロジェクトの比較

```python
# 2つのプロジェクトを比較
task = """
プロジェクトAとプロジェクトBを比較し、
以下の観点でレポートを作成してください:
- アーキテクチャの違い
- 使用技術の違い
- コード品質の比較
"""
```

---

## ❓ トラブルシューティング

### ファイルが見つからない

```
エージェントが「ファイルが見つかりません」と報告
```

**解決方法:**
- `cwd` パラメータが正しく設定されているか確認
- 対象ディレクトリが存在するか確認
- 相対パスと絶対パスを確認

### 書き込み権限エラー

```
PermissionError: [Errno 13] Permission denied
```

**解決方法:**
- ディレクトリの書き込み権限を確認
- 別の出力先を指定
- `allowedTools` に "Write" が含まれているか確認

### 処理が遅い

```
大量のファイルがあり、処理に時間がかかる
```

**解決方法:**
- タスク指示で対象ファイルを絞る
- 除外パターンを明示（venv, node_modules など）
- サンプリング分析を指示

---

## 📖 参考資料

- [ファイル操作ツール詳細](https://docs.claude.com/en/api/agent-sdk/tools#file-operations)
- [権限管理のベストプラクティス](https://docs.claude.com/en/api/agent-sdk/permissions)
- メインREADME: [../../README.md](../../README.md)
