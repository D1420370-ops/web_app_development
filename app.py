from app import create_app
from dotenv import load_dotenv

# 載入 .env 檔案的環境變數（如果存在的話）
load_dotenv()

# 建立 Flask 實例
app = create_app()

if __name__ == '__main__':
    # 啟動開發伺服器
    app.run(debug=True)
