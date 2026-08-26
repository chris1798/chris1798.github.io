---
title: "open-slide：专为 AI Agent 打造的幻灯片框架，用自然语言生成 React 投影片（7,000+ Star 分析）"
date: 2026-08-27
description: open-slide 是一款面向 AI Agent 的全新幻灯片框架（slide framework），基于 React 打造。它让你用自然语言描述简报内容，由编码 Agent 写出真正的 React 组件，框架负责画布缩放、导航、热重载与全屏演示。本文完整拆解其功能、架构与使用方式。
tags:
  - open-source
  - react
  - slides
  - ai-agent
  - typescript
  - dev-tool
cover: /assets/images/open-slide/cover.png
---

# open-slide：专为 AI Agent 打造的幻灯片框架

[![GitHub stars](https://img.shields.io/github/stars/1weiho/open-slide?style=for-the-badge)](https://github.com/1weiho/open-slide/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/1weiho/open-slide?style=for-the-badge)](https://github.com/1weiho/open-slide/network/members)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Vercel OSS](https://vercel.com/oss/program-badge-2026.svg)](https://vercel.com/open-source-program)

> **The slide framework built for agents.**
> 你的 Agent 写 React，open-slide 负责画布、缩放、导航、热重载与演示模式。

![open-slide 封面](/assets/images/open-slide/cover.png)

---

## 📊 项目速览

| 項目 | 資料 |
|------|------|
| **名稱** | open-slide |
| **授權** | MIT（© Yiwei Ho） |
| **Stars** | ⭐ 7,082（2026-08-27） |
| **Forks** | 498 |
| **開啟 Issue** | 90 |
| **開發語言** | TypeScript |
| **版本** | `@open-slide/core` v1.19.1 |
| **技術棧** | React 18 + Vite + Tailwind CSS + shadcn |
| **建立時間** | 2026-04-26（不到一年） |
| **Homepage** | [open-slide.dev](https://open-slide.dev) |
| **官方定位** | 全球首個為 AI 編碼 Agent 優化的投影片框架 |

---

## 🎯 核心概念：什麼是 open-slide？

### 一句話說明

> **把「用自然语言描述简报」→「Agent 写出真正可运行的 React 组件」→「框架负责渲染、缩放、导航与演示」**

一般投影片工具（PowerPoint、Google Slides）用的是**受限的 DSL**或視覺化編輯器。
open-slide 不同：每一頁都是一個**真正的 React 組件（Page component）**，你可以用全部 React + CSS 的能力自由發揮。

### 關鍵差異表

| 維度 | PowerPoint / Google Slides | open-slide |
|------|------|------|
| **本質** | 視覺化編輯器 | React 程式碼框架 |
| **每頁形式** | 專屬 DSL / 視覺物件 | `React.FC` 組件 |
| **畫布尺寸** | 可變 | 固定 **1920 × 1080**（全 HD） |
| **內容密度** | 有限 | 無限（可寫任何 React 程式碼） |
| **AI Agent 協作** | 支援度低 | **原生內建** |
| **部署** | 需匯出/上傳 | 靜態 HTML + 一鍵部署 |
| **客製化** | 受模板限制 | 完全自由 |

### 核心設計哲學

```
Slides are visual code. Agents are great at writing code.
```
> 投影片本質是「視覺化的程式碼」，而 AI Agent 最擅長寫程式碼。
> open-slide 就是那個把「做關於 X 的投影片」變成精美、可簡報的簡報的**缺失執行環境**。

---

## ✨ 四大亮點功能

### 🤖 1. Agent-native 作者工具（Agent 原生撰寫）

open-slide 與**所有編碼 Agent** 相容（Claude Code、Codex、Cursor、OpenCode 等）。
Scaffolder 內建了兩個核心 skills：

| Skill | 功能 |
|-------|------|
| **`/create-slide`** | 從頭到尾草擬一整套簡報。會問四個問題：① 主題與美學、② 頁數、③ 文字密度、④ 動態 vs 靜態。自動選擇 id、規劃結構、寫出頁面 |
| **`/slide-authoring`** | 技術參考文件。涵蓋 1920 × 1080 畫布、字體比例、配色、佈局規則。**Agent 在寫程式前會先讀它** |

```tsx
import type { Page } from '@open-slide/core';

// 每一頁都是一個 React 組件，預設匯出一個 Page 陣列
const Cover: Page = () => (
  <div className="flex h-full w-full items-center justify-center">
    <h1 className="text-[120px] font-bold">Hello, open-slide</h1>
  </div>
);

const pages: Page[] = [Cover];
export default pages;

export const meta = { title: 'Hello' };
```

### 🎯 2. 瀏覽器內 Inspector（互動式評審）

在 dev server 中**點擊任何元素**即可附上評論：

> *"make this red"*（改成紅色）
> *"change to 'Open Slide Rocks'"*（改文字）
> *"shrink the headline"*（縮小標題）

- 評論會持久化存成 `@slide-comment` 標記（source code 中）
- 執行 `/apply-comments`，Agent 就會套用所有待處理的編輯並清除標記

```
Loop：present → click to comment → /apply-comments → repeat
```

### 🖼️ 3. Assets Manager + svgl Logo 搜尋

| 功能 | 說明 |
|------|------|
| **資產管理面板** | 每場簡報的圖片、影片、字型都在一個面板中管理 |
| **svgl Logo 目錄** | 內建整合 [svgl.app](https://svgl.app/)，搜尋並拖放任何品牌 Logo（SVG 格式） |
| **免找檔案** | 不用再滿世界找 SVG 圖示 |

### 🎬 4. 專業演示模式（Present Mode）

- **全螢幕播放** + 鍵盤導航
- **講者模式（Presenter mode）**：
  - 目前/下一頁預覽
  - 講者備忘錄（Speaker notes）
  - 計時器（Timer）
- 為**真實演講舞台**設計，不只是瀏覽器分頁

### 📦 5. 匯出靜態 HTML 與 PDF

- 一行指令即可匯出：
  - **自包含的靜態 HTML 網站**（含所有資源）
  - **適合列印的 PDF**
- 可離線分享，**不需要伺服器**

### 📁 6. 簡報管理器（Slide Manager）

- 把簡報分組到資料夾
- 支援自訂 emoji 與拖曳重新排序
- 當簡報超過三套時，用來快速找到需要的檔案

### 🚀 7. 部署友善（Deploy-friendly）

- 輸出純靜態 build
- **一鍵部署**到：Vercel、Cloudflare Pages、Zeabur、Netlify，或任何靜態主機
- **不需要伺服器、不需要 runtime、沒有鎖定**

---

## 🏗️ 技術架構

### Repo 結構：pnpm + Turbo 單倉（Monorepo）

| 路徑 | 套件 | 角色 |
|------|------|------|
| **`packages/core`** | `@open-slide/core` | 核心執行環境（首頁、投影片檢視器、演示模式、Inspector）、Vite plugin、`open-slide` dev/build/preview CLI |
| **`packages/cli`** | `@open-slide/cli` | `npx @open-slide/cli init` 建立器 + 專案模板 |
| **`apps/demo`** | private | 範本工作區，用 `workspace:*` 消耗 `@open-slide/core`。用於本地開發框架 |
| **`apps/web`** | private | 行銷網站（Next.js） |

### 關鍵技術選型

| 技術 | 用途 |
|------|------|
| **React 18** | 投影片組件基礎 |
| **Vite 5.4** | 快速建構與 dev server |
| **Tailwind CSS 4.2** | 樣式系統 |
| **shadcn** | UI 元件庫 |
| **TypeScript 5.9** | 類型安全 |
| **Biome** | 程式碼格式化與 Lint |
| **Changeset** | 版本管理 |
| **Playwright** | E2E 測試 |
| **tsdown** | 套件打包 |

---

## 🛠️ 安裝與使用

### 快速開始

```bash
# 1. 建立新的投影片工作區
npx @open-slide/cli init my-slide

# 2. 進入目錄
cd my-slide

# 3. 安裝依賴並啟動 dev
pnpm install
pnpm dev
```

### 三個核心 CLI 指令

| 指令 | 功能 |
|------|------|
| **`open-slide dev`** | 啟動 dev server |
| **`open-slide build`** | 建立靜態網站 |
| **`open-slide preview`** | 預覽生產 build |

### 設定檔 `open-slide.config.ts`

所有選填欄位：

```ts
import type { OpenSlideConfig } from '@open-slide/core';

const openSlideConfig: OpenSlideConfig = {
  slidesDir: 'slides',   // 投影片目錄
  port: 5173,            // dev server 連接埠
};

export default openSlideConfig;
```

### 部署到子路徑（Subpath）

可用 `base` 欄位部署到子目錄（內網資料夾、GitHub Pages 專案網站、反向代理）：

```ts
const openSlideConfig: OpenSlideConfig = {
  base: '/my-slides/',   // 前後都要有斜線
};
```

### 內建導出的模組（Exports）

```ts
import {
  CANVAS_WIDTH,        // 1920
  CANVAS_HEIGHT,       // 1080
  MorphElement,        // 跨頁淡入淡出的元素過渡
  type Page,
  type SlideMeta,
  type SlideModule,
  type SlideTransition,
  type OpenSlideConfig,
} from '@open-slide/core';
```

---

## 📝 投影片撰寫規則

投影片放在 `slides/<kebab-case-id>/index.tsx`，預設匯出一個 `Page` 陣列：

```tsx
// slides/hello/index.tsx
import type { Page } from '@open-slide/core';

const Title: Page = () => (
  <div className="flex h-full w-full items-center justify-center">
    <h1 className="text-[120px] font-bold text-blue-600">
      我的投影片
    </h1>
  </div>
);

const Content: Page = () => (
  <div className="p-20">
    <h2 className="text-[80px] font-bold">核心內容</h2>
    <ul className="text-[60px] space-y-4">
      <li>✓ 功能一</li>
      <li>✓ 功能二</li>
    </ul>
  </div>
);

const pages: Page[] = [Title, Content];
export default pages;
```

### 三種撰寫方式

| 方式 | 說明 |
|------|------|
| **方式 1：純寫程式** | 直接編輯 `slides/<id>/index.tsx`，完全掌控 |
| **方式 2：AI Agent 協助** | 用 `/create-slide` 讓 Agent 從頭到尾寫好 |
| **方式 3：混合模式** | Agent 起草 → Inspector 點選微調 → `/apply-comments` 套用 |

---

## 🔑 核心概念比較表

| 概念 | 說明 |
|------|------|
| **Page** | 一頁投影片的 React 組件 |
| **SlideModule** | 整個投影片模組（含 pages + meta） |
| **SlideMeta** | 簡報的中繼資料（標題、作者等） |
| **SlideTransition** | 跨頁過渡效果 |
| **MorphElement** | 跨頁元素淡入淡出的過渡元件 |
| **@slide-comment** | Inspector 評論的持久化標記 |
| **open-slide.config.ts** | 專案設定檔（slidesDir、port、base） |

---

## 💰 授權與支持

| 項目 | 說明 |
|------|------|
| **授權** | MIT — 可自由使用、修改、商業化 |
| **作者** | Yiwei Ho（[@1weiho](https://github.com/1weiho)） |
| **支持** | [ko-fi.com/D1D11YPUP1](https://ko-fi.com/D1D11YPUP1) |
| **Vercel OSS** | 被收錄於 Vercel OSS 計畫 |

---

## 📈 為什麼值得關注？

1. **開創性定位**：全球首個專為 AI 編碼 Agent 優化的投影片框架
2. **降低門檻**：一句話提示 → 精美簡報，不需學複雜工具
3. **高度客製化**：真正的 React 程式碼，不受 DSL 限制
4. **部署簡潔**：靜態 HTML + 一鍵部署
5. **團隊協作**：Inspector + apply-comments 流程適合團隊迭代
6. **技術現代**：React 18 + Vite + Tailwind + TS，生態完整

---

## 🚀 適合誰使用？

| 使用者 | 適用原因 |
|--------|---------|
| **AI 應用開發者** | 快速生成技術簡報、產品演示 |
| **團隊** | Inspector + apply-comments 協作流程 |
| **教育訓練** | 自然語言即可生成教學投影片 |
| **行銷團隊** | 快速產出行銷簡報並一鍵部署 |
| **設計團隊** | 真正 React 程式碼，無限客製化 |

---

## 總結

open-slide 是一個**為 AI Agent 時代而生**的投影片框架：

```
自然語言提示 → AI Agent 寫 React → 框架負責渲染與演示
```

它打破了傳統投影片工具的 DSL 限制，讓每一頁都是**真正可運行的 React 組件**。
配合內建的 `/create-slide`、`/apply-comments`、Inspector、Assets Manager、演示模式與一鍵部署，
讓「做投影片」變成**純屬內容創作**的體驗。

對於已經在使用 Claude Code、Codex、Cursor 的開發者來說，open-slide 是**必試的工具**。

---

*本文於 2026-08-27 整理自 [github.com/1weiho/open-slide](https://github.com/1weiho/open-slide)*
