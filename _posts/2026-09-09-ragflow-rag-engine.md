---
title: "RAGFlow：開源 RAG 引擎與 Agent 平台功能總覽"
date: 2026-09-09
description: "RAGFlow 是一個領先的開源 Retrieval-Augmented Generation (RAG) 引擎，融合 RAG 與 Agent 能力，為 LLM 打造優質上下文層。支援深度文件理解、模板化分塊、Agentic Workflow、MCP 與多數據源整合。"
tags: [rag, retrieval-augmented-generation, agent, knowledge-base, llm]
---

# RAGFlow：開源 RAG 引擎與 Agent 平台功能總覽

![RAGFlow](/assets/images/ragflow/logo.svg)

[![Star History Chart](/assets/images/ragflow/star_history.svg)](https://star-history.com/#infiniflow/ragflow&Date)

## 專案概覽

**RAGFlow** 是一個領先的開源 Retrieval-Augmented Generation（RAG）引擎，融合最先進的 RAG 與 Agent 能力，為 LLM 打造優質的上下文層。它提供可適應任何規模企業的簡化 RAG 工作流。憑藉融合的 [context engine](https://ragflow.io/basics/what-is-agent-context-engine) 和預建 agent 模板，RAGFlow 讓開發者能高效精準地將複雜數據轉化為生產級 AI 系統。

| 項目 | 資訊 |
|------|------|
| **倉庫** | [infiniflow/ragflow](https://github.com/infiniflow/ragflow) |
| **Stars** | ⭐ 90,291 |
| **Forks** | 10,654 |
| **授權條款** | Apache License 2.0 |
| **主要語言** | Go + Python (3.13+) |
| **支援平台** | Docker（x86）、Linux / macOS / Windows |
| **最新版本** | v0.27.1 (2026-08) |
| **官網** | [ragflow.io](https://ragflow.io) |
| **文件** | [docs](https://ragflow.io/docs/dev/) |
| **Cloud** | [cloud.ragflow.io](https://cloud.ragflow.io) |
| **建立日期** | 2023-12 |

> RAGFlow 是 GitHub 上最受歡迎的 RAG 專案之一，曾入選 GitHub Octoverse。

## 核心功能

### 1. 深度文件理解（Deep Document Understanding）

- 基於深度文件理解的知識提取，支援複雜格式的無結構化數據
- 在無限 token 的「數據干草堆」中找出「針」
- 支援 Word、Slides、Excel、TXT、圖片、掃描件、結構化數據、網頁等
- 多模態模型理解 PDF/DOCX 中的圖片

### 2. 模板化分塊（Template-based Chunking）

![Chunking Demonstration](/assets/images/ragflow/chunking.gif)

- 智慧且可解釋的分塊策略
- 多種模板選項可供選擇
- 視覺化文本分塊，允許人工干預
- 快速查看關鍵引用和可追溯的引文

### 3. Agentic Workflow & MCP

![Agentic Workflow](/assets/images/ragflow/agentic.gif)

- **Agentic Workflow**：可編排的 agentic 工作流（2025-08）
- **MCP 支援**：Model Context Protocol 整合外部工具
- **Agent Memory**：AI agent 記憶功能（2025-12）
- **Code Executor**：Python/JavaScript 代碼執行組件（2025-05）
- **Orchestrable Ingestion Pipeline**：可編排的文件攝取管線（2025-10）

### 4. 多數據源整合

- **Confluence、S3、Notion、Discord、Google Drive** 數據同步（2025-11）
- 支援 Word、Slides、Excel、TXT、圖片、掃描件、結構化數據、網頁
- **MinerU & Docling** 文件解析方法（2025-10）

### 5. 多聊天通道

- **Feishu、Discord、Telegram、LINE** 等多聊天通道支援（2026-06）
- 將 RAG 知識庫直接嵌入團隊即時通訊工作流

### 6. Grounded Citations & 減少幻覺

- 可追溯引文支援有根據的回答
- 視覺化文本分塊允許人工干預
- 快速查看關鍵引用來源

### 7. 自動化 RAG 工作流

- 簡化的 RAG 編排，適合個人和大型企業
- 可配置的 LLM 和 embedding 模型
- 多重召回配融合重排序（fused re-ranking）
- 直覺 API 無縫整合業務系統

## 技術架構

![RAGFlow System Architecture](/assets/images/ragflow/architecture.png)

```
┌──────────────────────────────────────────────────────┐
│                  RAGFlow Platform                     │
├──────────────────────────────────────────────────────┤
│              Web UI (React + TypeScript)             │
│  ┌─────────┬──────────┬──────────┬──────────────┐   │
│  │ Dataset  │ Chat /   │ Agent    │ Knowledge   │   │
│  │ Manager  │ QA       │ Builder  │ Base        │   │
│  │(Upload/  │(RAG Q&A) │(Workflow)│(Search/     │   │
│  │ Chunk)   │          │          │ Cite)       │   │
│  └─────────┴──────────┴──────────┴──────────────┘   │
├──────────────────────────────────────────────────────┤
│              Core Engine (Python + Go)               │
│  ┌──────────┬──────────┬──────────┬─────────────┐   │
│  │ DeepDoc   │ Chunking │ Retrieval│ Agent       │   │
│  │(Deep     │(Template-│(Multi-   │ Engine      │   │
│  │ Doc       │ based)   │ recall + │(MCP/Tools/ │   │
│  │ Understd.)│          │ Re-rank) │ Memory)    │   │
│  └──────────┴──────────┴──────────┴─────────────┘   │
│  ┌──────────┬──────────┬──────────┬─────────────┐   │
│  │ LLM      │ Embedding│ Code     │ Data Sync   │   │
│  │ Manager  │ Models   │ Executor │(Confluence/ │   │
│  │(Multi-   │          │(Python/  │ S3/Notion/  │   │
│  │ Provider)│          │ JS/gVisor)│ Drive)     │   │
│  └──────────┴──────────┴──────────┴─────────────┘   │
├──────────────────────────────────────────────────────┤
│         Infrastructure                               │
│   Elasticsearch / Infinity (vector + full-text)      │
│   MySQL (metadata) / Redis (cache/queue)            │
│   MinIO (object storage)                            │
│   gVisor (sandbox for code executor)                │
│   Docker Compose                                    │
└──────────────────────────────────────────────────────┘
```

## 支援的模型與服務

| 類別 | 支援 |
|------|------|
| **LLM** | OpenAI GPT-5 系列、DeepSeek v4、Gemini 3 Pro、Anthropic Claude、及更多 |
| **Embedding** | 可配置 embedding 模型 |
| **文件解析** | MinerU、Docling、DeepDoc（內建） |
| **向量引擎** | Elasticsearch（預設）、Infinity（可切換） |

## 部署方式

### Docker Compose（推薦）

```bash
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/docker
git checkout v0.27.1
docker compose -f docker-compose.yml up -d
```

**硬體需求**：
- CPU >= 4 cores
- RAM >= 16 GB
- Disk >= 50 GB
- Docker >= 24.0.0 & Docker Compose >= v2.26.1

### GPU 加速 DeepDoc

```bash
sed -i '1i DEVICE=gpu' .env
docker compose -f docker-compose.yml up -d
```

### 從源碼開發

```bash
uv sync --python 3.13
uv run python3 ragflow_deps/download_deps.py
docker compose -f docker/docker-compose-base.yml up -d
# Backend:
source .venv/bin/activate && bash docker/launch_backend_service.sh
# Frontend:
cd web && npm install && npm run dev
```

### 切換向量引擎（Elasticsearch → Infinity）

```bash
docker compose -f docker/docker-compose.yml down -v
# 設定 DOC_ENGINE=infinity in docker/.env
docker compose -f docker/docker-compose.yml up -d
```

## v0.27.x 重要更新時間線

| 日期 | 更新 |
|------|------|
| 2026-06-15 | 支援多聊天通道（Feishu、Discord、Telegram、LINE） |
| 2026-04-24 | 支援 DeepSeek v4 |
| 2026-03-24 | RAGFlow Skill on OpenClaw |
| 2025-12-26 | 支援 AI Agent Memory |
| 2025-11-19 | 支援 Gemini 3 Pro |
| 2025-11-12 | 數據同步：Confluence、S3、Notion、Discord、Google Drive |
| 2025-10-23 | MinerU & Docling 文件解析 |
| 2025-10-15 | 可編排攝取管線 |
| 2025-08-08 | GPT-5 系列模型 |
| 2025-08-01 | Agentic Workflow & MCP |
| 2025-05-23 | Python/JavaScript Code Executor |
| 2025-03-19 | 多模態理解 PDF/DOCX 圖片 |

## 主要貢獻者

| 貢獻者 | Commits |
|--------|---------|
| cike8899 | 1,338 |
| KevinHuSh | 1,047 |
| JinHai-CN | 554 |
| writinwaters | 404 |
| dcc123456 | 403 |

## 與其他 RAG 框架比較

| 特性 | **RAGFlow** | LangChain | LlamaIndex | Dify |
|------|-------------|-----------|------------|------|
| 深度文件理解 | ✅ DeepDoc + MinerU/Docling | 需自組 | 需自組 | 基本 |
| 模板化分塊 | ✅ 多模板可視化 | ❌ | 部分 | ❌ |
| Agentic Workflow | ✅ 內建 | ✅ (LangGraph) | ✅ | ✅ |
| MCP 支援 | ✅ | 部分 | 部分 | 部分 |
| Code Executor | ✅ (gVisor sandbox) | ❌ | ❌ | 有限 |
| 多數據源同步 | ✅ Confluence/S3/Notion... | 需自組 | 需自組 | 有限 |
| 多聊天通道 | ✅ Feishu/Discord/TG/LINE | ❌ | ❌ | ✅ |
| 可追溯引文 | ✅ 內建 | 需自組 | 部分 | 部分 |
| 自託管 | ✅ Docker | ✅ | ✅ | ✅ |
| 授權 | Apache-2.0 | MIT | MIT | 混合 |

## 社群

- **Discord**: https://discord.gg/NjYzJD3GM3
- **X (Twitter)**: https://x.com/infiniflowai
- **GitHub Discussions**: https://github.com/orgs/infiniflow/discussions
- **Roadmap**: [RAGFlow Roadmap 2026](https://github.com/infiniflow/ragflow/issues/12241)

## 參考連結

- **GitHub**: https://github.com/infiniflow/ragflow
- **官網**: https://ragflow.io
- **Cloud**: https://cloud.ragflow.io
- **文件**: https://ragflow.io/docs/dev/
- **Docker Hub**: https://hub.docker.com/r/infiniflow/ragflow
- **Infinity（向量引擎）**: https://github.com/infiniflow/infinity
- **Star History**: https://star-history.com/#infiniflow/ragflow&Date
