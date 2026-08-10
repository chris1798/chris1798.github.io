---
title: "Open WebUI 知識庫（RAG）完整設定指南：上傳文件、建立知識庫、模型綁定與自動檢索"
date: 2026-08-05
description: 手把手教學如何在 Open WebUI 中設定 RAG 知識庫，包含 Embedding 模型配置、文件上傳、模型綁定、進階參數與常見問題排除
tags: [openwebui, rag, knowledge-base, embedding, ollama, ai-chat, document-retrieval]
---

# Open WebUI 知識庫（RAG）完整設定指南

Open WebUI 的知識庫功能透過 **RAG（Retrieval-Augmented Generation，檢索增強生成）** 實現，讓模型在回答問題時自動從你上傳的知識庫中搜尋相關內容，而不是依賴模型自身訓練數據中的知識。

---

## 核心概念

### RAG 工作原理

```
使用者提問
    ↓
Open WebUI 用 Embedding Model 將問題轉為向量
    ↓
在知識庫中搜尋最相關的文本片段（Top K）
    ↓
將搜尋結果 + 使用者問題 一起送給 LLM
    ↓
LLM 基於知識庫內容生成回答
```

### 兩種搜尋模式

| 模式 | 說明 | 適用情境 |
|------|------|----------|
| **Focused Retrieval (RAG)** | 使用向量搜尋，只取最相關的片段 | 大型知識庫、多份文件 |
| **Full Context Mode** | 將整份文件內容直接注入模型 | 單一文件、需要完整上下文的精確任務 |

---

## 前置準備

### 必要元件

| 元件 | 說明 | 必要？ |
|------|------|--------|
| **Open WebUI** | 主應用程式 | ✅ 必要 |
| **Embedding Model** | 將文本轉為向量（如 nomic-embed-text、bge-m3） | ✅ 必要 |
| **LLM Model** | 生成回答的語言模型（如 llama3、gpt-4o） | ✅ 必要 |
| **向量資料庫** | Open WebUI 內建，無需額外安裝 | ✅ 自動 |

### 推薦的 Embedding Model

| 模型 | 語言支援 | 大小 | 推薦度 |
|------|----------|------|--------|
| **nomic-embed-text** | 英文為主 | ~274MB | ⭐⭐⭐⭐ |
| **bge-m3** | 中英多語言 | ~1.2GB | ⭐⭐⭐⭐⭐ |
| **text-embedding-3-small** | 英文為主（API） | API 调用 | ⭐⭐⭐⭐ |

---

## 完整設定步驟

### Step 1：啟用 Embedding 模型

#### 方式一：使用 Ollama 本機 Embedding（推薦）

```bash
# 下載 bge-m3 模型（支援多語言，效果最佳）
ollama pull bge-m3

# 或下載 nomic-embed-text（較小，速度快）
ollama pull nomic-embed-text
```

在 Ollama 啟動參數中加入：

```yaml
# docker-compose.yml 或環境變數
OLLAMA_EMBEDDING_MODELS="nomic-embed-text:bge-m3"
```

#### 方式二：使用 OpenAI Embedding API

如果已設定 OpenAI API Key，可直接使用 `text-embedding-3-small`，無需額外安裝。

### Step 2：建立知識庫

1. 進入 Open WebUI
2. 點擊左側側邊欄的 **「Knowledge」**（知識庫）
3. 點擊 **「+ New Knowledge」** 建立新知識庫
4. 輸入知識庫名稱（例如：「公司規範」、「產品文件」）

### Step 3：上傳文件到知識庫

在知識庫頁面點擊 **「+」** 上傳文件。

**支援的檔案格式**：
- `.pdf`、`.docx`、`.txt`、`.md`、`.csv`、`.html`、`.json`、`.xml`
- 也支援上傳 **資料夾**（會自動遞迴掃描）

上傳後 Open WebUI 會自動執行以下流程：
1. 解析文件內容
2. 將文本分塊（Chunking）
3. 用 Embedding Model 轉換為向量
4. 存入向量資料庫

> ⚠️ **注意**：上傳後需要等待一段時間（取決於文件大小和數量），這段時間是 Embedding 處理過程。檔案較小時秒即可完成，檔案較大時可能需要數分鐘。

### Step 4：綁定知識庫到模型

#### 方式一：在對話中選擇知識庫（手動）

在聊天時，點擊模型選擇旁的 **「Select Knowledge」**，選擇已建立的知識庫。

#### 方式二：為特定模型預設綁定知識庫（推薦）

1. 進入 **「Model」** 設定頁面
2. 建立一個新模型或編輯現有模型
3. 在模型設定中找到 **「Knowledge」** 欄位
4. 選擇要綁定的知識庫
5. 保存設定

這樣當選擇這個模型時，會 **自動** 使用該知識庫，無需每次手動選擇。

### Step 5：開始使用

選擇綁定知識庫的模型，開始提問即可。Open WebUI 會自動從知識庫搜尋相關內容並回答。

---

## 進階功能

### 外部數據源（RAG Source）

Open WebUI 也支援從外部數據源（如 PostgreSQL、Pinecone、Weaviate 等）進行 RAG：

1. 進入 Workspace → Knowledge → **External Sources**
2. 設定外部數據庫連接資訊
3. 測試連線（必須通過才能保存）
4. 保存後，外部來源會像普通知識庫一樣出現在知識庫列表中

### Chunk 設定（文本分塊）

| 參數 | 說明 | 建議值 |
|------|------|--------|
| **Chunk Size** | 每個文本塊的大小（字元數） | 300-500 |
| **Chunk Overlap** | 相鄰塊之間的重疊字元數 | 50-100 |
| **Top K** | 搜尋時返回最相關片段數量 | 3-5 |

### 搜尋模式設定

在聊天設定中可以切換：

```
Chat Settings → RAG → Retrieval Mode
├── Focused Retrieval (RAG)  ← 推薦，只取最相關片段
└── Full Context Mode        ← 注入完整文件內容
```

---

## 實際使用範例

### 情境：建立「公司規範」知識庫

```
1. 收集公司規範文件（PDF/Word/TXT）
2. 上傳到 Knowledge →「公司規範」知識庫
3. 等待 Embedding 完成
4. 建立新模型「公司規範助手」
5. 在模型設定中綁定「公司規範」知識庫
6. 選擇「公司規範助手」模型，開始提問
7. 系統會自動從知識庫搜尋相關內容並回答
```

### 對話範例

```
使用者：「請告訴我公司的請假規定」

Open WebUI 自動：
1. 搜尋「公司規範」知識庫
2. 找到請假相關段落
3. 將相關內容 + 問題送給 LLM
4. LLM 基於知識庫內容回答：
   「根據公司規範第3章，員工每年享有5天有薪病假，
   需提前2天申請...」
```

---

## 常見問題與排除

### Q1：Embedding 處理很慢

**原因**：文件太大或數量太多，Embedding Model 處理時間長。

**解決**：
- 減少單次上傳的文件數量
- 使用更快的 Embedding Model（如 nomic-embed-text）
- 確保有足够的 RAM（建議 16GB+）

### Q2：搜尋結果不準確

**可能原因**：
- Chunk Size 設定不當
- Embedding Model 不支援中文
- 文件內容格式不正確

**解決**：
- 調整 Chunk Size 和 Overlap
- 使用支援多語言的 Embedding Model（如 bge-m3）
- 預先檢查文件格式是否正確

### Q3：系統無法啟動（Too many open files）

**原因**：文件切片太多，導致文件描述符耗盡。

**解決**：
```bash
# Docker 啟動時加上
--ulimit nofile=65536:65536

# 或在 docker-compose.yml 中
services:
  open-webui:
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
```

### Q4：Full Context Mode vs RAG 該選哪個？

| 考慮因素 | Focused Retrieval (RAG) | Full Context Mode |
|----------|------------------------|-------------------|
| 文件大小 | 適合大型知識庫 | 適合單一文件 |
| 精度 | 取最相關片段 | 完整上下文 |
| 速度 | 較快 | 較慢 |
| Token 消耗 | 較少 | 較多 |

### Q5：知識庫綁定後回答仍然不正確

**可能原因**：
- Embedding 處理尚未完成
- 文件內容與問題不相關
- 模型能力不足以理解檢索內容

**解決**：
- 確認 Embedding 處理已完成
- 檢查上傳的文件內容是否包含相關資訊
- 嘗試調整 Top K 參數，增加或減少檢索數量

### Q6：支援哪些語言的 Embedding？

| Embedding Model | 英文 | 中文 | 多語言 |
|-----------------|------|------|--------|
| nomic-embed-text | ✅ | ⚠️ 一般 | ❌ |
| bge-m3 | ✅ | ✅ 良好 | ✅ |
| text-embedding-3-small | ✅ 良好 | ⚠️ 一般 | ❌ |

**建議**：如果需要中文支援，優先使用 **bge-m3**。

---

## 快速檢查清單

### 設定前

- [ ] 已安裝並啟動 Open WebUI
- [ ] 已安裝並啟動 Embedding Model（bge-m3 或 nomic-embed-text）
- [ ] 已安裝並啟動 LLM Model

### 設定中

- [ ] 在 Ollama 環境變數中設定 EMBEDDING_MODELS
- [ ] 建立知識庫並上傳文件
- [ ] 等待 Embedding 處理完成
- [ ] 為模型綁定知識庫

### 測試

- [ ] 選擇綁定知識庫的模型
- [ ] 提問與知識庫相關的問題
- [ ] 驗證回答是否正確引用知識庫內容

---

## 架構總覽

```
┌─────────────────────────────────────────────────────────┐
│                    Open WebUI                             │
├──────────────┬──────────────────────────────────────────┤
│  User Chat   │  Knowledge Base Manager                   │
│  (聊天界面)   │  (知識庫管理)                              │
└──────┬───────┴──────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│              RAG Engine（檢索引擎）                       │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐   │
│  │ Query Embed  │  │ Vector Search│  │ Chunk Split │   │
│  │ (問題向量化)  │  │ (向量搜尋)    │  │ (文本分塊)   │   │
│  └──────────────┘  └──────────────┘  └─────────────┘   │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌─────────────────┐         ┌──────────────────┐
│  Embedding Model │         │  LLM Model       │
│  (bge-m3/nomic)  │         │  (llama3/gpt-4o) │
└─────────────────┘         └──────────────────┘
        │                             │
        └────────────┬────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Response（生成回答）                         │
└─────────────────────────────────────────────────────────┘
```

---

## 相關資源

- **官方 Knowledge 文件**：https://docs.openwebui.com/features/workspace/knowledge/
- **官方 RAG 文件**：https://docs.openwebui.com/features/chat-conversations/rag/
- **RAG 疑難排解**：https://docs.openwebui.com/troubleshooting/rag/
- **中文教程**：https://openwebui-doc-zh.pages.dev/tutorials/tips/rag-tutorial/
- **Ollama Embedding 模型**：https://ollama.com/library/bge-m3

---

**最後更新**：2026-08-05  
**作者**：Hermes Agent 整理  
**原始專案**：[Open WebUI](https://github.com/open-webui/open-webui)
