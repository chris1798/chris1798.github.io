---
title: 本週 GitHub Trending 熱門項目分析（2025/07）
date: 2025-07-18
categories:
  - 開源專案
  - 週報
tags:
  - GitHub Trending
  - AI
  - 開源
  - 工具推薦
---

## 本週 GitHub Trending 熱門項目分析（2025/07）

本週 GitHub Trending 呈現一個非常清晰的趨勢：**AI Agent 生態系全面爆發**。從 Coding Skills、MCP Server、平行 Agent 編排、到 AI 自動交易，前 25 名中有超過一半與 AI Agent 直接相關。以下逐一分析本週最受矚目的開源專案。

---

## 🏆 TOP 5 本週新增 Star 最多的專案

### 1. OpenCut — 開源 CapCut 替代品
- **⭐ 總 Stars**: 75,276 | **本週新增**: +12,718
- **語言**: TypeScript
- **GitHub**: [OpenCut-app/OpenCut](https://github.com/OpenCut-app/OpenCut)
- **網站**: [opencut.app](https://opencut.app/)

**分析**: OpenCut 是本週最爆紅的專案，定位為「開源版的 CapCut」。這是一款跨平台（Web/桌面/行動）的影片編輯器，MIT 授權，專注於快速剪輯、修剪和簡單敘事，而非重量級 VFX。

**亮點**:
- 使用者介面設計上手即可使用：時間軸、預覽、素材庫一目了然
- MIT 授權確保永遠不會被鎖定
- 隱私優先，所有處理在本地完成
- 對比 CapCut 日益增加的付費牆，OpenCut 提供真正的免費替代方案

**評價**: 在影片創作民主化的浪潮中，OpenCut 填補了「開源 + 易上手 + 跨平台」的空白。7.5 萬 Star 證明市場對免費影片編輯器的需求極為巨大。

---

### 2. mattpocock/skills — 工程師的 Agent Skills 合集
- **⭐ 總 Stars**: 176,247 | **本週新增**: +11,325
- **GitHub**: [mattpocock/skills](https://github.com/mattpocock/skills)

**分析**: 這是來自知名開發者 Matt Pocock 的個人 `.agents` 目錄中的 Skills 合集，專為 AI 編程助手（Codex、Cursor、Claude Code）設計。已突破 17.6 萬 Star，是 GitHub 上 Star 數最多的 Skills 類專案。

**亮點**:
- 真實工程師實戰經驗萃取的技能包
- 直接可用於 Claude Code、Cursor、Codex 等 AI 編程工具
- 涵蓋前端、後端、DevOps 等多領域最佳實踐
- 代表了一種新趨勢：開發者將自己的知識沉澱為 Agent 可執行的 Skills

**評價**: 這不只是工具集，更是「人類經驗 → Agent 能力」的典範。17.6 萬 Star 顯示 AI 編程助手生態已經成熟到需要專業 Skill 庫的程度。

---

### 3. hallmark — 反 AI 醜陋設計 Skill
- **⭐ 總 Stars**: 12,628 | **本週新增**: +8,075
- **GitHub**: [Nutlope/hallmark](https://github.com/Nutlope/hallmark)

**分析**: Hallmark 是一個專門為 Claude Code、Cursor 和 Codex 設計的反「AI 醜陋風格」設計技能包。核心理念是「拒絕看起來像 AI 生成的通用設計」。

**亮點**:
- 內建 20 種主題 × 4 種風格，按 T 鍵即可切換
- 由 Together AI 團隊製作
- 為 AI 生成的 UI 注入人性化設計感
- 解決了 AI 編程工具生成介面千篇一律的痛點

**評價**: 這反映了 AI 編程生態中的一個真實痛點 — AI 生成的 UI 缺乏個性。Hallmark 在一週內獲得 8,000+ Star，說明這個需求是真實且迫切的。

---

### 4. awesome-llm-apps — 100+ 可實際運行的 AI Agent 應用
- **⭐ 總 Stars**: 123,862 | **本週新增**: +6,252
- **GitHub**: [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)

**分析**: 這個倉庫收集了 100+ 個可以實際 Clone 下來運行的 AI Agent 和 RAG 應用，不是概念演示而是真正可執行的專案。

**亮點**:
- 12.3 萬 Star 的超級熱門倉庫
- 涵蓋 RAG、Agent、多模態等各種 AI 應用場景
- 每個專案都可以直接 Clone 使用
- 本週持續穩定增長 6,252 Star

**評價**: 從「AI Demo」到「實際可用」的過渡階段中，這個倉庫是最重要的資源之一。

---

### 5. Vibe-Trading — AI 個人交易代理
- **⭐ 總 Stars**: 24,871 | **本週新增**: +5,616
- **GitHub**: [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading)

**分析**: 由香港大學 HKUDS 團隊開發的 AI 個人交易代理，支援自然語言研究、回測、策略生成一站式交易研究。

**亮點**:
- 自然語言指令即可進行交易研究
  ```bash
  # 回測 BTC-USDT 20/50 移動平均線策略
  vibe-trading run -p "Backtest a BTC-USDT 20/50 moving-average strategy for 2024"
  # 預建 Alpha 策略庫基準測試
  vibe-trading alpha bench --zoo gtja191 --universe csi300
  ```
- Shadow Account 功能：上傳券商交易記錄，AI 分析你的交易行為並提取「影子策略」
- 支援 MCP 工具整合
- 一行命令完成策略回測 + 報告輸出

**評價**: 將 AI Agent 帶入金融交易領域的先驅之一。自然語言 → 策略 → 回測 → 報告的完整流程，對個人投資者極具吸引力。

---

## 🔥 其他值得關注的熱門專案

### 6. Orca — 平行 Agent 開發環境 (ADE)
- **⭐ 總 Stars**: 21,585 | **本週新增**: +5,409
- **GitHub**: [stablyai/orca](https://github.com/stablyai/orca)

**分析**: Orca 是新一代 Agent Development Environment (ADE)，讓你可以同時運行多個平行 AI 編程 Agent（Claude Code、Codex、Cursor、Pi、Grok 等 20+），使用你自己的 API 訂閱。

**核心功能**:
- 支援 Claude Code、Codex CLI、OpenCode、Pi、Grok 等 20+ Agent
- 在平行 git worktrees 中同時運行多個 Agent
- 原生 TUI + 檔案查看器
- 內建 Design Mode
- 行動 App 支援
- GitHub → Agent 任務追蹤
- 使用你自己的 API Key，不綁定特定供應商

---

### 7. OfficeCLI — AI Agent 的 Office 套件
- **⭐ 總 Stars**: 19,149 | **本週新增**: +4,611
- **GitHub**: [iOfficeAI/OfficeCLI](https://github.com/iOfficeAI/OfficeCLI)

**分析**: 第一個專為 AI Agent 設計的 Office 套件 — 讓 AI 編程助手可以直接讀取、編輯和自動化 Word、Excel、PowerPoint 文件。**單一執行檔，不需要安裝 Microsoft Office**。

**核心功能**:
- C# 開發，單一執行檔
- 支援 .docx、.xlsx、.pptx 完整編輯
- 內建 MCP Server，AI Agent 直接整合
- 即時 HTML 預覽 + 自動刷新
- 文件审阅註釋支援
- 外掛系統：可扩展 .doc、.hwpx、.pdf 匯出等

---

### 8. Graphify — 程式碼知識圖譜
- **⭐ 總 Stars**: 90,691 | **本週新增**: 持續高增長
- **GitHub**: [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)

**分析**: 在 AI 編程助手中輸入 `/graphify`，即可將整個專案資料夾（程式碼、SQL 架構、文件、PDF、圖片、影片）轉換為可查詢的知識圖譜。

**亮點**:
- 9 萬 Star 的熱門專案
- 支援 Claude Code、Codex、OpenCode、Cursor、Gemini CLI
- 程式碼使用 tree-sitter 本地解析（決定性、無需 LLM、不離開本機）
- 文件、PDF、圖片、影片使用語義索引
- 取代傳統的 grep 搜尋

---

### 9. OpenInterpreter — 開源模型的編程 Agent
- **⭐ 總 Stars**: 66,605 | **本週新增**: +2,009
- **GitHub**: [openinterpreter/openinterpreter](https://github.com/openinterpreter/openinterpreter)

**分析**: 一個支援開源模型（如 Kimi K3）的編程 Agent，讓你可以用開源 LLM 運行類 Cursor/Claude Code 的編程代理體驗。

---

### 10. OpenAI Codex CLI — 終端機編程 Agent
- **⭐ 總 Stars**: 99,320 | **本週新增**: +2,250
- **GitHub**: [openai/codex](https://github.com/openai/codex)

**分析**: OpenAI 官方推出的輕量級終端機編程 Agent，已經接近 10 萬 Star。

---

### 11. DesktopCommanderMCP — Claude 桌面控制 MCP Server
- **⭐ 總 Stars**: 8,484 | **本週新增**: +1,657
- **GitHub**: [wonderwhy-er/DesktopCommanderMCP](https://github.com/wonderwhy-er/DesktopCommanderMCP)

**分析**: 讓 Claude 獲得終端控制、檔案系統搜尋和 diff 檔案編輯能力的 MCP Server。支援命令黑白名單和路徑驗證。

---

### 12. DeepTutor — 終身個性化 AI 家教
- **⭐ 總 Stars**: 27,594 | **本週新增**: +1,801
- **GitHub**: [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor)

**分析**: 同樣來自 HKUDS 團隊，定位為「終身個性化教學」系統。

---

### 13. Cangjie Skill — 把內容蒸餾為 Agent Skills
- **⭐ 總 Stars**: 3,618 | **本週新增**: +1,158
- **GitHub**: [kangarooking/cangjie-skill](https://github.com/kangarooking/cangjie-skill)

**分析**: 將書、長影片、播客等高價值內容蒸餾為可執行的 Agent Skills。使用 RIA-TV++ 流水線，分多個階段將原始文字轉化為結構化 Skill。

**理念**: 「現有的閱讀方法論都是給人的，不是給 Agent 用的 — 需要面向執行而非面向消費的蒸餾方法。」

---

### 14. ui-skills — 設計工程師的 Skills
- **⭐ 總 Stars**: 4,780 | **本週新增**: +974
- **GitHub**: [ibelick/ui-skills](https://github.com/ibelick/ui-skills)

**分析**: 專為設計工程師打造的 UI 相關 Skills 合集。

---

### 15. Abseil C++ — Google 開源 C++ 函式庫
- **⭐ 總 Stars**: 17,971 | **本週新增**: +608
- **GitHub**: [abseil/abseil-cpp](https://github.com/abseil/abseil-cpp)

**分析**: Google 的 Abseil Common Libraries (C++)，本週穩健增長。

---

## 📊 本週趨勢總結

### 三大關鍵趨勢

#### 1. AI Agent Skill 生態系正式成型 🤖

本週最明顯的趨勢是 **AI Agent Skills** 成為獨立品類。從 mattpocock/skills（17.6 萬 Star）、hallmark（1.2 萬 Star）、cangjie-skill、ui-skills 到 Graphify，都代表了同一個方向：

> **人類知識 → 結構化 Skill → Agent 可直接執行**

這標誌著 AI 編程助手從「通用對話」進入「專業技能」時代。

#### 2. MCP 協議成為 AI 工具整合標準 🔌

DesktopCommanderMCP、OfficeCLI 的 MCP Server 整合、Graphify 的多 Agent 相容性，都顯示 **Model Context Protocol (MCP)** 正在成為連接 AI Agent 與外部工具的標準協議。

#### 3. 平行 Agent 編排成為新戰場 🚀

Orca 的崛起（5,400+ Star/週）顯示開發者開始需要同時管理多個 AI Agent 的工具。從單一 Agent 到 Agent Fleet 的管理，是下一代開發工具的關鍵差異。

### 非 AI 亮點

- **OpenCut** 作為唯一非 AI 類的 Top 5 專案，證明開源影片編輯器市場需求巨大
- **OfficeCLI** 雖然服務 AI Agent，但解決的是真實的 Office 文件自動化痛點

### 數據速覽

| 排名 | 專案 | 總 Stars | 本週新增 | 類別 |
|------|------|---------|---------|------|
| 1 | OpenCut | 75,276 | +12,718 | 影片編輯 |
| 2 | mattpocock/skills | 176,247 | +11,325 | Agent Skill |
| 3 | hallmark | 12,628 | +8,075 | Agent Skill |
| 4 | awesome-llm-apps | 123,862 | +6,252 | AI 合集 |
| 5 | Vibe-Trading | 24,871 | +5,616 | AI 交易 |
| 6 | Orca | 21,585 | +5,409 | Agent ADE |
| 7 | OfficeCLI | 19,149 | +4,611 | AI Office |
| 8 | OpenAI Codex | 99,320 | +2,250 | AI Agent |
| 9 | OpenInterpreter | 66,605 | +2,009 | AI Agent |
| 10 | DeepTutor | 27,594 | +1,801 | AI 教育 |

---

> *本文基於 2025 年 7 月 GitHub Trending 週榜數據整理。所有 Star 數為截圖時刻數據，實際數字可能略有變化。*
