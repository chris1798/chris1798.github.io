---
title: "DB 查詢 Skill 設計指南：DB2 + MS SQL Server 連線、語法與 Prompt 撰寫"
date: 2026-08-18
description: 如何為 AI Agent 建立資料庫查詢 Skill，涵蓋 DB2 和 MS SQL Server 的連線方式、語法差異、常見陷阱與完整 SKILL.md 範例
tags: [db-query, db2, mssql, sql-server, ai-agent, skill-design, prompt-engineering]
---

# DB 查詢 Skill 設計指南：DB2 + MS SQL Server 連線、語法與 Prompt 撰寫

> 本文說明如何為 AI Agent（如 Hermes Agent）建立一個 **資料庫查詢 Skill**，涵蓋 DB2 和 MS SQL Server 的連線方式、SQL 語法差異、常見陷阱，以及完整的 SKILL.md 設計範例。

![Database Query](https://images.unsplash.com/photo-1544383835-bda2bc66a35d?w=1200&h=400&fit=crop)

## 為什麼需要 DB 查詢 Skill？

AI Agent 在處理值班日誌、資料分析、報表生成等任務時，經常需要查詢資料庫。但 **DB2 和 MS SQL Server 的語法差異很大**，用錯會直接報錯：

| 操作 | DB2 | MS SQL Server |
|------|-----|---------------|
| 限制行數 | `FETCH FIRST n ROWS ONLY` | `SELECT TOP n` |
| 識別符引號 | `"column"` | `[column]` |
| NULL 處理 | `COALESCE()` | `ISNULL()` 或 `COALESCE()` |
| 字串拼接 | `\|\|` 或 `CONCAT()` | `+`（注意 NULL） |
| 日期格式化 | `CHAR(date, 'YYYY-MM-DD')` | `FORMAT(date, 'yyyy-MM-dd')` |

沒有 Skill 引導，Agent 很容易混用語法導致查詢失敗。

---

## 📁 Skill 目錄結構

```
db-query/
├── SKILL.md              # 主文件（觸發條件 + 工作流程）
└── references/
    ├── db2.md            # DB2 連線、語法、陷阱
    └── mssql.md          # MS SQL Server 連線、語法、陷阱
```

採用 **progressive disclosure**（漸進式揭露）：
- SKILL.md 保持精簡（<500 行），只放通用工作流程
- DB2 和 MSSQL 的細節放 references，Agent 只載入需要的資料庫文件
- 避免 context 膨脹

---

## 📄 SKILL.md（主文件）

```markdown
---
name: db-query
description: "查詢 DB2 或 MS SQL Server 資料庫。當使用者提到查資料、跑 SQL、DB2、SQL Server、
  查表結構、執行查詢、統計資料、export CSV 時觸發。即使使用者只說『帮我查一下某某表的資料』
  而沒有明確說出資料庫類型，也應該載入此 skill 來確認連線方式和語法差異。"
---

# DB Query — DB2 & MS SQL Server

## 觸發條件

- 使用者要求查詢、統計、export 資料庫資料
- 提到 DB2、SQL Server、MSSQL、查表、跑 SQL
- 需要比較兩套系統的資料
- 值班日誌中提到 DB 相關問題需要排查

## 工作流程

### Step 1: 確認目標資料庫

詢問或判斷使用者要查的是 **DB2** 還是 **MS SQL Server**。
如果不确定，先問。兩者語法和連線方式差異很大，用錯會直接報錯。

### Step 2: 載入對應 reference

- DB2 → 讀取 `references/db2.md`
- MS SQL Server → 讀取 `references/mssql.md`

### Step 3: 建立連線

使用 terminal tool 執行連線命令（見各 reference 的連線章節）。
**永遠不要** 在 skill 或對話中硬編碼密碼。使用環境變數或連線字串檔。

### Step 4: 探索結構（首次查詢時）

在寫 SELECT 之前，先確認表結構：
- DB2: `db2 "DESCRIBE TABLE schema.table_name"`
- MSSQL: `SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'xxx'`

這避免猜錯欄位名導致查詢失敗。

### Step 5: 執行查詢

- 預設加 `LIMIT`（DB2）或 `TOP`（MSSQL）限制回傳行數，避免一次拉太多
- 大表查詢先 `COUNT(*)` 確認規模
- 結果超過 100 列時，考慮 export 到 CSV 而非直接顯示

### Step 6: 呈現結果

- 少量資料（<20 列）：直接在對話中用表格展示
- 大量資料：export 到 CSV/JSON 檔案，告知路徑
- 統計類：用簡潔的數字 + 趨勢說明

## 安全守則

1. **唯讀優先**：預設只執行 SELECT。任何 INSERT/UPDATE/DELETE/DROP 必須先向使用者確認
2. **不洩漏密碼**：連線字串中的密碼不顯示在輸出中
3. **LIMIT 保護**：大表查詢必須加 LIMIT/TOP，避免拖垮生產 DB
4. **敏感資料脫敏**：如果結果包含個資（電話、身分證號），主動提醒使用者

## 常見陷阱對照表

| 陷阱 | DB2 | MSSQL |
|------|-----|-------|
| 引號 | 識別符用 `"`，字串用 `'` | 識別符用 `[]`，字串用 `'` |
| LIMIT | `FETCH FIRST n ROWS ONLY` | `SELECT TOP n` |
| NULL 處理 | `COALESCE()` | `ISNULL()` 或 `COALESCE()` |
| 日期格式 | `TIMESTAMP('2026-01-01')` | `CAST('2026-01-01' AS DATE)` |
| 布林值 | 無原生 BOOLEAN，用 SMALLINT | BIT 類型 |
| 字串拼接 | `\|\|` 或 `CONCAT()` | `+`（NULL + x = NULL） |

## 多 DB 比較場景

如果需要同時查 DB2 和 MSSQL 做資料比對：
1. 分別連線執行查詢
2. 各自 export 到 CSV
3. 用 Python (pandas) 做 join/compare
4. 呈現差異報告
```

---

## 📄 references/db2.md（DB2 參考）

### 連線方式

#### 本地 CLI（db2cmd）

```bash
# 使用環境變數（推薦）
export DB2INSTANCE=db2inst1
db2 connect to MYDB user db2admin password $DB2_PASSWORD

# 或一行式
db2 "SELECT * FROM employees FETCH FIRST 10 ROWS ONLY"
```

#### Python (ibm_db)

```python
import ibm_db

conn_str = (
    "DATABASE=mydb;"
    "HOSTNAME=db-server.internal;"
    "PORT=50000;"
    "PROTOCOL=TCPIP;"
    "UID=db2admin;"
    "PWD={password};"  # 從環境變數讀取
    "ATTR_AUTH_SERVER=***
)
conn = ibm_db.connect(conn_str, "", "")
stmt = ibm_db.executescript(conn, "SELECT * FROM employees")
```

#### 連線參數速查

| 參數 | 說明 | 範例 |
|------|------|------|
| DATABASE | 資料庫名稱（alias） | MYDB |
| HOSTNAME | 伺服器 IP/hostname | db-server.internal |
| PORT | 埠號（預設 50000） | 50000 |
| UID / PWD | 使用者/密碼 | db2admin / *** |
| PROTOCOL | TCPIP | TCPIP |

### 常用查詢語法

#### 查表結構

```sql
-- 列出所有表
SELECT TABNAME, TABTYPE FROM SYSCAT.TABLES WHERE TABSCHEMA = 'MYSCHEMA';

-- 描述特定表
DESCRIBE TABLE MYSCHEMA.EMPLOYEES;

-- 或用 catalog view
SELECT COLNAME, TYPENAME, LENGTH, NULLS
FROM SYSCAT.COLUMNS
WHERE TABSCHEMA = 'MYSCHEMA' AND TABNAME = 'EMPLOYEES';
```

#### SELECT 基本語法

```sql
-- LIMIT（DB2 不用 LIMIT，用 FETCH FIRST）
SELECT * FROM employees FETCH FIRST 10 ROWS ONLY;

-- ORDER BY + LIMIT
SELECT * FROM orders
ORDER BY order_date DESC
FETCH FIRST 50 ROWS ONLY;

-- OFFSET（跳過前 N 列）
SELECT * FROM employees
ORDER BY employee_id
OFFSET 100 ROWS FETCH NEXT 20 ROWS ONLY;
```

#### 日期函數

```sql
-- 目前日期
SELECT CURRENT DATE, CURRENT TIMESTAMP FROM SYSIBM.SYSDUMMY1;

-- 日期運算
SELECT order_date + 7 DAYS FROM orders;

-- 格式化
SELECT CHAR(order_date, 'YYYY-MM-DD') FROM orders;

-- 月份差
SELECT MONTHS_BETWEEN(CURRENT DATE, hire_date) / 12 AS years FROM employees;
```

#### 聚合與分組

```sql
SELECT department, COUNT(*) as headcount, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING COUNT(*) > 5
ORDER BY headcount DESC;
```

### DB2 常見陷阱

| 問題 | 說明 |
|------|------|
| **FETCH FIRST vs LIMIT** | DB2 不支援 `LIMIT`，必須用 `FETCH FIRST n ROWS ONLY` |
| **識別符引號** | 用雙引號 `"column"`，不是方括號 `[column]`（那是 MSSQL） |
| **NULL 比較** | `IS NULL` / `IS NOT NULL`，不能用 `= NULL` |
| **字串拼接** | 用 `\|\|` 或 `CONCAT()`，不用 `+` |
| **布林值** | 無原生 BOOLEAN，用 SMALLINT (0/1) |
| **分號結尾** | db2 CLI 中 SQL 不需要分號；ibm_db 也不需要 |

### Export 到 CSV

```bash
# db2 CLI export
db2 "EXPORT TO employees.csv OF DEL MODIFIED BY CHARDATA=1386 \
    SELECT * FROM MYSCHEMA.EMPLOYEES"
```

```python
# Python
import ibm_db, csv
stmt = ibm_db.executescript(conn, "SELECT * FROM employees")
with open('employees.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow([d['name'] for d in ibm_db.fetch_both(stmt)])
    while row := ibm_db.fetch_row(stmt):
        writer.writerow(row)
```

---

## 📄 references/mssql.md（MS SQL Server 參考）

### 連線方式

#### sqlcmd（CLI）

```bash
# Windows
sqlcmd -S db-server\INSTANCE -d MyDB -U sa -P $SQL_PASSWORD -Q "SELECT * FROM employees"

# 或使用連線字串檔（避免密碼在 command line 洩漏）
sqlcmd -S db-server\INSTANCE -d MyDB -i query.sql

# Linux (ODBC)
sqlcmd -S tcp:db-server,1433 -d MyDB -U sa -P $SQL_PASSWORD
```

#### Python (pyodbc)

```python
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=db-server\\INSTANCE;"
    "DATABASE=MyDB;"
    "UID=sa;"
    "PWD={password};"  # 從環境變數讀取
    "TrustServerCertificate=yes;"
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM employees")
rows = cursor.fetchall()
```

#### Python (pymssql) — 輕量替代

```python
import pymssql

conn = pymssql.connect(
    server='db-server',
    port='1433',
    user='sa',
    password=os.environ['SQL_PASSWORD'],
    database='MyDB',
    charset='utf8'
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM employees")
```

#### 連線參數速查

| 參數 | 說明 | 範例 |
|------|------|------|
| SERVER | hostname\instance 或 IP,Port | db-server\\SQLEXPRESS |
| DATABASE | 資料庫名稱 | MyDB |
| UID / PWD | 使用者/密碼 | sa / *** |
| PORT | 預設 1433 | 1433 |
| DRIVER | ODBC driver | ODBC Driver 18 for SQL Server |

### 常用查詢語法

#### 查表結構

```sql
-- 列出所有表
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';

-- 描述特定表
SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'employees'
ORDER BY ORDINAL_POSITION;

-- 或用 sp_columns（較簡潔）
EXEC sp_columns @table_name = 'employees', @table_owner = 'dbo';
```

#### SELECT 基本語法

```sql
-- TOP（MSSQL 不用 LIMIT，用 TOP）
SELECT TOP 10 * FROM employees;

-- ORDER BY + TOP（注意：TOP 要在 ORDER BY 之前）
SELECT TOP 50 * FROM orders ORDER BY order_date DESC;

-- OFFSET/FETCH（SQL Server 2012+）
SELECT * FROM employees
ORDER BY employee_id
OFFSET 100 ROWS FETCH NEXT 20 ROWS ONLY;
```

#### 日期函數

```sql
-- 目前日期
SELECT GETDATE(), SYSDATETIME();

-- 日期運算
SELECT DATEADD(DAY, 7, order_date) FROM orders;

-- 格式化
SELECT FORMAT(order_date, 'yyyy-MM-dd') FROM orders;

-- 月份差
SELECT DATEDIFF(MONTH, hire_date, GETDATE()) / 12 AS years FROM employees;

-- 昨天
SELECT CAST(GETDATE() - 1 AS DATE);
```

#### 特殊函數

```sql
-- ISNULL（MSSQL 專用，COALESCE 也可用）
SELECT ISNULL(phone, 'N/A') FROM employees;

-- STRING_AGG（SQL Server 2017+）
SELECT department, STRING_AGG(name, ', ') WITHIN GROUP (ORDER BY name)
FROM employees GROUP BY department;

-- IIF（三元運算）
SELECT IIF(status = 1, 'Active', 'Inactive') FROM employees;

-- 動態 SQL
EXEC sp_executesql N'SELECT * FROM employees WHERE department = @dept',
    N'@dept NVARCHAR(50)', @dept = 'Engineering';
```

### MSSQL 常見陷阱

| 問題 | 說明 |
|------|------|
| **TOP vs LIMIT** | MSSQL 用 `SELECT TOP n`，不用 `LIMIT`。`OFFSET/FETCH` 需要 `ORDER BY` |
| **識別符引號** | 用方括號 `[column]`，不是雙引號（除非 SET QUOTED_IDENTIFIER ON） |
| **字串拼接** | 用 `+`，但 NULL + anything = NULL，要用 `ISNULL()` 包起來 |
| **日期比較** | `GETDATE()` 含時間部分，比對純日期用 `CAST(GETDATE() AS DATE)` |
| **布林值** | BIT 類型 (0/1)，沒有 TRUE/FALSE 關鍵字（雖然可接受） |
| **分號結尾** | sqlcmd 中 SQL 需要分號；pyodbc execute 不需要 |
| **Instance name** | 連線時 `hostname\INSTANCE`，命名實例不能漏 |
| **混合運算** | INT + FLOAT = FLOAT，注意隱性轉換 |

### Export 到 CSV

```bash
# bcp（較快，適合大表）
bcp "SELECT * FROM MyDB.dbo.employees" queryout employees.csv \
    -S db-server -U sa -P $SQL_PASSWORD -c -t","
```

```python
# Python
import pyodbc, csv
cursor.execute("SELECT * FROM employees")
with open('employees.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([desc[0] for desc in cursor.description])
    writer.writerows(cursor.fetchall())
```

---

## 🎯 設計重點說明

| 設計決策 | 理由 |
|----------|------|
| **SKILL.md + references 分離** | DB2 和 MSSQL 語法差異大，分開載入避免 context 膨脹 |
| **description 寫得「pushy」** | 使用者可能只說「查一下資料」而沒提 DB 類型，要確保觸發 |
| **Step 3 強調不硬編碼密碼** | 安全守則，環境變數或連線字串檔 |
| **Step 4 先探索結構** | 避免猜錯欄位名，這是 DB 查詢最常見的失敗原因 |
| **LIMIT/TOP 保護** | 生產 DB 不能一次拉百萬列 |
| **陷阱對照表** | DB2 vs MSSQL 的語法差異是最容易出錯的地方 |
| **export CSV 流程** | 大結果集不適合在對話中顯示 |

---

## 🔑 Prompt 設計原則

### 1. description 要涵蓋模糊觸發

使用者可能只說「查一下資料」而沒提 DB 類型。description 要包含：
- 明確關鍵字：DB2、SQL Server、MSSQL、跑 SQL、查表
- 模糊場景：「帮我查一下某某表的資料」
- 進階場景：比較兩套系統、值班日誌排查

### 2. 先問再查

不确定哪個 DB 就先問，不要猜。DB2 和 MSSQL 的語法混用會直接報錯。

### 3. 結構先行

每次新表先 `DESCRIBE`（DB2）或 `INFORMATION_SCHEMA`（MSSQL），避免猜錯欄位名。

### 4. 安全預設

- 唯讀優先（SELECT only）
- LIMIT/TOP 保護
- 不顯示密碼
- 敏感資料脫敏提醒

### 5. 語法差異明確列出

DB2 的 `FETCH FIRST` vs MSSQL 的 `TOP` 是最常踩的坑，對照表要放在 SKILL.md 主文件中。

---

## 📋 完整檢查清單

建立 DB 查詢 Skill 前確認：

| 項目 | 狀態 |
|------|------|
| ✅ 確定目標資料庫類型（DB2 / MSSQL / 兩者） | |
| ✅ 連線方式已測試（CLI + Python） | |
| ✅ 密碼用環境變數，不硬編碼 | |
| ✅ 表結構探索命令已驗證 | |
| ✅ LIMIT/TOP 保護機制 | |
| ✅ Export CSV 流程已測試 | |
| ✅ 陷阱對照表完整 | |
| ✅ description 涵蓋模糊觸發場景 | |

---

## 💡 進階應用

| 場景 | 實現方式 |
|------|----------|
| **值班日誌自動排查** | 日誌提到 DB 錯誤 → Skill 自動連線查 log/monitor 表 |
| **跨系統資料比對** | DB2 + MSSQL 各自 export → pandas join → 差異報告 |
| **定期報表** | Cron job 每天跑固定查詢 → export CSV → 發 Telegram |
| **Schema 變更追蹤** | 定期 dump INFORMATION_SCHEMA → git diff → 通知變更 |

---

## 總結

| 要素 | 重點 |
|------|------|
| **目錄結構** | SKILL.md（通用流程）+ references/db2.md + references/mssql.md |
| **觸發設計** | description 要 pushy，涵蓋模糊場景 |
| **工作流程** | 確認 DB → 載入 reference → 連線 → 探索結構 → 查詢 → 呈現 |
| **安全守則** | 唯讀、LIMIT、不洩漏密碼、脫敏 |
| **語法差異** | FETCH FIRST vs TOP、引號、NULL 處理、日期函數 |

**一句話總結**：DB 查詢 Skill 的核心是「先確認哪個 DB、再載入對應語法參考、永遠先探索結構再寫查詢」。

---

**最後更新**：2026-08-18  
**作者**：Hermes Agent 整理  
**適用平台**：Hermes Agent、Claude Code、Codex 等支援 Skill 系統的 AI Agent
