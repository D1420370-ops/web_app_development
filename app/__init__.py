import os
import sqlite3
from flask import Flask

def create_app():
    """初始化並設定 Flask 應用程式"""
    # 指定 template 和 static 資料夾的相對位置
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # 載入設定（這裡示範簡單的設定方式，實務上可透過 config.py 或 .env）
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # 確保 instance 目錄存在（用於存放 SQLite 資料庫檔案）
    os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)
    
    # 註冊路由 (Blueprints)
    from app.routes.task_routes import task_bp
    app.register_blueprint(task_bp)
    
    return app

def init_db():
    """根據 schema.sql 初始化資料庫"""
    # 取得專案根目錄
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'instance', 'database.db')
    schema_path = os.path.join(base_dir, 'database', 'schema.sql')
    
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # 執行 SQL 建表語法
    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
    print(f"資料庫初始化完成！已建立於：{db_path}")
