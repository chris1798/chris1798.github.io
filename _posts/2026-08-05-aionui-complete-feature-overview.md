---
title: "AionUi：24/7 全天候 AI Agent 協作桌面應用完整功能介紹"
date: 2026-08-05
description: 深度解析 AionUi（iOfficeAI/AionUi）—— 統一管理 20+ CLI AI Agent 的開源桌面應用，支援並行執行、定時任務、遠端控制與多 Agent 協作
tags: [aionui, ai-agents, claude-code, codex, desktop-app, open-source, multi-agent, automation]
---

# AionUi：24/7 全天候 AI Agent 協作桌面應用完整功能介紹

> **AionUi**（讀音 "eye-on-you"）是一個免費、開源、跨平台的桌面應用程式，使用 Electron、React 和 TypeScript 建構。它以 **24.8k GitHub Stars** 和活躍的開發團隊，成為管理多個 CLI AI Agent 的首選界面。

![AionUi Banner](https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&h=400&fit=crop)

## 產品概覽

### 基本資訊

| 屬性 | 說明 |
|------|------|
| **專案名稱** | AionUi |
| **開發組織** | iOfficeAI |
| **GitHub 倉庫** | https://github.com/iOfficeAI/AionUi |
| **授權** | Apache-2.0（開源免費） |
| **Stars** | 24,800+（截至 2026 年 8 月） |
| **技術棧** | Electron + React + TypeScript |
| **支援平台** | Windows、macOS、Linux |
| **相關專案** | [AionCore](https://github.com/iOfficeAI/AionCore)（Rust 核心）、[OfficeCLI](https://github.com/iOfficeAI/OfficeCLI)（Office 自動化） |

### 核心定位

AionUi 的定位是 **「One desktop. Your AI agents, actually coworking.」**——一個桌面應用，讓 AI Agent 與你並肩工作：讀取檔案、撰寫程式碼、瀏覽網頁、生成圖片、自動化任務。

**與 Cursor、Copilot、Claude Desktop 的差異**：
- **Cursor/Copilot**：主要幫助開發者撰寫程式碼
- **Claude Desktop**：只能與單一模型互動
- **AionUi**：更廣泛、更靈活——AI 隊友處理你整個桌面上的日常工作中，你可以讓 Claude、ChatGPT、Gemini 並行協作

---

## 核心功能一覽

### 1. 20+ AI Agent 統一管理

AionUi 自動偵測本機已安裝的 CLI Agent，並透過 **ACP（Agent Client Protocol）** 統一管理：

#### 已支援的 Agent

| Agent | 開發者 | 用途 |
|-------|--------|------|
| **Claude Code** | Anthropic | 程式碼撰寫與重構 |
| **Codex** | OpenAI | 程式碼生成與修改 |
| **Hermes Agent** | Nous Research | 多工具 AI 助手 |
| **Gemini CLI** | Google | 多模態 AI 助手 |
| **OpenClaw** | OpenClaw | 通用 AI Agent |
| **OpenCode** | OpenCode | 程式碼助手 |
| **Qwen Code** | 阿里雲 | 中文語境程式碼助手 |
| **Kiro** | AWS | AWS 雲端開發助手 |
| **Snow CLI** | Snowflake | 數據分析助手 |
| **Cursor Agent** | Cursor | 程式碼編輯助手 |
| **GitHub Copilot** | GitHub/Microsoft | GitHub 生態開發助手 |
| **Goose** | Block (Square) | 通用任務自動化 |
| **Augment Code** | Augment | 程式碼生成 |
| **Kimi CLI** | 月之暗面 | 中文語境助手 |
| **Mistral Vibe** | Mistral | 法國 AI 助手 |
| **iFlow CLI** | iFlow | 流程自動化 |
| **Factory Droid** | Factory Droid | 工廠自動化 |
| **CodeBuddy** | CodeBuddy | 程式碼助手 |
| **Qoder** | Qoder | 程式碼助手 |
| **Nano Bot** | Nano Bot | 輕量級助手 |

### 2. 多 Agent 並行協作（Cowork）

AionUi 的核心特色是讓多個 AI Agent **同時工作、互相協作**：

```
任務：「重構認證模組，新增 Jest 測試，重新生成 README」

AionUi 自動分派：
├── Claude Code  → 重構 auth module
├── Codex        → 撰寫 Jest 測試
└── Gemini CLI   → 更新 README 文件
```

**並行協作的優勢**：
- ✅ 多個 Agent 同時執行，大幅縮短任務完成時間
- ✅ 每個 Agent 可以使用最適合的模型
- ✅ 自動整合各 Agent 的輸出結果
- ✅ 無需手動切換終端機視窗

### 3. 24/7 定時任務（Automation）

AionUi 內建排程系統，讓 AI Agent 在你離開後也能自動執行任務：

#### 三種排程模式

| 模式 | 說明 | 範例 |
|------|------|------|
| **Cron 表達式** | 標準 cron 格式（含時區設定） | `0 2 * * *`（每天凌晨 2 點） |
| **固定間隔** | 每隔 N 分鐘/小時執行 | 每 30 分鐘、每 2 小時 |
| **一次性觸發** | 指定時間執行一次 | 2026-08-05 14:00 |

#### 使用範例

```
# 每晚自動任務：爬取 GitHub 通知並生成摘要
Cron: 0 2 * * *
Prompt: "Summarize today's GitHub notifications into /reports/$(date).md"

# 每 30 分鐘任務：監控日誌並生成報告
Interval: 30m
Prompt: "Check logs for errors in the last 30 minutes"

# 一次性任務：生成季度報告
One-time: 2026-09-01T09:00:00
Prompt: "Generate Q3 sales report with charts"
```

#### 24/7 運作原理

- Agent 在背景持續運行，即使用戶關閉 GUI 也能繼續執行
- 支援斷線重連，恢復任務執行
- 可配置執行失敗時的警報通知

### 4. 遠端控制與監控（Remote）

即使離開座位，也能透過手機或瀏覽器控制 Agent：

#### 支援的通訊渠道

| 渠道 | 說明 |
|------|------|
| **Telegram** | 透過 Telegram Bot 發送指令 |
| **Slack** | 透過 Slack App 控制 |
| **Discord** | 透過 Discord Bot 監控 |
| **Lark（飛書）** | 透過 Lark Bot 管理 |
| **瀏覽器** | 透過 Web UI 訪問 |
| **手機 App** | 透過手機控制 |

#### 遠端控制範例

```
在 Telegram 發送：
"檢查專案進度"

→ Agent 在電腦上執行任務
→ 結果透過 Telegram 回傳
```

**設定步驟**：
1. 打開 AionUi Settings → WebUI Settings → Channel
2. 設定 Bot Token
3. 即可透過瀏覽器或手機控制 Agent

### 5. 內建 Agent（Built-in Agent）

AionUi 內建完整的 AI Agent 引擎，安裝後即可使用，無需額外配置：

- 支援自然語言對話
- 可讀取、寫入、編輯檔案
- 可執行指令
- 可瀏覽網頁
- 可生成圖片

### 6. 技能系統（Skills）

AionUi 支援技能系統，讓 Agent 學習並執行特定任務：

- **Office 文件處理**：透過 OfficeCLI 讀取、編輯 Word、Excel、PowerPoint
- **網頁 redesign**：自動化網頁設計任務
- **數據分析**：處理和分析數據
- **圖像處理**：自動化圖像編輯
- **文件撰寫**：自動化論文、報告撰寫

---

## 功能詳細說明

### Cowork 模式

Cowork 是 AionUi 的核心功能，允許多個 Agent 同時處理不同子任務：

```
┌─────────────────────────────────────────────────────┐
│                    AionUi Desktop                    │
├─────────────────────────────────────────────────────┤
│  📋 任務：重構認證模組，新增測試，更新文件             │
├─────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ Claude Code   │  │   Codex      │  │Gemini CLI  │ │
│  │ 重構 auth/    │  │ 撰寫 test/   │  │更新 docs/  │ │
│  │ • 模組結構    │  │ • 單元測試   │  │• API 文件  │ │
│  │ • 錯誤處理    │  │ • 整合測試   │  │• 使用範例  │ │
│  │ • 效能優化    │  │ • 邊界條件   │  │• 貢獻指南  │ │
│  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘ │
│         └─────────────────┼─────────────────┘        │
│                           ▼                          │
│                  📦 整合結果                         │
└─────────────────────────────────────────────────────┘
```

### Scheduled Tasks（排程任務）

排程任務管理界面：

```
┌─────────────────────────────────────────────┐
│            Scheduled Tasks                   │
├─────────────────────────────────────────────┤
│  🕐 每日 02:00  | GitHub 通知摘要  | ✅ 正常  │
│  🕐 每 30 分鐘 | 日誌監控     | ✅ 正常  │
│  📅 09/01 09:00 | Q3 銷售報告  | ⏳ 等待  │
│  🕐 每週一 08:00 | 週報生成    | ✅ 正常  │
└─────────────────────────────────────────────┘
```

### WebUI Settings（遠端控制設定）

```
┌─────────────────────────────────────────────┐
│           WebUI Settings                     │
├─────────────────────────────────────────────┤
│  Channel: [Telegram ▼]                       │
│  Bot Token: [****************************]  │
│  Status: ✅ Connected                        │
│  Agent Status: 🟢 Running                    │
└─────────────────────────────────────────────┘
```

---

## 與現有工具的比較

| 功能 | Cursor/Copilot | Claude Desktop | AionUi |
|------|---------------|----------------|--------|
| **多 Agent 支援** | ❌ 單一生態 | ❌ 單一生態 | ✅ 20+ Agent |
| **並行執行** | ❌ | ❌ | ✅ |
| **24/7 定時任務** | ❌ | ❌ | ✅ |
| **遠端控制** | ❌ | ❌ | ✅ |
| **跨生態系統** | ❌ 僅 VS Code | ❌ 僅 Claude | ✅ |
| **開源免費** | ❌ 付費 | ❌ 部分付費 | ✅ 開源 |
| **本地運行** | ✅ | ✅ | ✅ |
| **隱私優先** | ✅ | ✅ | ✅ |

---

## 安裝與設定

### 系統需求

| 項目 | 最低需求 | 推薦需求 |
|------|----------|----------|
| **作業系統** | Windows 10 / macOS 12 / Linux | Windows 11 / macOS 14+ |
| **RAM** | 8 GB | 16 GB+ |
| **硬碟空間** | 500 MB | 2 GB+ |
| **網路** | 需要（下載模型和更新） | 建議穩定連線 |

### 安裝步驟

```bash
# Windows
# 下載 .exe 安裝檔，執行安裝

# macOS
# 下載 .dmg 安裝檔，拖入 Applications

# Linux
# 下載 .AppImage 或 .deb 安裝檔
```

### 初始設定

1. **安裝 AionUi**
2. **安裝 CLI Agent**（選擇需要的 Agent 安裝）
3. **啟動 AionUi** → 自動偵測已安裝的 Agent
4. **設定 API Keys**（Claude、OpenAI、Google 等）
5. **開始使用！**

### 安裝後自動偵測

```
啟動 AionUi → 自動偵測：
├── Claude Code ✅
├── Codex ✅
├── Hermes Agent ✅
├── Gemini CLI ✅
├── OpenCode ✅
└── ... （自動偵測結果）
```

---

## 使用情境

### 情境 1：開發者日常

```
任務：「重構認證模組，新增 Jest 測試，更新 README」

AionUi 自動分派：
├── Claude Code  → 重構 auth/ 目錄
├── Codex        → 撰寫 test/ 目錄的 Jest 測試
└── Gemini CLI   → 更新 README.md 文件

結果：3 個任務並行執行，5 分鐘完成原本需要 30 分鐘的工作
```

### 情境 2：24/7 自動化

```
設定：每晚 2 點自動執行
Cron: 0 2 * * *
Prompt: "爬取 GitHub 通知，生成摘要報告"

流程：
1. 凌晨 2:00 → Agent 自動啟動
2. 爬取 GitHub Notifications API
3. 生成摘要報告到 /reports/$(date).md
4. 報告完成後透過 Telegram 通知
5. 即使電腦進入睡眠，任務仍會完成
```

### 情境 3：遠端監控

```
在會議室：
1. 手機開啟 Telegram
2. 發送：「檢查專案進度」
3. Agent 在電腦上執行任務
4. 結果回傳到手機

場景：
- 會議中監控 CI/CD 狀態
- 旅行中查看日誌錯誤
- 外出時控制 Home Lab 任務
```

### 情境 4：多模型協作

```
任務：「分析這週的銷售數據，生成報告和圖表」

AionUi 分派：
├── Claude Code  → 分析銷售數據（Python 分析）
├── Codex        → 生成銷售趨勢圖表（Chart.js）
├── Gemini CLI   → 撰寫報告文字
└── Hermes Agent → 整合所有輸出，格式化報告

結果：一份包含數據分析、圖表和文字說明完整報告
```

### 情境 5：Office 文件自動化

```
透過 OfficeCLI（AionUi 整合）：
1. 開啟 AionUi
2. 發送：「將這份 Excel 報告轉換為 PowerPoint 簡報」
3. AionUi 自動：
   - 讀取 Excel 數據
   - 生成 PowerPoint 簡報
   - 插入圖表和表格
   - 格式化版面
4. 輸出 .pptx 檔案
```

---

## 技術架構

### 核心架構

```
┌─────────────────────────────────────────────────────┐
│                   AionUi Desktop                     │
│  (Electron + React + TypeScript)                    │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │
│  │  UI Layer    │  │  Cowork     │  │ Automation │  │
│  │  (聊天界面)  │  │  (並行協作)  │  │ (排程任務) │  │
│  └──────┬──────┘  └──────┬──────┘  └─────┬──────┘  │
│         └────────────────┼────────────────┘         │
│                          ▼                           │
│              ┌─────────────────────┐                 │
│              │  Agent Router       │                 │
│              │  (ACP Protocol)     │                 │
│              └─────────┬───────────┘                 │
│                        ▼                             │
│  ┌──────────────────────────────────────────────┐    │
│  │            CLI Agent Layer                    │    │
│  │  Claude Code │ Codex │ Gemini │ Hermes │ ...  │    │
│  └──────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

### ACP（Agent Client Protocol）

ACP 是 AionUi 定義的代理客戶端協議，用於統一管理不同的 CLI Agent：

- **統一介面**：所有 Agent 透過同一個介面訪問
- **自動偵測**：自動識別已安裝的 Agent
- **動態加載**：動態載入新的 Agent
- **標準化通訊**：統一的訊息格式

### 技術棧

| 層級 | 技術 |
|------|------|
| **前端** | React + TypeScript |
| **桌面框架** | Electron |
| **核心** | AionCore（Rust） |
| **通訊協議** | ACP（Agent Client Protocol） |
| **Office 自動化** | OfficeCLI（單一二進位檔） |

---

## 相關專案生態

### iOfficeAI 生態系統

| 專案 | 說明 | GitHub |
|------|------|--------|
| **AionUi** | 主應用程式（Electron + React） | [GitHub](https://github.com/iOfficeAI/AionUi) |
| **AionCore** | Rust 核心引擎 | [GitHub](https://github.com/iOfficeAI/AionCore) |
| **OfficeCLI** | Office 文件自動化 CLI | [GitHub](https://github.com/iOfficeAI/OfficeCLI) |

### 與 Hermes Agent 的整合

AionUi 支援 Hermes Agent，提供桌面界面：

```
Hermes Agent（後端引擎）
    ↓
AionUi（桌面界面）
    ↓
20+ CLI Agent 統一管理
```

---

## 常見問題（FAQ）

### Q1：AionUi 與 Claude Desktop 有什麼不同？

**A**：Claude Desktop 只能與 Claude 模型互動，而 AionUi 可以管理 20+ 個不同的 CLI Agent，包括 Claude Code、Codex、Gemini CLI 等，並且支援並行協作和 24/7 定時任務。

### Q2：AionUi 是開源的嗎？

**A**：是的，AionUi 採用 Apache-2.0 授權，完全開源免費。

### Q3：AionUi 支援哪些作業系統？

**A**：支援 Windows、macOS 和 Linux。

### Q4：是否需要安裝特定的 CLI Agent？

**A**：不需要。AionUi 內建完整的 AI Agent 引擎，安裝後即可使用。你也可以選擇安裝額外的 CLI Agent（如 Claude Code、Codex 等）以獲得更多功能。

### Q5：AionUi 會將資料上傳到雲端嗎？

**A**：不會。AionUi 完全在本地運行，所有資料都儲存在你的電腦上，不會上傳到雲端。

### Q6：如何設定遠端控制？

**A**：在 AionUi Settings → WebUI Settings → Channel 中設定 Bot Token，即可透過 Telegram、Slack、Discord 等渠道遠端控制 Agent。

### Q7：AionUi 可以與現有工具整合嗎？

**A**：可以。AionUi 支援透過 OfficeCLI 處理 Office 文件，支援透過 ACP 整合任何相容的 CLI Agent。

### Q8：定時任務在電腦關閉後還會執行嗎？

**A**：不會。定時任務需要在電腦開啟且 AionUi 運行時才能執行。但 AionUi 可以在背景運行，即使關閉 GUI 窗口，Agent 仍會繼續執行任務。

---

## 快速開始

### Step 1：下載安裝

```bash
# Windows
# 下載 AionUi-setup.exe，執行安裝

# macOS
# 下載 AionUi.dmg，拖入 Applications

# Linux
# 下載 AionUi.AppImage，給予執行權限
chmod +x AionUi.AppImage
./AionUi.AppImage
```

### Step 2：啟動 AionUi

```
啟動 AionUi → 自動偵測已安裝的 Agent
→ 設定 API Keys
→ 開始使用！
```

### Step 3：開始 Cowork

```
在聊天界面輸入：
「重構認證模組，新增 Jest 測試，更新 README」

AionUi 自動：
1. 分派任務給合適的 Agent
2. 並行執行所有子任務
3. 整合結果並顯示
```

### Step 4：設定定時任務

```
打開 Scheduled Tasks → New Schedule
設定：
- Cron: 0 2 * * *
- Prompt: "Summarize today's GitHub notifications"
- Agent: Hermes Agent

完成！每天凌晨 2 點自動執行。
```

---

## 結論

AionUi 是目前最全面的 AI Agent 管理工具，提供以下核心優勢：

| 優勢 | 說明 |
|------|------|
| **20+ Agent 統一管理** | 無需切換多個應用程式 |
| **並行協作** | 多個 Agent 同時工作，縮短任務時間 |
| **24/7 自動化** | 定時任務無人值守執行 |
| **遠端控制** | 透過手機/瀏覽器隨時控制 |
| **開源免費** | Apache-2.0 授權，完全免費 |
| **隱私優先** | 本地運行，資料不上傳雲端 |
| **跨生態系統** | 支援 Claude、OpenAI、Google 等多個生態系統 |

**推薦場景**：
- ✅ 需要管理多個 AI Agent 的開發者
- ✅ 需要自動化重複性任務的用戶
- ✅ 需要遠端監控 Agent 執行的用戶
- ✅ 需要多模型協作的團隊

**GitHub Stars**：24,800+  
**官方網站**：https://aionui.com/  
**GitHub**：https://github.com/iOfficeAI/AionUi

---

**最後更新**：2026-08-05  
**作者**：Hermes Agent 整理  
**原始專案**：[AionUi](https://github.com/iOfficeAI/AionUi)
