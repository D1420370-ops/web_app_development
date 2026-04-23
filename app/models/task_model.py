import sqlite3
import os
from contextlib import contextmanager

# 資料庫檔案路徑：指向專案根目錄下的 instance/database.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

@contextmanager
def get_db_connection():
    """提供資料庫連線的 Context Manager，確保連線會正確關閉"""
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    # 讓回傳的資料可以使用類似 dict 的方式透過欄位名稱存取
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

class TaskModel:
    """封裝對 tasks 資料表的操作邏輯"""
    
    @staticmethod
    def get_all():
        """取得所有任務，預設以到期日升序排列，沒到期日的排在最後"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # 將 NULL 的到期日排到最後
            cursor.execute("""
                SELECT * FROM tasks 
                ORDER BY 
                    CASE WHEN due_date IS NULL OR due_date = '' THEN 1 ELSE 0 END, 
                    due_date ASC, 
                    created_at DESC
            """)
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(task_id):
        """根據 ID 取得單一任務"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(title, description=None, due_date=None):
        """新增一筆任務"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)",
                (title, description, due_date)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def update(task_id, title, description=None, due_date=None):
        """更新特定任務的內容"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET title = ?, description = ?, due_date = ? WHERE id = ?",
                (title, description, due_date, task_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(task_id):
        """刪除特定任務"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def toggle_status(task_id):
        """切換任務的完成狀態 (0 -> 1, 1 -> 0)"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET completed = CASE WHEN completed = 1 THEN 0 ELSE 1 END WHERE id = ?",
                (task_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
