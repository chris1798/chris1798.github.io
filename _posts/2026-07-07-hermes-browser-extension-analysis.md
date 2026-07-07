# Hermes Browser Extension — 專案功能分析報告

> 來源：[abundantbeing/hermes-browser-extension](https://github.com/abundantbeing/hermes-browser-extension)
> 分析日期：2026-07-07

---

## 一、專案概覽

| 項目 | 內容 |
|------|------|
| **倉庫名稱** | abundantbeing/hermes-browser-extension |
| **描述** | Browser-native side panel for Hermes Agent — connect web context to your local Hermes runtime |
| **Star 數** | ~691+ |
| **Fork 數** | 54+ |
| **版本** | v0.1.9（Public Alpha） |
| **語言** | JavaScript（Chrome Extension Manifest V3） |
| **授權** | MIT |
| **作者** | Jon Komet (@abundantbeing) |
| **Commits** | 77+ commits，2 branches，8 tags |

---

## 二、專案架構

```
hermes-browser-extension/
├── manifest.json                    # Root MV3 extension manifest
├── extension/
│   ├── manifest.json                # 源碼 manifest
│   ├── background.js                # Service Worker（262 行）
│   ├── content.js                   # 頁面內容收集器（257 行）
│   ├── sidepanel.html               # 側邊面板 UI（491 行）
│   ├── sidepanel.js                 # 主邏輯（5,829 行）— 核心！
│   ├── sidepanel.css                # 樣式（3,080 行）— 支援 6 個主題
│   ├── voice-dictation.html/js      # 語音.Dictation 備用頁面
│   ├── request-permissions.html/js  # 權限請求輔助頁
│   ├── sidepanel-preview.html       # Visual QA 預覽
│   ├── assets/                      # 字體、圖示、圖片
│   └── lib/                         # 模組化庫（12 個模組）
├── companion-plugin/                # Python 插件骨架（fail-soft 原型）
├── scripts/                         # 建置腳本
├── tests/                           # 測試檔案
└── assets/readme/                   # README 截圖
```

### 核心模組

| 檔案 | 角色 | 行數 | 說明 |
|------|------|------|------|
| `background.js` | Service Worker | 262 | 側邊面板管理、YouTube 字幕擷取 |
| `content.js` | Content Script | 257 | 頁面內容收集、敏感資料遮罩 |
| `sidepanel.js` | 主邏輯 | 5,829 | Hermes API 客戶端 + UI 狀態管理 |
| `sidepanel.css` | 樣式 | 3,080 | 6 套主題、深色/淺色模式 |

---

## 三、核心功能

### 3.1 連接模式（3 種）

| 模式 | 預設地址 | 認證方式 | 備註 |
|------|----------|----------|------|
| **本地 API** | `http://127.0.0.1:8642` | Bearer Token | 預設模式 |
| **遠端 API** | `http(s)://<host>:8642` | Bearer Token | 需 CORS 白名單 |
| **遠端 Dashboard (WS)** | `https://<dashboard-url>` | OAuth + Ticket | 僅 WS 功能，REST 功能不可用 |

### 3.2 頁面內容收集（content.js）

**收集項目**：
- 可讀文字（清除 script/style 後）
- 使用者選取文字
- 頁面標題與 URL
- 標頭（最多 25 個）
- 互動元素（連結、按鈕、表單，最多 40 個）
- 頁面 metadata（描述、語言、canonical URL）
- YouTube 影片 ID 與字幕軌跡
- 所有已開啟的分頁（若啟用）

**文字深度模式**：
- **Minimal** — 4K 字元
- **Normal** — 12K 字元
- **Full** — 30K 字元

### 3.3 安全與隱私機制

**敏感資料遮罩**：
- API Keys
- Bearer Tokens
- JWTs
- GitHub Tokens
- AWS Keys
- Slack Tokens
- Private Keys

**受限制頁面**（自動遮罩）：
- 銀行頁面
- 加密貨幣頁面
- 密碼管理頁面
- 醫療頁面
- 政府頁面

**隱私保護**：
- 所有頁面內容以「untrusted context」包裝後才發送至 Hermes
- 敏感 token 儲存於 `chrome.storage.local`，保存後永不顯示
- 只讀瀏覽器內容擷取（不支援點擊/輸入/表單提交行為）
- 每次訊息後顯示「What Hermes saw」收據（透明化）

### 3.4 快速命令（Quick Commands）

| 命令 | 功能 |
|------|------|
| `/summarize` | 摘要當前頁面 |
| `/explain` | 解釋當前頁面 |
| `/rewrite` | 重寫當前頁面文字 |
| `/tabs` | 列出所有已開啟分頁 |
| `/action-items` | 從頁面中提取待辦事項 |
| `/actions` | 列出可用行動 |

### 3.5 語音輸入（3 層回退）

```
第一層：Hermes STT（本地語音識別）
  ↓ 不可用
第二層：Browser Speech API（瀏覽器內建）
  ↓ 不可用
第三層：Extension Tab 頁語音（備用頁）
```

### 3.6 側邊面板功能

- **串流回應**：即時顯示 Hermes 回應與 token 使用量
- **模型選擇器**：瀏覽已連接 Hermes runtime 中的所有可用模型
- **情境範圍**：「跟隨活躍分頁」/「僅頁面」/「僅對話」
- **拖放附件**：支援檔案、圖片、資料夾
- **Live Tool Activity Strip**：即時顯示 Hermes tool 呼叫
- **模型發現**：從 API 伺服器、Dashboard、Session 歷史、外部來源
- **Agent 發現**：掃描本機執行中的 Hermes 實例
- **相容性面板**：顯示已支援/未支援功能
- **支援診斷**：遮罩後的 bug 報告工具
- **自動更新檢查**：比對 GitHub main branch
- **鍵盤快捷鍵**：`Alt+H` 開啟面板

---

## 四、Lib 模組化庫（12 個模組）

| 模組 | 功能 |
|------|------|
| `common.mjs` | 共用工具（渲染、遮罩、session 處理） |
| `commands.mjs` | 快速命令定義與解析 |
| `context-scope.mjs` | Tab/session 情境管理 |
| `panel-residency.mjs` | 側邊面板附著模式（tab-attached / global） |
| `browser-context-protocol.mjs` | 瀏覽器內容載荷通訊協定 |
| `runtime-events.mjs` | Runtime tool 事件正規化 |
| `support-diagnostics.mjs` | 遮罩式診斷報告 |
| `transcript.mjs` | YouTube 字幕擷取與解析 |
| `gateway-ws.mjs` | Gateway WebSocket 客戶端 |
| `dashboard-bridge.mjs` | Dashboard 認證與 ticket minting |
| `capabilities.mjs` | Gateway 功能探測 |
| `readiness.mjs` | 啟動就緒檢查 |
| `agent-discovery.mjs` | 本機 agent 掃描 |
| `model-discovery.mjs` | 多來源模型發現 |

---

## 五、權限需求

### 必要權限
| 權限 | 用途 |
|------|------|
| `activeTab` | 存取活躍分頁 |
| `scripting` | 注入 content scripts |
| `sidePanel` | 開啟側邊面板 |
| `storage` | 持久化設定 |
| `tabs` | 管理分頁 |

### 選填權限
| 權限 | 用途 |
|------|------|
| `audioCapture` | 麥克風（語音輸入） |

### 主機權限
- `http://127.0.0.1/*` / `http://localhost/*` — 本地 Hermes API
- `http://*/*` — 遠端 API
- `https://*/*` — Dashboard WebSocket

### 未實現（deferred）
`debugger`、`nativeMessaging`、`downloads`、`cookies`、`history`、`bookmarks`、瀏覽器控制權限

---

## 六、依賴與環境需求

| 項目 | 需求 |
|------|------|
| **Node.js** | 20+ |
| **Chrome** | 114+（Side Panel API） |
| **Hermes Agent** | 必須已安裝並運行 |

### 開發指令
```bash
npm run verify   # 測試 + 語法檢查 + manifest 驗證
npm run build    # 複製 extension/ 到 dist/
npm run lint     # ESLint
npm test         # 執行測試
```

---

## 七、資料流

```
使用者輸入（文字/語音）
    ↓
sidepanel.js（Composer）
    ↓
content.js（頁面內容收集 + 敏感資料遮罩）
    ↓
browser-context-protocol（封裝載荷）
    ↓
Hermes API Server / Dashboard WebSocket
    ↓
Hermes Agent Runtime
    ↓
串流回應 → sidepanel.js 即時渲染
```

### 發送至 Hermes 的資料
- 使用者訊息（文字或語音轉錄）
- 活躍分頁：標題 + URL
- 選取文字
- 可讀頁面文字（清理後）
- 頁面 metadata
- 標頭（最多 25 個）
- 互動元素（最多 40 個）
- 所有已開啟分頁（若啟用）
- YouTube 字幕（若可用）
- 附件（檔案、圖片、剪貼內容）
- 遮罩後內容（敏感資料已處理）

---

## 八、Companion Plugin（Python 原型）

位置：`companion-plugin/`

| 檔案 | 說明 |
|------|------|
| `__init__.py` | 插件初始化 |
| `context_store.py` | 情境儲存 |
| `events.py` | 事件處理 |
| `hooks.py` | Hermes hooks |
| `plugin.yaml` | 插件配置 |
| `policy.py` | 政策執行 |
| `protocol.py` | 協定輔助 |
| `tools.py` | 插件工具 |
| `skills/hermes-browser/SKILL.md` | Skill 文檔 |

**狀態**：Private prototype（fail-soft），不註冊 API-server 路由，不含瀏覽器控制通道。

---

## 九、GitHub 整合

- `npm run review:watch` — 本機 poller 偵測開放 PR/Issue
- `npm run review:event` — GitHub Actions / Webhook 事件運行器

---

## 十、文檔

| 文件 | 說明 |
|------|------|
| `README.md` | 完整指南（含截圖、安裝說明、疑難排解） |
| `CHANGELOG.md` | 版本歷史（v0.1.0-alpha → v0.1.9） |
| `CONTRIBUTING.md` | 貢獻指南 |
| `CONTRIBUTORS.md` | 貢獻者名單 |
| `DATA-FLOW.md` | 資料流文檔 |
| `PERMISSIONS.md` | 權限文檔 |
| `PRIVACY.md` | 隱私文檔 |
| `SECURITY.md` | 安全文檔 |

---

## 十一、安全模型

1. **本地 API 預設**：遠端需明確指定 URL、token、CORS
2. **強認證**：Bearer / API key 為必要條件
3. **只讀擷取**：不支援點擊/輸入/表單提交
4. **受限制頁面自動遮罩**：銀行/加密貨幣/密碼/醫療/政府頁面
5. **敏感資料遮罩**：API key、token、private key 等在發送前遮罩
6. **token 安全儲存**：僅存於 `chrome.storage.local`，保存後永不顯示
7. **透明化收據**：每次訊息後顯示「What Hermes saw」

---

## 十二、總結

這是一個**生產品質的 Chrome MV3 擴展**，提供原生側邊面板介面，作為 Chrome/Edge/Chromium 瀏覽器與 Hermes Agent 本機執行環境之間的橋接層。核心特色：

- ✅ **原生瀏覽器體驗**：側邊面板、分頁追蹤、語音輸入
- ✅ **隱私優先**：敏感資料遮罩、只讀模式、受限頁面保護
- ✅ **靈活連接**：支援本地 API、遠端 API、Dashboard WebSocket 三種模式
- ✅ **即時回饋**：串流回應、Live Tool Activity Strip、What Hermes saw 收據
- ✅ **多模型支援**：自動發現 Hermes runtime 中的可用模型
- ✅ **模組化架構**：12 個獨立模組，易於維護與擴展
- ✅ **完整文件**：README、CHANGELOG、安全/隱私/資料流文檔齊全

**適用人群**：使用 Hermes Agent 的開發者與進階用戶，希望將瀏覽器內容無縫整合至 AI 對話中的使用者。
