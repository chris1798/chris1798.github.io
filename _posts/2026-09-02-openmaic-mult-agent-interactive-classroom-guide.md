---
title: "OpenMAIC：清華大學開源的「多智能體互動課堂」平台，一鍵把主題變成沉浸式教學"
date: 2026-09-02
description: OpenMAIC（Open Multi-Agent Interactive Classroom）是由清華大學 MAIC 團隊開發的開源教育平台。它用多智能體協作，把任何主題或文件一鍵轉換成完整的互動課堂——有 AI 教師講課、AI 同學討論、白板繪圖、測驗與實作，支援 PPTX/HTML 匯出，可透過訊息 App 生成課堂。
tags:
  - open-source
  - education
  - multi-agent
  - ai
  - langgraph
  - nextjs
cover: /assets/images/openmaic/banner.png
---

# OpenMAIC：清華大學開源的「多智能體互動課堂」平台

![OpenMAIC](/assets/images/openmaic/banner.png)

> **一鍵把任何主題或文件，轉換成沉浸式多智能體互動課堂。**
> Get an immersive, multi-agent learning experience in just one click.

---

## 📊 專案速覽

| 項目 | 資料 |
|------|------|
| **名稱** | OpenMAIC（Open Multi-Agent Interactive Classroom） |
| **團隊** | 清華大學 MAIC（THU-MAIC） |
| **授權** | MIT（2026-06-28 由 AGPL-3.0 調整） |
| **Stars** | ⭐ 29,725 |
| **Forks** | 4,998 |
| **開發語言** | TypeScript |
| **技術棧** | Next.js 16 + React 19 + LangGraph 1.1 + Tailwind CSS 4 |
| **最新版本** | v1.0.0（2026-08-27） |
| **官方網站** | [openmaic.io](https://openmaic.io) / Demo: [open.maic.chat](https://open.maic.chat) |

---

## 🎯 什麼是 OpenMAIC？

### 一句話說明

> **把「一個主題」或「一份文件」，一鍵生成一個完整的互動式 AI 課堂。**

它不只是聊天式學習助手，而是把**讲授、提问、讨论、白板演示、互动实验、项目学习**整合成一套完整的課堂體驗。

### 核心機制：多智能體協作（Multi-Agent Orchestration）

OpenMAIC 調度多個專業 AI 智能體協同工作：

```text
        你的主題或文件
              ↓
   ┌─────────────────────┐
   │  多智能體協調引擎     │
   │  (LangGraph 驅動)    │
   └────────┬────────────┘
            ↓
   ┌────────┴──────────────┐
   ▼                      ▼
AI 教師                AI 同學
（講課、繪圖、       （即時討論、
  朗讀、發問）         提問、互動）
```

AI 教師與 AI 同學會**講課、在白板上畫圖寫公式、朗讀講解**，並與你進行**即時討論**。

---

## ✨ 主要功能

### 1. 一鍵生成課程（One-Click Lesson Generation）

| 功能 | 說明 |
|------|------|
| **描述主題** | 給一個主題，AI 幾分鐘內建好整堂課 |
| **上傳材料** | 附上你的文件，AI 從中生成內容 |
| **多場景類型** | 投影片、測驗、互動 HTML 模擬、專案學習（PBL） |

### 2. 多智能體課堂（Multi-Agent Classroom）

- **AI 教師**：講課、在白板繪圖、寫公式、朗讀講解
- **AI 同學**：與你即時互動、討論、提問
- **即時討論**：多角色對話式學習

### 3. 白板與語音（Whiteboard & TTS）

- 智能體會**在白板上繪製圖表、寫公式**
- **TTS 語音朗讀**：智能體「講」出解釋
- 支援**聲音克隆**（VoxCPM2）

### 4. 深度互動模式（Deep Interactive Mode）

| 互動類型 | 說明 |
|---------|------|
| **3D 視覺化** | 三維模型展示 |
| **模擬實驗** | 互動式模擬 |
| **遊戲** | 遊戲化學習 |
| **心智圖** | Mind Map |
| **線上程式設計** | 實作環境 |

### 5. 匯出與分享（Export Anywhere）

| 格式 | 說明 |
|------|------|
| **`.pptx`** | 可編輯的簡報投影片 |
| **`.html`** | 互動式網頁 |
| **`.mp4`** | 一鍵影片匯出（選用） |
| **ZIP** | 課堂打包匯出/匯入 |

### 6. OpenClaw 整合（從訊息 App 生成課堂）

```text
用 OpenClaw，從下列 App 直接生成課堂，零設定：
  飛書 / Slack / Discord / Telegram / 20+ 訊息 App
```

```bash
# 安裝
clawhub install openmaic
# 然後對你的助手說：「教我量子物理」
```

- **Hosted 模式**：在 [open.maic.chat](https://open.maic.chat) 取得 access code
- **Self-hosted 模式**：逐步引導你 clone、設定、啟動

---

## 🚀 v1.0.0 重點更新（Agent Workbench）

2026-08-27 推出的 v1.0.0 新增了**專業工作區（Pro Workbench）**：

| 能力 | 說明 |
|------|------|
| **規劃課程** | 規劃多堂課大綱、建立課程與資料夾、搬移重命名 |
| **建置與編輯** | 讀取/搜尋 stage DSL、單場景原子編輯、增刪排序頁面 |
| **使用材料** | 上傳檔案、提取文件/音訊/影片、搜尋文字、抓取網頁 |
| **建立媒體** | 生成圖片、影片、旁白音訊 |
| **匯入檢視** | 匯入 `.pptx` 保留版面、場景預覽 |
| **設定課堂** | 列舉語音、設定智能體名單、聲音克隆 |

### 20 個內建 Skills

涵蓋：課程規劃、深度研究、互動、講授、工作坊、職训等教學風格，簡報/舞台設計、PPTX 匯入、編輯、風格重用。

---

## 🏗️ 技術架構

| 層 | 技術 |
|----|------|
| **前端框架** | Next.js 16（App Router） |
| **UI 庫** | React 19 + Tailwind CSS 4 |
| **程式語言** | TypeScript 5 |
| **狀態機/協調** | LangGraph 1.1（多智能體流程） |
| **後端** | Next.js API Routes（~18 端點） |
| **生成流程** | 大綱 → 內容 → 圖片 → TTS |
| **可選儲存** | PostgreSQL（後端持久化） |

### API 結構

```text
app/
├── api/                    # Server API routes (~18 端點)
│   ├── generate/           # 場景生成流程（大綱、內容、圖片、TTS…）
│   ├── generate-classroom/ # 非同步課堂任務提交 + polling
│   ├── chat/               # 多智能體討論（SSE 串流）
│   ├── pbl/                # 專案學習端點
│   └── ...
```

---

## ⚙️ 支援的模型與供應商

### 支援的 LLM 供應商

| 供應商 | 備註 |
|--------|------|
| **OpenAI** | GPT 系列 |
| **Azure OpenAI** | 企業版 |
| **Anthropic** | Claude 系列 |
| **Amazon Bedrock** | AWS |
| **Google Gemini** | Gemini 3 系列（推薦 Gemini 3 Flash） |
| **DeepSeek** | 中國 |
| **Qwen** | 通義千問 |
| **Kimi** | 月之暗面 |
| **MiniMax** | M2.7 |
| **Grok (xAI)** | |
| **OpenRouter** | 多模型聚合 |
| **Doubao** | 豆包 |
| **Tencent Hunyuan** | 騰訊混元 |
| **Xiaomi MiMo** | 小米 |
| **GLM (Zhipu)** | 智譜 |
| **Ollama** | 本地 |
| **Lemonade** | 本地 OpenAI 相容 |
| **FunASR** | 本地語音辨識 |

### 支援的模型（更新至 v1.0.0）

```text
GLM-5.2、Kimi K2.7 Code、Qwen3.7 Plus/Max
Gemini 3 Flash / 3.1 Pro、GPT-5.5、Claude Opus 4.8
DeepSeek-V4、GPT-Image-2、Xiaomi MiMo、Hy3
```

---

## 🛠️ 快速安裝步驟

### 環境需求

- **Node.js** >= 20
- **pnpm** >= 10

### 步驟 1：Clone 並安裝

```bash
git clone https://github.com/THU-MAIC/OpenMAIC.git
cd OpenMAIC
pnpm install
```

### 步驟 2：設定

```bash
cp .env.example .env.local
```

至少填入一個 LLM 供應商金鑰：

```env
OPENAI_API_KEY=sk-...
# 其他可選：
AZURE_OPENAI_API_KEY=...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
GROK_API_KEY=xai-...
DEFAULT_MODEL=google:gemini-3-flash-preview
```

### 步驟 3：啟動

```bash
pnpm dev
```

開啟 [http://localhost:3000](http://localhost:3000)

### 步驟 4：生產建置

```bash
pnpm build && pnpm start
```

---

## 📦 其他部署方式

### Vercel 一鍵部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FTHU-MAIC%2FOpenMAIC)

### Docker 部署

```bash
cp .env.example .env.local
# 編輯 .env.local 填入 API key，然後：
docker compose up --build
```

### 中國加速（Docker）

```bash
ALPINE_MIRROR=mirrors.tuna.tsinghua.edu.cn \
NPM_REGISTRY=https://registry.npmmirror.com \
docker compose up --build
```

### ACCESS_CODE 保護（共享部署）

```env
ACCESS_CODE=your-secret-code
```

---

## 🧩 進階可選設定

| 功能 | 說明 |
|------|------|
| **Lemonade（本地 AI）** | LLM / 圖片 / TTS / ASR，无需 API key |
| **FunASR（本地語音辨識）** | SenseVoiceSmall / Paraformer / Fun-ASR-Nano |
| **ffmpeg（本地音影片提取）** | 提取時間戳字幕與影片幀 |
| **MinerU（文件解析）** | 複雜表格、公式、OCR |
| **VoxCPM2（自架 TTS）** | 声音克隆，支援 vLLM / Python / Nano-vLLM |
| **Postgres 持久化** | 課程資料伺服器端保存 |
| **MP4 影片匯出** | 透過 render-service 容器渲染 |
| **分階段模型路由** | 每個階段可用不同模型 |

---

## 🎓 使用場景

| 場景 | 說明 |
|------|------|
| **教師備課** | 一鍵生成教案與授課內容 |
| **自學** | 丟一份文件給它，自動變成教學 |
| **企業訓練** | 職訓任務引擎 |
| **技術教學** | 3D 視覺化、模擬、實作 |
| **遠端教學** | 從訊息 App 直接調用 |

---

## 🏆 為什麼值得關注？

| 亮點 | 說明 |
|------|------|
| **一鍵生成** | 從主題到完整課堂，幾分鐘完成 |
| **多智能體** | AI 教師 + AI 同學即時互動 |
| **中立設計** | 帶自己的模型、媒體、搜尋、儲存後端 |
| **開源免費** | MIT 授權 |
| **部署彈性** | 本地 / Docker / Vercel 皆可 |
| **生態整合** | OpenClaw 訊息 App 整合 |
| **文獻支援** | 已發表於 JCST'26 |

---

## 總結

OpenMAIC 是清華大學 MAIC 團隊開發的**開源多智能體互動課堂平台**，核心亮點：

```text
一個主題/文件 → 多智能體協調 → 完整互動課堂
（講課、討論、白板、測驗、實作、PBL）
```

它把教育技術與 **AI 智能體協作**結合，讓 anyone 都能快速生成高質量的互動教學內容。配合中立設計（自帶模型/媒體/儲存）與靈活的部署方式（本地 / Docker / Vercel / OpenClaw），適合教師、自學者、企業訓練等多種場景。

對於想在**教育、訓練、教學**場景中利用 AI 的人，OpenMAIC 是值得收藏的開源專案。

---

*本文於 2026-09-02 整理自 [github.com/THU-MAIC/OpenMAIC](https://github.com/THU-MAIC/OpenMAIC)*
