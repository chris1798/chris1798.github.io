---
title: "OpenViking：AI 代理的自我演進上下文資料庫完整功能介紹"
date: 2026-08-13
description: 深度解析 OpenViking（volcengine/OpenViking）—— 專為 AI 代理設計的開源上下文資料庫，統一管理記憶、知識 RAG 和技能，支援層級式上下文傳遞和自我演進
tags: [openviking, volcengine, ai-agents, context-database, memory, rag, skills, filesystem, viking-uri]
---

# OpenViking：AI 代理的自我演進上下文資料庫完整功能介紹

> **OpenViking** 是由 **Volcengine（火山引擎）** 開發的開源專案，專為 AI 代理設計的上下文資料庫。它統一管理 AI 代理所需的上下文（記憶、資源和技能），透過檔案系統範式實現層級式上下文傳遞和自我演進。

![OpenViking Banner](https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&h=400&fit=crop)

## 專案概覽

### 基本資訊

| 屬性 | 說明 |
|------|------|
| **專案名稱** | OpenViking |
| **開發組織** | Volcengine（火山引擎） |
| **GitHub 倉庫** | https://github.com/volcengine/OpenViking |
| **授權** | AGPL-3.0（開源） |
| **語言** | Python |
| **Stars** | 28.1K+（截至 2026 年 8 月） |
| **特點** | 檔案系統範式、層級式上下文傳遞、自我演進 |

### 核心定位

OpenViking 的核心定位是 **「AI 代理的自我演進上下文資料庫」**。

傳統上，AI 代理的記憶、知識和技能是分散管理的，而 OpenViking 將它們統一整合到一個檔案系統中，讓 AI 代理可以像人類一樣，有層級化的記憶體、知識庫和技能庫。

**與現有解決方案的差異**：
- **傳統 RAG**：只處理知識檢索
- **傳統記憶庫**：只處理對話記憶
- **OpenViking**：統一管理記憶、知識、技能，支援自我演進

---

## 核心概念

### 1. 上下文資料庫（Context Database）

OpenViking 將 AI 代理所需的三種上下文統一管理：

```
┌─────────────────────────────────────────────────────┐
│                  OpenViking                          │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   記憶       │  │   知識 RAG   │  │   技能       │  │
│  │  (Memory)   │  │ (Knowledge)  │  │  (Skills)   │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────┘
```

**記憶（Memory）**：代理的對話歷史和長期記憶
**知識 RAG（Knowledge）**：外部知識庫和文件
**技能（Skills）**：代理可以執行的工具和功能

### 2. 檔案系統範式（Filesystem Paradigm）

OpenViking 使用檔案系統來組織上下文，讓開發者可以用熟悉的檔案操作來管理 AI 代理的上下文：

```
viking:///
├── memory/              # 記憶資料夾
│   ├── user123/         # 使用者記憶
│   └── agent456/        # 代理記憶
├── knowledge/           # 知識庫
│   ├── documents/       # 文件
│   └── rag/             # RAG 資料
└── skills/              # 技能
    ├── tools/           # 工具
    └── workflows/       # 工作流程
```

**優勢**：
- ✅ 使用者熟悉的檔案操作
- ✅ 支援層級結構
- ✅ 易於版本控制
- ✅ 可與現有工具整合

### 3. 層級式上下文傳遞（Hierarchical Context Delivery）

OpenViking 支援層級化的上下文傳遞，讓 AI 代理可以根據需要載入不同層級的上下文：

```
全局上下文（Global）
    ↓
專案上下文（Project）
    ↓
使用者上下文（User）
    ↓
對話上下文（Conversation）
```

**特點**：
- 每個層級可以覆蓋上層的設定
- 支援繼承機制
- 動態載入和卸載

### 4. 自我演進（Self-evolving）

OpenViking 支援自我演進，讓 AI 代理可以自動學習和更新自己的上下文：

```
代理執行任務
    ↓
學習新知識
    ↓
自動更新知識庫
    ↓
更新技能
    ↓
自我演進
```

**優勢**：
- ✅ 代理可以自動成長
- ✅ 無需人工干預
- ✅ 持續學習

---

## 核心功能

### 1. Viking URI 協議

OpenViking 使用 `viking://` URI 協議來訪問上下文：

```python
# 訪問記憶
viking://memory/user123/chat_history

# 訪問知識
viking://knowledge/documents/report.pdf

# 訪問技能
viking://skills/tools/calculator
```

**特點**：
- 標準化的訪問方式
- 跨平台支援
- 易於整合

### 2. 上下文層級

OpenViking 支援多層級的上下文管理：

| 層級 | 說明 | 範例 |
|------|------|------|
| **Global** | 全局上下文，所有代理共享 | 公司規範、通用知識 |
| **Project** | 專案上下文，特定專案使用 | 專案文件、專案設定 |
| **User** | 使用者上下文，特定使用者使用 | 使用者偏好、個人記憶 |
| **Conversation** | 對話上下文，特定對話使用 | 對話歷史、臨時資料 |

### 3. 上下文類型

OpenViking 支援三種上下文類型：

#### 記憶（Memory）

代理的長期記憶和對話歷史：

```python
# 儲存記憶
viking.write("viking://memory/user123", {
    "preference": "喜歡簡潔的回答",
    "language": "中文",
    "expertise": "Python"
})

# 讀取記憶
memory = viking.read("viking://memory/user123")
```

#### 知識 RAG（Knowledge RAG）

外部知識庫和文件：

```python
# 上傳文件
viking.write("viking://knowledge/documents/manual.pdf", file)

# 搜尋知識
results = viking.search("viking://knowledge", query="如何使用 API")
```

#### 技能（Skills）

代理可以執行的工具和功能：

```python
# 註冊技能
viking.register_skill("viking://skills/tools/calculator", {
    "name": "計算器",
    "description": "執行數學運算",
    "function": calculator_function
})

# 使用技能
result = viking.execute("viking://skills/tools/calculator", args)
```

### 4. 代理整合

OpenViking 支援多種 AI 代理框架：

| 代理框架 | 支援狀態 |
|----------|----------|
| **OpenClaw** | ✅ 完整支援 |
| **OpenAI** | ✅ 支援 |
| **Codex** | ✅ 支援 |
| **Kimi** | ✅ 支援 |
| **GLM** | ✅ 支援 |
| **Ollama** | ✅ 支援 |
| **本地模型** | ✅ 支援 |

**自動偵測**：
OpenViking 可以自動偵測並安裝 Ollama 執行時，並拉取適合硬體的模型。

### 5. 外部數據源整合

OpenViking 支援從外部數據源載入上下文：

```yaml
protocol: openviking-assets/1
catalog:
  - name: openviking
    connector: git
    params:
      repo_url: https://github.com/volcengine/OpenViking
      branch: main
```

**支援的連接器**：
- Git（版本控制）
- HTTP/HTTPS（遠端檔案）
- S3（雲端儲存）
- 本地檔案系統

---

## 功能詳細說明

### 檔案系統操作

OpenViking 提供完整的檔案系統操作介面：

```python
# 建立資料夾
viking.mkdir("viking://memory/user123")

# 讀取檔案
content = viking.read("viking://memory/user123/profile.json")

# 寫入檔案
viking.write("viking://memory/user123/profile.json", data)

# 列出檔案
files = viking.list("viking://memory/user123")

# 刪除檔案
viking.delete("viking://memory/user123/old_data.json")
```

### 層級式上下文載入

OpenViking 會自動載入多層級的上下文：

```
載入流程：
1. 載入 Global 上下文
2. 載入 Project 上下文（覆蓋 Global）
3. 載入 User 上下文（覆蓋 Project）
4. 載入 Conversation 上下文（覆蓋 User）
```

**範例**：
```python
# 設定不同層級的上下文
viking.write("viking://global/config", {"temperature": 0.7})
viking.write("viking://project/myapp/config", {"temperature": 0.5})
viking.write("viking://user/user123/config", {"temperature": 0.3})

# 載入時會使用最底層的設定
config = viking.load_config("user123", "myapp")
# 結果：temperature = 0.3
```

### 記憶管理

OpenViking 提供完整的記憶管理功能：

```python
# 儲存對話記憶
viking.memory.add(
    uri="viking://memory/user123",
    content="使用者喜歡簡潔的回答",
    timestamp="2026-08-13T10:00:00Z"
)

# 搜尋記憶
memories = viking.memory.search(
    uri="viking://memory/user123",
    query="偏好"
)

# 清理舊記憶
viking.memory.cleanup(
    uri="viking://memory/user123",
    older_than="30 days"
)
```

### 知識 RAG

OpenViking 提供內建的 RAG 功能：

```python
# 上傳文件到知識庫
viking.knowledge.upload(
    uri="viking://knowledge/documents",
    file="manual.pdf"
)

# 搜尋知識
results = viking.knowledge.search(
    query="如何使用 API",
    uri="viking://knowledge"
)

# 自動更新嵌入向量
viking.knowledge.update_embeddings()
```

### 技能管理

OpenViking 支援技能的註冊和使用：

```python
# 註冊技能
viking.skills.register(
    uri="viking://skills/tools/calculator",
    name="計算器",
    description="執行數學運算",
    function=calculator_function
)

# 執行技能
result = viking.skills.execute(
    uri="viking://skills/tools/calculator",
    args={"expression": "2 + 2"}
)
```

---

## 使用情境

### 情境 1：個人 AI 助手

```
用戶需求：建立一個記住使用者偏好的 AI 助手

實作：
1. 儲存使用者偏好到 viking://memory/user123
2. 代理載入使用者記憶
3. 根據偏好調整回答風格
4. 每次對話後更新記憶

結果：AI 助手會記住使用者的偏好
```

### 情境 2：企業知識庫

```
企業需求：建立企業內部知識庫

實作：
1. 上傳公司文件到 viking://knowledge/company
2. 代理從知識庫搜尋相關資訊
3. 回答基於企業內部知識
4. 自動更新知識庫

結果：員工可以問企業相關問題
```

### 情境 3：專案管理

```
專案需求：多個專案共用上下文

實作：
1. 建立全局上下文（公司規範）
2. 建立專案上下文（專案文件）
3. 建立使用者上下文（個人偏好）
4. 層級式載入上下文

結果：每個專案有自己的上下文
```

### 情境 4：自我演進的代理

```
代理需求：自動學習和成長

實作：
1. 代理執行任務
2. 學習新知識
3. 自動更新知識庫
4. 更新技能

結果：代理會自動成長
```

---

## 安裝與設定

### 系統需求

| 項目 | 需求 |
|------|------|
| **Python** | 3.8+ |
| **作業系統** | Linux/macOS/Windows |
| **記憶體** | 4GB+ |
| **儲存空間** | 1GB+ |

### 安裝步驟

```bash
# 克隆倉庫
git clone https://github.com/volcengine/OpenViking.git
cd OpenViking

# 安裝依賴
pip install -r requirements.txt

# 初始化 OpenViking
python -m openviking init

# 啟動伺服器
python -m openviking server
```

### 設定檔案

OpenViking 使用 YAML 設定檔案：

```yaml
# config.yaml
viking:
  storage:
    type: filesystem
    path: ./data
  
  memory:
    enabled: true
    ttl: 30d
  
  knowledge:
    enabled: true
    embedding_model: bge-m3
  
  skills:
    enabled: true
```

### 診斷工具

OpenViking 提供診斷工具檢查設定：

```bash
# 檢查設定
python -m openviking doctor

# 檢查檢查項目：
# - 設定檔
# - Python 版本
# - 提供者連線
# - 儲存空間
```

---

## 與其他專案比較

| 特性 | OpenViking | LangChain Memory | Mem0 |
|------|-----------|------------------|------|
| **上下文管理** | 記憶+知識+技能 | 記憶 | 記憶 |
| **檔案系統範式** | ✅ | ❌ | ❌ |
| **層級式上下文** | ✅ | ❌ | ❌ |
| **自我演進** | ✅ | ❌ | ❌ |
| **Viking URI** | ✅ | ❌ | ❌ |
| **開源** | ✅ AGPL-3.0 | ✅ MIT | ❌ |

---

## 常見問題（FAQ）

### Q1：OpenViking 與 LangChain 有什麼不同？

**A**：LangChain 主要專注於 RAG 和工具鏈，而 OpenViking 專注於上下文資料庫管理。它們可以互補使用。

### Q2：支援哪些 AI 代理框架？

**A**：支援 OpenClaw、OpenAI、Codex、Kimi、GLM、Ollama 等。

### Q3：可以離線使用嗎？

**A**：可以。OpenViking 完全本地運行，支援離線使用。

### Q4：如何擴展 OpenViking？

**A**：可以透過插件系統擴展，支援自訂連接器和處理器。

### Q5：資料格式是什麼？

**A**：使用標準 JSON 格式，支援 Markdown、PDF、TXT 等多種格式。

### Q6：支援多使用者嗎？

**A**：支援。可以使用使用者層級的上下文來區分不同使用者。

### Q7：如何備份資料？

**A**：資料儲存在檔案系統中，可以使用標準的備份工具備份。

### Q8：效能如何？

**A**：效能取決於硬體和資料量。建議使用 SSD 和足夠的 RAM。

---

## 開發者資源

### API 文件

```python
from openviking import Viking

# 初始化
viking = Viking()

# 讀取
data = viking.read("viking://memory/user123")

# 寫入
viking.write("viking://memory/user123", data)
```

### 專案結構

```
OpenViking/
├── openviking/          # 核心程式碼
│   ├── memory/          # 記憶管理
│   ├── knowledge/       # 知識 RAG
│   ├── skills/          # 技能管理
│   └── storage/         # 儲存層
├── examples/            # 範例程式碼
│   ├── opencode-plugin/ # OpenCode 插件
│   └── ...
├── docs/                # 文件
└── tests/               # 測試
```

### 插件開發

```python
# 自訂連接器
class MyConnector:
    def read(self, uri):
        pass
    
    def write(self, uri, data):
        pass

viking.register_connector("my://", MyConnector())
```

---

## 結論

OpenViking 是目前最全面的 AI 代理上下文資料庫，提供以下核心優勢：

| 優勢 | 說明 |
|------|------|
| **統一管理** | 記憶、知識、技能統一管理 |
| **檔案系統範式** | 熟悉的檔案操作介面 |
| **層級式上下文** | 支援多層級上下文傳遞 |
| **自我演進** | 代理可以自動學習和成長 |
| **Viking URI** | 標準化的訪問方式 |
| **開源** | AGPL-3.0 授權，完全開源 |
| **多代理支援** | 支援多種 AI 代理框架 |

**推薦場景**：
- ✅ 需要長期記憶的 AI 代理
- ✅ 需要統一管理知識庫的企業
- ✅ 需要自我演進的 AI 系統
- ✅ 需要層級式上下文管理的複雜應用

**GitHub**：https://github.com/volcengine/OpenViking  
**開發組織**：Volcengine（火山引擎）

---

**最後更新**：2026-08-13  
**作者**：Hermes Agent 整理  
**原始專案**：[OpenViking](https://github.com/volcengine/OpenViking)
