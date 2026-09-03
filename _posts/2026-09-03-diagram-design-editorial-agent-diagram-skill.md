---
title: "Diagram Design：給 AI Agent 用的「編輯設計圖庫」，39 種編輯風格圖表、自訂 HTML+SVG、可吸你的品牌色"
date: 2026-09-03
description: Diagram Design 是由 Cathryn Lavery 開源的 Claude Code / Codex / Pi 技能，把「一個指令」生成「編輯設計品質」的自包含 HTML 圖表。39 種圖表類型、自訂品牌色彩、匯入 draw.io/Mermaid、匯出 PNG/SVG。
tags:
  - open-source
  - agent-skills
  - claude-code
  - codex
  - svg
  - data-visualization
  - diagrams
cover: /assets/images/diagram-design/architecture.png
---

# Diagram Design：給 AI Agent 的「編輯設計圖表」技能

![Diagram Design](/assets/images/diagram-design/architecture.png)

> **39 種編輯風格圖表，給 Claude Code、Codex、Factory Droid、Pi。**
> 自包含 HTML + SVG。無陰影。無 Mermaid 醜圖。

---

## 📊 專案速覽

| 項目 | 資料 |
|------|------|
| **名稱** | cathrynlavery/diagram-design |
| **作者** | Cathryn Lavery（BestSelf.co 創辦人） |
| **授權** | MIT |
| **Stars** | ⭐ 29,529 |
| **Forks** | 1,877 |
| **開發語言** | HTML |
| **版本** | v2.6 |
| **建立時間** | 2026-04-16 |
| **官方 Gallery** | [cathrynlavery.github.io/diagram-design](https://cathrynlavery.github.io/diagram-design/) |

---

## 🎯 什麼是 Diagram Design？

### 一句話說明

> **一個技能（Skill），讓 AI Agent（如 Claude Code）幫你画出「編輯設計品質」的圖表——不是那種圓角方塊的醜圖，而是像專業編輯雜誌插图的圖表。**

### 背後的痛点

作者 Cathryn Lavery 在 [littlemight.com](https://littlemight.com) 寫文章時，需要圖表但總是遇到：

```text
找 Claude 要圖表 → 回傳「通用圓角方塊圖」→
跟整個網站風格不符 → 跟 Figma 拚 30 分鐘 → 乾脆放棄
```

所以她自己做了這個 Claude Code 技能，**39 種圖表類型、編輯設計品質、60 秒吸你的品牌色**。

---

## ✨ 核心特色

### 1. 自包含 HTML（Self-contained）

- **單檔 HTML + 內聯 SVG + CSS**
- **雙擊直接在瀏覽器開啟**
- **離線可用**（只調用 Google Fonts）
- **無 build step、無 JavaScript、無外部圖片依賴**

### 2. 設計系統（Editorial Design System）

| 元素 | 規範 |
|------|------|
| **色彩** | 1 個強調色（accent），每圖只強調 1–2 個焦點元素 |
| **字體** | 3 族：Instrument Serif（標題 + 斜體註解）、Geist（節點名）、Geist Mono（技術副標籤） |
| **邊框** | 1px 髮絲線、陰影為 0、半徑 ≤ 10px |
| **網格** | 座標、寬度、間隔全部是 4 的倍數 |
| **語氣** | 珊瑚 coral 強調色 ≠ 警示旗，僅用於重點 |

> **核心哲學：最高品質的動作通常是「刪除」。**
> 每個節點代表一個獨立概念；兩個總是一起出現的節點就是一個節點。目標密度 4/10。

### 3. 39 種圖表類型（三大靜態變體）

每種圖表都附三套**靜態變體**：
```text
minimal light（淺色簡潔）
minimal dark（深色簡潔）
full-editorial（完整編輯，附摘要卡片）
```

---

## 📐 39 種圖表類型總覽

### 架構與流程類

| 圖表 | 用途 |
|------|------|
| **Architecture** | 元件 + 連線 |
| **IT current-state** | 既有架構 + 現代化 |
| **Flowchart** | 決策邏輯 |
| **Sequence** | 訊息隨時間 |
| **State machine** | 狀態 + 轉換 |
| **ER / data model** | 實體 + 欄位 |
| **Timeline** | 時間軸事件 |
| **Swimlane** | 跨職能流程 |
| **High-Level** | 端到端堆疊在叢集 |
| **Process** | 多角色序列流程 |

### 層級與關係類

| 圖表 | 用途 |
|------|------|
| **Quadrant** | 兩軸定位（如 Q2 專案 | 影響 vs 努力） |
| **Nested** | 透過包含的階層 |
| **Tree** | 父 → 子 |
| **Org chart** | 擁有權 + 路由 |
| **Layer stack** | 堆疊抽象 |
| **Venn** | 集合重疊 |
| **Pyramid / funnel** | 排名階層或漏斗 |

### 圖表與數據類

| 圖表 | 用途 |
|------|------|
| **Radar / spider** | 多軸比較 |
| **Polar chart** | 環狀幅度 |
| **Bar chart** | 分類比較 |
| **Treemap** | 面積顯示部分與整體 |
| **Line chart** | 趨勢隨時間 |
| **Gantt** | 任務 + 階段在時間軸 |
| **Scatter plot** | 分佈 + 相關性 |

### 資料系統與部署類

| 圖表 | 用途 |
|------|------|
| **Loop / flywheel** | 增強循環 + 共享中繼站 |
| **Medallion** | 多層資料儲存 |
| **Data flow** | 依角色劃分的管線 |
| **DP integration** | 資料來源 → 核心 → 消費者 |
| **DP security matrix** | 依角色的存取權限 |
| **Sankey** | 可拆分與合併的量 |
| **Fishbone** | 分組原因 → 單一結果 |
| **Wardley map** | 价值链 × 進化 |
| **Kanban** | 按狀態的進行中工作 |
| **User journey** | 階段、動作與情緒 |
| **Deployment** | 區域、主機與產出 |
| **Dependency graph** | Fan-in、排名與迴圈 |
| **UML class** | 類別、操作與型別關係 |
| **Story map** | 脊柱 × 版本切片 |
| **Database schema** | 實體資料表 + 外鍵欄位 |

---

## 🎨 品牌自訂（Onboarding）

### 60 秒把你的品牌套到所有圖表

```text
你：   "onboard diagram-design to https://yoursite.com"
Agent：→ 抓取首頁
       → 提取主導配色 + 字體組合
       → 把偵測值對應到語義角色：
           paper、ink、muted、accent、link
       → 顯示差異預覽
       → 把你的 tokens 寫入 references/style-guide.md
你：   "yes, apply it"
```

### 自動提取規則

| 從你的網站偵測 | 變成 |
|---|---|
| `<body>` 背景 | `paper` token |
| 主要文字顏色 | `ink` token |
| 次要 / 說明文字 | `muted` token |
| 卡片或容器 | `paper-2` token |
| 最常使用的品牌色（CTA、link、標題） | `accent` token |
| `<h1>` 字體族 | `title` 字體 |
| `<body>` 字體族 | `node-name` 字體 |
| `<code>` / `<pre>` 字體 | `sublabel` 字體 |

### 自動對比檢查

寫入 tokens 前會驗證 **WCAG AA** 對比。如果你的網站在圖表尺寸（9–12px）有顏色對比不足，會提出調整值並解釋原因。

### 多客戶管理

```text
吸一次品牌 → 存成 named profile →
在每個客戶專案加 .diagram-design marker（含 profile: <slug>）→
並行工作區可各自用不同品牌，不會覆蓋共享的 style-guide.md
```

---

## 🔌 匯入（Import from draw.io / Mermaid）

已有用 draw.io 或 Mermaid 畫的圖？直接給它源檔案，它會**重繪**——同樣內容、用這個設計系統。

### 四大旋鈕（The Four Dials）

| 旋鈕 | 選項 | 改變 |
|------|------|------|
| **Format** | `html` · `svg` · `png` · `html+png` | 交付物。SVG 給 Figma、PNG 給投影片、HTML 給網頁 |
| **Size** | `doc-inline` · `doc-wide` · `slide-16x9` · `social-og` · `print-a4-landscape` 等 | viewBox 與字型大小（投影片得 16px 節点名） |
| **Detail** | `faithful`（≤24 節點）· `balanced`（≤12）· `simplified`（≤7） | 透過固定退化梯隊保留多少來源 |
| **Audience** | `engineer` · `mixed` · `executive` | 用詞，非數量 |

```bash
# draw.io
/diagram-design:import-drawio platform.drawio --size=slide-16x9 --detail=simplified --audience=executive

# Mermaid
/diagram-design:import-mermaid README.md --diagram=all
```

### 永遠不繼承 vs 永遠會繼承

```text
永遠不繼承：來源座標、來源配色、來源字體、draw.io 的斜線連線、Mermaid 自動佈局
永遠會繼承：元件、關係、分組、方向
```

---

## 📤 匯出（Export PNG / SVG）

圖表以自包含 HTML 交付，但可匯出給 Figma、投影片、社群卡。

| 格式 | 說明 |
|------|------|
| **SVG** | 抽出 `<svg>`、注入 Google Fonts，可獨立在瀏覽器/Figma/Illustrator 渲染 |
| **PNG** | 透過 Playwright 以 2× 栅格化 |

```bash
# Claude Code
/diagram-design:export-diagram path/to/diagram.html --svg-only
/diagram-design:export-diagram path/to/diagram.html --png-only --scale=3

# 安裝 Playwright（PNG 匯出）
pip install playwright && playwright install chromium
```

---

## 🎬 語義模式與可選動畫

### 語義模式（Semantic Patterns）

當「行為」比「外型」更重要時，技能**優先選語義模式、再選視覺類型**。七種路由模式：

```text
fan-in 佇列與瓶頸、重複槽位、非結構化輸入轉換、
配對政策追蹤、安全鋪面、治理目錄、補償式安全層
```

### 可選動畫（Optional Motion）

| 模式 | 說明 |
|------|------|
| `none` | **預設**、靜態、無指令碼 |
| `reveal` | 逐點揭示 |
| `step` | 分步 |
| `loop` | 循環 |

> 動作用是可選的、不創建新圖表類型。`prefers-reduced-motion` 顯示完整靜幀並隱藏播放控制。動作用**精確審查過的 controller**，拒絕遠端資產、CSS `@import`、可執行 HTML 屬性。

---

## ⚙️ 安裝方式

### Claude Code

```text
/plugin marketplace add cathrynlavery/diagram-design
/plugin install diagram-design@diagram-design
```

### Codex

```bash
codex plugin marketplace add cathrynlavery/diagram-design
codex plugin add diagram-design@diagram-design
```

### Factory Droid

```bash
droid plugin marketplace add https://github.com/cathrynlavery/diagram-design
droid plugin install diagram-design@diagram-design --scope user
```

### Pi

```bash
pi install https://github.com/cathrynlavery/diagram-design
# /reload 後用 /skill:diagram-design 呼叫
```

---

## 🏗️ 專案架構（Progressive Disclosure）

```text
diagram-design/
├── .claude-plugin/  .codex-plugin/  .factory-plugin/   # 各平台 manifest
├── skills/diagram-design/
│   ├── SKILL.md                    # 哲學、選型指引、清單
│   ├── references/                 # 選中某類型/原語時才載入
│   │   ├── style-guide.md          # 色彩 + 字體的單一真源
│   │   ├── semantic-patterns.md    # 與佈局獨立的行為模式
│   │   ├── animation.md            # 可選動畫 + 無障礙合約
│   │   ├── onboarding.md           # URL → tokens 流程
│   │   ├── profiles.md             # 命名客戶 profile + marker
│   │   ├── import-drawio.md        # draw.io 重繪程序
│   │   ├── import-mermaid.md       # Mermaid 重繪程序
│   │   ├── output-spec.md          # format × size × detail
│   │   ├── export.md               # SVG / PNG 匯出
│   │   ├── type-*.md               # 39 種類型的佈局參考
│   │   └── primitive-*.md          # 註解、手繪、圖示原語
│   ├── scripts/                    # drawio_extract、mermaid_extract、self_check
│   └── assets/                     # 圖庫 index.html、template、示例
```

### 什麼時候載入什麼（Progressive Disclosure）

| 你要… | Agent 載入 |
|---|---|
| 「畫個流程圖」 | `SKILL.md` + 一種 type 參考 |
| 「畫架構圖」 | `SKILL.md` + type-architecture.md |
| 「比較兩份政策請求差異」 | `SKILL.md` + semantic-patterns.md + type-flowchart.md |
| 「把那條政策追蹤動起來」 | 先選型 + animation.md |
| 「吸我的品牌」 | `SKILL.md` + onboarding.md + style-guide.md |

> **關鍵：無論有幾種類型，Agent 只讀你需要的那一份。**

---

## 🧩 原語（Primitives）

| 原語 | 說明 |
|------|------|
| **Annotation callout** | 斜體 Instrument Serif + 虛線貝氏曲線，放邊界的編輯式旁註 |
| **Sketchy filter** | SVG 紊流 + 位移地圖，手繪變體（適合文章、非技術文件） |
| **Icon set** | 55 個單色 IT/雲圖示（筆電、手機、伺服器、DB、Docker、K8s、AWS、Azure…） |

---

## ✅ 什麼時候「算做好」

- 常規請求（「畫流程圖」）只載入 `SKILL.md` 加一種 type 參考
- 畫之前，Agent 會先說出選的類型、模式、尺寸、打算砍掉什麼，再渲染
- 輸出一個 `.html` 檔，雙擊可開、可離線，只調 Google Fonts
- 無障礙讀屏會朗讀圖表的標題與描述
- `prefers-reduced-motion` 顯示完整靜幀
- `python3 skills/diagram-design/scripts/self_check.py <file>` 印出 `OK`
- 吸完品牌後，新圖表用你網站的 paper、ink、accent、字體（附 fidelity receipt）

---

## 🚫 什麼情況下「不要用」

- 推文或終端機快速 unicode 圖表 → 用 wiretext 技能
- **任何列表** → 用表格或條列
- **前後比較** → 用表格
- **單圖形「圖表」**（一個方塊加標籤）→ 直接寫句子

> 畫之前問：**讀者會從圖學到比好段落更多的東西嗎？** 若不會，就别画。

---

## 📐 CI 驗證（工程品質）

這個專案的 CI 非常嚴格，涵蓋：

| 檢查 | 說明 |
|------|------|
| **lint-skin.py** | 讀來源、檢查 skin |
| **lint-render.py** | Chromium 無頭渲染、檢查裁切/溢出 |
| **verify-geometry.py** | 標籤遮罩不會覆蓋後方節點 |
| **verify-treemap.py** | 面積誤差為相對值（不是絕對值） |
| **verify-sankey.py** | Sankey 守恆 + 幾何 |
| **verify-polar.py** | 極座標編碼量化 |
| **verify-doctor.py** | 環境診斷合約 |
| **verify-drawio-import.py** | 四種 container 格式真抽取器 |
| **verify-mermaid-import.py** | 支援所有 grammar、多區塊 Markdown |

所有 PR 與 push 在 Linux / Windows / macOS 三平台 CI 自動驗證。

---

## 總結

**Diagram Design** 是 Cathryn Lavery 開源給 AI Agent（Claude Code / Codex / Pi / Factory Droid）的技能，核心亮點：

```text
一個指令 → 39 種編輯風格圖表 → 自包含 HTML/SVG
（無陰影、品牌自訂、匯入 draw.io/Mermaid、匯出 PNG/SVG）
```

它解決了「AI 畫的圖表太醜、不符合品牌」的痛點，用**編輯設計品質**的標準（無陰影、4px 網格、1 強調色）生成圖表，並能**自動吸你網站的品牌色**。配合進階的匯入/匯出、可選動畫、語義模式，以及嚴格的 CI 驗證，是技術作者、PM、架構師製作高品質圖表的強大工具。

---

*本文於 2026-09-03 整理自 [github.com/cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)*
