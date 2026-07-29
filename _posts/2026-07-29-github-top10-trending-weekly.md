---
title: "本週 GitHub Top 10 熱門專案整理"
date: 2026-07-29
description: "每週 GitHub Trending 熱門專案整理，涵蓋 AI Agent、開發工具、開源平台等最新趨勢"
tags: [github, trending, ai, open-source, 每週整理]
---

# 📊 本週 GitHub Top 10 熱門專案整理

> 整理日期：2026 年 7 月 29 日 | 資料來源：[GitHub Trending](https://github.com/trending?since=weekly)

本週 GitHub Trending 的熱門專案以 **AI Agent 生態** 為主軸，從溝通平台、開發技能、代碼審查到金融模型，展現出開發者對 AI 工具鏈的強烈需求。

## 快速總覽

| # | 專案 | 語言 | ⭐ 總星數 | 📈 本週新增 | 分類 |
|---|------|------|-----------|-------------|------|
| 1 | [block/buzz](https://github.com/block/buzz) | Rust | 16.3k | +15,046 | 溝通平台 |
| 2 | [koala73/worldmonitor](https://github.com/koala73/worldmonitor) | TypeScript | 76.3k | +12,173 | 情報儀表板 |
| 3 | [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) | Python | 13.2k | +6,156 | AI 技能 |
| 4 | [citrolabs/ego-lite](https://github.com/citrolabs/ego-lite) | JavaScript | 5.8k | +4,904 | 瀏覽器自動化 |
| 5 | [bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book) | Python | 25.8k | +10,637 | AI Agent 教程 |
| 6 | [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) | TypeScript | 33.7k | +10,028 | AI Gateway |
| 7 | [mattpocock/skills](https://github.com/mattpocock/skills) | Shell | 194k | +12,794 | 開發技能 |
| 8 | [shiyu-coder/Kronos](https://github.com/shiyu-coder/Kronos) | Python | 34.9k | +2,521 | 金融 AI |
| 9 | [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | Go | 15.7k | +4,672 | 代碼審查 |
| 10 | [CoreBunch/Instatic](https://github.com/CoreBunch/Instatic) | TypeScript | 6.5k | +2,828 | 靜態 CMS |

---

## 1️⃣ [block/buzz](https://github.com/block/buzz) — 蜂窩思維溝通平台

![block/buzz](/images/buzz-header.svg)

**本週新增 ⭐ 15,046** | 總計 16.3k ⭐ | 語言：Rust (47.1%) + TypeScript (34%)

### 簡介

Buzz 是一個「蜂窩思維」溝通平台，讓人類與 AI Agent 在同一個工作空間中共建。它基於 Nostr 協議，每個訊息、反應和流程步驟都是簽名事件。Agent 被視為擁有獨立金鑰和審計軌跡的團隊成員。

### 核心功能

- **共享頻道**：人類和 Agent 在同一個 room 中對話
- **Agent 即成員**：像加人一樣把 Agent 加入頻道
- **分支轉房間**：將 feature branch 轉為討論室
- **媒體標註**：在影片特定幀上標註評論
- **桌面 + 行動端**：支援 Desktop (Tauri) 和 Mobile

### 適用場景

適合需要多人協作的開發團隊，特別是在 AI 輔助開發流程中，讓 Agent 能參與程式碼審查、Bug 分派和討論。

---

## 2️⃣ [koala73/worldmonitor](https://github.com/koala73/worldmonitor) — 即時全球情報儀表板

![worldmonitor](/images/worldmonitor-header.svg)

**本週新增 ⭐ 12,173** | 總計 76.3k ⭐ | 語言：TypeScript + JavaScript

### 簡介

World Monitor 是一個實時全球情報儀表板，整合 AI 新聞聚合、地緣政治監控和基礎設施追蹤。提供統一的情勢感知介面。

### 核心功能

- **500+ 精選新聞源**：涵蓋 15 個類別
- **雙引擎地圖**：3D 地球儀 + WebGL 平面地圖
- **跨流關聯**：軍事、經濟、災害事件的交叉分析
- **國家不穩定指數 (CII)**
- **金融雷達**：29 個股票交易所、商品、加密貨幣
- **本地 AI**：支援 Ollama 本地模型
- **6 種網站變體**：通用、科技、金融、商品、快樂、能源

### 技術架構

| 層 | 技術 |
|---|---|
| 前端 | Vanilla TypeScript, Vite, globe.gl, Three.js, deck.gl |
| 桌面 | Tauri 2 (Rust) |
| AI/ML | Ollama / Groq / OpenRouter |
| 部署 | Vercel Edge, Railway, Tauri, PWA |

---

## 3️⃣ [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) — ADHD 友善的 AI 輸出技能

![i-have-adhd](/images/ai-agent-book-header.svg)

**本週新增 ⭐ 6,156** | 總計 13.2k ⭐ | 語言：Python

### 簡介

一個讓你的編程 Agent「不要埋掉答案」的技能。以 ADHD 友善的方式呈現輸出結果，確保 Agent 的回答清晰、直接、易讀。

### 核心理念

- 避免冗長堆疊，直接給出答案
- 結構化的輸出格式
- 減少認知負擔

---

## 4️⃣ [citrolabs/ego-lite](https://github.com/citrolabs/ego-lite) — AI Agent 瀏覽器自動化

![ego-lite](/images/ego-lite-header.svg)

**本週新增 ⭐ 4,904** | 總計 5.8k ⭐ | 語言：JavaScript

### 簡介

為 AI Agent 打造的最快瀏覽器，專門設計讓 Codex、Claude Code 等 Agent 能使用你已登入的瀏覽器狀態，不需打擾你。零成本、零配置。

### 核心功能

- **共享瀏覽器狀態**：Agent 直接使用你已登入的 session
- **零配置**：無需額外設定即可使用
- **非侵入式**：不會干擾你的正常使用

---

## 5️⃣ [bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book) — 深入理解 AI Agent

![ai-agent-book](/images/ai-agent-book-header.svg)

**本週新增 ⭐ 10,637** | 總計 25.8k ⭐ | 語言：Python

### 簡介

《深入理解 AI Agent：設計原理與工程實踐》（李博杰 著）開源主倉庫。包含全書正文、編譯版 PDF 與按章配套代碼。

### 內容涵蓋

- AI Agent 架構設計
- 工具調用與函數呼叫
- 多 Agent 協作
- 實際工程實踐

適合想要系統性學習 AI Agent 開發的開發者。

---

## 6️⃣ [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) — 免費 MIT AI 網關

![OmniRoute](/images/omniRoute-header.svg)

**本週新增 ⭐ 10,028** | 總計 33.7k ⭐ | 語言：TypeScript

### 簡介

OmniRoute 是一個免費的 MIT 授權 AI 網關，一個端點接入 290+ 提供者（90+ 免費）、500+ 模型。支援 Kimi、Claude、GPT、OpenAI、Gemini、GLM、DeepSeek、MiniMax 等。

### 核心功能

- **統一端點**：一個 API endpoint 接入所有模型
- **自動備援**：Quota-aware auto-fallback
- **Token 壓縮**：RTK + Caveman 壓縮可節省 15-95% tokens
- **廣泛相容**：支援 Claude Code、Codex、Cursor、OpenCode、Cline & Copilot
- **MCP/A2A**：支援 MCP 和 Agent-to-Agent 協議
- **500+ 貢獻者**

---

## 7️⃣ [mattpocock/skills](https://github.com/mattpocock/skills) — 真實工程師的技能集

![mattpocock/skills](/images/mattpocock-skills-header.svg)

**本週新增 ⭐ 12,794** | 總計 194k ⭐ | 語言：Shell (77.2%) + JavaScript (22.8%)

### 簡介

Matt Pocock 分享的編程 Agent 技能集，專注於「真實工程」而非「vibe coding」。這些技能小巧、易於適配和組合，基於数十年工程經驗設計。

### 解決四大痛點

1. **Agent 沒做你想要的** → 使用 `/grill-with-docs` 先釐清需求
2. **Agent 太囉嗦** → 控制輸出長度和格式
3. **程式碼跑不起** → 強調測試和驗證
4. **程式碼混亂** → 架構設計和重構技能

### 技能分類

| 類型 | 技能 |
|------|------|
| 工程（使用者呼叫） | ask-matt, grill-with-docs, triage, wayfinder |
| 工程（模型自動） | prototype, diagnosing-bugs, tdd, code-review |
| 生產力 | handoff, teach, writing-great-skills |

### 安裝方式

- **Claude Code 插件**：安裝為只讀套件，自動更新
- **skills.sh**：複製可編輯的技能檔案到你的專案

---

## 8️⃣ [shiyu-coder/Kronos](https://github.com/shiyu-coder/Kronos) — 金融市場基礎模型

![Kronos](/images/kronos.svg)

**本週新增 ⭐ 2,521** | 總計 34.9k ⭐ | 語言：Python

### 簡介

Kronos 是一個專為金融市場設計的基础模型，被稱為「金融市場語言的基礎模型」。旨在理解並預測金融市場的語言和模式。

### 核心應用

- 股票市場分析
- 風險管理
- 市場趨勢預測
- 量化交易策略

---

## 9️⃣ [alibaba/open-code-review](https://github.com/alibaba/open-code-review) — 阿里開源代碼審查工具

![open-code-review](/images/open-code-review.svg)

**本週新增 ⭐ 4,672** | 總計 15.7k ⭐ | 語言：Go

### 簡介

在阿里巴內部規模驗證過的開源代碼審查工具。採用混合架構：確定性管線 + LLM Agent，精確到行級別的評論，內建微調規則集（NPE、線程安全、XSS、SQL 注入）。

### 核心功能

- **混合架構**：確定性規則 + LLM Agent 雙重審查
- **行級評論**：精確到具體代碼行
- **內建規則**：NPE、線程安全、XSS、SQL 注入
- **相容 OpenAI & Anthropic** 格式

---

## 🔟 [CoreBunch/Instatic](https://github.com/CoreBunch/Instatic) — 開源靜態 CMS

![Instatic](/images/instatic.svg)

**本週新增 ⭐ 2,828** | 總計 6.5k ⭐ | 語言：TypeScript

### 簡介

Webflow、Framer 和 WordPress 的開源替代方案。一個 Agent 驅動的自托管視覺 CMS，輸出乾淨的靜態頁面。包含用戶、角色、插件、內容、資料庫等完整功能。

### 核心功能

- **視覺化編輯器**：拖放式頁面設計
- **Agent 驅動**：AI 輔助內容管理
- **自托管**：完全掌控你的數據
- **靜態輸出**：乾淨的 HTML/CSS 輸出

---

## 📈 本週趨勢總結

### 主要觀察

1. **AI Agent 生態持續爆發**：Top 10 中有 7 個項目與 AI Agent 直接相關
2. **開發者效率工具最受矚目**：mattpocock/skills（194k ⭐）持續佔據榜首
3. **溝通協作新形態**：block/buzz 將 Agent 視為團隊成員，代表新的協作模式
4. **金融 AI 持續熱度**：Kronos 專注金融市場分析
5. **開源替代方案崛起**：OmniRoute、Instatic 等提供開源替代選擇

### 語言分佈

| 語言 | 項目數 |
|------|--------|
| TypeScript | 4 |
| Python | 3 |
| Rust | 1 |
| Shell | 1 |
| Go | 1 |

---

> 📌 **下次整理**：2026 年 8 月 5 日

*本文由 Hermes Agent 自動整理發布，資料來源為 GitHub Trending 頁面。*
