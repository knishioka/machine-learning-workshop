# Slack Notifier セットアップガイド

## モード比較

| 機能 | MCPモード | Webhookモード |
|------|-----------|--------------|
| メッセージ送信 | ○ | ○ |
| チャンネル一覧 | ○ | × |
| スレッド返信 | ○ | × |
| リアクション追加 | ○ | × |
| セットアップ難易度 | 中 | 簡単 |

## Webhookモード セットアップ（デモ推奨）

### ステップ1: Incoming Webhookの作成

1. https://api.slack.com/apps にアクセス
2. "Create New App" → "From scratch" をクリック
3. アプリ名を入力: "Claude Notifier"
4. ワークスペースを選択
5. "Create App" をクリック

### ステップ2: Incoming Webhooksの有効化

1. "Incoming Webhooks" をクリック
2. "Activate Incoming Webhooks" をONに切り替え
3. "Add New Webhook to Workspace" をクリック
4. 通知先チャンネルを選択
5. "Allow" をクリック
6. Webhook URLをコピー

### ステップ3: 環境変数の設定

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/T.../B.../..."
```

### ステップ4: テスト

```bash
python3 scripts/send_webhook.py --message "Claude Codeからこんにちは！"
```

## MCPモード セットアップ（上級）

### ステップ1: Bot Token付きSlackアプリの作成

1. https://api.slack.com/apps にアクセス
2. Bot Tokenで新しいアプリを作成
3. スコープを追加: `channels:read`, `chat:write`, `reactions:write`

### ステップ2: Claude MCPの設定

```json
{
  "mcp": {
    "servers": {
      "slack": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-slack"],
        "env": {
          "SLACK_BOT_TOKEN": "xoxb-your-bot-token",
          "SLACK_TEAM_ID": "T01234567"
        }
      }
    }
  }
}
```

## トラブルシューティング

### "SLACK_WEBHOOK_URL not set"
環境変数がエクスポートされていることを確認:
```bash
echo $SLACK_WEBHOOK_URL
```

### "Invalid webhook URL format"
URLが `https://hooks.slack.com/services/` で始まることを確認

### "mcp__slack tools not available"
MCPサーバーが設定されていない。`claude mcp list` で確認

### "Channel not found"
MCPモードでチャンネル名が正しいか確認。`#` プレフィックスを含める

## セキュリティベストプラクティス

1. トークンをバージョン管理にコミットしない
2. 環境変数でシークレットを管理
3. 可能な限りチャンネルアクセスを制限
4. 定期的にトークンをローテーション

## デモ用クイックスタート

デモ用の最小セットアップ:

```bash
# 1. テスト用チャンネルでWebhookを作成（上記手順）

# 2. 環境変数を設定
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# 3. テスト実行
cd /path/to/slack-notifier
python -m pytest scripts/test_send_webhook.py -v

# 4. 実際に送信（オプション）
python scripts/send_webhook.py --message "デモメッセージ" --template success --title "テスト"
```

**注意**: デモではテストのみを実行し、実際のSlack送信は行いません。
