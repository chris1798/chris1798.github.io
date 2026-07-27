---
title: "20 分鐘看完 Google AI 課程 Day 2+3 精華：MCP、A2A、Skills 完整解析"
date: 2026-07-27
description: Google 五天 AI 課程 Day 2 與 Day 3 重點整理，深入解析 MCP 通用插座、A2A Agent 協作協議、Skills 四大地雷、四道防線與 Meta-Skill，帶你快速掌握 AI Agent 生產環境的關鍵技術。
tags: [Google AI, MCP, A2A, Skills, AI Agent, Model Context Protocol, Agent-to-Agent]
categories: [AI, 教學]
---

# 20 分鐘看完 Google AI 課程 Day 2+3 精華：MCP、A2A、Skills 完整解析

> 來源：Gary Chen 影片整理 — [20 分鐘看完 Google AI 課程 Day 2+3 精華。MCP, A2A, Skills 解析](https://www.youtube.com/watch?v=XTCP1qoa3cc)

![影片截圖](https://i.ytimg.com/vi/XTCP1qoa3cc/maxresdefault.jpg)

Google 五天 AI 課程的 Day 2 和 Day 3 聚焦在 AI Agent 如何「真正連接世界」——不是停留在模型推理，而是讓 AI 接上外部工具、與其他 Agent 協作、並安全地上線生產環境。

本文根據 YouTube 創作者 Gary Chen 的精華整理影片，完整解析這三天課程的核心重點：**MCP、A2A、Skills、四大地雷、四道防線，以及 Meta-Skill**。

---

## 時間軸導航

- [0:00 開場](#000-開場)
- [1:44 MCP 通用插座](#144-mcp-通用插座)
- [6:00 A2A 找 AI 同事](#600-a2a-找-ai-同事)
- [10:28 Skill 四大地雷](#1028-skill-四大地雷)
- [15:54 四道防線](#1554-四道防線)
- [19:15 Meta-Skill](#1915-meta-skill)

---

## 0:00 開場

Google 五天 AI 課程的 Day 1 介紹了 AI Agent 的基本概念，Day 2 和 Day 3 則深入探討讓 Agent 真正能「做事」的三大關鍵技術：

1. **MCP（Model Context Protocol）**：讓 AI 連接外部工具的通用插座
2. **A2A（Agent-to-Agent Protocol）**：讓 AI Agent 之間互相分工合作的協議
3. **Skills**：讓 AI 具備專業能力的技能模組

這三大技術解決的核心問題是：**AI 不只是聊天機器人，而是能真正接上你的工作流程、自動執行任務的智能代理。**

---

## 1:44 MCP 通用插座

### 什麼是 MCP？

**MCP（Model Context Protocol）** 是由 Anthropic 發起、現在成為業界標準的開放協議，專為了解決 AI 應用與外部系統之間的連接問題。

簡單比喻：**MCP 就像是 AI 世界的「USB-C 通用插座」**。

### MCP 解決的問題

在 MCP 之前，每個 AI 應用要連接不同的外部服務（資料庫、檔案系統、API）都需要：

- 為每個服務撰寫專屬的整合程式碼
- 處理不同的認證機制
- 維護各自的連接邏輯
- 難以跨不同 AI 模型複用

### MCP 的三個核心角色

| 角色 | 說明 |
|------|------|
| **Host（主機）** | AI 應用程式（如 Claude Desktop、Cursor、Hermes Agent） |
| **Client（客戶端）** | 負責與 MCP Server 溝通的中介層 |
| **Server（伺服器）** | 提供工具（Tools）、資源（Resources）、提示（Prompts）的後端服務 |

### MCP 的三大能力

1. **Tools（工具）**：讓 AI 可以呼叫外部函數，如查詢資料庫、呼叫 API、執行程式
2. **Resources（資源）**：讓 AI 可以讀取外部資料，如檔案、資料庫內容
3. **Prompts（提示）**：讓 Server 可以定義結構化的提示模板

### MCP 在 2026 年的現狀

到了 2026 年，MCP 已經被所有主流 AI 供應商採用：
- Claude Desktop 內建 MCP 支援
- Cursor、VS Code 等 IDE 整合 MCP
- Google Cloud、AWS、Azure 都推出官方 MCP Server

### MCP vs A2A：何時用哪個？

| 維度 | MCP | A2A |
|------|-----|-----|
| 連接對象 | AI ↔ 工具/資料 | AI Agent ↔ AI Agent |
| 用途 | 讓 AI 存取外部資源 | 讓 AI 互相協作、委派任務 |
| 發起者 | Anthropic | Google（50+ 公司聯合） |

> **核心原則：MCP 讓 Agent 有手有腳（能做事），A2A 讓 Agent 有同事（能協作）。**

---

## 6:00 A2A 找 AI 同事

### 什麼是 A2A？

**A2A（Agent-to-Agent Protocol）** 是由 Google 在 2025 年推出、2026 年 1 月發布 v1.0 的開放協議，專為了解決多個 AI Agent 之間的協作問題。

簡單比喻：**A2A 就像是 AI 世界的「企業通訊軟體」**，讓不同 Agent 可以發現彼此、溝通協作、委派任務。

### A2A 解決的問題

當任務變得複雜時，單一 Agent 往往無法獨立完成。例如：
- 分析財務報表 → 需要「資料分析 Agent」+「財務專家 Agent」+「報告撰寫 Agent」
- 開發軟體 → 需要「需求分析 Agent」+「程式碼 Agent」+「測試 Agent」

在 A2A 之前，這些 Agent 之間沒有標準化的溝通方式，每個系統都要自己實現協作邏輯。

### A2A 的四大核心概念

| 概念 | 說明 |
|------|------|
| **Agent Card（代理卡片）** | Agent 的「名片」，宣告它能做什麼、支援什麼格式 |
| **Task（任務）** | Agent 之間委派的具體工作項目 |
| **Message（訊息）** | Agent 之間的溝通內容 |
| **Artifact（產出）** | 任務完成的產出物（報告、程式碼、分析結果） |

### A2A 的工作流程

```
1. 發現（Discovery）：Agent A 透過 Agent Card 找到合適的 Agent B
2. 委派（Delegation）：Agent A 將任務委派給 Agent B
3. 執行（Execution）：Agent B 執行任務，並回報進度
4. 交付（Delivery）：Agent B 提交產出物（Artifact）
5. 整合（Integration）：Agent A 整合結果，繼續後續任務
```

### A2A 的生態系

A2A v1.0 發布時已有 50+ 技術夥伴支援，包括：
- **企業軟體**：Salesforce、SAP、ServiceNow、Workday
- **開發工具**：Atlassian、Box、MongoDB、Langchain
- **顧問公司**：Accenture、Deloitte、McKinsey、BCG

---

## 10:28 Skill 四大地雷

### 什麼是 Skills？

**Skills** 是讓 AI Agent 具備特定專業能力的模組化技能。Google 在 Cloud Next 2026 推出了官方的 Agent Skills Repository，為 AI Agent 提供 BigQuery、GKE、Gemini API 等產品的專業知識。

### 地雷一：技能描述過於模糊

**問題**：Skill 的觸發條件和步驟描述不清楚，導致 AI 無法正確判斷何時使用。

**正確做法**：
- 使用明確的觸發條件（trigger conditions）
- 步驟用編號列出，包含具體指令
- 加入常見錯誤（pitfalls）和驗證步驟

### 地雷二：缺少邊界定義

**問題**：Skill 沒有定義「不該做什麼」，導致 AI 過度依賴或錯誤套用。

**正確做法**：
- 明確列出 Skill 的適用範圍
- 說明何時應該呼叫其他工具或 Skill
- 定義失敗條件和回退策略

### 地雷三：資訊過時或未維護

**問題**：Skill 中的 API endpoint、工具版本、指令過時，但沒有人更新。

**正確做法**：
- 定期檢查和更新 Skill 內容
- 使用版本標記（version）
- 執行 Skill 時發現問題，立即修正

### 地雷四：缺乏安全防護

**問題**：Skill 允許 AI 執行高風險操作（如刪除資料、修改設定），但沒有權限控制。

**正確做法**：
- 對危險操作加入確認機制
- 限制 AI 可以存取的工具和資源
- 遵循最小權限原則（Principle of Least Privilege）

---

## 15:54 四道防線

Google 在白皮書中提出了 AI Agent 上線前的四道安全防線：

### 防線一：輸入過濾（Input Sanitization）

- 過濾惡意提示（Prompt Injection）
- 防止 AI 被操縱執行非預期操作
- 使用規則過濾 + AI 檢測雙層防護

### 防線二：權限控制（Access Control）

- AI Agent 只能存取必要的資源
- 使用 Role-Based Access Control（RBAC）
- 敏感操作需要人類確認（Human-in-the-loop）

### 防線三：輸出驗證（Output Validation）

- 驗證 AI 的輸出是否合理、安全
- 防止 AI 產生錯誤建議或惡意內容
- 對程式碼執行靜態分析

### 防線四：監控日誌（Observability）

- 記錄 AI Agent 的所有操作
- 即時監控異常行為
- 建立警報機制，發現問題立即停止

---

## 19:15 Meta-Skill

### 什麼是 Meta-Skill？

**Meta-Skill** 是「管理 Skill 的 Skill」——一種更高層級的抽象，讓 AI 能夠：
- 自動選擇最適合的 Skill 來解決問題
- 組合多個 Skill 完成複雜任務
- 在沒有明確 Skill 時，動態產生新的工作流程

### Meta-Skill 的核心能力

| 能力 | 說明 |
|------|------|
| **Skill 發現** | 根據任務類型，自動找到可用的 Skill |
| **Skill 組合** | 將多個 Skill 串連成完整的工作流程 |
| **Skill 學習** | 從成功/失敗經驗中優化 Skill 選擇策略 |
| **Skill 生成** | 遇到新任務時，動態產生臨時 Skill |

### Meta-Skill 的實際應用

例如，當用戶說「幫我分析這份財務報告並做簡報」時，Meta-Skill 會：

1. 分析任務需求（分析 + 簡報）
2. 選擇對應的 Skill（資料分析 Skill + PPT 製作 Skill）
3. 協調兩個 Skill 的執行順序
4. 整合產出物，完成最終交付

---

## 總結

| 技術 | 核心問題 | 一句話總結 |
|------|----------|------------|
| **MCP** | AI 如何連接外部工具 | AI 的 USB-C 通用插座 |
| **A2A** | Agent 如何互相協作 | AI 世界的企業通訊軟體 |
| **Skills** | AI 如何具備專業能力 | AI 的專業技能模組 |
| **四道防線** | 如何安全上線 | 輸入過濾 → 權限控制 → 輸出驗證 → 監控日誌 |
| **Meta-Skill** | 如何智能組合 Skill | 管理 Skill 的 Skill |

這五個概念共同構成了 AI Agent 從「原型」走向「生產環境」的完整技術路徑。

> **影片來源**：Gary Chen — [20 分鐘看完 Google AI 課程 Day 2+3 精華。MCP, A2A, Skills 解析](https://www.youtube.com/watch?v=XTCP1qoa3cc)
> **原文 Patreon**：[完整文章與提示詞模板](https://www.patreon.com/GaryChen/posts/cong-mcp-a2a-dao-164872945/)

