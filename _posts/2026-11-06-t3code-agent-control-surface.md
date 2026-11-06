---
title: "T3 Code：一套 App 遠端指揮所有 Coding Agent——Claude Code / Codex / Cursor 的統一控制面"
date: 2026-11-06
description: T3 Code（pingdotgg，Theo 的 t3.gg 團隊出品，48.7k stars，TypeScript，MIT）：不是 harness，是「agent 控制面」——你機器上已登入的 Claude Code、Codex、Cursor、Grok Build、OpenCode、Antigravity 全部接進來，用 iOS/Android App、網頁、桌面端從任何地方指揮。npx t3 up 一鍵遠端、T3 Connect 內建隧道、worktree 並行、PR 整合、checkpoint 回滾，100% 開源免費。
tags: [github, ai-agent, coding-agents, claude-code, codex, cursor, mobile, remote-development, typescript, opensource]
---

# T3 Code：一套 App 遠端指揮所有 Coding Agent——Claude Code / Codex / Cursor 的統一控制面

**T3 Code**（`pingdotgg/t3code`，官方站 [t3.codes](https://t3.codes)）是 t3.gg 團隊（Theo Browne）做的「**agent harness 控制面（control surface）**」：把你電腦上已安裝、已登入的各家 coding agent——Claude Code、Codex、Cursor、Grok Build、OpenCode、Google Antigravity、fx——全部接進一個統一介面，然後用 **iOS / Android App、網頁 App（app.t3.codes）、Electron 桌面端**從任何地方控制它們。

一句話定位：**它不是 agent，是「restaurant」**——官方 FAQ 的比喻：Chef = LLM，Kitchen = harness（Claude Code / Codex），T3 Code = 讓你帶任何廚房進來的餐廳。

## 專案概況

| 項目 | 資料 |
|---|---|
| 倉庫 | [github.com/pingdotgg/t3code](https://github.com/pingdotgg/t3code) |
| Star / Fork | **~48,800 / ~9,700**（2026-11-06 查證） |
| 語言 / 授權 | TypeScript / **MIT** |
| 創建時間 | 2026-02-08（不到一年衝到近 5 萬星） |
| 發布節奏 | 每天多個 nightly（v0.1.8-nightly.20261106.x，單版 129 changes / 44 貢獻者） |
| 平台 | Windows / macOS / Linux 全支援（Intel Mac 只能用桌面版）；Windows 可跑 WSL 內 agent |
| 價格 | **免費**，無付費方案；用自己的 agent 訂閱（BYO sub） |

## 為什麼不是直接用 Claude Code / Codex App？

官方 FAQ 直白回答：受 Codex desktop、Conductor、Claude Desktop、Cursor Glass 啟發，但「沒有一個達到我們的標準」。T3 Code 的四個賣點：

1. **Bring your own sub**——Claude、Codex、Cursor……你已裝什麼就用什麼，不加一層訂閱
2. **Best in class remote**——任何機器上 `npx t3 up`，從任何地方駕駛它（Theo 自述：不到 5% 的 prompt 跑在自己的筆電上）
3. **Best in class mobile app**——iOS / Android 原生 App，手機是遙控器，電腦幹活
4. **Truly 100% open source**——「我們走歪了，你就 fork」

各家 harness 在裡面操作手感幾乎一致——換 agent 不用換工作流。

## 核心功能

### 多 Agent 統一介面
- 支援 **Claude Code、Codex、Cursor、Grok Build、OpenCode、Google Antigravity、fx、Pi、Muse Code**
- 全部走官方 binding（ACP）/ 官方 SDK，官方聲明符合各家 TOS，並與 xAI/Cursor 合作整合
- 同一 provider 可加多組執行緒（工作帳號 + 個人帳號）；也支援 OpenRouter / API key 端點
- 每個 thread 綁一個 **git worktree**：多 agent 並行改代碼互不打架；設定裡有自動清理（有用戶清掉 500 GB）

### 遠端控制（招牌）
- **T3 Connect**：內建遠端通道，流量走 Cloudflare 隧道（你機器上的 cloudflared），中繼只建立連線、**不代理你的 HTTP/WebSocket session**——程式碼和 prompt 只在你機器 ↔ provider 之間流動
- 免費連 3 台機器；綁 T3 Chat Pro 10 台 / Premier 100 台；不想用可走 **LAN pairing 或 Tailscale**
- 手機 App 語音輸入（iPhone/Android 預設裝置端語音識別）

### 開發工作流整合
- **PR 全流程**：thread 綁多個 PR、PR stack UI、review composer 自動補全 @user/#issue、GitLab merge request 與 pipeline job 檢查面板
- **Checkpoints**：用隱藏 git ref 快照工作區（不在你的分支加 commit），回滾時同步 agent 對話狀態
- **權限模式**：per-project 設定 agent 自動執行/審批等級
- **事件驅動架構**：command → event → projection，指令重試冪等；斷線重連從 snapshot 續播
- MCP server：讓你在 ChatGPT、Claude 等其他用戶端反向操控 T3 Code 的 thread

## 安裝

```bash
# CLI（macOS/Linux）
curl -fsSL https://t3.codes/install.sh | sh
# Windows PowerShell
irm https://t3.codes/install.ps1 | iex

t3              # 啟動 server 並開啟本機 web app
t3 service install   # 裝成背景服務
npx t3@latest   # 免安裝試一次
```

桌面版：`winget install T3Tools.T3Code` / `brew install --cask t3-code` / `.deb` / AUR（`t3code-bin`，stable+nightly）/ nixpkgs。

前提：先裝好至少一個 agent CLI 並登入（`claude auth login`、`codex login`、`agent login`(Cursor)、`grok login`、`opencode auth login`…）。Provider 沒出現＝CLI 不在 server 那台機器的 PATH 上。

## 適用場景

- **通勤/咖啡廳遙控家裏 GPU 機跑 agent**：`npx t3 up` + 手機 App，agent 在你桌上那台機器繼續幹活
- **多 agent 並行**：一個 repo 開 N 個 worktree thread，Claude 修 bug、Codex 寫測試、Cursor 重構，全部一屏管理
- **訂閱盤多的人**：Claude + Codex + Cursor 訂閱全利用，不用每個家各開一套 App
- **Code review 流**：PR 建立、review comment、checks、merge 通知全在一個介面，含 GitLab
- **不想被單一廠商綁死**：harness 手感統一，換模型零學習成本

## 與同類方案比較

| | **T3 Code** | Conductor | Codex 桌面 App | Claude Desktop | 純 CLI + tmux |
|---|---|---|---|---|---|
| 開源 | ✅ MIT 100% | 部分 | ❌ | ❌ | — |
| 多家 agent | ✅ 7+ 家 | ✅ 以 Claude 為主 | ❌ 只 Codex | ❌ 只 Claude | 各 CLI 自己切 |
| 手機 App | ✅ 原生 iOS/Android | ❌ | 有限 | 有限 | ❌ |
| 遠端 | ✅ T3 Connect/Tailscale/LAN | 本地為主 | 帳號綁定 | 帳號綁定 | 自己搭 |
| worktree 並行 | ✅ | ✅ | ✅ | — | 手動 |
| 本機模型 | ❌ 明確拒絕 | — | — | — | ✅ |

## 注意事項

- **專案很早期**：官方自述「We are very very early. Expect bugs」；基本不收大功能 PR
- **Claude 5 小時限額消耗較快**：經 Anthropic Agent SDK 的已知 bug（不影響週限額），官方已回報 Anthropic
- **不支持本地模型**：官方立場強硬——「能本地跑的模型做不了有意義的工程」；要接 OpenRouter/API key 可以
- **Telemetry**：發產品使用事件（provider/model/token 總量，無 prompt 無檔案內容）；`T3CODE_TELEMETRY_ENABLED=false` 可關
- 多帳號池管理官方不建議內建（TOS 風險），要玩大池子自己架 CLIProxyAPI 再接 Usage

## 與 Herdr / Agent Desktop 的關係（本部落格前兩篇）

三者互補不互斥：**Herdr** 管「agent 住進終端、跨機面板」；**Agent Desktop** 給 agent「操作桌面 App 的手」；**T3 Code** 給你「手機上指揮所有 agent 的控制面」。T3 Code 站在 harness（Claude Code/Codex）之上，Herdr 站在終端旁，各取所需。

## 參考資料

- 官方站：[https://t3.codes](https://t3.codes)
- GitHub：[https://github.com/pingdotgg/t3code](https://github.com/pingdotgg/t3code)
- FAQ：[docs/user/faq.md](https://github.com/pingdotgg/t3code/blob/main/docs/user/faq.md)
- 遠端存取指南：[docs/user/remote-access.md](https://github.com/pingdotgg/t3code/blob/main/docs/user/remote-access.md)
- 「What is a harness?」：[t3.gg blog](https://t3.gg/blog/post/what-is-a-harness)
- iOS / Android App Store 上架（T3 Code – Remote Claude & More）
