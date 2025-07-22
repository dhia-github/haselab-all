import requests
import pypdf
import os

# --- 設定項目 ---

# 2. 翻訳したいPDFファイルの名前を指定してください
PDF_FILE_NAME = "2201.10703v2-1.pdf"


# 1. DeepL APIキー
DEEPL_API_KEY = "7c4841a5-8196-419e-a3d2-4188c4697419:fx"


# --- 設定はここまで ---


# --- 以下はプログラムの本体（変更不要） ---
def extract_text_from_pdf(pdf_path):
    """PDFファイルから全てのテキストを抽出する関数"""
    print(f"'{pdf_path}' からテキストを抽出しています...")
    if not os.path.exists(pdf_path):
        return f"エラー: ファイル '{pdf_path}' が見つかりません。"

    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        print("テキストの抽出が完了しました。")
        return text
    except Exception as e:
        return f"PDFの読み込み中にエラーが発生しました: {e}"

def translate_text_with_deepl(text, api_key):
    """DeepL APIを使ってテキストを翻訳する関数"""
    print("DeepL APIで翻訳を開始します...")
    if not text.strip():
        return "エラー: 翻訳するテキストがありません。"

    # DeepL APIのエンドポイント（Freeプラン用）
    url = "https://api-free.deepl.com/v2/translate"

    params = {
        "auth_key": api_key,
        "text": text,
        "source_lang": "EN", # 翻訳元言語（英語）
        "target_lang": "JA"  # 翻訳先言語（日本語）
    }

    try:
        response = requests.post(url, data=params)
        response.raise_for_status() # エラーがあれば例外を発生させる

        result = response.json()
        translated_text = result["translations"][0]["text"]
        print("翻訳が完了しました。")
        return translated_text
    except requests.exceptions.RequestException as e:
        return f"APIリクエスト中にエラーが発生しました: {e}"
    except Exception as e:
        return f"翻訳中に予期せぬエラーが発生しました: {e}"

def save_to_text_file(text, original_filename):
    """翻訳結果をテキストファイルに保存する関数"""
    output_filename = os.path.splitext(original_filename)[0] + "_jp.txt"
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"翻訳結果を '{output_filename}' に保存しました。")
    except Exception as e:
        print(f"ファイルの保存中にエラーが発生しました: {e}")


# --- メインの処理 ---
if __name__ == "__main__":
    # 1. PDFからテキストを抽出
    extracted_text = extract_text_from_pdf(PDF_FILE_NAME)

    if "エラー:" not in extracted_text:
        # 2. 抽出したテキストを翻訳
        translated_text = translate_text_with_deepl(extracted_text, DEEPL_API_KEY)

        if "エラー:" not in translated_text:
            # 3. 翻訳結果をファイルに保存
            save_to_text_file(translated_text, PDF_FILE_NAME)