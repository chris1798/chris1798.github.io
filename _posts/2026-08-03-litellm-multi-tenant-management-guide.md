---
title: "LiteLLM 多租戶（Multi-Tenant）完整管理指南"
date: 2026-08-03
description: 深入解析 LiteLLM 四層多租戶架構、預算控制、模型路由、速率限制與企業級管理實踐
tags: [litellm, multi-tenant, enterprise, api-gateway, budget-control, rbac]
---

# LiteLLM 多租戶（Multi-Tenant）完整管理指南

LiteLLM 的多租戶功能讓單一 Proxy 可以同時服務多個部門、團隊或客戶，每個租戶擁有獨立的預算、模型權限和使用量追蹤，且彼此完全隔離。

![Architecture](https://docs.litellm.ai/docs/imgs/litellm-proxy-arch.png)

## 多租戶架構（四層隔離）

```
┌─────────────────────────────────────────────────────────┐
│               Organization（組織層）                      │
│          最高隔離層，Org 之間完全不可見                     │
│  Org Admin 可管理所有 Team，但無法看見其他 Org 的資料       │
└─────────────────┬───────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌──────────────┐     ┌──────────────┐
│   Team A     │     │   Team B     │
│  部門/團隊    │     │  部門/團隊    │
│  獨立預算     │     │  獨立預算     │
│  獨立模型列表  │     │  獨立模型列表  │
└──────┬───────┘     └──────┬───────┘
       │                    │
  ┌────┴────┐            ┌───┴───┐
  ▼         ▼            ▼       ▼
Virtual   Virtual    Virtual  Virtual
 Key 1    Key 2      Key 3    Key 4
```

| 層級 | 用途 | 隔離內容 | 管理員 | 是否需要企業版 |
|------|------|----------|--------|---------------|
| **Organization** | 跨公司、不同法人實體 | 資料、key、預算完全隔離 | Org Admin | ✅ 企業版 |
| **Team** | 部門/團隊 | 獨立預算、模型列表、key 管理 | Team Admin | ❌ 免費 |
| **Project** | Team 下子專案 | Team 內部的專案隔離 | Project Admin | ✅ 企業版 |
| **Virtual Key** | 認證和預算控制層 | 限定的模型、預算、速率限制 | Team Admin | ❌ 免費 |

---

## 建立與管理步驟

### Step 1：建立 Organization（可選）

```bash
curl -X POST http://localhost:4000/org/new \
  -H "Authorization: Bearer sk-master-key-change-this-please" \
  -H "Content-Type: application/json" \
  -d '{
    "org_name": "Acme Corporation",
    "org_id": "acme-corp"
  }'
```

為組織分配管理員：

```bash
curl -X POST http://localhost:4000/org/admin/new \
  -H "Authorization: Bearer sk-master-key-change-this-please" \
  -H "Content-Type: application/json" \
  -d '{
    "org_id": "acme-corp",
    "user_email": "admin@acme.com",
    "role": "org_admin"
  }'
```

### Step 2：建立 Team（部門）

每個部門是一個 Team，擁有獨立的預算和模型列表。

```bash
# 技術部
curl -X POST http://localhost:4000/team/new \
  -H "Authorization: Bearer sk-master-key-change-this-please" \
  -H "Content-Type: application/json" \
  -d '{
    "team_name": "Engineering",
    "team_id": "eng-team",
    "org_id": "acme-corp",
    "max_budget": 2000,
    "budget_duration": "30d",
    "models": ["gpt-4o", "gpt-4o-mini", "claude-sonnet-4", "llama3"],
    "metadata": {
      "department": "engineering",
      "cost_center": "ENG-001",
      "head_of_department": "cto@acme.com"
    }
  }'

# 行銷部
curl -X POST http://localhost:4000/team/new \
  -H "Authorization: Bearer sk-master-key-change-this-please" \
  -H "Content-Type: application/json" \
  -d '{
    "team_name": "Marketing",
    "team_id": "marketing-team",
    "max_budget": 500,
    "budget_duration": "30d",
    "models": ["gpt-4o-mini", "gemini-pro", "claude-haiku"],
    "metadata": {
      "department": "marketing",
      "cost_center": "MKT-001"
    }
  }'

# 客服部
curl -X POST http://localhost:4000/team/new \
  -H "Authorization: Bearer sk-master-key-change-this-please" \
  -H "Content-Type: application/json" \
  -d '{
    "team_name": "Support",
    "team_id": "support-team",
    "max_budget": 300,
    "budget_duration": "30d",
    "models": ["gpt-3.5-turbo", "claude-haiku", "llama3"],
    "metadata": {
      "department": "support",
      "cost_center": "SUP-001"
    }
  }'
```

### Step 3：為 Team 指派管理員和成員

```bash
# 指派 Team Admin（部門主管）
curl -X POST http://localhost:4000/team/admin/new \
  -H "Authorization: Bearer sk-master-key-change-this-please" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "eng-team",
    "user_email": "cto@acme.com",
    "role": "team_admin"
  }'

# 加入 Team 成員
curl -X POST http://localhost:4000/team/member/new \
  -H "Authorization: Bearer sk-master-key-change-this-please" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "eng-team",
    "user_email": "zhang.wei@acme.com",
    "role": "member"
  }'

curl -X POST http://localhost:4000/team/member/new \
  -H "Authorization: Bearer sk-master-key-change-this-please" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "eng-team",
    "user_email": "li.zhao@acme.com",
    "role": "member"
  }'
```

### Step 4：建立 Virtual Key（虛擬金鑰）

Virtual Key 是實際的認證憑證，綁定到特定 Team，控制模型使用和預算。

#### 4a：部門共用 Key

```bash
# 技術部共用 Key
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer sk-master-key-change-this-please" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "eng-team",
    "models": ["gpt-4o", "gpt-4o-mini", "claude-sonnet-4", "llama3"],
    "max_budget": 2000,
    "budget_duration": "30d",
    "duration": "30d",
    "user_email": "engineering@acme.com",
    "metadata": {
      "department": "engineering",
      "key_type": "department-shared"
    }
  }'

# 返回結果：
# {
#   "key": "sk-RV-l2BJEZ_LYNChSx2EueQ",
#   "key_type": "team_key",
#   "team_id": "eng-team"
# }
```

#### 4b：個人 Key（每個使用者獨立預算）

```bash
# 為張偉建立個人 Key
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer sk-master-key-change-this-please" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "eng-team",
    "user_email": "zhang.wei@acme.com",
    "models": ["gpt-4o", "gpt-4o-mini", "claude-sonnet-4"],
    "max_budget": 50,
    "budget_duration": "30d",
    "rpm_limit": 50,
    "tpm_limit": 200000,
    "duration": "30d",
    "metadata": {
      "name": "張偉",
      "role": "senior-developer",
      "employee_id": "ENG-0042"
    }
  }'

# 返回結果：
# {
#   "key": "sk-personal-key-zhang-abc123",
#   "key_type": "user_key",
#   "team_id": "eng-team",
#   "user_email": "zhang.wei@acme.com"
# }
```

---

## 預算控制機制

LiteLLM 的預算控制是**多層級疊加**的，請求路徑上的每一層都會獨立計算。

### 預算層級結構

```
請求路徑：使用者 → Virtual Key → Team → Organization
              ↓            ↓          ↓           ↓
           個人預算     Key 預算    Team 預算    Org 預算
              ↓            ↓          ↓           ↓
           獨立限額     獨立限額    獨立限額     獨立限額
```

**關鍵規則**：任何一層超預算，請求就會被拒絕。

### config.yaml 中的全域預算設定

```yaml
general_settings:
  # 整個 Proxy 的每月花費上限（設 0 表示不限制）
  max_budget: 10000.0
  budget_duration: "30d"

  # 全域 RPM/TPM 限制
  rpm_limit_global: 10000
  tpm_limit_global: 5000000

litellm_settings:
  # 每個模型的全域 RPM 限制
  model_rpm_limits:
    gpt-4o: 1000
    gpt-4o-mini: 5000
    claude-sonnet-4: 500
    llama3: 200
    gemini-pro: 2000
```

### Team 級預算（透過 API 設定）

```bash
# 更新 Team 預算
curl -X PATCH http://localhost:4000/team/update \
  -H "Authorization: Bearer sk-master-key-change-this-please" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "eng-team",
    "max_budget": 3000,          # 調高預算至 $3,000
    "budget_duration": "30d"
  }'
```

### Key 級預算（Virtual Key 中設定）

```json
{
  "team_id": "eng-team",
  "user_email": "zhang.wei@acme.com",
  "max_budget": 50,             // 個人月預算 $50
  "budget_duration": "30d",     // 每月重置
  "rpm_limit": 50,              // 每分鐘最多 50 次請求
  "tpm_limit": 200000           // 每分鐘最多 20 萬 tokens
}
```

### 預算使用查詢

```bash
# 查詢 Team 預算
curl http://localhost:4000/team/eng-team/budget \
  -H "Authorization: Bearer sk-master-key-change-this-please"

# 查詢 Key 預算
curl http://localhost:4000/key/info?key=sk-RV-l2BJEZ_LYNChSx2EueQ \
  -H "Authorization: Bearer sk-master-key-change-this-please"

# 查詢 Team 花費明細
curl http://localhost:4000/teammate/spend/ \
  -H "Authorization: Bearer sk-master-key-change-this-please" \
  -d '{
    "team_id": "eng-team",
    "start_time": "2026-07-01",
    "end_time": "2026-07-30"
  }'
```

### 預算警報設定

```yaml
general_settings:
  budget_alerts:
    enabled: true
    thresholds:
      - 50    # 50% 時通知
      - 75    # 75% 時通知
      - 90    # 90% 時通知
      - 100   # 100% 時暫停
    notification_webhook: "https://hooks.slack.com/your-webhook-url"
    notify_on_exceeded: true
    pause_on_exceeded: true
```

---

## 部門級模型路由

每個 Team 可以有不同的模型白名單，甚至可以指向不同的 API Key（例如不同 Azure OpenAI 實例）。

### model_list 配置

```yaml
model_list:
  # === OpenAI 模型 ===
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: ${OPENAI_API_KEY}
      max_tokens: 4096
      temperature: 0.7
    model_group: gpt-4o
    fallbacks:
      - gpt-4o-mini
      - claude-sonnet-4

  - model_name: gpt-4o-mini
    litellm_params:
      model: openai/gpt-4o-mini
      api_key: ${OPENAI_API_KEY}
    model_group: gpt-4o-mini

  - model_name: gpt-3.5-turbo
    litellm_params:
      model: openai/gpt-3.5-turbo
      api_key: ${OPENAI_API_KEY}
    model_group: gpt-3.5

  # === Anthropic 模型 ===
  - model_name: claude-sonnet-4
    litellm_params:
      model: anthropic/claude-sonnet-4
      api_key: ${ANTHROPIC_API_KEY}
    model_group: claude-sonnet

  - model_name: claude-haiku
    litellm_params:
      model: anthropic/claude-3-haiku-20240307
      api_key: ${ANTHROPIC_API_KEY}
    model_group: claude-haiku

  # === Google Gemini ===
  - model_name: gemini-pro
    litellm_params:
      model: gemini/gemini-pro
      api_key: ${GOOGLE_API_KEY}
    model_group: gemini-pro

  # === 本地 Ollama ===
  - model_name: llama3
    litellm_params:
      model: ollama/llama3
      api_base: http://ollama:11434
    model_group: llama3

  - model_name: qwen2.5
    litellm_params:
      model: ollama/qwen2.5:72b
      api_base: http://ollama:11434
    model_group: qwen2.5
```

### 各部門可用模型總覽

| 部門 | Team ID | 可用模型 | 預算 | RPM 限制 |
|------|---------|----------|------|----------|
| 技術部 | `eng-team` | gpt-4o, gpt-4o-mini, claude-sonnet-4, llama3 | $2,000/月 | 500 |
| 行銷部 | `marketing-team` | gpt-4o-mini, gemini-pro, claude-haiku | $500/月 | 200 |
| 客服部 | `support-team` | gpt-3.5-turbo, claude-haiku, llama3 | $300/月 | 100 |
| 管理層 | `mgmt-team` | gpt-4o, claude-sonnet-4, gemini-pro | $1,000/月 | 300 |

### 個人 Key 的模型控制

個人 Key 的 `models` 欄位可以比 Team 更少（縮小範圍）：

```json
// 技術部共用 Key — 可訪問所有 Team 模型
{
  "team_id": "eng-team",
  "models": ["gpt-4o", "gpt-4o-mini", "claude-sonnet-4", "llama3"]
}

// 實習生個人 Key — 只能使用基礎模型
{
  "team_id": "eng-team",
  "user_email": "intern@acme.com",
  "models": ["gpt-4o-mini", "llama3"],
  "max_budget": 10
}
```

---

## 速率限制

LiteLLM 支援多層級速率限制：

```yaml
litellm_settings:
  # === 全域限制 ===
  rpm_limit_global: 10000
  tpm_limit_global: 5000000

  # === 每個模型的全域 RPM ===
  model_rpm_limits:
    gpt-4o: 1000
    gpt-4o-mini: 5000
    claude-sonnet-4: 500
    llama3: 200

  # === Team 級 RPM/TPM ===
  team_rpm_limit: 500
  team_tpm_limit: 2000000

  # === Key 級 RPM/TPM ===
  key_rpm_limit: 100
  key_tpm_limit: 500000

  # === 最終使用者級 RPM/TPM ===
  user_rpm_limit: 30
  user_tpm_limit: 100000
```

各層級限制同時生效，取**最嚴格**的值。

---

## 企業版進階功能

以下功能需要 LiteLLM Enterprise License。

### 1. Organization 層級（最高隔離）

```bash
# 建立 Organization
curl -X POST http://localhost:4000/org/new \
  -H "Authorization: Bearer ***" \
  -d '{"org_name": "Acme Corp", "org_id": "acme-corp"}'

# 加入 Organization 的 Team
curl -X POST http://localhost:4000/team/new \
  -H "Authorization: Bearer ***" \
  -d '{
    "team_name": "Engineering",
    "team_id": "eng-team",
    "org_id": "acme-corp",
    "max_budget": 2000
  }'

# 每個 Org 有獨立的 Admin
curl -X POST http://localhost:4000/org/admin/new \
  -H "Authorization: Bearer ***" \
  -d '{
    "org_id": "acme-corp",
    "user_email": "org-admin@acme.com",
    "role": "org_admin"
  }'
```

### 2. Project 層級（Team 內子專案）

```bash
# 建立 Project
curl -X POST http://localhost:4000/project/new \
  -H "Authorization: Bearer ***" \
  -d '{
    "project_name": "Customer Portal v2",
    "project_id": "portal-v2",
    "team_id": "eng-team",
    "max_budget": 500
  }'

# Project Key（綁定 Team + Project）
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer ***" \
  -d '{
    "team_id": "eng-team",
    "project_id": "portal-v2",
    "models": ["gpt-4o"],
    "max_budget": 500,
    "duration": "30d"
  }'
```

### 3. JWT / SSO 認證

適合已部署 Okta、Azure AD 等 SSO 的企業：

```yaml
general_settings:
  enable_jwt_auth: true
  litellm_jwtauth:
    team_id_jwt_field: "department"      # JWT 中的部門欄位
    user_id_jwt_field: "sub"             # JWT 中的使用者 ID
    virtual_key_claim_field: "client_id"  # 用於查找 Virtual Key
    unregistered_jwt_client_behavior: "fallback_team_mapping"
    jwt_public_key_url: "https://your-idp/.well-known/jwks.json"
```

### 4. SCIM 自動同步

自動從企業 LDAP/Okta 同步用戶和群組：

```yaml
# 透過 Open WebUI 的 SCIM 整合
# 訪問 http://webui:8080/admin/settings → Authentication → SCIM
```

### 5. Custom Auth 自訂驗證

適合需要結合企業系統的場景：

```python
# custom_auth.py
from litellm.proxy.proxy_server import UserAPIKeyAuth

def custom_key_generate_fn(key, models, user_email, max_budget, duration):
    """自訂 key 生成邏輯"""
    # 從 LDAP 查詢用戶資訊
    user_info = ldap_lookup(user_email)

    # 根據 LDAP 群組設定預設權限
    if "engineering" in user_info.groups:
        return {
            "models": ["gpt-4o", "gpt-4o-mini", "claude-sonnet-4"],
            "max_budget": 100,
            "duration": "30d",
            "metadata": {"department": "engineering"}
        }
    elif "marketing" in user_info.groups:
        return {
            "models": ["gpt-4o-mini", "gemini-pro"],
            "max_budget": 25,
            "duration": "30d",
            "metadata": {"department": "marketing"}
        }
    else:
        return {
            "models": ["gpt-4o-mini"],
            "max_budget": 10,
            "duration": "30d"
        }
```

```yaml
# config.yaml
general_settings:
  custom_key_generate: custom_auth.custom_key_generate_fn
```

### 6. 按 Team 路由不同 API Key（Per-Team Credential Routing）

不同部門可以使用不同供應商的 API Key：

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: ${OPENAI_API_KEY}
    model_group: gpt-4o
    litellm_team_metadata:
      eng-team:
        api_key: ${ENG_OPENAI_KEY}      # 技術部用專屬 Key
      marketing-team:
        api_key: ${MKT_OPENAI_KEY}      # 行銷部用專屬 Key

  # 不同部門使用不同 Azure OpenAI 實例
  - model_name: azure-gpt4
    litellm_params:
      model: azure/gpt-4
      api_key: ${AZURE_EAST_KEY}
    model_group: azure-gpt4
    litellm_team_metadata:
      eng-team:
        api_key: ${AZURE_EAST_KEY}      # 技術部用東區實例
      support-team:
        api_key: ${AZURE_WEST_KEY}      # 客服部用西區實例（資料 residency）
```

---

## 管理儀表板

### Admin UI

訪問 `http://your-server:4000/ui` 可查看：

| 功能 | 說明 |
|------|------|
| **Usage Dashboard** | 總使用量、花費趨勢圖 |
| **Team Budgets** | 各部門預算使用情況（剩餘金額、使用百分比） |
| **Key Usage** | 每個 Virtual Key 的呼叫量和花費 |
| **Spend by Team** | 按部門統計花費排行 |
| **Spend by Model** | 按模型統計花費 |
| **User Activity** | 每個使用者的活動記錄 |
| **Rate Limits** | 當前速率限制狀態 |
| **Model Health** | 各模型的健康狀態和延遲 |

### 管理 API 總覽

```bash
# 查看所有 Teams
curl http://localhost:4000/team/list -H "Authorization: Bearer ***"

# 查看所有 Virtual Keys
curl http://localhost:4000/key/list -H "Authorization: Bearer ***"

# 查看所有 Users
curl http://localhost:4000/user/list -H "Authorization: Bearer ***"

# 查看所有 Organizations
curl http://localhost:4000/org/list -H "Authorization: Bearer ***"

# 刪除 Team
curl -X DELETE http://localhost:4000/team/delete \
  -H "Authorization: Bearer ***" \
  -d '{"team_id": "old-team-id"}'

# 刪除 Key
curl -X DELETE http://localhost:4000/key/delete \
  -H "Authorization: Bearer ***" \
  -d '{"key": "sk-deleted-key"}'
```

---

## 完整企業部署範例

### 200 人企業多租戶配置

```yaml
# config.yaml — 完整範例

general_settings:
  master_key: sk-enterprise-master-key-2026
  store_model_in_db: true
  enable_jwt_auth: false
  max_budget: 10000
  budget_duration: "30d"

  budget_alerts:
    enabled: true
    thresholds:
      - 50
      - 75
      - 90
      - 100
    notify_on_exceeded: true
    pause_on_exceeded: true

model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: ${OPENAI_API_KEY}
    fallbacks:
      - gpt-4o-mini
      - claude-sonnet-4

  - model_name: gpt-4o-mini
    litellm_params:
      model: openai/gpt-4o-mini
      api_key: ${OPENAI_API_KEY}

  - model_name: gpt-3.5-turbo
    litellm_params:
      model: openai/gpt-3.5-turbo
      api_key: ${OPENAI_API_KEY}

  - model_name: claude-sonnet-4
    litellm_params:
      model: anthropic/claude-sonnet-4
      api_key: ${ANTHROPIC_API_KEY}

  - model_name: claude-haiku
    litellm_params:
      model: anthropic/claude-3-haiku-20240307
      api_key: ${ANTHROPIC_API_KEY}

  - model_name: gemini-pro
    litellm_params:
      model: gemini/gemini-pro
      api_key: ${GOOGLE_API_KEY}

  - model_name: llama3
    litellm_params:
      model: ollama/llama3
      api_base: http://ollama:11434

router_settings:
  num_retries: 3
  retry_after: 5
  timeout: 120

litellm_settings:
  max_budget: 10000
  budget_duration: "30d"
  rpm_limit_global: 10000
  tpm_limit_global: 5000000
  model_rpm_limits:
    gpt-4o: 1000
    gpt-4o-mini: 5000
    claude-sonnet-4: 500
    llama3: 200
    gemini-pro: 2000
```

### 批量建立腳本

```bash
#!/bin/bash
# batch-setup-enterprise.sh

LITELLM_URL="http://localhost:4000"
MASTER_KEY="sk-enterprise-master-key-2026"

# === 建立各部門 ===

# 技術部
curl -s -X POST "$LITELLM_URL/team/new" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "team_name": "Engineering",
    "team_id": "eng-team",
    "max_budget": 2000,
    "budget_duration": "30d",
    "models": ["gpt-4o", "gpt-4o-mini", "claude-sonnet-4", "llama3"],
    "metadata": {"department": "engineering", "cost_center": "ENG-001"}
  }' && echo " ✓ Engineering"

# 行銷部
curl -s -X POST "$LITELLM_URL/team/new" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "team_name": "Marketing",
    "team_id": "marketing-team",
    "max_budget": 500,
    "budget_duration": "30d",
    "models": ["gpt-4o-mini", "gemini-pro", "claude-haiku"],
    "metadata": {"department": "marketing", "cost_center": "MKT-001"}
  }' && echo " ✓ Marketing"

# 客服部
curl -s -X POST "$LITELLM_URL/team/new" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "team_name": "Support",
    "team_id": "support-team",
    "max_budget": 300,
    "budget_duration": "30d",
    "models": ["gpt-3.5-turbo", "claude-haiku", "llama3"],
    "metadata": {"department": "support", "cost_center": "SUP-001"}
  }' && echo " ✓ Support"

# 管理層
curl -s -X POST "$LITELLM_URL/team/new" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "team_name": "Management",
    "team_id": "mgmt-team",
    "max_budget": 1000,
    "budget_duration": "30d",
    "models": ["gpt-4o", "claude-sonnet-4", "gemini-pro"],
    "metadata": {"department": "management", "cost_center": "MGT-001"}
  }' && echo " ✓ Management"

# 財務部
curl -s -X POST "$LITELLM_URL/team/new" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "team_name": "Finance",
    "team_id": "finance-team",
    "max_budget": 200,
    "budget_duration": "30d",
    "models": ["gpt-4o-mini", "claude-haiku"],
    "metadata": {"department": "finance", "cost_center": "FIN-001"}
  }' && echo " ✓ Finance"

echo ""
echo "All departments created successfully!"

# === 建立部門共用 Key ===

# 技術部 Key
ENG_KEY=$(curl -s -X POST "$LITELLM_URL/key/generate" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"team_id":"eng-team","models":["gpt-4o","gpt-4o-mini","claude-sonnet-4","llama3"],"max_budget":2000,"budget_duration":"30d","duration":"30d","user_email":"engineering@acme.com","metadata":{"key_type":"department-shared"}}' | grep -o '"key":"[^"]*"' | cut -d'"' -f4)
echo "Engineering Key: $ENG_KEY"

# 行銷部 Key
MKT_KEY=$(curl -s -X POST "$LITELLM_URL/key/generate" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"team_id":"marketing-team","models":["gpt-4o-mini","gemini-pro","claude-haiku"],"max_budget":500,"budget_duration":"30d","duration":"30d","user_email":"marketing@acme.com","metadata":{"key_type":"department-shared"}}' | grep -o '"key":"[^"]*"' | cut -d'"' -f4)
echo "Marketing Key: $MKT_KEY"

# 客服部 Key
SUP_KEY=$(curl -s -X POST "$LITELLM_URL/key/generate" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"team_id":"support-team","models":["gpt-3.5-turbo","claude-haiku","llama3"],"max_budget":300,"budget_duration":"30d","duration":"30d","user_email":"support@acme.com","metadata":{"key_type":"department-shared"}}' | grep -o '"key":"[^"]*"' | cut -d'"' -f4)
echo "Support Key: $SUP_KEY"

# 管理層 Key
MGT_KEY=$(curl -s -X POST "$LITELLM_URL/key/generate" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"team_id":"mgmt-team","models":["gpt-4o","claude-sonnet-4","gemini-pro"],"max_budget":1000,"budget_duration":"30d","duration":"30d","user_email":"management@acme.com","metadata":{"key_type":"department-shared"}}' | grep -o '"key":"[^"]*"' | cut -d'"' -f4)
echo "Management Key: $MGT_KEY"

# 財務部 Key
FIN_KEY=$(curl -s -X POST "$LITELLM_URL/key/generate" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"team_id":"finance-team","models":["gpt-4o-mini","claude-haiku"],"max_budget":200,"budget_duration":"30d","duration":"30d","user_email":"finance@acme.com","metadata":{"key_type":"department-shared"}}' | grep -o '"key":"[^"]*"' | cut -d'"' -f4)
echo "Finance Key: $FIN_KEY"

echo ""
echo "All department keys created!"
```

---

## 月度成本預估（200 人企業）

| 部門 | 人數 | 每人月預算 | 部門月預算 | 模型 |
|------|------|-----------|-----------|------|
| 技術部 | 50 | $50 | $2,500 | GPT-4o, Claude Sonnet, 本地模型 |
| 行銷部 | 30 | $25 | $750 | Gemini Pro, GPT-4o-mini |
| 客服部 | 40 | $10 | $400 | GPT-3.5-turbo, 本地模型 |
| 管理層 | 10 | $150 | $1,500 | GPT-4o, Claude Sonnet, Gemini |
| 財務部 | 10 | $30 | $300 | GPT-4o-mini, Claude Haiku |
| **合計** | **140** | - | **$5,450** | - |

> 💡 使用本地 Ollama 模型可大幅降低基礎成本，適合客服部和內部工具。

---

## 快速啟動檢查清單

```bash
# ✅ 多租戶部署前檢查

# 1. 確認所有 API Keys 已設定
cat .env | grep -E "API_KEY"

# 2. 啟動服務
docker compose up -d

# 3. 確認服務正常
docker compose ps

# 4. 測試 LiteLLM 健康狀態
curl -s http://localhost:4000/health

# 5. 確認 Open WebUI 可訪問
curl -s http://localhost:8080/api/info

# 6. 執行批量建立腳本
bash batch-setup-enterprise.sh

# 7. 在 LiteLLM Admin UI 確認部門和 Keys
# 訪問 http://localhost:4000/ui

# 8. 在 Open WebUI 中建立用戶群組
# 訪問 http://localhost:8080/admin

# 9. 測試部門模型隔離
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer $ENG_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4o", "messages": [{"role": "user", "content": "test"}]}'

# 10. 測試預算限制（行銷部嘗試訪問 gpt-4o 應該被拒絕）
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer $MKT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4o", "messages": [{"role": "user", "content": "test"}]}'
# 預期：403 Forbidden（行銷部沒有 gpt-4o 權限）
```

---

## 常見問題

**Q: 預算用完了會怎樣？**
A: LiteLLM 會在預算用完時自動拒絕請求，返回 `ExceededBudget` 錯誤。管理員可以透過 Admin UI 調高預算。

**Q: 如何讓不同部門使用不同的 API Key？**
A: 在 `model_list` 中配置 `litellm_team_metadata`，為不同 Team 指定不同的 `api_key`。

**Q: 如何整合企業 LDAP/SSO？**
A: 使用 `custom_auth`（自訂驗證）或 `enable_jwt_auth`（JWT 認證）功能。

**Q: 如何限制使用者只能使用特定模型？**
A: 在 Virtual Key 的 `models` 欄位設定白名單，或使用 Open WebUI 的 RBAC 群組控制。

**Q: Team 之間可以互相看到對方的資料嗎？**
A: 不可以。每個 Team 的預算、模型列表、key 都是完全隔離的。

**Q: 本地模型和雲端模型可以混合使用嗎？**
A: 可以。在 `model_list` 中同時配置兩種類型，透過 Team 的模型白名單控制。

---

**最後更新**: 2026-07-30  
**作者**: Hermes Agent 整理  
**原始專案**: [LiteLLM](https://github.com/BerriAI/litellm)
