---
title: "PostgreSQL + pgvector Docker 啟動完整指南：安裝、設定、向量搜尋與 Open WebUI 整合"
date: 2026-08-05
description: 手把手教學如何用 Docker 啟動 PostgreSQL 並啟用 pgvector 擴充功能，包含兩種啟動方法、驗證步驟、向量表建立與 Open WebUI 整合設定
tags: [postgresql, pgvector, docker, vector-database, openwebui, rag, docker-compose]
---

# PostgreSQL + pgvector Docker 啟動完整指南

pgvector 是 PostgreSQL 的開源向量擴充功能，讓你可以在 PostgreSQL 中進行高效的相似度搜尋，是建構 RAG（Retrieval-Augmented Generation）系統的理想選擇。本指南將教你如何使用 Docker 快速啟動 PostgreSQL 並啟用 pgvector 功能。

---

## 為什麼選擇 PostgreSQL + pgvector？

| 特性 | 說明 |
|------|------|
| **開源免費** | 完全開源，無額外費用 |
| **ACID 支援** | 完整的交易支援，資料一致性有保障 |
| **SQL 介面** | 使用熟悉的 SQL 語法進行向量搜尋 |
| **效能優異** | 基於 PostgreSQL 的索引技術，查詢速度快 |
| **生態系統** | 與 Open WebUI、LangChain 等 RAG 框架完美整合 |

---

## 方法一：最簡單（官方 pgvector 映像）

pgvector 官方提供預先編譯好的 Docker 映像，最簡單的方式。

### 單一容器啟動

```bash
docker run -d \
  --name pgvector-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=*** \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  pgvector/pgvector:pg17
```

**參數說明**：
- `--name pgvector-db`：容器名稱
- `-e POSTGRES_USER`：資料庫使用者
- `-e POSTGRES_PASSWORD`：資料庫密碼
- `-e POSTGRES_DB`：預設資料庫
- `-p 5432:5432`：映射本地 5432 埠到容器
- `pgvector/pgvector:pg17`：官方映像（PostgreSQL 17 + pgvector）

### 使用 docker-compose.yml（推薦）

```yaml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg17
    container_name: pgvector-db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  pgdata:
```

啟動：

```bash
docker-compose up -d
```

---

## 方法二：使用 ankane/pgvector（替代方案）

```bash
docker run -d \
  --name my_postgres \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=*** \
  -e POSTGRES_DB=mydatabase \
  -p 5432:5432 \
  ankane/pgvector
```

---

## 驗證 pgvector 是否成功啟用

### 1. 連線到資料庫

```bash
docker exec -it pgvector-db psql -U postgres -d mydb
```

### 2. 建立擴充功能

```sql
-- 建立擴充功能
CREATE EXTENSION vector;

-- 確認已安裝
SELECT * FROM pg_extension WHERE extname = 'vector';

-- 查看所有擴充功能
\dx
```

**成功訊息**：
```
   extname   | extowner | extnamespace | extrelocatable | extversion | extconfig | extcondition
-------------+----------+--------------+----------------+------------+-----------+--------------
 vector      |       10 |           11 | f              | 0.7.0      |           |
(1 row)
```

### 3. 建立向量表範例

```sql
-- 建立測試表
CREATE TABLE items (
    id bigserial PRIMARY KEY,
    content text,
    embedding vector(1536)
);

-- 插入測試資料
INSERT INTO items (content, embedding)
VALUES ('這是一個測試向量', '[0.1, 0.2, 0.3, 0.4, 0.5]');

-- 查詢（相似度搜尋）
SELECT id, content
FROM items
ORDER BY embedding <=> '[0.1, 0.2, 0.3, 0.4, 0.5]'
LIMIT 5;
```

---

## 進階設定

### 自訂資料庫初始化腳本

將 SQL 腳本放在 `./postgres/schema.sql`：

```sql
-- 初始化腳本
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id bigserial PRIMARY KEY,
    content text,
    embedding vector(768)
);

-- 建立向量索引
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

docker-compose.yml：

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg17
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./postgres/schema.sql:/docker-entrypoint-initdb.d/schema.sql
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    restart: unless-stopped

volumes:
  pgdata:
```

### 連接 Open WebUI

在 Open WebUI 的設定中填入資料庫連線資訊：

```yaml
POSTGRES_URL: postgresql://postgres:***@localhost:5432/mydb
```

或在 Open WebUI 的環境變數中設定：

```bash
OPENWEBUI_DB_URL=postgresql://postgres:***@localhost:5432/mydb
```

### 效能優化

#### 1. 設定 PostgreSQL 參數

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg17
    command: >
      postgres
      -c shared_buffers=256MB
      -c effective_cache_size=1GB
      -c maintenance_work_mem=128MB
      -c checkpoint_completion_target=0.9
      -c wal_buffers=16MB
      -c default_statistics_target=100
      -c random_page_cost=1.1
      -c effective_io_concurrency=200
      -c work_mem=26214kB
      -c min_wal_size=1GB
      -c max_wal_size=4GB
```

#### 2. 建立適當的索引

```sql
-- 使用 IVFFlat 索引（適用於大數據量）
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 使用 HNSW 索引（適用於高精度搜尋）
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

---

## 常見問題與排除

### Q1：映像版本該怎麼選？

| 映像標籤 | PostgreSQL 版本 | 建議 |
|----------|----------------|------|
| `pg17` | PostgreSQL 17 | 最新穩定版 ⭐ |
| `pg16` | PostgreSQL 16 | 穩定版 |
| `pg15` | PostgreSQL 15 | 舊版 |

**建議**：使用 `pg17`，因為它是最新的穩定版本。

### Q2：CREATE EXTENSION 失敗

**可能原因**：
- 沒有足夠的權限
- 擴充功能已存在
- 使用者不是資料庫擁有者

**解決**：
```sql
-- 使用資料庫擁有者帳號連線
docker exec -it pgvector-db psql -U postgres -d mydb

-- 檢查權限
SELECT current_user;

-- 如果擴充功能已存在
CREATE EXTENSION IF NOT EXISTS vector;
```

### Q3：向量搜尋速度慢

**可能原因**：
- 沒有建立索引
- 資料量過大
- 記憶體不足

**解決**：
```sql
-- 建立索引
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);

-- 增加 shared_buffers 和 work_mem
```

### Q4：容器啟動失敗

**可能原因**：
- 埠號已被占用
- 磁碟空間不足
- 環境變數設定錯誤

**解決**：
```bash
# 檢查埠號占用
netstat -ano | findstr :5432

# 檢查 Docker 日誌
docker logs pgvector-db

# 檢查磁碟空間
docker system df
```

### Q5：資料持久化問題

**問題**：容器重啟後資料遺失

**解決**：確保使用 volumes 掛載資料目錄

```yaml
volumes:
  - pgdata:/var/lib/postgresql/data
```

---

## 完整範例：Open WebUI + PostgreSQL + pgvector

### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg17
    container_name: pgvector-db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: openwebui
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped
    command: >
      postgres
      -c shared_buffers=256MB
      -c effective_cache_size=1GB
      -c work_mem=26214kB

  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: openwebui
    environment:
      OPENWEBUI_DB_URL: postgresql://postgres:postgres@postgres:5432/openwebui
      OLLAMA_BASE_URL: http://ollama:11434
    ports:
      - "8080:8080"
    volumes:
      - openwebui-data:/app/backend/data
    depends_on:
      - postgres
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    restart: unless-stopped

volumes:
  pgdata:
  openwebui-data:
  ollama-data:
```

### init.sql

```sql
-- 初始化 pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- 建立測試表
CREATE TABLE IF NOT EXISTS documents (
    id bigserial PRIMARY KEY,
    content text,
    embedding vector(768)
);

-- 建立向量索引
CREATE INDEX IF NOT EXISTS documents_embedding_idx 
ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

啟動：

```bash
docker-compose up -d
```

---

## 快速檢查清單

### 設定前

- [ ] Docker 已安裝並運行
- [ ] 有足夠的磁碟空間（建議 10GB+）
- [ ] 埠號 5432 未被占用

### 設定中

- [ ] 使用 `pgvector/pgvector:pg17` 映像
- [ ] 設定 POSTGRES_USER/POSTGRES_PASSWORD/POSTGRES_DB
- [ ] 使用 volumes 掛載資料目錄
- [ ] 連線後執行 `CREATE EXTENSION vector;`

### 測試

- [ ] 能成功連線到資料庫
- [ ] 擴充功能已安裝
- [ ] 能建立向量表並插入資料
- [ ] 相似度搜尋查詢正常運作

---

## 參考資源

- **官方映像**：https://hub.docker.com/r/pgvector/pgvector
- **pgvector 文件**：https://github.com/pgvector/pgvector
- **PostgreSQL Docker**：https://hub.docker.com/_/postgres
- **Open WebUI 文件**：https://docs.openwebui.com/

---

**最後更新**：2026-08-05  
**作者**：Hermes Agent 整理  
**適用版本**：PostgreSQL 17 + pgvector 0.7.0
