---
title: "Oh My PPT：本地優先 AI 簡報生成器功能總覽"
date: 2026-09-09
description: "Oh My PPT 是一個本地優先的 AI 簡報工具，用自然語言描述主題即可生成可編輯 HTML 簡報，支援 PPTX 雙向轉換、AI 生圖配圖、90+ 風格模板與多格式導出。"
tags: [ai-ppt, presentation, html-slides, local-first, electron]
---

# Oh My PPT：本地優先 AI 簡報生成器功能總覽

![Oh My PPT Demo](/assets/images/oh-my-ppt/demo.gif)

[![Star History Chart](/assets/images/oh-my-ppt/star_history.svg)](https://star-history.dera.page/#arcsin1/oh-my-ppt&Date)

## 專案概覽

**Oh My PPT** 是一個本地優先（local-first）的 AI 簡報生成與編輯工具。用自然語言描述你想表達的內容，AI 自動完成大綱、頁面排版與配圖，生成可編輯的 HTML 簡報。從創作到編輯、演示與導出，全部在本地完成——不需要帳號、不上傳雲端。

| 項目 | 資訊 |
|------|------|
| **倉庫** | [arcsin1/oh-my-ppt](https://github.com/arcsin1/oh-my-ppt) |
| **Stars** | ⭐ 1,934 |
| **Forks** | 190 |
| **授權條款** | Apache License 2.0 |
| **主要語言** | TypeScript (React + Electron) |
| **支援平台** | Windows / macOS（桌面應用） |
| **最新版本** | v2.5.1 (2026-09) |
| **官網** | [ohmyppt.cc](https://www.ohmyppt.cc) |
| **建立日期** | 2026-04 |

> 核心理念：讓 AI HTML PPT 成為可能。生成的是 HTML 版簡報——打開即預覽、無需安裝軟體、一個瀏覽器搞定，還能隨心改樣式、加動效、插代碼、導出分享。

## 核心功能

### 1. PPTX 雙向轉換（純自研）

Oh My PPT 最突出的能力是 **PPTX 的雙向轉換**，由作者純自研實現：

| 方向 | 說明 |
|------|------|
| **📥 PPTX 導入** | 已有 PPTX 模板、歷史匯報或客戶文件可導入，接近 **100%** 視覺與結構還原，轉為可拖拽、AI 修改和版本管理的頁面 |
| **📤 PPTX 導出** | 編輯完成後導出為 PowerPoint / Keynote 中可繼續修改的真實 PPTX，保留文字、圖片、顏色、公式和基本佈局 |

相關開源套件：
- [@arcsin1/pptx2json](https://www.npmjs.com/package/@arcsin1/pptx2json) — PPTX 解析與結構化轉換
- [@arcsin1/html2pptx](https://www.npmjs.com/package/@arcsin1/html2pptx) — HTML 轉可編輯 PPTX

> 複雜形狀、圖表、表格、動畫和極端排版仍在持續優化中。

### 2. 多種創作入口

| 入口 | 說明 |
|------|------|
| **主題創作** | 填寫主題、尺寸格式和詳細描述，AI 生成完整簡報 |
| **對話創作** | 多輪對話梳理主題、資料、受眾和結構，適合需求不清晰的場景 |
| **上傳文檔解析** | 上傳 txt / md / csv / docx，自動整理主題和頁數，參考原文件內容生成 |
| **從模板創建** | 選擇已保存的模板，沿用版式、配色和視覺節奏重新生成 |

### 3. 多尺寸 / 多內容格式畫布

不只支援傳統 PPT 尺寸：

- 16:9 寬屏演示
- 4:3 投屏
- 9:16 豎屏
- 3:4 豎版
- 1:1 方圖
- 小紅書圖文格式

生成、預覽、編輯和導出都會保留真實比例。

### 4. AI 生圖與智能配圖

| 使用場景 | 操作方式 | 結果 |
|----------|----------|------|
| **整套演示稿** | 設置中驗證生圖模型 → 創建頁勾選「啟用配圖」→ 選帶「支持生圖」標識的風格 | AI 僅在合適位置自動生成插畫、背景或視覺元素，保留文字安全區 |
| **編輯已有頁面** | 打開編輯頁的生圖面板，參考當前頁內容生成提示詞 | 可預覽結果，插入畫布排版或設為頁面背景 |

支援的生圖 Provider：即夢 3.0/4.0、Agnes AI、Seedream、矽基流動、Gemini、OpenAI 兼容圖片接口。

> 自動配圖不會機械地給每頁塞圖——只在真正需要視覺素材的位置生成，保持風格一致性。

### 5. 90+ 內建風格 Skill

![Style Library](/assets/images/oh-my-ppt/style.webp)

內建 90+ 種設計風格：極簡白、賽博霓虹、包豪斯、日式簡約、小紅書白……也支持自訂風格。可透過官方 [style-generate-skill](https://github.com/arcsin1/style-generate-skill) 把參考設計整理成可導入的風格包。

### 6. 對話式修改與視覺化編輯

- **對話式修改**：對著某一頁說「標題換個顏色」「加個數據圖表」，精準修改不用重做
- **視覺化編輯**：一切可見元素皆可拖拽和調整大小，皆可檢選並讓 AI 修改
- **插入圖片/視頻**：從素材庫或本地文件添加，也能與 AI 生成圖片混用
- **複製元素**：一鍵複製任意元素，自動偏移並獨立可編輯
- **撤銷/重做**：隨時操作，最後統一保存為版本記錄

### 7. 動畫支持

![Animation Demo](/assets/images/oh-my-ppt/anime.gif)

- **16+ 種頁面切換動畫**
- 內建本地 **Anime.js v4** 動畫運行時
- 可選中單個元素設置入場、強調或退出效果
- 調整自動/點擊觸發、時長和方向
- AI 可自動為標題、數據卡片、圖片、圖表容器添加演示動畫

### 8. 字體管理

![Font Management](/assets/images/oh-my-ppt/font.webp)

- 內建 14 款精選 Google 字體（含中文）
- 支持上傳本地 `.woff2` 字體文件
- 創建時可分別指定**標題字體**和**正文字體**，也可交給 AI 自動匹配
- 導出 PPTX 時已使用的字體自動嵌入

### 9. 演講稿生成

支持為整套幻燈片或當前頁生成演講稿，內建四種風格：
- 正式演講
- 輕鬆對話
- 敘事風格
- 自訂風格

### 10. 多格式導出

| 格式 | 用途 |
|------|------|
| **PDF** | 直接分享、歸檔和列印 |
| **PNG（批量）** | 插入文檔、Notion、公眾號或社媒 |
| **PNG 長圖** | 整套頁面縱向拼接，適合社媒和行動端 |
| **可編輯 PPTX** | PowerPoint / Keynote 中繼續修改 |
| **MP4** | 發布到社媒或不方便播放 PPT 的場景 |
| **HTML 打包文件** | 單個可執行檔，雙擊即開預覽，無需安裝 |

### 11. 本地 Ollama 模型支援

透過 OpenAI 兼容協議接入本地 Ollama：

```text
provider:  openai
base_url:  http://127.0.0.1:11434/v1
model:     qwen2.5-coder:14b（建議 14B+）
api_key:   ollama（任意非空字串）
```

> Ollama 配置用於文字生成、文檔解析和編輯對話；生圖需另行配置支援圖片生成的 Provider。

### 12. 其他實用功能

- **多任務並行**：同時提交多個生成任務，後台完成時自動通知
- **歷史版本回退**：自動保存每次修改記錄，任意版本一鍵回退
- **模板庫**：將已生成/編輯的簡報保存為模板，PPTX 也可導入為模板
- **圖片識別生成風格**：上傳截圖/設計稿，自動識別視覺特徵並生成獨特風格（需多模態模型）
- **數學公式渲染**：支援 LaTeX 公式顯示，適合課堂和技術分享
- **會話管理**：區分 AI 創建和 PPTX 導入的會話
- **一鍵打包**：HTML 簡報打包為單一可執行檔

## 使用流程

```
選擇創作方式（主題/對話/文檔/模板/PPTX導入）
        ↓
確認主題 / 資料 / 頁數 / 尺寸 / 風格 / 字體 / 配圖
        ↓
AI 生成 HTML 簡報
        ↓
預覽 → 演示 → 編輯（拖拽、對話修改、生圖、動畫）
        ↓
導出：PPTX / PDF / PNG / MP4 / HTML 打包
```

## 技術架構

```
┌──────────────────────────────────────────────┐
│            Oh My PPT (Electron Desktop)      │
├──────────────────────────────────────────────┤
│              React + TypeScript UI           │
│  ┌─────────┬──────────┬──────────────────┐  │
│  │ 編輯器   │ 預覽/演示 │  模板庫 / 會話    │  │
│  │(拖拽/AI) │(全屏播放) │  (版本管理)       │  │
│  └─────────┴──────────┴──────────────────┘  │
├──────────────────────────────────────────────┤
│           Core Engine                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ PPTX     │  │ AI 生圖   │  │ 動畫引擎  │  │
│  │ 雙向轉換  │  │ Provider │  │ Anime.js │  │
│  │(自研)    │  │ 管理器    │  │ v4       │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ 90+ 風格  │  │ 字體管理  │  │ 多尺寸   │  │
│  │ Skill    │  │(14款+自訂)│  │ 畫布引擎  │  │
│  └──────────┘  └──────────┘  └──────────┘  │
├──────────────────────────────────────────────┤
│         AI Backend (OpenAI-compatible)       │
│   Ollama / DeepSeek / Kimi / GPT / Claude    │
│   + 生圖: 即夢/Seedream/Gemini/OpenAI        │
└──────────────────────────────────────────────┘
```

## 與其他 AI PPT 工具比較

| 特性 | **Oh My PPT** | 一般 AI PPT 工具 |
|------|---------------|-----------------|
| 輸出格式 | HTML（可編輯）+ PPTX | 固定格式 PPTX |
| PPTX 導入還原 | 接近 100%（純自研） | 通常不支援或還原度低 |
| 本地優先 | ✅ 無需帳號/雲端 | ❌ 多數需雲端 |
| AI 生圖配圖 | ✅ 多 Provider | 部分支援 |
| 對話式修改 | ✅ 精準到單頁元素 | ❌ 通常只能重新生成 |
| 動畫 | 16+ 切換 + Anime.js 元素動畫 | 有限或無 |
| 多尺寸畫布 | 6+ 種（含豎屏/方圖） | 通常僅 16:9 |
| 歷史版本回退 | ✅ 任意版本一鍵回退 | ❌ |
| MP4 導出 | ✅ | 部分支援 |
| 本地 Ollama | ✅ OpenAI 兼容 | ❌ |

## 推薦模型配置

README 推薦的文本生成模型：
- **國產**：DeepSeek V4、Kimi、豆包（Doubao）、Qwen、GLM、小米 MiMo、MiniMax
- **國際**：GPT、Claude
- **本地**：Ollama + Qwen 14B+

## 已知限制

- macOS / Windows 首次開啟可能出現未簽名應用安全提示（非損壞）
- PPTX 導入/導出對極端複雜排版仍在優化中
- 逐字級字幕僅英文（Kokoro 限制，同 abogen 專案）
- 生圖會將提示詞發送到所選 Provider（注意隱私政策）

## 主要貢獻者

| 貢獻者 | Commits | 角色 |
|--------|---------|------|
| arcsin1 | 451 | 核心開發者 |
| Jacobinwwey | 34 | 功能貢獻 |
| whisper-xiang | 23 | 功能貢獻 |

## 參考連結

- **GitHub**: https://github.com/arcsin1/oh-my-ppt
- **官網**: https://www.ohmyppt.cc
- **Releases（下載安裝包）**: https://github.com/arcsin1/oh-my-ppt/releases
- **pptx2json**: https://www.npmjs.com/package/@arcsin1/pptx2json
- **html2pptx**: https://www.npmjs.com/package/@arcsin1/html2pptx
- **Style Generate Skill**: https://github.com/arcsin1/style-generate-skill
- **Discord**: https://discord.gg/FSkzBgsQ
- **Star History**: https://star-history.dera.page/#arcsin1/oh-my-ppt&Date
