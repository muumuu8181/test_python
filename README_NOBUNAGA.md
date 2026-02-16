# 織田信長ボット (Oda Nobunaga Bot)

Wikipediaの情報を元に、織田信長になりきって対話するボットです。
Google Gemini APIを使用しています。

## 前提条件

*   Python 3.7以上
*   Google Gemini APIキー

## インストール

必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
```

## APIキーの設定

Google Gemini APIキーを取得し、環境変数 `GOOGLE_API_KEY` に設定します。

### Linux / macOS

```bash
export GOOGLE_API_KEY="your_api_key_here"
```

### Windows (PowerShell)

```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

## 実行方法

以下のコマンドでボットを起動します。

```bash
python nobunaga_bot.py
```

起動すると、織田信長として挨拶します。質問を入力すると、Wikipediaの情報を元に信長らしい口調で回答してくれます。
終了するには `exit` または `quit` と入力してください。

## 注意事項

*   このボットはWikipediaの情報を元に回答を生成しますが、常に正確な情報を提供するとは限りません。
*   APIの使用量によっては課金が発生する場合がありますのでご注意ください。
