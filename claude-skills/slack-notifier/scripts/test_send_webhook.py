#!/usr/bin/env python3
"""
send_webhook.py のユニットテスト

5テストでコア機能をカバー（モックのみ、実送信なし）:
- URL Validation: 2テスト
- Template Application: 2テスト
- Mock Send: 1テスト

実行: python -m pytest test_send_webhook.py -v
または: python test_send_webhook.py
"""
import json
import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO

import send_webhook


class TestValidateWebhookUrl(unittest.TestCase):
    """Webhook URL検証のテスト"""

    def test_valid_url_passes(self):
        """有効なSlack Webhook URLが検証を通ること"""
        valid_url = "https://hooks.slack.com/services/T12345678/B12345678/abcdefghijklmnop"
        self.assertTrue(send_webhook.validate_webhook_url(valid_url))

    def test_invalid_url_fails(self):
        """無効なURLが検証に失敗すること"""
        invalid_urls = [
            "http://hooks.slack.com/services/T12345678/B12345678/abc",  # HTTP (not HTTPS)
            "https://evil.com/services/T12345678/B12345678/abc",  # Wrong domain
            "https://hooks.slack.com/wrong/path",  # Wrong path
            "",  # Empty
        ]
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(send_webhook.validate_webhook_url(url))


class TestApplyTemplate(unittest.TestCase):
    """テンプレート適用のテスト"""

    def test_success_template(self):
        """successテンプレートがチェックマーク絵文字を含むこと"""
        result = send_webhook.apply_template("success", "テスト", "メッセージ")
        text = result["blocks"][0]["text"]["text"]

        self.assertIn(":white_check_mark:", text)
        self.assertIn("テスト", text)
        self.assertIn("メッセージ", text)

    def test_error_template(self):
        """errorテンプレートがアラート絵文字を含むこと"""
        result = send_webhook.apply_template("error", "エラー", "詳細")
        text = result["blocks"][0]["text"]["text"]

        self.assertIn(":rotating_light:", text)
        self.assertIn("エラー", text)


class TestSendMessage(unittest.TestCase):
    """メッセージ送信のテスト（モック）"""

    def setUp(self):
        """テストフィクスチャのセットアップ"""
        self.valid_url = "https://hooks.slack.com/services/T12345678/B12345678/abcdefghijklmnop"

    @patch('urllib.request.urlopen')
    def test_successful_send(self, mock_urlopen):
        """モックでの送信成功"""
        # 成功レスポンスをモック
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b"ok"
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        result = send_webhook.send_message(
            webhook_url=self.valid_url,
            message="テストメッセージ"
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Message sent successfully")

        # urlopenが呼ばれたことを確認
        mock_urlopen.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
