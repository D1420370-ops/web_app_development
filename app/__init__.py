import os
import sqlite3
from flask import Flask
from .routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key')
    
    # 初始化 Blueprints
    register_blueprints(app)
    
    return app

def init_db():
    from app.models.record import DB_PATH
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        
    schema_path = os.path.join(db_dir, 'schema.sql')
    if os.path.exists(schema_path):
        conn = sqlite3.connect(DB_PATH)
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    else:
        print(f"Error: Schema file not found at {schema_path}")
