#!/usr/bin/env python3
"""
Slack Webhook メッセージ送信スクリプト

Incoming Webhook URL経由でSlackにメッセージを送信。
Slack MCPサーバーが利用できない場合のフォールバック。

使用方法:
    python3 send_webhook.py --message "Hello!"
    python3 send_webhook.py --message "Alert!" --template error
    python3 send_webhook.py --json '{"text": "Custom payload"}'

環境変数:
    SLACK_WEBHOOK_URL: 必須。Slack Incoming Webhook URL。

セキュリティ:
    - Webhook URLはログ出力しない
    - 送信前にURLフォーマットを検証
    - エラーメッセージはサニタイズ
"""
import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import Optional, Dict, Any


# テンプレート定義
TEMPLATES: Dict[str, Dict[str, Any]] = {
    "success": {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":white_check_mark: *{title}*\n{message}"
                }
            },
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": ":calendar: {timestamp}"}
                ]
            }
        ]
    },
    "warning": {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":warning: *{title}*\n{message}"
                }
            },
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": ":calendar: {timestamp}"}
                ]
            }
        ]
    },
    "error": {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":rotating_light: *{title}*\n{message}"
                }
            },
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": ":calendar: {timestamp}"}
                ]
            }
        ]
    },
    "info": {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":information_source: *{title}*\n{message}"
                }
            },
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": ":calendar: {timestamp}"}
                ]
            }
        ]
    }
}


def validate_webhook_url(url: str) -> bool:
    """
    Slack Webhook URLフォーマットを検証。

    Args:
        url: 検証するURL

    Returns:
        Slack Webhookパターンに一致すればTrue
    """
    pattern = r'^https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[a-zA-Z0-9]+$'
    return bool(re.match(pattern, url))


def get_timestamp() -> str:
    """メッセージ用のフォーマット済みタイムスタンプを取得"""
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")


def apply_template(
    template_name: str,
    title: str,
    message: str
) -> Dict[str, Any]:
    """
    メッセージテンプレートを適用。

    Args:
        template_name: テンプレート名（success, warning, error, info）
        title: メッセージタイトル
        message: メッセージ本文

    Returns:
        フォーマット済みSlackメッセージペイロード
    """
    if template_name not in TEMPLATES:
        raise ValueError(f"Unknown template: {template_name}")

    template = TEMPLATES[template_name]
    timestamp = get_timestamp()

    # ディープコピーしてフォーマット
    payload: Dict[str, Any] = {"blocks": []}
    for block in template["blocks"]:
        formatted_block = json.loads(
            json.dumps(block)
            .replace("{title}", title)
            .replace("{message}", message)
            .replace("{timestamp}", timestamp)
        )
        payload["blocks"].append(formatted_block)

    return payload


def send_message(
    webhook_url: str,
    message: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
    template: Optional[str] = None,
    title: Optional[str] = None
) -> Dict[str, Any]:
    """
    Webhook経由でSlackにメッセージを送信。

    Args:
        webhook_url: Slack Webhook URL
        message: シンプルテキストメッセージ
        payload: カスタムJSONペイロード
        template: 使用するテンプレート名
        title: テンプレート用タイトル

    Returns:
        成功ステータスを含むレスポンスdict
    """
    # URL検証
    if not validate_webhook_url(webhook_url):
        return {
            "success": False,
            "error": "Invalid Slack webhook URL format"
        }

    # ペイロード構築
    if payload:
        data = payload
    elif template:
        title = title or "Notification"
        message = message or ""
        data = apply_template(template, title, message)
    elif message:
        data = {"text": message}
    else:
        return {
            "success": False,
            "error": "No message content provided"
        }

    # リクエスト送信
    try:
        request = urllib.request.Request(
            webhook_url,
            data=json.dumps(data).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Claude-Slack-Notifier/1.0"
            },
            method="POST"
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            response_text = response.read().decode("utf-8")

            if response.status == 200 and response_text == "ok":
                return {"success": True, "message": "Message sent successfully"}
            else:
                return {
                    "success": False,
                    "error": f"Unexpected response: {response_text}"
                }

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {
            "success": False,
            "error": f"HTTP {e.code}: {error_body or e.reason}"
        }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "error": f"Network error: {str(e.reason)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def main():
    """CLI使用のメインエントリポイント"""
    parser = argparse.ArgumentParser(
        description="Webhook経由でSlackにメッセージを送信",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
    python3 send_webhook.py --message "Hello!"
    python3 send_webhook.py --message "ビルド失敗" --template error --title "CIアラート"
    python3 send_webhook.py --json '{"text": "カスタムメッセージ"}'
        """
    )

    parser.add_argument(
        "--message", "-m",
        help="送信するメッセージテキスト"
    )
    parser.add_argument(
        "--template", "-t",
        choices=["success", "warning", "error", "info"],
        help="使用するメッセージテンプレート"
    )
    parser.add_argument(
        "--title",
        help="テンプレート用タイトル（--templateと併用）"
    )
    parser.add_argument(
        "--json", "-j",
        help="送信する生JSONペイロード"
    )
    parser.add_argument(
        "--webhook-url",
        help="Slack Webhook URL（SLACK_WEBHOOK_URL環境変数を上書き）"
    )

    args = parser.parse_args()

    # Webhook URL取得
    webhook_url = args.webhook_url or os.environ.get("SLACK_WEBHOOK_URL")

    if not webhook_url:
        print(json.dumps({
            "success": False,
            "error": "SLACK_WEBHOOK_URL environment variable not set"
        }))
        sys.exit(1)

    # JSONペイロードをパース
    payload = None
    if args.json:
        try:
            payload = json.loads(args.json)
        except json.JSONDecodeError as e:
            print(json.dumps({
                "success": False,
                "error": f"Invalid JSON: {str(e)}"
            }))
            sys.exit(1)

    # メッセージ送信
    result = send_message(
        webhook_url=webhook_url,
        message=args.message,
        payload=payload,
        template=args.template,
        title=args.title
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
