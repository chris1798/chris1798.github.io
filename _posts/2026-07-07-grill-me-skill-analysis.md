---
title: "Grill Me Skill 深度分析 — 讓 AI 嚴厲質問你的計畫，避免踩坑"
date: 2026-07-07
categories: [AI, Open Source, Skills, GitHub, 效率工具]
tags: [Grill Me, MattPocock, 開源, AI 協作, 規劃, 決策樹]
---

# 🌶️ Grill Me Skill 深度分析

**📅 日期:** 2026-07-07

---

## 📖 什麼是 Grill Me？

**Grill Me** 是一個開源的 AI 協作 Skill，由知名開發者 [Matt Pocock](https://github.com/mattpocock) 設計並推廣。它的核心理念是：**在動手做之前，先用一連串嚴厲的問題把你的計畫「拷問」一遍**。

> 🌶️ *Grill* 在這裡的意思是「嚴厲質問」— 就像燒烤前的醃製，把問題問到最深處，讓你的想法經過充分考驗。

- 📂 原始專案：[mattpocock/skills](https://github.com/mattpocock/skills)
- 🌟 曾登上 Reddit / Hacker News / 各大社群熱門
- 🤖 支援超過 40+ AI 程式助手（Claude Code、Cursor、Codex、OpenCode、Continue、Windsurf 等）

---

## 🎯 解決的核心問題

Matt Pocock 指出，使用 AI 程式助手時最常见的失敗模式是 **「溝通不對齊」**：

### 問題：「Agent 做的不是你想要的」

> "No-one knows exactly what they want." — David Thomas & Andrew Hunt, *The Pragmatic Programmer*

你以為開發者（AI）知道你想要什麼，但看完產出才發現——他完全沒理解你的意思。

### 解法：Grilling Session

在開始寫任何程式碼之前，讓 AI 用一系列深入的問題，跟你一起把計畫搞清楚。

---

## 🧠 工作原理

Grill Me 的核心機制是一個 **決策樹問答流程**：

```
┌─────────────────────────────────────┐
│           開始 Grill Session         │
├─────────────────────────────────────┤
│  1. 確認計畫名稱與領域               │
│  2. 識別主要探討分支                 │
│  3. 一個分支一個分支深入               │
│     ├── Understand (理解)            │
│     ├── Probe ( probing 假設)        │
│     ├── Challenge (質疑)             │
│     └── Resolve (解決)               │
├─────────────────────────────────────┤
│  結束條件：                          │
│  • DECIDED  — 明確決策               │
│  • DEFERRED — 暫緩處理               │
│  • RESOLVED — 討論完畢               │
└─────────────────────────────────────┘
```

### 三個終止狀態

| 狀態 | 意義 | 舉例 |
|------|------|------|
| **DECIDED** | 做出明確決策，並記錄理由 | 「選擇 PostgreSQL 因為...」 |
| **DEFERRED** | 使用者決定先處理其他事 | 「這個先放一邊，後面再說」 |
| **RESOLVED** | 討論後滿意，問題已釐清 | 「好，我理解了，繼續吧」 |

---

## 🎭 角色定位： interviewer 不是 executor

這是 Grill Me **最重要的規則**：

> ❌ **它不會幫你做事**
> ✅ **它只會幫你「想清楚」**

| ✅ 允許做的 | ❌ 不允許做的 |
|------------|-------------|
| 讀程式碼來了解現狀 | 寫程式碼、腳本、報告 |
| 寫 Session 紀錄檔 | 執行 agent 來做任務 |
| 問問題、挑戰假設 | 直接產出計畫要產出的東西 |

---

## 📚 領域範圍（Scope Discipline）

Grill Me 會根據你指定的領域自動切換角色：

| 你說的領域 | 它會扮演的角色 | 探probe 的內容 |
|-----------|--------------|---------------|
| 產品設計 | 產品思維者 | 用戶需求、市場定位、功能優先順序 |
| 軟體架構 | 技術審查者 | 架構決策、實作選擇、依賴關係 |
| 創業計畫 | 策略顧問 | 商業模式、競爭分析、風險評估 |
| 創作（小說等） | 故事編輯 | 角色動機、劇情結構、主題連貫性 |

它會主動提醒你跨領域問題，例如：「這觸及技術可行性——要往那邊討論，還是留在產品面？」

---

## 📝 Session 檔案機制

Grill Me 會維護一個持續的紀錄檔，讓你可以在不同對話之間中斷、繼續：

```
grill-me-sessions/<plan-name>.grill.md
```

檔案格式包含：

```markdown
# Grill Session: my-project

Status: in-progress | complete
Domain: <領域>

## Decision Log
### DECIDED: database choice
- Decision: PostgreSQL
- Rationale: 需要複雜查詢和 JSONB
- Date: 2026-07-06

### DEFERRED: 進階安全功能
- Reason: 優先完成 MVP
- Risk: 後期補救成本較高
- Date: 2026-07-06

## Open Threads
- 目前討論中的主題...

## Parking Lot
- 使用者提到但尚未探索的主題...
```

---

## 🔍 深入 probe 的常見面向

Grill Me 在問話過程中，會針對以下面向深入挖掘：

| 面向 | 範例問題 |
|------|---------|
| **未聲明的假設** | 「你假設 X 是成立的，事實上是這樣嗎？」 |
| **遺漏的失敗模式** | 「當這個失敗時，會發生什麼？」 |
| **範圍蔓延信號** | 「這聽起來可能變成三件事，你第一個要做的到底是哪件？」 |
| **依賴風險** | 「這需要 Y 先存在。如果 Y 不存在呢？」 |
| **前後矛盾** | 「你剛才說 A，但這個做法暗示 B，到底是哪個？」 |
| **模糊語言** | 「你說『簡單』— 請定義什麼是簡單。」 |
| **缺失的 tradeoff** | 「選擇這個方法，你放棄了什麼？」 |

---

## 💡 為什麼它會爆紅？

1. **普世性** — 不只是寫程式，任何需要做決策的場景都適用
2. **反直覺** — 大多數人習慣讓 AI 直接做事，Grill Me 反其道而行
3. **可組合** — 可以跟其他 skill 搭配使用
4. **跨工具** — 不綁定特定 AI 助手，支援 40+ 工具
5. **可持續** — Session 檔案讓對話可以斷點續接

---

## 🛠️ 如何使用？

### 安裝方式

```bash
npx skills@latest add mattpocock/skills
```

### 直接呼叫

在支援的 AI 程式助手中輸入：
- `/grill-me`
- `/grill-with-docs`（加強版，會建立共用語言文件）
- 或口頭說："grill me about [你的計畫]"

### 支援的工具

Claude Code、Cursor、Codex、OpenCode、Continue、Windsurf、Gemini CLI、Cline 等 40+ 種

---

## ⚠️ 使用限制

- **不適合**：程式碼審查、除錯、重構、一般性程式碼回饋
- **適合**：規劃階段、設計階段、任何需要釐清想法的場景
- **需要**：使用者願意接受被「質問」，且能耐心回答問題

---

## 🌟 編輯推薦

如果你常常遇到以下情況：
- ✅ AI 做的東西不是你想要的
- ✅ 計畫做了半天發現方向有誤
- ✅ 團隊（或你 + AI）對需求理解不一致

Grill Me 是非常值得嘗試的 Skill。它就像一個**不怕得罪你的搭檔**，在你衝下去做之前，先幫你找到所有可能踩的坑。

---

## 🔗 相關連結

- [原始 Skill 倉庫](https://github.com/mattpocock/skills)
- [Grill Me 單一倉庫](https://github.com/RobMitt/grill-me-skill)
- [Hacker News 討論](https://news.ycombinator.com/item?id=47550391)
- [Matt Pocock 的 Newsletter](https://www.aihero.dev/s/skills-newsletter)

---

*本文分析整理自多個開源倉庫，原始資料來源：GitHub*
