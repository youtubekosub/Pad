import requests
import os
import datetime

# 取得対象のPadlet URL（Markdownエクスポート用）
URL = "https://padlet.com/padlets/n0g1c0jl2ak3grc5/exports/markdown.md"
# 保存するファイル名
FILE = "information.md"

def main():
    print(f"Checking for updates: {URL}")
    try:
        # 1. データのダウンロード
        # タイムアウトを設定してフリーズを防止
        res = requests.get(URL, timeout=30)
        
        # ステータスチェック（200 OK 以外はエラー）
        if res.status_code != 200:
            print(f"Error: Status code {res.status_code}")
            return
            
        # 中身がHTML（ログイン画面やエラーページ）になっていないかチェック
        if res.text.strip().startswith("<!DOCTYPE html>"):
            print("⚠️ Error: Received HTML error page. Skipping update.")
            return
        
        new_body = res.text.strip()

        # 2. 変更チェック（既存ファイルがある場合）
        if os.path.exists(FILE):
            with open(FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # 最初の2行（最終更新日時ヘッダー）を飛ばして本文のみを抽出
                if len(lines) >= 2:
                    existing_body = "".join(lines[2:]).strip()
                    # 内容に変化がなければ、何もしない（GitHubの履歴を汚さない）
                    if new_body == existing_body:
                        print("✅ No changes detected in Padlet content.")
                        return

        # 3. ファイルの保存（日本時間 JST でタイムスタンプを付与）
        # GitHub Actionsのサーバー（UTC）に 9時間を足して日本時間に変換
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        timestamp = now.strftime("%Y/%m/%d %H:%M:%S")

        with open(FILE, "w", encoding="utf-8") as f:
            # 1行目に更新日時を入れることで、ファイルが更新されたことが分かりやすくなります
            f.write(f"最終更新: {timestamp}\n\n")
            f.write(new_body)
        
        print(f"🔄 Success: {FILE} has been updated at {timestamp}")

    except Exception as e:
        # 万が一のエラーをログに出力
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    main()
