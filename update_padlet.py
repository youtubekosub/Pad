import requests
import os
import datetime
import sys

# 取得対象のPadlet URL（Markdown形式）
URL = "https://padlet.com/padlets/n0g1c0jl2ak3grc5/exports/markdown.md"
# 保存するファイル名
FILE = "information.md"

def main():
    print(f"Checking for updates: {URL}")
    
    # Padlet側のブロックを避けるためのUser-Agent設定
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # 1. データのダウンロード
        res = requests.get(URL, headers=headers, timeout=30)
        
        # ステータスチェック
        if res.status_code != 200:
            print(f"❌ Error: Status code {res.status_code}")
            sys.exit(0)
            
        new_body = res.text.strip()

        # 中身がHTML（ログイン画面等）になっていないか厳格にチェック
        if not new_body or new_body.startswith("<!DOCTYPE html>") or "<html" in new_body.lower():
            print("⚠️ Warning: Received invalid content or HTML error page. Skipping update.")
            sys.exit(0)
        
        # 2. 変更チェック（既存ファイルがある場合）
        existing_body = ""
        if os.path.exists(FILE):
            with open(FILE, "r", encoding="utf-8") as f:
                content = f.read()
                # 「最終更新: ...」の行（1行目）と空行（2行目）を除去して本文を取り出す
                parts = content.split('\n\n', 1)
                if len(parts) > 1:
                    existing_body = parts[1].strip()
                else:
                    existing_body = content.strip()
        
        # 内容に変化がなければ終了
        if new_body == existing_body:
            print("✅ No changes detected in Padlet content.")
            return

        # 3. ファイルの保存（日本時間 JST）
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        timestamp = now.strftime("%Y/%m/%d %H:%M:%S")

        with open(FILE, "w", encoding="utf-8") as f:
            f.write(f"最終更新: {timestamp}\n\n")
            f.write(new_body)
        
        print(f"🔄 Success: {FILE} has been updated at {timestamp}")

    except Exception as e:
        print(f"❌ Critical Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
