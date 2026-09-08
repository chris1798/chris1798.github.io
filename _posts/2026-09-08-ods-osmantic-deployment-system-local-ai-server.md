---
title: "ODS（Osmantic Deployment System）：一指令把 PC/Mac/Linux 變成私人 AI 伺服器"
date: 2026-09-08
description: ODS（Osmantic Deployment System）是開源的本地 AI 部署系統，把 LLM 推論、Chat UI、語音、Agent、工作流、RAG、圖片生成整合成一個可一指令安裝的完整堆疊。支援 NVIDIA/AMD/Apple Silicon/Intel Arc，Apache-2.0。
tags:
  - open-source
  - local-ai
  - llm
  - self-hosted
  - docker
  - llama-cpp
  - open-webui
cover: /assets/images/ods/osmantic-lockup.png
---

# ODS（Osmantic Deployment System）：把電腦變成私人 AI 伺服器

![ODS](/assets/images/ods/osmantic-lockup.png)

> **Turn your PC, Mac, or Linux box into a private AI server.**
> LLM 推論、Chat UI、語音、Agent、工作流、RAG、圖片生成——一指令搞定。

---

## 📊 專案速覽

| 項目 | 資料 |
|------|------|
| **名稱** | ODS（Osmantic Deployment System） |
| **組織** | Osmantic |
| **授權** | Apache-2.0 |
| **Stars** | ⭐ 6,254 |
| **Forks** | 899 |
| **開發語言** | Python |
| **版本** | v2.6.0（stable） |
| **建立時間** | 2026-02-09 |
| **官方網站** | [osmantic.com](https://osmantic.com) |

---

## 🎯 什麼是 ODS？

### 一句話說明

> **把「跑本地 AI」這件事，從手動拼裝十幾個專案（Ollama、Open WebUI、n8n、ComfyUI…），變成一指令安裝的完整堆疊。**

ODS 自動偵測你的 GPU、選適合的模型、生成憑證、啟動所有服務，並給你本地網頁 UI。

### 為什麼要 ODS？

```text
傳統做法：手動裝 Ollama + Open WebUI + n8n + ComfyUI + Whisper…
          → 寫 Docker config → 禱告它們能互相溝通 → 大部分人放棄回 OpenAI

ODS：一指令 → 偵測 GPU → 選模型 → 啟動全部 → 2 分鐘內開始聊天
```

---

## ✨ 核心特色

### 1. 一指令安裝（One-Command Install）

**Linux / macOS：**
```bash
curl -fsSL https://install.osmantic.com/ods.sh | bash
```

**Windows PowerShell：**
```powershell
# 下載 source ZIP → 執行 install.ps1
```

> **API endpoint**：Linux Docker 預設 `http://localhost:11434`（llama-server），macOS/Windows native 用 `http://localhost:8080`。Open WebUI 在 `http://localhost:3000`。

### 2. Bootstrap Mode（免等待）

```text
1. 先下載一個 1.5B 小模型（< 1 分鐘）
2. 你立刻可以開始聊天
3. 完整模型在背景下載
4. 下載完熱切換——零停機時間
```

### 3. 硬體自動偵測（Hardware Auto-Detection）

安裝器偵測 GPU → 分配確定性硬體 tier → 讀 `model-library.json` 選最佳 GGUF。

| 平台 | 支援狀態 |
|------|---------|
| **Linux**（NVIDIA + AMD + Intel Arc） | ✅ 可裝可用 |
| **Windows**（NVIDIA + AMD，WSL2/Docker Desktop） | ✅ 可裝可用 |
| **macOS**（Apple Silicon M1+） | ✅ 可裝可用 |

### 4. 完全可改（Fully Moddable）

每個服務都是「extension」——一個含 `manifest.yaml` + `compose.yaml` 的資料夾。Dashboard、CLI、健康檢查、compose stack 都會自動發現。

```bash
ods enable my-service     # 啟用
ods disable my-service    # 停用
ods list                  # 看全部
```

---

## 📦 What's In The Box（內建服務）

### 💬 Chat & Inference

| 服務 | 說明 |
|------|------|
| **Open WebUI** | 完整聊天介面、對話歷史、網頁搜尋、文件上傳、30+ 語言 |
| **llama-server** | 高性價比 LLM 推論、continuous batching、自動選 GPU |
| **LiteLLM** | API gateway，支援 local/cloud/hybrid |
| **TEI Embeddings** | 文字嵌入服務（RAG/搜尋） |

### 🎙️ Voice

| 服務 | 說明 |
|------|------|
| **Whisper** | 語音轉文字（STT） |
| **Kokoro** | 文字轉語音（TTS） |

### 🤖 Agents & Automation

| 服務 | 說明 |
|------|------|
| **Hermes Agent** | 預設 local-first 自主/瀏覽器 agent，含記憶、skills、magic-link proxy |
| **OpenClaw** | 已棄用 legacy agent（遷移期間仍可選） |
| **n8n** | 工作流自動化，400+ 整合（Slack、email、DB、API） |
| **APE** | Agent Policy Engine——審計與治理自主工具呼叫 |
| **OpenCode** | 瀏覽器 AI coding assistant，接本地堆疊 |
| **Memory Shepherd** | agent 記憶生命週期管理（host/systemd helper） |

### 🔍 Knowledge & Search

| 服務 | 說明 |
|------|------|
| **Qdrant** | 向量資料庫（RAG） |
| **SearXNG** | 自架網頁搜尋（無追蹤） |
| **Perplexica** | 深度研究引擎 |
| **Brave Search** | 選用付費 Brave API |

### 🎨 Creative

| 服務 | 說明 |
|------|------|
| **ComfyUI** | 節點式圖片生成 |

### 🔒 Privacy & Ops

| 服務 | 說明 |
|------|------|
| **Privacy Shield** | PII scrubbing proxy（API 呼叫前洗掉個人資料） |
| **Dashboard** | 即時 GPU metrics、服務健康、模型管理 |
| **Token Spy** | token 用量監控（local + proxied LLM 流量） |
| **Langfuse** | 選用 LLM observability / tracing |

---

## 🖥️ 硬體自動選型（Auto-Model Selection）

### NVIDIA

| Tier / VRAM | 預設模型 | Context | 例 |
|------|---------|---------|-----|
| 0 / 8 GB CPU fallback | Qwen3.5 2B (Q4_K_M) | 8K | 低 RAM CPU-only |
| 1 / 8 GB | Qwen3.5 9B (Q4_K_M) | 32K | RTX 4060, 3060 12GB |
| 2 / 12 GB | Phi-4 14B (Q4_K_M) | 16K | RTX 4070-class |
| 3 / 24 GB | Qwen3.5 27B (Q4_K_M) | 32K | RTX 4090, A6000 |
| 4 / 48 GB | DeepSeek R1 Distill Llama 70B (Q4_K_M) | 32K | A6000 Ada, L40S |
| NV_ULTRA / 90+ GB | Qwen3 Coder Next (Q4_K_M) | 128K | Multi-GPU A100/H100 |

### AMD Strix Halo（統一記憶體）

| Tier / RAM | 預設模型 | Context |
|------|---------|---------|
| SH_COMPACT / 64 GB | Qwen3.6 35B-A3B (UD-Q4_K_M) | 128K |
| SH_LARGE / 96 GB | DeepSeek R1 Distill Llama 70B (Q4_K_M) | 32K |

### Apple Silicon（統一記憶體、Metal）

| Tier / RAM | 預設模型 | Context |
|------|---------|---------|
| 0 / 8 GB | Phi-4 Mini (Q4_K_M) | 128K |
| 1 / 16 GB | Qwen3.5 9B (Q4_K_M) | 32K |
| 2 / 32 GB | Phi-4 14B (Q4_K_M) | 16K |
| 3 / 48 GB | Qwen3.5 27B (Q4_K_M) | 32K |
| 4 / 64+ GB | Qwen3.6 35B-A3B (UD-Q4_K_M) | 128K |

### Intel Arc（Linux、SYCL）

| Tier / VRAM | 預設模型 | Context |
|------|---------|---------|
| ARC_LITE / 6 GB | Phi-4 Mini (Q4_K_M) | 128K |
| ARC_LITE / 8 GB | Qwen3.5 9B (Q4_K_M) | 32K |
| ARC / 16 GB | Phi-4 14B (Q4_K_M) | 16K |

---

## 🔄 切換模型（Switching Models）

```bash
ods model current              # 現在跑什麼？
ods model list                 # 所有可用 tier
ods model swap T3              # 切到不同 tier

# 先預下載再切換
./scripts/pre-download.sh --tier 3
ods model swap T3              # 切換（重啟 llama-server）
```

> **自動回滾**：新模型載入失敗時，ODS 自動回到你之前的模型。

---

## 🧩 Extensibility（擴展系統）

每個服務都是 extension——資料夾含 `manifest.yaml` + `compose.yaml`：

```text
extensions/services/
  my-service/
    manifest.yaml      # 金鑰：name、port、health endpoint、GPU backends
    compose.yaml       # Docker Compose fragment（自動合併進 stack）
```

安裝器本身也是模組化——19 library modules、共享 service registry、13 ordered phases。

---

## ⌨️ ods-cli（命令列管理）

```bash
ods status                # 健康檢查 + GPU 狀態
ods list                  # 所有服務及狀態
ods logs llm              # tail log（別名：llm, stt, tts）
ods restart [service]     # 重啟一個或全部
ods start / stop          # 啟動/停止 stack

ods mode cloud            # 切到 cloud API（LiteLLM）
ods mode local            # 切回本地推論
ods mode hybrid           # 本地為主、cloud fallback

ods model swap T3         # 切換硬體 tier
ods enable n8n            # 啟用 extension
ods disable whisper       # 停用一個

ods config show           # 看 .env（secrets masked）
ods preset save gaming    # 快照目前設定
ods preset load gaming    # 還原
```

---

## ☁️ Cloud Mode（無 GPU 也能跑）

```bash
./install.sh --cloud
```

同一套完整 stack，改用 OpenAI/Anthropic/Together API 而非本地推論。

---

## 📊 How It Compares（比較表）

| | ODS | Ollama + Open WebUI | LocalAI |
|---|:---:|:---:|:---:|
| **Scope** | 完整 AI stack（推論→agent→工作流） | LLM + chat | 僅 LLM |
| 一指令安裝 | 全部自動配置 | 僅 LLM + chat | 僅 LLM |
| 硬體自動偵測 + 選型 | NVIDIA + AMD Strix Halo + Apple Silicon + Intel Arc + CPU/cloud | 無 | 無 |
| AMD APU 統一記憶體 | 平台專用加速後端 | 部分（Vulkan） | 無 |
| 自主 AI agents | Hermes Agent 預設 | 無 | 無 |
| 工作流自動化 | n8n（400+） | 無 | 無 |
| 語音（STT + TTS） | Whisper + Kokoro | 無 | 無 |
| 圖片生成 | ComfyUI | 無 | 無 |
| RAG pipeline | Qdrant + embeddings | 無 | 無 |
| Extension 系統 | Manifest-based、熱插拔 | 無 | 無 |
| Multi-GPU | 是（NVIDIA） | 部分 | 部分 |

---

## 🏗️ 專案架構

```text
ODS/
├── README.md             # 公開說明
├── installers/           # 各平台安裝器
├── .github/workflows/    # CI
└── ods/                  # 產品 runtime
    ├── services/         # 各服務
    ├── installer phases/ # 13 ordered phases
    ├── compose overlays/ # Docker Compose 覆蓋
    ├── dashboard/        # 控制儀表板
    ├── cli/              # ods CLI
    ├── tests/            # 測試
    └── docs/             # operator 文件
```

---

## 📝 Release Validation（發布驗證）

ODS 用 release-grade fleet + distro lab 做驗證：

- **zero-prereq bootstrap**——零前置依賴引導
- **fresh installs**——全新安裝
- **product flows**——產品流程
- **full-model capabilities**——完整模型能力
- **lifecycle recovery**——生命週期恢復
- **User Green gate**——最終使用者綠燈

所有 PR 與 push 在 Linux / Windows / macOS 三平台 CI 自動驗證。

---

## 📚 文件索引

| 文件 | 說明 |
|------|------|
| [Quickstart](https://github.com/Osmantic/ODS/blob/main/ods/QUICKSTART.md) | 逐步安裝指南 + 除錯 |
| [Docs Index](https://github.com/Osmantic/ODS/tree/main/ods/docs) | operator/contributor/reviewer 地圖 |
| [Build On ODS](https://github.com/Osmantic/ODS/blob/main/ods/docs/BUILD-ON-ODS-SERVER.md) | fork、自訂版、extension 模板 |
| [Forkability](https://github.com/Osmantic/ODS/blob/main/ods/docs/FORKABILITY.md) | 如何 fork、審計、自訂 |
| [Support Matrix](https://github.com/Osmantic/ODS/blob/main/ods/docs/SUPPORT-MATRIX.md) | 平台 + GPU 支援狀態 |
| [Hardware Guide](https://github.com/Osmantic/ODS/blob/main/ods/docs/HARDWARE-GUIDE.md) | 該買什麼、tier 建議 |
| [Extensions](https://github.com/Osmantic/ODS/blob/main/ods/docs/EXTENSIONS.md) | 如何加自訂服務 |

---

## 🏆 為什麼值得關注？

| 亮點 | 說明 |
|------|------|
| **一指令安裝** | 偵測 GPU、選模型、啟動全部 |
| **2 分鐘內聊天** | Bootstrap mode 立即可用 |
| **完整堆疊預接線** | chat/agent/voice/workflow/RAG/image/privacy |
| **完全可改** | 每個服務是 extension，熱插拔 |
| **跨平台** | Linux / Windows / macOS Apple Silicon |
| **隱私優先** | 資料留本地，cloud 可選 |
| **AMD Featured Developer** | AMD Lemonade Developer Challenge 2026-05 獲獎 |

---

## 總結

**ODS（Osmantic Deployment System）** 是 Osmantic 開發的開源本地 AI 部署系統，核心亮點：

```text
一指令 → 偵測 GPU → 選模型 → 啟動完整堆疊
（LLM 推論 + Chat UI + 語音 + Agent + 工作流 + RAG + 圖片生成）
```

它解決了「跑本地 AI 要手動拼裝十幾個專案」的痛點，用**一指令安裝 + 硬體自動選型 + Bootstrap mode**讓 anyone 在 2 分鐘內開始跟自己的模型聊天。配合完整的 extension 系統、跨平台支援（NVIDIA/AMD/Apple Silicon/Intel Arc）、隱私優先設計（資料留本地），以及嚴格的 release validation，是想要自架私人 AI 伺服器的強大工具。

對於想在**家中實驗室、工作站、辦公室**跑本地 AI 的人，ODS 是目前最完整的開源方案之一。

---

*本文於 2026-09-08 整理自 [github.com/Osmantic/ODS](https://github.com/Osmantic/ODS)*
