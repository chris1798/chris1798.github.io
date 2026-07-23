---
title: "Tabbit AI 原生瀏覽器 — 功能解析與使用場景"
description: 深入解析美團旗下 Tabbit AI 瀏覽器：內建 Agent、Skills、MCP，10+ 頂級模型隨呼隨到
tags: [AI, Browser, Agent, Tabbit, Meituan]
categories: [AI, 工具推薦]
---

# Tabbit AI 原生瀏覽器 — 功能解析與使用場景

## 📌 專案概覽

**Tabbit** 是美團旗下 GN06 團隊開發的新一代 **AI 原生瀏覽器**，2026 年 6 月正式推出 1.0 版本，由新加坡註冊公司 **Lumina Lab** 營運。

| 指標 | 數值 |
|------|------|
| 月活用戶 | 853 萬（截至 2026-06） |
| 支援平台 | macOS 12+（Apple Silicon / Intel）、Windows 10+ |
| 支援模型 | 10+ 頂級模型 |
| Agent Skills | 2000+（覆蓋前 100 常用網站） |
| Agent 任務成功率 | 91.8% |

**下載**：[https://www.tabbit.ai/](https://www.tabbit.ai/)

---

## 🏗️ 核心架構理念

Tabbit 與「傳統瀏覽器 + AI 側邊欄」的疊加邏輯不同，它從底層就將 **大模型問答、搜尋、Agent 自動化** 打包進原生操作環境。

```
WHATEVER YOU BRING IN          WHAT TABBIT HARNESSES
─────────────────────          ─────────────────────────
Pages                          Site MCPs
Screenshots                    Skills
Highlights                     Top models
Local files                    Agent Memory
```

---

## 🎯 核心功能

### 1. 多模態上下文理解（@ Anything）

Tabbit 的 Agent 可以讀取和理解各種上下文：

- **@tab** — 引用當前或特定標籤頁內容
- **@file** — 引用本地文件（PDF、圖片、Excel）
- **@highlight** — 引用你標記的網頁段落
- **@screenshot** — 引用螢幕截圖
- **@bookmark** — 引用書籤

**使用方式**：在對話框中輸入 `@` 即可呼叫對應資源，Agent 會讀取、規劃並執行。

---

### 2. 多 Agent 協作系統（Multi-Agent + Skills）

Tabbit 內建四個專職 Agent：

| Agent | 職責 |
|-------|------|
| 📚 Research | 閱讀論文、網頁研究 |
| 🕹️ Operator | 操作網頁、執行爬蟲 |
| ✍️ Writer | 撰寫文章、報告 |
| 📊 Analyst | 數據分析、統計 |

每個 Agent 根據任務自動載入對應的 **Skills**（技能模組），例如 Research Agent 載入「論文解析 Skill」，Operator Agent 載入「網站 MCP」。

---

### 3. Site MCPs（網站級模型上下文協議）

Tabbit 為常用網站建立專屬的 **MCP（Model Context Protocol）**，讓 Agent 能真正操作網站而非只是「看」：

- **YouTube** — 整理影片清單、提取字幕、挖掘真實評論
- **GitHub** — 探索 Repo、分析程式碼、追蹤 Issues
- **Gmail** — 搜尋郵件、整理收件匣、自動回覆
- **Reddit** — 挖掘高質討論、過濾噪音
- **Substack** — 訂閱管理、重點提取
- **Bilibili** — 影片推薦、內容整理

---

### 4. 2000+ Agentic Skills（妙招廣場）

Tabbit 提供大量預置的 **Agent Skills**，覆蓋前 100 個常用網站：

**YouTube Skills 範例**：
| Skill | 功能 |
|-------|------|
| `@feed-trim` | 從 47 則上傳中篩選 3 支值得看的影片，按你實際看完的影片排序 |
| `@longform-co` | 從 2 小時 Podcast 中提取所有引用、時間戳、書籍推薦 |
| `@discourse-mine` | 找出影片下方的實質性討論，跳過熱門但無意義的留言 |
| `@kb-drop` | 將影片存到 Notion / Obsidian，附 TLDR + 完整字幕 |

**其他 Skills**：
- 論文快速摘要
- 新聞來源比對
- 電商價格追蹤
- 社媒內容排程

---

### 5. 內建 10+ 頂級模型（Day One）

Tabbit 承諾新模型發布 **12 小時內** 上線：

- GPT-5.6
- Claude 4.8
- Gemini 3.1 Pro
- Grok 4.3
- DeepSeek V4
- Kimi K3
- GLM 5.2
- Doubao Seed 1.9
- Qwen 3.7
- MiniMax M3

用戶可在對話框上方隨時切換模型，確認自己的 Prompt 送往哪個供應商。

---

### 6. Agent 自動化操作

Tabbit 的 Agent 不只「回答」，還能真正「執行」：

- ✅ 操作網頁（填表、點擊、導航）
- ✅ 生成 PDF / PPT / Excel / Word
- ✅ 爬蟲抓取特定資料
- ✅ 跨網頁整合資訊
- ✅ 自動整理標籤頁

---

### 7. 智慧標籤管理

- 自動分組標籤頁
- 標記「已關閉標籤」可隨時喚回
- 按主題、專案自動整理
- AI 建議關閉不再需要的標籤

---

### 8. 寫作助手

- 閱讀網頁後協助撰寫筆記
- 多語言翻譯與潤飾
- 生成結構化報告

---

## 💡 使用場景

### 場景 1：研究與學習

**任務**：快速了解某個主題的學術研究

1. 輸入：「幫我整理 2026 年大語言模型推理能力的最新論文」
2. Research Agent 自動搜尋 arXiv、Hugging Face、Google Scholar
3. 載入「Papers Skill」解析每篇論文
4. 產出：論文摘要、關鍵發現、對比表格、引用連結

---

### 場景 2：旅行規劃

**任務**：2000 美元預算規劃東京自由行

1. 輸入：「Plan a Tokyo solo trip on $2k」
2. Agent 讀取你的偏好（從歷史對話）
3. Operator Agent 操作訂票網站查詢航班
4. Writer Agent 產出逐日行程 + 預算分配 PDF
5. Analyst Agent 優化路線與花費

---

### 場景 3：Podcast / 內容製作

**任務**：從海量內容中篩選節目素材

1. `@feed-trim` — 從 YouTube 訂閱清單中篩選值得看的影片
2. `@longform-co` — 從 Podcast 提取所有引用和時間戳
3. `@kb-drop` — 將素材存到 Obsidian 知識庫
4. Writer Agent 協助撰寫節目腳本

> 使用者「劉飛」（播客主持人）表示：「每集播客前需要篩選近百萬字內容，Tabbit 是目前最有效的解決方案。」

---

### 場景 4：電商購物決策

**任務**：比較筆電規格與價格

1. 在 Amazon、Best Buy、蝦皮等頁面間切換
2. `@tab1 @tab2 @tab3` — 引用多個商品頁面
3. Agent 自動比較規格、價格、評價
4. 產出：對比表格 + 購買建議

---

### 場景 5：程式開發輔助

**任務**：探索開源專案並提取關鍵資訊

1. 載入 GitHub Repo 頁面
2. 使用 GitHub Skill 分析專案結構
3. Agent 提取 API 文件、依賴、最佳實踐
4. 產出：專案摘要報告

---

### 場景 6：日常資訊整理

**任務**：整理閱讀內容到筆記軟體

1. 標記網頁重點段落
2. `@highlight` — 引用標記內容
3. Writer Agent 產出摘要
4. `@kb-drop` — 同步到 Notion / Obsidian

---

## 🆚 與其他 AI 瀏覽器對比

| 功能 | Tabbit | Arc | Chrome AI | Perplexity |
|------|--------|-----|-----------|------------|
| AI 原生架構 | ✅ | ❌ | ❌ | ❌ |
| 多 Agent 系統 | ✅ | ❌ | ❌ | 部分 |
| Agent Skills | 2000+ | ❌ | ❌ | ❌ |
| Site MCPs | ✅ | ❌ | ❌ | ❌ |
| 模型選擇 | 10+ | 單一 | 單一 | 單一 |
| 本地資料加密 | ✅ | ✅ | ❌ | ❌ |
| 網頁操作能力 | ✅ | ❌ | ❌ | ❌ |
| 永久免費功能 | ✅ | ❌ | 部分 | ❌ |

---

## 🔒 隱私與資料保護

| 面向 | 做法 |
|------|------|
| 本地資料 | 歷史、書籤、標記、對話加密於你的設備 |
| 同步 | 使用新加坡/當地合規雲端供應商 |
| Prompt 去向 | 僅送往你選擇的模型供應商 |
| 數據出售 | ❌ 不販售用戶數據 |
| 模型訓練 | ❌ 不用用戶數據訓練模型 |
| 內容過濾 | ❌ 不決定你看到什麼 |

---

## 💰 定價

| 方案 | 價格 | 內容 |
|------|------|------|
| Trial | 免費 | 每週重置的 AI 額度 |
| Standard | 免費 | 設為預設瀏覽器解鎖 10 倍額度 |
| Pro | 付費 | 頂級模型 + 高頻 Agent 調用 |

> **永久免費**：基礎對話、網頁閱讀、常用 Skills 永久免費。

---

## 📊 用戶評價

> 「Tabbit has become my default browser.」  
> — Kassadin，CEO, VR Media

> 「Creating a podcast requires me to sift through nearly a million words of content before each episode... Tabbit is currently my most effective solution.」  
> — 劉飛，播客主持人

> 「This is, without a doubt, the best browser I've encountered among all AI-native browsers when it comes to integrating artificial intelligence capabilities.」  
> — 楊明輝，Founder, Bodhi Cat

> 「Since I started using Tabbit, web pages have become increasingly clear, especially with its smart organization and word explanation features.」  
> — Sam Carter，Independent AI Creator

---

## 🚀 總結

Tabbit 是目前 AI 原生瀏覽器領域最成熟的產品之一，特色包括：

1. **真正 AI 原生** — 不是側邊欄插件，而是從底層整合
2. **多 Agent + Skills 生態** — 2000+ 技能覆蓋日常場景
3. **Site MCPs** — 真正操作網站，不只能看
4. **10+ 頂級模型隨選** — 新模型 12 小時內上線
5. **隱私優先** — 本地加密、不賣數據、不訓練模型
6. **核心功能永久免費** — 降低使用門檻

> ⭐ [下載 Tabbit](https://www.tabbit.ai/) | [快速入門](https://www.tabbit.ai/quick-start)
