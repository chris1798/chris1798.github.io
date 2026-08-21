---
title: "Google 開源 MCP 資料庫服務器：MCP Toolbox for Databases 功能說明與安裝 SOP"
date: 2026-08-21
description: "Google 官方開源的 Model Context Protocol (MCP) 資料庫服務器，讓 AI Agent、IDE、應用程式直接連上企業資料庫。本文完整解說其雙重定位、支援資料庫、核心功能，並提供從零到上線的完整安裝 SOP。"
tags: [mcp, googleapis, database, agent, ai-tool, mcp-toolbox, 資料庫]
---

# MCP Toolbox for Databases 功能說明與安裝 SOP

[MCP Toolbox for Databases](https://github.com/googleapis/mcp-toolbox) 是 Google 官方開源的 [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) 資料庫服務器，讓 AI Agent、IDE、應用程式能直接連上企業資料庫。

它原本名為「Gen AI Toolbox for Databases」（`googleapis/genai-toolbox`），後為與 MCP 相容而更名為 `mcp-toolbox`。目前最新穩定版為 **v1.9.0**，採用 Apache 2.0 授權。

![MCP Toolbox for Databases 架構](/assets/images/mcp-toolbox/architecture.png)

## 一、為什麼需要 MCP Toolbox？

這是一套同時具備「**即用型服務器**」與「**自訂工具框架**」雙重定位的開源專案：

| 定位 | 說明 | 適合情境 |
|------|------|----------|
| **Build-Time（即用型）** | 使用預先建立的通用工具（Prebuilt Tools），一行配置即可讓 AI 工具連上資料庫 | 讓 Gemini CLI、Claude Code、Codex 等直接查詢資料、探索 Schema |
| **Run-Time（自訂框架）** | 用 `tools.yaml` 建立高度客製化、高安全性 AI 工具 | 生產環境中，定義結構化查詢、語義搜尋、NL2SQL |

**核心價值：**

- 🚀 **開箱即用**：預建通用工具（如 `list_tables`、`execute_sql`），無需寫重複程式碼即可查詢資料
- 🛠️ **自訂框架**：用結構化查詢 + 受限存取（Restricted Access）確保安全性
- ⚡ **簡化開發**：整合進 ADK、LangChain、LlamaIndex 等，少於 10 行程式碼即可完成
- 📈 **效能優異**：內建連線池、整合式驗證（IAM）、端到端可觀察性（OpenTelemetry）
- 🔒 **強化安全**：整合身份驗證，讓資料存取更安全
- 📊 **端到端可觀察性**：內建 OpenTelemetry 支援，提供指標與追蹤

## 二、支援的資料庫

Toolbox 支援海量資料庫，涵蓋雲端平台與常見開源資料庫：

### 雲端平台（Google Cloud）

| 資料庫 | 說明 |
|--------|------|
| AlloyDB | Google 高效能 PostgreSQL 相容資料庫 |
| BigQuery | 企業級資料倉儲 |
| Cloud SQL | 支援 PostgreSQL / MySQL / SQL Server |
| Spanner | 全球分散式關聯式資料庫 |
| Firestore | NoSQL 文件式資料庫 |
| Knowledge Catalog | 原 Dataplex 資料治理 |

### 其他資料庫

PostgreSQL、MySQL、MariaDB、SQL Server、Oracle、MongoDB、Redis、Elasticsearch、CockroachDB、ClickHouse、Couchbase、Neo4j、Snowflake、Trino 等。

> 💡 支援清單持續擴充，完整資料可參考 [Prebuilt Tools Reference](https://mcp-toolbox.dev/documentation/configuration/prebuilt-configs/)。

## 三、核心功能：`tools.yaml` 配置檔案

Toolbox 透過 `tools.yaml` 設定檔案定義所有功能，主要包含四大區塊：

### 1. Sources（資料來源）

定義 Toolbox 可以存取的資料連線資訊：

```yaml
kind: source
name: my-pg-source
type: postgres
host: 127.0.0.1
port: 5432
database: toolbox_db
user: toolbox_user
password: my-password
```

### 2. Tools（工具）

定義 AI Agent 可以執行的動作、使用的來源與參數：

```yaml
kind: tool
name: search-hotels-by-name
type: postgres-sql
source: my-pg-source
description: Search for hotels based on name.
parameters:
  - name: name
    type: string
    description: The name of the hotel.
statement: SELECT * FROM hotels WHERE name ILIKE '%' || $1 || '%';
```

### 3. Toolsets（工具集）

將多個工具分組，方便依 Agent 或應用程式載入：

```yaml
kind: toolset
name: my_first_toolset
tools:
    - my_first_tool
    - my_second_tool
```

### 4. Prompts（提示模板）

定義可用於與 LLM 互動的提示模板：

```yaml
kind: prompt
name: code_review
description: "Asks the LLM to analyze code quality and suggest improvements."
messages:
  - content: >
         Please review the following code for quality, correctness,
         and potential improvements: \n\n{{.code}}
arguments:
  - name: "code"
    description: "The code to review"
```

---

## 四、安裝 SOP（標準作業流程）

以下提供三種主要安裝方式，依需求選擇其一即可。

### ✅ 方法一：NPM 執行（最簡單，適合快速測試）

適合已安裝 Node.js 的使用者，一行命令即可啟動：

```bash
# 使用自訂工具
npx @toolbox-sdk/server --config tools.yaml

# 或使用預建工具（範例：PostgreSQL）
npx -y @toolbox-sdk/server --prebuilt=postgres --stdio
```

> ⚠️ 此方法為求方便而設計，效能與穩定性最佳化建議使用下列二、三法。

### ✅ 方法二：下載二进制檔（推薦，適合生產環境）

**Windows（PowerShell）：**

```powershell
$VERSION = "1.9.0"
curl.exe -o toolbox.exe "https://storage.googleapis.com/mcp-toolbox-for-databases/v$VERSION/windows/amd64/toolbox.exe"
```

**Windows（Command Prompt）：**

```cmd
set VERSION=1.9.0
curl -o toolbox.exe "https://storage.googleapis.com/mcp-toolbox-for-databases/v%VERSION%/windows/amd64/toolbox.exe"
```

**Linux（AMD64）：**

```bash
export VERSION=1.9.0
curl -L -o toolbox https://storage.googleapis.com/mcp-toolbox-for-databases/v$VERSION/linux/amd64/toolbox
chmod +x toolbox
```

**macOS（Apple Silicon）：**

```bash
export VERSION=1.9.0
curl -L -o toolbox https://storage.googleapis.com/mcp-toolbox-for-databases/v$VERSION/darwin/arm64/toolbox
chmod +x toolbox
```

### ✅ 方法三：Docker 容器

```bash
export VERSION=1.9.0
docker pull us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:$VERSION

docker run -p 5000:5000 \
  -v $(pwd)/tools.yaml:/app/tools.yaml \
  us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:$VERSION \
  --config "/app/tools.yaml"
```

> 🍺 若使用 macOS / Linux，也可透過 Homebrew 安裝：`brew install mcp-toolbox`

### 📦 由原始碼編譯（開發者）

需先安裝 [Go](https://go.dev/doc/install)：

```bash
go install github.com/googleapis/mcp-toolbox@v1.9.0
```

---

## 五、啟動與連線

### 啟動服務器

下載二進制檔後，確認已建立 `tools.yaml`，即可啟動：

```bash
./toolbox --config "tools.yaml"
```

> 🔁 **動態重載**：Toolbox 預設啟用動態重載。如需關閉，加上 `--disable-reload` 旗標。
>
> 可用 `toolbox help` 查看所有可用旗標；按 `Ctrl+C` 可停止服務。

### 連接到 MCP 客戶端

在 MCP 相容的 IDE 或客戶端（如 Gemini CLI、Claude Code、Codex 等）的設定檔（通常為 `mcp.json` 或 `claude_desktop_config.json`）中加入：

```json
{
  "mcpServers": {
    "toolbox": {
      "type": "http",
      "url": "http://127.0.0.1:5000/mcp"
    }
  }
}
```

若只想連接到特定工具集，將 URL 改為 `http://127.0.0.1:5000/mcp/{工具集名稱}`。

---

## 六、其他進階功能

### 1. Toolbox UI（互動式測試介面）

使用 `--ui` 旗標啟動互動式網頁界面，可直接測試工具與參數：

```bash
./toolbox --ui
```

### 2. Telemetry（可觀察性）

Toolbox 透過 OpenTelemetry 匯出追蹤與指標：

```bash
--telemetry-otlp=<endpoint>
```

可匯出到任何 OTLP 相容後端（如 Google Cloud Monitoring 等）。

### 3. Generate Agent Skills（生成 Agent 技能）

使用 `skills-generate` 命令，可將「工具集」轉換為符合 [Agent Skill 規格](https://agentskills.io/specification) 的技能包：

```bash
toolbox --config tools.yaml skills-generate \
  --name "my-skill" \
  --toolset "my_toolset" \
  --description "A skill containing multiple tools"
```

生成後可安裝進 Gemini CLI：

```bash
gemini skills install ./skills/my-skill
```

### 4. 多語言 SDK 整合

Toolbox 提供 Python、JavaScript/TypeScript、Go、Java 等多語言 SDK，可輕鬆將工具整合到自訂應用程式中。

**Python（核心）範例：**

```python
from toolbox_core import ToolboxClient

async with ToolboxClient("http://127.0.0.1:5000") as client:
    tools = await client.load_toolset("toolset_name")
```

**JavaScript（核心）範例：**

```javascript
import { ToolboxClient } from '@toolbox-sdk/core';

const URL = 'http://127.0.0.1:5000';
let client = new ToolboxClient(URL);
const tools = await client.loadToolset('toolsetName');
```

完整 SDK 清單與文件請見 [Toolbox SDKs](https://mcp-toolbox.dev/)。

---

## 七、版本政策

MCP Toolbox for Databases 遵循 [語義化版本控制](https://semver.org/)（Semantic Versioning）：

| 版本層級 | 觸發條件 |
|----------|----------|
| Major（主版本） | 不相容的 CLI 或設定檔變更 |
| Minor（次版本） | 新增功能，含預建工具集或 beta 功能變更 |
| Patch（修補） | 向後相容的錯誤修正 |

---

## 八、常見問題

**Q1：舊的 `genai-toolbox` 倉庫怎麼辦？**
若已克隆舊倉庫，請更新 remote：

```bash
git remote set-url origin https://github.com/googleapis/mcp-toolbox.git
```

**Q2：需要管理型服務嗎？**
Google Cloud 提供 [管理型 MCP Servers](https://cloud.google.com/blog/products/databases/managed-mcp-servers-for-google-cloud-databases)，適合想要免維運的使用者。差異說明見 [FAQ](https://mcp-toolbox.dev/dev/reference/faq/)。

**Q3：完整文件在哪裡？**
完整文件請至官方文件網站：[https://mcp-toolbox.dev](https://mcp-toolbox.dev/)

---

## 九、總結

MCP Toolbox for Databases 是 Google 推出的一站式資料庫 AI 整合方案，兼具「**開箱即用**」與「**高度客製**」雙重能力。透過標準化的 MCP 協定，它能讓各種 AI Agent、IDE、應用程式安全、高效地存取企業資料，同時內建連線池、身份驗證、可觀察性等企業級功能，是建構 AI-Database 應用場景的理想基礎設施。

無論你是想快速在開發環境測試，還是準備上線生產環境，Toolbox 都能提供對應的安裝方式與支援。

**快速連結：**

- 📦 [原始碼倉庫](https://github.com/googleapis/mcp-toolbox)
- 📖 [官方文件](https://mcp-toolbox.dev/)
- 🏷️ [版本釋放](https://github.com/googleapis/mcp-toolbox/releases)
- 💬 [Discord 社群](https://discord.gg/Dmm69peqjh)
