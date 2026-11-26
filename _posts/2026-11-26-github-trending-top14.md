---
title: "本週 GitHub 熱門項目整理（2026-11-26）"
date: 2026-11-26
description: "2026 年第 47 週 GitHub Trending 榜單：14 個專案深度整理，涵蓋 AI Agent 技能、瀏覽器自動化、代碼審查與金融應用。"
tags: [github, trending, agent, mcp]
---

# 本週 GitHub 熱門項目整理（2026-11-26）

資料來源：GitHub Trending（`https://github.com/trending?since=weekly`），星數與 fork 數皆為頁面即時數據。本週榜單共 **14 個專案**，全部收錄，並依「本週新增星數」降序排列。

本週主題：榜單呈現「AI Agent 基礎設施全面升級」的圖景——技能（skill）生態、MCP 伺服器、代碼審查輔助與 Agent-User 互動協議，幾乎佔滿全部名次；同時 Google、Meta、阿里、n8n、ChromeDevTools 等大廠帳號同台競逐，代表 Agent 工具鏈已成主流賽道。

## 一覽表

| 排名 | 專案 | 語言 | 總星數 | 本週新增 | 主題 |
|---|---|---|---|---|---|
| 1 | [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | Python | 75,513 | +5,302 | AI 研究技能 |
| 2 | [kajisho5/ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) | Python | 11,377 | +3,048 | 影片處理技能 |
| 3 | [meta/astryx](https://github.com/meta/astryx) | TypeScript | 33,270 | +2,635 | Meta 設計系統 |
| 4 | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | TypeScript | 13,173 | +2,616 | 設計技能庫 |
| 5 | [dream-num/univer](https://github.com/dream-num/univer) | TypeScript | 31,927 | +2,319 | AI 辦公室 SDK |
| 6 | [GoogleChrome/modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src) | TypeScript | 11,186 | +2,309 | 現代 Web 指引 |
| 7 | [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | Go | 56,558 | +2,259 | AI 代碼審查 |
| 8 | [backnotprop/plannotator](https://github.com/backnotprop/plannotator) | TypeScript | 15,190 | +1,764 | 計畫/審查工具 |
| 9 | [we-promise/sure](https://github.com/we-promise/sure) | Ruby | 18,033 | +1,509 | 個人理財 App |
| 10 | [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) | Python | 8,536 | +1,422 | 交易技能 |
| 11 | [ag-ui-protocol/ag-ui](https://github.com/ag-ui-protocol/ag-ui) | TypeScript | 21,811 | +1,421 | Agent-User 協議 |
| 12 | [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | TypeScript | 59,454 | +1,203 | 瀏覽器 MCP |
| 13 | [n8n-io/nod](https://github.com/n8n-io/nod) | TypeScript | 3,818 | +1,008 | 個人自動化 Agent |
| 14 | [pookjw/HermesEnabler](https://github.com/pookjw/HermesEnabler) | Objective-C | 2,535 | +318 | Apple Watch 面錶 |

## 深度介紹

### 第 1 名：mvanhorn/last30days-skill — AI 研究技能：跨平台深度調研器

一句定位：在 Agent 中一鍵執行 30 天內的跨平台（Reddit、X、YouTube、HN、Polymarket、網頁）調研，產出有來源依據的摘要。

- **功能說明**：支援 Claude Code、Codex、Cursor、Gemini CLI、Grok、DeepSeek Harness、claude.ai 等 Agent Skills 宿主；以來源得分排序、並整理熱門討論，是目前榜上星數最高的技能專案（75,513 總星、+5,302 本週）。
- **適用場景**：主題調研、市場情緒擷取、競品觀察；想讓 Agent 自主完成「近期全網討論」式情報搜集時最直接。

### 第 2 名：kajisho5/ffmpeg-skill — 給 coding agent 的本地影片編輯器

一句定位：42 個 FFmpeg 工具配上機器可讀契約與 MCP 伺服器，讓 agent 直接完成剪輯、字幕、調整、爆音與平台匯出。

- **功能說明**：支援 Claude Code、Cursor、Codex；無雲端、無需 API key；包含 loudness、reframe、caption 等全流程。
- **適用場景**：自動化影片處理、社群素材製作、無頭環境之影片批次處理。

### 第 3 名：meta/astryx — Meta 開源設計系統

一句定位：全可客製化且 Agent 友善的開源設計系統，為產品打下一致的設計基礎。

- **功能說明**：涵蓋 Foundations、Components、Patterns 三層；支援 npm/pnpm/yarn 安裝；定位「agent-ready」的組件庫與設計系統核心。
- **適用場景**：產品團隊建立標準設計語言、Agent 驅動開發環境下的一致 UI 輸出。

### 第 4 名：google-labs-code/stitch-skills — Google 開源的 Stitch Agent 技能庫

一句定位：為 Stitch MCP 伺服器設計的 Agent Skills 合集，遵循 Agent Skills 開放標準。

- **功能說明**：支援 Antigravity、Gemini CLI、Claude Code、Cursor；可整套插件安裝或選擇式安裝各 skill。
- **適用場景**：與 Stitch 系統整合的設計/視覺工作流；想讓 Agent 自主完成 UI 設計任務。

### 第 5 名：dream-num/univer — AI 辦公室 SDK

一句定位：開源 Univer Office SDK，將編輯、計算、協作與檔案處理能力帶入你的產品與 Agent。

- **功能說明**：開源核心基礎上的協作/編輯/ Facade API/事件系統；支援 AI 與人互動的 office-like 應用組裝。
- **適用場景**：內部協作平台、文件/表格處理應用、Agent 驅動的辦公自動化。

### 第 6 名：GoogleChrome/modern-web-guidance-src — 讓 Agent 保持最新 Web 最佳實踐

一句定位：Google Chrome 團隊公開的現代 Web 指引（Source），供 coding agent 即時取得最新規範。

- **功能說明**：含 CSS & Layout（144 項）、HTML & DOM（38 項）等完整特性清單；可查詢 guide by ID 或掃描代碼庫尋找舊式寫法。
- **適用場景**：Agent 生成 Web 程式碼時自動遵循當前瀏覽器規範、現代化重構檢查。

### 第 7 名：alibaba/open-code-review — 阿里開源代碼審查工具

一句定位：結合確定性的流水線與 LLM Agent，在阿里千萬級代碼庫上驗證過的安全、快速、高效審查工具。

- **功能說明**：Go 實作，hybrid 架構（deterministic pipeline + LLM agent）；內建 NPE、thread-safety、XSS、SQL injection 等多語言規則；支援 OpenAI & Anthropic 相容 API。
- **適用場景**：企業代碼審查流程、PR 自動檢查、高併發多語言專案的品質門。

### 第 8 名：backnotprop/plannotator — Agent inbox / 計畫審查工具

一句定位：在工作階段中與 Agent 保持同步——審查計畫、批注程式碼、分享回饋。

- **功能說明**：Plan Inbox、Herdr 終端批注、HTML artifact / live site 導覽審查；支援 Code Review 與 Plan mode。
- **適用場景**：資深工程師審查 Agent 產出物、團隊對 Agent 提案進行批註、長線 Agent 工作流的人工關卡。

### 第 9 名：we-promise/sure — 全民個人理財 App

一句定位：由全民打造的開源個人理財應用，支援自架與 fork。

- **功能說明**：以 Ruby 構建、開源自架，含一鍵部署與 Demo 資料載入；具備性能與自託管說明文件。
- **適用場景：** 個人預算管理、自架開源理財工具、想看懂如何做開源金融 App 的參考實作。

### 第 10 名：tradermonty/claude-trading-skills — Claude 交易技能套件

一句定位：為 Claude Code / Claude Web 設計的股票交易技能，涵蓋市場分析、技術圖表、經濟日曆、選股器與策略開發。

- **功能說明**：包含 example outputs、成本說明、無 API Key 起步路徑；支援 Claude Web/桌面與 CLI。
- **適用場景：** 投資者情緒分析、個人投資研究、技術分析工具鏈。

### 第 11 名：ag-ui-protocol/ag-ui — Agent-User 互動協議

一句定位：任何 Agent 都能接任何 App 的開放協議，將 Agent 帶入前端應用。

- **功能說明**：定義 Server/Events 兩層、SDK 與 integrations 列表，支援 Agent 與前端 UI 的雙向互動。
- **適用場景：** 前端應用嵌入 Agent、Agent 驅動的 UI 工作流、Agent 框架與前端框架的標準化對接。

### 第 12 名：ChromeDevTools/chrome-devtools-mcp — 給 Agent 的 Chrome DevTools

一句定位：Chrome DevTools MCP 伺服器，讓 coding agent 直接控制瀏覽器。

- **功能說明**：支援 CLI 安裝、CLI/MCP 雙模式、Skills 插件；已有大量使用者與 MCP 生態整合。
- **適用場景：** Agent 自動化端到端測試、網頁除錯、前端功能驗證。

### 第 13 名：n8n-io/nod — 個人自動化 Agent

一句定位：擁有自己電腦的開源個人 Agent，會追帳單、備妥會議、取消訂閱，並先詢問再執行。

- **功能說明**：由 n8n 出品，TypeScript 實作，在本機執行、使用者自選模型；Agent 會在操作前詢問同意。
- **適用場景：** 個人工作流自動化、重複性 Web 操作替代、日常行事曆/帳單管理。

### 第 14 名：pookjw/HermesEnabler — Apple Watch 面錶支援

一句定位：為任何 Apple Watch 裝置啟用 Hermès Watch Faces。

- **功能說明**：Objective-C 實作，支援 IPA 安裝與 Xcode 自建；macOS 與 Windows 雙平台文件。
- **適用場景：** Apple Watch 懷錶客製化、開源 watchOS 開發參考。

## 本週觀察

1. **大廠入局**：Google（Stitch、modern-web-guidance）、Meta（Astryx）、阿里（open-code-review）、n8n（nod）、ChromeDevTools 同台競技——頭部賽道已從「個人技能」走向「開發基礎設施與 Agent 協議」。
2. **技能生態爆發**：去年還是少數人使用的 Agent Skills，已出現 last30days、ffmpeg、trading 等橫跨研究、影片、金融的深度技能，生態加速成熟。
3. **Agent-User 協議成關鍵**：AG-UI 以 Agent-User 協議定位自身，顯示「Agent 與前端應用的標準對接」已成趨勢；類似地，Chrome DevTools MCP 是另一場「讓 Agent 接管工具」的比賽。
4. **開源金融/生活應用**：sure 以「全民個人理財」定位吸引社群；n8n nod 以「自己跑個人 Agent」主張進入生活自動化。

## 方法說明

- 資料來源：`https://github.com/trending?since=weekly`（2026-11-26 抓取，約 575 KB 頁面）。
- 每個專案的總星數、fork 數、本週新增星數皆直接解析自頁面，未使用後端 API 估算。
- 排序依據：本週新增星數數值降序。
- README 以 `raw.githubusercontent.com/<owner>/<repo>/HEAD/README.md` 抓取，內容整理為繁中介紹。
