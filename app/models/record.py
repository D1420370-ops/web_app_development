import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'app.db')

class Record:
    def __init__(self, id, type, amount, category, record_date, note, created_at=None):
        self.id = id
        self.type = type
        self.amount = amount
        self.category = category
        self.record_date = record_date
        self.note = note
        self.created_at = created_at

    @staticmethod
    def get_connection():
        # 確保 database 目錄存在
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, record_type, amount, category, record_date, note=''):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO records (type, amount, category, record_date, note) VALUES (?, ?, ?, ?, ?)',
            (record_type, amount, category, record_date, note)
        )
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        return record_id

    @classmethod
    def get_all(cls):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM records ORDER BY record_date DESC, id DESC')
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def get_by_id(cls, record_id):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM records WHERE id = ?', (record_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(*row)
        return None

    @classmethod
    def update(cls, record_id, record_type, amount, category, record_date, note=''):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE records SET type=?, amount=?, category=?, record_date=?, note=? WHERE id=?',
            (record_type, amount, category, record_date, note, record_id)
        )
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, record_id):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()

    @classmethod
    def get_summary_by_month(cls, year_month):
        """
        year_month 格式例如 '2023-10'
        取得該月總收入與總支出
        """
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT type, SUM(amount) as total
            FROM records
            WHERE record_date LIKE ?
            GROUP BY type
        ''', (f'{year_month}%',))
        rows = cursor.fetchall()
        conn.close()
        
        summary = {'income': 0, 'expense': 0, 'balance': 0}
        for row in rows:
            if row['type'] == 'income':
                summary['income'] = row['total']
            elif row['type'] == 'expense':
                summary['expense'] = row['total']
                
        summary['balance'] = summary['income'] - summary['expense']
        return summary
