---
title: "CatDesk：把 ChatGPT 變成本地 Coding Agent，不用 API、不用 Codex 額度（ChatGPT Plus 就夠了）"
date: 2026-08-31
description: CatDesk 是一款開源的 Rust 工具，讓你能用 ChatGPT Web 的 Custom Connector 功能，把 ChatGPT 變成能读写檔案、跑命令的本地 Coding Agent。不需要逆向工程、不用 API、不需要 Codex，只要有 ChatGPT Plus 訂閱就夠了。
tags:
  - open-source
  - rust
  - mcp
  - coding-agent
  - chatgpt
cover: /assets/images/catdesk/preview.gif
---

# CatDesk：把 ChatGPT 變成本地 Coding Agent

![CatDesk 在 ChatGPT Web 中](/assets/images/catdesk/preview.gif)

> **An open-source tool that lets you use ChatGPT Chat as a local coding agent.**
> 不需逆向工程、不用 API、不用 Codex、不用 Work 模式，只要 ChatGPT Plus 訂閱就夠了。

---

## 📊 專案速覽

| 項目 | 資料 |
|------|------|
| **名稱** | CatDesk |
| **作者** | Xeift |
| **授權** | MIT |
| **Stars** | ⭐ 110（2026-08-31） |
| **Forks** | 25 |
| **開啟 Issue** | 3 |
| **開發語言** | Rust |
| **版本** | 持續更新 |
| **建立時間** | 2026-03-18（約 6 個月） |
| **分发方式** | npm (`npm install -g catdesk`) |
| **MCP 版本** | `2026-07-28` |

---

## 🎯 什麼是 CatDesk？

### 核心概念

> **ChatGPT Web + CatDesk = 降版的 Codex**

CatDesk 是一個跑在**本地的 MCP Server**，讓 ChatGPT Web 透過「Custom Connector」功能連接到它。連接後，ChatGPT 就能像 Codex 一樣：

- ✅ **读写你的檔案**
- ✅ **執行_shell 命令_
- ✅ **控制瀏覽器**（可選）
- ✅ **管理進程**

### 為什麼要叫「CatDesk」？

專案內建了一隻可愛的**鯊魚貓（Binagotchy）**吉祥物，作者原本就做了它，後來決定放進專案裡。每次啟動時會隨機生成一隻，喜歡的話可以設為你的夥伴。

<img src="/assets/images/catdesk/preview.gif" alt="Binagotchy" width="200" />

---

## 💡 為什麼需要 CatDesk？

### 背景問題

如果你常用 AI 編碼工具，可能遇過這些情況：

| 工具 | 問題 |
|------|------|
| **Codex** | 額度用超快，第一天就燒光，要等 7 天才 reset |
| **Claude Code** | 5 小時額度限制（💀 RIP） |
| **Antigravity** | 表現好但額度也有限 |

### CatDesk 的解法

> **大多數有 Plus 訂閱的人，一週用不到 10% 的「思考訊息」额度**
> 為什麼不拿你的 3,000 則每週訊息來寫程式呢？

| 項目 | ChatGPT Chat + CatDesk | Codex | OpenAI API |
|------|----------------------|-------|-----------|
| **使用量** | 3,000 則/週 | 慷慨的週額度（但燒得快） | 用多少付多少 |
| **優點** | 穩定、不需額外付費、近乎無限* | 穩定、不需額外付費 | 穩定 |
| **缺點** | 不如原生 Codex 順 | 額度很快用完 | Token 昂貴 |

\* 假設你每天睡 6 小時，天天使用 CatDesk：`3,000 ÷ (24−6) ÷ 7 = 23.8` 則/小時。因為思考與工具呼叫耗時，很難用盡每週 3,000 則。

---

## 🏗️ 運作原理

```text
1. 需要 ChatGPT Plus 或更高訂閱
        ↓
2. CatDesk 在本地以 MCP Server 身分執行
   （能跑命令、改檔案，像 Codex 一樣）
        ↓
3. 用 ChatGPT Web 的 Custom Connector 連接 CatDesk
   （Plus/Pro 用戶獨享功能）
        ↓
4. 完成！ChatGPT Web 現在能控制你的電腦寫程式
```

**重點**：作者先用 GPT-5.2 測試，效果不佳；改用 **GPT-5.4 Thinking** 後發現效果驚人。GPT-5.5、GPT-5.6 更順滑，尤其是 GPT-5.6 對使用 CatDesk 特別強，而且很快。

```text
ChatGPT Web + CatDesk
= 降版的 Codex
= OpenClaw（但沒有 cron 等主動工具）
```

---

## 🔑 核心功能：工具（Tools）

CatDesk 有兩種本地工具模式：

| 模式 | 工具數量 |
|------|---------|
| **`multi-tools`**（多工具） | 10 個工具 |
| **`read-only`**（唯讀） | 3 個工具 |

### multi-tools 模式的完整工具列表

| 工具 | 類型 | 功能 |
|------|------|------|
| **`catdesk_instruction`** | 指南 | 回傳 CatDesk 使用說明，並渲染 Binagotchy |
| **`read`** | 讀取 | 讀取工作區內的一或多個文字檔案 |
| **`search`** | 讀取 | 用 `rg` / `grep` / 內建掃描搜尋工作區文字 |
| **`write`** | 寫入 | 建立或覆寫檔案 |
| **`edit`** | 寫入 | 原子式的受保護替換/區間編輯 |
| **`delete`** | 寫入 | 刪除檔案或資料夾 |
| **`run_command`** | Shell | 執行短命令並等待完成 |
| **`start_command`** | 工作 | 啟動長時間命令，立即回傳 job ID |
| **`poll_command`** | 工作 | 讀取背景命令的增量輸出與狀態 |
| **`cancel_command`** | 工作 | 停止背景命令及其子行程樹 |

### 長時間命令設計

編譯、安裝依賴、長時間測試、dev server 等應該用：

```
start_command → poll_command（搭配 nextCursor）
```

- 長時間命令刻意與 MCP HTTP 請求的生命週期**解耦**
- 回應有大小限制，若 `hasMoreOutput: true`，要繼續用 `nextCursor` 輪詢
- `run_command` 適合短命令，最長 120 秒 timeout

---

## 📚 上下文窗口（Context Window）

ChatGPT Web 的上下文與 Codex CLI 不同：

| 層級 | CatDesk + ChatGPT Web（in + out = 總和） | Codex CLI（總和） |
|------|----------------------------------------|-----------------|
| **Plus** | 128K + 128K = **256K** | 258K（實驗性 1M） |
| **Pro** | 272K + 128K = **400K** | 258K（實驗性 1M） |

---

## 🖥️ 技術架構（Stack）

| 層 | 技術 |
|----|------|
| **核心** | Rust |
| **MCP Server** | 自實作（不用 SDK） |
| **MCP 版本** | `2026-07-28` |
| **伺服器** | Axum + Tokio |
| **TUI** | Ratatui |
| **通道** | ngrok |
| **瀏覽器控制** | chrome-devtools-mcp |
| **Widget** | HTML + JavaScript |
| **分發** | npm |

---

## ⚡ 快速開始（Quickstart）

> [!CAUTION]
> 此工具很強大，可能**格式化你整個硬碟**或產生意外結果。
> 建議在 **VM 或容器**（DevContainer 是不錯的選擇）中執行。
> 把它當作 OpenClaw：容器化、隔離。

### 步驟 1：安裝

```bash
npm install -g catdesk
```

### 步驟 2：執行

```bash
catdesk
```

啟動時選擇模式：
- `Control Computer`（控制電腦）
- `Control Browser`（控制瀏覽器）
- `Both`（兩者）

進階設定：
- 按 `l` 在英文/繁體中文間切換（設定存到 `~/.catdesk/config.toml`）
- 若啟用瀏覽器控制，選一個受支援的 Chromium 瀏覽器
- 首次啟動需輸入 **ngrok authtoken** 與 **ngrok static domain**（從 [ngrok dashboard](https://dashboard.ngrok.com/get-started/setup) 取得）
- 預設監聽 `port 3200`，可用 `PORT` 覆蓋
- 工作區根目錄預設為目前工作目錄，可用 `WORKSPACE_ROOT` 覆蓋

### 步驟 3：等待 TUI 顯示 MCP Server URL

### 步驟 4：開啟 ChatGPT 連接器設定

[chatgpt.com/plugins#settings/Connectors](https://chatgpt.com/plugins#settings/Connectors?create-connector=true)

### 步驟 5：填寫連接器表單

| 欄位 | 填寫 |
|------|------|
| **Name** | `CatDesk` 或任意名稱 |
| **MCP Server URL** | TUI 中顯示的完整 URL |
| **Authentication** | `None` |

### 步驟 6-7：建立並連接

1. 點 `I understand and want to continue`
2. 點 `Create`，再點 `Connect`
3. **權限預設為 Allow read actions**；為最順暢體驗，建議設為 **Allow all actions**（等同 Codex 的 `--yolo`，但需谨慎）

### 步驟 8：加入 Custom Instructions

```text
CatDesk is a coding tool and a custom connector.
Always use CatDesk if the user wants to do anything
related to file operations.
Always call `catdesk_instruction` after `list_resources`,
and follow the instructions it contains.
```

### 步驟 9：開始使用

**重要提示**：
- 讓 ChatGPT 自動決定用哪個連接器。也可用 `/` 或 `@` 手動選擇，這樣 ChatGPT 只能存取選中的連接器，可提高穩定性（但 `web.search` 與 `web.open` 會停用）

<img src="/assets/images/catdesk/connector_slash.png" alt="用 / 選擇 CatDesk" width="300" />
<img src="/assets/images/catdesk/connector_at.png" alt="用 @ 選擇 CatDesk" width="300" />

- **每個小功能開新 session** 可提昇效能、避免高記憶體使用
- 需要上下文時，可讓 ChatGPT 建立 handoff note 貼到新 session
- 超過 50+ 工具呼叫後會變得**非常卡**

<img src="/assets/images/catdesk/high_ram_usage.png" alt="3.9 GB 記憶體使用" width="300" />

---

## 🔒 安全性（Safety）

> [!CAUTION]
> **不要與任何人分享 `MCP Server URL`**
> 擁有該 URL 的人就能存取你的電腦。

### URL 結構

| 部分 | 範例 | 說明 |
|------|------|------|
| **Public URL** | `https://xxxx.ngrok-free.dev` | 你的 ngrok 固定網域 |
| **Random path** | `/Ab3kL9xQ2pTm7VhC` | 首次啟動時生成的隨機路徑 |
| **MCP endpoint** | `/mcp` | 實際的 MCP 端點 |

完整 URL 長這樣：

```text
https://xxxx.ngrok-free.dev/Ab3kL9xQ2pTm7VhC/mcp
```

固定網域與隨機路徑都持久化在 `~/.catdesk/config.toml`，所以完整 URL 在各次啟動間保持不變，只需設定一次連接器。

---

## 📂 常見問題（FAQ）

### 可以關掉紅色的 CSP 按鈕嗎？

可以。開啟 [Advanced connector settings](https://chatgpt.com/#settings/Connectors/Advanced)，開啟 `Enforce CSP in developer mode`，即可移除紅按鈕。CatDesk 會自動把目前 ngrok 網域加進 widget CSP，所以開 CSP 強制後 widget 仍能運作。

<img src="/assets/images/catdesk/csp_button.png" alt="紅色的 CSP 按鈕" width="200" />

### 為什麼連接後要重複連接？

這是 ChatGPT 的 bug（作者後來發現已被修復）。最可靠方式是**移除 CatDesk 再重新安裝**（步驟 2–7）。

### CatDesk 能用在其他 app 嗎？

理論上可以，例如支援 custom remote MCP server 的 Claude。不過因為 Claude Chat mode 與 Claude Code 共用相同的使用額度，實際上較少人這麼做。

### Token 如何計算？

CatDesk 向 ChatGPT Web 取得非官方估算，用 `o200k_base` tokenizer（GPT-5.5 系列家族）：

| 欄位 | 符號 | 含意 | 價格 |
|------|------|------|------|
| `inputTokens` | `↓` | 工具輸入 ≈ LLM 輸出 | ≈ $30 / 1M 輸出 token |
| `outputTokens` | `↑` | 工具輸出 ≈ LLM 輸入 | ≈ $5 / 1M 輸入 token |
| `totalTokens` | `Σ` | input + output | 兩者相加 |

### 什麼是 Workspace？

Workspace 是 CatDesk 允許操作的根目錄。預設為你啟動 CatDesk 的目錄，可用 `WORKSPACE_ROOT` 覆蓋。工具以它為基礎路徑，工作區外的路徑會被拒絕。

### AGENTS.md 要放哪裡？

有三個位置，CatDesk 會依序檢查：

1. Workspace root
2. `~/.catdesk/AGENTS.md`
3. `~/.codex/AGENTS.md`

---

## 📦 競品比較

| 專案 | 說明 |
|------|------|
| **[CatDesk](https://github.com/Xeift/CatDesk)** | 專為 ChatGPT Chat + Custom Connector 設計 |
| **[Desktop Commander](https://github.com/wonderwhy-er/DesktopCommanderMCP)** | 通用目的 MCP：檔案、終端、進程管理 |
| **[DevSpace](https://github.com/Waishnav/devspace)** | 自架 MCP，把 Codex 風格帶到 ChatGPT |
| **[CodexPro](https://github.com/rebel0789/codexpro)** | 本地 MCP，限授權的 repo |
| **[ChatGPT Local Coder](https://github.com/hoangcoderr/chatgpt-local-coder)** | 給 ChatGPT Web 檔案、Shell、Git、patch、上下文工具 |
| **[Proxide](https://github.com/tt-a1i/proxide)** | Agent-agnostic 工作區橋接 |

---

## 🎯 適合誰使用？

| 使用者 | 適用原因 |
|--------|---------|
| **Codex 額度用超快的人** | 用 ChatGPT Plus 的 3,000 則週額度 |
| **網頁開發者 / 爬蟲開發者** | CatDesk 讓 ChatGPT 透過 chrome-devtools 讀元素、控制瀏覽器 |
| **想省成本的人** | 不用 API、不用額外付費 |
| **ChatGPT Pro 用戶** | 可享用 400K 上下文窗口 |

---

## 總結

CatDesk 是一個設計精巧的開源工具，核心亮點在於：

```text
ChatGPT Web + Custom Connector + 本地 MCP Server
= 降版的 Codex 體驗，且额度幾乎無限
```

| 亮點 | 說明 |
|------|------|
| **省成本** | 用 Plus 訂閱的 3,000 則週額度，不用 API 付費 |
| **易部署** | `npm install -g catdesk` 一行搞定 |
| **功能強** | 10 個本地工具，含檔案读写、命令執行、進程管理 |
| **瀏覽器控制** | 整合 chrome-devtools，適合爬蟲與網頁開發 |
| **安全隔離** | 建議用 VM/容器，URL 隨機路徑保護 |
| **有趣** | 內建 Binagotchy 鯊魚貓吉祥物 |

如果你已經在用 ChatGPT，CatDesk 是值得試一試的開源工具！

---

*本文於 2026-08-31 整理自 [github.com/Xeift/CatDesk](https://github.com/Xeift/CatDesk)*
