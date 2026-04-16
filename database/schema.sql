CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,          -- 'income' or 'expense'
    amount INTEGER NOT NULL,
    category TEXT NOT NULL,
    record_date TEXT NOT NULL,   -- 儲存為 'YYYY-MM-DD' 格式
    note TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
