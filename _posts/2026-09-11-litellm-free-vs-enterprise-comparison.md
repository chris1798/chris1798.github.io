---
title: "LiteLLM 免費版 vs 企業版：完整差異比較"
date: 2026-09-11
description: LiteLLM（BerriAI）是開源的 LLM 代理閘道器。本文整理 Free（OSS，MIT）與 Enterprise 兩版的完整功能差異：SSO、RBAC、審計日誌、多區域部署、支援 SLA 等。
tags:
  - litellm
  - llm
  - ai-gateway
  - self-hosted
  - enterprise
---

# LiteLLM 免費版 vs 企業版：完整差異比較

> **LiteLLM**（BerriAI）是開源的 LLM 代理閘道器（AI Gateway），讓你的應用用一個 OpenAI 相容 API 存取 100+ 個模型供應商。
> 本文整理 **Free（OSS，MIT）** 與 **Enterprise** 兩版的完整功能差異。

---

## 📊 專案速覽

| 項目 | 資料 |
|------|------|
| **名稱** | LiteLLM（BerriAI / Berrie AI Inc.） |
| **授權** | MIT（OSS）/ Enterprise License |
| **Stars** | ⭐ 30,000+ |
| **技術棧** | Python（FastAPI + Uvicorn） |
| **支援版本** | 最近 4 個 stable minor lines（2026-06：1.86–1.89） |
| **官方網站** | [litellm.ai](https://www.litellm.ai) |
| **文件** | [docs.litellm.ai](https://docs.litellm.ai) |

---

## 🎯 什麼是 LiteLLM？

### 一句話說明

> **一個 OpenAI 相容的代理閘道器，讓你的應用用同一個 API 存取 100+ 個 LLM 供應商（OpenAI、Anthropic、Google、本地模型…），並附帶成本追蹤、預算、fallback、日誌等治理功能。**

### OSS 已包含的核心功能

LiteLLM OSS（免費）已經涵蓋了基礎：
- ✅ OpenAI 相容閘道器
- ✅ Virtual keys（虛擬金鑰）
- ✅ Spend tracking（成本追蹤）
- ✅ Budgets（預算）
- ✅ Fallbacks（fallback 機制）
- ✅ Request/response logging

> **Enterprise 是在 OSS 之上加「大組織需要的治理、安全、支援」，不是不同的核心。**

---

## ⚖️ Free vs Enterprise：完整功能比較

### 🔐 認證與存取控制（Authentication & Access Control）

| 功能 | Free (OSS) | Enterprise |
|------|:---------:|:----------:|
| **API keys** | ✅ | ✅ |
| **SSO**（Okta、Azure AD、Google Workspace、OIDC/SAML） | ❌ | ✅ |
| **SCIM**（自動用戶同步） | ❌ | ✅ |
| **JWT-based Authentication** | ❌ | ✅ |
| **Virtual keys / users / teams** | ✅ | ✅ |
| **Organizations + org/team admins** | ❌ | ✅ |
| **Delegated admin roles** | ❌ | ✅ |
| **Key rotations**（自動輪換） | ❌ | ✅ |
| **Secret Managers**（AWS KMS、Azure Key Vault、GCP KMS、HashiCorp Vault…） | ❌ | ✅ |
| **IP address-based ACLs**（CIDR 限制） | ❌ | ✅ |
| **Public & private route controls** | ❌ | ✅ |

> **SSO 免費額度**：最多 5 個用戶可免費用 SSO。超過 5 人需 Enterprise license。

---

### 🛡️ Guardrails（安全護欄）

| 功能 | Free (OSS) | Enterprise |
|------|:---------:|:----------:|
| **Set guardrails per request** | ✅ | ✅ |
| **Default-on guardrails** | ✅ | ✅ |
| **Custom guardrails + Presidio（PII masking）** | ✅ | ✅ |
| **Key/team-scoped guardrails** | ❌ | ✅ |
| **llmguard_moderations** | ❌ | ✅ |
| **llamaguard_moderations** | ❌ | ✅ |
| **hide_secrets** | ❌ | ✅ |
| **openai_moderations** | ❌ | ✅ |
| **google_text_moderation** | ❌ | ✅ |
| **lakera_prompt_injection** | ❌ | ✅ |
| **aporia_prompt_injection** | ❌ | ✅ |

> OSS 支援自訂 guardrails + Presidio（PII masking）。但幾個內建 callback 整合（moderation、prompt injection 偵測）需要 Enterprise license。

---

### 📊 Logging & Observability（日誌與可觀察性）

| 功能 | Free (OSS) | Enterprise |
|------|:---------:|:----------:|
| **Request/response logging** | ✅ | ✅ |
| **Prometheus metrics** | ✅ | ✅ |
| **Datadog / S3 / GCS / Azure Data Lake logging** | ✅ | ✅ |
| **Per-key / per-team routing to Langfuse, LangSmith, Arize** | ❌ | ✅ |
| **Team-based logging**（每隊獨立 Langfuse project） | ❌ | ✅ |
| **Disable logging per team**（GDPR opt-out） | ❌ | ✅ |
| **Log export to GCS / Azure Blob** | ❌ | ✅ |
| **Management-op logs**（管理操作日誌） | ❌ | ✅ |

---

### 💰 Spend Tracking & Budgets（成本追蹤與預算）

| 功能 | Free (OSS) | Enterprise |
|------|:---------:|:----------:|
| **Track spend by model/key/user/team** | ✅ | ✅ |
| **Track spend for org** | ❌ | ✅ |
| **Track spend for custom tags** | ❌ | ✅ |
| **API endpoints for spend reporting** | ❌ | ✅ |
| **Set budgets by key/user/team** | ✅ | ✅ |
| **Set rate limits by key/user/team** | ✅ | ✅ |
| **Temporary budget increase**（時間限定臨時提高） | ❌ | ✅ |
| **Budget/rate limit tiers** | ❌ | ✅ |
| **Tag-based budgets** | ❌ | ✅ |
| **Model-specific budgets per virtual key** | ❌ | ✅ |
| **Soft budget email alerts** | ❌ | ✅ |
| **Generate spend reports**（程式化存取） | ❌ | ✅ |

---

### 👥 User & Team Management（用戶與團隊管理）

| 功能 | Free (OSS) | Enterprise |
|------|:---------:|:----------:|
| **Create / manage users** | ✅ | ✅ |
| **Create / manage teams** | ✅ | ✅ |
| **Create / manage orgs** | ❌ | ✅ |
| **Assign team admins** | ❌ | ✅ |
| **Assign org admins** | ❌ | ✅ |
| **Control model access（by key/user/team）** | ✅ | ✅ |
| **Model access groups** | ❌ | ✅ |
| **Team-only models** | ❌ | ✅ |
| **Admin UI internal user self-serve** | ❌ | ✅ |
| **Auto-add SSO user to teams** | ❌ | ✅ |

---

### 🏗️ Deployment（部署）

| 功能 | Free (OSS) | Enterprise |
|------|:---------:|:----------:|
| **Single-region proxy** | ✅ | ✅ |
| **Multi-region deployment under one license** | ❌ | ✅ |
| **Admin/worker split** | ❌ | ✅ |

---

### 🎨 Branding & Operations（品牌與操作）

| 功能 | Free (OSS) | Enterprise |
|------|:---------:|:----------:|
| **Custom Swagger branding** | ❌ | ✅ |
| **Custom email branding**（logo + colors） | ❌ | ✅ |
| **Max request/response size limits** | ❌ | ✅ |
| **Team-managed models**（團隊自帶 keys/fine-tunes） | ❌ | ✅ |
| **AI Hub**（公開品牌化模型/agent 頁面） | ❌ | ✅ |

---

### 📁 Projects（專案管理）

> Enterprise 獨有的功能：把 virtual keys 按應用或用途分組，每個 project 有獨立預算、owner、rate limit、隔離的 spend view。

| 功能 | Free (OSS) | Enterprise |
|------|:---------:|:----------:|
| **Group keys by app/environment/customer** | ❌ | ✅ |
| **Per-project budgets, rate limits, model allowlists** | ❌ | ✅ |
| **Dedicated owners and spend dashboards** | ❌ | ✅ |

---

### 🤝 Support（支援）

| 功能 | Free (OSS) | Enterprise |
|------|:---------:|:----------:|
| **Community support**（GitHub issues/Discord） | ✅ | ✅ |
| **Dedicated Slack/Teams channel** | ❌ | ✅ |
| **Support hours** | — | 9am–9pm PST, Mon–Fri |
| **24/7 Support SLA**（額外費用） | ❌ | ✅ |

#### 24/7 SLA 回應時間

| Severity | 說明 | 回應時間 |
|----------|------|---------|
| **Sev 0** | 100% production traffic failing | **1 小時** |
| **Sev 1** | Partial production impact | **6 小時** |
| **Sev 2–3** | Setup issues, non-urgent bugs | **24 小時**（7am–7pm PT, Mon–Sat） |
| **Security patches** | 安全修補 | **72 小時** |

---

## 💵 定價

### Free (OSS)

```text
$0 / 永久免費自架
MIT license，可商用
無 token markup（不向模型供應商加價）
```

### Enterprise

```text
依部署規模定價（不是 per-token）
SSO 最多 5 用戶免費；超過需 license
30 天免費試用
聯絡銷售取得報價
AWS / Azure Marketplace 可採購
```

> **注意**：Enterprise 的 $250/月起（據第三方報導）只是軟體授權費，實際 TCO 還包含基礎設施（$300–700）+ DevOps 時間（~$1,730），約 **$2,280–2,680/月**。

---

## 🏗️ 技術架構

```text
LiteLLM Proxy (FastAPI + Uvicorn)
├── OpenAI-compatible API endpoint
├── Virtual Key management
├── Spend tracking + budgets
├── Fallback / retry logic
├── Logging (Datadog, S3, GCS, Azure, Langfuse…)
├── Guardrails (custom + Presidio)
└── 100+ provider integrations
    ├── OpenAI, Anthropic, Google, AWS Bedrock
    ├── Azure, Cohere, Mistral, Groq
    ├── Local: Ollama, vLLM, llama.cpp
    └── ...
```

---

## 📊 支援的版本線

LiteLLM 支援**最近 4 個 stable minor lines**，每個 line 持續收 patch：

| 時間 | 支援的 lines |
|------|-------------|
| 2026-06-29 起 | **1.86, 1.87, 1.88, 1.89** |
| 之後 | 向前滾動（新 stable line 發布時，最舊的 EOL） |

> 比這更舊的版本會達到 end-of-life，停止收更新。

---

## 🎯 該選哪個？

### 選 Free (OSS) 如果：

- ✅ 團隊 < 20 人
- ✅ 不需要 SSO（或 ≤5 用戶）
- ✅ AI 用途是實驗性 / 內部工具
- ✅ 想完全掌控、自架在自家基礎設施
- ✅ 預算有限

### 選 Enterprise 如果：

- ✅ 100+ 用戶或 10+ production AI use-cases
- ✅ 需要 SSO（Okta/Azure AD/Google）+ SCIM
- ✅ 需要審計日誌 + RBAC + IP ACL
- ✅ 需要多區域部署 + admin/worker split
- ✅ 需要 24/7 SLA 支援
- ✅ 需要 per-team logging、tag-based budgets、project management
- ✅ 需要品牌化（Swagger/email）+ AI Hub

---

## 🏆 客戶案例

| 公司 | 使用方式 |
|------|---------|
| **NVIDIA** | 「單一一致的方式存取 100+ AI model endpoints」 |
| **Netflix** | 「讓團隊在模型發布後一天內就能用，省下幾個月工作」 |
| **Okta** | 「切換 backend model 只需改 gateway config，不需 code changes / procurement / security review」 |
| **AT&T** | 「某些進階 AI 任務（coding）成本降低最多 56%」 |
| **Lemonade** | 「簡化管理多個 LLM models 的複雜性」 |

---

## 總結

**LiteLLM Free vs Enterprise 的核心差異**：

```text
Free (OSS)：OpenAI 相容閘道器 + virtual keys + spend tracking + budgets + fallbacks + logging
Enterprise：+ SSO/SCIM + RBAC + 審計日誌 + multi-region + per-team logging + project management + 24/7 SLA
```

| 維度 | Free | Enterprise |
|------|:----:|:----------:|
| **核心閘道器** | ✅ 相同 | ✅ 相同 |
| **成本追蹤** | 基本（key/user/team） | 進階（org/tag/project/model-specific） |
| **安全** | API keys + guardrails | + SSO/SCIM + RBAC + IP ACL + key rotation + secret managers |
| **部署** | Single-region | + Multi-region + admin/worker split |
| **支援** | Community | Dedicated channel + 24/7 SLA |

> **關鍵原則**：Enterprise 是在 OSS 之上加「治理、安全、支援」，不是不同的核心。如果團隊小（<20 人）且不需要 SSO/RBAC，OSS 就夠了。

---

*本文於 2026-09-11 整理自 [litellm.ai/features](https://www.litellm.ai/features) 與 [docs.litellm.ai/docs/enterprise](https://docs.litellm.ai/docs/enterprise)*
