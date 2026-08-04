---
title: "Open WebUI + LiteLLM 企業級部署指南：部門權限與模型路由完整實作"
date: 2026-08-03
description: 手把手教學如何使用 Open WebUI 搭配 LiteLLM Proxy 搭建企業 AI 平台，實現按部門區分模型權限、預算控制和 RBAC 管理
tags: [openwebui, litellm, enterprise, ai-gateway, docker, rbac, multi-tenant]
---

# Open WebUI + LiteLLM 企業級部署指南：部門權限與模型路由完整實作

本指南將完整說明如何在企業環境中部署 **Open WebUI** 搭配 **LiteLLM Proxy**，打造一個集中管理、按部門隔離模型權限、控制預算的企業級 AI 平台。

![Architecture](https://docs.litellm.ai/docs/imgs/litellm-proxy-arch.png)

## 架構總覽

```
┌─────────────────────────────────────────────────────────┐
│                    企業員工瀏覽器                          │
│                  http://webui.company.com:8080           │
└────────────────────┬────────────────────────────────────┘
                     │ OpenAI 相容 API (v1/chat/completions)
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Open WebUI (Docker)                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  前端 UI     │  │  RBAC 權限管理 │  │  對話/記憶管理  │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │ http://litellm:4000/v1
                     ▼
┌─────────────────────────────────────────────────────────┐
│              LiteLLM Proxy (Docker)                      │
│  ┌─────────────────────────────────────────────────┐    │
│  │  ① 請求路由：根據 Team / Virtual Key 路由模型     │    │
│  │  ② 預算控制：Team Budget / Key Budget / User Budget│    │
│  │  ③ 速率限制：TPM / RPM / 並行請求限制              │    │
│  │  ④ 成本追蹤：按部門/用戶/模型統計花費              │    │
│  │  ⑤ 負載均衡：自動 Failover / 模型自動切換          │    │
│  └─────────────────────────────────────────────────┘    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ PostgreSQL│  │  Redis    │  │  Admin UI│              │
│  │ (用戶/預算)│  │(快取/限流) │  │ (管理介面)│              │
│  └──────────┘  └──────────┘  └──────────┘              │
└──────┬───────────┬───────────┬───────────┬──────────────┘
       │           │           │           │
       ▼           ▼           ▼           ▼
  ┌────────┐ ┌──────────┐ ┌────────┐ ┌──────────┐
  │OpenAI  │ │ Anthropic │ │Gemini  │ │ 本地 Ollama│
  │  API   │ │   API     │ │  API   │ │  Server  │
  └────────┘ └──────────┘ └────────┘ └──────────┘
```

### 核心概念

| 層級 | 說明 | 對應場景 |
|------|------|----------|
| **Organization** | 最高隔離層級，企業可有多個 Org | 跨公司合作、不同法人實體 |
| **Team** | 部門/團隊層級，擁有獨立預算和模型列表 | 技術部、行銷部、客服部 |
| **Project** | Team 下的子專案（企業版功能） | 某部門下的特定專案 |
| **Virtual Key** | 虛擬 API Key，綁定 Team 和使用權限 | 部門共用 key 或個人 key |
| **User** | 最終使用者，可綁定到 Team | 部門員工 |

---

## 第一階段：環境準備

### 所需元件

| 元件 | 版本 | 用途 |
|------|------|------|
| Docker + Docker Compose | 2.0+ | 容器化部署 |
| Open WebUI | latest | 前端 UI |
| LiteLLM Proxy | latest | LLM 路由中繼層 |
| PostgreSQL | 15+ | 用戶資料、預算、key 管理 |
| Redis | 7+ | 快取、速率限制、預算同步 |
| Nginx (可選) | latest | 反向代理、TLS 終端 |

### 硬體建議

| 規模 | CPU | RAM | 儲存 |
|------|-----|-----|------|
| 小型 (50 人) | 4 核心 | 8 GB | 50 GB |
| 中型 (200 人) | 8 核心 | 16 GB | 100 GB |
| 大型 (1000+ 人) | 16 核心 | 32 GB+ | 200 GB+ |

---

## 第二階段：Docker Compose 部署

### 2.1 目錄結構

```
enterprise-ai/
├── docker-compose.yml          # 主部署檔
├── litellm/
│   └── config.yaml             # LiteLLM 主配置
├── nginx/
│   └── nginx.conf              # 反向代理配置
└── .env                        # 環境變數（API Keys）
```

### 2.2 環境變數檔 (.env)

```bash
# ============ PostgreSQL ============
POSTGRES_USER=litellm_user
POSTGRES_PASSWORD=your_strong_password_here
POSTGRES_DB=litellm_db
POSTGRES_PORT=5432

# ============ Redis ============
REDIS_PASSWORD=your_redis_password_here
REDIS_PORT=6379

# ============ LiteLLM ============
LITELLM_MASTER_KEY=sk-master-key-change-this-please
UI_USERNAME=admin
UI_PASSWORD=admin_password_here

# ============ LLM Provider API Keys ============
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GOOGLE_API_KEY=your-google-key
MISTRAL_API_KEY=your-mistral-key

# ============ 本地 Ollama（可選） ============
OLLAMA_BASE_URL=http://ollama:11434

# ============ 網域設定（生產環境） ============
DOMAIN=ai.company.com
```

### 2.3 主 docker-compose.yml

```yaml
version: '3.8'

services:
  # ============ PostgreSQL ============
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - ai-network

  # ============ Redis ============
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    networks:
      - ai-network

  # ============ LiteLLM Proxy ============
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    restart: unless-stopped
    command:
      - "--config"
      - "/app/config.yaml"
      - "--port"
      - "4000"
      - "--num_workers"
      - "8"
      - "--detailed_debug"
    ports:
      - "4000:4000"
    environment:
      - LITELLM_MASTER_KEY=${LITELLM_MASTER_KEY}
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      - STORE_MODEL_IN_DB=true
      - UI_USERNAME=${UI_USERNAME}
      - UI_PASSWORD=${UI_PASSWORD}
      - REDIS_HOST=redis
      - REDIS_PASSWORD=${REDIS_PASSWORD}
      - REDIS_PORT=6379
      - ENABLE_LITELLM_DB=true
      - PROXY_SQLITE_DB=/app/proxy.db  # 本地備用
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - MISTRAL_API_KEY=${MISTRAL_API_KEY}
    volumes:
      - ./litellm/config.yaml:/app/config.yaml
    depends_on:
      - db
      - redis
    networks:
      - ai-network

  # ============ Open WebUI ============
  webui:
    image: ghcr.io/open-webui/open-webui:main
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - OPENAI_API_KEY=dummy-key  # 透過 LiteLLM 代理，不需要真正的 key
      - OPENAI_API_BASE_URL=http://litellm:4000/v1
      - ENABLE_OLLAMA_API=false
      - AUTH_TYPE_BYPASS_FOR_SIGNUP=false
      - ENABLE_SIGNUP=true
      - ENABLE_API_KEY=true
    volumes:
      - webui_data:/app/backend/data
    depends_on:
      - litellm
    networks:
      - ai-network

  # ============ Nginx 反向代理（可選，生產環境建議） ============
  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - webui
      - litellm
    networks:
      - ai-network

volumes:
  pgdata:
  redis_data:
  webui_data:

networks:
  ai-network:
    driver: bridge
```

### 2.4 Nginx 配置

```nginx
upstream webui_backend {
    server webui:8080;
}

upstream litellm_backend {
    server litellm:4000;
}

server {
    listen 80;
    server_name ai.company.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ai.company.com;

    ssl_certificate     /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # Open WebUI
    location / {
        proxy_pass http://webui_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # LiteLLM Admin UI
    location /litellm/ {
        proxy_pass http://litellm_backend/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 第三階段：LiteLLM 核心配置 — 部門模型路由

### 3.1 基本 config.yaml

```yaml
# ============ 一般設定 ============
general_settings:
  master_key: sk-master-key-change-this-please
  database_url: postgresql://litellm_user:password@db:5432/litellm_db
  store_model_in_db: true
  master_key: sk-enterprise-master-key-2026

  # 全域預算上限（整個 proxy 每月花費上限，設 0 表示不限制）
  max_budget: 5000.0
  budget_duration: "30d"

  # JWT 認證（可選，適合有企業 SSO 的環境）
  # enable_jwt_auth: true
  # litellm_jwtauth:
  #   team_id_jwt_field: "department"
  #   user_id_jwt_field: "sub"

# ============ 模型列表 ============
model_list:

  # === OpenAI 模型 ===
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: ${OPENAI_API_KEY}
      max_tokens: 4096
      temperature: 0.7

  - model_name: gpt-4o-mini
    litellm_params:
      model: openai/gpt-4o-mini
      api_key: ${OPENAI_API_KEY}

  - model_name: gpt-3.5-turbo
    litellm_params:
      model: openai/gpt-3.5-turbo
      api_key: ${OPENAI_API_KEY}

  # === Anthropic 模型 ===
  - model_name: claude-sonnet-4
    litellm_params:
      model: anthropic/claude-sonnet-4
      api_key: ${ANTHROPIC_API_KEY}

  - model_name: claude-haiku
    litellm_params:
      model: anthropic/claude-3-haiku-20240307
      api_key: ${ANTHROPIC_API_KEY}

  # === Google Gemini ===
  - model_name: gemini-pro
    litellm_params:
      model: gemini/gemini-pro
      api_key: ${GOOGLE_API_KEY}

  # === 本地 Ollama 模型（免費、資料不出企業） ===
  - model_name: llama3
    litellm_params:
      model: ollama/llama3
      api_base: http://ollama:11434

  - model_name: qwen2.5
    litellm_params:
      model: ollama/qwen2.5:72b
      api_base: http://ollama:11434

  # === Mistral ===
  - model_name: mistral-large
    litellm_params:
      model: mistral/mistral-large-latest
      api_key: ${MISTRAL_API_KEY}

# ============ 路由策略 ============
router_settings:
  num_retries: 3
  retry_after: 5
  timeout: 120
  fallbacks:
    - gpt-4o: [gpt-4o-mini, claude-sonnet-4]
    - claude-sonnet-4: [claude-haiku, gpt-4o-mini]

# ============ 速率限制 ============
litellm_settings:
  max_budget: 5000
  budget_duration: "30d"
  set_verbose: True
  drop_params: True
  success_callback: ["langfuse"]
  failure_callback: ["langfuse"]

  # 全域 RPM/TPM 限制
  rpm_limit_global: 10000
  tpm_limit_global: 5000000

  # 每個模型的全域限制
  model_rpm_limits:
    gpt-4o: 1000
    gpt-4o-mini: 5000
    claude-sonnet-4: 500
    llama3: 200
    gemini-pro: 2000
```

---

## 第四階段：部門隔離與權限管理

這是整個架構的**核心**——按部門區分模型權限和預算。

### 4.1 透過 Admin UI 建立部門 (Teams)

訪問 LiteLLM Admin UI：`http://your-server:4000/ui`

#### 步驟 1：建立部門

```
Admin UI → Teams → Create Team
```

#### 步驟 2：為每個部門設定模型白名單和預算

| 部門 | Team ID | 可用模型 | 月預算 | RPM 限制 |
|------|---------|----------|--------|----------|
| 技術部 (Engineering) | `eng-team` | gpt-4o, gpt-4o-mini, claude-sonnet-4, llama3 | $2,000 | 500 |
| 行銷部 (Marketing) | `marketing-team` | gpt-4o-mini, gemini-pro, claude-haiku | $500 | 200 |
| 客服部 (Support) | `support-team` | gpt-3.5-turbo, claude-haiku, llama3 | $300 | 100 |
| 管理層 (Management) | `mgmt-team` | gpt-4o, claude-sonnet-4, gemini-pro | $1,000 | 300 |
| 財務部 (Finance) | `finance-team` | gpt-4o-mini, claude-haiku | $200 | 100 |

#### 步驟 3：建立 Virtual Key 綁定部門

每個部門至少有一個 Virtual Key，Open WebUI 用戶通過這個 key 來使用模型。

```bash
# 透過 LiteLLM API 建立部門 Virtual Key
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer sk-master-key-change-this-please" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "",
    "team_id": "eng-team",
    "models": ["gpt-4o", "gpt-4o-mini", "claude-sonnet-4", "llama3"],
    "max_budget": 2000,
    "budget_duration": "30d",
    "duration": "30d",
    "user_email": "eng-dept@company.com",
    "metadata": {
      "department": "engineering",
      "cost_center": "ENG-001"
    }
  }'
```

### 4.2 config.yaml 中的部門級路由配置

除了透過 UI 管理外，也可以在 `config.yaml` 中預設部門路由規則：

```yaml
# ============ 部門級模型路由 ============
# 每個 team 可以有不同的模型列表和 API Key
model_group_mapping:
  eng-team:
    models:
      - gpt-4o
      - gpt-4o-mini
      - claude-sonnet-4
      - llama3
    team_id: eng-team
    metadata:
      department: engineering
      cost_center: ENG-001
      priority: 1

  marketing-team:
    models:
      - gpt-4o-mini
      - gemini-pro
      - claude-haiku
    team_id: marketing-team
    metadata:
      department: marketing
      cost_center: MKT-001
      priority: 2

  support-team:
    models:
      - gpt-3.5-turbo
      - claude-haiku
      - llama3
    team_id: support-team
    metadata:
      department: support
      cost_center: SUP-001
      priority: 3

  mgmt-team:
    models:
      - gpt-4o
      - claude-sonnet-4
      - gemini-pro
    team_id: mgmt-team
    metadata:
      department: management
      cost_center: MGT-001
      priority: 1

# ============ 預算分配 ============
budget_allocation:
  eng-team:
    max_budget: 2000
    budget_duration: "30d"
    rpm_limit: 500
    tpm_limit: 2000000

  marketing-team:
    max_budget: 500
    budget_duration: "30d"
    rpm_limit: 200
    tpm_limit: 800000

  support-team:
    max_budget: 300
    budget_duration: "30d"
    rpm_limit: 100
    tpm_limit: 500000

  mgmt-team:
    max_budget: 1000
    budget_duration: "30d"
    rpm_limit: 300
    tpm_limit: 1500000

  finance-team:
    max_budget: 200
    budget_duration: "30d"
    rpm_limit: 100
    tpm_limit: 400000
```

### 4.3 透過 Virtual Key 實現使用者級控制

除了部門級別外，還可以為個人使用者建立 Virtual Key：

```python
# 為技術部員工建立個人 key
virtual_key_config = {
    "key": "sk-personal-key-abc123",
    "team_id": "eng-team",          # 繼承部門的預算
    "user_id": "zhang.wei@company.com",
    "models": ["gpt-4o", "gpt-4o-mini", "claude-sonnet-4"],  # 繼承部門模型列表
    "max_budget": 50,               # 個人月預算 $50
    "budget_duration": "30d",
    "duration": "30d",
    "rpm_limit": 50,                # 個人 RPM
    "tpm_limit": 200000,            # 個人 TPM
    "metadata": {
        "name": "張偉",
        "department": "engineering",
        "role": "senior-developer",
        "cost_center": "ENG-001"
    }
}
```

### 4.4 模型優先級與 Failover

LiteLLM 支援按優先級路由模型，當主模型不可用時自動切換：

```yaml
model_list:
  # 技術部：優先使用 GPT-4o，失敗則用 Claude Sonnet
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: ${OPENAI_API_KEY}
    model_info:
      id: gpt-4o
      pricing: {"input": 0.0025, "output": 0.01}
    model_group: gpt-4o
    fallbacks:
      - claude-sonnet-4
      - gpt-4o-mini

  # 行銷部：優先使用 Gemini（成本效益最高）
  - model_name: gemini-pro
    litellm_params:
      model: gemini/gemini-pro
      api_key: ${GOOGLE_API_KEY}
    model_group: gemini-pro
    fallbacks:
      - gpt-4o-mini
      - claude-haiku
```

---

## 第五階段：Open WebUI RBAC 權限管理

Open WebUI 有自己的 RBAC（Role-Based Access Control）系統，與 LiteLLM 的部門體系配合使用。

### 5.1 RBAC 權限層級

| 角色 | 權限 | 適用對象 |
|------|------|----------|
| **Admin** | 完全管理權限，可管理用戶、模型、設定 | IT 管理員 |
| **User** | 基本使用權限，可建立對話、使用已授權模型 | 一般員工 |
| **Pending** | 等待管理員審核，無使用權限 | 新申請者 |
| **Power User** | 額外權限（建立群組、管理知識庫） | 部門主管 |

### 5.2 Open WebUI 權限清單

#### 模型相關權限

| 權限 | 說明 |
|------|------|
| `models:create` | 建立自訂模型 |
| `models:delete` | 刪除模型 |
| `models:edit` | 編輯模型設定 |
| `models:read` | 查看所有模型 |
| `models:use` | 使用模型 |

#### 對話相關權限

| 權限 | 說明 |
|------|------|
| `conversations:create` | 建立新對話 |
| `conversations:delete` | 刪除對話 |
| `conversations:export` | 匯出對話 |
| `conversations:share` | 分享對話 |

#### 管理相關權限

| 權限 | 說明 |
|------|------|
| `admin:access` | 管理後台 |
| `admin:users` | 管理用戶 |
| `admin:groups` | 管理群組 |
| `admin:settings` | 修改設定 |
| `admin:audit` | 查看審計日誌 |

### 5.3 群組 (Group) 配置

Open WebUI 支援兩種群組類型：

```
Permission Groups（權限群組）:
  └── [Perms] Engineering       → 技術部：可使用所有模型
  └── [Perms] Marketing         → 行銷部：可使用部分模型
  └── [Perms] Support           → 客服部：基礎模型權限
  └── [Perms] Management        → 管理層：完整模型權限

Sharing Groups（分享群組）:
  └── [Share] Engineering-Shared → 技術部知識庫共享
  └── [Share] Company-Wide       → 全公司共享
```

### 5.4 配置步驟

1. 訪問 Open WebUI Admin Panel：`http://your-server:8080/admin`
2. 進入 **Users → Groups**
3. 建立與部門對應的群組
4. 為每個群組設定模型使用權限

```
Admin Panel → Users → Groups → Create Group

Group Name: Engineering
Group Type: Permission Group
Models Allowed: gpt-4o, gpt-4o-mini, claude-sonnet-4, llama3
Permission Overrides:
  - models:read: true
  - models:use: true
  - models:create: false
  - conversations:share: true
```

---

## 第六階段：完整部門管理範例

### 6.1 企業部門架構

```
Company AI Platform
│
├── Engineering Department (技術部)
│   ├── Team ID: eng-team
│   ├── Budget: $2,000/月
│   ├── Models: gpt-4o, gpt-4o-mini, claude-sonnet-4, llama3
│   ├── Members: 30 人
│   ├── Per-user Budget: $50/月
│   ├── RPM Limit: 50/user
│   └── Priority: 高（可訪問昂貴模型）
│
├── Marketing Department (行銷部)
│   ├── Team ID: marketing-team
│   ├── Budget: $500/月
│   ├── Models: gpt-4o-mini, gemini-pro, claude-haiku
│   ├── Members: 15 人
│   ├── Per-user Budget: $25/月
│   ├── RPM Limit: 20/user
│   └── Priority: 中（成本效益優先）
│
├── Support Department (客服部)
│   ├── Team ID: support-team
│   ├── Budget: $300/月
│   ├── Models: gpt-3.5-turbo, claude-haiku, llama3
│   ├── Members: 20 人
│   ├── Per-user Budget: $10/月
│   ├── RPM Limit: 10/user
│   └── Priority: 低（基礎模型即可）
│
├── Management (管理層)
│   ├── Team ID: mgmt-team
│   ├── Budget: $1,000/月
│   ├── Models: gpt-4o, claude-sonnet-4, gemini-pro
│   ├── Members: 5 人
│   ├── Per-user Budget: $150/月
│   ├── RPM Limit: 50/user
│   └── Priority: 高（需要最好的模型）
│
└── Finance Department (財務部)
    ├── Team ID: finance-team
    ├── Budget: $200/月
    ├── Models: gpt-4o-mini, claude-haiku
    ├── Members: 5 人
    ├── Per-user Budget: $30/月
    ├── RPM Limit: 10/user
    └── Priority: 中（需要準確性，不需要最新模型）
```

### 6.2 透過 API 批量建立部門

```bash
#!/bin/bash
# batch-create-teams.sh - 批量建立部門

LITELLM_URL="http://localhost:4000"
MASTER_KEY="sk-enterprise-master-key-2026"

# 技術部
curl -X POST "$LITELLM_URL/team/new" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "team_name": "Engineering",
    "team_id": "eng-team",
    "max_budget": 2000,
    "budget_duration": "30d",
    "models": ["gpt-4o", "gpt-4o-mini", "claude-sonnet-4", "llama3"],
    "metadata": {
      "department": "engineering",
      "cost_center": "ENG-001",
      "head_of_department": "cto@company.com"
    }
  }'

# 行銷部
curl -X POST "$LITELLM_URL/team/new" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "team_name": "Marketing",
    "team_id": "marketing-team",
    "max_budget": 500,
    "budget_duration": "30d",
    "models": ["gpt-4o-mini", "gemini-pro", "claude-haiku"],
    "metadata": {
      "department": "marketing",
      "cost_center": "MKT-001",
      "head_of_department": "cmo@company.com"
    }
  }'

# 客服部
curl -X POST "$LITELLM_URL/team/new" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "team_name": "Support",
    "team_id": "support-team",
    "max_budget": 300,
    "budget_duration": "30d",
    "models": ["gpt-3.5-turbo", "claude-haiku", "llama3"],
    "metadata": {
      "department": "support",
      "cost_center": "SUP-001",
      "head_of_department": "cs-manager@company.com"
    }
  }'

# 管理層
curl -X POST "$LITELLM_URL/team/new" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "team_name": "Management",
    "team_id": "mgmt-team",
    "max_budget": 1000,
    "budget_duration": "30d",
    "models": ["gpt-4o", "claude-sonnet-4", "gemini-pro"],
    "metadata": {
      "department": "management",
      "cost_center": "MGT-001",
      "head_of_department": "ceo@company.com"
    }
  }'

# 財務部
curl -X POST "$LITELLM_URL/team/new" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "team_name": "Finance",
    "team_id": "finance-team",
    "max_budget": 200,
    "budget_duration": "30d",
    "models": ["gpt-4o-mini", "claude-haiku"],
    "metadata": {
      "department": "finance",
      "cost_center": "FIN-001",
      "head_of_department": "cfo@company.com"
    }
  }'

echo "All teams created successfully!"
```

### 6.3 建立部門 Virtual Keys

```bash
#!/bin/bash
# create-department-keys.sh - 為每個部門建立 Virtual Key

LITELLM_URL="http://localhost:4000"
MASTER_KEY="sk-enterprise-master-key-2026"

# 技術部 Key（部門共用）
curl -X POST "$LITELLM_URL/key/generate" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "eng-team",
    "models": ["gpt-4o", "gpt-4o-mini", "claude-sonnet-4", "llama3"],
    "max_budget": 2000,
    "budget_duration": "30d",
    "duration": "30d",
    "user_email": "engineering@company.com",
    "metadata": {
      "department": "engineering",
      "key_type": "department-shared"
    }
  }'

# 行銷部 Key
curl -X POST "$LITELLM_URL/key/generate" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "marketing-team",
    "models": ["gpt-4o-mini", "gemini-pro", "claude-haiku"],
    "max_budget": 500,
    "budget_duration": "30d",
    "duration": "30d",
    "user_email": "marketing@company.com",
    "metadata": {
      "department": "marketing",
      "key_type": "department-shared"
    }
  }'

# ... 類似方式建立其他部門 key
```

### 6.4 個人使用者 Key 建立

```bash
# 為張偉（技術部工程師）建立個人 key
curl -X POST "$LITELLM_URL/key/generate" \
  -H "Authorization: Bearer $MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "eng-team",
    "user_email": "zhang.wei@company.com",
    "models": ["gpt-4o", "gpt-4o-mini", "claude-sonnet-4"],
    "max_budget": 50,
    "budget_duration": "30d",
    "duration": "30d",
    "rpm_limit": 50,
    "tpm_limit": 200000,
    "metadata": {
      "name": "張偉",
      "department": "engineering",
      "role": "senior-developer",
      "employee_id": "ENG-0042"
    }
  }'
```

---

## 第七階段：Open WebUI 配置與部門綁定

### 7.1 Open WebUI 環境變數

```yaml
# docker-compose.yml 中 webui 服務的 environment
environment:
  - OPENAI_API_KEY=dummy-key
  - OPENAI_API_BASE_URL=http://litellm:4000/v1

  # RBAC 相關設定
  - AUTH_TYPE_BYPASS_FOR_SIGNUP=false
  - ENABLE_SIGNUP=true
  - ENABLE_API_KEY=true

  # 模型預設值
  - DEFAULT_MODEL=gpt-4o-mini

  # 安全設定
  - ENABLE_MODEL_PROXY=true
  - ENABLE_ADMIN_EXPORT=true
```

### 7.2 Open WebUI 管理面板配置

1. 訪問 `http://your-server:8080/admin`
2. **Settings → Models**：確認模型列表正確（應顯示 LiteLLM 中配置的所有模型）
3. **Settings → Authentication**：啟用 RBAC
4. **Users → Groups**：建立與部門對應的群組

### 7.3 用戶群組與部門對應表

| Open WebUI Group | 對應 LiteLLM Team | 可用模型 | 權限 |
|-----------------|-------------------|----------|------|
| `[Perms] Engineering` | `eng-team` | gpt-4o, gpt-4o-mini, claude-sonnet-4, llama3 | 完整使用權 |
| `[Perms] Marketing` | `marketing-team` | gpt-4o-mini, gemini-pro, claude-haiku | 標準使用權 |
| `[Perms] Support` | `support-team` | gpt-3.5-turbo, claude-haiku, llama3 | 基礎使用權 |
| `[Perms] Management` | `mgmt-team` | gpt-4o, claude-sonnet-4, gemini-pro | 完整使用權 |
| `[Perms] Finance` | `finance-team` | gpt-4o-mini, claude-haiku | 標準使用權 |

---

## 第八階段：監控與成本追蹤

### 8.1 LiteLLM 管理儀表板

訪問 `http://your-server:4000/ui` 可查看：

- **Usage Dashboard**：總使用量、花費趨勢
- **Team Budgets**：各部門預算使用情況
- **Key Usage**：各 Virtual Key 的使用量
- **Model Performance**：各模型的回應時間、成功率
- **Spend by Department**：按部門統計花費

### 8.2 預算監控 API

```bash
# 查詢各部門預算使用情况
curl -X GET "http://localhost:4000/team/eng-team/budget" \
  -H "Authorization: Bearer sk-master-key-change-this-please"

# 返回：
# {
#   "team_id": "eng-team",
#   "current_spend": 1250.50,
#   "max_budget": 2000,
#   "budget_duration": "30d",
#   "remaining": 749.50,
#   "usage_percentage": 62.5
# }

# 查詢個人使用者預算
curl -X GET "http://localhost:4000/key/zhang.wei@company.com/budget" \
  -H "Authorization: Bearer sk-master-key-change-this-please"
```

### 8.3 設定預算警報

```yaml
# 在 config.yaml 中設定預算警報通知
general_settings:
  budget_alerts:
    enabled: true
    thresholds:
      - 50   # 50% 時通知
      - 75   # 75% 時通知
      - 90   # 90% 時通知
      - 100  # 100% 時暫停
    notification_webhook: "https://hooks.slack.com/your-webhook-url"
    notify_on_exceeded: true
    pause_on_exceeded: true
```

### 8.4 透過 Langfuse 進行進階分析（可選）

```yaml
litellm_settings:
  success_callback: ["langfuse"]
  failure_callback: ["langfuse"]

# 需要額外部署 Langfuse
# docker-compose add:
# langfuse:
#   image: ghcr.io/langfuse/langfuse:latest
#   ports:
#     - "3000:3000"
```

---

## 第九階段：生產環境最佳實踐

### 9.1 安全建議

| 項目 | 建議 |
|------|------|
| **Master Key** | 使用 32+ 字元隨機字串，定期更換 |
| **API Keys** | 使用 .env 檔管理，不要硬編碼在 config.yaml |
| **網路隔離** | LiteLLM 和 PostgreSQL 不應暴露到公网，只通過 Nginx 訪問 |
| **TLS/SSL** | 生產環境必須啟用 HTTPS |
| **RBAC** | 啟用 Open WebUI 的 RBAC，不要允許所有人註冊 |
| **Audit Log** | 啟用審計日誌，追蹤所有 API 呼叫 |

### 9.2 效能優化

| 項目 | 建議 |
|------|------|
| **Redis** | 必裝，用於快取和速率限制 |
| **PostgreSQL** | 必裝，用於持久化用戶和預算資料 |
| **Num Workers** | 根據 CPU 核心數調整（建議核心數 × 2） |
| **Connection Pooling** | 使用 PgBouncer 管理 PostgreSQL 連線 |
| **CDN** | 為靜態資源使用 CDN |
| **Load Balancer** | 多用戶場景使用 Nginx 或 HAProxy |

### 9.3 備份策略

```bash
# PostgreSQL 備份腳本
#!/bin/bash
BACKUP_DIR="/backups/litellm"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 備份 PostgreSQL
pg_dump -h db -U litellm_user litellm_db > $BACKUP_DIR/litellm_db_$DATE.sql

# 備份 LiteLLM config
cp /app/config.yaml $BACKUP_DIR/config_$DATE.yaml

# 清理 30 天前的備份
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "config_*.yaml" -mtime +30 -delete
```

### 9.4 日誌管理

```bash
# Docker Compose 日誌配置
# 在每個 service 中加入：
logging:
  driver: "json-file"
  options:
    max-size: "50m"
    max-file: "3"
```

---

## 第十階段：進階功能

### 10.1 自訂驗證（Custom Auth）

適合需要結合企業 SSO 或 LDAP 的場景：

```python
# custom_auth.py
from litellm.proxy.proxy_server import UserAPIKeyAuth

def custom_key_generate_fn(key, models, user_email, max_budget, duration):
    """自訂 key 生成邏輯"""
    # 從 LDAP 查詢用戶資訊
    user_info = ldap_lookup(user_email)

    # 根據 LDAP 群組設定預設權限
    if "engineering" in user_info.groups:
        default_models = ["gpt-4o", "gpt-4o-mini", "claude-sonnet-4"]
        default_budget = 100
    elif "marketing" in user_info.groups:
        default_models = ["gpt-4o-mini", "gemini-pro"]
        default_budget = 25
    else:
        default_models = ["gpt-4o-mini"]
        default_budget = 10

    return {
        "models": models or default_models,
        "max_budget": max_budget or default_budget,
        "duration": duration or "30d",
        "metadata": {
            "ldap_id": user_info.ldap_id,
            "department": user_info.department
        }
    }
```

```yaml
# config.yaml
general_settings:
  custom_key_generate: custom_auth.custom_key_generate_fn
```

### 10.2 JWT 認證（企業 SSO）

適合已部署 OKTA、Azure AD 等 SSO 的企業：

```yaml
general_settings:
  enable_jwt_auth: true
  litellm_jwtauth:
    team_id_jwt_field: "department"
    user_id_jwt_field: "sub"
    virtual_key_claim_field: "client_id"
    unregistered_jwt_client_behavior: "fallback_team_mapping"
    jwt_public_key_url: "https://your-idp/.well-known/jwks.json"
```

### 10.3 模型自動切換策略

```yaml
model_list:
  # 主模型 → 備用模型 → 降級模型
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: ${OPENAI_API_KEY}
      max_tokens: 4096
      temperature: 0.7
    model_group: primary
    fallbacks:
      - model_name: gpt-4o-mini
        litellm_params:
          model: openai/gpt-4o-mini
          api_key: ${OPENAI_API_KEY}
      - model_name: claude-sonnet-4
        litellm_params:
          model: anthropic/claude-sonnet-4
          api_key: ${ANTHROPIC_API_KEY}

  # 成本效益模型（行銷部優先使用）
  - model_name: gemini-pro
    litellm_params:
      model: gemini/gemini-pro
      api_key: ${GOOGLE_API_KEY}
    model_group: cost-effective
    fallbacks:
      - model_name: gpt-4o-mini
        litellm_params:
          model: openai/gpt-4o-mini
          api_key: ${OPENAI_API_KEY}
```

### 10.4 模型權重與負載均衡

```yaml
model_list:
  # 同一個邏輯模型名稱，配置多個實例，按權重分發
  - model_name: production-gpt4o
    model_info:
      id: production-gpt4o
      pricing: {"input": 0.0025, "output": 0.01}
    model_group: gpt4o-prod
    model_info:
      weight: 0.7  # 70% 流量
    litellm_params:
      model: openai/gpt-4o
      api_key: ${OPENAI_API_KEY}

  - model_name: staging-gpt4o
    model_info:
      id: staging-gpt4o
      pricing: {"input": 0.0025, "output": 0.01}
    model_group: gpt4o-prod
    model_info:
      weight: 0.3  # 30% 流量
    litellm_params:
      model: openai/gpt-4o
      api_key: ${OPENAI_STAGING_KEY}
```

---

## 成本預估

### 月度成本估算（200 人企業）

| 部門 | 人數 | 每人月預算 | 部門月預算 | 模型 |
|------|------|-----------|-----------|------|
| 技術部 | 50 | $50 | $2,500 | GPT-4o, Claude Sonnet |
| 行銷部 | 30 | $25 | $750 | Gemini Pro, GPT-4o-mini |
| 客服部 | 40 | $10 | $400 | GPT-3.5-turbo, 本地模型 |
| 管理層 | 10 | $150 | $1,500 | GPT-4o, Claude Sonnet |
| 財務部 | 10 | $30 | $300 | GPT-4o-mini, Claude Haiku |
| **合計** | **140** | - | **$5,450** | - |

> 💡 使用本地 Ollama 模型（如 llama3）可以大幅降低基礎模型成本，尤其適合客服部和內部工具。

---

## 快速啟動檢查清單

```bash
# ✅ 部署前檢查

# 1. 確認所有 API Keys 已設定
cat .env | grep -E "API_KEY"

# 2. 啟動服務
docker compose up -d

# 3. 確認服務狀態
docker compose ps

# 4. 測試 LiteLLM 是否正常
curl -s http://localhost:4000/health

# 5. 確認 Open WebUI 可訪問
curl -s http://localhost:8080/api/info

# 6. 建立部門
bash batch-create-teams.sh

# 7. 建立部門 Virtual Keys
bash create-department-keys.sh

# 8. 在 Open WebUI 中建立用戶群組
# 訪問 http://localhost:8080/admin

# 9. 測試部門模型隔離
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-eng-team-key" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4o", "messages": [{"role": "user", "content": "test"}]}'
```

---

## 常見問題

### Q: 用戶無法看到某個模型？
**A:** 檢查該用戶的 Virtual Key 是否綁定了正確的 Team ID，以及該 Team 的 model_list 中是否包含該模型。

### Q: 預算用完了怎麼辦？
**A:** LiteLLM 會在預算用完時自動拒絕請求，並返回 `ExceededBudget` 錯誤。管理員可以透過 Admin UI 調高預算。

### Q: 如何讓不同部門使用不同的 API Key（例如不同 Azure OpenAI 實例）？
**A:** 在 `model_list` 中為每個模型配置不同的 `api_key`，並透過 Team 的 `metadata` 或 Custom Auth 來路由。

### Q: 如何整合企業 LDAP/SSO？
**A:** 使用 LiteLLM 的 `custom_auth` 或 `JWT Auth` 功能，將企業身份系統與 Virtual Key 管理對接。

### Q: 如何限制用戶只能使用特定模型？
**A:** 兩種方式：(1) 在 Virtual Key 中設定 `models` 白名單；(2) 在 Open WebUI 的 RBAC 群組中設定模型使用權限。

### Q: 本地模型和雲端模型如何混合使用？
**A:** 在 `model_list` 中同時配置雲端模型（如 `openai/gpt-4o`）和本地模型（如 `ollama/llama3`），透過 Team 的模型白名單來控制。

---

## 相關資源

- **Open WebUI 官方文件**: https://docs.openwebui.com/
- **LiteLLM 官方文件**: https://docs.litellm.ai/
- **LiteLLM Enterprise 文件**: https://docs.litellm.ai/docs/enterprise
- **Open WebUI RBAC 文件**: https://docs.openwebui.com/features/authentication-access/rbac/
- **LiteLLM 多租戶架構**: https://docs.litellm.ai/docs/proxy/multi_tenant_architecture

---

**最後更新**: 2026-07-30  
**作者**: Hermes Agent 整理  
**原始專案**: [Open WebUI](https://github.com/open-webui/open-webui) · [LiteLLM](https://github.com/BerriAI/litellm)
