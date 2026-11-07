---
title: "GitHub 本週熱門專案榜（2026/11/01–11/07）：Agent Skills 全面刷屏"
date: 2026-11-07
description: 本週 GitHub Trending 前 19 名整理：t3code 單週 +16,782 星领跑，mattpocock/skills、claude-mem、Scrapling、impeccable 等 AI Agent 技能與工具專案佔了絕大半席，紫微斗數排盤引擎與 Kronos 金融模型也衝進榜內。
tags: [GitHub, Trending, AI Agent, 開源專案, 週報]
---

# GitHub 本週熱門專案榜（2026/11/01–11/07）

> 資料來源：[GitHub Trending（每週）](https://github.com/trending?since=weekly)，擷取於 2026-11-07。「本週新增」為 Trending 頁面標示的週增星數。

本週榜單几乎被 AI Agent 生態包場：**Agent Skills（技能包）就佔了 6 席**，從 Anthropic 官方、Matt Pocock 到社群自製的設計技能應有盡有；其余也是 browser 自動化、worktree 並行代理、PR 審查等 Agent 基礎設施。唯一的「純传统軟體」代表是 Wayland 合成器 Hyprland。

## 總覽表（依本週新增星數排序）

| # | 專案 | 語言 | 本週新增 | 累計 ⭐ | 一句話 |
|---|------|------|---------|---------|--------|
| 1 | [pingdotgg/t3code](https://github.com/pingdotgg/t3code) | TypeScript | +16,782 | 50,709 | AI 代理控制台面（詳見[上週專文](/2026/11/06/t3code-agent-control-surface.html)） |
| 2 | [mattpocock/skills](https://github.com/mattpocock/skills) | Shell | +9,589 | 317,343 | 「給真正工程師的技能」——從作者 .agents 目錄直接釋出 |
| 3 | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | TypeScript | +8,726 | 114,298 | 給所有 Agent 的跨工作階段持久記憶 |
| 4 | [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) | Python | +8,372 | 99,151 | 處理一切反爬對抗的網頁抓取框架 |
| 5 | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Rust | +8,172 | 105,259 | 給 coding agent 的「設計詞彙表」，引導更有品味的 UI 產出 |
| 6 | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | CSS | +6,900 | 50,023 | 反 AI 腔（anti-slop）設計技能，支援 Claude Code / Cursor / Codex |
| 7 | [milind-soni/OpenMausBot](https://github.com/milind-soni/OpenMausBot) | TypeScript | +6,395 | 16,508 | 開源 Grok Bot 替代品，附虛擬機供 bot 使用 |
| 8 | [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | Shell | +6,018 | 36,397 | 把 Claude Code 變成完整遊戲開發工作室：49 個 agent、72 個技能 |
| 9 | [Renhuai123/ziwei-doushu](https://github.com/Renhuai123/ziwei-doushu) | TypeScript | +5,476 | 16,682 | 紫微斗數開源排盤引擎（倪海廈《天紀》體系） |
| 10 | [obra/superpowers](https://github.com/obra/superpowers) | Shell | +4,577 | 313,938 | 代理技能框架與軟體開發方法論 |
| 11 | [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) | Python | +4,405 | 78,070 | 開源 agentic 影片生產系統：12 條管線、100+ 技能 |
| 12 | [github/spec-kit](https://github.com/github/spec-kit) | Python | +4,202 | 148,338 | GitHub 官方 SDD（規格驅動開發）工具包 |
| 13 | [anthropics/skills](https://github.com/anthropics/skills) | Python | +3,159 | 188,470 | Anthropic 官方 Agent Skills 倉庫 |
| 14 | [shiyu-coder/Kronos](https://github.com/shiyu-coder/Kronos) | Python | +2,984 | 47,171 | 金融市場「語言」基礎模型 |
| 15 | [max-sixty/worktrunk](https://github.com/max-sixty/worktrunk) | Rust | +2,184 | 11,896 | 為平行 AI agent 工作流設計的 Git worktree CLI |
| 16 | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | Markdown | +1,921 | 11,421 | 建構優秀介面的 agent 技能合集 |
| 17 | [The-PR-Agent/pr-agent](https://github.com/The-PR-Agent/pr-agent) | Python | +1,523 | 15,390 | 原版開源 PR 審查代理 |
| 18 | [hyprwm/Hyprland](https://github.com/hyprwm/Hyprland) | C++ | +1,413 | 40,472 | 高可設定動態平鋪 Wayland 合成器 |
| 19 | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | Rust | +1,404 | 46,542 | 給 AI agent 的瀏覽器自動化 CLI |

## 本週三大看點

### 1. Agent Skills 成為「開源硬通货」

榜上 6 個技能倉庫（mattpocock/skills、anthropics/skills、obra/superpowers、jakubkrehel/skills、impeccable、hallmark）合計單週新增超過 3.4 萬星。值得注意的是兩個趨勢：

- **個人技能目錄直接變熱門專案**：Matt Pocock 只是把自己 `.agents` 目錄推上 GitHub，就拿到 +9,589 星、累計 31.7 萬星——說明開發者更信任「真實工作流裡長出來的技能」，而非官方範例。
- **審美類技能崛起**：impeccable 和 hallmark 都主打「反 AI slop」——用一套設計詞彙與規範約束 agent 產出的 UI，解決 AI 生成介面千篇一律的痛點。CSS/設計能進 Rust/Python 主導的榜單，本身就是訊號。

### 2. Agent 基礎設施持續補洞

- **claude-mem（+8,726）**：解決「每次對話都失憶」——把 agent 的行為.capture 成跨 session 的持久脈絡，通用於各家 agent。
- **worktrunk（+2,184）**：Git worktree 的 CLI 封裝，讓多個 agent 平行開發互不干擾，是「多代理並行」成為日常後的必然產物。
- **vercel-labs/agent-browser（+1,404）**：Rust 寫的瀏覽器自動化 CLI，專為 agent 操作網頁設計。
- **spec-kit（+4,202）**：GitHub 官方押注 Spec-Driven Development——先寫規格、再讓 agent 實作。

### 3. 榜外的「非 AI  minority」

- **Hyprland（+1,413）**：Linux 桌面圈常青樹，本週榜上唯一與 AI 無關的基礎軟體。
- **Kronos（+2,984）**：把金融 K 線當「語言」訓練的基礎模型，量化圈關注度持續發酵。
- **ziwei-doushu（+5,476）**：紫微斗數排盤引擎衝進全球榜——完整排盤演算法、四化系統、格局知識庫加古籍原文資料，中式命理開源化少見的完成度。

## 我的觀察

上週還在討論「哪個 coding agent 最好用」，本週熱點已整體遷移到**如何餵養與約束 agent**：技能包、記憶層、工作流隔離、設計規範。開源社群的共識很明確——模型本身夠強了，下一步拼的是工程化的外圍生態。

---

*本文由 AI 擷取 GitHub Trending 每週榜單（19 個專案）整理，星數為抓取當下快照，僅供參考。*
