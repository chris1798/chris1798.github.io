---
title: magpie 完整功能介紹 — 所有 AI Agent 的模型統一網關（20K Stars）
date: 2026-10-23
description: yetone/magpie 專案完整解析：一個本地網關讓 Claude Code 跑 Kimi、Codex 跑 DeepSeek，訂閱額度自動接力、路由群組、外掛中介層、用量統計與跨裝置同步
tags: [AI, LLM, ClaudeCode, Codex, API網關, 開發者工具, 開源專案, macOS]
---

# magpie 完整功能介紹 — 所有 AI Agent 的模型統一網關

![magpie](/assets/images/magpie/icon-256.png)

## 專案總覽

**magpie**（[yetone/magpie](https://github.com/yetone/magpie)）的口號是 **"Every agent's model. One place."**——一個跑在選單列／背景的本機 App + 本地 API 網關，讓你的所有 AI 編碼代理自由換模型：

> **Claude Code on Kimi. Codex on DeepSeek. Gemini CLI on GLM. OpenCode on your ChatGPT plan.**

每個 agent 都把模型設定藏在自家檔案、自家格式、自家 key 裡；你付的訂閱只能餵一個 agent。magpie 把這一切收攏到**一個本機網關（`127.0.0.1:3425`）**背後：從選單列點一下就換模型，額度用完了**無聲切換到下一個帳號**，agent 完全不會看到錯誤。

由 yetone（Obsidian 社群熟悉的名字）於 2026-09 建立，一個月內衝到近 2 萬星。

## 📊 基本資訊

| 項目 | 數值 |
|------|------|
| GitHub Stars | **19,975** ⭐（建立僅約 1 個月） |
| Forks | 1,518 |
| 建立時間 | 2026-09-23 |
| 最後推送 | 2026-10-23（高度活躍） |
| 語言 | Go（單機執行檔）＋ JS plugin runtime（Bun） |
| License | MIT |
| 平台 | macOS / Windows / Linux／Docker／Termux |
| 介面 | 選單列 App、視窗、TUI、Web UI、CLI |
| 官網 / 文件 | [usemagpie.ai](https://usemagpie.ai) / [docs](https://usemagpie.ai/docs/start) |

![Star 歷史](/assets/images/magpie/star-history.svg)

## 🎯 核心痛點與定位

**它解決什麼**：你同時用 Claude Code、Codex、Gemini CLI……每個 agent 各有一套 config 檔、base URL、key；訂閱額度各自為政。magpie 讓你可以：

1. **任何 agent 選任何模型**——從一個統一清單挑選，magpie 直接原子化改寫該 agent config 裡關鍵的那個 key（保留註解、順序、格式）
2. **一個供應商到處用**——一份 API key、一個本機模型、或你已登入的 Claude / ChatGPT / Copilot / Gemini / Grok **訂閱方案**都能餵給所有 agent
3. **額度斷電不斷線**——路由群組自動換下一個帳號／模型

官方也直說：如果你只用一個 agent 配原廠訂閱，**不需要它**。

## 🤖 支援的 Agent（50+）

Claude Code、Claude Desktop、Codex、Gemini CLI、Antigravity CLI、OpenCode、Cursor CLI、Zed、VS Code Chat、Copilot CLI、JetBrains Air、Goose、Cline、Qwen Code、Kimi Code、Devin、Hermes Agent、AstrBot……（完整清單見 README；只顯示你機器上已安裝的）。

任何能吃 base URL 的工具也能直接掛網關：

```sh
export OPENAI_BASE_URL=http://127.0.0.1:3425/v1   OPENAI_API_KEY=magpie
export ANTHROPIC_BASE_URL=http://127.0.0.1:3425   ANTHROPIC_API_KEY=magpie
export GOOGLE_GEMINI_BASE_URL=http://127.0.0.1:3425 GEMINI_API_KEY=magpie
```

## 🏗️ 架構：四協議翻譯網關

網關同時說 **OpenAI Chat、OpenAI Responses、Anthropic Messages、Gemini** 四種 API 方言，並互相翻譯——**串流（streaming）、tool calls、reasoning 都覆蓋**。這是它的技術核心：Claude Code 的 Anthropic 請求可以送到 DeepSeek，反過來 Codex 的 OpenAI Responses 請求可以送到 Kimi。

![架構圖](/assets/images/magpie/architecture.svg)

## 📦 功能全覽

### 1. Agents 頁與 Profiles

統一模型清單（`provider/model` 格式）＋每個 agent 可自訂短清單。**Profiles**（如 "Budget"、"Focus"）一次儲存所有 agent 的配置、一鍵整體切換。

![Agents 頁](/assets/images/magpie/agents.png)

![選單列面板與模型選擇器](/assets/images/magpie/picker.png)

### 2. Providers：預設供應商＋models.dev

40+ 供應商預設：Anthropic、OpenAI、Gemini、Vertex AI、Bedrock、DeepSeek、Kimi、智譜 GLM、MiniMax、StepFun、Qwen、百度千帆、騰訊雲、華為 MaaS、火山方舟、Mistral、Groq、xAI、OpenRouter、Together、Fireworks、SiliconFlow、NVIDIA NIM、ModelScope、Ollama、LM Studio……任何 OpenAI／Anthropic 相容 URL 也行。模型清單來自 [models.dev](https://models.dev)，今早發布的新模型下次重新整理就進清單。每個 key／帳號可各走各的 proxy；可一鍵匯入 CC Switch、Claude Code、Codex 的既有供應商。

![Add provider](/assets/images/magpie/add-provider.png)

### 3. Subscriptions：把訂閱變成供應商（殺手級功能）

已登入的 agent＝一個有模型背後的訂閱，magpie 把它變成餵給**所有其他 agent** 的供應商：

- **Claude**：驅動本機真正的 `claude` binary，透過 MCP 橋接 agent 的工具
- **Codex / ChatGPT**：你的 ChatGPT plan 模型出現在任何 agent 裡
- **GitHub Copilot、Gemini Code Assist、Antigravity、Grok SuperGrok** 等
- 同一訂閱可掛**多個帳號自動 failover**
- **Daily warm-up**：按你選的時間（或上一個額度重置的瞬間）啟動每個 Claude／ChatGPT 帳號的 5 小時視窗

隱私控制：它會讀 agent 的登入檔（Claude Code / Codex 檔案、Keychain）來發現訂閱帳號，可在 Settings → Privacy 關閉或用 `magpie accounts discovery off`。

### 4. Routing Groups：五種路由模式

一個 `group/daily-coding` 讓 agent 一次選一組模型，網關在成員的 key／帳號間分配請求：

| 模式 | 行為 |
|------|------|
| `smart` | 在還有額度的訂閱中，用**最快重置**的那個——減少重置時的浪費 |
| `order` | 第一個用到不能答，再換下一個 |
| `rotate` | 每一輪換下一個成員 |
| `usage` | 最少用的優先 |
| `pace` | 按「每小時剩餘週額度」最多的帳號用，撐到重置 |

細節設計：**對話黏在回答它的帳號上**（保住 vendor 的 prompt cache）；群組可巢狀；**Intent routing** 讓一個你選的小模型讀每個新回合——測試交給強模型、快問快答給便宜模型；Routing 視圖即時顯示每次決策。

![Routing 視圖](/assets/images/magpie/routing.png)

![Intent routing 追蹤](/assets/images/magpie/intent-trace.png)

### 5. Plugins：供應商外掛＋網關中介層

- 直接裝 **npm 上的 OpenCode plugin / pi package**（`magpie plugin add opencode-gemini-auth`），plugin 自帶登入流程，其模型像普通供應商一樣可用；執行期用 Bun
- **Gateway middleware**：JS 攔截每個請求／串流事件／回覆——`onRequest` 可改寫或拒絕請求、`onEvent` 看每個 stream event、`onResponse` 看完整回覆；hook 出錯或超時則原樣放行。官方提供與 [New API](https://github.com/QuantumNous/new-api) channels 相同 JSON 格式的現成中介層：`param-override`、`model-map`、`system-prompt`、`word-guard`（敏感詞過濾）、`think-tags`

```js
// alias.middleware.js — magpie plugin add ./alias.middleware.js
export function onRequest(body, ctx) {
  if (body.model === "fast") return { ...body, model: "deepseek/deepseek-chat" };
}
```

### 6. Usage & Cost：用量儀表板

Token／快讀寫／reasoning／呼叫數、依牌價（美元或人民幣）估算成本（可自訂模型單價）、每個 key／plan／帳號的餘額與額度視窗（`magpie quota`）、視窗重置前的提醒、每段 agent 對話的成本與標題（一鍵在終端重開 session）、context window 填充度與快取命中率、按帳號／上游 key 的帳單、**OTLP export** 接自家 observability。

![Usage 頁](/assets/images/magpie/usage.png)

### 7. Sharing：跨裝置與團隊

- **區網分享**：開關一按，給每個 client 一個具名 gateway key，各自設每日／每週／每月的 token 與成本上限
- **Remote magpie**：筆電直接用桌上型 magpie 的供應商、帳號、群組
- **Docker**：`ghcr.io/yetone/magpie` 跑在伺服器或 NAS，Web UI 管理
- **Sync**：檔案備份，或經 WebDAV（Nutstore、Nextcloud）、S3、加密 GitHub repo 跨機同步

### 8. 其他亮點

- **Library**：instructions、MCP servers、skills、subagents 寫一次，magpie 按各 agent 的格式寫入各自檔案（且只刪除自己寫入的部分）
- **Web search for any model**：不會搜尋的模型獲得搜尋——可串 Tavily、Brave、Exa、Firecrawl、You.com、SearXNG 等依序 fallback，多 key 輪替；任何 agent 也能把同一個搜尋掛成 MCP server（`web_search` + `web_fetch`）
- **Images and video**：透過 MCP 給任何 agent 一個圖片生成工具（模型自選），Grok 訂閱可生成影片
- **Agents kept current**：顯示每個 CLI 版本並按原安裝方式更新
- **WSL**：Windows 上也能接 WSL distro 裡的 agent 並計入用量

## ⌨️ CLI 快速上手

```sh
curl -fsSL https://usemagpie.ai/install.sh | sh   # 安裝（macOS 簽章+公證、自動更新）

magpie provider add deepseek sk-…                # 預設供應商只需貼 key
magpie claude deepseek/deepseek-v4-pro           # Claude Code 跑 DeepSeek
magpie codex moonshot/kimi-k2.5                  # Codex 跑 Kimi
magpie group add "Opus anywhere" models=claude/claude-opus-5-5,copilot/claude-opus-5.5 routing=smart
magpie claude group/opus-anywhere                # 訂閱間 failover
magpie save work && magpie use work              # profiles
magpie quota                                     # 所有方案剩餘額度
magpie tui                                       # 全部功能在終端裡
```

## 🔒 隱私與遙測

Prompts、回覆、key、帳號**只去你用的供應商**。每日一次的匿名統計（隨機 id、版本、系統、用了哪些 agent/provider/model 的 magpie 內部 id；自己加的供應商只記 `custom`），不含名稱、URL、帳號、key、prompt。可在 Settings → Privacy 或 `DO_NOT_TRACK=1` 關閉。官方 [Privacy 頁](https://usemagpie.ai/docs/privacy)逐項列出所有外傳資料。

## ⚠️ 注意事項

- **不收外部 PR**：只有 maintainer 能開 pull request，提議走 Discord——社群貢獻模式特殊
- open issues 1,500+：專案成長極快、迭代猛，遇到問題先查 Discord
- README 內嵌贊助商連結（APINEBULA、零詞元、Kimi）與 `usemagpie.ai/go/…` referral 跳轉——目錄／預設清單有商業合作成分
- 讀取 agent 登入檔以發現訂閱帳號，隱私敏感者記得關 accounts discovery

## 🆚 與類似工具比較

| | magpie | CC Switch | LiteLLM Proxy |
|---|---|---|---|
| 定位 | 選單列 App＋本地網關，agent×模型全矩陣 | Claude/Codex 配置切換器 | 伺服器端 LLM 網關 |
| 訂閱帳號當供應商 | ✅（Claude/ChatGPT/Copilot…） | 部分 | ❌ |
| 四協議互翻＋路由 failover | ✅ | ❌ | ✅（API 間） |
| 用量／成本儀表板 | ✅ | ❌ | 進階版有 |
| 安裝門檻 | 單執行檔、GUI/CLI | 單執行檔 | Python/Docker 服務 |

對個人多 agent、多訂閱的開發者是降維打擊；團隊伺服器場景 LiteLLM 仍更常見。

## 🔗 參考連結

- 專案：<https://github.com/yetone/magpie>
- 官網／下載：<https://usemagpie.ai>
- 文件：<https://usemagpie.ai/docs/start>｜[Reference](https://github.com/yetone/magpie/blob/main/docs/reference.md)
- 社群外掛目錄：<https://github.com/magpie-community/plugins>
- Discord：<https://discord.gg/vGSnD3ZKQF>
