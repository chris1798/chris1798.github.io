---
title: "Paperclip 專案解析：開源的「AI 代理商公司」管理控制台"
date: 2026-11-13
description: Paperclip 是_paperclipai_開源（MIT）的 AI agent 編排平台——Node.js server + React UI，把 Claude Code、Codex、OpenClaw、Cursor、Gemini CLI、Hermes 等各種 agent 組織成有組織架構、預算、治理與目標對齊的「公司」。本文整理其四大支柱、系統架構、安装方式、生态與適用場景。
tags: [AI, AI Agents, 代理編排, 開源專案, TypeScript, 工作流自動化, MCP, 專案管理]
---

# Paperclip 專案解析：開源的「AI 代理商公司」管理控制台

**Paperclip** 是 Paperclip Labs 開源的 AI agent 編排平台，README 的一句話定位非常直白：

> **The open-source app everyone uses to manage agents for work.**
> **If OpenClaw is an *employee*, Paperclip is the *company*.**

它是一個 Node.js server + React UI，把一群 AI agent（Claude Code、Codex、OpenClaw、Cursor、Gemini CLI、OpenCode、Hermes、Grok Build、Kimi Code⋯）編織成一家「公司」：有組織架構圖、職位與匯報線、預算與成本管控、審批治理、目標對齊，而人類管理者看到的就是**一個長得像任務管理工具的儀表板**。

- 倉庫：<https://github.com/paperclipai/paperclip>
- 官網 / 文件：<https://paperclip.ing> / <https://docs.paperclip.ing>
- 授權：MIT（© 2026 Paperclip Labs, Inc）
- 統計（2026-11-13 查詢）：**113,555 顆星**、18,844 forks、約 **264 位貢獻者**、已合併 **超過 5,900 個 PR**、最新 release `v2026.1106.0`。自 2026-03-02 開源以來，8 個多月衝上十萬星，是目前 AI agent 基礎設施賽道成長最快的專案之一。

## 它在解決什麼問題？

README 的「 Problems Paperclip solves」表寫得很直白，說的就是很多重度 agent 使用者的日常：

| 沒有 Paperclip | 有 Paperclip |
| :--- | :--- |
| 開著 20 個 Claude Code 分頁，記不得每個在幹嘛，重開機全丟光 | 任務是 ticket、對話是執行緒，session 跨重開機持久保存 |
| 要手動從各處收集上下文，「提醒」你的 agent 你到底在做什麼 | 上下文從任務→專案→公司目標自動向下流動，agent 永遠知道做什麼、**為什麼** |
| agent 設定資料夾亂成一團，四處重造任務管理與 agent 間溝通 | 組織圖、ticket、委派、治理全部內建——你在經營公司，不是一堆腳本 |
| 失控迴圈燒掉數百美元 token，配额爆了才發現 | 支出追蹤、預算告警、到線自動暫停 |
| 例行工作（客服、社群、報告）要記得手動 kick-off | Routines 按排程自動建立任務、留執行歷史 |
| 有個想法要開 repo、起 Claude Code、開分頁盯場 | 在 Paperclip 建一個任務，coding agent 自己幹到完成，管理 agent 負責審查 |

關鍵主張：**「Manage business goals, not pull requests.」** 你管理的是「把 AI 筆記應用做到 $1M MRR」這種業務目標，而不是逐個 PR。

## 四大支柱（Four Pillars）

Paperclip 自述圍繞組織 AI agent 必備的四件事設計：

| 支柱 | 給誰用 | 涵蓋內容 |
| :--- | :--- | :--- |
| **Agentic Task Manager**——宣告意圖、agent 做事、你驗收 | 所有人，每天 | 任務、審批與 review gate、主動型 agent 同事、可稽核的例程、從 diff / 截圖 / 測試驗證產出 |
| **Org Chart for Agents**——人類與 agent 混合的角色、權限與邊界 | 管理者 | 人機混合組織圖、職責／委派／專精、治理（谁能做什麼）、scoped secrets 與公司邊界、連線權限與責任人身分 |
| **Agent Employee Training**——設計、訓練、評估你的 AI 員工 | 賦能者 | Skill Studio 與全組織共用技能、evals 與存檔測試輸入、主動學習迴圈與品質指標、agent 績效考核、技能版本歷史與回滾 |
| **Agentic OS**——讓工作跑起來的基礎設施 | IT / 平台 | 跨供應商 runtime（任何模型任何 agent）、沙箱、MCP server 整合、SSO / GRC / RBAC 與成本控制、執行歷史與選配 tracing |

## 「Bring Your Own Agent」：只要收得到心跳，就錄取

Paperclip **不是 agent 框架**——它不教你怎麼做 agent，它教你怎麼**經營一家由 agent 組成的公司**。正式支援的 adapter 生態：

- **Claude Code**、**Codex**、**Cursor**（含 Cursor Cloud）、**Gemini CLI**、**OpenCode**、**Pi**、**Hermes（+ Gateway）**、**Grok Build**、**Kimi Code**
- **OpenClaw** 等 HTTP / webhook bot 型 agent（claw 系是旗艦整合對象，topics 裡直接寫 `openclaw`）
- 自訂程序、HTTP endpoint 與外部 adapter 套件可擴編名單（`packages/adapters`、`adapter-plugin.md`）

口號是 **"If it can receive a heartbeat, it's hired."**（收得到心跳就錄取）。每組 agent 可各自選模型與 harness，同時共享同一份任務、技能、權限與歷史。

## 系統架構：控制平面，不是包装殼

README 特別強調「Before you build any of this yourself, know that it already exists」——它是完整的 control plane。核心子系統：

```
PAPERCLIP SERVER（Node.js + 內嵌 PostgreSQL，生產可接外部 Postgres）
 ├ Identity & Access   兩種部署模式（信任本機 / 驗證模式）、人类角色權限、agent API key、短效 run JWT
 ├ Org Chart & Agents  角色、頭銜、匯報線、權限、預算
 ├ Work & Tasks        任務帶 company/project/goal/parent 連結、原子化 checkout + 執行鎖、阻塞依賴、文件/附件/工作產品
 ├ Heartbeat Execution DB 佇列喚醒（合併、預算檢查、工作區解析、secret 注入、技能載入、adapter 呼叫）
 ├ Workspaces & Runtime git worktree 隔離工作區、開發伺服器／預覽 URL、沙箱供應商
 ├ Governance & Approvals 董事會審批流、執行政策 stage、預算硬停、agent 暫停/恢復/終止
 ├ Budget & Costs      以公司/agent/專案/目標/任務/供應商/模型維度記 token 與成本，告警閾值＋硬停
 ├ Routines & Schedules cron / webhook / API 觸發的例行任務
 ├ Plugins             程序外 plugin（能力閘控的 host 服務、排程、工具暴露、UI 擴充）——不改 code 就能擴充
 ├ Secrets & Storage   公司 secrets、加密憑證、本機或 S3 相容儲存
 ├ Activity & Events   所有變更動作寫成持久活動日誌可稽核
 └ Company Portability 組織打包匯出/匯入（agents、skills，自動脫敏 secrets）
        ▲         ▲         ▲         ▲
   Claude Code   Codex   CLI agents   HTTP/web bots
```

其中幾個被點名的「難而正確」的編排細節：

- **原子化任務 checkout**：單一受讓人＋執行鎖，防止多 agent 搶同一任務互相打架。
- **持久工作上下文**：任務、評論、文件留在 Paperclip，支援的 adapter 跨 run 恢復存檔 session。
- **執行期技能注入**：agent 在 runtime 學到 Paperclip 工作流與專案上下文，不用重訓。
- **可回滾的治理**：審批 gate 強制執行，設定變更逐版記錄，壞變更可安全回滾。
- **可負責的連線**：人類存取、agent 資格、gateway 動作權限是三層獨立控制；工具呼叫可「批准一次」或存可撤銷規則。
- **目標感知執行**：任務帶著目標血統（goal ancestry）執行，agent 看到「為什麼」，不只是標題。

## 快速上手

開源、自架、**不需要 Paperclip 帳號**。需要 Node.js 24.11+（原始碼開發再加 pnpm 9.15+）：

```bash
# 官方推薦的一鍵上手（預設信任本機 loopback 模式）
npx paperclipai@latest onboard --yes

# 隔離试玩執行個例（內嵌 Postgres、自動初始化一個 CEO agent、不裝服務）
ANTHROPIC_API_KEY=*** npx paperclipai test-drive
OPENAI_API_KEY=*** npx paperclipai test-drive --harness codex
OPENROUTER_API_KEY=*** npx paperclipai test-drive \
  --harness opencode --model openrouter/anthropic/claude-sonnet-4.5

# 原始碼開發：UI + API 於 http://localhost:3100，自動建立內嵌 PostgreSQL
git clone https://github.com/paperclipai/paperclip.git
cd paperclip && pnpm install && pnpm dev
```

遠端存取建議驗證模式＋私有網路綁定（Tailscale），或用 Docker 部署。生產環境把你的 Postgres 接上即可隨意部署。

有趣的細節：官方甚至建議「**Just ask your agent to install Paperclip**」——把安裝指南丟給你的 agent 讓它自己裝自己，這很符合專案的世界觀。

## 程式碼規模與工程面貌

以 GitHub Languages 統計（位元組數）粗估：

| 語言 | 位元組 | 角色 |
| :--- | :--- | :--- |
| TypeScript | ~163 MB（94%） | server / UI / packages 主體 |
| JavaScript | ~5.9 MB | 工具與腳本 |
| Rust | ~4.5 MB | 原生 Paperclip Runner（自架預設執行器） |
| PLpgSQL | ~0.7 MB | DB migration / 函式 |
| Python | ~0.57 MB | 訂閱登入輔助等 |

Monorepo（pnpm workspace + turbo）頂層結構：`server/`（~4,600 檔）、`packages/`（adapters、mcp-server、paperclip-runner、paperclip-eval-kernel、skills-catalog、teams-catalog、db、plugins⋯）、`ui/`（React）、`tests/`（~2,250 檔）、`doc/` + `docs/`、`cli/`、`skills/`、`docker/`、`.agents/skills`。測試分 Vitest（預設便宜路徑）與 Playwright 瀏覽器 suite 兩層；有 `DESIGN.md`（88 KB 設計紀錄）、`AGENTS.md`、`ROADMAP.md`，還提供 OpenTelemetry 與 Sentry 的選配接點。Telemetry 預設開啟但匿名、有資料契約文件，`PAPERCLIP_TELEMETRY_DISABLED=1` / `DO_NOT_TRACK=1` 可關。

釋放採 CalVer（`v2026.1106.0` 等），穩定高頻出版；官方 FAQ 直接回答「這是維護中的專案還是垃圾？」——**已合併超過 2,700 PR**（實際查询已近 6,000），背後是正式公司（Paperclip Labs，有招聘頁面）加上 Paperclip Cloud 託管版等特清單。

## 它自述「不是」什麼

README 有一節少見的清醒自我定位：

- **不是聊天機器人**：對話錨定在任務、計畫、決策與產出上（實驗性 Agent Chat 可把對話交接成任務）。
- **不是 agent 框架**：不教做 agent，只教經營公司。
- **不只是工作流編輯器**：Routines 運作在有角色、目標、預算、治理的組織裡。
- **不是 prompt 管理工具**：agent 自帶 prompt、模型、runtime。
- **不局限單一 agent、不局限 code review**：從一個 agent 起步，長成有共享技能、委派與審查的團隊；研究、維運、內容等各種工作都放得下。

「What Paperclip is not」加上 Roadmap 的透明度（`⚪ MAXIMIZER MODE`、Self-Organization、自動組織學習等還沒影的事直接列出來），對評估者相當友善。

## 與相近工具的定位差異

| 工具 | 定位 | 與 Paperclip 的關係 |
| :--- | :--- | :--- |
| OpenClaw / Claude Code / Codex 等 | 單個「員工」agent | Paperclip **使用**它們，把它們編成公司 |
| Asana / Trello / Linear | 人類任務管理 | 給 agent 用缺了 checkout 鎖、session 恢復、成本監控、治理這些編排細節（BYO ticket 系統在 Roadmap） |
| n8n / 一般工作流工具 | 固定流程自動化 | Paperclip 的 Routines 運作在組織語境（角色、目標、預算、治理）內 |
| CrewAI / AutoGen 等框架 | 寫 code 定義多 agent 協作 | Paperclip 管的是「已存在的heterogeneous agent 隊伍」，跨供應商、含人類審批 |

## 適用場景與注意事項

**適合**：同時跑多個 agent（尤其 Claude Code 開一排的人）、要 24/7 自主執行但要能稽核與介入、要成本預算硬控、想從手機管理、想建「自主 AI 組織」的團隊。

**評估時留意**：

1. **重量級**：完整控制平面（組織圖、治理、RBAC、secrets、S3、SSO），一個 agent 的小場景會嫌重——雖然官方也說「從一個 agent 開始也能用」。
2. **自架為主的現在式**：託管版 Paperclip Cloud 還在等特清單；自架需 Node 24.11+，遠端要自己處理 Tailscale / Docker / 驗證模式。
3. **權限面很大**：它能注入 secrets、管 GitHub 連線、跑 shell 級 adapter——治理工具齊全，但這代表部署時的安全紀律要跟上（README 有 Superagent 安全姿態徽章與 SECURITY.md）。
4. **Telemetry 預設開**（匿名、可關，私有 repo 參考雜湊後上傳）。
5. 快節奏演進：CalVer 出＋5,900 PR 的合併速度，API 與 UI 變動快，跟版成本要列入考量。

## 結語

Paperclip 押注的趨勢很明確：agent 不會只是一個工具，而是會變成「員工」——到時缺的不是更聰明的 agent，而是**管理員工的系統**：誰做什麼、權限多大、錢花在哪、誰批准、怎麼驗收。它把這層做成了 MIT 授權、可自架、跨供應商的開放控制平面，並用 113k 星與近 6,000 個 PR 證明了速度。對已经在用多 agent 工作流的個人與團隊，它幾乎是現階段「agent 編排層」的標竿實作；想親眼看看「AI 公司怎麼跑」，一行 `npx paperclipai test-drive` 就會給你一間預載 CEO 的小公司。

---

**參考來源**

- GitHub 倉庫 README、ROADMAP.md、AGENTS.md、docs.paperclip.ing（adapters、routines、budgets、deployment-modes、plugins 指南）
- GitHub API 統計：stars / forks / 語言組成 / contributors / merged PR / releases（查詢日期 2026-11-13）
