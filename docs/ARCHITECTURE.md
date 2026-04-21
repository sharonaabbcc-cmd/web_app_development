# 系統架構設計 (Architecture)

## 1. 技術架構說明
本專案採用經典的伺服器端渲染 (Server-Side Rendering) 架構，不進行前後端分離，以保持架構輕量且易於維護。

- **後端框架**：**Python + Flask**
  - **原因**：Flask 是輕量級的 Web 框架，適合小型專案與個人工具開發，開發速度快且彈性高。
- **模板引擎**：**Jinja2**
  - **原因**：與 Flask 深度整合，負責將後端資料動態渲染成 HTML 頁面並回傳給瀏覽器。
- **資料庫**：**SQLite**
  - **原因**：輕量級的關聯式資料庫，無需額外架設資料庫伺服器，資料儲存於單一檔案中，非常適合個人單機使用的應用情境。

**MVC 模式說明**：
- **Model (模型)**：負責資料庫的結構定義與資料存取邏輯（景點、筆記、標籤的 CRUD 操作）。
- **View (視圖)**：負責呈現使用者介面，由 Jinja2 模板 (HTML/CSS/JS) 構成。
- **Controller (控制器)**：由 Flask 的路由 (Routes) 擔任，負責接收使用者的 HTTP 請求、呼叫 Model 處理資料，並將結果傳遞給 View 渲染。

## 2. 專案資料夾結構
```text
web_app_development/
├── app/
│   ├── __init__.py        # Flask 應用程式初始化與配置
│   ├── models/            # 資料庫模型 (Model)
│   │   └── models.py      # 景點、筆記與標籤的資料表定義
│   ├── routes/            # Flask 路由控制器 (Controller)
│   │   └── spot_routes.py # 處理景點相關的 HTTP 請求
│   ├── templates/         # Jinja2 模板檔案 (View)
│   │   ├── base.html      # 網頁共用版型 (Header, Footer)
│   │   ├── index.html     # 景點列表與搜尋頁
│   │   ├── detail.html    # 景點詳細資訊與筆記頁
│   │   └── form.html      # 新增/編輯景點的表單頁
│   └── static/            # 靜態資源檔案
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── instance/
│   └── database.db        # SQLite 資料庫檔案
├── docs/
│   ├── PRD.md             # 產品需求文件
│   └── ARCHITECTURE.md    # 系統架構文件 (本文件)
├── requirements.txt       # Python 依賴套件清單
└── app.py                 # 應用程式執行入口
```

## 3. 元件關係圖

```mermaid
graph TD
    Browser[瀏覽器 (Client)]
    
    subgraph Server [Flask Web Server]
        Controller[Flask Route (Controller)]
        View[Jinja2 Template (View)]
        Model[Data Model (Model)]
    end
    
    DB[(SQLite Database)]

    Browser -- 1. HTTP Request (GET/POST) --> Controller
    Controller -- 2. 查詢 / 更新資料 --> Model
    Model -- 3. 讀寫 --> DB
    DB -- 4. 回傳資料 --> Model
    Model -- 5. 回傳資料 --> Controller
    Controller -- 6. 傳遞資料渲染 --> View
    View -- 7. 產生 HTML --> Controller
    Controller -- 8. HTTP Response (HTML) --> Browser
```

## 4. 關鍵設計決策

1. **採用 Server-Side Rendering (SSR) 搭配 Jinja2**
   - **原因**：此專案為個人使用的輕量級工具，不需要複雜的單頁應用 (SPA) 狀態管理。SSR 開發速度最快，且 SEO 與首次載入速度表現良好，能最快達成 MVP 目標。
2. **選擇 SQLite 作為資料庫**
   - **原因**：此專案只需支援單人存取，無高併發寫入需求。SQLite 免安裝、免設定，資料庫就是一個檔案 (`instance/database.db`)，備份與遷移極度方便。
3. **依功能拆分 Routes 與 Models**
   - **原因**：雖然目前專案規模不大，但將路由 (`routes/`) 與模型 (`models/`) 拆分至獨立資料夾，能讓程式碼職責更清晰。未來若加入「標籤管理」等功能，架構也能輕鬆擴充。
4. **表單與輸入安全防護**
   - **原因**：即使是個人工具，仍需考量基本的安全性。利用 ORM 的參數化查詢防範 SQL Injection，Jinja2 則會自動轉義字串防範 XSS，確保應用程式的安全。
