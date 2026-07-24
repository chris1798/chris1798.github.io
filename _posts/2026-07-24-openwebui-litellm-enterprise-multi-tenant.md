---
layout: post
title: "Open WebUI + LiteLLM 企業級多租戶部署指南：整合、權限與部門化模型管理"
date: 2026-07-24
description: 使用 Open WebUI 作為前端、LiteLLM 作為代理層，搭建企業內部多人使用的 LLM 平台，並按部門隔離模型權限與費用。
tags: [AI, LiteLLM, Open WebUI, Enterprise, Multi-Tenant]
---

# Open WebUI + LiteLLM 企業級多租戶部署指南

## 架構總覽

企業內部部署 AI 平台的典型架構如下：

```
使用者 ──→ Open WebUI (UI 層, 權限管理) ──→ LiteLLM Proxy (API 層, 模型路由) ──→ 多個 LLM Provider
```

各層角色：

| 組件 | 職責 |
|------|------|
| **Open WebUI** | 使用者介面、帳號管理、RBAC（功能權限）、聊天歷史、知識庫 |
| **LiteLLM Proxy** | 統一 API 入口、模型路由（100+ 模型）、**Team 層多租戶隔離**、費用追蹤與限額、API Key 管理 |
| **上游 Provider** | OpenAI / Azure / Anthropic / Bedrock / Vertex / 本地模型等 |

核心原則：**RBAC 在 Open WebUI 管 UI 功能，Team + Virtual Key 在 LiteLLM 管模型存取與費用**。

---

## 第一步：部署 LiteLLM Proxy

### 安裝與基本啟動

```bash
pip install litellm[proxy]

# 建立 config.yaml（下方說明）
litellm --config config.yaml --port 4000
```

### config.yaml 範例（企業多租戶）

```yaml
general_settings:
  master_key: sk-your-master-key-change-me
  max_budget: 5000          # 全站總預算上限 (USD)
  budget_duration: 30d

# 上游模型定義
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: claude-sonnet-4
    litellm_params:
      model: claude-sonnet-4-20250514
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: llama-3-70b
    litellm_params:
      model: ollama/llama3.1:70b
      api_base: http://localhost:11434
```

### 啟動管理 UI

LiteLLM 內建管理面板：`http://<server>:4000/ui`

在此可管理 Organization / Team / User / Key，無需寫 API。

---

## 第二步：多租戶架構 — 按部門隔離

LiteLLM 的層級模型：

```
Organization (企業版) ──→ Team ──→ User ──→ Virtual Key
```

- **Open Source 版**：最高層級為 Team，適合以「部門」為租戶
- **Enterprise 版**：加上 Organization 層（SSO、審計日誌等）

### 建立部門 Teams

透過 Admin UI (`/ui`) 或 API 建立。以下為 API 範例：

```bash
# 工程團隊 — 可存取高階模型 + 較高的預算與速率
curl -X POST http://localhost:4000/team/new \
  -H "Authorization: Bearer sk-your-master-key" \
  -H "Content-Type: application/json" \
  -d '{
    "team_alias": "engineering",
    "max_budget": 500,
    "budget_duration": "30d",
    "rpm_limit": 1000,
    "models": ["gpt-4o", "claude-sonnet-4", "llama-3-70b"]
  }'

# 行銷團隊 — 限制模型 + 較低預算
curl -X POST http://localhost:4000/team/new \
  -H "Authorization: Bearer sk-your-master-key" \
  -H "Content-Type: application/json" \
  -d '{
    "team_alias": "marketing",
    "max_budget": 200,
    "budget_duration": "30d",
    "rpm_limit": 500,
    "models": ["gpt-4o"]
  }'

# 財務團隊 — 僅本地模型，零外部 API 費用
curl -X POST http://localhost:4000/team/new \
  -H "Authorization: Bearer sk-your-master-key" \
  -H "Content-Type: application/json" \
  -d '{
    "team_alias": "finance",
    "max_budget": 50,
    "rpm_limit": 200,
    "models": ["llama-3-70b"]
  }'
```

### Team 隔離能力

| 能力 | 說明 |
|------|------|
| **模型存取** | Team 的 `models` 清單決定成員可用哪些模型 |
| **預算限制** | `max_budget` + `budget_duration`，超支後請求被拒 |
| **速率限制** | `rpm_limit` (req/min) + `tpm_limit` (tokens/min) |
| **Team Admin** | 可指派 team admin 管理該部門成員與 Key，無需 proxy_admin 權限 |
| **費用歸屬** | 所有請求的費用自動歸算至 Team、User、Key |

### 加入使用者至 Team

```bash
# 建立使用者
curl -X POST http://localhost:4000/user/new \
  -H "Authorization: Bearer sk-your-master-key" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "alice@company.com"}'

# 加入 engineering team
curl -X POST http://localhost:4000/team/member_add \
  -H "Authorization: Bearer sk-your-master-key" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "<engineering-team-id>",
    "max_budget_in_team": 100,
    "member": {
      "role": "user",
      "user_id": "alice@company.com"
    }
  }'
```

---

## 第三步：Open WebUI 連接 LiteLLM

### 啟動 Open WebUI

```bash
docker run -d -p 3000:8080 \
  -v open-webui:/app/backend/data \
  -e ENABLE_FORWARD_USER_INFO_HEADERS=True \
  ghcr.io/open-webui/open-webui:main
```

### 建立 LiteLLM Virtual Key

為 Open WebUI 建立一個服務用 Key，指定其可存取哪些模型：

```bash
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer sk-your-master-key" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "<your-team-id>",
    "models": ["*"]
  }'
# 記錄回傳的 key，例如 sk-owui-xxx
```

### 在 Open WebUI 中新增連接

1. 開啟 Open WebUI → **Settings** → **Connections**
2. 新增 OpenAI Compatible 連接：
   - **URL**: `http://<litellm-server>:4000`
   - **Key**: 上方建立的 Virtual Key

此時 Open WebUI 的模型下拉選單只會顯示該 Key 被允許的模型。

---

## 第四步：Open WebUI 權限管理（RBAC）

Open WebUI 有三層權限架構：

1. **Role** — Admin / User / Pending
2. **Group** — 自訂群組，可額外授予權限
3. **Permission** — 細部功能開關（加總制：True 優先）

### 推薦設定方式

```
Global Default（最低權限） ──→ Group（部門/角色） ──→ User
```

1. **Global Default**：設為「所有人都需要的最小權限」
   - 聊天基本功能：開啟
   - 進階功能（Image Gen、Code Interpreter、Tools）：關閉

2. **建立部門 Groups**：
   - `Engineering-Users` — 開啟 Web Search、Code Interpreter、API Keys
   - `Marketing-Users` — 開啟 Image Generation、Web Search
   - `Finance-Users` — 僅基本聊天、Temporary Chat

3. **ACL 共用模型/知識庫**：
   - 某些模型或 Knowledge Base 可設為「僅特定 Group 可見」

### 注意事項

- **Tools Access ≈ Root 權限**（可執行任意 Python 代碼），僅授與受信任者
- Open WebUI RBAC **不控制模型存取** — 模型層由 LiteLLM Team 管轄

---

## 第五步：端對端模型存取控制流程

完整的模型存取限制在 LiteLLM 與 Open WebUI 兩層實現：

```
使用者登入 Open WebUI
    │
    ├── Open WebUI Role + Group → 決定 UI 功能權限
    │       (能否用 Image Gen / Code Interpreter / Web Search)
    │
    ├── Open WebUI Model ACL → 決定 UI 上顯示哪些模型
    │       (可設為僅特定 Group 可見某模型)
    │
    └── LiteLLM Team + Key → 決定 API 層實際能否呼叫某模型
            (最關鍵的防護層：即使 UI 顯示了，LiteLLM 仍會拒絶未經授權的模型)
```

### 實際操作範例

假設「行銷部 Alice」：

1. LiteLLM：`marketing` Team → 僅 `models: ["gpt-4o"]`
2. Open WebUI：`Marketing-Users` Group → 開啟 Image Gen，關閉 Code Interpreter
3. Open WebUI Model ACL：`gpt-4o` → 允許 `Marketing-Users` 使用
4. 結果：Alice 只能用 gpt-4o 和圖生成功能，無法呼叫 claude 或 llama

---

## 第六步：每人用量追蹤

### 啟用使用者 Header 傳遞

Open WebUI 環境變數：
```bash
ENABLE_FORWARD_USER_INFO_HEADERS=True
```

LiteLLM `config.yaml`：
```yaml
general_settings:
  user_header_mappings:
    - header_name: X-OpenWebUI-User-Id
      litellm_user_role: internal_user
    - header_name: X-OpenWebUI-User-Email
      litellm_user_role: customer
```

### 效果

- LiteLLM `/ui/logs` 可看到每個請求對應的 Open WebUI 使用者
- 可建立個人 API Key，綁定 LiteLLM User + Team，實現**每人獨立預算**

---

## 第七步：進階 — SSO 與自動 provisioning

### 方案 A：Keycloak / Azure AD + LiteLLM JWT

LiteLLM 支援 JWT Auth，可接 OIDC 提供者：

```yaml
general_settings:
  jwt_auth:
    issuer: "https://login.microsoftonline.com/{tenant_id}/v2.0"
    algorithm: "RS256"
```

### 方案 B：Open WebUI + LDAP / SAML

Open WebUI 支援 LDAP、OIDC、SAML（企業版），可接現有 AD。

### 自動將新使用者分配到 Team

使用 Webhook 或管理腳本：當使用者在 Open WebUI 註冊時，呼叫 LiteLLM API 自動建立 User + 加入對應 Team。

```python
import requests

LITELLM_URL = "http://litellm-server:4000"
MASTER_KEY = "sk-your-master-key"

def provision_user(email, department):
    # 建立 user
    resp = requests.post(f"{LITELLM_URL}/user/new",
        headers={"Authorization": f"Bearer {MASTER_KEY}"},
        json={"user_id": email})
    
    # 加入 team (需先查詢 team_id)
    team_id = get_team_id(department)
    requests.post(f"{LITELLM_URL}/team/member_add",
        headers={"Authorization": f"Bearer {MASTER_KEY}"},
        json={"team_id": team_id, "member": {"user_id": email}})
```

---

## 部署架構總結

| 需求 | 由誰負責 |
|------|---------|
| 使用者登入、帳號管理 | Open WebUI（可接 LDAP/SAML） |
| UI 功能權限（Image Gen、Code Interpreter 等） | Open WebUI RBAC |
| 模型存取控制 | **LiteLLM Team `models` 清單**（關鍵） |
| 部門費用隔離 | LiteLLM Team Budget |
| 每人用量追蹤 | LiteLLM User + Header Mapping |
| 速率限制、API Key 管理 | LiteLLM |
| 審計日誌（API 層） | LiteLLM `/logs`（可接 Langfuse / S3） |

---

## 參考資料

- [Open WebUI RBAC 文件](https://docs.openwebui.com/features/authentication-access/rbac/)
- [LiteLLM Multi-Tenant Architecture](https://docs.litellm.ai/docs/proxy/multi_tenant_architecture)
- [LiteLLM + Open WebUI Tutorial](https://docs.litellm.ai/docs/tutorials/openweb_ui)
- [LiteLLM Users & Budgets](https://docs.litellm.ai/docs/proxy/users)
- [LiteLLM Admin UI](https://docs.litellm.ai/docs/proxy/admin_ui)
