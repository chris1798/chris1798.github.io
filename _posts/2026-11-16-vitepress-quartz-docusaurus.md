---
title: "VitePress vs Quartz vs Docusaurus：三個靜態站產生器的功能與場景比較"
date: 2026-11-16
description: 比較 VitePress（Vue/Vite 系文件站）、Quartz（數位花園筆記站）與 Docusaurus（Meta 維護的多語言文件平台）三個 TypeScript 靜態站產生器：定位、核心功能矩陣、維護模式、建置體驗與適用場景，附選擇決策清單與 2026-11-16 驗證的星數、授權、最新版本數據。
tags: [VitePress, Quartz, Docusaurus, 靜態網站, 文件站, 數位花園, 比較, TypeScript, 開源專案]
---

# VitePress vs Quartz vs Docusaurus：三個靜態站產生器的功能與場景比較

這三個專案常被放在一起搜尋——它們都是 TypeScript 寫成、MIT 授權的靜態站產生器（SSG），但**它們解答的其實是三個不同的問題**。本文以 2026-11-16 的 GitHub API 驗證數據為基礎，比較功能矩陣與適用場景。

## 基本盤

| | VitePress | Quartz (v5) | Docusaurus |
|---|---|---|---|
| 倉庫 | [vuejs/vitepress](https://github.com/vuejs/vitepress) | [jackyzha0/quartz](https://github.com/jackyzha0/quartz) | [meta/docusaurus](https://github.com/meta/docusaurus) |
| 定位自述 | Vite & Vue 驅動的文件站 | 把筆記發佈成網站的「數位花園」工具 | 易於維護的開源專案網站 |
| 星數 | 18,491 | 13,596 | **66,747** |
| Fork | 2,759 | 4,144 | 10,140 |
| 授權 | MIT | MIT | MIT |
| 創建 | 2020-04 | 2021-07 | 2017-06 |
| 最新版本 | v2.0.0-alpha.21（2026-10-25） | v5.1.0（2026-11-09） | v3.10.2（2026-07-10） |
| 維護者 | Evan You（Vue 作者）＋ VoidZero/Vue 生態贊助 | 個人開發者 jackyzha0（讚助手計畫） | Meta（倉庫要 facebook/docusaurus 已遷移至 meta 組織） |
| 最近 push | 2026-11-12 | 2026-11-15 | 2026-11-15 |
| 開放議題 | 381 | 72 | 441 |

三個都在活躍維護。值得留意的是版本態勢：VitePress 正式版停在 v1.x，**v2.0 仍在 alpha**（alpha.21）；Quartz 已演進到完全重寫的 v5；Docusaurus 在 v3 線上穩定小步快跑。

## 定位：一句話版

* **VitePress**：「Vue 生態的 Vite 文件站」。Markdown 檔案就是頁面、內嵌 Vue SFC 就是互動元件，開發伺服器與建置都騎在 Vite 上。VuePress 的精神繼承者。
* **Quartz**：「把 Obsidian／Markdown 筆記變成双向連結的知識網站」。重點不是文件結構，而是**筆記之間的連結圖**：wikilink、反鏈、圖譜、彈出預覽，全站靜態產出。
* **Docusaurus**：「開源專案的官網基建」。文件＋版本化文件＋部落格＋多語言＋主題設定，一個 CLI 生成，Meta 用來支撐自家大量 OSS 專案的官網。

## 功能矩陣

| 功能 | VitePress | Quartz | Docusaurus |
|---|:---:|:---:|:---:|
| 技術基底 | Vite + Vue 3 | 自建管線（TypeScript，UI 精簡、強調速度） | React + webpack/MF 系工具鏈（v3 起內建 Swc） |
| 文件側欄／目錄 | ✅ 主題內建 | ⚙️ Explorer 元件（樹狀導覽） | ✅ 側欄系統，自動生成 |
| 部落格 | ⚙️ 自建（社区主題） | ✅ 文章即筆記 | ✅ 內建（作者、RSS、標籤） |
| **文件版本化**（v1/v2 並存） | ❌ | ❌ | ✅ 招牌功能 |
| 多語言 i18n | ✅ 內建 | ✅ 內建 | ✅ 深度內建（CrowdIn 流程） |
| 站內搜尋 | ✅ 本機搜尋＋Algolia DocSearch | ✅ FlexSearch 全文 | ⚙️ 外掛（Local/Algolia/DocSearch） |
| 雙向連結／反鏈 | ❌ | ✅ wikilink、Backlinks、Popovers | ❌ |
| **連結圖譜視覺化** | ❌ | ✅ 全站圖譜 | ❌ |
| Obsidian 相容（`[[wikilink]]`、組件） | ❌ | ✅ Obsidian-flavored MD | ❌ |
| Mermaid／LaTeX | ⚙️ 生態（md 外掛） | ✅ 內建流水線 | ⚙️ 外掛 |
| MDX（JSX in Markdown） | ⚙️（Vue SFC 取代） | ❌（纯 MD 流水線） | ✅ 招牌 |
| OpenAPI／API 文件 | ⚙️ 社区方案 | ❌ | ⚙️ 外掛生態 |
| 主題自定義 | Vue 元件＋themeConfig | CSS 變數＋佈局層 | **JSON 主題設定＋swizzle**（免碰原始碼） |
| 外掛生態 | 小（Vue 生態補位） | 中（Quartz 插件管線） | **大**（官方＋社群外掛最多） |
| 部署 | 任意靜態託管 | GitHub Actions 一鍵 | 內建 deploy presets（GH Pages 等） |
| 全站 OG 圖／RSS | ⚙️ 外掛 | ✅ 內建 | ⚙️ 外掛 |
| 建置速度（大站感受） | 快（Vite 開發體驗極佳） | 最快級（v5 主打） | 中（功能多、冷啟動較重） |
| 學習曲線 | 低（會 Vue 就通） | 低（寫作導向，少寫設定） | 中（體系大、API 面廣） |

## 維護模式與生態訊號

* **VitePress** 掛在 vuejs 組織下，README 的贊助清單就是 Vite 生態全家福：VoidZero（Vite/Vitest/Rolldown/Oxc）、StackBlitz（線上 playground）、Algolia（DocSearch）、BrowserStack、Netlify。它的長期方向由 v2 alpha 主導—— Rolldown 化、更深的 Vite 整合。
* **Quartz** 是這三者中唯一的「個人專案」，靠讚助手維持，議題數（72）與節奏顯示維護極勤。它的設計哲學是**內容零建置負擔**：push 到 GitHub 就發站，功能是內建開關而非外掛市場。
* **Docusaurus** 由 Meta 出錢出人，README 明言「為了支撐 Meta 大量 OSS 專案而開源」；倉庫從 facebook 遷到 meta 組織也反映其歸屬。功能面它最「全套」：5 分鐘教學、`npm init docusaurus@latest` 一分鐘起站，docusaurus.new 瀏覽器秒開 playground。

## 適用場景

**選 VitePress，當…**
- 你的專案是 **Vue／Vite 系**，文件站要能直接嵌互動元件（示範 demo、playground）。
- 你要的是**精簡文件站**：侧欄＋搜尋＋深色模式＋i18n 全部內建，不想碰主題工程。
- 你享受 Vite 的開發體驗：改檔即時熱更新、配置寫在 `config.mts` 有型別提示。
- 例：元件庫文件、SDK 指南、個人技術部落格（配社区主題）。

**選 Quartz，當…**
- 你是**筆記重度使用者**（尤其 Obsidian），想把幾千則互相連結的筆記原樣發佈，連結關係不能斷。
- 你要的是**數位花園**：圖譜、反鏈、hover 預覽、全文搜尋——這些在另外兩個都是外掛也湊不齊的體驗。
- 你完全不想寫程式：改設定、丟 .md、git push，網站自己出現。
- 例：個人知識庫、研究筆記公開版、Zettelkasten 入口站。

**選 Docusaurus，當…**
- 你維護**有版本概念的產品文件**（v2 文件不能污染 v3 文件）——三家中獨有的版本化文件。
- 你要**多語言官方文件**且有人分工翻譯（CrowdIn 流程完整）。
- 你要**專案官網整套**：首頁＋文件＋部落格＋行銷頁＋MDX 互動区块，还要外掛生態（搜尋、PWA、表單、分析）。
- 例：開源庫官方文件（React Native、Supabase 等級的站點都是這系）、公司開發者入口。

## 常見誤區

1. **拿 Quartz 當文件站**：沒有版本化、沒有 sidebars 語意、搜尋是筆記向——它是知識網，不是產品文件。
2. **拿 VitePress 做多語言大型文件平台**：i18n 有，但翻譯流程、版本化、MDX 生態都薄；超過一定規模會開始自己造輪子。
3. **低估 Quartz 的定制度**：v5 是整條管線重寫，功能開關＋插件管線比 v4 彈性得多，「個人專案＝停滯」是錯覺。
4. **VitePress 用 v2 alpha 上生產**：alpha.21 仍會破壞 API，生產站點建議 v1.x，alpha 留給 Vite 生態追新者。
5. **Docusaurus 冷啟動慢＝專案沒落**：v3 的建置重量是「功能全內建」的代價；發佈節奏（v3.10.x 穩定推）與議題處理都很健康。

## 一句總結

> **文件要版本化、站點要成套 → Docusaurus；Vue 生態的精緻文件站 → VitePress；筆記的雙向連結要原樣上網 → Quartz。**

![Star history 三案對照](https://api.star-history.com/svg?repos=vuejs/vitepress,jackyzha0/quartz,meta/docusaurus&type=Date)

## 方法說明

星數、fork、授權、議題數、最新版本與 push 時間以 GitHub API 於 2026-11-16 驗證（VitePress 18,491／Quartz 13,596／Docusaurus 66,747）；功能矩陣整理自三案官方文件與 README（vitepress.dev、quartz.jzhao.xyz、docusaurus.io）；star-history 為即時熱鏈圖表。相關單案深度文章見 [Crucible](/crucible-agent-3d-engine/)、[Stela](/stela-macos-on-pc/)。
