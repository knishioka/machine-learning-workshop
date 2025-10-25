# MCP連携編: Context7によるリアルタイムドキュメント取得

Context7 MCPサーバーを使用して、最新のライブラリドキュメントをリアルタイムで取得し、Agent SDKに統合するデモです。

## 📚 このセクションで学べること

- Context7 MCPの基本概念と利点
- Agent SDKでのMCPサーバー設定方法
- 外部MCPサーバーとの統合
- リアルタイムドキュメント取得の実装
- 拡張可能なエージェント設計

## 🎯 Context7 MCP とは？

Context7は、AIエージェントに**最新のバージョン固有のドキュメント**とコード例を動的に提供するMCPサーバーです。

### 解決する問題

従来のLLMは訓練データが古く、以下の問題がありました：

- 🚫 古いトレーニングデータによる古いコード生成
- 🚫 存在しないAPIの幻覚
- 🚫 バージョン不一致によるエラー
- 🚫 ドキュメント検索の手間

Context7はこれらを解決し、**常に最新のドキュメント**を提供します。

### 主な機能

1. **リアルタイムドキュメント取得**: 最新の公式ドキュメントを動的に取得
2. **バージョン固有のコード例**: 指定バージョンの正確なコード例
3. **最新のAPI仕様**: 最新のAPIリファレンス
4. **プロンプトへの自動統合**: "use context7" で簡単に利用

### 提供されるツール

| ツール名 | 用途 | パラメータ |
|---------|------|-----------|
| **resolve-library-id** | ライブラリ名をContext7 IDに変換 | `libraryName` (必須) |
| **get-library-docs** | ライブラリのドキュメントを取得 | `libraryId` (必須)<br>`topic` (オプション)<br>`tokens` (オプション) |

### サポートされているライブラリ例

- **JavaScript/TypeScript**: Next.js, React, Vue, Node.js, Express, TypeScript
- **Python**: FastAPI, Django, Flask, Pandas, NumPy
- **CSS**: Tailwind CSS
- その他多数のライブラリ

## 🚀 セットアップ

### 前提条件

- **Python 3.8+**
- **Node.js 18+** (Context7 MCPサーバーの実行に必要)
- **npm または npx**

```bash
# Node.jsのバージョン確認
node --version  # 18以上が必要
npx --version
```

### ステップ1: Python環境の準備

```bash
# 依存関係がインストール済みであることを確認
pip install claude-agent-sdk rich python-dotenv

# APIキーの設定
# .env ファイルに ANTHROPIC_API_KEY を設定
```

### ステップ2: Context7の確認

Context7は`npx`で自動的にダウンロード・実行されるため、事前のインストールは不要です。

ただし、Claude Desktopなどで恒久的に使用したい場合は、以下のコマンドでインストールできます：

```bash
# オプション: Claude Desktopへのインストール
npx -y @smithery/cli install @upstash/context7-mcp --client claude
```

### ステップ3: デモの実行

```bash
python examples/04_mcp/mcp_example.py
```

## 📋 デモの動作

### 実行フロー

1. **初期化**
   - Context7 MCPサーバーへの接続
   - 利用可能なツールの確認

2. **ライブラリID解決**
   - `resolve-library-id` ツールを使用
   - "Next.js" → `/vercel/next.js/v14.3.0-canary.87`
   - "React" → `/reactjs/react.dev`

3. **ドキュメント取得**
   - `get-library-docs` ツールを使用
   - 最新のドキュメントとコード例を取得

4. **結果の表示**
   - 主要機能の説明
   - 実用的なコード例
   - トークン使用量と費用

### 期待される出力

```
╭─ Context7 MCP Demo ─╮
│ リアルタイムで最新の │
│ ドキュメントを取得   │
╰─────────────────────╯

📚 Context7でドキュメントを取得中...

╭─ 📊 取得したドキュメント情報 ─╮
│                                │
│ ## Next.js 14                  │
│ - サーバーコンポーネント       │
│ - App Router                   │
│ - データフェッチパターン       │
│                                │
│ ## React 18                    │
│ - useState/useEffect           │
│ - カスタムフック               │
│ - クリーンアップ関数           │
│                                │
╰────────────────────────────────╯

💰 トークン使用量と費用
合計: 76,849トークン
費用: $0.12
```

## 💡 実装の詳細

### Agent SDKでのMCP設定

```python
from claude_agent_sdk import query, ClaudeAgentOptions

# Context7 MCPサーバーの設定
options = ClaudeAgentOptions(
    mcp_servers={
        "context7": {
            "command": "npx",
            "args": ["-y", "@upstash/context7-mcp"]
        }
    },
    permission_mode="bypassPermissions"  # デモのためツールを自動承認
)

# エージェント実行
async for message in query(prompt=task, options=options):
    # メッセージ処理
    ...
```

### MCP設定の2つの方法

#### 方法1: 辞書で直接設定（デモで使用）

```python
options = ClaudeAgentOptions(
    mcp_servers={
        "context7": {
            "command": "npx",
            "args": ["-y", "@upstash/context7-mcp"]
        }
    }
)
```

#### 方法2: 設定ファイルのパスを指定

```python
from pathlib import Path

config_path = Path(__file__).parent / "mcp_config.json"
options = ClaudeAgentOptions(mcp_servers=config_path)
```

`mcp_config.json`:
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

### ツール許可モード

Agent SDKには4つの許可モードがあります：

| モード | 説明 | 使用場面 |
|--------|------|---------|
| `default` | 各ツール使用時に確認 | 本番環境（推奨） |
| `acceptEdits` | 編集系ツールを自動承認 | 開発環境 |
| `plan` | プラン作成後に一括確認 | レビュー重視 |
| `bypassPermissions` | すべて自動承認 | **デモ・テスト専用** |

**デモでは `bypassPermissions` を使用していますが、本番環境では `default` を推奨します。**

## 🎨 活用例

### 例1: 最新フレームワークの学習

```python
task = """
Next.js 15 の新機能について、Context7を使って最新ドキュメントを取得し、
以下の点をまとめてください:
1. Server Actionsの新しい使い方
2. Partial Prerenderingの仕組み
3. 実用的なコード例

use context7
"""
```

### 例2: マイグレーションガイドの生成

```python
task = """
React 17から18へのマイグレーションガイドを作成してください。
Context7で両バージョンのドキュメントを取得し、
主要な変更点と移行手順を説明してください。

use context7
"""
```

### 例3: ライブラリ比較

```python
task = """
FastAPIとFlaskの最新バージョンを比較してください。
Context7でドキュメントを取得し、以下を比較:
1. ルーティング定義
2. 非同期処理のサポート
3. バリデーション機能
4. パフォーマンス

use context7
"""
```

## 🔧 カスタマイズ

### トピックの絞り込み

`get-library-docs` ツールの `topic` パラメータで、取得するドキュメントを絞り込めます：

```python
task = """
React 18のHooksについて、Context7で以下のトピックに絞ってドキュメントを取得:
- useState
- useEffect
- useContext

topic: "hooks"を指定してください。
use context7
"""
```

### トークン数の制御

`tokens` パラメータで、取得するドキュメントの長さを制御できます：

```python
task = """
Next.js 14のApp Routerについて、簡潔な説明を取得してください。
tokens: 5000を指定してください（デフォルトは10000）。
use context7
"""
```

## 🔒 セキュリティとベストプラクティス

### 1. 許可モードの選択

```python
# ❌ 本番環境で非推奨
options = ClaudeAgentOptions(
    mcp_servers={...},
    permission_mode="bypassPermissions"  # すべて自動承認
)

# ✅ 本番環境で推奨
options = ClaudeAgentOptions(
    mcp_servers={...},
    permission_mode="default"  # 各ツールで確認
)
```

### 2. エラーハンドリング

```python
try:
    async for message in query(prompt=task, options=options):
        # メッセージ処理
        ...
except Exception as e:
    console.print(f"[red]エラー: {str(e)}[/red]")
    # 適切なフォールバック処理
```

### 3. タイムアウト設定

```python
options = ClaudeAgentOptions(
    mcp_servers={...},
    max_turns=10  # 最大ターン数を制限
)
```

## 📖 他のMCPサーバー

Context7以外にも、様々なMCPサーバーがあります：

### 公式MCPサーバー

| サーバー名 | 用途 | インストール |
|-----------|------|-------------|
| **filesystem** | ファイルシステム操作 | `@modelcontextprotocol/server-filesystem` |
| **github** | GitHub連携 | `@modelcontextprotocol/server-github` |
| **postgres** | PostgreSQL | `@modelcontextprotocol/server-postgres` |
| **puppeteer** | ブラウザ自動化 | `@modelcontextprotocol/server-puppeteer` |

**公式サーバー一覧**: https://github.com/modelcontextprotocol/servers

### 複数MCPサーバーの使用

```python
options = ClaudeAgentOptions(
    mcp_servers={
        "context7": {
            "command": "npx",
            "args": ["-y", "@upstash/context7-mcp"]
        },
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
        }
    }
)
```

## ❓ トラブルシューティング

### Node.jsが見つからない

```
Error: command not found: npx
```

**解決方法:**
```bash
# Node.jsのインストール確認
node --version

# インストールされていない場合
# macOS (Homebrew):
brew install node

# Windows (Chocolatey):
choco install nodejs

# Linux (apt):
sudo apt install nodejs npm
```

### Context7サーバーの起動エラー

```
Error: Failed to start MCP server 'context7'
```

**解決方法:**
```bash
# npxが利用可能か確認
npx --version

# 手動でContext7を試す
npx -y @upstash/context7-mcp

# ネットワーク接続を確認
```

### 権限エラー

```
Tool use requires permission
```

**解決方法:**
```python
# permission_modeを設定
options = ClaudeAgentOptions(
    mcp_servers={...},
    permission_mode="bypassPermissions"  # デモ用
)
```

### トークン使用量が多い

Context7は大量のドキュメントを取得するため、トークン使用量が多くなります。

**対策:**
1. `tokens` パラメータで制限
2. トピックを絞り込む
3. キャッシュ読取を活用（2回目以降は安価）

```python
task = """
Next.jsのApp Routerについて、簡潔に説明してください。
tokens: 5000
topic: "app-router"
use context7
"""
```

## 🚀 次のステップ

Context7 MCP連携を理解したら：

1. **他のライブラリで試す**
   ```bash
   # プロンプトを変更して実行
   python examples/04_mcp/mcp_example.py
   ```

2. **他のMCPサーバーを追加**
   - Filesystemサーバーでファイル操作
   - GitHubサーバーでコード管理
   - 複数サーバーの組み合わせ

3. **独自のエージェントを作成**
   - Context7を統合した学習ツール
   - ドキュメント生成自動化
   - コードレビューアシスタント

4. **プレゼン資料を確認**
   ```bash
   cat ../../docs/PRESENTATION.md
   ```

## 📚 参考資料

### Context7関連

- [Context7 公式ページ](https://glama.ai/mcp/servers/@upstash/context7-mcp)
- [Context7 GitHubリポジトリ](https://github.com/upstash/context7-mcp)
- [Context7 LobeHub](https://lobehub.com/mcp/upstash-context7)

### MCP関連

- [MCP 公式サイト](https://modelcontextprotocol.io/)
- [MCP サーバーリポジトリ](https://github.com/modelcontextprotocol/servers)
- [Agent SDK + MCP ガイド](https://docs.anthropic.com/en/api/agent-sdk/mcp)

### Agent SDK関連

- [Agent SDK ドキュメント](https://docs.claude.com/en/api/agent-sdk/overview)
- [Python SDK リポジトリ](https://github.com/anthropics/claude-agent-sdk-python)

---

## 🎓 まとめ

このデモでは、Context7 MCPサーバーを使用して：

✅ **リアルタイムドキュメント取得**: 最新のNext.js 14とReact 18のドキュメントを取得
✅ **Agent SDKとの統合**: MCPサーバー設定と使用方法を学習
✅ **実用的な実装**: 実際に動作するコード例を提供
✅ **拡張可能な設計**: 他のMCPサーバーも追加可能な設計

Context7により、エージェントは常に最新のドキュメントを参照し、古いAPIや存在しない機能を提案することがなくなります。

メインREADME: [../../README.md](../../README.md)
