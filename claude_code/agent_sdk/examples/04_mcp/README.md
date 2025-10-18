# MCP連携編: 拡張可能なエージェント

Model Context Protocol (MCP) を使用して、Agent SDK の拡張性を実証するデモです。

## 📚 このセクションで学べること

- MCPの基本概念と利点
- MCPサーバーの設定方法
- カスタムツールの追加
- 外部サービスとの統合
- 拡張可能なエージェント設計

## 🎯 Model Context Protocol (MCP) とは？

MCP は、AIエージェントが外部ツールやデータソースと標準化された方法で連携するためのプロトコルです。

### 主な利点

1. **標準化**: 統一されたインターフェースで様々なサービスと連携
2. **拡張性**: 簡単に新しいツールを追加可能
3. **再利用性**: MCPサーバーは複数のエージェントで共有
4. **セキュリティ**: 明確な権限管理とアクセス制御

### アーキテクチャ

```
┌─────────────────┐
│  Agent SDK      │
│  (エージェント) │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  MCP Protocol   │
│  (標準IF)       │
└────────┬────────┘
         │
         v
┌─────────────────────────────────┐
│  MCP Servers                    │
├─────────────────────────────────┤
│  • Filesystem Server            │
│  • GitHub Server                │
│  • Database Server              │
│  • Custom Business Logic        │
│  • ...                          │
└─────────────────────────────────┘
```

## 🚀 セットアップ

### 前提条件

- Node.js 18+ (MCPサーバーの多くはNode.jsで実装)
- npm または npx

### ステップ1: MCPサーバーのインストール

公式のMCPサーバーから選択してインストール:

```bash
# ファイルシステムサーバー
npm install -g @modelcontextprotocol/server-filesystem

# GitHubサーバー
npm install -g @modelcontextprotocol/server-github

# Slackサーバー
npm install -g @modelcontextprotocol/server-slack
```

**公式サーバー一覧:**
https://github.com/modelcontextprotocol/servers

### ステップ2: 設定ファイルの編集

`mcp_config.json` を編集して、使用するMCPサーバーを設定:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/your-name/allowed-directory"
      ]
    }
  }
}
```

**重要:**
- `filesystem` サーバーの場合: アクセスを許可するディレクトリパスを指定
- `github` サーバーの場合: `GITHUB_TOKEN` 環境変数を設定
- `database` サーバーの場合: 接続文字列を設定

### ステップ3: デモの実行

```bash
python examples/04_mcp/mcp_example.py
```

## 📋 利用可能なMCPサーバー

### 公式MCPサーバー

| サーバー名 | 用途 | 提供ツール例 |
|-----------|------|-------------|
| **filesystem** | ファイルシステム操作 | read_file, write_file, list_directory, search |
| **github** | GitHub連携 | create_pr, list_issues, create_issue, comment |
| **gitlab** | GitLab連携 | 同上（GitLab版） |
| **slack** | Slack連携 | send_message, list_channels, get_thread |
| **postgres** | PostgreSQL | query, insert, update, delete |
| **sqlite** | SQLite | 同上（SQLite版） |
| **puppeteer** | ブラウザ自動化 | navigate, screenshot, click, scrape |
| **google-drive** | Google Drive | list_files, read_file, upload |

### コミュニティMCPサーバー

- **Notion**: ページ作成、検索、更新
- **Jira**: チケット管理
- **AWS**: S3, Lambda などのAWSリソース操作
- **カスタムサーバー**: 独自のビジネスロジック

## 🎬 デモ実行

### 基本デモ

```bash
python examples/04_mcp/mcp_example.py
```

**期待される動作:**

```
┌─ Claude Agent SDK - MCP Integration Demo ─┐
│ Model Context Protocolを使用した拡張性のデモ│
└───────────────────────────────────────────┘

✅ MCP設定ファイルを読み込みました

┌─ 📘 MCPの基礎知識 ─┐
│                    │
│ Model Context Protocol (MCP) とは？│
│ ...                │
└────────────────────┘

🔧 MCPタスクを実行中...

🔧 ツール使用: filesystem_read_file
💭 ファイルを読み取っています...
🔧 ツール使用: filesystem_write_file
💭 結果を保存しています...

┌─ 📊 実行結果 ─┐
│ ...            │
└────────────────┘
```

## 💡 「すごさ」のポイント

### 1. 無限の拡張性

基本のAgent SDKに、任意のツールを追加可能:

```
Agent SDK (基本)
  ↓
+ Filesystem MCP → ファイル操作
+ GitHub MCP     → コード管理
+ Slack MCP      → チーム連携
+ Database MCP   → データ管理
+ Custom MCP     → 独自ロジック
  ↓
= 超強力なエージェント
```

### 2. 標準化の威力

MCPを使えば:
- **同じインターフェース**: どんなサービスも同じ方法で使える
- **簡単な切り替え**: PostgreSQL → MySQL も設定変更だけ
- **コード再利用**: 一度書けば、他のプロジェクトでも使える

### 3. セキュリティと制御

- **明確な権限**: どのツールを使えるか制御
- **アクセス制限**: ファイルシステムのアクセス範囲を制限
- **監査可能**: すべてのツール使用を追跡可能

### 4. エコシステム

- **公式サーバー**: すぐに使える高品質なサーバー
- **コミュニティ**: 常に新しいサーバーが追加
- **カスタム**: 独自のサーバーも簡単に作成

## 🛠 カスタムMCPサーバーの作成

独自のビジネスロジックをMCPサーバーとして実装できます。

### 最小限のMCPサーバー例

```javascript
// custom-mcp-server.js
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "custom-business-logic",
  version: "1.0.0"
});

// カスタムツールの定義
server.setRequestHandler("tools/list", async () => ({
  tools: [{
    name: "calculate_discount",
    description: "顧客の割引率を計算",
    inputSchema: {
      type: "object",
      properties: {
        customerId: { type: "string" },
        orderAmount: { type: "number" }
      }
    }
  }]
}));

// ツールの実行
server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "calculate_discount") {
    // ビジネスロジックを実装
    const discount = calculateBusinessDiscount(
      request.params.arguments.customerId,
      request.params.arguments.orderAmount
    );
    return { content: [{ type: "text", text: `Discount: ${discount}%` }] };
  }
});

// サーバー起動
const transport = new StdioServerTransport();
await server.connect(transport);
```

### MCPサーバーを登録

```json
{
  "mcpServers": {
    "business-logic": {
      "command": "node",
      "args": ["custom-mcp-server.js"]
    }
  }
}
```

## 🎨 活用例

### 例1: GitHub連携の自動化

```python
task = """
以下のタスクを実行:
1. GitHubで未解決のIssueを一覧取得
2. 各Issueの内容を分析
3. 優先度を評価
4. 対応方針をコメントとして投稿
"""
```

### 例2: データベース分析

```python
task = """
PostgreSQLデータベースを分析:
1. 全テーブルのスキーマを取得
2. 各テーブルのレコード数をカウント
3. パフォーマンス問題がありそうなクエリを特定
4. 改善提案のレポートを生成
"""
```

### 例3: マルチサービス統合

```python
task = """
以下のワークフローを実行:
1. Slackで今日のタスクを確認
2. GitHubで対応するPRをチェック
3. 進捗状況をNotionに記録
4. 完了報告をSlackに投稿
"""
```

## 🔒 セキュリティベストプラクティス

### 1. 最小権限の原則

```json
{
  "filesystem": {
    "args": [
      "/path/to/specific/allowed/dir"  // 特定のディレクトリのみ
    ]
  }
}
```

### 2. 機密情報の管理

```bash
# 環境変数で管理
export GITHUB_TOKEN="your_token"
export DATABASE_URL="postgresql://..."

# .env ファイルに記載（gitignore推奨）
```

### 3. ツールの明示的な許可

```python
options={
    "allowedTools": [
        "filesystem_read",  # 読み取りのみ
        # "filesystem_write" は許可しない
    ]
}
```

## 📖 参考資料

### 公式ドキュメント

- [MCP 公式サイト](https://modelcontextprotocol.io/)
- [MCP サーバーリポジトリ](https://github.com/modelcontextprotocol/servers)
- [Agent SDK + MCP ガイド](https://docs.claude.com/en/api/agent-sdk/mcp)

### コミュニティ

- [MCP Discord](https://discord.gg/modelcontextprotocol)
- [サンプルコード集](https://github.com/modelcontextprotocol/examples)

## ❓ トラブルシューティング

### MCPサーバーが起動しない

```
Error: Cannot find module '@modelcontextprotocol/server-filesystem'
```

**解決方法:**
```bash
npm install -g @modelcontextprotocol/server-filesystem
# または
npx -y @modelcontextprotocol/server-filesystem
```

### 権限エラー

```
PermissionError: Access denied
```

**解決方法:**
- 設定ファイルのパスを確認
- 環境変数（トークンなど）を確認
- MCPサーバーのログを確認

### 接続エラー

```
Failed to connect to MCP server
```

**解決方法:**
- MCPサーバーのコマンドが正しいか確認
- Node.jsがインストールされているか確認
- ファイアウォール設定を確認

---

## 🚀 次のステップ

MCP連携編を理解したら:

1. **デモスクリプトを実行**: 全体の流れを確認
   ```bash
   cd ../../demo
   python run_all_demos.py
   ```

2. **プレゼン資料を確認**: Agent SDKの全体像を把握
   ```bash
   cat ../../docs/PRESENTATION.md
   ```

3. **独自のエージェントを作成**: 学んだ知識を活用

---

**まとめ:**
MCP連携により、Agent SDKは無限の可能性を持つプラットフォームになります。基本的なファイル操作から、GitHub、Slack、データベース、そして独自のビジネスロジックまで、あらゆるものをエージェントに統合できます。

メインREADME: [../../README.md](../../README.md)
