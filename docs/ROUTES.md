# 任務管理系統 - 路由與頁面設計 (Routes)

這份文件基於 PRD 與架構設計，詳細規劃了 Flask 應用程式的路由與對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 任務列表 (首頁) | GET | `/` | `index.html` | 取得資料庫中所有任務，顯示任務清單 |
| 新增任務頁面 | GET | `/tasks/create` | `task_form.html` | 顯示空白的新增任務表單 |
| 建立任務 | POST | `/tasks/create` | — | 接收表單並寫入資料庫，完成後重導向至 `/` |
| 編輯任務頁面 | GET | `/tasks/<int:id>/edit` | `task_form.html` | 顯示帶有原資料的表單供修改 |
| 更新任務 | POST | `/tasks/<int:id>/edit` | — | 接收表單並更新資料庫中特定 ID 紀錄，重導向至 `/` |
| 切換完成狀態 | POST | `/tasks/<int:id>/toggle` | — | 切換任務完成狀態，完成後重導向至 `/` |
| 刪除任務 | POST | `/tasks/<int:id>/delete` | — | 刪除特定 ID 任務，完成後重導向至 `/` |

*(註：由於 HTML 預設表單只支援 GET 與 POST，刪除與更新操作使用 POST)*

## 2. 每個路由的詳細說明

### `GET /` (任務列表)
- **輸入**：無
- **處理邏輯**：呼叫 `TaskModel.get_all()` 取得排序後的任務清單。
- **輸出**：渲染 `index.html`，並將任務串列 (list of dicts) 傳入模板。
- **錯誤處理**：若資料庫連線或查詢失敗，顯示 HTTP 500 錯誤。

### `GET /tasks/create` (新增任務頁面)
- **輸入**：無
- **處理邏輯**：不需存取資料庫，單純準備頁面。
- **輸出**：渲染 `task_form.html`，並傳遞變數讓模板知道目前是「新增」模式。

### `POST /tasks/create` (建立任務)
- **輸入**：表單欄位 `title` (必填), `description` (選填), `due_date` (選填)。
- **處理邏輯**：
  1. 後端驗證 `title` 欄位是否為空。
  2. 若無誤，呼叫 `TaskModel.create(...)` 將任務存入資料庫。
- **輸出**：重導向 (Redirect) 至首頁路由 `/`。
- **錯誤處理**：若 `title` 為空，重新渲染 `task_form.html` 並回傳 400 錯誤與提示訊息。

### `GET /tasks/<int:id>/edit` (編輯任務頁面)
- **輸入**：URL 路徑參數 `id`。
- **處理邏輯**：呼叫 `TaskModel.get_by_id(id)` 取得該任務原始資料。
- **輸出**：渲染 `task_form.html`，將取得的資料預先填入表單中，並傳遞變數標示目前為「編輯」模式。
- **錯誤處理**：若找不到該 ID，呼叫 `abort(404)` 回傳 404 Not Found 錯誤頁面。

### `POST /tasks/<int:id>/edit` (更新任務)
- **輸入**：URL 路徑參數 `id`，表單欄位 `title`, `description`, `due_date`。
- **處理邏輯**：
  1. 呼叫 `TaskModel.get_by_id(id)` 確認任務是否存在。
  2. 驗證 `title` 是否為空。
  3. 呼叫 `TaskModel.update(...)` 更新資料庫。
- **輸出**：重導向 (Redirect) 至首頁路由 `/`。
- **錯誤處理**：若找不到該 ID 回傳 404；若 `title` 為空，重新渲染表單並提示。

### `POST /tasks/<int:id>/toggle` (切換狀態)
- **輸入**：URL 路徑參數 `id`。
- **處理邏輯**：呼叫 `TaskModel.toggle_status(id)`。
- **輸出**：重導向 (Redirect) 至首頁路由 `/`。
- **錯誤處理**：若找不到該 ID，回傳 404。

### `POST /tasks/<int:id>/delete` (刪除任務)
- **輸入**：URL 路徑參數 `id`。
- **處理邏輯**：呼叫 `TaskModel.delete(id)`。
- **輸出**：重導向 (Redirect) 至首頁路由 `/`。
- **錯誤處理**：若找不到該 ID，回傳 404。

## 3. Jinja2 模板清單

所有的模板檔案將放置於 `app/templates/` 目錄下：

1. **`base.html`**
   - **說明**：所有頁面的基礎版型 (Base Template)，包含 `<html>` 結構、共用的 Header (網站標題)、Footer，以及載入 CSS/JS 的標籤。使用 `{% block content %}{% endblock %}` 預留給子模板填寫。
2. **`index.html`**
   - **說明**：首頁，繼承自 `base.html`。使用 `{% for task in tasks %}` 迴圈顯示任務清單。提供按鈕執行刪除、編輯與完成狀態切換。
3. **`task_form.html`**
   - **說明**：新增與編輯共用的表單，繼承自 `base.html`。根據後端傳入的變數 (如 `task` 物件是否存在) 動態改變表單的 `action` 網址、按鈕文字與標題。
