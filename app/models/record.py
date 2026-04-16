import sqlite3
import os

# 使用 os.path 取得專案根目錄，並將資料庫路徑設為 instance/database.db
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, 'instance', 'database.db')

class Record:
    """
    收支紀錄 Model
    主要負責管理個人的收入與支出資料
    """
    def __init__(self, id, type, amount, category, record_date, note, created_at=None):
        self.id = id
        self.type = type
        self.amount = amount
        self.category = category
        self.record_date = record_date
        self.note = note
        self.created_at = created_at

    @staticmethod
    def get_db_connection():
        """
        取得資料庫連線
        會自動建立 instance 資料夾（如果不存在的話）
        並設定 row_factory 為 sqlite3.Row 以便用字典方式存取欄位
        """
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, data):
        """
        新增一筆記錄
        
        :param data: 包含 type, amount, category, record_date, note 的字典
        :return: 回傳新建立的紀錄 id
        """
        conn = None
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO records (type, amount, category, record_date, note) VALUES (?, ?, ?, ?, ?)',
                (data.get('type'), data.get('amount'), data.get('category'), data.get('record_date'), data.get('note', ''))
            )
            conn.commit()
            record_id = cursor.lastrowid
            return record_id
        except sqlite3.Error as e:
            print(f"Database error during create: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @classmethod
    def get_all(cls):
        """
        取得所有記錄，按日期遞減與 ID 遞減排序
        
        :return: 回傳 Record 物件的列表
        """
        conn = None
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM records ORDER BY record_date DESC, id DESC')
            rows = cursor.fetchall()
            return [cls(*row) for row in rows]
        except sqlite3.Error as e:
            print(f"Database error during get_all: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @classmethod
    def get_by_id(cls, record_id):
        """
        取得單筆記錄
        
        :param record_id: 紀錄的 ID
        :return: 回傳單筆 Record 物件，若不存在則回傳 None
        """
        conn = None
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM records WHERE id = ?', (record_id,))
            row = cursor.fetchone()
            if row:
                return cls(*row)
            return None
        except sqlite3.Error as e:
            print(f"Database error during get_by_id: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @classmethod
    def update(cls, record_id, data):
        """
        更新記錄
        
        :param record_id: 要更新的紀錄 ID
        :param data: 包含 type, amount, category, record_date, note 的字典
        :return: 成功回傳 True，失敗回傳 False
        """
        conn = None
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE records SET type=?, amount=?, category=?, record_date=?, note=? WHERE id=?',
                (data.get('type'), data.get('amount'), data.get('category'), data.get('record_date'), data.get('note', ''), record_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error during update: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @classmethod
    def delete(cls, record_id):
        """
        刪除記錄
        
        :param record_id: 要刪除的紀錄 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        conn = None
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error during delete: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @classmethod
    def get_summary_by_month(cls, year_month):
        """
        取得特定月份的總收入、總支出與結餘
        
        :param year_month: 年月字串，格式例如 '2023-10'
        :return: 包含 income, expense, balance 的字典
        """
        conn = None
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT type, SUM(amount) as total
                FROM records
                WHERE record_date LIKE ?
                GROUP BY type
            ''', (f'{year_month}%',))
            rows = cursor.fetchall()
            
            summary = {'income': 0, 'expense': 0, 'balance': 0}
            for row in rows:
                if row['type'] == 'income':
                    summary['income'] = row['total']
                elif row['type'] == 'expense':
                    summary['expense'] = row['total']
                    
            summary['balance'] = summary['income'] - summary['expense']
            return summary
        except sqlite3.Error as e:
            print(f"Database error during get_summary_by_month: {e}")
            return {'income': 0, 'expense': 0, 'balance': 0}
        finally:
            if conn:
                conn.close()

