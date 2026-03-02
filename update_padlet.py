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
            # Actionsを失敗扱いにせず終了（一時的なネットワークエラー対策）
            sys.exit(0)
            
        new_body = res.text.strip()

        # 中身がHTML（ログイン画面等）になっていないか厳格にチェック
        if new_body.startswith("<!DOCTYPE html>") or "<html" in new_body.lower():
            print("⚠️ Warning: Received HTML error page. Skipping update to protect existing data.")
            sys.exit(0)
        
        # 2. 変更チェック（既存ファイルがある場合）
        existing_body = ""
        if os.path.exists(FILE):
            with open(FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # 最初の2行（最終更新日時ヘッダー）を飛ばして本文のみを比較
                if len(lines) >= 2:
                    existing_body = "".join(lines[2:]).strip()
        
        # 内容に変化がなければ終了（無駄なコミットを防止）
        if new_body == existing_body:
            print("✅ No changes detected in Padlet content.")
            return

        # 3. ファイルの保存（日本時間 JST でタイムスタンプを付与）
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        timestamp = now.strftime("%Y/%m/%d %H:%M:%S")

        with open(FILE, "w", encoding="utf-8") as f:
            f.write(f"最終更新: {timestamp}\n\n")
            f.write(new_body)
        
        print(f"🔄 Success: {FILE} has been updated at {timestamp}")

    except Exception as e:
        print(f"❌ Critical Error: {e}")
        # 致命的なエラーの場合はActionsに通知するため1で終了
        sys.exit(1)

if __name__ == "__main__":
    main()
