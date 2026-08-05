---
title: "Oracle 11g Data Guard 物理備份資料庫建置完整指南：步驟、注意事項與故障排除"
date: 2026-08-05
description: 手把手教學如何建置 Oracle 11g Data Guard 物理備份資料庫，包含前置準備、RMAN 備份、Active Duplicate、Log Transport、保護模式、Switchover 與 Failover
tags: [oracle, data-guard, standby, rman, database-recovery, high-availability]
---

# Oracle 11g Data Guard 物理備份資料庫建置完整指南

Data Guard 是 Oracle 的備份資料庫解決方案，用於災難復原（Disaster Recovery）和高可用性（High Availability）。本指南將完整說明如何建置 Oracle 11g 物理備份資料庫。

![Oracle Data Guard](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Oracle_Data_Guard.svg/1200px-Oracle_Data_Guard.svg.png)

---

## 架構概述

```
┌─────────────────────────┐         網路          ┌─────────────────────────┐
│       Primary DB        │  ◄── Redo Log ──►    │      Standby DB         │
│     (主資料庫)            │    (Archive Log)     │    (備份資料庫)          │
│                         │                        │                         │
│  - 讀寫操作              │                        │  - 只讀（Active Data Guard）│
│  - 產生 Redo Log         │                        │  - 自動應用 Redo        │
│  - 產生 Archive Log      │                        │  - 支援 Switchover       │
└─────────────────────────┘                        └─────────────────────────┘
```

### 保護模式（Protection Modes）

| 模式 | 說明 | 資料安全性 | 效能 |
|------|------|-----------|------|
| **Maximum Performance**（預設） | ASYNC 傳輸，不等待 Standby 確認 | 中 | 最高 |
| **Maximum Availability** | SYNC 傳輸，等待 Standby 確認 | 高 | 中 |
| **Maximum Protection** | SYNC 傳輸，Standby 確認後才提交 | 最高 | 最低 |

---

## 前置準備

### 1.1 環境需求

| 項目 | Primary Server | Standby Server |
|------|---------------|----------------|
| **作業系統** | Linux/Windows | 相同版本 |
| **Oracle 版本** | 11.2.0.x | 相同版本 |
| **Oracle Home** | /u01/app/oracle/product/11.2.0/dbhome_1 | 相同路徑 |
| **DB_NAME** | DB11G | DB11G（必須相同） |
| **DB_UNIQUE_NAME** | DB11G | DB11G_STBY（必須不同） |
| **安裝狀態** | 已安裝並運行 | 僅安裝軟體（Software Only） |

### 1.2 網路需求

- Primary 和 Standby 之間可以互相 ping 通
- 1521 端口開放
- TNS 配置正確

### 1.3 磁碟空間

- Standby 需要與 Primary 相同大小的磁碟空間
- 包含所有 datafile、redo log、archivelog

---

## 建置步驟

### Step 1：Primary Server 設定

#### 1.1 啟用 Archivelog 模式

```sql
-- 檢查當前模式
SELECT log_mode FROM v$database;

-- 如果顯示 NOARCHIVELOG，切換為 ARCHIVELOG
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
ALTER DATABASE ARCHIVELOG;
ALTER DATABASE OPEN;

-- 驗證
SELECT log_mode FROM v$database;
-- 預期結果：ARCHIVELOG
```

#### 1.2 啟用 Forced Logging

```sql
ALTER DATABASE FORCE LOGGING;
```

#### 1.3 設定 Initialization Parameters

```sql
-- 設定 LOG_ARCHIVE_CONFIG
ALTER SYSTEM SET LOG_ARCHIVE_CONFIG='DG_CONFIG=(DB11G,DB11G_STBY)' SCOPE=BOTH;

-- 設定 LOG_ARCHIVE_DEST_2（Primary 發送 redo 到 Standby）
ALTER SYSTEM SET LOG_ARCHIVE_DEST_2='SERVICE=db11g_stby ASYNC VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=DB11G_STBY' SCOPE=BOTH;

-- 設定 LOG_ARCHIVE_DEST_STATE_2
ALTER SYSTEM SET LOG_ARCHIVE_DEST_STATE_2=ENABLE SCOPE=BOTH;

-- 設定 LOG_ARCHIVE_FORMAT
ALTER SYSTEM SET LOG_ARCHIVE_FORMAT='%t_%s_%r.arc' SCOPE=SPFILE;

-- 設定 LOG_ARCHIVE_MAX_PROCESSES
ALTER SYSTEM SET LOG_ARCHIVE_MAX_PROCESSES=30 SCOPE=SPFILE;

-- 設定 REMOTE_LOGIN_PASSWORDFILE
ALTER SYSTEM SET REMOTE_LOGIN_PASSWORDFILE=EXCLUSIVE SCOPE=SPFILE;

-- 設定 DB_UNIQUE_NAME（如果尚未設定）
ALTER SYSTEM SET DB_UNIQUE_NAME='DB11G' SCOPE=BOTH;
```

#### 1.4 建立密碼檔案

```bash
# 在 Primary Server
orapwd file=$ORACLE_HOME/dbs/orapwDB11G password=your_password entries=10 force=Y
```

#### 1.5 建立 Standby Redo Log

```sql
-- 查看當前 Redo Log 配置
SELECT GROUP#, THREAD#, SEQUENCE#, BYTES, MEMBERS FROM v$log;

-- 建立 Standby Redo Log（數量 = Redo Log 組數 + 1）
ALTER DATABASE ADD STANDBY LOGFILE GROUP 4 ('/u01/app/oracle/oradata/DB11G/sredo04.log') SIZE 50M;
ALTER DATABASE ADD STANDBY LOGFILE GROUP 5 ('/u01/app/oracle/oradata/DB11G/sredo05.log') SIZE 50M;
ALTER DATABASE ADD STANDBY LOGFILE GROUP 6 ('/u01/app/oracle/oradata/DB11G/sredo06.log') SIZE 50M;
ALTER DATABASE ADD STANDBY LOGFILE GROUP 7 ('/u01/app/oracle/oradata/DB11G/sredo07.log') SIZE 50M;
```

#### 1.6 建立 PFILE

```sql
-- 從 SPFILE 建立 PFILE
CREATE PFILE='/tmp/pfile_db11g.ora' FROM SPFILE;
```

#### 1.7 設定 Listener 和 TNS

```bash
# listener.ora
LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = primary_host)(PORT = 1521))
      (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
    )
  )

# tnsnames.ora
DB11G =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = primary_host)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = DB11G)
    )
  )

DB11G_STBY =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = standby_host)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = DB11G_STBY)
    )
  )
```

### Step 2：Standby Server 設定

#### 2.1 建立目錄結構

```bash
# 建立與 Primary 相同的目錄結構
mkdir -p /u01/app/oracle/oradata/DB11G
mkdir -p /u01/app/oracle/fast_recovery_area/DB11G
mkdir -p /u01/app/oracle/admin/DB11G/adump
```

#### 2.2 設定 Listener 和 TNS

```bash
# listener.ora
LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = standby_host)(PORT = 1521))
      (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
    )
  )

SID_LIST_LISTENER =
  (SID_LIST =
    (SID_DESC =
      (GLOBAL_DBNAME = DB11G_STBY)
      (ORACLE_HOME = /u01/app/oracle/product/11.2.0/dbhome_1)
      (SID_NAME = DB11G_STBY)
    )
  )

# tnsnames.ora
DB11G =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = primary_host)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = DB11G)
    )
  )

DB11G_STBY =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = standby_host)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = DB11G_STBY)
    )
  )
```

#### 2.3 建立密碼檔案

```bash
orapwd file=$ORACLE_HOME/dbs/orapwDB11G_STBY password=your_password entries=10 force=Y
```

#### 2.4 建立 PFILE

```bash
# 將 Primary 的 PFILE 複製到 Standby
scp /tmp/pfile_db11g.ora standby_host:/tmp/

# 編輯 PFILE，修改以下參數
vi /tmp/pfile_db11g.ora

# 修改以下行：
db_unique_name='DB11G_STBY'
log_archive_config='DG_CONFIG=(DB11G,DB11G_STBY)'
log_archive_dest_1='LOCATION=/u01/app/oracle/fast_recovery_area/DB11G/valid_for=(all_logfiles,all_roles) db_unique_name=DB11G_STBY'
log_archive_dest_2='SERVICE=db11g ASYNC VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=DB11G'
fal_server='DB11G'
standby_file_management='AUTO'
```

### Step 3：建立備份資料庫

#### 3.1 方法一：Active Duplicate（推薦，11gR2+）

```bash
# 在 Standby Server
export ORACLE_SID=DB11G_STBY
sqlplus / as sysdba

# 啟動到 nomount
STARTUP NOMOUNT PFILE='/tmp/pfile_db11g.ora';

# 使用 RMAN Active Duplicate
rman target sys/your_password@DB11G auxiliary sys/your_password@DB11G_STBY

RMAN> DUPLICATE TARGET DATABASE FOR STANDBY FROM ACTIVE DATABASE DORECOVER
  SPFILE SET "db_unique_name"="DB11G_STBY"
  SET "log_archive_config"="DG_CONFIG=(DB11G,DB11G_STBY)"
  SET "log_archive_dest_2"="SERVICE=db11g ASYNC VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=DB11G"
  SET "fal_server"="DB11G"
  SET "standby_file_management"="AUTO"
  NOFILENAMECHECK;
```

#### 3.2 方法二：Backup-based Duplicate（備份還原）

```bash
# 在 Primary Server 建立備份
RMAN> BACKUP DATABASE FORMAT='/tmp/backup/%U';
RMAN> BACKUP CURRENT CONTROLFILE FOR STANDBY FORMAT='/tmp/backup/controlfile.ctl';
RMAN> BACKUP ARCHIVELOG ALL FORMAT='/tmp/backup/archive_%U';

# 複製備份到 Standby
scp -r /tmp/backup/ standby_host:/tmp/

# 在 Standby Server 還原
rman target /

RMAN> RESTORE STANDBY CONTROLFILE FROM '/tmp/backup/controlfile.ctl';
RMAN> ALTER DATABASE MOUNT STANDBY DATABASE;
RMAN> RESTORE DATABASE;
RMAN> RECOVER STANDBY DATABASE;
```

### Step 4：啟動 Redo Apply

```bash
# 在 Standby Server
sqlplus / as sysdba

-- 啟動 Redo Apply
ALTER DATABASE RECOVER MANAGED STANDBY DATABASE DISCONNECT FROM SESSION;

-- 驗證
SELECT PROCESS, STATUS, THREAD#, SEQUENCE# FROM v$managed_standby;

-- 預期結果：
-- PROCESS   STATUS       THREAD#  SEQUENCE#
-- --------- ------------ -------- ----------
-- ARCH      CONNECTED    0        0
-- ARCH      CONNECTED    0        0
-- MRPO      WAIT_FOR_LOG 1        123
```

### Step 5：驗證 Data Guard 狀態

```bash
# 在 Primary Server
sqlplus / as sysdba

-- 檢查 Data Guard 狀態
SELECT DEST_NAME, STATUS, ERROR FROM v$archive_dest WHERE dest_id=2;

-- 檢查 Archivelog 傳輸
SELECT NAME, SEQUENCE#, APPLIED FROM v$archived_log ORDER BY SEQUENCE#;

-- 檢查 Standby 狀態
SELECT NAME, OPEN_MODE, DATABASE_ROLE, SWITCHOVER_STATUS FROM v$database;
```

---

## 保護模式設定

### Maximum Performance（預設）

```sql
-- Primary Server
ALTER SYSTEM SET LOG_ARCHIVE_DEST_2='SERVICE=db11g_stby ASYNC VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=DB11G_STBY' SCOPE=BOTH;
```

### Maximum Availability

```sql
-- Primary Server
ALTER SYSTEM SET LOG_ARCHIVE_DEST_2='SERVICE=db11g_stby SYNC AFFIRM VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=DB11G_STBY' SCOPE=BOTH;

-- 設定 Data Guard Protection Mode
ALTER SYSTEM SET DG_BROKER_START=TRUE SCOPE=BOTH;
```

### Maximum Protection

```sql
-- Primary Server
ALTER SYSTEM SET LOG_ARCHIVE_DEST_2='SERVICE=db11g_stby SYNC AFFIRM VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=DB11G_STBY' SCOPE=BOTH;

-- 切換 Protection Mode
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
ALTER DATABASE SET STANDBY DATABASE TO MAXIMIZE PROTECTION;
ALTER DATABASE OPEN;
```

---

## Switchover 和 Failover

### Switchover（計劃性切換）

```bash
# 在 Primary Server
sqlplus / as sysdba

-- 檢查 Switchover 狀態
SELECT SWITCHOVER_STATUS FROM v$database;
-- 預期結果：TO STANDBY 或 SESSIONS ACTIVE

-- 執行 Switchover
ALTER DATABASE COMMIT TO SWITCHOVER TO PHYSICAL STANDBY WITH SESSION SHUTDOWN;

-- 重啟 Primary（現在是 Standby）
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
ALTER DATABASE RECOVER MANAGED STANDBY DATABASE DISCONNECT FROM SESSION;
```

```bash
# 在 Standby Server（現在是 Primary）
sqlplus / as sysdba

-- 切換為 Primary
ALTER DATABASE COMMIT TO SWITCHOVER TO PRIMARY WITH SESSION SHUTDOWN;

-- 打開資料庫
ALTER DATABASE OPEN;
```

### Failover（緊急切換）

```bash
# 在 Standby Server
sqlplus / as sysdba

-- 檢查是否有未應用的 Redo
SELECT MAX(SEQUENCE#) FROM v$archived_log WHERE APPLIED='NO';

-- 應用所有可用的 Redo
ALTER DATABASE RECOVER MANAGED STANDBY DATABASE FINISH FORCE;

-- 切換為 Primary
ALTER DATABASE COMMIT TO SWITCHOVER TO PRIMARY;

-- 打開資料庫
ALTER DATABASE OPEN;
```

---

## Active Data Guard（只讀備份）

Active Data Guard 允許在備份資料庫上執行只讀查詢，同時持續應用 Redo Log。

```sql
-- 停止 Redo Apply
ALTER DATABASE RECOVER MANAGED STANDBY DATABASE CANCEL;

-- 打開為只讀
ALTER DATABASE OPEN READ ONLY;

-- 驗證
SELECT OPEN_MODE FROM v$database;
-- 預期結果：READ ONLY

-- 啟動 Redo Apply（在只讀模式下）
ALTER DATABASE RECOVER MANAGED STANDBY DATABASE DISCONNECT FROM SESSION;
```

---

## Flashback Database

Flashback Database 允許快速將備份資料庫恢復到之前的狀態。

```sql
-- 啟用 Flashback
ALTER DATABASE FLASHBACK ON;

-- 設定 Flashback Retention Target
ALTER SYSTEM SET DB_FLASHBACK_RETENTION_TARGET=1440 SCOPE=BOTH;  -- 24 小時（分鐘）

-- 查看 Flashback 日誌
SELECT NAME, VALUE FROM v$parameter WHERE NAME LIKE 'db_flashback%';

-- 使用 Flashback 恢復（在 Switchover 失敗時）
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
FLASHBACK DATABASE TO TIMESTAMP TO_TIMESTAMP('2026-08-05 10:00:00', 'YYYY-MM-DD HH24:MI:SS');
ALTER DATABASE OPEN RESETLOGS;
```

---

## 注意事項與最佳實踐

### 5.1 重要注意事項

| 項目 | 說明 |
|------|------|
| **DB_NAME 必須相同** | Primary 和 Standby 的 DB_NAME 必須相同 |
| **DB_UNIQUE_NAME 必須不同** | Primary 和 Standby 的 DB_UNIQUE_NAME 必須不同 |
| **Oracle 版本必須相同** | Primary 和 Standby 的 Oracle 版本必須相同 |
| **作業系統必須相容** | 建議使用相同的作業系統版本 |
| **密碼檔案必須相同** | 兩端的密碼檔案必須相同（密碼、 entries） |
| **時區必須相同** | Primary 和 Standby 的時區必須相同 |

### 5.2 網路注意事項

- 確保 Primary 和 Standby 之間可以互相 ping 通
- 確保 1521 端口開放
- 建議使用專用的網路連結
- 考慮使用 VPN 或加密連結

### 5.3 磁碟空間注意事項

- Standby 需要與 Primary 相同大小的磁碟空間
- 確保有足够的空間存放 Archivelog
- 定期清理舊的 Archivelog
- 使用 Fast Recovery Area 管理 Archivelog

### 5.4 效能注意事項

- **Maximum Performance 模式**：使用 ASYNC 傳輸，效能影響最小
- **Maximum Availability 模式**：使用 SYNC 傳輸，效能影響中等
- **Maximum Protection 模式**：使用 SYNC 傳輸，效能影響最大
- 根據業務需求選擇適當的保護模式
- 定期監控 Redo Transport 延遲

### 5.5 監控注意事項

- 定期監控 Data Guard 狀態
- 監控 Archivelog 傳輸延遲
- 監控 Standby Redo Log 應用進度
- 設置警報當 Redo Transport 延遲超過閾值
- 定期測試 Switchover 和 Failover

### 5.6 安全性注意事項

- 使用強密碼保護密碼檔案
- 限制對 Data Guard 配置的管理訪問
- 啟用 Oracle Audit Vault 追蹤 Data Guard 操作
- 定期審查 Data Guard 配置

---

## 故障排除

### 6.1 常見問題

#### 問題 1：Archivelog 傳輸失敗

```bash
# 檢查 Log Transport 狀態
SELECT DEST_NAME, STATUS, ERROR FROM v$archive_dest WHERE dest_id=2;

# 檢查 Log Writer 進程
SELECT PROCESS, STATUS, THREAD#, SEQUENCE# FROM v$managed_standby;

# 解決方案：
-- 重啟 Log Transport
ALTER SYSTEM SET LOG_ARCHIVE_DEST_STATE_2=DEFER SCOPE=BOTH;
ALTER SYSTEM SET LOG_ARCHIVE_DEST_STATE_2=ENABLE SCOPE=BOTH;
```

#### 問題 2：Standby Redo Log 不足

```bash
# 檢查 Standby Redo Log
SELECT GROUP#, THREAD#, SEQUENCE#, BYTES, MEMBERS FROM v$standby_log;

# 解決方案：
-- 增加 Standby Redo Log（數量 = Redo Log 組數 + 1）
ALTER DATABASE ADD STANDBY LOGFILE GROUP 4 ('/u01/app/oracle/oradata/DB11G/sredo04.log') SIZE 50M;
ALTER DATABASE ADD STANDBY LOGFILE GROUP 5 ('/u01/app/oracle/oradata/DB11G/sredo05.log') SIZE 50M;
ALTER DATABASE ADD STANDBY LOGFILE GROUP 6 ('/u01/app/oracle/oradata/DB11G/sredo06.log') SIZE 50M;
ALTER DATABASE ADD STANDBY LOGFILE GROUP 7 ('/u01/app/oracle/oradata/DB11G/sredo07.log') SIZE 50M;
```

#### 問題 3：Redo Apply 停止

```bash
# 檢查 Redo Apply 狀態
SELECT PROCESS, STATUS, THREAD#, SEQUENCE# FROM v$managed_standby;

# 解決方案：
-- 重新啟動 Redo Apply
ALTER DATABASE RECOVER MANAGED STANDBY DATABASE CANCEL;
ALTER DATABASE RECOVER MANAGED STANDBY DATABASE DISCONNECT FROM SESSION;
```

### 6.2 診斷命令

```bash
# 檢查 Data Guard 配置
SELECT NAME, VALUE FROM v$parameter WHERE NAME LIKE '%dg%';

# 檢查 Archivelog 狀態
SELECT NAME, SEQUENCE#, APPLIED, COMPLETION_TIME FROM v$archived_log ORDER BY SEQUENCE#;

# 檢查 Redo Transport 延遲
SELECT NAME, VALUE FROM v$dataguard_stats WHERE NAME LIKE '%transport%latency%';

# 檢查保護模式
SELECT PROTECTION_MODE, PROTECTION_LEVEL FROM v$database;
```

---

## Data Guard Broker（可選）

Data Guard Broker 提供集中的 Data Guard 管理功能。

### 7.1 啟用 Broker

```sql
-- Primary Server
ALTER SYSTEM SET DG_BROKER_START=TRUE SCOPE=BOTH;

-- Standby Server
ALTER SYSTEM SET DG_BROKER_START=TRUE SCOPE=BOTH;
```

### 7.2 建立 Broker Configuration

```bash
# 在 Primary Server
dgmgrl sys/your_password@DB11G

DGMGRL> CREATE CONFIGURATION 'mydg_config' AS PRIMARY DATABASE IS 'DB11G' CONNECT IDENTIFIER IS DB11G;
DGMGRL> ADD DATABASE 'DB11G_STBY' AS CONNECT IDENTIFIER IS DB11G_STBY MAINTAINED AS PHYSICAL;
DGMGRL> ENABLE CONFIGURATION;
DGMGRL> SHOW CONFIGURATION;
```

### 7.3 Broker 管理操作

```bash
# 查看配置狀態
DGMGRL> SHOW CONFIGURATION VERBOSE;

# 執行 Switchover
DGMGRL> SWITCHOVER TO 'DB11G_STBY';

# 執行 Failover
DGMGRL> FAILOVER TO 'DB11G_STBY';

# 查看保護模式
DGMGRL> SHOW DATABASE VERBOSE 'DB11G';
```

---

## 完整設定檢查清單

### Primary Server

- [ ] 啟用 Archivelog 模式
- [ ] 啟用 Forced Logging
- [ ] 設定 LOG_ARCHIVE_CONFIG
- [ ] 設定 LOG_ARCHIVE_DEST_2
- [ ] 設定 LOG_ARCHIVE_DEST_STATE_2
- [ ] 設定 LOG_ARCHIVE_FORMAT
- [ ] 設定 LOG_ARCHIVE_MAX_PROCESSES
- [ ] 設定 REMOTE_LOGIN_PASSWORDFILE
- [ ] 設定 DB_UNIQUE_NAME
- [ ] 建立密碼檔案
- [ ] 建立 Standby Redo Log
- [ ] 建立 PFILE
- [ ] 設定 Listener 和 TNS

### Standby Server

- [ ] 建立目錄結構
- [ ] 設定 Listener 和 TNS
- [ ] 建立密碼檔案
- [ ] 建立/修改 PFILE
- [ ] 使用 RMAN Duplicate 建立備份資料庫
- [ ] 啟動 Redo Apply
- [ ] 驗證 Data Guard 狀態

### 測試

- [ ] 驗證 Archivelog 傳輸
- [ ] 驗證 Redo Apply
- [ ] 測試 Switchover
- [ ] 測試 Failover（可選）
- [ ] 設置監控警報

---

## 相關資源

- **Oracle Data Guard 官方文檔**: https://docs.oracle.com/en/database/oracle/oracle-database/11.2/sbydb/
- **ORACLE-BASE Data Guard 文章**: https://oracle-base.com/articles/11g/data-guard-setup-11gr2
- **Oracle Data Guard Broker**: https://docs.oracle.com/cd/E11882_01/server.112/e40776/broker.htm

---

**最後更新**: 2026-08-05  
**作者**: Hermes Agent 整理  
**原始資料來源**: Oracle 官方文檔、ORACLE-BASE
