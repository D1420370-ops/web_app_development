# 路由設計文件 (ROUTES) - 個人記帳簿

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (儀表板) | GET | `/` | `templates/index.html` | 顯示當月總收入、總支出、結餘與近期收支紀錄清單 |
| 新增支出頁面 | GET | `/expense/new` | `templates/expense_form.html` | 顯示新增支出的填表畫面 |
| 送出新增支出 | POST | `/expense` | — | 接收支出表單資料，寫入 DB，成功後重導至首頁 |
| 新增收入頁面 | GET | `/income/new` | `templates/income_form.html` | 顯示新增收入的填表畫面 |
| 送出新增收入 | POST | `/income` | — | 接收收入表單資料，寫入 DB，成功後重導至首頁 |
| 統計圖表頁面 | GET | `/statistics` | `templates/statistics.html` | 顯示支出與收入的分類圓餅圖等數據統計 |
| 刪除指定項目 | POST | `/record/<int:id>/delete` | — | 接收要刪除的紀錄 ID，從 DB 刪除，重導至首頁 |

## 2. 每個路由的詳細說明

### 首頁 (`/`)
- **輸入**：無特別參數（可選用 GET 參數做月份篩選如 `?month=YYYY-MM`）
- **處理邏輯**：
  - 呼叫 `Record.get_summary_by_month()` 取回該月的收入、支出、結餘。
  - 呼叫 `Record.get_all()` （或按月過濾的歷史紀錄）取得近期清單。
- **輸出**：傳入該些資料，讓 Jinja2 渲染 `templates/index.html`。
- **錯誤處理**：無。

### 建立紀錄 (`/expense/new` \ `/income/new` \ `/expense` \ `/income`)
- **輸入 (GET)**：無。
- **輸入 (POST)**：`amount`, `category`, `record_date`, `note` 欄位資料。
- **處理邏輯**：
  - POST 請求將接收到的欄位透過 `Record.create()` 存入資料庫。如果呼叫 `/expense`，則 `type` 指定為 `'expense'` ；如果呼叫 `/income`，`type` 則指定為 `'income'`。
- **輸出 (GET)**：渲染表單。
- **輸出 (POST)**：成功後執行 `redirect(url_for('main.index'))` 回到第一頁。
- **錯誤處理**：驗證欄位是否都有帶資料，少帶則由 flash message 顯示。

### 統計圖表 (`/statistics`)
- **輸入**：無。
- **處理邏輯**：
  - 從資料庫抓回過往紀錄或當月紀錄，整理成分類總額。
- **輸出**：將資料餵給 `templates/statistics.html` 渲染圖表。
- **錯誤處理**：無。

### 刪除 (`/record/<int:id>/delete`)
- **輸入**：URL 路徑中夾帶整數 `id`。
- **處理邏輯**：
  - 呼叫 `Record.get_by_id(id)` 檢查此筆紀錄是否存在。
  - 若存在則呼叫 `Record.delete(id)` 刪除紀錄。
- **輸出**：無論成功與否都 `redirect(url_for('main.index'))`。
- **錯誤處理**：如果 id 不存在則可選擇報錯或者靜默回首頁。

## 3. Jinja2 模板清單

| 檔案名稱 | 繼承 | 說明 |
| :--- | :--- | :--- |
| `base.html` | (自定義的根網頁) | 存放公用 `<head>`、CSS Bootstrap / Tailwind 與公用 Navbar |
| `index.html` | `base.html` | 呈現首頁儀表板數據區塊與近期明細的表格 |
| `expense_form.html` | `base.html` | 新增支出的表單介面 |
| `income_form.html` | `base.html` | 新增收入的表單介面 |
| `statistics.html` | `base.html` | 視覺化圖表整合畫面，需要載入 Chart.js 等函式庫 |

## 4. 路由骨架程式碼
請參考以下 Python 檔案中的 Blueprint 骨架：
- `app/routes/main.py`
- `app/routes/records.py`
