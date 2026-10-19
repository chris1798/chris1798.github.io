---
title: "本週 GitHub 熱門項目整理（2026-10-19）"
date: 2026-10-19
description: 本週 GitHub Trending 十大熱門專案完整功能介紹：REA 逆向工程 MCP、ArtCraft 創作 IDE、AnyPS5、diagram-design、Ghidra、HyperFrames、ai-job-search、Claude 官方插件目錄、context-mode、Cursor plugins。星數已透過 GitHub API 驗證。
tags: [github, trending, ai-agent, mcp, reverse-engineering, claude-code]
---

# 本週 GitHub 熱門項目整理（2026-10-19）

資料來源：[GitHub Trending（週榜）](https://github.com/trending?since=weekly)，抓取自 2026-10-19。總星數已逐個透過 GitHub API 於當日驗證。

**本週主題觀察**：榜上十個專案有九個與 AI agent 生態直接相關——逆向工程 MCP、agent 插件目錄、context 優化、HTML 渲染影片、agent 技能庫。Agent 工具鏈已從「模型能力」競賽轉為「外圍基建」競賽。

## 一覽表（依本週新增星數排序）

| # | 專案 | 語言 | 總星數 | 本週新增 | 主題 |
|---|---|---|---|---|---|
| 1 | [morluto/rea](https://github.com/morluto/rea) | TypeScript | 322,117 | 229,268 | 逆向工程 MCP |
| 2 | [storytold/artcraft](https://github.com/storytold/artcraft) | Rust | 32,714 | 16,379 | AI 影像創作 IDE |
| 3 | [boykopovar/AnyPS5](https://github.com/boykopovar/AnyPS5) | C++ | 43,201 | 14,224 | PS5 執行檔轉接 |
| 4 | [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | HTML | 57,686 | 7,901 | Agent 圖表技能 |
| 5 | [NationalSecurityAgency/ghidra](https://github.com/NationalSecurityAgency/ghidra) | Java | 90,894 | 7,602 | 逆向工程框架 |
| 6 | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | TypeScript | 66,731 | 5,883 | HTML 渲染影片 |
| 7 | [MadsLorentzen/ai-job-search](https://github.com/MadsLorentzen/ai-job-search) | Python | 53,132 | 5,742 | AI 求職框架 |
| 8 | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Python | 42,679 | 4,774 | Claude 官方插件目錄 |
| 9 | [mksglu/context-mode](https://github.com/mksglu/context-mode) | TypeScript | 30,753 | 4,138 | Context 視窗優化 |
| 10 | [cursor/plugins](https://github.com/cursor/plugins) | TypeScript | 12,737 | 1,717 | Cursor 插件規格 |

## 深度介紹

### 第 1 名：REA（Reverse Engineer Anything）— 一個 MCP 打通二進制、應用與執行期逆向

本週爆發性成長（單週 +229K 星，總數 322K）。REA 是給 AI coding agent 用的逆向工程 MCP server，安裝只要 `npx rea-agents setup`：

- **三種分析對象**：原生二進制（binary）、完整應用程式（app 行為層）、執行期行為（runtime）——看到喜歡的機能，讓 agent 追到實作層
- **生成式 MCP 工具目錄**：契約文件化（docs/mcp-contracts.md 有自動生成的 catalog）
- 支援各家 agent（Claude Code、Codex、Cursor 等），網站 rea.tools 有指南與 showcase
- MIT 授權；README 有 22 種語言版本（含繁體中文）
- 本站上週已發過專題：[REA 完整功能介紹](/rea-reverse-engineer-anything/)

**適用場景**：competitor 功能研究、無原始碼的舊系統接手、惡意程式初階分析、安全研究教學。

### 第 2 名：ArtCraft — 給創作者的「IDE 式」AI 影像生成

Rust 寫的桌面應用（macOS/Windows 可下載），定位是「IDE for artists」——把 prompting 變成 crafting：

- **先在場景裡摆好再生成**：2D 構圖 + 3D 舞台（角色定位、相機擺位），再選模型生成，結果可重複
- **模型可選**：依作品需求挑不同的生成模型，不綁單一供應商
- 面向藝術家、設計師、影像工作者；官方有兩分鐘 YouTube demo
- 本週從默默无闻衝到週榜第二，成長速度極快

**適用場景**：需要穩定角色一致性與鏡頭控制的短片/概念設計；不想只靠文字 prompt 的視覺創作者。

### 第 3 名：AnyPS5 — PS5 執行檔自動轉接到 Linux/Windows

C++ 工具，走的是「**relinker 而非模擬器**」路線：

- **relinker** 把 PS5 執行檔（ORBIS 格式）直接轉成目標系統的原生格式，再把 PS5 系統 PRX 函式庫動態連結過去——沒有模擬器、沒有獨立 runtime process
- **Shader 重編譯器**可產出經 SPIRV-Tools 驗證的 SPIR-V
- 有純瀏覽器版 Web converter（檔案不出裝置）；relinker-only 版可在 macOS（含 Apple Silicon）執行
- 社群維護 per-game 進度地圖（blocker map）與 Game bring-up 討論區；SDL 手把映射 + ini 檔鍵鼠設定
- 注意：專案定位為 interoperability 研究，實際可玩性仍以進度圖為準

**適用場景**：Linux 遊戲相容性研究、格式轉換/重連結技術參考。（法律與倫理自負。）

### 第 4 名：diagram-design — 讓 agent 畫「品牌級」圖表的技能

給 Claude Code / Codex / Copilot / Cursor 的 agent skill，一句 `npx skills add cathrynlavery/diagram-design`：

- **產物是單一自含的 HTML+SVG 檔**，雙開即看；45 種圖型（架構圖、四象限、序列圖……）
- **品牌貼合**：`Onboard <你的網站>` 會抓你的調色盤與字型，之後每張圖自動符合品牌
- 拒絕 Mermaid 預設風：明確反「陰影、Mermaid slop」，走編輯設計感路線
- 可從 drawio / Mermaid / Excalidraw 匯入；可輸出 PNG/SVG
- 網站 diagramdesign.dev 有 gallery

**適用場景**：技術文件配图、簡報圖、需要公司視覺一致的架構圖。

### 第 5 名：Ghidra — 國安局出品逆向工程框架（回榜）

經典重訊，配合 REA 的爆發重新上榜：

- NSA 維護的 SRE 框架：**反組譯、重組、反編譯（decompiler）、圖形化、腳本化**，數百項功能
- 支援大量 CPU 指令集與執行檔格式；Windows/macOS/Linux 跨平台
- 可 user-interactive 或自動化批次執行；Java/Python 寫 extension 與 script
- 安裝：JDK 25 + 官方 release zip；注意官方警示部分版本有已知漏洞，先讀 Security Advisories

**適用場景**：正式 RE 工作流、CTF、韌體/惡意程式分析——REA 讓 agent 跑腿，Ghidra 是底層重武器。

### 第 6 名：HyperFrames — 寫 HTML，渲染成影片

HeyGen 開源的「HTML → MP4」框架，專為 agent 設計：

- HTML/CSS/多媒體/可 seek 動畫 → **確定性（deterministic）MP4 輸出**
- 三種入口：本機 CLI、AI coding agent skills（Claude Code plugin 一行安裝）、託管工作流的渲染核心
- agent skills 教完整製作迴圈：企劃 → 寫合法 HTML → 接可 seek 動畫 → 加多媒體 → lint → preview → render（共 21 個已發布 skills）
- 支援 Claude Code、Codex、Cursor、Gemini CLI 等

![HyperFrames 示例](/assets/images/hyperframes/img1.png)
![HyperFrames 架構](/assets/images/hyperframes/img2.png)

**適用場景**：用 agent 批次產產品介紹片、文件動效、社群短片；把「影片剪輯」變成「寫前端」。

### 第 7 名：ai-job-search — 在你機器上跑的 AI 求職框架

基於 Claude Code 求職工作流，作者是被裁員的地球物理學家，用這套框架投了 69 份履歷、20 場初試、拿到 AI 工程師 offer 後開源：

- **`/scrape` `/apply` `/interview` 三大指令**：抓取職缺、評估適配度、tailor CV、應徵信撰寫、面試準備
- **drafter-reviewer 管線**：生成與審查分離，品質可控；核心流程語言無關（任何語文簡歷可用）
- 全部在本機跑，個資不出門；明確聲明與 Anthropic 無關聯、無加密貨幣/付費贊助（防仿冒詐騙）

**適用場景**：大規模求職季、轉職者批量投遞＋個人化 CV；對「AI 履歷」透明化的求職策略。

### 第 8 名：claude-plugins-official — Anthropic 官方 Claude Code 插件目錄

Anthropic 自己維護的 curated marketplace：

- `/plugins`（Anthropic 內部插件）+ `/external_plugins`（合作夥伴/社群，需過品質與安全審核）
- 安裝：`/plugin install {name}@claude-plugins-official` 或 `/plugin > Discover`
- **plugin slug 不可變**：`name` 一旦發布不能改（改了會炸使用者安裝），要改名用 `displayName` 或 `renames` 映射自動遷移
- 標準結構：`plugin.json` metadata + `.mcp.json` + commands/agents/skills
- 官方警告：安裝第三方插件前自行信任評估

**適用場景**：找可信 Claude Code 插件的預設入口；開發者要發布插件的合規參考。

### 第 9 名：context-mode — 把工具輸出關進沙箱，省 98% context

給 AI coding agent 的 context 視窗優化 MCP server（曾登 HN 第一、570+ 分）：

- **痛點量化**：Playwright snapshot 56KB、20 個 GitHub issues 59KB、一份 access log 45KB——30 分鐘後 40% 的 context 被垃圾輸出吃掉；compact 時又會忘記正在編譯的檔案與任務進度
- **做法**：sandbox 化所有 MCP 工具輸出（宣稱削減 98%）、壓縮 agent 的 filler 輸出、維持工作記憶（編輯中的檔案、任務、最後指令）
- 安裝自 npm（`context-mode`），ELv2 授權

![Context Mode 示意](/assets/images/context-mode/img1.jpg)

**適用場景**：重度 MCP 工作流（瀏覽器自動化、大量 GitHub/日誌查詢）省 token、延長單輪工作長度、降低 compact 後失憶。

### 第 10 名：cursor/plugins — Cursor 官方插件規格與目錄

Cursor 把自家 agent 插件體系開源成規格＋官方插件集：

- 每個插件是倉庫根目錄一個目錄，含 `.cursor-plugin/plugin.json` manifest
- 官方插件例：`teaching`（學習計畫）、`thermos`（嚴苛分支安全/正確性審查）、`ralph-loop`（自引用迭代迴圈）、`pr-review-canvas`（PR diff 畫布化）、`continual-learning`（transcript 驅動 AGENTS.md 記憶更新）、`create-plugin`（脚手架）
- 與 Claude 插件目錄同一波「agent 插件標準化」浪潮

**適用場景**：Cursor 用戶擴充工作流；寫跨 agent 插件時對照兩家規格。

## 本週觀察

1. **逆向工程成為 agent 新戰場**：REA 單週 22.9 萬星（史上罕見）＋ Ghidra 回榜＋AnyPS5 上榜——「讓 agent 讀懂别人的實作」是當紅需求。
2. **插件目錄軍備競賽**：Anthropic 官方目錄、Cursor 官方規格同週上榜，agent 生態正式進入「分发渠道＋規格標準」階段。
3. **Context 經濟學浮上台面**：context-mode 把「工具輸出吃掉 40% context」量化成賣點，省 token 基建從技巧變成產品。
4. **多媒體產線 agent 化**：HyperFrames（HTML→MP4）與 ArtCraft（場景先行生成）都把影像製作拆成 agent 可執行的確定性步驟。
5. **週榜星數需保留解讀空間**：REA 單週 +229K 的曲線極為異常（上週它還只是新星榜常客），榜單熱度與實際採樣可能有落差，使用前建議自行審查代碼與供應鏈。

## 方法說明

- 榜單來源：GitHub Trending weekly 頁面，抓取自 2026-10-19，解析 `article.Box-row` 區塊
- 本週新增星數：頁面「stars this week」欄位
- 總星數：逐 repo 經 GitHub REST API（`/repos/{owner}/{repo}`）當日查詢，非推估
- 功能描述：整理自各專案官方 README 全文
- 圖片：僅本地化自各 README 的靜態圖片資產；README 無內容圖的專案以純文字介紹
