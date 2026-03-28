import os
import sys
import wikipedia
import google.generativeai as genai

def get_nobunaga_info():
    """Wikipediaから織田信長の情報を取得する"""
    try:
        wikipedia.set_lang("ja")
        # ページが存在するか確認し、内容を取得
        page = wikipedia.page("織田信長")
        return page.content
    except wikipedia.exceptions.PageError:
        print("エラー: Wikipediaページ '織田信長' が見つかりませんでした。")
        return None
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"エラー: 曖昧さ回避が必要です: {e.options}")
        return None
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

def main():
    # APIキーの確認
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("エラー: 環境変数 'GOOGLE_API_KEY' が設定されていません。")
        print("export GOOGLE_API_KEY='your_api_key_here' を実行してから再度試してください。")
        return

    # Wikipediaから情報を取得
    print("織田信長の情報をWikipediaから取得中...")
    nobunaga_info = get_nobunaga_info()
    if not nobunaga_info:
        print("情報の取得に失敗したため、終了します。")
        return

    # Gemini APIの設定
    genai.configure(api_key=api_key)

    # システムプロンプトの作成
    system_prompt = f"""
あなたは織田信長です。以下のWikipediaの情報を元に、ユーザーの質問に答えてください。
回答は常に織田信長らしい尊大な口調（「わしは...じゃ」「...であるか」など）で行ってください。
現代の知識についても、当時の視点や価値観を交えてコメントしてください。

【織田信長の情報】
{nobunaga_info[:20000]}  # トークン制限を考慮して適当な長さに切り詰める
"""

    # モデルの初期化
    try:
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[
            {"role": "user", "parts": [system_prompt]},
            {"role": "model", "parts": ["うむ、わしが織田信長じゃ。何用か？"]}
        ])
    except Exception as e:
        print(f"モデルの初期化に失敗しました: {e}")
        return

    print("\n--- 織田信長ボット (終了するには 'exit' または 'quit' と入力) ---")
    print("信長: うむ、わしが織田信長じゃ。何用か？")

    while True:
        try:
            user_input = input("あなた: ")
            if user_input.lower() in ['exit', 'quit', '終了']:
                print("信長: さらばじゃ。")
                break

            if not user_input.strip():
                continue

            response = chat.send_message(user_input)
            print(f"信長: {response.text}")

        except (KeyboardInterrupt, EOFError):
            print("\n信長: 中断か。まあよい。さらばじゃ。")
            break
        except Exception as e:
            print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
