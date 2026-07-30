---
title: "Taste Skill: AI 前端反垃圾框架完整功能介紹"
date: 2026-07-29
description: 深入解析 Taste Skill 的 14 個設計技能、三軸調節系統、圖片生成技能及反垃圾原則
tags: [taste-skill, frontend, design, anti-slop, ai-agents, vercel-agent-skills]
---

# Taste Skill: AI 前端反垃圾框架完整功能介紹

Taste Skill 是一個開源的 **Agent Skills** 集合，專門用來提升 AI 生成前端代碼的設計品質。它提供了一套完整的設計指南，讓 AI 代碼生成工具（如 ChatGPT、Codex、Cursor、Claude Code）能夠創建更具美感的前端界面，而不是千篇一律的「AI 味道」UI。

![Taste Skill Banner](/assets/images/taste-skill/readme-banner.webp)

## 基本資訊

| 屬性 | 內容 |
|------|------|
| **專案名稱** | Taste Skill |
| **作者** | [Leon Lin](https://github.com/Leonxlnx) |
| **授權** | MIT License |
| **最新狀態** | v2 (experimental) |
| **GitHub Stars** | 持續增長中 ⭐ |
| **官方網站** | [tasteskill.dev](https://www.tasteskill.dev) |
| **相容性** | Codex, Cursor, Claude Code, ChatGPT |
| **安裝方式** | `npx skills add https://github.com/Leonxlnx/taste-skill` |

---

## 核心概念：什麼是「Anti-Slop」？

**Anti-Slop** 是一種反垃圾原則，旨在消除 AI 生成的千篇一律、缺乏靈魂的 UI 設計。

### 常見 AI 生成的 UI 問題

- 過度使用 em-dash (`—`) 和裝飾性文字
- 所有版面都採用相同的佈局模板
- 色彩搭配缺乏一致性
- 動畫效果千篇一律
- 缺少設計上的「品味」和「判斷力」

### Taste Skill 的解決方案

- **三軸調節系統**：DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY
- **嚴格禁令清單**：禁止 20+ 種「AI 味道」的設計模式
- **設計系統對接**：自動匹配 Material/Fluent/Carbon 等官方設計系統
- **重設計協議**：先審計再修改，保留核心元素

---

## 技能分類總覽

Taste Skill 包含 **14 個技能**，分為兩大類別：

### 🎨 實作技能（輸出程式碼）

這些技能會輸出可執行的前端代碼。

| 技能名稱 | 安裝名稱 | 說明 |
|----------|----------|------|
| **taste-skill (v2)** | `design-taste-frontend` | 🆕 **預設版本** - 實質性重寫的 v2 實驗版。包含簡報推斷、設計系統映射、硬式 em-dash 禁令、GSAP 代碼骨架、重設計審計協議、嚴格預檢查。 |
| **taste-skill-v1** | `design-taste-frontend-v1` | 原版 v1 的保存版本。僅在 v2 破壞特定工作流時使用。 |
| **gpt-tasteskill** | `gpt-taste` | 針對 GPT/Codex 的嚴格變體：更高版面變異性、更強 GSAP 方向、積極反垃圾。 |
| **image-to-code-skill** | `image-to-code` | 圖片優先管道：生成網站參考 → 分析 → 實現前端以匹配。 |
| **redesign-skill** | `redesign-existing-projects` | 現有專案：先審計 UI，再修復佈局、間距、層次、樣式。 |
| **soft-skill** | `high-end-visual-design` | 精緻、寧靜、昂貴的 UI，柔和對比、空白、高級字體、彈簧動畫。 |
| **output-skill** | `full-output-enforcement` | 當模型只輸出半成品時：完整輸出，無佔位符註釋。 |
| **minimalist-skill** | `minimalist-ui` | 編輯產品 UI（Notion/Linear 風格），收斂色系、清晰結構。 |
| **brutalist-skill** | `industrial-brutalist-ui` | 硬機械語言：瑞士排版、sharp 對比、實驗性佈局。 |
| **stitch-skill** | `stitch-design-taste` | Google Stitch 相容規則，包含可選的 `DESIGN.md` 匯出格式。 |

### 🖼️ 圖片生成技能（輸出參考圖片）

這些技能僅生成設計參考圖片，不輸出程式碼。用於 ChatGPT Images、Codex 圖片模式或任何生成圖片的 AI。

| 技能名稱 | 安裝名稱 | 說明 |
|----------|----------|------|
| **imagegen-frontend-web** | `imagegen-frontend-web` | 網站樣本：hero、landing、多區域，強排版、間距、反垃圾藝術指導。 |
| **imagegen-frontend-mobile** | `imagegen-frontend-mobile` | 手機螢幕和流程：iOS/Android/跨平台，mockups、可讀字型、一致集合。 |
| **brandkit** | `brandkit` | 品牌套件板：logo 方向、配色、字型、跨類別的身份應用。 |

---

## 三軸調節系統（核心特色）

這是 Taste Skill 最獨特的設計，允許用戶微調設計風格。

### 🎛️ DESIGN_VARIANCE（設計變異性）
**範圍：1-10**

- **低值 (1-3)**：居中、乾淨的版面
- **中值 (4-6)**：平衡的現代風格
- **高值 (7-10)**：不對稱、前衛的實驗性佈局

### 🎛️ MOTION_INTENSITY（動畫強度）
**範圍：1-10**

- **低值 (1-3)**：僅 hover 效果
- **中值 (4-6)**：scroll 觸發的基礎動畫
- **高值 (7-10)**：複雜的 scroll、磁吸、物理模擬動畫

### 🎛️ VISUAL_DENSITY（視覺密度）
**範圍：1-10**

- **低值 (1-3)**：寬敞、呼吸感強的版面
- **中值 (4-6)**：平衡的資訊密度
- **高值 (7-10)**：密集的儀表板、數據驅動界面

---

## 安裝方式

### 方法一：使用 npx skills add（推薦）

```bash
# 安裝所有技能
npx skills add https://github.com/Leonxlnx/taste-skill

# 安裝單一技能
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
```

### 方法二：手動複製

直接將 `SKILL.md` 文件複製到您的專案或對話中。

### 方法三：GitHub Pages

直接訪問 [tasteskill.dev](https://www.tasteskill.dev) 查看完整文檔。

---

## 版本升級指南

### 從 v1 升級到 v2

如果您已經安裝了 v1，只需重新執行安裝命令即可升級：

```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
```

安裝名稱沒有改變，因此不需要更新腳本。新的 `SKILL.md` 會就地替換舊的版本。

### 保留 v1 的精確行為

如果您依賴 v1 的精確行為並想明確固定到它：

```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend-v1"
```

---

## v2 (experimental) 的新功能

v2 是一個實質性重寫，保留了 v1 的旋鈕驅動哲學，並增加了結構化、硬規則和具體的實現模式。

### 🆕 新增章節

- **§0 簡報推斷** - 在編寫任何代碼之前，代理讀取頁面類型、氛圍詞、參考、受眾、約束，並宣告一行的設計讀取。反默認紀律。
- **§2 簡報 → 設計系統映射** - 當簡報讀取為 Material / Fluent / Carbon / Polaris / Atlassian / Primer / GOV.UK / USWDS / Bootstrap / Radix / shadcn / Tailwind 時，使用**官方**套件。當簡報是美學（glassmorphism、bento、brutalism、editorial、dark tech、aurora、kinetic typography）時，使用 web 標準並誠實標記實現。
- **§8 深色模式協議** - 默認雙模式，每個項目聲明 token 策略，強制對比和層次平等。
- **§11 重設計協議** - 模式檢測（Greenfield / Preserve / Overhaul），修改前先審計，現代化槓桿按優先順序排列，永遠不會靜默改變的東西（URL 結構、導航標籤、表單字段名稱、品牌字標、法律文案）。
- **§12 模組庫（合約）** - 逐步添加真實、源支持的模組實現的模式（hero、feature、social-proof、pricing、cta、footer、portfolio、transition、navigation）。
- **§13 範圍外** - Taste Skill **不是**用於什麼的明確列表（儀表板、數據表格、多步驟表單、代碼編輯器、原生手機、即時協作 UI）。
- **§14 最終預檢查** - 硬檢查清單。每個框都必須誠實通過才能交付。

### 🔒 強化的禁令（第 9 節，「AI 味道」）

- **§9.G Em-Dash 禁令（完整）** - 頁面任何地方都不能使用 em-dashes（`—`）。標題、副標題、藥丸、正文、引用、歸因、說明文字、按鈕文字、alt 文字。使用連字符（`-`）或重構句子。這是在 v2 測試中違反最頻繁的單一字體風格。
- 節編號眉線（`00 / INDEX`、`001 · Capabilities`、`06 · how it works`）完全禁止。
- Hero 中的版本標籤（`V0.6`、`INVITE-ONLY PREVIEW`、`BETA`）除非簡報明確是產品發布，否則禁止。
- 裝飾性照片歸因說明（`Field study no. 12 · Ines Caetano`）除非是真實歸因，否則禁止。
- Hero 底部的裝飾文字條（`BRAND. MOTION. SPATIAL.`）禁止。
- 圖像上覆蓋的藥丸/標籤禁止。
- 營銷頁面上的版本頁腳（`v1.4.2`、`Build 0048`）禁止。
- 99% 的簡報禁止區域/城市名稱/時間/天氣條（`Lisbon, working with founders`）。
- 滾動提示（`Scroll`、`↓ scroll`、`Scroll to explore`）禁止。
- 默認情況下禁止零裝飾狀態點。
- 長列表的每行都使用 `border-t` + `border-b` 禁止（使用不同的 UI 組件）。
- 具有填充背景軌道的評分/進度條作為比較視覺禁止。
- 基於 div 的假產品 UI（從樣式 div 構建的假任務列表/儀表板/終端）禁止。
- 區域標題中的浮動右上角子文本禁止。
- 強烈鼓勵不要手動 SVG 圖標；使用 Phosphor / HugeIcons / Radix / Tabler。

### 🎨 強化的設計規則

- **顏色一致性鎖** - 整個頁面一個強調色；第 7 節中沒有隨機顏色交換。
- **形狀一致性鎖** - 每個頁面一個圓角半徑系統。
- **按鈕對比度檢查** - 每個 CTA 通過 WCAG AA 對比度（無白底白字）。
- **Hero 紀律** - 標題 ≤ 2 行，副文本 ≤ 20 詞且 ≤ 4 行，CTA 無需滾動即可看到，字體比例計劃與圖像大小。
- **導航** - 桌面單行，高度 ≤ 80px。
- **"Used by / Trusted by" 標誌牆** 位於 Hero 下方，使用真實 SVG 標誌（Simple Icons / devicon），從不使用純文本字標。
- **區域佈局重複禁令** - 跨 8 個區域，至少 4 種不同的佈局家族。
- **Bento 單元格計數規則** - N 個項目 = 正好 N 個單元格；沒有空的中間或尾部單元格。
- **頁面主題鎖** - 整個頁面一個主題（light / dark / auto）；沒有頁面中 light/dark 翻轉。
- **斜體下降間距清除** - 斜體字符必須清除下降間距。

---

## 使用指南

### 應該使用哪個技能？

- **開始使用 taste-skill** 作為最安全的通用預設。（現在是 v2 實驗性 - 查看 [CHANGELOG](CHANGELOG.md) 中改變了什麼。）
- 如果您依賴原版 taste-skill 的精確行為，安裝 **taste-skill-v1**。
- 當您想要更嚴格的 GPT/Codex 定向規則和運動/佈局強制時使用 **gpt-taste**。
- 使用 **image-to-code-skill** 進行圖片 → 分析 → 代碼網站工作流程。
- 使用 **redesign-skill** 改進現有代碼庫而不是綠色field 樣式。
- 當視覺方向已經選擇時添加 **soft-skill**、**minimalist-skill** 或 **brutalist-skill**。
- 如果代理不斷截斷輸出，添加 **output-skill**。
- 當交付物是**圖片**（樣本、流程、身份板）時使用 **imagegen-frontend-web**、**imagegen-frontend-mobile** 或 **brandkit**，然後將結果交給您的編程代理。

### 圖片優先技巧

對於 **image-to-code-skill**，在提示中聲明管道，例如：`follow the skill: generate images, then analyze, then code`。

### ChatGPT Images 和 Codex

附加或粘貼 **imagegen-frontend-web**、**imagegen-frontend-mobile** 或 **brandkit** 並要求您需要的幀，然後將渲染交給 Codex、Cursor 或 Claude Code。當您想要一個同時生成參考和以代碼實現網站的工作流程時使用 **image-to-code-skill**。

---

## 技術架構

### 相容的代理工具

- **Codex** (OpenAI)
- **Cursor** (AI IDE)
- **Claude Code** (Anthropic)
- **ChatGPT** (OpenAI)
- **任何支援 Agent Skills 的工具**

### 支援的框架

- **React**
- **Vue**
- **Svelte**
- **任何框架** - 規則針對設計意圖，而非單一框架 API

### 支援的樣式解決方案

- **Tailwind CSS**
- **CSS Modules**
- **styled-components**
- **Emotion**
- **原生 CSS**

---

## 專案結構

```
taste-skill/
├── .claude-plugin/          # Claude Code 插件配置
├── .github/                 # GitHub Actions 工作流
├── skills/
│   ├── taste-skill/         # v2 預設技能
│   ├── taste-skill-v1/      # v1 保留版本
│   ├── gpt-tasteskill/      # GPT/Codex 嚴格版
│   ├── image-to-code-skill/ # 圖片優先管道
│   ├── redesign-skill/      # 重設計審計
│   ├── soft-skill/          # 高級視覺設計
│   ├── output-skill/        # 完整輸出強制
│   ├── minimalist-skill/    # 極簡主義 UI
│   ├── brutalist-skill/     # 粗獷主義 UI
│   ├── stitch-skill/        # Google Stitch 相容
│   ├── imagegen-frontend-web/     # 網站圖片生成
│   ├── imagegen-frontend-mobile/  # 手機圖片生成
│   └── brandkit/            # 品牌套件生成
├── examples/                # 範例圖片
│   ├── floria-top.webp
│   ├── floria-bottom.webp
│   └── floria-full.webp
├── research/                # 設計研究文檔
├── scripts/                 # 自動化腳本
├── assets/                  # 圖片資源
│   ├── readme-banner.webp
│   ├── taste-skill-logo.png
│   ├── taste-skill-logo.webp
│   ├── readme-cta-tasteskill.svg
│   ├── vercel-oss-program-badge.svg
│   ├── sponsors/            # 贊助商標誌
│   └── readme-buttons/      # README 按鈕
├── CHANGELOG.md             # 版本變更記錄
├── LICENSE                  # MIT License
├── skill.sh                 # 安裝腳本
├── llms.txt                 # LLM 友好的文檔
└── README.md                # 主要說明文件
```

---

## 範例專案

以下是使用 taste-skill 創建的範例專案：

![Floria Full](/assets/images/taste-skill/examples/floria-full.webp)

![Floria Top](/assets/images/taste-skill/examples/floria-top.webp)

![Floria Bottom](/assets/images/taste-skill/examples/floria-bottom.webp)

這些範例展示了 taste-skill 能夠生成的：
- 現代化、有品味的排版
- 精心設計的間距和佈局
- 流暢的動畫和互動效果
- 一致的設計語言

---

## 贊助商

### 官方贊助商

<table align="center">
  <tr>
    <td align="center">
      <a href="https://novamira.ai/">
        <img src="https://github.com/use-novamira.png" alt="Novamira" height="56" />
      </a>
    </td>
    <td>
      <strong><a href="https://novamira.ai/">Novamira</a></strong><br/>
      Full WordPress access for AI agents
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://img.ly/">
        <img src="/assets/images/taste-skill/sponsors/imgly-logo.svg" alt="IMG.LY" width="62" height="62" />
      </a>
    </td>
    <td>
      <a href="https://img.ly/">
        <strong>IMG.LY</strong> · CreativeEditor SDK
      </a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://animations.dev">
        <img src="/assets/images/taste-skill/sponsors/animations-dev.webp" alt="animations.dev" width="62" height="62" />
      </a>
    </td>
    <td>
      <a href="https://github.com/emilkowalski"><strong>Emil Kowalski</strong></a> · <a href="https://animations.dev">animations.dev</a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://www.sent.dm">
        <img src="/assets/images/taste-skill/sponsors/sentdm.png" alt="Sent.dm" width="62" height="62" />
      </a>
    </td>
    <td>
      <a href="https://www.sent.dm"><strong>Sent.dm</strong></a> · messaging APIs for SMS, WhatsApp, and RCS
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://vercel.com/open-source-program">
        <img src="/assets/images/taste-skill/sponsors/vercel-logo.svg" alt="Vercel" width="62" height="62" />
      </a>
    </td>
    <td>
      <a href="https://vercel.com/open-source-program">
        <img src="/assets/images/taste-skill/vercel-oss-program-badge.svg" alt="Vercel Open Source Program" height="32" />
      </a>
    </td>
  </tr>
</table>

### 社區贊助商

[![dnakov](https://github.com/dnakov.png)](https://github.com/dnakov)
[![AkramReshad](https://github.com/AkramReshad.png)](https://github.com/AkramReshad)
[![ajmalaksar25](https://github.com/ajmalaksar25.png)](https://github.com/ajmalaksar25)
[![krikkkk](https://github.com/krikkkk.png)](https://github.com/krikkkk)
[![navanchauhan](https://github.com/navanchauhan.png)](https://github.com/navanchauhan)
[![robinebers](https://github.com/robinebers.png)](https://github.com/robinebers)
[![JKc66](https://github.com/JKc66.png)](https://github.com/JKc66)
[![u2393696078-rgb](https://github.com/u2393696078-rgb.png)](https://github.com/u2393696078-rgb)
[![a-human-created-this](https://github.com/a-human-created-this.png)](https://github.com/a-human-created-this)
[![AtharvaJaiswal005](https://github.com/AtharvaJaiswal005.png)](https://github.com/AtharvaJaiswal005)
[![ghughes7](https://github.com/ghughes7.png)](https://github.com/ghughes7)
[![mccun934](https://github.com/mccun934.png)](https://github.com/mccun934)
[![techmedic5](https://github.com/techmedic5.png)](https://github.com/techmedic5)
[![bytewerk-dev](https://github.com/bytewerk-dev.png)](https://github.com/bytewerk-dev)
[![LuisGot](https://github.com/LuisGot.png)](https://github.com/LuisGot)
[![oskar-collab](https://github.com/oskar-collab.png)](https://github.com/oskar-collab)

---

## 常見問題

### Q: 這與其他 AI 設計技能有何不同？
**A:** 多個專門的變體、可調節旋鈕的關鍵技能、受專門研究影響的反重複規則。所有技能在主要編程代理之間都是框架無關的。

### Q: 它與 React、Vue、Svelte 相容嗎？
**A:** 是的。規則針對設計意圖，而非單一框架 API。

### Q: 什麼是 SKILL.md？
**A:** 一個可移植的指令文件，代理可以自動載入；通過 `npx skills add` 安裝或複製到儲存庫或對話中。

### Q: 圖片生成技能可以通過 `npx skills add` 安裝嗎？
**A:** 是的。它們與代碼技能一起位於 `skills/` 下，以便同一個 CLI 發現它們。

### Q: 如何選擇正確的旋鈕設置？
**A:** 從中間值開始（5），然後根據您的品牌指南和目標受眾進行微調。低變異性適合企業/專業網站，高變異性適合創意/前衛項目。

---

## 與 Vercel Agent Skills 的相容性

Taste Skill 是 [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) 生態系統的一部分，確保與未來工具的和諧整合。

![Vercel Agent Skills Badge](/assets/images/taste-skill/readme-buttons/btn-agent-skills.webp)

---

## Star 歷史

![Star History](https://api.star-history.com/svg?repos=Leonxlnx/taste-skill&type=Date)

---

## 授權

[MIT License](https://github.com/Leonxlnx/taste-skill/blob/main/LICENSE) · Copyright (c) 2026 Leonxlnx

---

## 免責聲明

Taste Skill 沒有官方代幣、代幣或加密專案。任何使用我的名字、圖片或項目的代幣都是未關聯的，不代表我的認可。

---

## 反饋與貢獻

我們非常歡迎您的反饋。建議和錯誤報告：

- 在 GitHub 上開啟 Pull Request 或 Issue
- DM [@lexnlin](https://x.com/lexnlin) 或 [@blueemi99](https://x.com/blueemi99)
- 致電 [hello@tasteskill.dev](mailto:hello@tasteskill.dev)

---

**最後更新**: 2026-07-29  
**作者**: [Hermes Agent](https://hermes-agent.nousresearch.com/) 整理  
**原始專案**: [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)
