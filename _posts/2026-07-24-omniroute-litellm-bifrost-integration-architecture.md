---
layout: post
title: "OmniRoute + LiteLLM + Bifrost 整合架構規劃：打造企業級 AI Gateway"
date: 2026-07-24
description: 分析 OmniRoute、LiteLLM、Bifrost 三個 AI Gateway 項目的功能定位，並規劃三者整合的架構，打造高可用、多租戶、極速、智能路由的企業 AI 平台。
tags: [AI, AI Gateway, OmniRoute, LiteLLM, Bifrost, Architecture, Enterprise]
---

# OmniRoute + LiteLLM + Bifrost 整合架構規劃

## 三個項目的定位

在規劃整合前，先釐清三者各自的核心競爭力與功能重疊：

### LiteLLM：治理與多租戶核心

| 面向 | 說明 |
|------|------|
| 語言 | Python |
| 核心優勢 | 成熟的 **Team/Org/User/Key 四層多租戶**、階層式預算、Guardrails（PII、注入防禦） |
| Provider | 100+ |
| 定位 | **企業治理層** — 管人、管錢、管權限、管安全 |

### Bifrost：效能與 MCP 核心

| 面向 | 說明 |
|------|------|
| 語言 | Go |
| 核心優勢 | **極致效能**（<100 µs overhead）、**MCP Gateway**、內建 Semantic Cache、叢集模式 |
| Provider | 23+ |
| 定位 | **效能與工具層** — 管速度、管快取、管 MCP 工具 |

### OmniRoute：智能路由與 Provider 池核心

| 面向 | 說明 |
|------|------|
| 語言 | Node.js / TypeScript |
| 核心優勢 | **250+ Provider（含 90+ 免費 tier）**、18 種路由策略、**RTK+Caveman 壓縮（省 15-95% token）**、自動 fallback |
| Provider | 250+（最多） |
| 定位 | **智能路由層** — 管供應商池、管成本優化、管 token 壓縮 |

---

## 為什麼要整合？

單一工具的限制：

| 單一方案 | 問題 |
|---------|------|
| 只用 LiteLLM | 效能受限（Python）、MCP 功能不足 |
| 只用 Bifrost | Provider 池不夠大、缺少 OSS Guardrails |
| 只用 OmniRoute | 缺少企業級多租戶治理（Team Budget / Role） |

整合後的目標：**用 LiteLLM 管治理、Bifrost 管效能與 MCP、OmniRoute 管路由與供應商池**。

---

## 整合架構總覽

```
                          ┌────────────────────────────────────────┐
                          │            Open WebUI                  │
                          │      (UI / RBAC / Chat History)       │
                          └──────────────────┬─────────────────────┘
                                             │ /v1/chat/completions
                                             ▼
                          ┌────────────────────────────────────────┐
                          │         LiteLLM Proxy                  │
                          │   (治理層：Team / Budget / Guardrails) │
                          │   - 多租戶隔離、費用追蹤               │
                          │   - Virtual Key 權限控制               │
                          │   - Guardrails：PII / Prompt Injection │
                          └──────────────────┬─────────────────────┘
                                             │ 轉發至後端路由層
                                             ▼
                ┌──────────────────────────────────────────────────┐
                │              Bifrost Cluster                     │
                │   (效能層：MCP / Semantic Cache / HA)           │
                │   - <100µs overhead Go 路由                     │
                │   - MCP Gateway（工具整合）                      │
                │   - Semantic Cache（語意快取）                   │
                │   - 叢集模式、負載平衡                           │
                └──────────────────┬───────────────────────────────┘
                                   │ 智能路由與 fallback
                                   ▼
                ┌──────────────────────────────────────────────────┐
                │              OmniRoute                           │
                │   (路由層：智能選取 / Provider 池 / 壓縮)        │
                │   - 250+ Provider（含免費 tier）                 │
                │   - 18 種路由策略（cost-opt / auto-combo）       │
                │   - RTK + Caveman 壓縮（省 token）               │
                │   - 自動 fallback（毫秒級切換）                   │
                └──────────────────┬───────────────────────────────┘
                                   │ 最終調用
                ┌──────────────────────────────────────────────────┐
                │            Upstream Providers                    │
                │  OpenAI / Anthropic / Bedrock / Vertex / Ollama │
                │  + 200+ 其他 Provider（含免費 tier）             │
                └──────────────────────────────────────────────────┘
```

**請求流程：**

```
使用者 → Open WebUI → LiteLLM → Bifrost → OmniRoute → Provider
         [UI/RBAC]    [治理]     [效能/MCP] [路由/壓縮]  [LLM]
```

---

## 各層職責詳細說明

### 第一層：Open WebUI（UI 層）

| 職責 | 說明 |
|------|------|
| 使用者登入 | LDAP / OIDC / SAML 整合 |
| RBAC | Group / Permission 控制 UI 功能 |
| Model ACL | 控制 UI 上顯示哪些模型 |
| 聊天歷史 | 儲存對話紀錄、知識庫 |

**連接設定：**
- Base URL → `http://litellm:4000`
- Key → LiteLLM Virtual Key

### 第二層：LiteLLM（治理層）

| 職責 | 說明 |
|------|------|
| 多租戶隔離 | Team 層級隔離，每個部門獨立預算與模型權限 |
| 費用追蹤 | 每個請求歸算至 Team / User / Key |
| Guardrails | PII 遮蔽、Prompt Injection 防禦、輸出審核 |
| Virtual Key | 控制可存取哪些模型（即使 UI 顯示，API 層仍會拒絕） |
| Budget | 階層式預算（Org → Team → User → Key） |

**關鍵設定：**

```yaml
# LiteLLM config.yaml
general_settings:
  master_key: sk-master-key
  max_budget: 10000
  user_header_mappings:
    - header_name: X-OpenWebUI-User-Id
      litellm_user_role: internal_user

litellm_settings:
  max_budget: 10000

model_list:
  # 指向 Bifrost 作為上游
  - model_name: gpt-4o
    litellm_params:
      model: gpt-4o
      api_base: http://bifrost:8080

  - model_name: claude-sonnet-4
    litellm_params:
      model: claude-sonnet-4
      api_base: http://bifrost:8080

# Guardrails
guardrails:
  - guardrail_name: "presidio-pii"
    litellm_params:
      guardrail: presidio
      mode: pre_call
      default_on: true
```

### 第三層：Bifrost（效能與 MCP 層）

| 職責 | 說明 |
|------|------|
| 極速路由 | Go 原生 <100 µs overhead，適合高併發 |
| MCP Gateway | 統一管理模型與外部工具（FS、Web Search、DB） |
| Semantic Cache | 語意快取減少重複請求 |
| Cluster Mode | 叢集部署，水平擴展 |
| Load Balancing | 智能負載平衡至下游 |
| 可觀測性 | Prometheus Metrics、Tracing |

**關鍵設定：**

```json
{
  "providers": [
    {
      "id": "omniroute",
      "type": "openai-compatible",
      "baseUrl": "http://omniroute:20128/v1",
      "apiKey": "sk-omniroute-key"
    }
  ],
  "features": {
    "semanticCache": {
      "enabled": true,
      "similarityThreshold": 0.95
    },
    "mcp": {
      "enabled": true,
      "servers": ["filesystem", "web-search", "database"]
    }
  }
}
```

### 第四層：OmniRoute（智能路由與 Provider 池層）

| 職責 | 說明 |
|------|------|
| Provider 池 | 250+ Provider，含大量免費 tier（~1.6B token/月免費） |
| 18 種路由策略 | cost-optimized、auto-combo、fill-first、headroom、fusion… |
| RTK+Caveman 壓縮 | 自動壓縮 prompt（省 15-95% token） |
| 4-Tier Fallback | Subscription → API → Cheap → Free，毫秒級切換 |
| Circuit Breaker | 自動切斷失敗的 Provider |

**關鍵設定：**

```json
{
  "routingStrategy": "cost-optimized",
  "compression": {
    "rtk": true,
    "caveman": true
  },
  "fallback": {
    "enabled": true,
    "tiers": ["subscription", "api", "cheap", "free"]
  },
  "providers": [
    { "id": "openai", "apiKey": "sk-...", "type": "subscription" },
    { "id": "anthropic", "apiKey": "sk-...", "type": "subscription" },
    { "id": "siliconflow", "apiKey": "...", "type": "free" },
    { "id": "openrouter", "apiKey": "...", "type": "api" }
  ]
}
```

---

## 跨層協作流程（實際場景）

### 場景：行銷部 Alice 發出一個請求

```
1. Open WebUI：
   - Alice 登入 → Group: Marketing-Users → 可顯示 gpt-4o
   - 發送請求至 LiteLLM

2. LiteLLM：
   - 檢查 Team（marketing）→ models: ["gpt-4o"] ✓
   - 檢查 Guardrails → PII 遮蔽 ✓
   - 檢查 Budget → 本月剩餘 $180 ✓
   - 轉發至 Bifrost

3. Bifrost：
   - Semantic Cache 檢查 → 未命中
   - 極速路由至 OmniRoute（<100 µs）

4. OmniRoute：
   - cost-optimized 策略 → 先選 OpenAI gpt-4o（$2.5/MT）
   - RTK+Caveman 壓縮 → token 從 5000 → 3200（省 36%）
   - 呼叫 OpenAI API

5. 回應沿路返回：
   - LiteLLM 記錄費用：$0.0032 → 歸算至 marketing Team
```

### 場景：OpenAI 限流時的 Fallback

```
1. OmniRoute 收到 OpenAI 429 Too Many Requests
2. Circuit Breaker 自動觸發
3. 毫秒級 fallback 至下一最佳選擇（如 Bedrock Claude）
4. 對上游（Bifrost → LiteLLM → 使用者）完全透明
5. LiteLLM 仍正確歸算費用至對應 Team
```

---

## 部署架構（Docker Compose 範例）

```yaml
version: "3.9"

services:
  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    ports: ["3000:8080"]
    environment:
      ENABLE_FORWARD_USER_INFO_HEADERS: "True"
      OPENAI_API_BASE_URL: "http://litellm:4000"
      OPENAI_API_KEY: "sk-owui-key"
    volumes: ["open-webui:/app/backend/data"]

  litellm:
    image: ghcr.io/berriai/litellm:main-stable
    ports: ["4000:4000"]
    command: ["--config", "/app/config.yaml"]
    environment:
      MASTER_KEY: "sk-master-key"
      OPENAI_API_KEY: "sk-litellm-key"
      ANTHROPIC_API_KEY: "sk-ant-key"
    volumes: ["./litellm-config.yaml:/app/config.yaml"]
    depends_on: [bifrost]

  bifrost:
    image: maximhq/bifrost:latest
    ports: ["8080:8080"]
    volumes: ["bifrost-data:/app/data"]
    environment:
      BIFROST_UPSTREAM_URL: "http://omniroute:20128"
    depends_on: [omniroute]

  omniroute:
    image: diegosouzapw/omniroute:latest
    ports: ["20128:20128"]
    volumes: ["omniroute-data:/app/data"]
    environment:
      ROUTING_STRATEGY: "cost-optimized"
      # 各 Provider API Key
      OPENAI_API_KEY: "sk-..."
      ANTHROPIC_API_KEY: "sk-..."
    depends_on: []

volumes:
  open-webui:
  bifrost-data:
  omniroute-data:
```

---

## 架構優缺點分析

### 優點

| 優點 | 說明 |
|------|------|
| **各司其職** | LiteLLM 管治理、Bifrost 管效能、OmniRoute 管路由，互補不重疊 |
| **高可用** | 三層防護：OmniRoute fallback + Bifrost HA + LiteLLM circuit breaker |
| **成本優化** | OmniRoute 路由 + 壓縮 + 免費 tier，節省顯著 |
| **安全** | LiteLLM Guardrails 為所有請求提供防護 |
| **擴展性** | Bifrost 叢集模式可水平擴展 |
| **MCP 整合** | Bifrost MCP Gateway 統一管理工具 |

### 缺點

| 缺點 | 說明 |
|------|------|
| **架構複雜** | 四層串接增加部署與除錯難度 |
| **延遲疊加** | 每層增加微小延遲（雖然總和仍很小） |
| **維護成本** | 需同時維護四個服務的更新與相容性 |
| **過殺** | 小團隊可能不需要如此完整的架構 |

---

## 簡化方案建議

根據團隊規模選擇合適架構：

### 方案 A：完整方案（大型企業）
```
Open WebUI → LiteLLM → Bifrost → OmniRoute → Providers
```
- 適合：千人以上、多部門、預算 > $5k/月、需完整治理

### 方案 B：LiteLLM + OmniRoute（中型企業）
```
Open WebUI → LiteLLM → OmniRoute → Providers
```
- LiteLLM 管治理，OmniRoute 管路由與 Provider 池
- 適合：百人以上、多部門、預算 $1k-5k/月

### 方案 C：單用 LiteLLM（小型團隊）
```
Open WebUI → LiteLLM → Providers
```
- LiteLLM 內建 Load Balancing + Fallback，功能已足夠
- 適合：50 人以下、單一/少數部門

### 方案 D：LiteLLM + Bifrost（效能優先）
```
Open WebUI → LiteLLM → Bifrost → Providers
```
- LiteLLM 管治理，Bifrost 管效能與 MCP
- 適合：高併發需求、需 MCP 工具整合

---

## 總結

| 層次 | 工具 | 核心價值 |
|------|------|---------|
| UI / RBAC | Open WebUI | 使用者介面、功能權限 |
| 治理層 | LiteLLM | Team/Org/User 多租戶、預算、Guardrails |
| 效能層 | Bifrost | <100µs 延遲、MCP Gateway、Semantic Cache |
| 路由層 | OmniRoute | 250+ Provider、18 策略、RTK 壓縮、Fallback |

**三者完全可以整合使用**，各司其職互補不足，打造「治理嚴謹、效能極速、成本優化、高可用」的企業 AI Gateway。但請根據團隊規模選擇合適方案，避免過度工程化。

---

## 參考資料

- [OmniRoute GitHub](https://github.com/diegosouzapw/OmniRoute)
- [LiteLLM GitHub](https://github.com/BerriAI/litellm)
- [Bifrost GitHub](https://github.com/maximhq/bifrost)
- [Open WebUI GitHub](https://github.com/open-webui/open-webui)
