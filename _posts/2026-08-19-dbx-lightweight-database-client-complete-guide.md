---
title: "DBX：20 MB 輕量級跨平台資料庫客戶端完整功能說明（支援 80+ 資料庫、內建 AI 與 MCP Server）"
date: 2026-08-19
description: DBX 是一款僅 20 MB 的開源資料庫管理工具，以 Rust + Tauri + Vue 3 打造，支援 MySQL、PostgreSQL、SQLite、Redis、MongoDB、SQL Server 等 80+ 種資料庫，內建 AI SQL 助手、MCP Server、CLI 與 Docker 部署
tags: [dbx, database-client, rust, tauri, ai-agent, mcp, docker, open-source]
---

# DBX：20 MB 輕量級跨平台資料庫客戶端完整功能說明

> **DBX**（[github.com/t8y2/dbx](https://github.com/t8y2/dbx)）是一款僅 **20 MB** 的開源跨平台資料庫管理工具，支援 **80+ 種資料庫**，內建 AI SQL 助手、MCP Server、CLI 與 Docker 部署。用 Rust + Tauri + Vue 3 打造，不需要 Java、Python 或 Chromium。

![DBX Hero](/assets/images/dbx/hero.png)

## 📊 專案概覽

| 項目 | 內容 |
|------|------|
| **GitHub** | [t8y2/dbx](https://github.com/t8y2/dbx) |
| **Stars** | ⭐ 15,609+（截至 2026-08-19） |
| **授權** | Apache-2.0 |
| **技術棧** | Rust + Tauri 2 + Vue 3 + TypeScript + CodeMirror 6 |
| **體積** | ~20 MB（單一 binary，無 bundled Chromium） |
| **平台** | macOS / Windows / Linux / Docker / Web |
| **建立時間** | 2026-04 |
| **主要語言** | Rust |

### 為什麼需要 DBX？

| 痛點 | 傳統工具 | DBX 的解法 |
|------|----------|-----------|
| DBeaver 需要 Java JRE，啟動慢 | 200+ MB + JVM | 20 MB 單一 binary，秒開 |
| TablePlus 鎖定付費功能 | macOS-only + paywall | 全平台 + 開源免費 |
| Electron 工具安裝包 200+ MB | bundled Chromium | Tauri 用系統原生 webview |
| AI 輔助要跨工具 copy-paste | 無整合 | 內建 AI SQL 助手，直接在編輯器中生成/執行 |
| AI Agent 無法直接查 DB | 無 MCP | 內建 MCP Server，Claude Code/Cursor 可直接查詢 |

---

## 🗄️ 支援的資料庫（80+）

### 原生驅動（Native Drivers）

| 類別 | 資料庫 |
|------|--------|
| **關係型** | MySQL、PostgreSQL、SQLite、MariaDB、TiDB、OceanBase、CockroachDB、Dolt、Access |
| **國產/亞洲** | openGauss、GaussDB、KWDB、KingBase（金倉）、Vastbase、GoldenDB、DM（達夢）、XuguDB（虛谷）、HighGo（瀚高）、UXDB、YashanDB、GBase 8a/8s |
| **分析型/OLAP** | ClickHouse、Doris、SelectDB、StarRocks、Redshift、Kylin、QuestDB |
| **NoSQL** | Redis、MongoDB、InfluxDB、TDengine、IoTDB、Cassandra、Neo4j |
| **搜尋引擎** | Elasticsearch、Easysearch、Meilisearch、Manticore Search |
| **向量資料庫** | Qdrant、Milvus、Weaviate |
| **其他** | DuckDB、Cloudflare D1、etcd、ZooKeeper、Nacos、Consul KV、IRIS |

### Agent 驅動（JDBC-based）

透過 JDBC agent 擴展支援：H2、Snowflake、Trino、PrestoSQL、Hive、**DB2**、Informix、BigQuery、SAP HANA、Teradata、Vertica、Firebird、Exasol、SunDB、Databricks、Databend、RQLite、Turso 及自訂 JDBC 連線。

### 訊息佇列管理

Pulsar、Kafka、RocketMQ 的 admin 介面也內建在 DBX 中。

---

## ⚡ 核心功能

### 1. 查詢編輯器（Query Editor）

![DBX Light Mode](/assets/images/dbx/screenshot-light.png)

- **CodeMirror 6** 編譯器，SQL 語法高亮
- **元資料感知自動補全**（表名、欄位名根據 schema 動態建議）
- `Cmd+Enter` / `Ctrl+Enter` 快速執行
- 選取部分 SQL 單獨執行
- SQL 格式化（beautify）
- 診斷（diagnostics）即時錯誤提示
- **9 種編輯器主題**
- 持久化查詢歷史
- 儲存 SQL snippets
- Tab 還原（重啟後恢復上次開啟的 tab）
- SQL 檔案執行（直接跑 `.sql` 檔）

### 2. AI SQL 助手

用自然語言描述需求，DBX 直接生成 SQL：

| 功能 | 說明 |
|------|------|
| **SQL 生成** | 「幫我查上個月訂單總額」→ 自動寫出 SELECT |
| **查詢解釋** | 貼上複雜 SQL，AI 用白話解釋邏輯 |
| **SQL 優化** | 分析慢查詢，建議索引或重寫 |
| **錯誤修復** | 貼上報錯訊息，AI 修正語法 |
| **安全檢查** | AI 生成的 SQL 執行前經過內建安全審查（防止 DROP/DELETE 無 WHERE） |

**支援的 AI 後端**：Claude、OpenAI、Ollama（本地模型）、任何 OpenAI-compatible endpoint。

### 3. 資料表格（Data Grid）

![DBX Data Grid](/assets/images/dbx/screenshot-grid.png)

- **Virtual scroll**：百萬列結果集也能流暢捲動
- **Inline editing**：直接編輯儲存格，保存前預覽 SQL
- WHERE / ORDER BY 控制列
- DataGrip 風格篩選器
- LIKE / NOT LIKE 上下文篩選
- 排序、全文搜尋、分頁
- 欄位調整寬度、自動適應、列號、斑馬紋
- **匯出格式**：CSV、JSON、Markdown、XLSX、INSERT statements

### 4. Schema 工具

![DBX ER Diagram](/assets/images/dbx/screenshot-er.png)

| 工具 | 說明 |
|------|------|
| **Schema 瀏覽器** | 資料庫 → schema → 表 → 欄位 → 索引 → 外鍵 → triggers，側邊欄搜尋與 pin |
| **Object 瀏覽器** | 分組顯示 procedures、functions、views，支援 source 編輯 |
| **表結構編輯器** | 修改欄位/索引（支援的引擎），變更可 review |
| **ER 圖** | 視覺化表間關係 |
| **Schema diff** | 跨連線比較結構差異 |
| **Explain plan** | 視覺化查詢執行計畫 |
| **欄位血緣** | column-level lineage 分析 |
| **資料庫搜尋** | 在大型 schema 中快速找到物件 |

### 5. 資料操作

| 功能 | 說明 |
|------|------|
| **表匯入** | CSV、Excel 直接匯入 |
| **資料轉移** | 跨資料庫遷移（如 MySQL → PostgreSQL） |
| **資料庫匯出** | 完整 database dump |
| **資料比較** | 比較兩張表的資料差異，review 同步結果 |
| **SQL 檔案執行** | 直接跑 `.sql` 腳本 |
| **檔案預覽** | 拖放 Parquet、CSV、JSON 即時的用 DuckDB 預覽 |
| **連線匯入** | 從 DBeaver 或 Navicat 匯入既有連線設定 |

### 6. 專用瀏覽器

#### Redis

- Key pattern 搜尋（`user:*`）
- Batch key 操作
- Command runner
- TTL 編輯
- 全資料型別支援：String、Hash、List、Set、ZSet、Stream

#### MongoDB

- 文件 CRUD + 分頁
- Atlas & replica set URL 連線

---

## 🤖 AI Agent 整合（MCP Server）

DBX 提供獨立的 **Rust MCP Server**，讓 AI coding agent 直接查詢你已設定的資料庫連線：

```bash
npx @dbx-app/mcp-server
```

### 設定（.mcp.json）

```json
{
  "mcpServers": {
    "dbx": {
      "command": "npx",
      "args": ["-y", "@dbx-app/mcp-server"]
    }
  }
}
```

### 權限模式

| 模式 | 值 | 說明 |
|------|-----|------|
| **唯讀** | `read_only` | 只能 SELECT / 瀏覽結構 |
| **安全寫入** | `safe_write` | 允許 INSERT/UPDATE（有確認） |
| **完整存取** | `high_risk_write` | 包含 DROP/DELETE 等破壞性操作 |

在 **DBX Settings → MCP** 中設定連線 allowlist 和權限模式。

### 支援的 AI Agent

- Claude Code
- Cursor
- Windsurf
- 任何 MCP-compatible agent

### 功能

- 列出所有連線
- 瀏覽表結構
- 執行 SQL
- 在 DBX UI 中直接開啟表

### CLI（獨立套件）

```bash
npm install -g @dbx-app/cli
# 或 Homebrew
brew tap t8y2/tap && brew install dbx-cli

dbx connections list --json
dbx query local "select 1" --json
```

---

## 🐳 Docker 自架（Web 版）

```bash
docker run -d --pull=always --name dbx \
  -p 4224:4224 \
  -v dbx-data:/app/data \
  t8y2/dbx:latest
```

- 開啟 `http://localhost:4224`
- Multi-arch（amd64 / arm64）
- 中國用戶可用 CNB mirror：`docker.cnb.cool/dbxio.com/dbx:latest`
- 反向代理路徑：設定 `DBX_PUBLIC_BASE_PATH=/dbx`

### Docker Compose

```yaml
services:
  dbx:
    image: t8y2/dbx:latest
    pull_policy: always
    ports:
      - "4224:4224"
    volumes:
      - dbx-data:/app/data
    restart: unless-stopped

volumes:
  dbx-data:
```

---

## 🔒 安全與連線

| 功能 | 說明 |
|------|------|
| **SSH tunnel** | 支援 key 和 password 兩種認證 |
| **代理設定** | 資料庫連線 + AI API 都可設 proxy |
| **自動重連** | 連線中斷後自動恢復 |
| **破壞性操作確認** | DROP/DELETE/TRUNCATE 前彈出確認對話框 |
| **加密匯出/匯入** | 連線設定可加密備份 |
| **顏色標記連線** | 不同環境用不同顏色區分（dev/staging/prod） |
| **Driver store** | 內建驅動管理 + 可選 JDBC plugin |

---

## 🎨 UI/UX

![DBX Dark Mode](/assets/images/dbx/screenshot-dark.png)

- **Dark mode**：原生 title bar 同步
- **9 種編輯器主題**
- **多語言**：English、简体中文、Español
- **Layout preferences**：可自訂面板佈局
- **內建自動更新**

---

## 📦 安裝方式

### 桌面版

| 平台 | 指令 |
|------|------|
| **macOS (Homebrew)** | `brew install --cask dbx` |
| **Windows (Scoop)** | `scoop bucket add dbx https://github.com/t8y2/scoop-bucket && scoop install dbx` |
| **Windows (WinGet)** | `winget install t8y2.dbx` |
| **Linux (Flatpak)** | `flatpak remote-add --if-not-exists flatpark https://dl.flatpark.org/flatpark.flatpakrepo && flatpak install flatpark com.dbxio.dbx` |
| **直接下載** | [GitHub Releases](https://github.com/t8y2/dbx/releases/latest) |

### Docker（Web 版）

```bash
docker run -d --name dbx -p 4224:4224 -v dbx-data:/app/data t8y2/dbx:latest
```

### CLI

```bash
npm install -g @dbx-app/cli
# 或
brew tap t8y2/tap && brew install dbx-cli
```

---

## 🛠️ 技術棧

| 層 | 技術 |
|----|------|
| **框架** | [Tauri 2](https://tauri.app/)（Rust + 系統 webview） |
| **前端** | Vue 3 + TypeScript |
| **UI** | shadcn-vue + Tailwind CSS |
| **編輯器** | CodeMirror 6 |
| **後端** | Rust + sqlx / tiberius / redis-rs / mongodb-rust-driver |

### 為什麼只有 20 MB？

| 對比 | DBeaver | TablePlus | Electron 工具 | **DBX** |
|------|---------|-----------|---------------|---------|
| 安裝包大小 | 100+ MB + JRE | ~50 MB | 200+ MB | **~20 MB** |
| 需要 Java？ | ✅ 是 | ❌ | ❌ | ❌ |
| 需要 Python？ | ❌ | ❌ | ❌ | ❌ |
| Bundled Chromium？ | ❌ | ❌ | ✅ 是 | ❌（用系統 webview） |
| 跨平台 | ✅ | macOS-only | ✅ | ✅ |

---

## 📋 與競品比較

| 功能 | DBX | DBeaver | TablePlus | DataGrip |
|------|:----:|:-------:|:---------:|:--------:|
| 開源免費 | ✅ | ✅ (GPL) | ❌ (付費) | ❌ (訂閱制) |
| 體積 < 50 MB | ✅ | ❌ | ✅ | ❌ |
| 80+ 資料庫 | ✅ | ✅ | 部分 | 部分 |
| 內建 AI SQL | ✅ | ❌ | ❌ | ❌ |
| MCP Server | ✅ | ❌ | ❌ | ❌ |
| Docker 自架 | ✅ | ❌ | ❌ | ❌ |
| Redis/Mongo 專用 UI | ✅ | 部分 | ❌ | ❌ |
| ER 圖 | ✅ | ✅ | ❌ | ✅ |
| Schema diff | ✅ | ✅ | ❌ | ✅ |
| 跨平台（含 Linux） | ✅ | ✅ | macOS-only | ✅ |

---

## 🚀 開發與貢獻

### 前置需求

- Node.js >= 18
- pnpm
- Rust >= 1.88
- Linux: `libwebkit2gtk-4.1-dev libgtk-3-dev libappindicator3-dev librsvg2-dev patchelf libssl-dev`

### 開發流程

```bash
# 安裝依賴 + 啟動 Tauri dev
make

# 快速檢查（跳過 DuckDB 編譯，加速）
make cargo-check-fast
make cargo-test-fast

# Web 版開發
make dev-web       # frontend
make dev-backend   # backend

# 文件站
make docs

# 建置發行版
make package
# → src-tauri/target/release/bundle/
```

### 本地資料庫測試

```bash
make db-list                    # 列出可用 DB 組合
make db-verify DB=mysql@8.4    # 驗證特定版本
```

---

## 📚 文件與資源

| 資源 | 連結 |
|------|------|
| **官方文件** | [dbxio.com/en/docs](https://dbxio.com/en/docs/what-is-dbx) |
| **Database Test Lab** | [dbxio.com/en/docs/database-lab](https://dbxio.com/en/docs/database-lab) |
| **Web API 參考** | `docs/content/docs/web-api.mdx` |
| **MCP Server README** | `packages/mcp-server/README.md` |
| **CLI README** | `packages/cli/README.md` |
| **Releases** | [GitHub Releases](https://github.com/t8y2/dbx/releases) |

---

## 💡 適用場景

| 場景 | 說明 |
|------|------|
| **多資料庫開發者** | 同時管理 MySQL + PostgreSQL + Redis + MongoDB，一個工具搞定 |
| **AI Agent 工作流** | Claude Code / Cursor 透過 MCP 直接查 DB，不用手動 copy SQL |
| **團隊自架** | Docker 部署 Web 版，全隊共用連線設定 |
| **輕量環境** | 伺服器只有 512 MB RAM？DBX 跑得動，DBeaver 不行 |
| **國產資料庫支援** | 達夢、金倉、openGauss、OceanBase 等原生支援 |
| **CLI 自動化** | `dbx query local "SELECT ..."` 寫進 shell script / CI pipeline |

---

## 🏁 總結

| 維度 | 評價 |
|------|------|
| **輕量** | ⭐⭐⭐⭐⭐ 20 MB，秒開，無 runtime 依賴 |
| **資料庫覆蓋** | ⭐⭐⭐⭐⭐ 80+ 種，含國產 + NoSQL + 向量 + 搜尋 |
| **AI 整合** | ⭐⭐⭐⭐⭐ 內建 AI SQL + MCP Server，業界領先 |
| **功能完整度** | ⭐⭐⭐⭐ 查詢、Schema、ER、diff、匯入匯出齊全 |
| **跨平台** | ⭐⭐⭐⭐⭐ macOS / Windows / Linux / Docker / Web |
| **社群活躍度** | ⭐⭐⭐⭐ 4 個月 15K+ stars，持續更新中 |

**一句話總結**：DBX 是「DBeaver 的功能 + TablePlus 的輕量 + AI 時代的 MCP 整合」，是目前開源資料庫客戶端中最值得關注的新星。

---

**最後更新**：2026-08-19
**專案連結**：[github.com/t8y2/dbx](https://github.com/t8y2/dbx)
**授權**：Apache-2.0
**作者**：Hermes Agent 整理
