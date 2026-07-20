---
layout: post
title: "Everything Claude Code 深度分析 — Claude Code 最完整的配置工具包"
date: 2026-07-20
categories: [AI Tools, Open Source, Claude Code]
tags: [Claude Code, AI Agent, MCP, 開源專案]
---

# Everything Claude Code 深度分析

**專案連結：** [WorldFlowAI/everything-claude-code](https://github.com/worldflowai/everything-claude-code)（原始：[affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)）

**Stars：** 541+ ｜ **Forks：** 100+ ｜ **授權：** MIT

## 專案概述

Everything Claude Code 是一個 **Anthropic Hackathon 冠軍團隊** 開發的 Claude Code 配置工具包。經過 10 個月的實際產品開發驗證，收集了生產環境等級的 Agents、Skills、Hooks、Commands、Rules 和 MCP 配置。

這是一個 **Claude Code Plugin**，可以透過 marketplace 直接安裝，也可以手動複製各組件使用。

## 核心架構

專案採用模組化設計，將 Claude Code 的配置分為六大核心模塊：

### 1. Agents（子代理）— 9 個專業化子代理

| Agent | 功能說明 |
|-------|---------|
| `planner.md` | 功能實作規劃，拆解任務步驟 |
| `architect.md` | 系統架構設計決策 |
| `tdd-guide.md` | 測試驅動開發引導 |
| `code-reviewer.md` | 程式碼品質與安全性審查 |
| `security-reviewer.md` | 漏洞分析與安全審查 |
| `build-error-resolver.md` | 構建錯誤診斷與修復 |
| `e2e-runner.md` | Playwright E2E 測試執行 |
| `refactor-cleaner.md` | 死碼清理與重構 |
| `doc-updater.md` | 文件同步更新 |

每個 Agent 都有明確的範圍限制和工具清單，可透過委派（delegation）機制調用。

### 2. Skills（工作流程定義）— 11 個領域技能

| Skill | 功能說明 |
|-------|---------|
| `coding-standards/` | 各語言最佳實踐標準 |
| `backend-patterns/` | API、資料庫、快取模式 |
| `frontend-patterns/` | React/Next.js 前端模式 |
| `continuous-learning/` | 自動從會話中提取模式為可重用技能（Longform Guide） |
| `strategic-compact/` | 手動壓縮建議（Longform Guide） |
| `tdd-workflow/` | TDD 方法論（RED→GREEN→REFACTOR） |
| `security-review/` | 安全檢查清單 |
| `eval-harness/` | 驗證循環評估框架（Longform Guide） |
| `verification-loop/` | 持續驗證機制（Longform Guide） |
| `project-guidelines-example/` | 專案指南範例 |
| `clickhouse-io/` | ClickHouse 資料庫專門技能 |

### 3. Commands（斜線指令）— 10 個快捷指令

| Command | 功能說明 |
|---------|---------|
| `/tdd` | 啟動測試驅動開發流程 |
| `/plan` | 功能實作規劃 |
| `/e2e` | E2E 測試生成 |
| `/code-review` | 程式碼品質審查 |
| `/build-fix` | 修復構建錯誤 |
| `/refactor-clean` | 死碼移除與重構 |
| `/learn` | 會話中提取模式（Longform Guide） |
| `/checkpoint` | 保存驗證狀態（Longform Guide） |
| `/verify` | 運行驗證循環（Longform Guide） |
| `/setup-pm` | 配置套件管理器 |

### 4. Rules（強制規則）— 6 項始終遵循的指導原則

| Rule | 功能說明 |
|------|---------|
| `security.md` | 強制安全檢查（禁止硬編碼金鑰） |
| `coding-style.md` | 不可變性、文件組織規範 |
| `testing.md` | TDD、80%+ 覆蓋率要求 |
| `git-workflow.md` | Commit 格式、PR 流程 |
| `agents.md` | 何時委派給子代理 |
| `performance.md` | 模型選擇、Context 管理 |

### 5. Hooks（觸發式自動化）

核心創新功能，透過事件觸發自動執行：

- **memory-persistence/** 會話生命週期 Hooks（跨會話記憶持久化）
- **strategic-compact/** 壓縮建議 Hooks
- **hooks.json** 配置檔，支援 PreToolUse、PostToolUse、Stop 等事件

**Hook 運作原理：**
```json
{
  "matcher": "tool == \"Edit\" && file_path matches \\.(ts|tsx|js|jsx)$",
  "hooks": [{
    "type": "command",
    "command": "grep -n 'console.log' \"$file_path\" && echo '[Hook] Remove console.log'"
  }]
}
```

### 6. MCP Configs（MCP 伺服器配置）

預設集成了多個 MCP 服務器配置：
- GitHub、Supabase、Vercel、Railway 等
- **重要提醒：** 不要一次啟用所有 MCP，200k context window 可能會縮減到 70k
- 建議每專案維持 10 個以下 MCP，總工具數 80 個以下

## 進階功能（Longform Guide）

### Token 優化策略
- 模型選擇策略（不同任務用不同模型）
- System prompt 瘦身技巧
- 背景進程減少 token 消耗

### 記憶持久化
- Hooks 自動保存/加載會話上下文
- Node.js 實現的跨平台兼容
- 會話開始/結束自動狀態管理

### 持續學習機制
- 自動從會話中提取模式
- 轉化為可重用的 Skills
- 持續改進工作流

### 驗證循環
- Checkpoint vs 持續評估兩種模式
- Grader 類型與 pass@k 指標
- 確保代碼質量的自動化驗證

### 平行化策略
- Git worktrees 多線作業
- Cascade method 級聯方法
- 何時擴展 Agent 實例的決策指南

### 子代理編排
- Context 問題解決方案
- 迭代檢索模式（iterative retrieval pattern）

## 跨平台支援

全新改寫為 **Node.js** 腳本，完整支援 Windows、macOS、Linux：

- 自動偵測套件管理器（npm/pnpm/yarn/bun）
- 六層偵測優先級（環境變數 > 專案配置 > package.json > lock file > 全域配置 > Fallback）
- 完整的測試套件（`node tests/run-all.js`）

## 安裝方式

### 方式一：Plugin 安裝（推薦）

```bash
/plugin marketplace add affaan-m/everything-claude-code
/plugin install everything-claude-code@everything-claude-code
```

### 方式二：手動安裝

```bash
git clone https://github.com/affaan-m/everything-claude-code.git
cp everything-claude-code/agents/*.md ~/.claude/agents/
cp everything-claude-code/rules/*.md ~/.claude/rules/
cp everything-claude-code/commands/*.md ~/.claude/commands/
cp -r everything-claude-code/skills/* ~/.claude/skills/
```

## 背景故事

作者 Affaan Mustafa 從 Claude Code 實驗階段開始使用，於 2025 年 9 月在 Anthropic x Forum Ventures Hackathon 中，完全使用 Claude Code 構建 [zenith.chat](https://zenith.chat) 並獲得冠軍。這些配置經過多個生產級應用驗證。

## 適合誰使用

- **Claude Code 重度使用者** — 大幅提升開發效率
- **AI 輔助開發團隊** — 統一的開發標準和工作流
- **學習 Claude Code 最佳實踐** — 從實戰中驗證的配置模板
- **建構自定義 Agent 系統** — 作為基礎框架擴充

## 關鍵洞察

1. **模組化設計** — 六大模塊互相獨立，可選擇性安裝
2. **從實戰中誕生** — 不是理論框架，而是 10+ 個月生產環境的沉澱
3. **Hooks 是最核心創新** — 事件觸發式自動化，讓 Claude Code 從「被動回應」變為「主動管理」
4. **Context Window 管理** — 實用的 MCP 管理建議（20-30 個配置，10 個啟用，80 個工具上限）
5. **跨平台優先** — 全面 Node.js 重寫，解決了 Shell 腳本的跨平台問題
6. **開源社群導向** — 明確鼓勵貢獻，提供貢獻指南和擴展方向

## 總結

Everything Claude Code 是目前最完整的 Claude Code 配置生態系統。它不僅提供了現成的模板，更重要的是展示了如何系統性地組織 AI 輔助開發的配置——從 Agent 委派到 Skill 工作流，從 Hook 自動化到 MCP 集成。對於認真使用 Claude Code 的開發者來說，這是一個必備的起點。
