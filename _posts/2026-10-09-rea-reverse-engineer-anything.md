---
title: "REA 完整功能介紹：用 AI Agent 逆向工程任何東西——從 App 行為到原生二進位檔"
date: 2026-10-09
description: morluto/rea 是一個把 AI Agent 接上逆向工程工具的 MCP：分析原生二進位、JavaScript/Electron 應用、.NET 組件、網站、APK、韌體與執行期行為，結果附證據。完整功能、安裝、CLI 與案例整理。
tags: [reverse-engineering, ai-agents, mcp, ghidra, hopper, electron, developer-tools]
---

# REA 完整功能介紹：Reverse Engineer Anything

![REA 在 Hopper 內啟動分析橋，檢視原生二進位檔](/assets/images/rea/rea-hopper-analysis.png)

**REA（Reverse Engineer Anything）** 是一個開源的 MCP（Model Context Protocol）伺服器與 CLI 工具集，把 AI Agent 直接接上專業逆向工程工具鏈。它的核心主張很明確：

> 看到別家 App 裡你想要的功能？讓你的 Agent 用 REA 去調查它——不需要原始程式碼，就能解釋這個功能怎麼運作、給出證據，甚至為你的專案重建一個版本。

一句話定位：**一個 MCP 覆蓋二進位、應用程式與執行期行為的逆向工程。**

## 專案基本資訊

| 項目 | 內容 |
|---|---|
| 倉庫 | [github.com/morluto/rea](https://github.com/morluto/rea) |
| 官方網站 | [rea.tools](https://rea.tools/)（指南與案例研究） |
| 定位 | 用 AI Agent 做逆向工程：從 App 行為一路追到原生二進位 |
| 語言 / 形式 | TypeScript，npm 套件 `rea-agents`（MCP server + CLI） |
| Stars / Forks | 約 27,500 stars / 3,100+ forks（2026-10 實測 API 數據，README 亦慶祝破 20,000 星） |
| 授權 | MIT |
| 建立時間 | 2026-04（成長極快，曾登上 TrendShift 趨勢榜） |
| 執行需求 | Node.js 22.19+ / 24.11+ / 26+ 及 npm |
| 主題標籤 | agent-skills、binary-analysis、decompiler、disassembler、ghidra、hopper、mcp、reverse-engineering、static-analysis 等 |

![REA GitHub star 成長曲線](/assets/images/rea/star-history.svg)

## REA 如何運作

REA 本身不做「AI 猜測式」分析。它的流程是：

1. 你的 Agent（Claude Code、Codex、Cursor 等）透過 **MCP** 呼叫 REA 的分析工具；
2. REA 在**本地**檢查目標——調用 Hopper / Ghidra / IDA 反編譯、解析 JavaScript 模組圖、讀取 .NET metadata、觀察瀏覽器網路行為等；
3. REA 回傳**附帶證據（evidence）的發現**：程式碼、位址引用、來源位置，以及明確標示的「未知項與限制」；
4. Agent 用這些發現追問、解釋行為，或直接**寫出並測試一個實作**。

![REA 調查流程：Agent 提問 → REA 以分析工具檢查與追蹤 → Agent 用回傳的程式碼、引用與未知項去解釋、實作、測試](/assets/images/rea/rea-investigation-flow.svg)

同一套工作流也能從終端機直接用 CLI 跑，結果契約完全相同——這讓 REA 既能當 Agent 的「眼睛」，也能腳本化進 CI 或研究流程。

## 可分析的目標類型（完整功能矩陣）

這是 REA 最核心的能力清單：

| 目標類型 | REA 回傳的內容 | 前置需求 |
|---|---|---|
| **原生二進位檔** | 偽代碼（pseudocode）、組語、字串、符號、呼叫與交叉引用（xrefs） | Hopper、Ghidra 或 IDA |
| **離線 ELF 結構** | Sections、segments、原始符號/重定位、靜態緩解候選 | Linux x64 + 呼叫方提供的 pwntools |
| **EVM 位元組碼** | Dispatch selectors、位元偏移、推斷的引數與可变性 | 本地 raw/hex 載體 |
| **已記錄的 Linux crash** | 原始 notes、每個執行緒的暫存器/信號、可選映射候選 | pwntools；可選 GDB/pwndbg |
| **JavaScript / Electron 應用** | 模組、imports、source maps、路由、IPC 與原生附加模組（native add-on）關係 | 只需 Node.js/npm，**不需任何反編譯引擎** |
| **網站** | 頁面結構、腳本、網路觀察、要求的截圖 | Chrome 系瀏覽器 |
| **已存網路封包（HAR）** | 請求、回應、暴露的 payload 與來源位置 | HAR 檔；Linux 上 mitmdump 處理 mitmproxy 捕獲 |
| **.NET 組件** | Metadata、CIL 指令、宣告的原生相依、建置比較 | 純靜態檢查，不需執行 |
| **Android APK** | Manifest 宣告、類別、反編譯方法與引用 | Headless JADX + 完整 JDK（Linux/macOS） |
| **韌體（Firmware）** | 區域劃分、抽取結果、交接給原生分析 | Binwalk / Unblob（Linux） |
| **套件與資源檔** | 檔案清單、摘要、plist、Apple bundle 結構、抽取的資源 | 內建（Apple 應用分析指南） |
| **程序行為（process）** | 終端輸出、互動、結束與檔案系統觀察、多次執行比較 | Linux/macOS 原生 PTY |

補充設計原則：

- **靜態分析不執行目標**：JavaScript 與 .NET 檢查只讀檔案，不跑應用——安全且可自動化。
- **執行期捕獲會真的執行/互動**：以你的使用者權限運行，每份指南都說明其副作用。
- **原生格式支援依 provider 而異**：Ghidra 甚至支援 16-bit DOS 分析（PC-98 老遊戲可玩）；Windows 上的 Ghidra 支援為 experimental；大型二進位可用 `REA_GHIDRA_STARTUP_TIMEOUT_MS` 拉長啟動期限。

## 安裝與 Agent 整合

### 一行設定 Agent

```bash
npx rea-agents setup
```

Setup 會多選列出支援的 Agent，展示將要修改的設定、經你批准後寫入（並備份既有設定）。之後重啟 Agent 即可。支援的客戶端非常廣：

| 客戶端 | `--client` 值 |
|---|---|
| Claude Code / Claude Desktop | `claude_code` / `claude_desktop` |
| Codex | `codex` |
| Cursor | `cursor` |
| Gemini CLI | `gemini_cli` |
| Windsurf / Devin / OpenCode | `windsurf` / `devin` / `opencode` |
| Antigravity / GitHub Copilot CLI | `antigravity` / `copilot_cli` |
| VS Code / Command Code / Grok Build | `vscode` / `commandcode` / `grok_build` |

任何支援本地 MCP server 的 Agent 都能手動註冊 REA；Grok Bot 則走帳號 connector 的手動路徑。另有 [skills.sh](https://skills.sh/morluto/rea/reverse-engineer-anything) 上的 agent skill，提供調查工作流的指令（skill-only 安裝）。

### 直接問 Agent

```text
理解 Notes app 的搜尋功能怎麼運作，給我看證據，並為我的專案做一個類似功能。
```

### 安裝 CLI 供日常使用

```bash
npm install --global rea-agents
rea --help
```

### 更新

```bash
rea update                      # npm 全域安裝
npx rea-agents@latest setup     # npx 用法（同時刷新 agent 註冊與 skill）
```

## CLI 功能一覽

CLI 與 MCP 共用同一套工作流與證據契約。原生分析指令（以 Ghidra 為例）：

```bash
rea analyze program --provider ghidra --json     # 總覽
rea search  program "keyword" --provider ghidra  # 字串/符號搜尋
rea function program main                        # 函式檔案（dossier）
rea decompile program 0x1000                     # 偽代碼
rea instructions program 0x1000                  # 純組語指令
rea xrefs program 0x1000                         # 交叉引用
rea trace program "keyword"                      # 從線索追蹤到相關程式碼
```

JavaScript/Electron 靜態分析（免引擎）：

```bash
npx -y rea-agents@latest analyze-javascript-application /absolute/path/to/app --json
```

其他關鍵指令：

- `rea providers` / `rea capabilities`：列出可用 provider 與支援操作；provider 選擇可用 `--provider`、環境變數 `REA_ANALYSIS_PROVIDER`，MCP 內則在 `open_binary` 傳 `provider_id`（支援 `auto`）。選定的 provider 綁定整個 session，不會在失敗後被自動替換。
- **分析快照（snapshots）**：`--snapshot path.json` 保存分析結果；目標位元組、操作、參數、provider、設定完全相符時直接復用快取（精確命中時甚至不用啟動 provider 程序）。MCP 端 `open_binary`/`close_binary` 也支援 `snapshot_path`。
- **Evidence 匯入/匯出/比較**：證據記錄保留 artifact 身分、來源位置、觀察與推論，可供後續比對（如 `compare_web_captures` 比對前後兩次網頁觀察）。
- **`rea doctor`**：診斷各 Agent 註冊是否 aligned/stale/missing/invalid，以及分析引擎（如 `rea doctor --provider ID --json`）的就緒狀態。
- **退出碼契約**：`0` 完成（可能含部分證據/警告/未解問題）、`1` 無法完成（結構化輸出說明原因）、`128+N` 信號終止。

## MCP 工具契約（給 Agent 開發者）

REA 的 MCP 介面設計相當嚴謹，值得注意的幾個特性：

- **`binary_session`**：回報現行套件、server、SDK 與協商協議；`result.tool_availability` 給出完整工具清單及每個工具的可用性、原因與補救方式——Agent 可據此動態選擇可呼叫的操作。
- **完整 canonical 工具目錄**：`tools/list` 永遠回傳完整清單（含目前不可用的工具），開/關目標不會觸發 `list_changed` 抖動。
- **Schema 相容性剖面**：輸入 schema 限制巢狀深度（10 層），輸出 schema 以本地引用共享重複定義——刻意避開 recursive schema，兼容各家模型 API 的限制。
- **進度與取消**：session 透過 `analysis_activity` 回報進行中的工作；client 逾時只結束等待，provider 分析繼續進行。
- **生成式目錄**：建置時產生 `product-catalog.json`，机器可讀地列出所有工具、provider 與 CLI 指令，文件站直接提供。

## 實戰案例（Showcases）

官方網站收錄了完整案例研究，幾個代表性例子：

1. **DX-Ball 聲像定位重建**：從聲音呼叫追進「位置→pan」計算的 helper，檢查指令、把不完整的偽代碼還原成 C——重建結果通過 3,205 個原始 x86 測試案例，並**逐 byte 重現全部 63 個編譯後的函式位元組**。
2. **Notion 的 Electron 剪貼簿橋**：找到 renderer 的剪貼簿 API，沿 preload → IPC 一路追蹤到 main process，檢查其 rich clipboard 格式——典型的 Electron 逆向工程流程。
3. **TH04（PC-98 東方舊作）DOS 彈環計算**：檢查 16-bit 指令，還原固定角與瞄準角的計算，再把重建的 C++ 與歷史編譯器輸出比對。

## 隱私與安全

- **分析全程在本地執行**——REA 不會上傳你的 App；只有 Agent 本身（及其模型供應商）會看到回傳的工具結果。
- 快照檔案採 owner-only 權限。
- 專案聲明：REA 提供的是合法逆向工程研究工具，取得授權與遵守法規是使用者的責任。

## 與傳統逆向工程工具的比較

| 面向 | Ghidra / Hopper / IDA 單獨使用 | REA |
|---|---|---|
| 使用方式 | 人工在 GUI 裡翻偽代碼、追 xrefs | Agent 用自然語言提問，REA 自動調引擎並整理證據 |
| JavaScript/Electron | 不支援 | 原生支援，靜態分析免引擎 |
| .NET / APK / 韌體 / HAR | 需另裝插件或工具 | 內建工作流（借助 JADX、Binwalk 等） |
| 執行期觀察 | 需 debugger / 抓包工具手動操作 | 網站、程序行為、網路封包捕獲內建 |
| 證據管理 | 人工筆記 | 結構化 Evidence，可匯入/匯出/比對、快照復用 |
| 定位 | 專業逆向工程師的主力工具 | 把這些引擎變成 AI Agent 的「手與眼」 |

REA 不是取代 Ghidra/Hopper——它是讓你的 Agent 能**驅動**這些引擎、並以證據契約取回結果的一層。

## 快速上手建議

1. `npx rea-agents setup` → 選你的 Agent → 重啟 Agent。
2. 沒有原生引擎也沒關係：先從 JavaScript/Electron 或 .NET 靜態分析開始（免引擎）。
3. 有 Hopper（setup 可經批准代裝）或 Ghidra/IDA 後，再玩原生二進位與 DOS/ELF 分析。
4. 研究流程要反覆查詢同一個二進位時，用 `--snapshot` 保存分析結果。
5. 遇到 bug 先 `rea update`——這個專案迭代非常快，多數問題新版已修。

## 參考連結

- 官方網站與指南：[rea.tools](https://rea.tools/) / [Guides](https://rea.tools/guides/) / [Showcases](https://rea.tools/showcase/)
- 倉庫：[github.com/morluto/rea](https://github.com/morluto/rea)
- npm：[rea-agents](https://www.npmjs.com/package/rea-agents)
- Agent skill：[skills.sh/morluto/rea](https://skills.sh/morluto/rea/reverse-engineer-anything)
- 文件：[Installation](https://github.com/morluto/rea/blob/main/docs/installation.md) · [CLI and Evidence](https://github.com/morluto/rea/blob/main/docs/cli.md) · [MCP contracts](https://github.com/morluto/rea/blob/main/docs/mcp-contracts.md) · [Roadmap](https://github.com/morluto/rea/blob/main/docs/roadmap.md)
- Discord 社群：[discord.gg/GkcryMnJDM](https://discord.gg/GkcryMnJDM)
