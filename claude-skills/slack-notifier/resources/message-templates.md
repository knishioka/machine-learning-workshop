# Slackメッセージテンプレート

一般的な通知タイプ用の事前構築テンプレート。

## アラートテンプレート

### 成功アラート
```json
{
  "blocks": [
    {
      "type": "header",
      "text": {"type": "plain_text", "text": "成功", "emoji": true}
    },
    {
      "type": "section",
      "text": {"type": "mrkdwn", "text": "*{title}*\n{message}"}
    },
    {
      "type": "context",
      "elements": [
        {"type": "mrkdwn", "text": "{timestamp} | Claude Code"}
      ]
    }
  ]
}
```

### エラーアラート
```json
{
  "blocks": [
    {
      "type": "header",
      "text": {"type": "plain_text", "text": "エラー", "emoji": true}
    },
    {
      "type": "section",
      "text": {"type": "mrkdwn", "text": "*{title}*\n{message}"},
      "accessory": {
        "type": "button",
        "text": {"type": "plain_text", "text": "詳細を見る"},
        "url": "{details_url}"
      }
    },
    {
      "type": "divider"
    },
    {
      "type": "section",
      "fields": [
        {"type": "mrkdwn", "text": "*重要度:*\n{severity}"},
        {"type": "mrkdwn", "text": "*時刻:*\n{timestamp}"}
      ]
    }
  ]
}
```

## レポートテンプレート

### ビルドレポート
```json
{
  "blocks": [
    {
      "type": "header",
      "text": {"type": "plain_text", "text": "ビルドレポート", "emoji": true}
    },
    {
      "type": "section",
      "text": {"type": "mrkdwn", "text": "*{project_name}* - {branch}"}
    },
    {
      "type": "section",
      "fields": [
        {"type": "mrkdwn", "text": "*ステータス:*\n{status}"},
        {"type": "mrkdwn", "text": "*所要時間:*\n{duration}"},
        {"type": "mrkdwn", "text": "*コミット:*\n`{commit_sha}`"},
        {"type": "mrkdwn", "text": "*実行者:*\n{author}"}
      ]
    }
  ]
}
```

### テストレポート
```json
{
  "blocks": [
    {
      "type": "header",
      "text": {"type": "plain_text", "text": "テスト結果", "emoji": true}
    },
    {
      "type": "section",
      "fields": [
        {"type": "mrkdwn", "text": "*成功:*\n{passed}"},
        {"type": "mrkdwn", "text": "*失敗:*\n{failed}"},
        {"type": "mrkdwn", "text": "*スキップ:*\n{skipped}"},
        {"type": "mrkdwn", "text": "*カバレッジ:*\n{coverage}%"}
      ]
    }
  ]
}
```

## 変数リファレンス

| 変数 | 説明 | 例 |
|------|------|-----|
| `{title}` | メッセージタイトル | "ビルド完了" |
| `{message}` | メイン内容 | "全テスト合格" |
| `{timestamp}` | ISOタイムスタンプ | "2025-11-27 10:30 UTC" |
| `{status}` | ステータス表示 | "成功" |
| `{duration}` | 所要時間 | "2分34秒" |
| `{severity}` | 重要度 | "高" |
| `{project_name}` | プロジェクト名 | "my-app" |
| `{branch}` | ブランチ名 | "main" |
| `{commit_sha}` | コミットハッシュ | "abc1234" |
| `{author}` | 実行者 | "田中太郎" |
| `{passed}` | 成功テスト数 | "42" |
| `{failed}` | 失敗テスト数 | "0" |
| `{skipped}` | スキップテスト数 | "2" |
| `{coverage}` | カバレッジ率 | "85" |
