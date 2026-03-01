import requests
import os
import datetime

# 取得対象のPadlet URL（Markdownエクスポート用）
URL = "https://padlet.com/padlets/n0g1c0jl2ak3grc5/exports/markdown.md"
# 保存するファイル名
FILE = "padlet_export.md"

def main():
    print(f"Checking for updates: {URL}")
    try:
        # 1. データのダウンロード
        res = requests.get(URL, timeout=30)
        
        # ステータスチェック（200以外、またはエラーページ(HTML)が返ってきたら中断）
        if res.status_code != 200:
            print(f"Error: Status code {res.status_code}")
            return
            
        if res.text.strip().startswith("<!DOCTYPE html>"):
            print("⚠️ Error: Received HTML error page. Skipping update.")
            return
        
        new_body = res.text.strip()

        # 2. 変更チェック（既存ファイルがある場合）
        if os.path.exists(FILE):
            with open(FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # 最初の2行（最終更新日時ヘッダー）を飛ばして本文を比較
                if len(lines) >= 2:
                    existing_body = "".join(lines[2:]).strip()
                    if new_body == existing_body:
                        print("✅ No changes detected in Padlet content.")
                        return

        # 3. ファイルの保存（日本時間でタイムスタンプを付与）
        # GitHub ActionsのサーバーはUTCなので、+9時間してJSTにする
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        timestamp = now.strftime("%Y/%m/%d %H:%M:%S")

        with open(FILE, "w", encoding="utf-8") as f:
            f.write(f"最終更新: {timestamp}\n\n")
            f.write(new_body)
        
        print(f"🔄 Success: {FILE} has been updated at {timestamp}")

    except Exception as e:
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    main()
