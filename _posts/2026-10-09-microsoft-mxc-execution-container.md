---
title: "Microsoft MXC 完整功能介紹：為 AI Agent 打造的政策式沙箱執行容器"
date: 2026-10-09
description: Microsoft eXecution Container（MXC）是微軟開源的跨平台沙箱代碼執行系統，用統一的政策模型與 Rust/.NET/Node SDK，讓 AI 模型輸出、外掛與工具等不受信任代碼在 Windows、Linux、macOS 上安全執行。
tags: [microsoft, mxc, sandbox, ai-agent, security, rust, open-source]
---

# Microsoft MXC 完整功能介紹：為 AI Agent 打造的政策式沙箱執行容器

## 專案概況

| 項目 | 內容 |
|---|---|
| 專案名稱 | Microsoft eXecution Container（MXC） |
| 官方倉庫 | https://github.com/microsoft/mxc |
| 定位 | 政策驅動（policy-driven）、分層隔離的代碼沙箱執行系統 |
| 開發語言 | Rust（核心引擎）＋ TypeScript / C# SDK |
| 授權 | MIT |
| 支援平台 | Windows 11、Linux、macOS |
| Stars / Forks | 約 2,100+ / 115（2026-10 實測） |
| 建立時間 | 2026-02（2026 Build 大會發表，2026-10 官方部落格正式推出） |
| 分發管道 | crates.io（Rust）、NuGet（.NET）、npm（Node） |

MXC 要解決的問題非常具體：**AI Agent 會即時生成並執行代碼**——模型輸出、工具呼叫、外掛程式都是「不受信任的代碼」。讓它們直接跑在你的電腦上，等於把整個檔案系統、網路和剪貼簿交給一段沒人審查過的程式。MXC 提供一個 SDK 層級的沙箱：你的 App 宣告「這個工作需要哪些權限」，MXC 驗證政策、挑選合適的隔離後端，然後把代碼放進容器裡執行。

微軟官方部落格提到，GitHub Copilot 已用 MXC 做沙箱執行，而 Anthropic Claude Code、Box、Egnyte、Heidi Health、**Hermes Agent（Nous Research）**、Manus、Perplexity、Raycast、Simular 等廠商也都計畫支援 MXC。

## MXC 是什麼、怎麼嵌入你的應用

MXC 不是獨立執行的容器服務或 daemon，而是一個**編譯進你 App 裡的 SDK 依賴**：

```
你的應用程式（Launch API）
        │
        ▼
MXC SDK（Rust / .NET / Node，in-process）
        │
        ▼
選定的隔離後端（in-process）
        │
        ▼
隔離中的工作負載（ProcessContainer / Bubblewrap / Seatbelt / MicroVM …）
```

應用只需要指定三件事：

1. **容器類型**（用哪個後端）
2. **containment 規則**（檔案、網路、UI 政策）
3. **要執行的命令**

MXC 負責驗證請求合法性、選擇後端、啟動容器並執行工作負載。

## 核心功能

### 1. 多隔離後端（Multi-backend containment）

MXC 最大的特色是「一套政策模型，多種隔離強度」——從 OS 原生行程沙箱到完整 VM 都能用同一個 API 驅動：

| 執行平台 | 預設後端 | 其他後端 | 隔離機制 |
|---|---|---|---|
| Windows 11 x64/ARM64 | `processcontainer` | `windows_sandbox`*、`wslc`、`microvm`*、`hyperlight`*、`isolation_session` | AppContainer SID、WFP 防火牆規則、Hyper-V |
| Linux x64/ARM64 | `bubblewrap` | `lxc`、`microvm`、`hyperlight` | user namespace、namespaces、KVM |
| macOS ARM64/x64 | `seatbelt` | — | Apple 内核 Seatbelt（App Sandbox 同款） |

（* 為 experimental 實驗性後端）

各後端重點：

- **ProcessContainer（Windows 預設）**：以容器 SID 為範圍的 AppContainer/BaseContainer，搭配 WFP egress 過濾規則與 per-container WinHTTP 代理，每次啟動不需要 UAC 提示。
- **Bubblewrap（Linux 預設，stable）**：用 Linux user namespaces 做**非特權沙箱**，不需要 root、不需要容器 runtime，kernel 3.8+ 即可。
- **Seatbelt（macOS 預設）**：MXC 把你的 JSON 政策翻譯成 Seatbelt profile，在 `fork()` 與 `exec()` 之間用 `sandbox_init()` 套用——和 Mac App Store 的 App Sandbox 同一套内核機制。無 root、無 daemon、無安裝，沙箱生命週期就是被包住的那棵行程樹。
- **LXC**：完整 Linux 容器（PID/mount/network/user namespaces + iptables），適合需要強隔離的場景。
- **WSLC（WSL Container）**：在 Windows 上跑 Linux 容器，透過 WSLC SDK；stable 後端，需 WSL 2.9.9+。
- **Windows Sandbox**：一次性可棄式 VM 或 state-aware 共用 VM（經 detached daemon 管理），實驗性。
- **Nanvix MicroVM**：輕量 VM，**冷啟動約 100 ms、常駐記憶體約 100 MB**，Windows 走 WHP、Linux 走 KVM 的硬體隔離。
- **Hyperlight**：Hyperlight + Unikraft unikernel 微 VM，guest 從 warm snapshot 還原，x86_64（KVM/WHP）。
- **IsolationSession**：Windows 的 session 級隔離（網路不可限制，政策需如實宣告 allow）。

### 2. 政策驅動的沙箱（Policy-driven sandboxing）

所有容器用**版本化的 JSON 設定**描述（stable schema `1.0.0`，dev schema `1.1.0-alpha`），支援 JSON Schema 自動補全與驗證。三大政策面：

**檔案系統政策**
```json
"filesystem": {
  "readwritePaths": ["C:\\temp"],
  "readonlyPaths":  ["C:\\data"],
  "deniedPaths":    ["C:\\Windows"]
}
```

**網路政策（方向式 egress / ingress）**
```json
"network": {
  "egress": {
    "default": "deny",
    "allow": [{ "to": [{ "cidr": "140.82.112.0/20" }],
               "ports": [{ "protocol": "tcp", "port": 443 }] }]
  },
  "ingress": { "default": "deny", "hostLoopback": "deny" }
}
```
- 預設全拒絕（deny-by-default）：省略 `network` 就是 egress/ingress 全 deny。
- 支援 CIDR、協定、埠號的明確 allow/deny 規則（明確 deny 永遠勝過 allow）。
- 也可改用 `runtimeConfig.networkProxy` 走呼叫方自管的 HTTP/S 代理（由代理負責目的地過濾）；兩種模式不可混用。
- 舊版欄位（`defaultPolicy`、`enforcementMode`、`allowedHosts`、`network.proxy` 等）已淘汰，v0.9+ 精確契約會直接拒絕。

**UI 政策**：剪貼簿、顯示、GUI 存取的控制（如 Seatbelt 的 `guiAccess`、ProcessContainer 的 UIPolicy schema）。

**程序設定**：`commandLine`（必要）、`cwd`、`env`、`timeout`（毫秒，0 = 不設限）、`lifecycle.destroyOnExit` 等。

### 3. 狀態感知容器生命週期（State-aware lifecycle）

除了「跑一次就結束」的 one-shot（`run` / `spawn`），MXC 支援持久容器完整生命週期：

```
provision → start → exec（可重複多次）→ stop → deprovision
```

適合 Agent 多輪工具執行、需要保留容器狀態（工作目錄、已裝好的環境）的場景。Windows Sandbox、WSLC、IsolationSession 等都有 state-aware 路徑。

### 4. 三語言 SDK，版本化 API

| SDK | 安裝方式 |
|---|---|
| Rust | `cargo add mxc-sdk`（crates.io） |
| .NET | `Microsoft.Mxc.Sdk`（NuGet，含原生 runtime 資產） |
| Node | `npm i @microsoft/mxc-sdk`（含原生 runtime 資產） |

公開 API 統一掛在 `mxc_sdk::v1` / `Microsoft.Mxc.Sdk.V1` / `@microsoft/mxc-sdk/v1` 命名空間下，與原生 wire contract 獨立版本化。Node 端最小範例：

```typescript
import { spawn, type ContainerRequest } from '@microsoft/mxc-sdk/v1';

const request: ContainerRequest = {
  command: 'node -e "console.log(\'hello from container\')"',
  network: { egress: { default: 'deny' } },
  timeoutMs: 30_000,
};

const child = await spawn(request);
```

SDK 能力對照：`run`（擷取輸出的一次性執行）、`spawn`（串接即時 stdio）、`provisionContainer` / `startContainer` / `exec` / `stopContainer` / `deprovisionContainer`（持久容器），另有 containment 支援探測（dry-run probe）可先問「這台機器上這個後端能不能用」。

**不用 SDK 也行**：平台原生執行器（如 Windows 的 `wxc-exec.exe`、Linux 的 `lxc-exec`、macOS 的 `mxc-exec-mac`）直接吃 JSON 容器請求，適合測試或無法嵌入 SDK 的場景。

### 5. 沙箱除錯工具：Learning mode / Audit mode

沙箱最常見的痛點是「程式跑不起來，因為政策沒給權限」。MXC 提供兩套診斷機制（Windows AppContainer 系後端）：

- **Learning mode（deny-and-record）**：把被拒絕的檔案/註冊機存取記錄成可觀察事件，政策作者據此重建「這個工具实际需要哪些路徑」的政策，而不是猜。
- **Audit mode**：`wxc-exec.exe --audit policy.json`  temporarily 完全關閉沙箱、記錄所有實際存取，產出政策撰寫素材。⚠️ 官方警告：audit 模式下完全沒有隔離，**絕不可用於不受信任的代碼**。
- `--debug` 旗標則輸出 MXC 自身的診斷資訊（不影響工作負載的 stdio）。

### 6. 遥測與隱私控制（Telemetry）

微軟官方 build 可選上傳診斷遥測，但預設關閉，且需同時滿足：個別 run 選擇加入、Windows 使用者明確同意、管理政策允許、App 在請求中啟用遥測選項。管理員只能**封鎖**遥測，不能代替使用者同意。本地開源 build 不往微軟送遥測，非 Windows 平台遥測為 no-op。

## 技術架構

Rust workspace 為主體，TypeScript / C# SDK 經 FFI 綁定：

| 路徑 | 內容 |
|---|---|
| `src/mxc-sdk/src/core/` | 引擎、精確契約（exact contracts）、共享 runtime、遥測、跨後端模組 |
| `src/mxc-sdk/src/backends/` | 各後端的驗證、政策、綁定、執行模組 |
| `src/ffi/` | 語言綁定用的原生介面 |
| `sdk/` | TypeScript 與 C# SDK |
| `schemas/` | 已發布與開發中的 JSON 設定 schema |
| `samples/` | 可跑的 Rust/.NET/Node 範例（fs containment、network containment、PTY 互動、stdio 串流、持久容器、deny 記錄等 10+ 個場景） |

設計上採「exact contract」哲學：每個 schema 版本（0.9.0-alpha、1.0.0、1.1.0-alpha）都是精確契約，舊格式請求會被**明確拒絕**而非靜默遷移——避免政策語意被版本升級悄悄改變。

## 安裝與自建

**一般使用者：直接裝 SDK 套件即可，不需要 clone 倉庫**（見上表）。

**從原始碼建置**（開發 MXC 或要用 standalone 執行器時）：

前置需求：Rust 1.93（由 `rust-toolchain.toml` 釘版本）、Node.js 24+、各後端的平台工具鏈。

```bash
# Windows
build.bat --all

# Linux
./build.sh --all

# macOS
./build-mac.sh --all

# 啟用實驗性後端
./build.sh --with-hyperlight
build.bat --with-microvm
```

## 與近似方案的比較

| | MXC | Docker/容器 | Firecracker | 各 OS 原生沙箱 |
|---|---|---|---|---|
| 定位 | 嵌入 App 的 SDK 沙箱層 | 容器平台 | Serverless microVM | OS 功能 |
| 跨平台統一 API | ✅ 三平台三語言 | 部分 | ❌ Linux 為主 | ❌ 各寫各的 |
| 隔離強度可選 | ✅ 行程沙箱→microVM→VM | 中 | 高 | 單一 |
| 政策即 JSON Schema | ✅ 版本化契約 | compose 檔 | 自建 | 自建 |
| 冷啟動開銷 | 低（processcontainer 近乎零開銷；Nanvix ~100ms） | 秒級 | ~125ms | 零 |
| 為 AI agent 設計 | ✅（Copilot 已採用） | 通用 | 通用 | ❌ |

MXC 的差異點在於「**統一政策模型 + 後端可插拔**」：同一份 JSON 政策，在 Windows 走 ProcessContainer、在 Linux 走 Bubblewrap、在 macOS 走 Seatbelt，需要更強隔離時換成 microVM——應用代碼不用改。

## 適用情境

- **AI coding agent 的沙箱執行**：Copilot 式 agent 執行模型生成的命令時，鎖檔案範圍（只開 repo 與 temp）、鎖網路（只allow 指定 CIDR/代理）。
- **外掛/工具代碼隔離**：插件、MCP 工具、使用者腳本在受控政策下執行。
- **多租戶 SaaS 執行不受信任代碼**：文件處理、報表腳本等。
- **開發除錯**：用 audit/learning mode 反向推導出最小權限政策。

## 小結

MXC 是微軟把「AI agent 執行不受信任代碼」這個新需求標準化的嘗試：它不發明的新的隔離技術（AppContainer、Bubblewrap、Seatbelt、Hyperlight 都是既有 OS 能力），而是把它們包進**一個版本化、政策驅動、跨平台的 SDK 契約**裡，讓任何應用——尤其是 agent 產品——能用同一套 API 獲得從輕量行程沙箱到硬體 microVM 的彈性隔離。對正在做 agent 工具鏈（Open WebUI、LiteLLM、自建 agent）的開發者來說，這是值得關注的 OS 級沙箱標準候選。

## 參考連結

- 官方倉庫：https://github.com/microsoft/mxc
- 微軟官方部落格（2026-10-07）：https://blogs.windows.com/windowsdeveloper/2026/10/07/microsoft-execution-containers-policy-driven-containment-for-ai-agents/
- Rust SDK：https://crates.io/crates/mxc-sdk
- .NET SDK：https://www.nuget.org/packages/Microsoft.Mxc.Sdk
- Node SDK：https://www.npmjs.com/package/@microsoft/mxc-sdk
- 倉庫內文件：`docs/schema.md`、`docs/container-lifecycle.md`、`docs/backends/`、`docs/logging-access-denied.md`、`samples/README.md`
