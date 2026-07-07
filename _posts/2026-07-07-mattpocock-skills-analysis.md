---
title: "深度分析 mattpocock/skills — 20 個 AI 協作 Skill 功能解析"
date: 2026-07-07
categories: [GitHub, 開源, AI, 程式設計, 效率工具]
tags: [MattPocock, Skills, AI協作, OpenSource, 程式開發, 最佳實踐]
---

# 🔍 深度分析 mattpocock/skills — 20 個 AI 協作 Skill 功能解析

**📅 日期:** 2026-07-07
**🔗 來源:** [github.com/mattpocock/skills](https://github.com/mattpocock/skills)

---

## 📖 專案概述

[mattpocock/skills](https://github.com/mattpocock/skills) 是由知名 TypeScript 開發者 **Matt Pocock** 建立的一套 AI 程式助手 Skill 集合。他的理念是：

> **真實的工程師需要的不是「vibe coding」，而是有紀律的工程實踐。**

這些 Skill 設計為 **小、易調整、可組合**，支援任何模型，基於數十年的工程經驗整理而成。支援 Claude Code、Cursor、Codex、OpenCode 等 **40+ 種 AI 程式助手**。

---

## ⚙️ Skill 分類架構

整個倉庫分為 **2 大類別**，每類又分 **User-invoked**（使用者主動呼叫）和 **Model-invoked**（模型自動觸發）：

```
mattpocock/skills/
├── skills/
│   ├── engineering/       ← 工程類 (14 個 Skill)
│   │   ├── [User-invoked] 7 個
│   │   └── [Model-invoked] 7 個
│   └── productivity/      ← 效率類 (5 個 Skill)
│       ├── [User-invoked] 4 個
│       └── [Model-invoked] 1 個
```

> **User-invoked**: 使用者必須主動輸入（如 `/grill-me`）才能觸發，負責「指揮調度」。
> **Model-invoked**: 使用者或模型都能觸發，包含「可複用的專業紀律」，可被 User-invoked Skill 調用。

---

## ⚙️ 工程類 Skills（Engineering — 14 個）

### 🟠 User-invoked Skills（7 個）

這些是「指揮官」型 Skill，由使用者主動呼叫，負責調度其他模型 Skill 完成工作。

| # | Skill 名稱 | 功能說明 |
|---|-----------|---------|
| 1 | **[ask-matt](https://github.com/mattpocock/skills/tree/main/skills/engineering/ask-matt)** | **路由器** — 不確定要用哪個 Skill 時，問 Matt 即可自動推薦最合適的 Skill 或流程 |
| 2 | **[grill-with-docs](https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs)** | **進階版拷問** — 在拷問計畫的同時，自動建立/更新專案的領域模型（`CONTEXT.md`）和架構決策記錄（ADR），讓團隊與 AI 建立共用語言 |
| 3 | **[triage](https://github.com/mattpocock/skills/tree/main/skills/engineering/triage)** | **Issue 分診** — 將 Issue 透過狀態機進行分類和指派（類似 Jira 分派流程） |
| 4 | **[improve-codebase-architecture](https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture)** | **架構救星** — 掃描整個程式碼庫，找出「深化機會」（Deepening Opportunities），以視覺化 HTML 報告呈現，再針對每個機會進行深入探討 |
| 5 | **[setup-matt-pocock-skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/setup-matt-pocock-skills)** | **一鍵初始化** — 為工程 Skill 設定倉庫級配置（Issue 追蹤器、分診標籤、領域文檔格式），每個專案只需執行一次 |
| 6 | **[to-issues](https://github.com/mattpocock/skills/tree/main/skills/engineering/to-issues)** | **計畫分解** — 將任何計畫、規格或 PRD 拆解為獨立可執行的 Issue（使用垂直切片方法） |
| 7 | **[to-prd](https://github.com/mattpocock/skills/tree/main/skills/engineering/to-prd)** | **自動生成 PRD** — 根據現有對話和程式碼庫理解，自動產出產品需求文件，不需再被問話拷問 |

### 🔵 Model-invoked Skills（7 個）

這些是「專業工兵」型 Skill，包含可複用的專業知識，可被自動調用。

| # | Skill 名稱 | 功能說明 |
|---|-----------|---------|
| 1 | **[prototype](https://github.com/mattpocock/skills/tree/main/skills/engineering/prototype)** | **快速原型** — 建立一次性原型來回答設計問題。針對狀態/邏輯問題生成可執行終端 App，UI 問題則產生多個可切換的介面變體 |
| 2 | **[diagnosing-bugs](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs)** | **系統化除錯** — 嚴格的除錯流程：重現 → 最小化 → 假設 → 插裝偵測 → 修復 → 回歸測試。不鼓勵跳過任何階段 |
| 3 | **[research](https://github.com/mattpocock/skills/tree/main/skills/engineering/research)** | **背景研究** — 啟動背景 Agent 對高信任來源（官方文件、原始碼、規格）進行調查，結果以引用的 Markdown 檔案儲存，不阻塞主工作 |
| 4 | **[tdd](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd)** | **測試驅動開發** — 紅→綠循環的 TDD 參考。教 AI 寫出值得保留的測試，一次只處理一個垂直切片的功能或 Bug 修復 |
| 5 | **[domain-modeling](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling)** | **領域建模** — 主動建構和精煉專案的領域模型。挑戰術語、用邊界案例測試、並自動更新 `CONTEXT.md` 和 ADR |
| 6 | **[codebase-design](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design)** | **程式碼庫設計** — 共用設計紀律：在乾淨的界面上放置「高功能、小介面」的深層模組，並通過該介面進行測試 |
| 7 | **[code-review](https://github.com/mattpocock/skills/tree/main/skills/engineering/code-review)** | **雙軸程式碼審查** — 從兩個軸線審查差異：① **標準**（是否遵循專案規範）② **規格**（是否忠實實現了原始 Issue/PRD）。以並行子 Agent 執行，避免互相汙染 |

---

## 📋 效率類 Skills（Productivity — 5 個）

### 🟢 User-invoked Skills（4 個）

| # | Skill 名稱 | 功能說明 |
|---|-----------|---------|
| 1 | **[grill-me](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me)** | **計畫拷問** — 對你的計畫、設計或想法進行連環拷問，直到決策樹的每個分支都得到解決。不寫程式碼，只幫你釐清思路 |
| 2 | **[handoff](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff)** | **工作交接** — 將當前對話壓縮成交接文件，讓另一個 Agent 可以繼續工作。包含「建議 Skill」列表 |
| 3 | **[teach](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach)** | **教學模式** — 跨多個 Session 教授新技能或概念。利用當前目錄作為有狀態的教學工作空間 |
| 4 | **[writing-great-skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills)** | **Skill 寫作指南** — 教你怎麼寫出好的 Skill：預測性、確定性、一致性等核心原則 |

### 🟡 Model-invoked Skills（1 個）

| # | Skill 名稱 | 功能說明 |
|---|-----------|---------|
| 1 | **[grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling)** | **拷問引擎** — `grill-me` 和 `grill-with-docs` 的底層核心。負責拷問的通用循環邏輯，可被其他 Skill 調用 |

---

## 🎯 設計哲學與核心理念

Matt Pocock 在 README 中提出使用這些 Skill 要解決的 **四大問題**：

### 1. Agent 做的不是你想要的 → `/grill-me` + `/grill-with-docs`
> 開發中最常見的失敗模式是「溝通不對齊」。先問清楚再做，比做完再改便宜 100 倍。

### 2. Agent 太啰嗦 → 共用語言（`CONTEXT.md`）
> 讓 AI 學會你的專案術語，減少用 20 個字說 1 個字的事。變數、函式、檔案名稱也會變得一致。

### 3. 程式碼跑不起來 → `/tdd` + `/diagnosing-bugs`
> 沒有測試回饋，Agent 就像在盲飛。紅→綠→重構循環提供一致的測試回饋。

### 4. 程式碼庫變成一團亂 → `/improve-codebase-architecture` + `/codebase-design`
> Agent 加速了寫程式的速度，但也加速了「軟體熵增」。建議每幾天跑一次架構掃描。

---

## 🔄 Skill 之間的依賴關係

```
                    ┌───────────────────┐
                    │  ask-matt (路由器)  │
                    └────────┬──────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌──────────────┐   ┌──────────────────┐   ┌──────────────┐
│  grill-me    │   │  grill-with-docs │   │  improve-    │
│  (拷問)      │   │  (拷問+領域建模) │   │  codebase-   │
│              │   │                  │   │  architecture│
└──────┬───────┘   └────────┬─────────┘   └──────┬───────┘
       │                   │                    │
       ▼                   ▼                    ▼
┌──────────────┐   ┌──────────────────┐   ┌──────────────┐
│  grilling    │   │  domain-modeling │   │  掃描 + 拷問  │
│  (拷問引擎)  │   │  (領域建模)      │   │              │
└──────────────┘   └──────────────────┘   └──────────────┘

┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  to-prd      │   │  to-issues   │   │  code-review │
│  (生成PRD)   │   │  (分解Issue) │   │  (程式碼審查) │
└──────────────┘   └──────────────┘   └──────────────┘

┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  prototype   │   │  tdd         │   │  diagnosing  │
│  (原型)      │   │  (TDD)       │   │  bugs        │
└──────────────┘   └──────────────┘   └──────────────┘

┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  handoff     │   │  teach       │   │  research    │
│  (交接)      │   │  (教學)      │   │  (背景研究)   │
└──────────────┘   └──────────────┘   └──────────────┘

┌──────────────┐
│  writing-    │
│  great-skills│
│  (Skill寫作) │
└──────────────┘
```

---

## 💡 推薦使用流程

### 新專案起手式
1. `/setup-matt-pocock-skills` → 初始化配置
2. `/grill-with-docs` → 拷問計畫 + 建立領域模型
3. `/to-issues` → 將計畫拆解為 Issue

### 日常開發
4. `/tdd` → 測試驅動開發
5. `/triage` → Issue 分診
6. `/code-review` → 程式碼審查

### 遇到問題時
7. `/diagnosing-bugs` → 系統化除錯
8. `/research` → 背景研究（不阻塞）
9. `/improve-codebase-architecture` → 架構健康檢查

---

## 📊 Skill 統計

| 類別 | 子類 | 數量 |
|------|------|------|
| Engineering | User-invoked | 7 |
| Engineering | Model-invoked | 7 |
| Productivity | User-invoked | 4 |
| Productivity | Model-invoked | 1 |
| **合計** | | **19** |

---

## 🌟 編輯推薦

### 最實用的 5 個 Skill

| 排名 | Skill | 理由 |
|------|-------|------|
| 🥇 | grill-with-docs | 解決了 AI 開發最大的痛點：溝通不對齊 |
| 🥈 | improve-codebase-architecture | 對抗軟體熵增，長期維護必備 |
| 🥉 | tdd | 讓 AI 寫出值得保留的測試 |
| 4 | research | 背景研究不阻塞，效率拉滿 |
| 5 | code-review | 雙軸審查確保品質 |

---

## 🔗 相關連結

- [原始倉庫](https://github.com/mattpocock/skills)
- [skills.sh 安裝器](https://skills.sh/mattpocock/skills)
- [Matt Pocock Newsletter](https://www.aihero.dev/s/skills-newsletter)
- [Grill Me 詳細分析](/2026-07-07-grill-me-skill-analysis/)

---

*本文分析整理自 [mattpocock/skills](https://github.com/mattpocock/skills) 原始倉庫*
