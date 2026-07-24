---
layout: post
title: "grill-me Skill 分析：AI 代理的嚴苛訪談模式"
date: 2026-07-23
category: AI-Skills
tags: [grill-me, grilling, ai-agents, skills, claude, mattpocock]
---

## 原始出處

- 作者：Matt Pocock ([mattpocock](https://github.com/mattpocock))
- 專案：[skills](https://github.com/mattpocock/skills) — 超過 186k Star 的 AI Agent Skills 集合
- 位置：`skills/productivity/grill-me/`

---

## 一、grill-me 是什麼？

**grill-me** 是 mattpocock/skills 中 `productivity` 分類下的 skill，功能是啟動一個「嚴苛訪談（relentless interview）」流程，讓 AI 代理扮演審問者角色，針對使用者提出的計畫、設計或決策，逐一追問直到決策樹的所有分支都得到解答。

官方描述：

> Get relentlessly interviewed about a plan or design until every branch of the decision tree is resolved.

簡單來說，就是「AI 追到你無法迴避為止」。

---

## 二、目錄結構

grill-me 的完整目錄結構如下：

```
skills/productivity/grill-me/
├── SKILL.md              ← 主 skill 定義
└── agents/
    └── openai.yaml       ← OpenAI 代理介面設定
```

注意：實際的「訪談行為」定義在**另一個獨立 skill** `grilling` 中（`skills/productivity/grilling/SKILL.md`），grill-me 本質上是一個觸發器/入口。

---

## 三、檔案內容解析

### 1. SKILL.md

```yaml
---
name: grill-me
description: A relentless interview to sharpen a plan or design.
disable-model-invocation: true
---

Run a `/grilling` session.
```

重點：

- `disable-model-invocation: true`：禁止模型自行調用此 skill，必須由使用者手動觸發。
- 內容只有一行指令：`Run a /grilling session.` — 代表 grill-me 本身不含有邏輯，只是將流程導向 grilling skill。

### 2. agents/openai.yaml

```yaml
interface:
  display_name: "Grill Me"
  short_description: "Sharpen a plan through interview"
policy:
  allow_implicit_invocation: false
```

- `display_name`：在代理介面顯示的名稱。
- `allow_implicit_invocation: false`：不允許隱式（自動）調用，確保使用者明確要求才會啟動。

---

## 四、grilling Skill（實際行為定義）

grill-me 啟動後會載入的 `grilling` skill，其 SKILL.md 內容：

```yaml
---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.

Do not act on it until I confirm we have reached a shared understanding.
```

### 核心行為規則

1. **逐一追問**：一次只問一個問題，等待使用者回答後才繼續。
2. **覆蓋決策樹**：沿著決策樹的所有分支追問，直到所有依賴都被釐清。
3. **提供建議**：每個問題同時附上 AI 的推薦答案。
4. **事實 vs. 決策**：
   - 可查詢的事實 → AI 自行查閱（檔案系統、工具等）。
   - 主觀決策 → 交由使用者決定。
5. **不自行行動**：直到使用者確認雙方理解一致，才開始執行。

---

## 五、使用方式

### 觸發方式

- 使用 `/grilling` 指令（在支援 slash command 的代理中）。
- 或使用「grill」相關觸發詞，例如：
  - 「grill me on this plan」
  - 「帮我嚴苛審查這個設計」
  - 「追問我這個決策」

### 典型流程

```
使用者：「我打算用 Next.js 做一個電商平台，grill me」

AI：「好的。第一個問題：你的目標使用者是誰？
     我建議：聚焦在 18-35 歲、追求快速購物體驗的年輕族群。
     你的想法？」

使用者：「對，但我也想吸引中高齡」

AI：「收到。第二個問題：你打算用哪種資料庫？
     我建議：PostgreSQL，因為事務一致性對電商至關重要。
     你的想法？」

...（持續追問直到決策樹完整）

AI：「我們已經覆蓋了：使用者、資料庫、支付、部署、SEO、安全。
     你確認這是我們的一致理解嗎？」

使用者：「是的，開始實作」

AI：「好的，開始執行。」
```

---

## 六、設計理念與優點

| 特點 | 說明 |
|------|------|
| **強制釐清模糊需求** | 很多失敗專案源於需求不明確，grill-me 用追問方式逼出隱藏假設 |
| **一次一問** | 避免資訊轟炸，讓使用者專注於單一決策 |
| **AI 查事實，人做決策** | 分工清晰，AI 負責蒐集資訊，人負責價值判斷 |
| **不自行行動** | 確保最終執行方向是使用者認可的，避免 AI「自作主張」 |
| **提供推薦答案** | 不只是追問，還附上建議，降低使用者決策負擔 |

### 適用場景

- 技術架構決策（選框架、資料庫、微服務拆分等）
- 產品設計審視（使用者旅程、功能優先級）
- 專案計畫評估（時程、風險、資源分配）
- 任何「你覺得這個主意好嗎」的模糊提問

### 不適用場景

- 需要快速原型、不追求完美規劃時
- 使用者已經有完整需求文件（直接讀文件比追問快）
- 使用者處於決策疲勞狀態（連續追問會造成壓力）

---

## 七、技術架構洞察

grill-me 的設計展現了 mattpocock/skills 的幾個重要模式：

1. **Skill 拆分**：grill-me（入口）與 grilling（行為）分離，方便複用與組合。
2. **明確的觸發策略**：`disable-model-invocation: true` + `allow_implicit_invocation: false` 確保不被濫用。
3. **代理化（Agentization）**：透過 `agents/openai.yaml` 將 skill 暴露為可調用的代理。

---

## 八、與類似 Skill 的對比

| Skill | 用途 | 差異 |
|-------|------|------|
| **grill-me / grilling** | 嚴苛追問，釐清決策 | 互動式、一次一問、覆蓋決策樹 |
| **teach** | AI 教學使用者 | 知識傳遞，非決策釐清 |
| **handoff** | 會議話摘要移交 | 壓縮對話，供其他代理接手 |
| **plan**（Hermes） | 產生待辦計畫 | 一次性輸出，非互動追問 |

---

## 九、總結

grill-me 是一個設計精緻的「決策壓力測試」工具。它不產生代碼、不寫文件，而是通過結構化的追問流程，幫助使用者在執行前釐清所有假設、依賴和模糊點。

核心理念很簡單：**在你開始做事之前，先確保你真的想清楚了。**

對於習慣跳過規劃直接實作的開發者來說，這是一個強烈的提醒——以及一個友善的「攔路虎」。

---

## 參考連結

- [mattpocock/skills](https://github.com/mattpocock/skills)
- [grill-me 原始碼](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me)
- [grilling skill](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling)
- [Productivity Skills README](https://github.com/mattpocock/skills/blob/main/skills/productivity/README.md)
