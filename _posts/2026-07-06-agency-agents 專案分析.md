# msitarzewski/agency-agents 專案分析

> **專案網址**: https://github.com/msitarzewski/agency-agents
> **授權**: MIT License
> **數據**: 114k Star · 18.6k Fork · 87 位貢獻者

---

## 專案概述

**The Agency** 是一個開放原始碼的 **AI 智能體（Agent）人格庫**，彙集了 **232 個專門化的 AI Agent**，分為 **16 個部門**。每個 Agent 都是一個具有獨特個性、工作流程和明確交付物的專家角色定義。

起源於 Reddit 討論，經過數月實戰迭代，由社群共同維護推動。

---

## 核心功能

1. **專門化的 Agent 人格** — 每個 Agent 不是通用的提示範本，而是具有獨特語氣、工作方式和成功指標的專家
2. **多工具整合** — 支援 12 種主流 AI 開發工具
3. **一鍵安裝** — 透過 `install.sh` 腳本自動偵測系統工具並互動式安裝
4. **開放貢獻** — 社群驅動，歡迎提交新 Agent 或改進現有內容

---

## 支援工具

| 工具 | 格式 | 安裝路徑 |
|------|------|----------|
| Claude Code | `.md` | `~/.claude/agents/` |
| GitHub Copilot | `.md` | `~/.github/agents/` + `~/.copilot/agents/` |
| Antigravity | `SKILL.md` | `~/.gemini/antigravity/skills/` |
| Gemini CLI | extension + `SKILL.md` | `~/.gemini/extensions/agency-agents/` |
| OpenCode | `.md` | `.opencode/agents/` |
| Cursor | `.mdc` | `.cursor/rules/` |
| Aider | `CONVENTIONS.md` | `./CONVENTIONS.md` |
| Windsurf | `.windsurfrules` | `./.windsurfrules` |
| OpenClaw | `SOUL.md` + `AGENTS.md` + `IDENTITY.md` | — |
| Qwen Code | `.md` SubAgent | `~/.qwen/agents/` |
| Kimi Code | YAML agent spec | `~/.config/kimi/agents/` |
| Codex | TOML custom agent | `~/.codex/agents/` |

---

## 16 個部門

### 💻 Engineering — 工程部門
前端、後端、行動開發、DevOps、AI 工程、嵌入式系統、智慧合約、資料庫優化、Git 工作流、軟體架構、SRE、資料工程、CMS、語音 AI、IT 服務管理等 30+ Agent

### 🎨 Design — 設計部門
UI 設計、UX 研究、UX 架構、品牌守護、視覺敘事、趣味注入、AI 影像提示詞、包容性視覺、角色體驗走查

### 💰 Paid Media — 付費廣告部門
PPC 策略、搜尋詞分析、廣告稽核、追蹤測量、創意策略、程式化購買、付費社群

### 💼 Sales — 業務部門
外電策略、探索訪談教練、商機策略、銷售工程、提案策略、管道分析、客戶策略、業務教練、產品導向開發

### 📢 Marketing — 行銷部門
成長駭客、內容創作、社群經營（Twitter、TikTok、Instagram、Reddit、LinkedIn）、中國平台（小紅書、微信、知乎、B 站、抖音、快手、微博）、SEO、ASO、跨國電商、電子報、公關、AI 搜尋優化

### 📊 Product — 產品部門
衝刺優先級、市場調研、使用者回饋彙整、行為助推、產品經理

### 🎬 Project Management — 專案管理部門
製作人、專案協調、營運管理、實驗追蹤、資深專案經理、Jira 工作流、會議記錄

### 🧪 Testing — 測試部門
視覺 QA、現實核查、測試結果分析、效能基準、API 測試、工具評估、工作流程優化、無障礙稽核

### 🔒 Security — 安全部門
安全架構、應用程式安全、滲透測試、雲端安全、事件回應、威脅情報、威脅偵測、SecOps、合規稽核、區塊鏈安全

### 🛟 Support — 支援部門
客戶服務、分析報告、財務追蹤、基礎設施維護、法律合規、高階摘要生成

### 🥽 Spatial Computing — 空間運算部門
XR 介面架構、macOS Spatial/Metal、WebXR、駕駛艙互動、visionOS、終端機整合

### 🎯 Specialized — 專門部門
多 Agent 協同、LSP/Index、銷售資料擷取、身分圖檔、應付帳款、文化智慧、開發者倡議、ML QA、Zettelkasten、MCP 建置、文件生成、自動化治理、企業培訓、個人成長、政府數位化、醫療行銷合規、招募、留學、供應鏈、工作流程架構、Salesforce、法國顧問市場、韓國商務、土木工程、客服、HR 導入、翻譯、法律、房貸、房地產、零售退貨、商業策略、變革管理、幕僚長、客戶成功、補助撰寫、醫療收碼、定價分析、CFO、ESG、資料隱私、營運管理、併購整合、組織心理學、策略對決

### 💵 Finance — 財務部門
記帳與主控、財務分析、FP&A、投資研究、稅務策略

### 🎮 Game Development — 遊戲開發部門
跨引擎（遊戲設計、關卡設計、技術美術、音效、敘事）＋ Unity 系列（架構、著色器、多人、Editor 工具）＋ Unreal 系列（系統、技術美術、多人、世界建造）＋ Godot 系列（腳本、多人、著色器）＋ Blender（外掛工程）＋ Roblox（系統腳本、體驗設計、角色造型）

### 📚 Academic — 學術部門
人類學、地理學、歷史學、敘事學、心理學（世界建構、故事敘事、角色設計）

### 🌍 GIS — 地理資訊系統部門
技術顧問、解決方案工程、GIS 分析、空間資料工程、地理處理、QA 工程、GeoAI/ML、BIM/GIS、3D 場景、空間數據科學、無人機測繪、Web GIS、地圖設計

---

## 安裝方式

```bash
# 方式一：Claude Code（推薦）
./scripts/install.sh --tool claude-code
# 或手動複製
cp engineering/*.md ~/.claude/agents/

# 方式二：其他工具
./scripts/convert.sh          # 生成各工具格式
./scripts/install.sh          # 互動式安裝，自動偵測

# 方式三：指定部門 / Agent
./scripts/install.sh --tool claude-code --division engineering,security
./scripts/install.sh --tool cursor --agent frontend-developer,ui-designer
```

---

## Agent 設計哲學

1. **強烈個性** — 不是通用範本，而是有角色和語氣的專家
2. **明確交付物** — 具體的產出，非模糊的指引
3. **成功指標** — 可衡量的結果與品質標準
4. **成熟工作流程** — 經實證有效的步驟流程
5. **學習記憶** — 模式識別與持續改進

---

## 實際應用情境

| 情境 | 組合 Agent |
|------|-----------|
| 新創 MVP 開發 | 前端開發者 + 後端架構師 + 成長駭客 + 快速原型 + 現實核查 |
| 行銷活動上線 | 內容創作 + Twitter 經營 + Instagram 策展 + Reddit 社群 + 分析報告 |
| 企業功能開發 | 資深專案經理 + 資深開發者 + UI 設計師 + 實驗追蹤 + 證據收集 + 現實核查 |
| 付費廣告接管 | 廣告稽核 + 追蹤測量 + PPC 策略 + 搜尋詞分析 + 創意策略 + 分析報告 |
| 智慧校園數位雙生 | 技術顧問 + BIM/GIS + 無人機測繪 + Web GIS + 3D 場景 + GeoAI + GIS QA |

---

## 社群翻譯

| 語言 | 維護者 | 備註 |
|------|--------|------|
| 簡體中文 | @jnMetaCode | 141 個翻譯 + 46 個中國市場原創 |
| 簡體中文 | @dsclca12 | 獨立翻譯，含 B 站、微信、小紅書在地化 |
| 日本語 | @sscodeai | 281 個在地化 + 97 個日本市場原創 + 27 個工作流程 |
| Português | @jnMetaCode | 184 個翻譯 |
| Русский | @jnMetaCode | 184 個翻譯 |
| 한국어 | @jnMetaCode | 184 個翻譯 |
| العربية | @jnMetaCode | 184 個翻譯 |
| Bahasa Indonesia | @jnMetaCode | 184 個翻譯 |

---

## 專案結構

```
agency-agents/
├── academic/          # 學術部門 Agent
├── design/            # 設計部門 Agent
├── engineering/       # 工程部門 Agent
├── examples/          # 多 Agent 協作範例
├── finance/           # 財務部門 Agent
├── game-development/  # 遊戲開發部門 Agent
├── gis/               # GIS 部門 Agent
├── integrations/      # 各工具整合格式
├── marketing/         # 行銷部門 Agent
├── paid-media/        # 付費廣告部門 Agent
├── product/           # 產品部門 Agent
├── project-management/# 專案管理部門 Agent
├── sales/             # 業務部門 Agent
├── scripts/           # 安裝/轉換腳本
├── security/          # 安全部門 Agent
├── spatial-computing/ # 空間運算部門 Agent
├── specialized/       # 專門部門 Agent
├── strategy/          # 策略部門 Agent
├── support/           # 支援部門 Agent
├── testing/           # 測試部門 Agent
├── CONTRIBUTING.md
├── divisions.json
└── README.md
```

---

## 總結

The Agency 適合需要 **AI Agent 提示工程** 的開發者與團隊，特別是使用 Claude Code 等 AI 編碼工具時，可以快速組合不同專長的 Agent 來組成「夢幻團隊」，提升 AI 協助開發的品質與一致性。每個 Agent 檔案包含身分與個性、核心任務、關鍵規則、技術交付物、工作流程、以及成功指標，可直接複製使用或依需求客製化。
