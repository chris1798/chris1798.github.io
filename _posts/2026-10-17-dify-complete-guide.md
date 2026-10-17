---
title: "Dify 完整功能解析與適用場景：企業自架前必讀的选型指南"
date: 2026-10-17
description: Dify 是目前 GitHub star 數最高的開源 LLM 應用開發平台（~144k）。本文完整梳理其功能地圖、自架架構、授權與版本分界、適用與不適用場景，並與 Open WebUI、n8n、LangGraph 對比。
tags: [AI, LLM, Dify, RAG, Agent, 自架, 開源]
---

# Dify 完整功能解析與適用場景：企業自架前必讀的选型指南

> 整理日期：2026-10-17。資料來源：Dify 官方文件（docs.dify.ai）、GitHub 倉庫（langgenius/dify）與 LICENSE 原文。

## 一、Dify 是什麼

**Dify**（名字取自 **D**o **I**t **F**or **Y**ou）是一個開源的 LLM 應用開發平台，把「Agent 編排、視覺化工作流、RAG 知識管線、模型管理、應用發布」整合在同一個協作工作區裡。定位是讓團隊從原型一路做到生產，不必中途換掉技術棧。

| 基本資訊 | 數值（2026-10） |
|---|---|
| GitHub Stars | ~144k（同類專案最高） |
| 授權 | Dify Open Source License（Apache 2.0 修改版 + 附加條款） |
| 主要語言 | Python（後端）+ TypeScript（前端） |
| 部署方式 | Dify Cloud（托管）/ Docker Compose 自架 / VPC |
| 生態 | 插件 Marketplace、MCP Server/Client、REST API、difyctl CLI |

## 二、核心功能地圖

### 1. 五種應用類型

| 類型 | 說明 | 典型用途 |
|---|---|---|
| **Chatbot** | 對話型應用，可掛知識庫與工具 | 客服、內部問答 |
| **Chatflow** | 對話 + 視覺化工作流：每輪對話走過你定義的節點流程 | 有狀態的多輪向導式助手 |
| **Workflow** | 一次性批次流程：輸入→處理→輸出 | 報告生成、資料處理管線、批次打标 |
| **Agent** | 模型自主決定呼叫哪些工具（Function Calling / ReAct） | 需要動態工具選擇的任務 |
| **Text Generator** | 單輪提示型生成 | 翻譯、改寫、模板填充 |

### 2. 視覺化編排（Workflow / Chatflow 畫布）

- 拖曳節點連接流程：LLM 節點、知識檢索、程式碼執行（Python/JS 沙箱）、條件分支、迭代、變數聚合、HTTP 請求、模板轉換等。
- **除錯與版本控制**：逐節點试运行、時間軸回放、版本快照與回滾。
- **Snippets（片段）**：可重複使用的子流程，把常用邏輯模組化。
- 核心理念是「Agentic Workflow」：AI 仍做主要工作，但跑在你定義的結構化、可重複、有檢查點與回退路徑的流程邊界內——這正是它與純聊天工具最大的差異。

### 3. 知識庫（RAG）

- 多知識庫管理：每個知識庫可對應不同領域/資料源，應用中按需掛載。
- 文件上傳（PDF/Word/Markdown/HTML…）、網站抓取、Notion 同步等資料源。
- 多種 chunking 策略、embedding 模型可選、混合檢索（向量+全文）、重排序（rerank）、元資料過濾。
- **外部知識庫 API**：可把公司既有的向量庫/檢索服務接進來，不必遷移資料。
- 檢索測試介面：先驗證召回品質再接入應用。

### 4. 模型層

- 支援數百家模型供應商：OpenAI、Anthropic、Gemini、Azure、Bedrock、Ollama、本地 OpenAI-compatible 端點等。
- 每個供應商可設多組憑證與配額；支援多模態（圖片、語音輸入輸出）。
- **可接自建 Gateway**：任何 OpenAI-compatible 端點都能接，例如把 Dify 指向 LiteLLM Proxy，模型帳務與配額統一治理。

### 5. 工具與插件生態

- 內建工具 + Marketplace 社群插件（搜尋、資料庫、SaaS 整合…）一鍵安裝。
- 自製工具：OpenAPI schema / 自訂 endpoint。
- **MCP 雙向支援**：既能把 MCP 工具接進來當 agent 工具，也能把自己的應用**發布成 MCP Server** 給 Claude/Cursor 等外部 agent 使用。
- 插件開發 SDK：自己寫工具、模型供應商、擴展。

### 6. 發布與整合

| 管道 | 說明 |
|---|---|
| Web App | 一鍵發布成可分享的網頁應用（可嵌入既有網站的 widget） |
| REST API | 每個應用自動產生 API，後端/CI 直接呼叫 |
| MCP Server | 應用發布成 MCP 服務，供其他 agent 呼叫 |
| difyctl CLI | 從終端機/腳本/CI/AI agent 操作 Dify 應用 |

### 7. 監控與品質

- **日誌與追蹤**：每個應用的對話/執行記錄，可整合 Langfuse 等第三方 observability。
- **註解系統（Annotation）**：人工標記好/壞回答，作為後續 few-shot 範例回流。
- **Dashboard**：用量、成本、活躍用戶統計。
- **速率限制**：per-app 請求限流。

### 8. 工作區與協作

- 應用、知識庫、工具、成員在同一 workspace 集中管理。
- 社群版：單一 team、基本角色（admin/editor/normal）。
- **SSO（SAML/OIDC）、細粒度 RBAC（到 workflow 層）、多隔離 workspace、稽核日誌 → Enterprise 版功能**。

## 三、自架架構與部署

Docker Compose 一把啟動，主要服務：

```
nginx（入口）
├── web        前端（Next.js）
├── api        後端 API（Flask/Celery 隊列）
├── worker     非同步任務（文件索引等）
├── db         PostgreSQL
├── redis      快取/佇列
├── weaviate / qdrant / milvus…   向量庫（可選）
├── sandbox    程式碼執行沙箱
└── ssrf_proxy 出站請求安全代理
```

- **硬體**：一般 CPU 機器即可（除非本地跑 embedding/rerank 模型）；官方建議 2C4G 起，生產建議外加獨立 Postgres。
- **升級**：版本迭代快，升級需跑 migration，建議固定維護窗口；生產環境務必先備份 DB 與卷。
- **安全**：內建 SSRF proxy 與程式碼沙箱，預設比裸接 LLM 保守；對外發布應用建議放反向代理後並開 HTTPS。

## 四、授權與版本分界（重點）

LICENSE 原文兩條附加條款，企業自架前務必確認：

1. **多租戶限制**：不得用 Dify 原始碼營運 multi-tenant 環境，除非取得書面授權。**一個 tenant = 一個 workspace**。單一公司內部用一個 workspace 給所有員工 → 明確允許；開多個 workspace 給不同外部客戶 → 需要商業授權（Enterprise）。
2. **前端 LOGO/版權不可移除或修改**（`web/` 目錄部分）；純後端 API 使用不受此限。

| 功能 | Community（免費自架） | Enterprise（付費） |
|---|---|---|
| 全部編排/RAG/工具/發布功能 | ✅ | ✅ |
| workspace 數 | 單一 | 多個隔離 workspace |
| 登入方式 | Email/密碼 | SSO SAML/OIDC、強制 SSO |
| 權限 | 基本角色 | 細粒度 RBAC 到 workflow 層 |
| 稽核日誌 | ❌ | ✅ |
| 負載均衡/HA、SLA 支援 | ❌ | ✅ |
| 去品牌 | ❌（條款禁止） | ✅ |

實務提醒：社群版做「部門級隔離」需要大量客製（GitHub 討論區有企業部署案例證實），不要假設免費版能做到租戶級隔離。

## 五、適用場景分析

### ✅ 適合

| 場景 | 為什麼選 Dify |
|---|---|
| 企業內部知識問答（政策、IT 服務台、HR FAQ） | RAG 管線完整、非工程師也能維護知識庫 |
| 客服機器人 / 對外 FAQ | 掛知識庫 + 一鍵發布 Web App/API，有註解回流機制持續改善 |
| 表單式/批次流程自動化 | Workflow 類應用：報告生成、資料清洗、內容審核鏈 |
| 多部門共用一個 AI 應用工廠 | 應用模板、插件市場、協作工作區 |
| 把內部系統包成 MCP 給 coding agent 用 | 應用發布成 MCP Server 是獨有優勢 |
| 快速 PoC 給主管看 | 視覺化 + 模板市場，半天能出 demo |

### ❌ 不適合

| 場景 | 更好的選擇 |
|---|---|
| 純粹「員工聊天入口」，要 SSO/LDAP 免費內建 | Open WebUI（SSO/RBAC/稽核全免費） |
| 深度客製 agent 邏輯、需要完全掌控 prompt 邊界 | LangGraph / 直接寫 code |
| 與既有 IT 系統大量事件式整合（webhook、排程、400+ SaaS） | n8n |
| 給外部客戶各開一個租戶的 SaaS | 需付費商業授權，或改選 MIT 授權方案（如 Onyx） |
| 極致 RAG 品質研究、自訂檢索演算法 | 專用 RAG 框架（LlamaIndex、RAGFlow） |

## 六、與相近工具的定位對比

| | **Dify** | **Open WebUI** | **n8n** | **LangGraph** |
|---|---|---|---|---|
| 本質 | AI 應用**工廠** | 員工 AI **入口** | 流程**自動化** | agent **編排函式庫** |
| 使用者 | 開發者+公民開發者 | 全體員工 | IT/營運 | 工程師 |
| 視覺化編排 | ✅ 強 | ❌（代碼 pipelines） | ✅ 強（非 AI 導向） | ❌（程式碼圖） |
| RAG | 完整管線+調試 | 够用 | 弱 | 自己搭 |
| 免費 SSO/RBAC | ❌ Enterprise | ✅ | 部分 | — |
| 部署複雜度 | 中（7+ 服務） | 低（單 container） | 低-中 | 自己管 |
| 產出物 | 可發布的 App/API | 聊天體驗 | 自動化流程 | 你自己寫的系統 |

三者常見共存模式：**Open WebUI 當員工日常助手層、Dify 當應用產品化層、n8n 當系統整合層**，全部指向同一個 LiteLLM Gateway 做模型治理。

## 七、企業落地建議路徑

1. **試行（第 1 個月）**：Docker Compose 起社群版 → 模型端點指向公司 LLM Gateway → 單一 workspace，選 1–2 個團隊做知識庫問答 PoC。完全在免費授權範圍內。
2. **評估（第 2–3 個月）**：看三個指標——非工程師實際建應用數、RAG 回答可接受率（用註解系統統計）、維運事件數。
3. **決策**：需要部門隔離/SSO/稽核時，比較「買 Dify Enterprise」vs「Open WebUI（免費 SSO）+ 保留 Dify 做應用層」vs「MIT 授權替代品」。
4. **紅線**：不要把 Dify 包成對外多租戶服務、不要移除前端 LOGO，除非已購商業授權。

## 八、參考資料

- Dify GitHub：https://github.com/langgenius/dify
- Dify 官方文件：https://docs.dify.ai
- LICENSE 原文：https://github.com/langgenius/dify/blob/main/LICENSE
- Dify Enterprise：https://dify.ai/dify-enterprise
- Open WebUI 官方 Dify 對比頁：https://docs.openwebui.com/alternatives/dify/
