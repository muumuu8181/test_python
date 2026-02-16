import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# nobunaga_bot モジュールをインポートするためにパスを通す必要があれば通すが、同じディレクトリなのでそのままインポート
# ただし、main()を実行してしまうとループに入るので、import時に実行されないように __name__ == "__main__" ガードがあるか確認。
# あります。

import nobunaga_bot

class TestNobunagaBot(unittest.TestCase):

    @patch('nobunaga_bot.wikipedia')
    def test_get_nobunaga_info_success(self, mock_wikipedia):
        # Wikipediaのページ取得成功時のテスト
        mock_page = MagicMock()
        mock_page.content = "織田信長の情報です。"
        mock_wikipedia.page.return_value = mock_page

        content = nobunaga_bot.get_nobunaga_info()
        self.assertEqual(content, "織田信長の情報です。")
        mock_wikipedia.set_lang.assert_called_with("ja")
        mock_wikipedia.page.assert_called_with("織田信長")

    @patch('nobunaga_bot.wikipedia')
    def test_get_nobunaga_info_failure(self, mock_wikipedia):
        # Wikipediaのページ取得失敗時のテスト
        mock_wikipedia.exceptions.PageError = Exception
        mock_wikipedia.page.side_effect = Exception("Page not found")

        content = nobunaga_bot.get_nobunaga_info()
        self.assertIsNone(content)

    @patch.dict(os.environ, {}, clear=True)
    @patch('builtins.print')
    def test_main_no_api_key(self, mock_print):
        # APIキーがない場合のテスト
        nobunaga_bot.main()
        mock_print.assert_any_call("エラー: 環境変数 'GOOGLE_API_KEY' が設定されていません。")

    @patch.dict(os.environ, {"GOOGLE_API_KEY": "dummy_key"})
    @patch('nobunaga_bot.genai')
    @patch('nobunaga_bot.get_nobunaga_info')
    @patch('builtins.input', side_effect=['こんにちは', 'exit'])
    @patch('builtins.print')
    def test_main_flow(self, mock_print, mock_input, mock_get_info, mock_genai):
        # 正常なフローのテスト
        mock_get_info.return_value = "信長のWikipedia情報"

        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_model.start_chat.return_value = mock_chat
        mock_genai.GenerativeModel.return_value = mock_model

        mock_response = MagicMock()
        mock_response.text = "うむ、こんにちはじゃ。"
        mock_chat.send_message.return_value = mock_response

        nobunaga_bot.main()

        # 検証
        mock_genai.configure.assert_called_with(api_key="dummy_key")
        mock_genai.GenerativeModel.assert_called_with('gemini-pro')
        mock_model.start_chat.assert_called()

        # システムプロンプトが含まれているか確認
        args, kwargs = mock_model.start_chat.call_args
        history = kwargs.get('history', [])
        self.assertTrue(any("信長のWikipedia情報" in part for msg in history for part in msg['parts'] if msg['role'] == 'user'))

        # メッセージ送信の確認
        mock_chat.send_message.assert_called_with('こんにちは')

if __name__ == '__main__':
    unittest.main()
