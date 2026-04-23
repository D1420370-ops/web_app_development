# 任務管理系統 - 流程圖文件 (Flowchart)

這份文件透過視覺化的流程圖展示使用者在系統中的操作路徑，以及在執行核心功能（例如新增任務）時，系統背後的元件如何互動與傳遞資料。

## 1. 使用者流程圖 (User Flow)

這個流程圖展示了使用者（學生）進入系統後可以進行的主要操作步驟。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 任務列表]
    B --> C{要執行什麼操作？}
    
    C -->|想記錄新任務| D[點擊「新增任務」]
    D --> E[進入填寫表單頁面]
    E --> F[送出表單]
    F -->|成功| B
    
    C -->|想更改內容| G[點擊特定任務的「編輯」]
    G --> H[進入修改表單頁面]
    H --> I[儲存修改]
    I -->|成功| B
    
    C -->|任務已完成| J[點擊「標記完成 / 未完成」]
    J --> B
    
    C -->|想移除任務| K[點擊「刪除」]
    K --> L{確認刪除？}
    L -->|是| M[刪除任務]
    M -->|成功| B
    L -->|否| B
```

## 2. 系統序列圖 (Sequence Diagram)

這個序列圖以「新增任務」為例，展示了從使用者填寫表單、送出到資料寫入資料庫的完整技術流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (HTML/JS)
    participant Flask as Flask 路由 (Controller)
    participant Model as Task Model (Model)
    participant DB as SQLite 資料庫
    
    User->>Browser: 填寫「新增任務」表單並點擊送出
    Browser->>Flask: POST /tasks/create (攜帶表單資料)
    Flask->>Flask: 驗證資料是否完整 (例如標題必填)
    alt 資料無效
        Flask-->>Browser: 重新渲染表單頁並顯示錯誤提示
    else 資料有效
        Flask->>Model: 呼叫 create_task(title, description, due_date)
        Model->>DB: 執行 SQL INSERT INTO tasks ...
        DB-->>Model: 回傳寫入成功及新建立的 ID
        Model-->>Flask: 回傳成功狀態
        Flask-->>Browser: 重導向 (Redirect) 至首頁任務列表
        Browser->>Flask: GET / (請求首頁)
        Flask->>Model: 呼叫 get_all_tasks()
        Model->>DB: 執行 SQL SELECT * FROM tasks ...
        DB-->>Model: 回傳任務資料集
        Model-->>Flask: 回傳 Python 串列
        Flask->>Browser: 渲染 index.html 並回傳 HTML
        Browser-->>User: 顯示更新後的任務列表
    end
```

## 3. 功能清單對照表

以下為目前規劃的系統功能與其對應的 URL 路徑及 HTTP 方法：

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
|---|---|---|---|
| 檢視任務清單 (首頁) | `/` 或 `/tasks` | GET | 取得並顯示所有任務清單（依到期日排序），即將到期者高亮顯示 |
| 顯示新增表單頁面 | `/tasks/create` | GET | 顯示空白的新增任務表單讓使用者填寫 |
| 處理新增任務請求 | `/tasks/create` | POST | 接收表單傳來的資料並寫入資料庫 |
| 顯示編輯表單頁面 | `/tasks/<int:id>/edit` | GET | 根據任務 ID，查詢該任務資料並填入表單中顯示 |
| 處理編輯任務請求 | `/tasks/<int:id>/edit` | POST | 接收更新後的表單資料並覆寫資料庫原有紀錄 |
| 切換任務完成狀態 | `/tasks/<int:id>/toggle` | POST | 點擊時切換該任務的完成 (completed) 狀態 |
| 刪除任務 | `/tasks/<int:id>/delete` | POST | 根據任務 ID 刪除該筆特定任務 |
