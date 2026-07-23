---
title: "Awesome LLM Apps — 100+ 開源 AI Agent 與 RAG 應用整理分析"
description: 深度分析 GitHub 最火 LLM 應用合集 Shubhamsaboo/awesome-llm-apps，涵蓋 11 大類功能的完整解析
tags: [AI, LLM, Open Source, Agent, RAG]
categories: [AI, 開源專案]
---

# Awesome LLM Apps — 100+ 開源 AI Agent 與 RAG 應用整理分析

## 📌 專案概覽

**[Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)** 是目前 GitHub 上最受關注的 LLM 應用合集之一，擁有 **126k+ Stars** 和 **18.7k Forks**。

這個專案收錄了 **100+ 個開源 AI Agent、Agent Skills 和 RAG 應用**，全部採用 Apache-2.0 授權，手寫實測通過。支援 Claude、Gemini、GPT、DeepSeek、Llama、Qwen 等主流模型。

---

## 🏗️ 專案架構 — 11 大功能分類

### 1. 🧩 Agent Skills（代理技能）
給 coding agent（Claude Code、Codex、Cursor）安裝新能力的模組：

| 技能 | 功能說明 |
|------|---------|
| ⚰️ Project Graveyard | 找出所有被遺棄的副專案，分析失敗原因並幫助完成值得繼續的 |
| 🔭 Scope Creep Detector | 檢測 diff 是否超出原定意圖，建議保留/拆分/證明 |
| 🏺 Commit Archaeologist | 從 commit 歷史重建程式碼的起源與演變 |
| 🧠 Advisor Orchestrator Worker | Claude 當顧問、GPT 當協調者、Gemini Flash 當執行者 |
| ♾️ Self-Improving Agent Skills | 用 Gemini 和 ADK 自動優化和重寫 agent 技能 |

**特色**：每項技能附帶真實程式碼，通過安全 + eval CI 檢驗，一條命令安裝。

---

### 2. 🌱 Starter AI Agents（入門級 Agent）
單一檔案 Agent，只需要 API key 即可運作，適合快速上手：

- **🎙️ AI Blog to Podcast** — 將部落格 URL 轉為播客節目
- **❤️‍🩹 AI Breakup Recovery** — Agent 團隊陪伴度過分手低谷
- **📊 AI Data Analysis** — 用自然語言問 CSV/Excel 問題
- **🩻 AI Medical Imaging** — Gemini 輔助 X 光與影像診斷分析
- **😂 AI Meme Generator** — 操控瀏覽器自動製作迷因
- **🎵 AI Music Generator** — 文字提示 → MP3 音樂產出
- **🛫 AI Travel Agent** — 個人化逐日旅遊行程
- **✨ Gemini Multimodal Agent** — 影片分析 + 網頁搜尋
- **🔄 Mixture of Agents** — 多模型回答，單一模型聚合最佳結果
- **📊 xAI Finance Agent** — Grok 即時股市分析
- **🔍 OpenAI Research Agent** — 多 Agent 主題研究
- **🕸️ Web Scraping AI Agent** — 描述要提取的內容，Agent 自動爬取

---

### 3. 🚀 Advanced AI Agents（進階 Agent）
生產級 Agent，具備工具、記憶和多步驟推理能力：

| 應用 | 功能 |
|------|------|
| 🏚️ AI Home Renovation | 上傳照片 → 裝修計畫 + 逼真渲染圖 |
| 🧠 DevPulse AI | 多 Agent 聚合技術訊號，產出每日情報摘要 |
| 🔍 AI Deep Research | 結合 OpenAI Agents SDK + Firecrawl 的深度網路研究 |
| 📊 AI VC Due Diligence | 多 Agent 創業投資分析 |
| 🤝 AI Consultant | 市場分析 + 策略建議 + 即時網路研究 |
| 🏗️ AI System Architect | DeepSeek R1 推理 + Claude 架構審查 |
| 💰 AI Financial Coach | 個人化預算、債務、儲蓄分析 |
| 🎬 AI Movie Production | 一句話概念 → 劇本 + 選角建議 |
| 📈 AI Investment Agent | Yahoo Finance 數據的個股比較報告 |
| 📡 Earnings Call Analyst | YouTube 財報電話 → 同步分析工具 |
| 🏋️ AI Health & Fitness | 客製化飲食和運動計畫 |
| 🚀 AI Product Launch | 競爭對手新品上市的情報分析 |
| 🔍 AI Fraud Investigation | 公開記錄交叉比對，標記異常設施 |
| 🗞️ AI Journalist | 研究 → 撰寫 → 編輯新聞文章 |
| 🧠 AI Mental Wellbeing | 協調 Agent 團隊提供心理健康支持 |
| 📑 AI Meeting Agent | 會前情境、產業洞察、策略簡報 |
| 🧬 AI Self-Evolving Agent | Agent 自動重寫自己的工作流程 |
| 👨‍🏫 AI Teaching Agent Team | Agent 教師團隊建立完整學習路徑 |
| 💻 Multimodal Coding Agent Team | 拍照解題 + 沙箱執行 |

---

### 4. 🛰️ Always-on Agents（長駐 Agent）
背景定時/事件驅動的 Agent：

- **📰 HN Briefing Agent** — 排程偵察員，每日整理 Hacker News 並推送到 Slack/Email
- **📡 Release Radar Agent** — 監控套件版本更新，通知 Breaking changes、安全性更新、Deprecated

---

### 5. 🤝 Multi-agent Teams（多 Agent 團隊）
多個 Agent 協作完成複雜任務：

- 🧲 **Competitor Intelligence** — 競爭對手深度解構
- 💲 **Finance Agent Team** — 20 行 Python 的金融分析團隊
- 🎨 **Game Design Agent Team** — 完整遊戲概念從設計專家群組產出
- 🧭 **AG2 Adaptive Research** — 基於 AG2 的 Agent 路由和回退機制
- 👨‍⚖️ **Legal Agent Team** — 法律研究、合約分析、策略
- 💼 **Recruitment Agent Team** — 履歷篩選到面試排程
- 🏠 **Real Estate Agent Team** — 房產搜尋、市場分析、建議
- 👨‍💼 **Services Agency (CrewAI)** — 數位代理公司規劃軟體專案
- 👨‍🏫 **Teaching Agent Team** — 完整學習路徑規劃
- 💻 **Multimodal Coding Agent Team** — 拍照解題
- 🌏 **Travel Planner Agent Team** — 完整旅行行程規劃

---

### 6. 🗣️ Voice AI Agents（語音 Agent）
即時語音 API 驅動的 Agent：

- **AI Audio Tour Agent** — 根據位置和興趣導航語音導覽
- **Customer Support Voice Agent** — 基於自有文件的語音客服
- **Insurance Claim Live Agent Team** — Gemini Live 即時理賠處理
- **Voice RAG Agent** — 提問 PDF，語音回答
- **OpenSource Voice Dictation** — 開源語音聽寫

---

### 7. 🖼️ Generative UI Agents（生成式 UI）
Agent 不僅產出文字，還能渲染互動式 UI 組件：

- 🗂️ **Chat-driven Kanban Board** — 聊天驅動任務看板
- 🪙 **Financial Coach** — 預算/儲蓄/債務以互動卡片呈現
- 📊 **Dashboard Canvas** — 聊天描述 → 即時圖表佈局
- 🛠️ **MCP App Builder** — 描述 MCP 應用 → 即時沙箱執行個體
- ✈️ **MCP Apps Showcase** — 展示 MCP 應用的互動 UI（含航班搜尋）
- 🎛️ **Shadcn Component Generator** — 聊天生成生產級 shadcn 元件
- 🔍 **Deep Research Agent** — 每個工具呼叫渲染為即時工作卡

---

### 8. 🎮 Autonomous Game-Playing Agents
Agent 端到端遊戲：

- **AI 3D Pygame Agent** — DeepSeek R1 寫 PyGame 程式碼，瀏覽器執行
- **AI Chess Agent** — Agent White vs Agent Black，驗證每一步棋
- **AI Tic-Tac-Toe Agent** — 兩個不同 LLM 逐回合對決

---

### 9. ♾️ MCP AI Agents（Model Context Protocol）
透過 MCP 連接外部工具和資料：

- 🌐 **Browser MCP Agent** — 自然語言操控真實瀏覽器
- 🐙 **GitHub MCP Agent** — 用英文探索和 analyze 任何 repo
- 📑 **Notion MCP Agent** — 終端機與 Notion 對話
- 🌍 **AI Travel Planner MCP** — 基於 Airbnb 和 Google Maps 即時數據規劃行程
- 🔀 **Multi-MCP Agent Router** — 每個 Agent 接自己的 MCP Server

---

### 10. 📀 RAG（Retrieval Augmented Generation）
從簡單 chain 到 agentic 多來源檢索管線：

- 🔥 **Agentic RAG with Gemma** — 全本地 RAG
- 🧐 **Agentic RAG with Reasoning** — 觀察 Agent 逐步推理
- 📰 **AI Blog Search (RAG)** — LangGraph 上的部落格內容搜尋
- 🔄 **Contextual AI RAG** — 託管式 RAG 服務
- 📎 **Typed Agentic RAG with Pydantic AI** — 驗證答案 + 精確引用
- 🧬 **Multimodal Agentic RAG** — 文字/PDF/圖片/音訊/影片 + 引用
- 🖼️ **Vision RAG** — 基於 Embed-4 的圖片和 PDF 提問
- 🕸️ **Knowledge Graph RAG** — 多跳答案 + 來源歸屬驗證

---

### 11. 💾 LLM Apps with Memory
跨 session 保持記憶的 Agent 和 Chatbot：

- 💾 **AI ArXiv Agent with Memory** — 記住研究興趣的論文搜尋
- 🛩️ **AI Travel Agent with Memory** — 記住偏好的旅行助手
- 💬 **Llama3 Stateful Chat** — Llama 3 會話持久化聊天
- 📝 **LLM App with Personalized Memory** — 跨對話保持上下文
- 🗄️ **Local ChatGPT Clone with Memory** — 完全本地化，每用戶記憶
- 🧠 **Multi-LLM with Shared Memory** — 不同模型共享對話記憶

---

### 📦 其他分類

**💬 Chat with X** — 把任何資料來源變成對話介面（GitHub、Gmail、PDF、ArXiv、Substack、YouTube）

**🎯 LLM Optimization Tools** — 降低 token 使用和 API 成本（TOON 格式省 30-60%，Context Optimization 省 50-90%）

**🔧 LLM Fine-tuning** — 開源模型微調指南（Gemma 3 LoRA、Llama 3.2 微調）

**🧑‍🏫 AI Agent Framework Crash Courses** — Google ADK 和 OpenAI Agents SDK 的深入教學

---

## 📊 技術特點總覽

| 面向 | 特色 |
|------|------|
| **授權** | Apache-2.0，可商用 |
| **模型支援** | Claude、Gemini、GPT、DeepSeek、Llama、Qwen 等 |
| **安裝方式** | `npx skills add` 或 `git clone` + `pip install` |
| **測試** | 全部手寫實測通過，有 eval CI |
| **更新頻率** | 每週新增模板 |
| **Star 數** | 126k+ |
| **Fork 數** | 18.7k |
| **提交數** | 1,127+ |

## 💡 總結

這個專案是當前 LLM 應用開發最全面的開源資源庫之一，從入門級的單一檔案 Agent 到生產級的多 Agent 系統一應俱全。特別適合想要快速上手 LLM 應用開發的開發者，以及想要了解最新 AI Agent 架構趨勢的研究者。

> ⭐ [Star 原專案](https://github.com/Shubhamsaboo/awesome-llm-apps) 以獲取最新模板更新
