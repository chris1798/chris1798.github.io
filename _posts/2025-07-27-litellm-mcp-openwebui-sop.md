---
title: "LiteLLM MCP Gateway 整合 Open WebUI 完整 SOP"
date: 2025-07-27
description: 手把手教你在 LiteLLM Proxy 中新增 MCP Server 與 Tools，並串接 Open WebUI 使用。
tags: [liteLLM, MCP, Open WebUI, AI Gateway, Tools]
---

# LiteLLM MCP Gateway 整合 Open WebUI 完整 SOP

> **版本資訊**：LiteLLM v1.80+，Open WebUI v0.6.31+，MCP Protocol 2025-11-25

## 架構說明

整個流程是：

```
使用者 → Open WebUI → LiteLLM Proxy (MCP Gateway) → MCP Server(s) → Tools
```

- **LiteLLM Proxy** 扮演 MCP Gateway，提供固定 endpoint 管理所有 MCP tools
- **Open WebUI** 作為前端，透過 MCP Streamable HTTP 連到 LiteLLM
- **MCP Servers** 可以是 HTTP/SSE/stdio 三種 transport 之一

## 前置需求

1. **LiteLLM Proxy** 已安裝並運行（建議 v1.80+）
2. **Open WebUI** 已安裝並運行（v0.6.31+）
3. MCP Server 已準備好（第三方如 DeepWiki、Zapier，或自訂）

---

## Step 1：LiteLLM 啟用 MCP 儲存

要讓 LiteLLM 在資料庫中管理 MCP Server，需啟用 DB 儲存。

**環境變數方式：**

```bash
export STORE_MODEL_IN_DB=True
```

**config.yaml 方式（推薦）：**

```yaml
general_settings:
  store_model_in_db: true
  # 只儲存 MCP（可選）
  # supported_db_objects: ["mcp"]
```

---

## Step 2：在 LiteLLM 新增 MCP Server

兩種方式：UI 或 config.yaml。

### 方式 A：LiteLLM Admin UI

1. 開啟 LiteLLM UI → **MCP Servers** → **Add New MCP Server**
2. 輸入 Server URL 與 Transport 類型
3. 支援三種 transport：
   - **Streamable HTTP**（推薦，Open WebUI 使用此種）
   - **SSE**（Server-Sent Events）
   - **STDIO**（本地程式）

### 方式 B：config.yaml（推薦，便於版本管理）

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: sk-xxxxxxx

litellm_settings:
  # MCP Aliases（簡化呼叫名稱，可選）
  mcp_aliases:
    "github": "github_mcp"
    "zapier": "zapier_mcp"

mcp_servers:
  # ---- 範例 1: HTTP Streamable Server（推薦） ----
  deepwiki_mcp:
    url: "https://mcp.deepwiki.com/mcp"
    transport: "http"          # 預設 sse，Open WebUI 建議用 http
    description: "DeepWiki MCP"

  # ---- 範例 2: SSE Server ----
  zapier_mcp:
    url: "https://actions.zapier.com/mcp/sk-xxxx/sse"
    transport: "sse"

  # ---- 範例 3: STDIO Server（本地） ----
  circleci_mcp:
    transport: "stdio"
    command: "npx"
    args: ["-y", "@circleci/mcp-server-circleci"]
    env:
      CIRCLECI_TOKEN: "your-token"

  # ---- 範例 4: 帶認證的 HTTP Server ----
  github_mcp:
    url: "https://api.githubcopilot.com/mcp"
    auth_type: "bearer_token"
    auth_value: "ghp_your_token"
    description: "GitHub MCP with auth"

  # ---- 範例 5: OAuth 2.0 ----
  oauth_server:
    url: "https://example.com/mcp"
    auth_type: "oauth2"
    client_id: "os.environ/OAUTH_CLIENT_ID"
    client_secret: "os.environ/OAUTH_CLIENT_SECRET"
    scopes: ["tool.read", "tool.write"]
```

#### Auth Type 選項對照表

| auth_type | 產生的 Header |
|-----------|---------------|
| `none` | 無 |
| `api_key` | `X-API-Key: <value>` |
| `bearer_token` | `Authorization: Bearer <value>` |
| `basic` | `Authorization: Basic <value>` |
| `oauth2` | `Authorization: Bearer <token>`（PKCE/M2M） |
| `aws_sigv4` | AWS Signature V4 |

> **重要**：從 v1.80.18 起，MCP Server 名稱必須符合 SEP-986（工具命名規範），建議使用小寫 + 底線。

#### 讓特定 MCP 對所有 API Key 可用

```yaml
mcp_servers:
  public_mcp:
    url: "https://example.com/mcp"
    allow_all_keys: true   # 不需要特別授權
```

---

## Step 3：重啟 LiteLLM Proxy

```bash
# Docker 方式
docker restart litellm

# 直接運行方式
# Ctrl+C 後重新執行
litellm --config config.yaml
```

---

## Step 4：驗證 MCP Server 正常

### 列出所有可用 tools

```bash
curl http://localhost:4000/mcp-rest/tools/list \
  -H "Authorization: Bearer YOUR_LITELLM_API_KEY"
```

### 呼叫單一 tool（不需 LLM）

```bash
curl http://localhost:4000/mcp-rest/tools/call \
  -H "Authorization: Bearer YOUR_LITELLM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "deepwiki_mcp/get_wiki_content",
    "arguments": {"url": "https://example.com"}
  }'
```

如果能看到 tools 列表與回傳結果，代表 LiteLLM 端的 MCP 設定正確。

---

## Step 5：Open WebUI 串接 LiteLLM MCP

Open WebUI 本身支援 MCP，我們要把它連到 LiteLLM Proxy 的 MCP Gateway。

### Step 5.1：設定 LiteLLM API Key

在 Open WebUI 環境變數或設定中加入 LiteLLM 的 API Key：

```bash
# docker-compose.yml 中的 Open WebUI service
environment:
  - LITELLM_API_KEY=sk-your-litellm-key
```

### Step 5.2：Open WebUI 新增 MCP Server

1. 登入 Open WebUI → **Admin Settings** → **External Tools**
2. 點擊 **+ Add Server**
3. 設定：
   - **Type**: `MCP (Streamable HTTP)` ⚠️ 不是 OpenAPI
   - **Server URL**: `http://litellm:4000/mcp`（Docker 內網）或 `http://localhost:4000/mcp`
   - **Auth**: 輸入 LiteLLM API Key（Bearer Token）

> **常見錯誤**：Type 選成 OpenAPI 會導致 UI 卡住。務必選 `MCP (Streamable HTTP)`。

### Step 5.3：驗證

1. 存檔後，回到 Open WebUI 對話畫面
2. 選擇模型
3. 詢問一個需要工具的的問題（例如「用 DeepWiki 幫我抓取某個文件」）
4. 如果 LiteLLM 與 MCP Server 正常，模型會自動呼叫工具並回傳結果

---

## Step 6：進階設定

### 6.1 限制特定 API Key / Team 可用 MCP

透過 LiteLLM UI 的 MCP Permission Management，可以：

- 依 API Key 限制可用 MCP Server
- 依 Team 授權
- 依 Organization 管控

```bash
# 建立受限 API Key
curl http://localhost:4000/keys/new \
  -H "Authorization: Bearer sk-master-key" \
  -d '{
    "permissions": {
      "mcp_servers": ["deepwiki_mcp", "zapier_mcp"]
    }
  }'
```

### 6.2 傳入自訂 Headers

若 MCP Server 需要額外 headers：

```yaml
mcp_servers:
  my_server:
    url: "https://example.com/mcp"
    extra_headers: ["X-Custom-Header", "Authorization"]
    static_headers:
      X-Tenant-ID: "my-org"
```

在請求時用 header 指定：

```bash
# 格式：x-mcp-{server_alias}-{header_name}
curl http://localhost:4000/chat/completions \
  -H "x-mcp-my_server-authorization: Bearer token123"
```

### 6.3 使用 LiteLLM 的 /responses endpoint

呼叫 `/v1/responses` 時，`server_url` 必須用字串 `"litellm_proxy"`：

```bash
curl http://localhost:4000/v1/responses \
  -H "Authorization: Bearer sk-key" \
  -d '{
    "model": "gpt-4o",
    "tools": [{
      "type": "mcp",
      "server_label": "litellm",
      "server_url": "litellm_proxy",
      "require_approval": "never"
    }],
    "input": "幫我查 DeepWiki",
    "tool_choice": "required"
  }'
```

---

## 故障排除

| 問題 | 原因 | 解法 |
|------|------|------|
| Open WebUI 顯示 "MCP server not responding" | URL 錯誤或 LiteLLM 未啟動 | 檢查 `http://litellm:4000/mcp` 可達性 |
| 工具列表是空的 | MCP Server 未正確註冊 | 檢查 `curl /mcp-rest/tools/list` |
| UI 卡在 Loading | Type 選成 OpenAPI | 重設為 `MCP (Streamable HTTP)` |
| OAuth 工具每次重啟都失效 | Open WebUI 未設 `WEBUI_SECRET_KEY` | 加入環境變數並重新建立 container |
| 權限不足 | API Key 未獲 MCP 授權 | 檢查 Key 的 `mcp_servers` permission |

更多排錯請參考 [LiteLLM MCP Troubleshooting Guide](https://docs.litellm.ai/docs/mcp_troubleshooting)。

---

## 相關文件

- [LiteLLM MCP Overview](https://docs.litellm.ai/docs/mcp)
- [LiteLLM MCP Usage](https://docs.litellm.ai/docs/mcp_usage)
- [Open WebUI MCP](https://docs.openwebui.com/features/extensibility/mcp/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

---

> **更新記錄**
> - 2025-07-27：首版發布
