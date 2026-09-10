---
title: "Redhat 9 安裝liteLLM SOP"
collection: teaching
type: "Linux"
permalink: /teaching/2026-09-07-redhat9-litellm-sop
date: 2026-09-07
tags: "Redhat,Linux,Docker,liteLLM"
---

# redhat 9 安裝litellm SOP:

## 檢查firewall
```bash
firewall-cmd --state
firewall-cmd --list-all
systemctl status firewalld
```

## 停用firewall
```
systemctl stop firewalld
```

## 停用開機自動啟動
```
systemctl disable firewalld
```

## 永久開放 4224 端口
```
firewall-cmd --permanent --add-port=4224/tcp
firewall-cmd --reload
```

## 檢查 nodejs 模組版本
```
dnf module list nodejs
```

## 將nodesjs版本指定至24版,並更新
```
dnf module reset nodejs -y
dnf module enable nodejs:24 -y
dnf update nodejs -y
```

## 安裝Podman-compose
```
dnf install python3-pip -y
pip3 install podman-compose
podman-compose --version
```

## 查詢「全域安裝」的套件 (Global)
```
npm list -g --depth=0
npm list -g @dbx-app/mcp-server@0.4.80
```
## 查詢「當前專案」安裝的套件 (Local)
```
npm list --depth=0
```
## 安裝@dbx-app/mcp-server至全域環境
```
npm install -g @dbx-app/mcp-server@0.4.80
npm install -g @dbx-app/cli
```
## 安裝dbx,並啟用MCP
```
cd /root/ai/dbx/
mkdir data
vi docker-compose.yml
```
```yaml
services:
  dbx:
    image: t8y2/dbx:latest
    pull_policy: always
    ports:
      - "4225:4224"
    volumes:
      - ./data:/app/data:z
    environment:
      - DBX_WEB_PASSWORD=1798
      - DBX_WEB_MCP_TOKEN=1798
      - DBX_WEB_MCP_ALLOWED_HOSTS=127.0.0.1:4225,host.docker.internal:4225,192.168.1.122:4225
      - DBX_WEB_MCP_ALLOWED_ORIGINS=http://127.0.0.1:4225,http://host.docker.internal:4225,http://192.168.1.122:4225
    restart: unless-stopped
```
## 啟用dbx MCP server --此段可bypass
```
npx @dbx-app/mcp-server
```
## 原生 Streamable HTTP --此段可bypass
```
vi start_dbx_mcp.sh
export DBX_MCP_HTTP_HOST=0.0.0.0
export DBX_MCP_HTTP_PORT=5225
export DBX_MCP_HTTP_TOKEN=sk-1234
export DBX_MCP_HTTP_ALLOW_REMOTE=1
export DBX_MCP_HTTP_ALLOWED_HOSTS=localhost:5225,127.0.0.1:5225,host.docker.internal:5225,192.168.1.122:5225
export DBX_MCP_HTTP_ALLOWED_ORIGINS="http://localhost:5225,http://127.0.0.1:5225,http://host.docker.internal:5225,http://192.168.1.122:5225"
npx -y @dbx-app/mcp-server --http --http-allow-remote
```
	
## 安裝litellm
```
cd /root/ai/litellm
curl -sSLO https://docs.litellm.ai/docker-compose.yml
cd /root/ai/litellm
mkdir postgres_data
```
```yaml
vi docker-compose.yml
services:
  litellm:
    image: docker.litellm.ai/berriai/litellm-database:latest
    ports:
      - "4000:4000"
    environment:
      LITELLM_MASTER_KEY: sk-1234
      LITELLM_SALT_KEY: sk-1234
      DATABASE_URL: postgresql://litellm:litellm@db:5432/litellm
      STORE_MODEL_IN_DB: "True"
    volumes:
      - ./config.yaml:/app/config.yaml:z
    extra_hosts:
      - "host.docker.internal:host-gateway"	  
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: litellm
      POSTGRES_PASSWORD: litellm
      POSTGRES_DB: litellm
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U litellm"]
      interval: 5s
      timeout: 5s
      retries: 10
    volumes:
      - ./postgres_data:/var/lib/postgresql/data:z	
```
## 啟動docker for litellm
```
podman-compose up -d
```
## 查log for litellm
```
podman logs -f litellm_litellm_1
```

## 安裝db2 docker
```
podman pull icr.io/db2_community/db2
podman run -d \
  --name db2server \
  --privileged=true \
  -e LICENSE=accept \
  -e DB2INSTANCE=db2inst1 \
  -e DB2INST1_PASSWORD=Passw0rd \
  -e DBNAME=testdb \
  -p 50000:50000 \
  -v /root/ai/db2/database:/database:z \
  icr.io/db2_community/db2
```
或使用docker-compose.yml
```yaml
services:
  db2server:
    image: icr.io/db2_community/db2
    container_name: db2server
    privileged: true
    environment:
      LICENSE: "accept"
      DB2INSTANCE: "db2inst1"
      DB2INST1_PASSWORD: "Passw0rd"
      DBNAME: "testdb"
    ports:
      - "50000:50000"
    volumes:
      - /root/ai/db2/database:/database:z
    restart: unless-stopped
```
```	
podman-compose up -d
podman-compse down
podman exec -ti db2server su - db2inst1
docker logs -f db2server
```


## 建hermes帳號
```
sudo useradd hermes
sudo passwd hermes
```
依提示輸入兩次新密碼即可

## 賦予 sudo 管理員權限
```
sudo usermod -aG wheel hermes
```
重新登入一次

## 安裝git
```
sudo dnf install git -y
git --version
git config --global user.name "hermes"
git config --global user.email "hermes@mxic.com.tw"
git config --list
```

## 安裝 C++ 編譯器與開發套件群組
```
sudo dnf groupinstall "Development Tools" -y
```

## 安裝hermes
```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

## 安裝OpenWebUI
```
cd /root/ai/
mkdir open-webui
cd open-webui
vi docker-compose.yaml
```
```
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    restart: always
    ports:
      - "3000:8080"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      - WEBUI_SECRET_KEY=sk-My520
    volumes:
      - ./open-webui:/app/backend/data:z
```

## 透過 Docker 安裝與運行 Hermes Agent
## 1：複製專案儲存庫
```
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
```
## 2：設定環境變數
```
cp .env.example .env
```

## 3：使用 Docker Compose 啟動
```
docker compose up -d --build
```

## 4：進入容器或執行指令
```
docker compose exec hermes hermes
docker compose exec hermes hermes setup
docker compose exec hermes hermes gateway start
```

## 啟用Presidio PII 個人識別資訊 (PII) 
```
vi /root/ai/presidio/docker-compose.yml
```
```
services:
  presidio-analyzer:
    image: mcr.microsoft.com/presidio-analyzer:latest
    container_name: presidio-analyzer
    ports:
      - "5001:3000"
    restart: unless-stopped

  presidio-anonymizer:
    image: mcr.microsoft.com/presidio-anonymizer:latest
    container_name: presidio-anonymizer
    ports:
      - "5002:3000"
    restart: unless-stopped
```

## Guardrail Test
```
我的名字是張三峰,我的電子郵件是test@example.com,電話是0912-345-678,信用卡號 1111-2222-3333-4444,公司是旺宏電子,查詢旺宏電子公司的地址在哪?
```

## Cloudflare若要加新的litell1.chrisai.cc.cd DNS
若偏好直接在當前頁面點擊 [+ 新增記錄] 按鈕，類型需選擇 CNAME，名稱輸入 litellm1，
目標填入 Tunnel 的 UUID 網址（即 <Tunnel-UUID>.cfargotunnel.com），
fbe33848-5dc6-43ce-814b-3b1c93b53eff.cfargotunnel.com
並保持 通過 Proxy 處理 (橘色雲朵) 開啟。
