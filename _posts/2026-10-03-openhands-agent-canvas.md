---
title: "OpenHands 功能總覽：自託管的 AI 開發代理控制中心"
date: 2026-10-03
description: OpenHands（前 OpenHands/OpenHands，89.8k stars）現為 Agent Canvas——把 Claude Code、Codex、Gemini 等编码代理整合成自託管、可自動化排程的開發控制中心。完整功能、架構、安裝方式與比較整理。
tags: [OpenHands, Agent Canvas, AI Agent, 自託管, 自動化, LLM, ACP]
---

# OpenHands 功能總覽：自託管的 AI 開發代理控制中心

![OpenHands Logo](/assets/images/openhands/openhands-logo.png)

![Agent Canvas 自動化介面預覽](/assets/images/openhands/automation-preview.png)

**OpenHands**（[github.com/OpenHands/OpenHands](https://github.com/OpenHands/OpenHands)）是 GitHub 上最受關注的開源 AI 開發代理專案之一。專案現以 **Agent Canvas** 為核心——一個「自託管的開發者控制中心」，用來統一管理與運行各種编码 AI 代理（OpenHands 自身、Claude Code、Codex、Gemini CLI 等），並讓代理依排程或事件自動執行日常任務。

## 基本資訊

| 項目 | 內容 |
|------|------|
| Stars | ~89,800 ⭐ |
| Forks | ~11,900 |
| License | MIT |
| 主要語言 | TypeScript（前端）+ Python（Agent Server/SDK） |
| 現行版本 | Agent Canvas 1.24.0（2026-09-25 發布，發版節奏約每週） |
| 專案狀態 | Beta |
| 官網 | [openhands.dev](https://openhands.dev) |
| 文件 | [docs.openhands.dev](https://docs.openhands.dev) |
| 建立時間 | 2024-03 |

## 核心定位

> **The self-hosted developer control center for coding agents and automations.**

Agent Canvas 把你的编码代理變成一個「自託管、永遠在線的工程團隊」。它是一個開發者控制中心：

- 啟動與代理的對話、管理對話
- 自動化日常任務——例如自動產生報告發佈到 Slack、自動把 GitHub issue 拆解成任務
- 預設在本機運行，也能連到 Docker、VM、雲端等多種「代理後端」
- 可選擇跑在 OpenHands Cloud / Enterprise（商業服務）上

## 核心功能

### 1. 多代理統一介面（ACP Agents）

透過 **Agent Client Protocol（ACP）**——一個以 stdio JSON-RPC 溝通编码代理的標準協議——Agent Canvas 不只跑自家 OpenHands 代理，還能驅動任何第三方代理：

| 代理 | 預設啟動命令 | 訂閱登入（自動偵測） | API Key |
|------|------------|---------------------|---------|
| Claude Code | `npx -y @agentclientprotocol/claude-agent-acp` | Claude Pro/Max 登入（macOS Keychain 或 `~/.claude/.credentials.json`） | `ANTHROPIC_API_KEY` |
| Codex | `npx -y @zed-industries/codex-acp` | ChatGPT 登入（`codex login`，快取於 `~/.codex/auth.json`） | `OPENAI_API_KEY` |
| Gemini CLI | `npx -y @google/gemini-cli --acp` | Google 登入（快取於 `~/.gemini/oauth_creds.json`） | `GEMINI_API_KEY` |
| 自訂 ACP server | 自訂命令 | — | 自訂環境變數 |

運作方式：Agent Server 把代理自己的 CLI 當成子程序啟動並轉發每一輪對話；外部代理管理自己的 LLM、工具與執行，Canvas 只負責送訊息與渲染結果。若本機已登入該代理的 CLI，會自動沿用登入，通常不需要 API Key（訂閱登入優先於 API Key）。

### 2. 多後端切換（Backends）

任何 Canvas 前端可連任何 Agent Server 後端，UI 裡的 backend switcher 可新增/編輯/移除後端（名稱、host URL、API Key）。

- **Local**：本機直接跑（`agent-canvas` 自動建立本地後端）
- **Remote**：同機獨立程序、自託管 VM/容器、團隊共用伺服器
- **Cloud / Enterprise**：OpenHands 託管的沙箱與組織服務
- 支援 VM、Docker、Kubernetes (Helm)、Modal 等自託管後端服務

Settings、LLM 設定、MCP servers、automations 都依「作用中後端」分域——切換後端會一起切換這些設定。

### 3. 自動化（Automations）

Automation Server 讓代理依**排程**或**事件（webhook）**執行。內建 4 種預置自動化：

| 自動化 | 功能 |
|--------|------|
| Issue to Pull Request | 自動實作 issue tracker 的 issue 並建立 PR |
| GitHub PR Review Assistant | 自動審查 PR 並以留言回覆意見 |
| GitHub Repository Monitor | 監控 repo 事件並觸發代理動作 |
| Slack Channel Monitor | 聆聽 Slack 頻道，訊息符合模式時觸發代理 |

- 建立方式：從對話中請 OpenHands「幫你建立自動化」，或從 Automations 檢視的推薦流程
- 部分目錄項目附 **script bundle**（確定性腳本包：polling、去重、固定 API 呼叫），代理只負責需要判斷的部分
- 一個自動化可同時監控多個 repo
- 可整合 Slack、GitHub、Linear、Notion、Datadog 等第三方服務
- 自動化可指定 LLM profile 與 agent profile；與 Git 同步自動化設定

### 4. LLM Profiles（多模型設定檔）

- **Bring your own model**：支援任何 LiteLLM 支援的模型（Anthropic、OpenAI、Mistral、OpenHands provider 等已驗證）
- 每帳號最多 10 個 profile，可命名、編輯、設為預設、刪除
- **對話中即時切換模型**：chat 輸入框的 profile selector，或 `/model` 斜線指令（`/model` 列出、`/model <name>` 切換），不失去上下文
- 常見玩法：強模型規劃 → 低成本模型實作
- **讓代理自己選模型**：OpenHands profile 開啟「Let the agent switch LLM profiles」後，代理取得 `SwitchLLMTool`，會在對話時間軸顯示 `Switch LLM profile` 事件與理由
- 本地 LLM profile 儲存前會先對後端驗證（無效 key / 模型不存在會擋下）

### 5. Agent Profiles（代理設定檔）

- Agent Profile 決定「哪個代理跑對話」；LLM Profile 決定「OpenHands 代理用哪個模型」——兩層分開管理
- 對話開始前可選 agent profile；開始後不能換
- **Secret scope**：可設定 profile 能存取哪些 secrets（All / None / Selected），由 Agent Server 執行管制
- **MCP server scoping**：profile 可限定只使用部分 MCP servers 的工具

### 6. Critic（成功機率評估）

Critic 是额外的評估層：審查代理的工作並預測任務成功機率，結果以「成功likelihood 分數 + 問題標籤」顯示在對話時間軸。可設定低分時代理自動改進。OpenHands 託管的 critic 目前免費（用 OpenHands Provider LLM Key 認證）。僅適用於 OpenHands 代理對話。

### 7. 對話與工作區管理

- 對話 UI：聊天、終端機、瀏覽器、檔案、設定、自動化檢視
- 每個對話可跑在獨立 Docker 容器（`OH_CONVERSATION_RUNTIME=docker`），容器替換後工作區檔案與對話歷史保留
- 支援手機/平板存取

### 8. MCP 與 Plugins

- 支援 Model Context Protocol（MCP）servers，自動化安裝與管理
- Plugins / Agent Plugins Packages 擴展代理能力

### 9. 記憶壓縮（Memory Condensation）

Memory condenser 在長對話中摘要歷史、只保留最重要的資訊，降低延遲與 token 消耗，可設定觸發摘要的事件數。

## 系統架構

![Agent Canvas 架構圖](/assets/images/openhands/architecture.png)

Agent Canvas 是多倉庫系統的一環：

| 倉庫 | 職責 |
|------|------|
| `OpenHands/OpenHands` | Agent Canvas 前端、使用者控制中心、後端選擇、本地堆疊編排 |
| `OpenHands/software-agent-sdk` | Python SDK、Agent Server、agents、tools、conversations、workspaces、events、正式 server API |
| `OpenHands/typescript-client` | 瀏覽器相容的 TypeScript client（Agent Server API） |
| `OpenHands/automation` | 自動化定義、排程、webhooks、執行歷史、派遣 |

- **Agent Server**：單機單 port 的 REST API，可跑多個代理；Canvas 可連多個 Agent Server 並切換
- **Automation Server**：排程/事件觸發，決定何時跑，派遣對話到 Agent Server
- **Ingress**：把前端、Agent Server、自動化流量路由到同一個本地 origin
- 前端是 React + TypeScript（`src/api`、`src/components`、Zustand stores、i18n）

## 安裝方式

**前置**：Node.js 24+、`uv`

### 選項 1：無沙箱（直接裝在本機，代理有完整檔案系統存取權）

```sh
npm install -g @openhands/agent-canvas
agent-canvas
```

可拆分執行：`agent-canvas --frontend-only` / `--backend-only`。UI 在 `http://localhost:8000`。本地監聽預設僅 loopback（127.0.0.1）；`--host 0.0.0.0` 需走 API key 畫面。

### 選項 2：Docker 沙箱

```sh
export PROJECTS_PATH="$HOME/projects"
mkdir -p "$PROJECTS_PATH" "$HOME/.openhands"

docker run -it --rm \
  -p 127.0.0.1:8000:8000 \
  -e AGENT_CANVAS_ALLOW_LAN_SESSION_KEY=true \
  -v "$HOME/.openhands:/home/openhands/.openhands" \
  -v "${PROJECTS_PATH}:/projects" \
  ghcr.io/openhands/agent-canvas:1.24.0
```

代理只能存取 `PROJECTS_PATH` 下的專案。UI 在 `http://localhost:8000/canvas`。

### 選項 3：多 Docker 沙箱（並行多代理）

```sh
npm install -g @openhands/agent-canvas
OH_CONVERSATION_RUNTIME=docker agent-canvas
```

每個新對話一個容器，各自有 Agent Server 與工具；Canvas 在 host 路由對話請求。

### 選項 4：從來源

```sh
git clone https://github.com/OpenHands/OpenHands.git
cd OpenHands && npm install && npm run dev
```

### 自託管（server / 雲端 VM）

最強大的跑法是跑在雲端 server：筆電關機代理仍繼續運行，且方便被 Slack、GitHub、Datadog 等第三方服務觸發。詳見 `docs/SELF_HOSTING.md`（含安全加固）。也可以跑多台後端——例如與團隊共用一台做 code review 與依賴更新的 Agent Server，自己的代理跑在筆電上，同一個 Canvas 前端切換。

## 安全性

- 無沙箱模式代理有完整檔案系統存取權——README 明確警告，建議筆電使用 Docker 沙箱模式
- 本地監聽預設 loopback only，避免 session key 被網路其他機器取得
- 公開/LAN 曝露時不注入 session key，改用 API key 進入畫面；建議設 `LOCAL_BACKEND_API_KEY` 強值
- 自託管建議一般 server 加固：認證、HTTPS、防火牆、謹慎的工作區範圍
- Secrets 集中管理（Settings → Secrets），profile 可做 secret scope 限定

## 與其他代理工具比較

| 面向 | OpenHands Agent Canvas | Claude Code / Codex CLI | OpenClaw 類 |
|------|----------------------|------------------------|-------------|
| 定位 | 自託管控制中心 + 自動化平台 | 單一代理 CLI | 個人助理 gateway |
| 支援代理 | 自家 + 任何 ACP 代理（Claude/Codex/Gemini/自訂） | 僅自家 | 各家 LLM |
| 後端 | 本機/Docker/VM/K8s/Modal/雲端，可切換 | 本機 | 本機 |
| 自動化 | 排程 + webhook 事件、預置 4 種、Git 同步 | 無 | 排程 |
| 模型管理 | 10 個 LLM profile、對話中切換、代理自選 | 固定 | 可切換 |
| 品質評估 | Critic 成功機率評分 | 無 | 無 |
| 部署 | npm 一行 / Docker / 自託管 | CLI 安裝 | CLI 安裝 |
| License | MIT | 專有 | 開源 |

## 總結

OpenHands 從 2024 年的「開源 coding agent」演化成 2026 年的**代理控制中心平台**：把 OpenHands、Claude Code、Codex、Gemini 等代理收進同一個自託管 UI，加上多後端切換、排程/事件自動化、多模型 profile 管理、Critic 品質評估與 Docker 沙箱隔離。適合想把 AI 工程團隊「永遠在線」跑在自己伺服器、並讓代理自動處理 issue→PR、PR review、Slack 監控等日常工作的開發者與團隊。

## 參考連結

- GitHub：[github.com/OpenHands/OpenHands](https://github.com/OpenHands/OpenHands)
- 官網：[openhands.dev](https://openhands.dev)
- 文件：[docs.openhands.dev](https://docs.openhands.dev)
- Agent SDK：[OpenHands/software-agent-sdk](https://github.com/OpenHands/software-agent-sdk)
- Automation：[OpenHands/automation](https://github.com/OpenHands/automation)
- Slack 社群：[go.openhands.dev/slack](https://go.openhands.dev/slack)
