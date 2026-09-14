---
title: "ai-stock-report-generator：一鍵把台股代號轉成 Excel 財務模型 + PPTX 投資簡報的 Agent Skill"
date: 2026-09-14
description: ai-stock-report-generator（yangchunyi0814）是一個 Claude / Codex Agent Skill，輸入台股代號即可自動搜尋財務資料、建立 Excel 財務模型、產出 K 線圖表、並生成 PPTX 投資分析簡報。
tags:
  - open-source
  - stock
  - finance
  - agent-skill
  - claude
  - codex
  - taiwan
---

# ai-stock-report-generator：台股財務模型 + 投資簡報生成器

> **輸入一個台股代號，輸出完整的 Excel 財務模型 + PPTX 投資簡報 + K 線圖表。**

---

## 📊 專案速覽

| 項目 | 資料 |
|------|------|
| **名稱** | ai-stock-report-generator |
| **作者** | yangchunyi0814 |
| **Stars** | ⭐ 28 |
| **Forks** | 12 |
| **建立時間** | 2026-07-05 |
| **類型** | Claude Code / Codex Agent Skill |
| **用途** | 台股財務模型 + 投資簡報自動生成 |

---

## 🎯 這個 Skill 會做什麼？

輸入一個台股代號（如 `2303`、`6116`、`0050`），Skill 會驅動 Claude / Codex 執行：

```text
代號 → ①資料蒐集 → ②Excel財務模型 → ③K線型態圖 → ④PPTX投資簡報 → ⑤交付
```

### 使用方式

**Codex：**
```text
2303 //ai-stock-report-generator
```

**Claude Code：**
```text
使用 ai-stock-report-generator，幫我產出 2303 的財務模型與投資簡報
```

或用自然語言：
```text
幫我做 6116 的估值和簡報
建立 2330 財務模型
model up 6116
```

---

## 📦 輸出檔案

Skill 會產生以下檔案：

```text
{代號}_{名稱}_財務模型.xlsx
{代號}_{名稱}_投資分析簡報.pptx
{代號}_{名稱}_K線型態圖表.html
{代號}_{名稱}_K線型態圖表.png
```

### Excel 財務模型（至少 8 工作表）

| 工作表 | 內容 |
|--------|------|
| **總覽** | Dashboard：市場快照、基準情境摘要、核心觀點 |
| **假設** | 基礎輸入 + 三情境（保守/基準/樂觀）成長率與利益率 + 估值假設 |
| **歷史財務** | 年度損益、季度 EPS、最新季損益摘要、月營收 |
| **預測** | 三情境 2026E-2028E：營收→營業利益→業外→稅前→稅後→EPS |
| **估值** | P/B、P/S、DCF 簡化估值、相對估值、情境目標價、敏感度表 |
| **技術指標** | 近期日線、MA5/10/20、BB(20,2)、KD、MACD、成交量 |
| **風險分析** | 風險矩陣：機率×衝擊(1-5分)、附觀察指標 |
| **來源** | 所有資料來源 URL |

### PPTX 投資簡報（至少 14 頁）

1. **封面** — 代號、公司名、五大主題、資料截止日
2. **公司概況** — 基本資料、股價/市值/PB/營收
3. **歷史財務** — 年度營收 BAR + 年度 EPS BAR
4. **最新營運動能** — 季度 EPS BAR + 月營收 LINE
5. **成長動能** — 3 張主題卡片
6. **成長預測儀表板** — Bull/Base/Bear、Revenue/EBITDA/EBIT/Net Income/EPS/FCF
7. **三情境預測表** — 基準列淺藍底、轉正 EPS 綠字
8. **DCF + 相對估值分析** — DCF 估值 + 相對估值並列
9. **估值分析** — 情境目標價
10. **財務指標健檢**
11. **KD / MACD 技術面**
12. **K 線型態圖表**
13. **風險矩陣**
14. **結論**

---

## ⚙️ 技術規格

### 資料蒐集（3-5 次搜尋）

Skill 會即時搜尋（不依賴訓練記憶）：

1. `{代號} {公司名} 全年財報 EPS 營收` — 近三年年度營收、EPS
2. `{公司名} {代號} 股價 今日 每股淨值` — 最新收盤價、股淨比
3. `{公司名} {代號} 股價 大漲/展望 產業` — 題材、成長動能
4. （選配）`{代號} 財報分析 季度` — 最新季度損益細節

### 技術指標計算

- MA5、MA10、MA20
- Bollinger Bands (20,2)：中軌、上軌、下軌
- KD：RSV(9)、K(9,3)、D(9,3)
- MACD：EMA12、EMA26、DIF、MACD/Signal(9)、柱狀體
- 至少 60 個交易日數據

### K 線型態標記（規則式偵測）

- 布林通道突破或跌破
- 局部高點 / 局部低點
- 跳空缺口
- 十字線或長影線
- 均線黃金交叉 / 死亡交叉

> 若為規則式偵測，必須標註「型態標記為規則式偵測，適合教學與快速觀察，不等同投資建議」。

### 台股色彩規範

```text
紅色 = 上漲 / 正值 / 偏多
綠色 = 下跌 / 負值 / 偏空
```

> K 線實體、影線、成交量柱必須紅漲綠跌；MACD 柱狀體正柱紅色、負柱綠色。不得使用美股常見的綠漲紅跌。

---

## 🎨 Excel 色碼規範

| 顏色 | 用途 |
|------|------|
| **藍字 `0000FF`** | 輸入值 |
| **黑字** | 公式計算結果 |
| **綠字 `008000`** | 跨表連結 |
| **黃底** | 關鍵假設 |

**硬性要求：**
- 所有計算用 Excel 公式，禁止 Python 算好硬編碼
- 存檔後必跑 `recalc.py` 驗證，必須 `total_errors: 0`
- 每個硬編碼數字都要在備註欄標注來源與日期

### PPTX 設計規範

- Layout：16x9
- 字型：`Microsoft JhengHei`
- 配色：Midnight Executive（navy `1E2761` / ice `CADCFC` / gold `C9A227`）
- 深色封面與結論夾淺色內容頁

---

## 📝 設計原則

1. **分析與教學輔助**，不是自動投資建議
2. 必須標示資料來源
3. 不得把估值結果包裝成保證
4. 不得只用文字回覆，必須產出檔案
5. 假設要可調整
6. Excel 公式錯誤要檢查
7. 技術指標只作短線位置補充，不取代基本面估值
8. K 線型態若為規則式偵測，必須明確標註
9. 台股圖表必須使用台灣慣例色彩

---

## 🛠️ 安裝方式

### Codex（Windows PowerShell）

```powershell
$skillRoot = "$env:USERPROFILE\.codex\skills\ai-stock-report-generator"
New-Item -ItemType Directory -Force $skillRoot
Copy-Item .\skills\ai-stock-report-generator\SKILL.md "$skillRoot\SKILL.md" -Force
```

### Codex（macOS/Linux）

```bash
mkdir -p ~/.codex/skills/ai-stock-report-generator
cp skills/ai-stock-report-generator/SKILL.md ~/.codex/skills/ai-stock-report-generator/SKILL.md
```

### Claude Code（專案層級）

```bash
mkdir -p .claude/skills/ai-stock-report-generator
cp skills/ai-stock-report-generator/SKILL.md .claude/skills/ai-stock-report-generator/SKILL.md
```

### Claude Code（使用者層級）

```bash
mkdir -p ~/.claude/skills/ai-stock-report-generator
cp skills/ai-stock-report-generator/SKILL.md ~/.claude/skills/ai-stock-report-generator/SKILL.md
```

安裝後重啟 Claude Code / Codex。

---

## 📊 估值方法

| 情境 | 方法 |
|------|------|
| **虧損股** | 以 P/B 為主軸 + P/S 交叉驗證 |
| **獲利股** | 加入 P/E 情境 |
| **DCF** | 簡化 DCF 估值 |
| **相對估值** | 同業 P/E、EV/EBITDA、P/B、ROE 倍數比較 |

> 目標倍數區間參考該產業歷史常態，並於假設表說明。

---

## 🏆 為什麼值得關注？

| 亮點 | 說明 |
|------|------|
| **一鍵生成** | 從代號到完整財務模型 + 簡報 |
| **即時資料** | 搜尋最新公開財務數據與日線資料 |
| **可稽核** | Excel 公式連動、資料來源標注、recalc.py 驗證 |
| **台股慣例** | 紅漲綠跌、P/B/P/S 為主 |
| **可調整假設** | 三情境預測、敏感度表 |
| **技術 + 基本面** | KD/MACD/K線型態 + DCF/相對估值 |
| **免責清晰** | 明確標註「分析與教學輔助，不是投資建議」 |

---

## 總結

**ai-stock-report-generator** 是一個給 Claude Code / Codex 的 Agent Skill，核心功能：

```text
台股代號 → 即時搜尋財務資料 → Excel 財務模型（8 表）
         → K 線型態圖表（HTML/PNG）
         → PPTX 投資簡報（14 頁）
```

它解決了「想快速分析一支股票，但手動整理資料、建立模型、畫圖、做簡報太花時間」的痛點。配合 Agent 的即時搜尋能力、Excel/PPTX 技能規範（色碼、公式驗證、視覺 QA）、以及台股慣例色彩，讓 anyone 都能快速產出專業級的財務分析素材。

對於**台股投資人、分析師、教學用途**，這是一個非常實用的自動化工具。

---

*本文於 2026-09-14 整理自 [github.com/yangchunyi0814/ai-stock-report-generator](https://github.com/yangchunyi0814/ai-stock-report-generator)*
