---
title: "Claude SEO 功能介紹：Claude Code 裡的免費開源 SEO 全面稽核外掛"
date: 2026-10-28
description: "整理 AgriciDaniel/claude-seo：26 個子技能、19 個專職代理、30 個 /seo 指令，涵蓋技術 SEO、E-E-A-T、Schema.org、GEO/AEO、Agent Readiness、本地與電商 SEO，以及 9 個可選擴充。含架構、安裝、限制與比較表。"
tags: [seo, claude-code, ai-seo, geo, schema, open-source]
---

# Claude SEO 功能介紹：Claude Code 裡的免費開源 SEO 全面稽核外掛

**專案：** [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo)
**定位：** 一組給 Claude Code 使用的「通用 SEO 技能」，直接以 `/seo` 指令對任何網站跑完整稽核，10–15 分鐘內輸出依影響力排序的行動計畫。
**授權：** MIT（免費、無使用上限、無追蹤）。**主要語言：** Python。

---

## 一、專案概況

| 項目 | 內容 |
|---|---|
| 全名 | `AgriciDaniel/claude-seo` |
| 一句話描述 | 通用 SEO 技能：26 個子技能 + 19 個子代理，涵蓋技術 SEO、E-E-A-T、Schema、GEO/AEO、Agent Readiness、反向連結、本地/電商/國際 SEO、Google API、PDF/Excel 報告；另有 9 個可選擴充取得即時 SEO 資料 |
| Stars / Forks | 約 23,000 / 3,125（API 讀取當日數據） |
| 授權 | MIT License |
| 語言 | Python |
| 版本 | `pyproject.toml` 標示 2.5.0 |
| 建立 / 最近推送 | 2026-02-07 / 2026-10-22 |
| Open issues | 69 |
| 官方站 | `claude-seo.md`（作者自用站，自第一天起以此工具稽核） |
| 主題標籤 | ai, ai-seo, claude-code, claude-code-skill, marketing-automation, open-source, seo |

README 宣稱的測試規模：**1077 個測試通過**（badge），CI 走 `.github/workflows/ci.yml`。

---

## 二、它是什麼、不是什麼

它不是爬蟲工具，也不是排行追蹤 SaaS。它是一套**「把 SEO 顧問的檢查清單代理化」**的技能包：

- 給它任意網址 → 自動偵測業務類型（SaaS／本地／電商／出版／代理商）→ 調度最多 **17 個專職代理並行**稽核 → 匯總成 **SEO Health Score（0–100）** 與**依影響力排序的行動計畫**。
- 每條建議都說明「依據是什麼、依賴什麼、怎麼驗證它真的生效」。
- 報告以 Markdown 落地在本地，`/seo google report` 可轉成 PDF（另有 Excel 匯出）。

與 Screaming Frog 類工具的分工：爬蟲更快更深、大廠有自有反向連結資料庫；Claude SEO 的強項是**解釋與排序、AI 搜尋深度、可用自然語言追問**。作者明講「很多人兩者並用」。

---

## 三、架構：26 技能 × 19 代理

依 `docs/ARCHITECTURE.md`：**26 個子技能**（22 核心 + 1 主控 orchestrator + 1 框架整合 + 2 擴充鏡像）與 **19 個子代理**（16 核心 + 1 框架整合 + 2 擴充鏡像）。

### 3.1 目錄結構

```
claude-seo/
├── skills/seo/                 # 主控 orchestrator（路由與調度）
│   └── references/             # 按需載入的參考檔（13 個）
├── skills/seo-audit/           # 全站稽核（平行子代理）
├── skills/seo-page/            # 單頁深挖
├── skills/seo-technical/       # 技術 SEO（9 類）
├── skills/seo-content/         # E-E-A-T 與內容品質
├── skills/seo-content-brief/   # 競品式內容 brief
├── skills/seo-schema/          # Schema.org 偵測/驗證/生成
├── skills/seo-sitemap/         # XML sitemap 分析與生成
├── skills/seo-images/          # 圖片優化
├── skills/seo-geo/             # AI 搜尋（GEO）
├── skills/seo-agentic/         # Agent readiness（Lighthouse Agentic、WebMCP）
├── skills/seo-local/           # 本地 SEO（GBP、citation、評論）
├── skills/seo-maps/            # 地圖情報（geo-grid、GBP 稽核）
├── skills/seo-backlinks/       # 反向連結輪廓
├── skills/seo-cluster/         # 以 SERP 為基礎的語意叢集
├── skills/seo-sxo/             # 搜尋體驗優化
├── skills/seo-drift/           # SEO 漂移監控（baseline）
├── skills/seo-ecommerce/       # 電商 SEO
├── skills/seo-hreflang/        # 國際 SEO / hreflang
├── skills/seo-plan/            # 策略規劃（產業模板）
├── skills/seo-programmatic/    # 程式化 SEO
├── skills/seo-competitor-pages/# 競品比較頁生成
├── skills/seo-google/          # Google API（GSC/PSI/CrUX/GA4）
├── skills/seo-flow/            # FLOW 框架（CC BY 4.0）
├── skills/seo-dataforseo/      # DataForSEO MCP 鏡像（擴充）
└── skills/seo-image-gen/       # Banana MCP 鏡像（擴充）

agents/                         # 19 個 *.md 代理定義
extensions/                     # ahrefs, banana, bing-webmaster, dataforseo,
                                # firecrawl, matomo, profound, seranking, unlighthouse
scripts/                        # 61 個 Python 腳本（fetch_page, render_page,
                                # lighthouse_agentic, gsc_query, google_report ...）
hooks/  data/  schema/  docs/  tests/
```

### 3.2 全站稽核的調度流程

```
使用者請求
   │
   ▼
seo（主控 orchestrator）
   │ 偵測業務類型與訊號
   │ 平行 spawn 子代理
   ├─ seo-technical ─ seo-content ─ seo-schema ─ seo-sitemap
   ├─ seo-performance ─ seo-visual ─ seo-geo
   └─ 條件式：seo-google（有 Google API 憑證）、seo-local（本地商家）、
               seo-maps（本地 + DataForSEO MCP）、seo-backlinks（Moz/Bing/CC）、
               seo-cluster（內容策略訊號）、seo-sxo（全站稽核必開）、
               seo-drift（該 URL 已有 baseline）、seo-ecommerce（電商偵測）
   ▼
彙整 → SEO Health Score + 行動計畫 → FULL-AUDIT-REPORT.md / ACTION-PLAN.md
```

依 `docs/COMMANDS.md`：全站稽核最多爬 **500 頁**，分派 **9 個固定代理 + 8 個條件式代理**（最多 17 個並行）。

### 3.3 四個設計原則

1. **Progressive disclosure**：主 SKILL.md 控制在 500 行內，細節放子技能與按需載入的 reference 檔。
2. **平行處理**：代理彼此不阻塞，最後彙整。
3. **Quality gates**：內建門檻避免爛建議，例如地區頁上限（30 個警告／50 個硬停）、Schema 棄用警示、強制以 **INP 取代 FID**。
4. **產業感知**：SaaS／本地／電商／出版／代理商各有模板，從首頁訊號自動判斷。

### 3.4 執行環境的巧思

所有內建腳本都經由 `scripts/claude-seo` + `runtime.py` 啟動器呼叫，**不允許裸 `python` 直接跑**：

- 啟動器在 Python 3.11–3.14 範圍內解析可用解釋器（`CLAUDE_SEO_PYTHON` → 預設解釋器 → 最新版號）。
- 技能與代理以 `"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" run <script.py>` 的相對路徑呼叫，Claude Code 會展開該變數；**刻意不放頂層 `bin/`**，因為 claude.ai 託管的 marketplace 會以 `marketplace_sync_bin_directory_not_allowed` 拒絕。
- 環境狀態（runtime 結構、requirements 的 SHA-256、Python 版本、外掛版本、瀏覽器狀態）寫入 marker；環境替換先暫存、驗證失敗即回滾。
- `run` 只接受白名單腳本檔名、參數不經 shell、保留子程序 exit code、強制 UTF-8。

### 3.5 依賴（requirements.txt 有明確 CVE 下限）

`beautifulsoup4`、`requests`、`lxml`、`lxml_html_clean`、`playwright`、`urllib3`、`trafilatura`、`htmldate`、`courlan`、`matplotlib`、`numpy`、`weasyprint`、`openpyxl`、`pillow`，以及 Google API 系列（`google-api-python-client`、`google-auth`、`google-ads`、`google-analytics-data`）。版本以 `>=X,<Y` 綁定並在註解中標明修補的 CVE／GHSA。

---

## 四、19 個專職代理與對應指令

| Agent | 角色 | 模型 | 指令 |
|---|---|---|---|
| `seo-technical` | 技術 SEO 主責 | Sonnet | `/seo technical` |
| `seo-content` | 內容編輯（E-E-A-T） | Opus | `/seo content` |
| `seo-schema` | 結構化資料工程 | Sonnet | `/seo schema` |
| `seo-sitemap` | Sitemap 架構 | Sonnet | `/seo sitemap` |
| `seo-performance` | Core Web Vitals | Sonnet | `/seo audit` |
| `seo-visual` | 視覺/行動渲染 QA | Sonnet | `/seo audit` |
| `seo-geo` | AI 搜尋分析（GEO） | Opus | `/seo geo` |
| `seo-agentic` | Agent readiness | Sonnet | `/seo agentic` |
| `seo-local` | 本地 SEO | Sonnet | `/seo local` |
| `seo-maps` | 地圖情報 | Sonnet | `/seo maps` |
| `seo-google` | Google 資料分析 | Sonnet | `/seo google` |
| `seo-backlinks` | 連結分析 | Sonnet | `/seo backlinks` |
| Live data（擴充） | 即時資料分析 | Sonnet | `/seo audit` |
| `seo-image-gen`（擴充） | 圖片生產 | Sonnet | `/seo image-gen` |
| `seo-cluster` | 主題策略 | Opus | `/seo cluster` |
| `seo-sxo` | 搜尋體驗設計 | Opus | `/seo sxo` |
| `seo-drift` | 變更監控 | Opus | `/seo drift` |
| `seo-ecommerce` | 電商專責 | Sonnet | `/seo ecommerce` |
| `seo-flow` | FLOW 策略 | Sonnet | `/seo flow` |

**成本提醒：** 需要較多判斷力的代理跑 Opus，其餘跑 Sonnet，因此一次完整 `/seo audit` 會比單頁檢查吃掉更多額度；每個代理的模型可在 `agents/*.md` 內改。

---

## 五、30 個核心＋擴充指令（六大群組）

### 4.1 稽核與規劃（5）
- `/seo setup` — 建立/刷新隔離的 Python 執行環境與 Chromium
- `/seo doctor` — 唯讀檢查環境就緒度，不動系統
- `/seo audit <url>` — 全站稽核（平行代理）
- `/seo page <url>` — 單頁深挖
- `/seo plan <type>` — 策略規劃（saas / local / ecommerce / publisher / agency）

### 4.2 技術 SEO（7）
- `/seo technical <url>` — 9 類別技術稽核：可爬取性、可索引性、安全性、URL 結構、行動優化、Core Web Vitals（LCP/INP/CLS）、結構化資料、JS 渲染、IndexNow
- `/seo sitemap <url|generate>` — sitemap 分析或生成
- `/seo images <url>` — 圖片優化分析
- `/seo hreflang <url>` — hreflang / i18n 稽核與生成
- `/seo programmatic <url>` — 程式化 SEO 分析與規劃
- `/seo google [command]` — GSC、PageSpeed、CrUX、Indexing、GA4、PDF 報告
- `/seo drift baseline|compare|history <url>` — 以 SQLite 快照做漂移監控

### 4.3 內容與 E-E-A-T（6）
- `/seo content <url>` — 經驗/專業/權威/可信度 + AI 引用準備度 + 內容新鮮度
- `/seo content-brief <topic>` — 關鍵字、意圖、章節大綱、內鏈、競品切入角度
- `/seo cluster <keyword>` — 以 SERP 做語意叢集
- `/seo sxo <url>` — 頁型、user stories、personas
- `/seo flow [stage]` — FLOW 框架提示詞（CC BY 4.0，evidence-led）
- `/seo competitor-pages <url>` — 競品比較頁生成

### 4.4 Schema 與 AI 搜尋（3）
- `/seo schema <url>` — 偵測、驗證、生成 Schema.org
- `/seo geo <url>` — AI Overviews / Generative Engine Optimization：可被引用的程度、AI 爬蟲可及性、品牌在 Wikipedia/Reddit/YouTube/LinkedIn 的存在感
- `/seo agentic <url>` — Agent readiness：Lighthouse Agentic Browsing **X/N** 分數、accessibility tree、AI 代理存取、`llms.txt`、Markdown 版本、WebMCP

### 4.5 本地、連結、商務（4）
- `/seo local <url>` — GBP、citation、評論、map pack
- `/seo maps [command]` — geo-grid、GBP 稽核、評論、競品
- `/seo backlinks <url>` — Moz、Bing、Common Crawl（免費）；DataForSEO（付費）
- `/seo ecommerce <url>` — 產品 schema 與 marketplace 情報

### 4.6 擴充指令（5）
- `/seo image-gen [use-case]` — SEO 素材 AI 生圖
- `/seo seranking [command]` — ChatGPT/Gemini/Perplexity/AI Overviews/AI Mode 的 Share-of-Voice
- `/seo profound [command]` — LLM 引用追蹤（時間序列）
- `/seo bing [command] <url>` — Bing Webmaster Tools + IndexNow 即時提交
- `/seo unlighthouse <url>` — 本地跑全站 Lighthouse

---

## 六、安裝與第一次稽核

**需求：** Claude Code **1.0.33+**、Python **3.11–3.14**。

### 外掛方式（推薦）
```bash
/plugin marketplace add AgriciDaniel/claude-seo
/plugin install claude-seo@agricidaniel-claude-seo
/seo setup        # 準備獨立 Python 環境 + headless 瀏覽器
/seo doctor       # 隨時驗環境
```

### 手動安裝：macOS / Linux
```bash
git clone --depth 1 https://github.com/AgriciDaniel/claude-seo.git
bash claude-seo/install.sh
```

### 手動安裝：Windows（PowerShell）
```powershell
git clone --depth 1 https://github.com/AgriciDaniel/claude-seo.git
powershell -ExecutionPolicy Bypass -File claude-seo\install.ps1
```
作者特意說明用 `git clone` 而非 `irm ... | iex`：Claude Code 會把「下載並直接執行遠端程式」視為供應鏈風險，先 clone 才能檢查 `install.ps1`。

### 第一次跑
```bash
claude
/seo audit https://example.com         # 全站 + 排序後行動計畫
/seo page  https://example.com/pricing # 單頁深挖
/seo geo   https://example.com         # AI 搜尋準備度
/seo schema https://example.com        # 結構化資料檢查與生成
/seo local https://example.com         # 本地 SEO / GBP
```

**移除：** 外掛安裝者用 `/plugin uninstall claude-seo@agricidaniel-claude-seo`；手動安裝者跑 `claude-seo/uninstall.sh`。

---

## 七、兩條版本線

| 版本 | 授權／取得方式 | 差異 |
|---|---|---|
| 公開版 | MIT，任何人可用 | 全部功能、無使用限制 |
| 私享版 | [AI Marketing Hub Pro](https://www.skool.com/ai-marketing-hub-pro) 會員 | 新功能早期存取 |

私享版安裝：
```bash
/plugin marketplace add AI-Marketing-Hub/claude-seo
/plugin install claude-seo@ai-marketing-hub-claude-seo
/seo setup
```

---

## 八、9 個可選擴充（不裝也能完整運作）

| 擴充 | 提供什麼 |
|---|---|
| **Banana** | Claude Banana 的 AI 生圖（社群預覽圖、部落格主圖） |
| **SE Ranking** | 在 ChatGPT、Gemini、Perplexity、Google AI 回答中的 Share of Voice |
| **Profound** | AI 模型引用你網站的追蹤 |
| **Bing Webmaster** | Bing 資料 + IndexNow 即時提交 |
| **Unlighthouse** | 全站每頁 Lighthouse 分數（本地執行） |
| **DataForSEO** | 付費 SERP/關鍵字/商家資料（MCP） |
| **Firecrawl** | 抓取/渲染替代管線 |
| **Matomo** | GA4 的替代或補充（Reporting API） |
| **Ahrefs** | 反向連結與關鍵字資料（MCP） |

擴充各自帶 `install.sh` / `install.ps1` / `uninstall.*` 與 setup 文件，放在 `extensions/<name>/`。

---

## 九、價格／替代方案比較（作者自述，僅示意）

| | 人工執行 | 找代理商 | SEO 軟體 | **Claude SEO** |
|---|---|---|---|---|
| 單次稽核時間 | 4–8 小時 | 1–3 週 | 10–45 分鐘 | **10–15 分鐘** |
| 成本 | 計費工時 | 每案 $2k–$15k+ | $99–$999/月 | **免費（只需 Claude Code 方案）** |
| 檢查一致性 | 依執行者 | 依團隊 | 有 | **每次同一份清單** |
| 產出物 | 表格/PDF | 簡報 | 儀表板 + CSV | **Markdown / PDF / JSON，留在你手上** |
| 資料歸屬 | 有 | 無 | 無 | **在本機執行** |
| AI 搜尋覆蓋 | 不一定 | 不一定 | 常落後數月 | **有，跟隨 Google 最新指引** |
| 每項修正是否附驗證方法 | 有時 | 有時 | 罕見 | **有** |

---

## 十、限制與注意事項（README 明列）

1. **資料仍會送到 Anthropic 模型**：Claude SEO 在 Claude Code 內執行，被分析的頁面與資料如同你在 Claude Code 做的任何工作一樣會送給 Claude；報告只是落在本機檔案。除你自行接的擴充/API 外，沒有第三方 SEO 服務看到你的資料（另有 Wikipedia、Reddit、Common Crawl 等公開來源讀取，詳見 `PRIVACY.md`）。
2. **沒有 Google API key 時**，Core Web Vitals 是實驗室估計、索引狀態是推斷。
3. **需要滾動/點擊才出現內容的頁**，結果可能偏噪。
4. **成本**：完整稽核以 Opus 代理為主，較吃方案額度。
5. **不是爬蟲替代品**：深度與速度不如 Screaming Frog；反向連結資料庫不如商業套件。
6. **JS 站（Next.js / React / Vue）可行**：內容需 JS 呈現時會自動用 headless 瀏覽器開啟，以訪客所見狀態稽核。

---

## 十一、同家族專案

| 專案 | 用途 |
|---|---|
| [Claude Blog](https://github.com/AgriciDaniel/claude-blog) | 依 SEO 發現撰寫並優化部落格文章 |
| [Claude Banana](https://github.com/AgriciDaniel/banana-claude) | SEO 素材與貼文的 AI 生圖 |
| [ChatGPT SEO](https://github.com/AgriciDaniel/chatgpt-seo) | 在 ChatGPT 內把頁面/草稿/匯出檔變成有出處的修正計畫 |
| [FLOW](https://github.com/AgriciDaniel/flow) | 證據導向 SEO 框架，42 個 AI 提示詞 |
| [AI Marketing Claude](https://github.com/zubair-trabzada/ai-marketing-claude) | 文案、Email、廣告、漏斗的社群套件 |

---

## 十二、適合誰

- **SEO 代理商**：把「每季稽核」變成「每週每客戶稽核」，用 drift 監控抓變化。
- **企業內部 SEO 團隊**（SaaS、出版、電商）：每次上線/審稿前的第二雙眼睛，含 AI 搜尋。
- **自由接案顧問**：第一通電話就能給出真實分數與前幾項修正，再談提案。

反過來說：若你要的是**大規模爬取與自有連結資料庫**，請搭配 Screaming Frog / Ahrefs 等；Claude SEO 的價值在「解釋、排序、驗證方法、AI 搜尋準備度」。

---

## 參考

- 專案首頁：<https://github.com/AgriciDaniel/claude-seo>
- 架構文件：`docs/ARCHITECTURE.md`
- 指令參考：`docs/COMMANDS.md`
- 方法論：`skills/seo/references/thinking-framework.md`
- Google AI 優化指引：<https://developers.google.com/search/docs/fundamentals/ai-optimization-guide>
- 隱私：`PRIVACY.md`；安全：`SECURITY.md`；貢獻：`CONTRIBUTING.md`
- 作者：Agrici Daniel（<https://agricidaniel.com/about>）

*本文依 2026-10-28 讀取的 GitHub API、README、ARCHITECTURE.md、COMMANDS.md 與 requirements.txt 整理；Stars/Forks 為當日數值，會持續變動。*
