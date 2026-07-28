---
title: "AnythingLLM 完整功能解析：本地首選的 AI 聊天與 Agent 平台"
date: 2026-07-28
description: 深度解析 Mintplex-Labs 的 AnythingLLM 開源專案，涵蓋 RAG 文件對話、AI Agent、MCP 相容性、多用戶架構等核心功能，附完整技術規格。
tags: [AI, AnythingLLM, RAG, Agent, 開源, LLM, 本地部署]
---

# AnythingLLM 完整功能解析

![AnythingLLM Logo](https://github.com/Mintplex-Labs/anything-llm/blob/master/images/wordmark.png?raw=true)

## 專案概述

**AnythingLLM** 是由 Mintplex Labs 開發的開源一站式 AI 應用程式，標語為「停止租用你的智慧，用 AnythingLLM 擁抱它」。這個專案在 GitHub 上已獲得超過 **64,000+ Star**，是一個功能完備的本地優先（local-first）AI 體驗平台。

![GitHub Stats](https://api.star-history.com/svg?repos=mintplex-labs/anything-llm&type=Timeline)

### 核心定位

AnythingLLM 允許你建立一個私有的、功能完整的 ChatGPT — 沒有妥協。你可以連接偏好的本地或雲端 LLM，匯入文件，幾分鐘內開始對話。內建 agents、多用戶支援、向量資料庫和文件管線 — 無需額外的設定。

![Chat Interface Demo](https://github.com/Mintplex-Labs/anything-llm/releases/download/v1.11.2/AnythingLLM720p.gif)

## 🌟 核心功能一覽

### 1. 動態模型路由（Dynamic Model Routing）

根據你定義的規則，自動將對話路由到最佳的提供者和模型。這意味著不同的查詢可以智慧地選擇最適合的 LLM — 例如簡單問題走快速模型，複雜推理走強模型。

![Model Router](https://docs.anythingllm.com/assets/images/model-router-overview-5a7f1f1e4c2b5e0c8a9d3b2f4e6a7c8d.jpg)

### 2. 自動與使用者管理記憶（Memories）

讓你的 LLM 記住關於你或你的工作區的重要資訊。系統可以自動提取關鍵資訊，也可以由使用者手動管理記憶內容。

### 3. 排程任務（Scheduled Tasks）

在 cron 排程上執行重複任務或提示，具備完整的 Agent 能力。可以設定定期自動執行特定工作流。

### 4. 智慧技能選擇（Intelligent Skill Selection）

啟用 **無限** 工具給你的模型，同時每筆查詢可減少高達 **80%** 的 token 使用量。系統會自動選擇最相關的 tool。

### 5. 無程式碼 AI Agent 建構器（No-code Agent Builder）

透過視覺化介面建構複雜的 AI Agent 工作流，無需編寫程式碼。支援流程式的條件判斷、迴圈和資料轉換。

![Agent Builder](https://docs.anythingllm.com/assets/images/agent-flow-builder-3f5a7b9c1d2e4f6a8b0c1d2e3f4a5b6c.png)

### 6. MCP 相容性（MCP Compatibility）

支援 Model Context Protocol（MCP），讓 AnythingLLM 可以與各種外部工具和服務無縫整合。

### 7. 多模態支援

同時支援閉源和開源 LLM 的多模態功能，包括文字、圖片、語音等多種輸入輸出格式。

### 8. 自訂 AI Agent

建立具有特定職責和能力的自訂 Agent，每個 Agent 可以有獨立的人格、工具和記憶。

### 9. 多用戶支援

支援多用戶環境，每個使用者可以控制自己的存取權限和體驗，同時不影響例項的安全性或隱私權（Docker 版本）。

![Multi-user Setup](https://docs.anythingllm.com/assets/images/multi-user-setup-7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d.png)

### 10. 可嵌入的聊天小工具

提供自訂的網站嵌入聊天小工具，可以輕鬆將 AnythingLLM 整合到你的網站中（Docker 版本）。

### 11. 文件處理

支援多種文件格式的匯入：
- **PDF** 文件
- **TXT** 文字檔
- **DOCX** Word 文件
- 以及更多格式

支援拖放上傳和來源引用，對話 UI 直觀易用。

### 12. 生產級雲端部署

完全適合任何雲端部署環境，提供 Docker、AWS、GCP、Digital Ocean、Render.com 等多種部署方式。

### 13. 完整的開發者 API

提供完整的 API 介面，方便進行客製化整合。

### 14. 大文件集最佳化

針對大型文件集的最佳化 — 比其他聊天介面更低的成本和更快的回應速度。

## 📊 支援的模型與服務

### 大型語言模型（LLMs）— 超過 40+ 供應商

| 類型 | 支援的提供者 |
|------|------------|
| **開源本地** | llama.cpp 相容模型、Ollama、LM Studio、LocalAI、KoboldCPP |
| **雲端 API** | OpenAI、Anthropic、Google Gemini、AWS Bedrock、Azure OpenAI |
| **新興平台** | NVIDIA NIM、Together AI、Fireworks AI、Perplexity、DeepSeek、Mistral、Groq、xAI |
| **代理層** | OpenRouter、LiteLLM、Cohere、Apipie |
| **其他** | Text Generation Web UI、Novita AI、PPIO、Gitee AI、Moonshot AI、SambaNova Cloud、Minimax、Cerebras、oMLX |

### 向量資料庫（Vector Databases）

| 資料庫 | 類型 |
|--------|------|
| **LanceDB**（預設） | 本地嵌入式 |
| **PGVector** | PostgreSQL 擴充 |
| **Chroma** | 開源本地/雲端 |
| **Qdrant** | 高效能向量搜尋 |
| **Pinecone** | 雲端 managed |
| **Weaviate** | 開源/雲端 |
| **Milvus** | 企業級分散式 |
| **Zilliz** | Milvus 雲端版 |
| **Astra DB** | DataStax 雲端 |

### Embedding 模型

- AnythingLLM 原生（預設）
- OpenAI、Azure OpenAI、Google Gemini
- Ollama、LM Studio、LocalAI
- Cohere、Voyage AI、Mistral
- OpenRouter、LiteLLM
- 任何 OpenAI 相容的 embedding API

### 語音相關

| 功能 | 支援方案 |
|------|--------|
| **TTS（文字轉語音）** | 瀏覽器內建、PiperTTSLocal、OpenAI TTS、ElevenLabs |
| **STT（語音轉文字）** | 瀏覽器內建（預設） |
| **語音轉文字** | AnythingLLM 內建、OpenAI Whisper |

## 🏗 系統架構

AnythingLLM 採用 **monorepo** 架構，包含六個主要部分：

```
anything-llm/
├── frontend/          # ViteJS + React 前端
├── server/            # NodeJS Express 後端（向量DB + LLM 互動）
├── collector/         # NodeJS 文件處理服務
├── docker/            # Docker 建構指令
├── embed/             # 網站嵌入小工具（子模組）
└── browser-extension/ # Chrome 擴充功能（子模組）
```

![Architecture](https://docs.useanything.com/assets/images/architecture-overview-8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c.jpg)

### RAG 工作流程

1. **文件匯入** → 透過 collector 服務收集並解析文件
2. **文件分塊** → 文件被分割成適當大小的段落
3. **向量化** → 使用 embedding 模型轉換為向量
4. **儲存** → 存入可配置的向量資料庫
5. **查詢** → 使用者提問轉為向量，進行相似度搜尋
6. **回應** → 將相關上下文加入 LLM 提示，流式生成回應

## 🚀 部署方式

### 一鍵部署

| 平台 | 部署方式 |
|------|--------|
| **Docker** | 最常見的本地部署方式 |
| **AWS** | 雲端部署 |
| **GCP** | 雲端部署 |
| **Digital Ocean** | 雲端部署 |
| **Render.com** | 雲端部署 |
| **Railway** | 雲端部署 |
| **RepoCloud** | 雲端部署 |
| **Elestio** | 雲端部署 |
| **Northflank** | 雲端部署 |

### 桌面版本

提供 Mac、Windows、Linux 桌面應用程式，零設定即可使用。

![Desktop Download](https://github.com/Mintplex-Labs/anything-llm/blob/master/images/desktop-download.png?raw=true)

### 開發者環境

```bash
yarn setup           # 設定環境變數
yarn dev:server      # 啟動伺服器
yarn dev:frontend    # 啟動前端
yarn dev:collector   # 啟動文件收集器
```

## 🔒 隱私與資料處理

- **本地優先**：預設使用本地模型和向量資料庫（LanceDB）
- **資料不離線**：所有處理可在完全離線環境中執行
- **可選遙測**：可透過設定 `DISABLE_TELEMETRY=true` 關閉
- **權限控制**：多用戶環境下的精細權限管理

## 🔗 生態系統產品

| 產品 | 說明 |
|------|------|
| **AnythingLLM Mobile** | 手機應用程式（MIT 授權） |
| **AnythingLLM Browser Extension** | Chrome 瀏覽器擴充功能 |
| **AnythingLLM Embed** | 網站嵌入小工具 |

## 📈 社群與貢獻

- **貢獻者**：全球開發者共同維護
- **授權**：MIT License（完全開源）
- **社群**：Discord 社群活躍
- **文件**：[docs.anythingllm.com](https://docs.anythingllm.com)

![Contributors](https://contrib.rocks/image?repo=mintplex-labs/anything-llm)

## 💡 適合使用的情境

| 情境 | 說明 |
|------|------|
| **文件問答** | 上傳公司文件、手冊、論文，用自然語言查詢 |
| **研究助理** | 整合多個知識來源，輔助學術研究 |
| **內部知識庫** | 建立企業級的 AI 知識搜尋系統 |
| **自動化工作流** | 透過 Agent 和排程任務自動化日常任務 |
| **本地隱私** | 完全本地執行，資料不離開你的機器 |
| **多模型測試** | 在同一介面測試不同 LLM 的效果 |

## 🔗 參考資源

- **專案首頁**：[github.com/mintplex-labs/anything-llm](https://github.com/mintplex-labs/anything-llm)
- **官方文件**：[docs.anythingllm.com](https://docs.anythingllm.com)
- **下載桌面版**：[anythingllm.com/download](https://anythingllm.com/download)
- **Discord 社群**：[discord.gg/6UyHPeGZAC](https://discord.gg/6UyHPeGZAC)

---

*本文基於 GitHub 公開資訊整理，最後更新：2026-07-28*
