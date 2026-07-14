---
title: LiteLLM 與開源 LLM Gateway 產品比較
date: 2026-07-14
category: AI
tags: [LLM, Gateway, LiteLLM, 開源]
---

# LiteLLM 與開源 LLM Gateway 產品比較

> 整理日期：2026 年 7 月 14 日
>
> 本文整理目前與 **LiteLLM** 功能相似的 LLM Gateway / 代理工具，分析各產品的差異與適用場景。

---

## 📋 產品總覽

| 產品 | 語言 | 授權 | 開源 | 託管 | 自部署 |
|------|------|------|------|------|--------|
| **LiteLLM** | Python | MIT | ✅ | ✅ | ✅ |
| **Portkey** | Go | MIT (Gateway 2.0) | ✅ | ✅ | ✅ |
| **Cloudflare AI Gateway** | — | — | ❌ | ✅ | ❌ |
| **Kong AI Gateway** | Go | 商業 | ❌ | ✅ | ✅ (Enterprise) |
| **Bifrost** | Go | Apache 2.0 | ✅ | ✅ | ✅ |
| **OpenRouter** | — | — | ❌ | ✅ | ❌ |

---

## 🔍 各產品分析

### 1. LiteLLM

| 項目 | 說明 |
|------|------|
| **官網** | https://github.com/BerriAI/litellm |
| **GitHub Stars** | ~40k+ |
| **支援模型數** | 100+ 提供商，數百個模型 |
| **定位** | 開源 OpenAI 相容代理與 SDK |
| **核心功能** | 統一 API、虛擬金鑰管理、路由、成本追蹤、計費、虛擬金鑰預付卡 |
| **路由能力** | 基本路由 + fallback / load balancing |
| **Observability** | 整合 Langfuse、Helicone 等（非內建） |
| **Caching** | 支援語意快取（Semantic Caching） |
| **Guardrails** | ❌ 無內建 |
| **Governance** | 專案預設值、預算控制 |
| **費用** | 開源免費，託管版有付費方案 |
| **優勢** | 生態系最大、最廣為人知、100+ 提供商支援、OpenAI 相容 |
| **劣勢** | 性能不如 Go 寫的替代品、內建觀測性有限 |

---

### 2. Portkey

| 項目 | 說明 |
|------|------|
| **官網** | https://portkey.ai |
| **語言** | Go |
| **授權** | MIT（Gateway 2.0 開源） |
| **支援模型數** | 250+ 模型 |
| **定位** | 企業級 AI Gateway，強調觀測性與安全 |
| **核心功能** | 路由、Guardrails、語意快取、Observability、Governance |
| **路由能力** | ✅ 路由 + fallback + retry |
| **Observability** | ✅ 內建追蹤、錯誤分析、效能分析 |
| **Caching** | ✅ 語意快取（managed cloud） |
| **Guardrails** | ✅ 內容過濾、安全檢查 |
| **Governance** | SSO、VPC 託管（企業版） |
| **費用** | Free（10K logs/月）→ $49/月（Production）→ Enterprise（客製） |
| **優勢** | 觀測性最完整、Guardrails 內建、MIT 授權、輕量 |
| **劣勢** | 模型數不如 LiteLLM、語意快取需 managed cloud |

---

### 3. Cloudflare AI Gateway

| 項目 | 說明 |
|------|------|
| **官網** | https://www.cloudflare.com/products/ai-gateway/ |
| **定位** | Cloudflare 生態系下的邊緣快取代理 |
| **核心功能** | 邊緣快取、動態路由、Observability、Rate Limiting、Fallback |
| **路由能力** | ✅ 動態路由 |
| **Observability** | ✅ 內建分析儀表板 |
| **Caching** | ✅ 邊緣快取（核心差異） |
| **Guardrails** | ❌ 無內建 |
| **費用** | 核心功能免費（含於 Cloudflare 方案） |
| **優勢** | 邊緣快取性能極佳、Cloudflare 生態系整合、免費使用 |
| **劣勢** | 僅 Cloudflare 託管、無自部署選項、模型數較少、生態系鎖定 |

---

### 4. Kong AI Gateway

| 項目 | 說明 |
|------|------|
| **官網** | https://konghq.com/products/kong-ai-gateway |
| **語言** | Go |
| **授權** | 商業（非開源） |
| **定位** | 企業級 API 管理平台的 AI 擴展 |
| **核心功能** | 路由、成本控管、Token 速率限制、語意快取、安全防護 |
| **路由能力** | ✅ 進階路由 |
| **Observability** | ✅ 內建（Konnect 整合） |
| **Caching** | ✅ 語意快取 |
| **Guardrails** | ✅ 安全防護 |
| **Governance** | ✅ 企業級治理 |
| **費用** | 約 $105/月/服務（每連一個 LLM 提供商即算一個服務） |
| **優勢** | 成熟 API 管理平台延伸、企業級功能完整 |
| **劣勢** | **昂貴**（每服務 $105/月）、非開源、為 API Gateway 擴展而非原生 AI Gateway |

---

### 5. Bifrost

| 項目 | 說明 |
|------|------|
| **官網** | https://getmaxim.ai/bifrost |
| **語言** | Go |
| **授權** | Apache 2.0 |
| **支援模型數** | 1000+ 模型（23+ 提供商） |
| **定位** | 高性能企業 AI Gateway |
| **核心功能** | 自適應負載平衡、自動 Failover、語意快取、Guardrails、Observability |
| **路由能力** | ✅ 自適應負載平衡、自動 Failover |
| **Observability** | ✅ 內建 |
| **Caching** | ✅ 語意快取 |
| **Guardrails** | ✅ 內建 |
| **Governance** | ✅ 內建 |
| **費用** | 開源免費，Enterprise 版客製 |
| **優勢** | **50x 比 LiteLLM 快**（Go 寫）、性能極佳、功能完整、Apache 2.0 |
| **劣勢** | 知名度較低、生態系不如 LiteLLM 大 |

---

### 6. OpenRouter

| 項目 | 說明 |
|------|------|
| **官網** | https://openrouter.ai |
| **定位** | 託管型 LLM 聚合器（非代理工具） |
| **支援模型數** | 400+ 模型、60+ 提供商 |
| **核心功能** | 統一 API、整合計費、模型市場 |
| **路由能力** | ✅ 自動選擇最佳模型 |
| **Observability** | ✅ 請求日誌 |
| **Caching** | ❌ 無內建 |
| **Guardrails** | ❌ 無內建 |
| **費用** | 按 Token 計費（提供者價格直轉） |
| **優勢** | 模型數最多（400+）、單一金鑰存取所有模型 |
| **劣勢** | **非開源、不可自部署**、無自訂路由邏輯、依賴第三方 |

---

## 📊 功能對比總表

| 功能 | LiteLLM | Portkey | Cloudflare | Kong | Bifrost | OpenRouter |
|------|---------|---------|------------|------|---------|------------|
| **開源** | ✅ MIT | ✅ MIT | ❌ | ❌ | ✅ Apache 2.0 | ❌ |
| **自部署** | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |
| **託管版** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **OpenAI 相容 API** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **支援提供商數** | 100+ | 250+ | 少 | 少 | 23+ | 60+ |
| **路由能力** | ✅ 基本 | ✅ 進階 | ✅ 動態 | ✅ 進階 | ✅ 自適應 | ✅ 自動 |
| **自動 Failover** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **語意快取** | ✅ | ✅ (managed) | ✅ (邊緣) | ✅ | ✅ | ❌ |
| **Observability** | 整合 | ✅ 內建 | ✅ 內建 | ✅ 內建 | ✅ 內建 | 基本 |
| **Guardrails** | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ |
| **Governance/SSO** | 基本 | Enterprise | ❌ | ✅ | ✅ | ❌ |
| **Token 速率限制** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **成本追蹤** | ✅ 內建 | ✅ | ✅ | ✅ | ✅ | ✅ |
| **負載平衡** | ✅ | ✅ | ❌ | ✅ | ✅（自適應） | ❌ |
| **價格** | 免費 | $49/月起 | 免費 | $105/服務/月起 | 免費 | 按量計費 |

---

## 🎯 選擇建議

| 使用場景 | 推薦產品 | 原因 |
|----------|----------|------|
| **需要最大生態系 & 100+ 提供商** | LiteLLM | 支援最多、社群最大 |
| **需要內建 Observability 與 Guardrails** | Portkey | 觀測性最完整、MIT 授權 |
| **需要邊緣快取效能** | Cloudflare AI Gateway | 邊緣快取為核心差異 |
| **已有 Kong 基礎建設的企業** | Kong AI Gateway | 與現有 API 管理整合 |
| **需要最高性能（低延遲）** | Bifrost | Go 寫，50x 快於 LiteLLM |
| **不想自己管理，只想用** | OpenRouter | 單一金鑰存取 400+ 模型 |
| **開源 + 功能完整** | Bifrost | Apache 2.0，功能齊全 |
| **小型團隊 / 快速上線** | LiteLLM | 上手最簡單、文件最多 |

---

## 🔄 常見組合

許多團隊會混合使用：

1. **LiteLLM + Langfuse** — 開源代理 + 開源追蹤
2. **Portkey + OpenRouter** — Guardrails + 更多模型選擇
3. **Bifrost + Cloudflare** — 高性能代理 + 邊緣快取
4. **Kong + Helicone** — 企業治理 + 成本分析

---

## 📝 結語

LLM Gateway 生態系在 2025-2026 年快速成長。選擇時應考慮：

- **自部署需求**：LiteLLM、Portkey、Bifrost（開源可自部署）
- **性能要求**：Bifrost（Go）> Portkey（Go）> LiteLLM（Python）
- **功能完整度**：Portkey ≈ Bifrost > LiteLLM > OpenRouter
- **成本**：開源免費（自部署）> Cloudflare 免費 > 按量計費 > 企業授權

> ⚠️ 以上資訊截至 2026 年 7 月 14 日，各產品持續更新中，請以官方最新資訊為準。

---

*本文由 Hermes Agent 整理，資料來源為各產品官方文件與第三方比較文章。*
