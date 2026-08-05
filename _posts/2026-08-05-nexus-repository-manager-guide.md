---
title: "Nexus Repository Manager 功能說明與使用指南"
date: 2026-08-05
description: Sonatype Nexus Repository Manager 的完整功能介紹、核心概念、安裝方式與實作範例。
tags: [DevOps, Nexus, Repository, Maven, Docker, CI/CD]
---

# Nexus Repository Manager 功能說明與使用指南

## 什麼是 Nexus Repository？

[Nexus Repository Manager](https://www.sonatype.com/products/sonatype-nexus-repository) 是由 Sonatype 開發的**統一軟體倉儲管理器**，用於集中管理團隊或組織的軟體套件（packages/artifacts）。它可以作為代理（proxy）快取公共倉庫、託管（host）內部開發的產物，並將兩者組合為一組（group），讓開發工具透過單一 URL 取得所需套件。

Nexus 支援高達 **18 種套件格式**，涵蓋：

| 類別 | 支援格式 |
|------|----------|
| Java / JVM | Maven (maven2), Bower, npm, NuGet |
| 容器 | Docker |
| Linux | APT (Debian/Ubuntu), YUM (RHEL/CentOS) |
| 腳本語言 | PyPI (Python), Go (gopkg, gomod), RubyGems, Composer (PHP), Packagist |
| 基礎設施 | Helm (Kubernetes), Terraform, Conan (C++), Vagrant, CocoaPods |
| 通用 | Generic (任意二進制檔案) |
| 其他 | R (CRAN), Cargo (Rust) |

---

## 核心概念

### 三種倉庫類型

Nexus 有三種基本的倉庫類型，它們各自有不同的用途：

#### 1. Hosted Repository（託管倉庫）

用於存放**團隊自行開發或構建**的套件。例如：

- 公司內部開發的 Java 函式庫 JAR
- 構建完成的 Docker 影像
- 發布的 npm 套件

Hosted 倉庫支援三種部署策略：

| 策略 | 說明 |
|------|------|
| **Disabled** | 僅允許下載，禁止上傳（用於第三方套件快取） |
| **Allow Redeploy** | 允許覆蓋同名套件（開發環境常用） |
| **Docker** | 專門用於 Docker 影像的 Hosted 倉庫 |

#### 2. Proxy Repository（代理倉庫）

作為公共倉庫的**本地快取代理**。當開發者的構建工具請求套件時：

1. Nexus 先檢查本地快取是否有
2. 若有命中，直接返回（極快）
3. 若沒有，從上游倉庫下載後快取，再返回給開發者

優點：
- **加快構建速度** — 避免重複從網路下載
- **節省頻寬** — 多人共用同一份快取
- **離線可用** — 上游倉庫不可達時仍可安裝已快取的套件
- **降低外部依賴風險** — 公共倉庫掛了也不怕

常見的上游倉庫包括：
- `https://repo1.maven.org/maven2/` (Maven Central)
- `https://registry.npmjs.org/` (npm)
- `https://pypi.org/` (PyPI)
- `https://hub.docker.com/` (Docker Hub)
- `https://pkgs.dev.azure.com/` (NuGet)

#### 3. Group Repository（群組倉庫）

將多個 Hosted 和 Proxy 倉庫**合併為一個邏輯 URL**，讓開發工具只需指向一個地址就能取得所有套件。

典型組合：
```
Group URL → 包含
├── Hosted: 公司內部套件
├── Proxy: Maven Central
├── Proxy: npmjs
└── Proxy: Docker Hub
```

---

## 架構元件

### Blob Store（儲存區）

Nexus 將所有套件以**原始二進制檔案**存放在 Blob Store 中，而不是關係型資料庫。每個 Blob Store 對應一個本機目錄。

- **預設 Blob Store**：安裝後自動建立，命名為 `default`
- **自訂 Blob Store**：可為不同格式或大小需求建立獨立的 Blob Store
- **磁碟管理**：支援設定容量上限與清理政策（Cleanup Policy）

### 索引（Index）

Nexus 為每個倉庫維護索引，讓搜尋和解析依賴時能快速定位套件。

- 可選擇**本地索引**（本地建立索引表）或**遠端索引**（快取上游倉庫的索引）
- 索引更新可設定排程（如每小時同步）

### 安全與權限

- **角色-based 存取控制**：預設角色包括 `nx-admin`（系統管理員）、`nx-anonymous`（匿名使用者）等
- **使用者管理**：支援建立本地使用者或整合 LDAP / SAML
- **倉庫權限**：可為不同角色設定讀取或寫入權限
- **API Key**：支援產生 API Key 讓 CI/CD 工具認證

---

## 安裝方式

### 方式一：Docker（推薦快速上手）

```bash
# 建立持久化資料目錄
mkdir -p /opt/nexus/data
chown -R 200:200 /opt/nexus/data

# 啟動 Nexus
docker run -d \
  --name nexus \
  --restart unless-stopped \
  -p 8081:8081 \
  -p 8082:8082 \   # Docker hosted registry
  -p 8083:8083 \   # Docker proxy registry
  -v /opt/nexus/data:/nexus-data \
  -e INSTALL4J_ADD_VM_PARAMS="-Xms1g -Xmx2g" \
  sonatype/nexus3:latest
```

### 方式二：Docker Compose

```yaml
version: '3.8'
services:
  nexus:
    image: sonatype/nexus3:latest
    container_name: nexus
    ports:
      - "8081:8081"   # Web UI
      - "8082:8082"   # Docker hosted
      - "8083:8083"   # Docker proxy
    volumes:
      - nexus-data:/nexus-data
    environment:
      INSTALL4J_ADD_VM_PARAMS: "-Xms1g -Xmx2g -XX:MaxDirectMemorySize=2g"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8081/service/rest/v1/status"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 120s

volumes:
  nexus-data:
```

```bash
docker-compose up -d
```

### 方式三：Linux 原生安裝

```bash
# 下載
wget https://download.sonatype.com/nexus/3/latest-unix.tar.gz

# 解壓
sudo tar -xzvf latest-unix.tar.gz -C /opt/
sudo ln -s /opt/nexus-3.x.x /opt/nexus

# 建立使用者
sudo useradd --system --create-home --shell /bin/bash nexus
sudo chown -R nexus:nexus /opt/nexus
sudo chown -R nexus:nexus /opt/sonatype-work

# 啟動
sudo -u nexus /opt/nexus/bin/nexus run
```

### 方式四：Windows

1. 下載 Windows Installer (.exe)
2. 執行安裝程式，選擇安裝路徑
3. 安裝完成後從 Windows 服務啟動 `NexusRepository`
4. 預設存取 `http://localhost:8081`

---

## 初始設定

### 1. 取得初始管理員密碼

```bash
docker exec nexus cat /nexus-data/admin.password
```

將顯示的密碼貼到登入頁面的密碼欄位。

### 2. 設定管理員密碼

登入後會要求設定新的 `admin` 密碼。

### 3. 建立倉庫範例

#### 建立 Maven Proxy（快取 Maven Central）

1. 進入 **Admin → Repositories → Create repository → maven2 (proxy)**
2. 命名：`maven-central`
3. Remote URL：`https://repo1.maven.org/maven2/`
4. 儲存

#### 建立 Maven Hosted（存放公司套件）

1. **Admin → Repositories → Create repository → maven2 (hosted)**
2. 命名：`company-releases`
3. Deployment policy 選 `Allow Redeploy`
4. 儲存

#### 建立 Group（統一入口）

1. **Admin → Repositories → Create repository → maven2 (group)**
2. 命名：`maven-all`
3. 將 `company-releases` 和 `maven-central` 加入 Members
4. 儲存

### 4. 取得 Group URL

```
http://localhost:8081/repository/maven-all/
```

---

## 搭配構建工具使用

### Maven（settings.xml）

```xml
<settings>
  <mirrors>
    <mirror>
      <id>nexus</id>
      <mirrorOf>*</mirrorOf>
      <url>http://localhost:8081/repository/maven-all/</url>
    </mirror>
  </mirrors>
</settings>
```

### Gradle（build.gradle）

```groovy
repositories {
    maven {
        url "http://localhost:8081/repository/maven-all/"
    }
}
```

### npm (.npmrc)

```
registry=http://localhost:8081/repository/npm-group/
//localhost:8081/repository/company-npm/:_authToken=YOUR_TOKEN
```

### Docker

```bash
# 登入 Nexus Docker registry
docker login localhost:8082

# 標記影像
docker tag myapp:latest localhost:8082/company-docker/myapp:latest

# 推送
docker push localhost:8082/company-docker/myapp:latest
```

### APT (Debian/Ubuntu)

```
deb [trusted=yes] http://localhost:8081/repository/apt-group/ ./
```

### YUM (RHEL/CentOS)

```ini
[nexus]
name=Nexus Repository
baseurl=http://localhost:8081/repository/yum-group/
enabled=1
gpgcheck=0
```

---

## 進階功能

### 清理政策（Cleanup Policy）

自動清理過時或不再使用的套件，節省磁碟空間：

- **Maven**：移除已不屬於任何專案的 JAR
- **npm**：移除超過 N 天未被下載的套件
- **Docker**：移除超過 N 天未被 pull 的影像層

### 安全掃描（Pro 版）

Nexus Repository Pro 內建安全掃描：

- 自動掃描上傳套件的已知漏洞（CVE）
- 建立白名單（Allow List）禁止有高危漏洞的套件
- 與 OWASP Dependency-Check 整合

### 遠端主機檢查（RHC）

Pro 版功能，自動檢查倉庫中套件的舊版本，提醒開發者升級。

### 高可用性（Pro 版）

- 主從備援（Active-Active 或 Active-Standby）
- 自動故障轉移

### API 與自動化

Nexus 提供完整的 REST API，可用於：

- 程式化建立/管理倉庫
- 上傳/下載套件
- 管理使用者與權限
- CI/CD 整合（Jenkins、GitLab CI、GitHub Actions）

---

## 常見管理任務

### 備份

```bash
# 備份資料目錄
tar -czvf nexus-backup-$(date +%Y%m%d).tar.gz /opt/nexus/data/

# 排程每日備份（crontab）
0 2 * * * tar -czf /backup/nexus-backup-$(date +\%Y\%m\%d).tar.gz /opt/nexus/data/
```

### 監控狀態

透過 Health API 檢查：

```bash
curl -s http://localhost:8081/service/rest/v1/status
```

回傳 JSON：
```json
{"status":"green"}
```

### 更新版本

```bash
# Docker 環境
docker pull sonatype/nexus3:latest
docker stop nexus
docker rm nexus
# 重新執行 docker run 指令（保持相同 volume 和 ports）
```

---

## 總結

| 功能 | 說明 |
|------|------|
| 套件格式支援 | 18 種，涵蓋 Java、容器、Linux、腳本語言等 |
| 倉庫類型 | Hosted、Proxy、Group 三種基本類型 |
| 部署方式 | Docker、Docker Compose、Linux、Windows |
| 安全管理 | 角色權限、API Key、LDAP/SAML 整合 |
| 自動清理 | Cleanup Policy 管理磁碟空間 |
| 安全掃描 | Pro 版內建 CVE 掃描 |
| 高可用性 | Pro 版支援 Active-Active 備援 |
| API 整合 | 完整 REST API，支援 CI/CD 自動化 |

Nexus Repository Manager 是 DevOps 工具鏈中不可或缺的一環，能有效提升團隊的構建效率、降低外部依賴風險，並簡化套件管理流程。無論是小型團隊還是大型企業，都能從中獲得實質的效益。
