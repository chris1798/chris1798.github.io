---
title: "Gridex 完整功能介紹：Swift 原生跨平台資料庫 IDE，內建 MCP Server 與 AI Chat"
date: 2026-10-09
description: Gridex 是用 Swift + AppKit 打造的原生 macOS / Windows / Linux 資料庫 IDE，一個 App 連線 PostgreSQL、MySQL、SQLite、Redis、MongoDB、SQL Server、ClickHouse，並內建 MCP Server（15 個工具、5 層權限）與 AI Chat，讓 Claude / GPT / Gemini / Ollama 直接讀你的 schema 寫 SQL。
tags: [database, ide, mcp, ai, swift, postgresql, mysql, sqlite, redis, open-source]
---

# Gridex 完整功能介紹：Swift 原生跨平台資料庫 IDE，內建 MCP Server 與 AI Chat

## 專案概況

| 項目 | 內容 |
|---|---|
| 官方倉庫 | https://github.com/gridex/gridex |
| 官網 / 下載 | https://gridex.app |
| 定位 | AI-native 原生資料庫 IDE（macOS / Windows / Linux） |
| 技術棧 | macOS：Swift 5.10 + AppKit/SwiftUI；Windows：C++ + WinUI 3；Linux：C++20 + Qt 6 |
| 授權 | Apache-2.0 |
| Stars / Forks | 約 1,860+ / 156（2026-10 實測） |
| 建立時間 | 2026-04（曾登上 GitHub Trending / Trendshift） |
| 支援資料庫 | PostgreSQL、MySQL、SQLite、Redis、MongoDB、SQL Server、ClickHouse |
| 作者 | Thinh Nguyen |

Gridex 的兩個關鍵字是「**原生**」和「**AI-native**」：

- **原生**：不用 Electron、不用 WebView 畫資料表格——macOS 用 AppKit、Windows 用 WinUI 3、Linux 用 Qt 6，追求鍵盤驅動的快速介面。
- **AI-native**：把 MCP Server 和 AI Chat 直接做進 IDE 裡，讓 Claude Desktop、Cursor 等 MCP 客戶端能安全地讀你的資料庫。

![Gridex 總覽](/assets/images/gridex/show-case.png)

## 支援的資料庫與驅動

七種資料庫共用同一個 `DatabaseAdapter` 協議（約 50 個方法），因此**表格編輯、查詢編輯器、ER 圖、備份、MCP 等所有功能在每个資料庫上行為一致**：

| 資料庫 | 驅動 | 特色 |
|---|---|---|
| PostgreSQL | PostgresNIO（Vapor） | 參數化查詢、mTLS、sequences、完整 schema 檢視 |
| MySQL | MySQLNIO | 字元集處理、TLS、keepalive 自動重連 |
| SQLite | 系統 libsqlite3 | 檔案型、WAL 模式、零設定 |
| Redis | RediStack | Key 瀏覽器、SCAN 過濾、Server INFO 儀表板、Slow Log 檢視、`rediss://` TLS |
| MongoDB | MongoKitten（純 Swift） | 文件編輯器、NDJSON 備份/還原、aggregation pipeline |
| SQL Server | CosmoSQLClient（TDS 7.4，免 FreeTDS） | 原生 `BACKUP DATABASE`、stored procedures |
| ClickHouse | 純 Swift（URLSession HTTP） | 8123/8443 HTTP(S)、完整 mTLS（PKCS#12）、`system.*` 內部檢視、版本感知（CH 20.8+） |

平台覆蓋：macOS 全 7 種；Linux/Windows 6 種（ClickHouse 目前僅 macOS）。

## 核心功能

### 1. 內建 MCP Server（重點特色）

把任何已儲存的連線暴露給 MCP 客戶端（Claude Desktop、Cursor、自建 agent）：

- 傳輸：macOS stdio、Windows stdio + HTTP、Linux stdio
- **15 個工具、5 個權限層級**：

| 層級 | 工具 | 執行條件 |
|---|---|---|
| Schema | `list_connections`、`list_schemas`、`list_tables`、`describe_table`、`list_relationships`、`get_sample_rows` | 已啟用連線一律允許 |
| Read | `query`、`explain_query`、`search_across_tables` | `read_only` 以上；SQL sanitizer 拒絕寫入語句 |
| Write | `insert_rows`、`update_rows`、`delete_rows`、`execute_write_query` | 僅 `read_write`；行數估測器標記大量變更；需使用者核准 |
| DDL | （規劃中的 schema migration 工具） | `read_write` + 明確核准 |
| Advanced | （規劃中的 admin 工具） | 明確核准 |

**安全機制**（每層都是獨立元件）：

- `MCPPermissionEngine`：每條連線獨立模式（`locked` / `read_only` / `read_write`）
- `MCPSQLSanitizer`：拒絕越層的 DDL/DML
- `MCPIdentifierValidator`：防識別符 SQL 注入
- `MCPRowCountEstimator`：變更前預覽會影響多少列
- `MCPRateLimiter`：每工具每分鐘呼叫上限
- `MCPApprovalGate`：破壞性操作彈出人工核准

![MCP Server 設定](/assets/images/gridex/mcp.png)

**MCP 活動記錄**：每次工具呼叫都記錄層級、SQL、耗時、影響列數、核准狀態——「agent 昨晚對我的資料庫做了什麼」可以直接查，不用猜。MCP 視窗含 Overview / Setup / Connections / Activity / Advanced 五個分頁。

![MCP 活動記錄](/assets/images/gridex/mcp-logs.png)

### 2. AI Chat（讀你的 schema 寫 SQL）

內建聊天能理解你的表結構，SQL 生成範圍鎖定在你選的連線：

- **Anthropic Claude**：串流、tool use、extended thinking
- **OpenAI**：GPT-4.x / 5.x、function calling
- **Google Gemini**：Flash 與 Pro
- **Ollama**：本地模型，不需要 API key

隱私設計：請求從你的機器**直連**模型供應商，Gridex 不做代理；API key 存 macOS Keychain / Windows Credential Manager。

### 3. 資料表格與查詢編輯器

**資料表格**
- 儲存格內聯編輯（型別感知解析）
- 排序、過濾、分頁、欄寬調整、多欄排序
- 增删列有 pending-change 追蹤，一次 transaction 提交
- 複製列、匯出 CSV / JSON / SQL

**查詢編輯器**
- 多分頁（依資料庫分組的 Chrome 式分頁列）
- 語法高亮（關鍵字、字串、數字、註解、函式）
- 執行選取區或全部
- Redis 連線有 Redis CLI 模式
- 查詢歷史經 SwiftData 持久化：可搜尋、可收藏

**Schema 工具**
- 結構檢視：欄位、索引、外鍵、constraints
- 函式 / stored procedure 檢視器（原始碼 + 參數）
- Create Table / Create Database 對話框（型別感知預設值）

### 4. ER 圖（關係圖）

![ER Diagram](/assets/images/gridex/diagram.png)

- macOS：自製 `NSView` + CoreGraphics 渲染器；Windows：in-process Dagre 排版 + WebView。**兩平台都不需要外部 d2 / Graphviz 執行檔**
- 自動排版、平移、縮放、fit-to-view、外鍵關係走線
- 直接讀取目前連線的 live schema，不需要匯入步驟
- 點欄位跳到該表、雙開直接看資料

### 5. SSH Tunnel 與 mTLS

- **SSH Tunnel**：密碼 / 私鑰 / 帶 passphrase 的私鑰三種認證，經 `swift-nio-ssh` 做本地端口轉發；每個活躍連線一條 tunnel，斷線自動拆除
- **mTLS（Teleport 式）**：`sslKeyPath` + `sslCertPath` + `sslCACertPath` 雙向 TLS，PostgreSQL / MySQL / Redis / ClickHouse 全鏈路可用；ClickHouse 支援 PKCS#12 客戶端憑證套件 + pinned CA

### 6. 備份與還原

| 資料庫 | 備份方式 |
|---|---|
| PostgreSQL | `pg_dump`（custom / SQL / tar）+ `pg_restore` |
| MySQL | `mysqldump` + `mysql` |
| SQLite | 檔案複製 |
| MongoDB | NDJSON（每行一文件，純 Swift） |
| Redis | 經 SCAN 的 JSON snapshot（純 Swift） |
| SQL Server | 原生 `BACKUP DATABASE` |
| ClickHouse | SQL dump（`SHOW CREATE TABLE` + `FORMAT Values`，純 Swift） |

支援選表備份、壓縮、進度回報。

### 7. 從其他工具匯入連線

可直接匯入 **TablePlus**、**Navicat**（NCX，Blowfish 解密）、**DataGrip**、**DBeaver** 的連線設定——包含 SSH 設定與 keychain 裡的密碼，換工具幾乎零成本。

### 8. 隱私立場

憑證全部留在本機（macOS Keychain / Windows Credential Manager），**沒有雲端同步、沒有遥測、沒有代理**——這對值班/生產資料庫場景（資料不能出去）是重要賣點。

## 安裝

三平台都有官方安裝檔：

- **macOS**：universal DMG（Apple Silicon + Intel），簽章 + 公證，Sparkle 自動更新
- **Windows**：Velopack 安裝程式（Windows 10/11），支援 delta 更新
- **Linux**：x86_64 AppImage（Qt 6），經 JSON feed 自我更新

自建需求：macOS 14+ / Swift 5.10+ / Xcode 15+；Windows 10+ / VS 2022 / .NET 8 / vcpkg；Ubuntu 22.04+/Debian 12/Fedora 40 + Qt 6.4+ / GCC 11+ / CMake 3.24+。

```bash
# macOS 開發建置
git clone https://github.com/gridex/gridex.git && cd gridex
swift build && .build/debug/Gridex
./scripts/build-app.sh   # 或產出 .app

# Linux
cmake -S linux -B linux/build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build linux/build --parallel
```

## 技術架構

Clean Architecture 五層，依賴一律指向內層：

```
macos/
├── App/            生命週期、DI 容器、AppState
├── Core/           協議、模型、enum（零依賴）
│   └── Protocols/  DatabaseAdapter, LLMService, SchemaInspectable, MCPTool
├── Domain/         Use cases、repository 協議
├── Data/           7 個資料庫 Adapter + SwiftData 持久化 + Keychain
├── Services/       QueryEngine / AI(4 providers) / MCP / SSH / Export
└── Presentation/   AppKit 視圖、SwiftUI 設定、ViewModels
windows/            C++ WinUI 3
linux/              C++20 Qt 6（adapters、MCP、AppImage）
```

關鍵設計：

- `DatabaseAdapter` 協議統一七個驅動；`LLMService` 統一四個模型供應商（`AsyncThrowingStream` 串流）
- 執行緒安全用 Swift `actor`：`QueryEngine`、`ConnectionManager`、`SSHTunnelService`、`BackupService`、`MCPServer`
- 全 `async/await`、資料模型全 `Sendable`
- 驅動全部選純 Swift / SwiftNIO 系（PostgresNIO、MySQLNIO、RediStack、MongoKitten、swift-nio-ssh），ClickHouse 直接用 URLSession——不綁 C 函式庫（SQL Server 也刻意避開 FreeTDS）

## 與近似工具比較

| | Gridex | DBeaver | TablePlus | DataGrip |
|---|---|---|---|---|
| 技術 | 原生（AppKit/WinUI/Qt） | Java/Eclipse | 原生（macOS/Win） | JetBrains JVM |
| Redis / MongoDB / ClickHouse | ✅ | 部分 | ❌（Redis 另購） | 部分 |
| 內建 MCP Server | ✅ 15 工具＋權限層＋稽核 | ❌ | ❌ | ❌ |
| 內建 AI Chat（含 Ollama 本地） | ✅ | 外掛 | ❌ | ❌ |
| 遥測 | 無 | 有 | 有 | 有 |
| 授權 | Apache-2.0 開源 | GPL/商業 | 付費 | 付費 |
| 平台 | macOS/Win/Linux | 全 | 全 | 全 |

Gridex 的差異點：**開源＋原生＋MCP-first**。它把「AI agent 安全地存取資料庫」當成 IDE 的一等功能，而不是外掛——權限層級、SQL sanitizer、稽核記錄都是內建的。

## 適用情境

- **讓 Claude Desktop / Cursor 直接查你的資料庫**：開 MCP 就能問 schema、跑 read-only 查詢，寫入需核准且有記錄。
- **值班/生產 DB 管理**：SSH tunnel + mTLS + 無遥測，符合敏感環境要求。
- **多引擎混用**（Postgres + Redis + MongoDB 同時開）：一個 App 全部搞定，含 Redis Slow Log、Mongo aggregation 等引擎專屬工具。
- **從 TablePlus / DBeaver 遷移**：連線直接匯入。

## 小結

Gridex 是「下一代資料庫 IDE」形態的開源嘗試：用原生 UI 換掉 Electron 的重量，用統一 Adapter 協議換掉各引擎各做一套的功能碎片，再把 MCP Server 做成帶權限模型與稽核記錄的一級功能。對正在用 Claude Desktop / Cursor / 自建 agent 接資料庫的人（例如把 DB2、MS SQL 查詢流程交給 agent 的場景），它是目前把「AI 存取資料庫的安全邊界」做得最完整的開源工具之一。

## 星數成長

![Star History](/assets/images/gridex/star-history.svg)

## 參考連結

- 官方倉庫：https://github.com/gridex/gridex
- 官網與下載：https://gridex.app/download
- Discord 社群：https://discord.gg/UuV2Ktc6
- Releases：https://github.com/gridex/gridex/releases
