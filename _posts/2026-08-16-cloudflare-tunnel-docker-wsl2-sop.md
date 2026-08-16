---
title: "Windows Docker (WSL2) 外網穿透完整 SOP：Cloudflare Tunnel"
date: 2026-08-16
description: 解決 Windows Docker Desktop (WSL2) 容器服務無法從外網存取的問題，使用 Cloudflare Tunnel 建立加密隧道，免 port forwarding、免固定 IP、免開埠。
tags: [docker, cloudflare-tunnel, windows, wsl2, networking, sop]
---

# Windows Docker (WSL2) 外網穿透完整 SOP：Cloudflare Tunnel

## 問題背景

在 Windows 上跑 Docker Desktop（WSL2 backend）時，常遇到以下困境：

1. **`netstat -ano | findstr LISTEN` 查不到容器 port** — 因為 listener 在 WSL2 VM 內部的 `wsl-bootstrap` 進程，不在 Windows kernel socket table
2. **內網可以連（如 `192.168.1.10:4000`），外網連不上** — 路由器沒有 port forwarding + ISP 封鎖非標準埠
3. **傳統解法（port forwarding / DMZ）有安全風險**，且住宅寬頻通常只有 80/443 可被外部進入

### 為什麼 netstat 看不到？

```
外網 → 路由器 → Windows Host (vEthernet) → WSL2 VM → Docker Container
                                              ↑
                                     wsl-bootstrap 在這裡 bind socket
                                     Windows netstat 看不到
```

Docker Desktop on WSL2 **不使用** Windows NAT/portproxy 規則。流量進入 WSL2 VM 後，由 `wsl-bootstrap`（PID 1）bind socket 並 DNAT 到容器。Windows 原生的 `netstat`、`netsh portproxy` 都看不到這些 listener。

**正確檢查方式**：
```bash
# 在 WSL2 docker-desktop distro 內查看
wsl -d docker-desktop -- netstat -tlnp | grep :4000

# 或直接看 Docker
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

### 為什麼外網連不上？

完整鏈路分析：

```
外網用戶 → Public IP:4000
              ↓
        【ISP/電信層】← ❌ 住宅寬頻通常封鎖非 80/443 埠
              ↓
        【路由器 NAT / Port Forwarding】← ❌ 通常沒設
              ↓
        Windows Firewall ← 對 WSL2/Docker 流量通常放行
              ↓
        WSL2 (192.168.1.10:4000) → Container ✅
```

## 解法：Cloudflare Tunnel

Cloudflare Tunnel 讓本機主動向外建立加密隧道到 Cloudflare Edge，**完全繞過**：
- ISP 封埠問題（不需要外網進來）
- NAT / Port Forwarding（本機主動出連）
- 固定 IP 需求（動態 IP 沒問題）
- Windows Firewall（出站流量不受限）

### 架構

```
外網用戶 → https://your-domain.com
              ↓
        Cloudflare Edge (自動 SSL)
              ↓ 加密隧道 (QUIC/HTTP2)
         cloudflared (本機 Windows)
              ↓ localhost:4000
        Docker Desktop port mapping
              ↓
        WSL2 VM → Container ✅
```

## 前置需求

| 項目 | 說明 |
|---|---|
| Cloudflare 帳號 | 免費即可 |
| 一個網域 | 已放在 Cloudflare DNS 管理（如 `example.com`） |
| API Token | 需要 Zone 讀取 + Tunnel 管理權限（DNS 可手動加） |
| Windows 10/11 | Docker Desktop (WSL2 backend) |
| 容器服務 | 已在本機 port 上監聽（如 `localhost:4000`） |

## Step-by-Step

### Step 1：安裝 cloudflared

```powershell
# 方法 A：winget（需要 tty）
winget install --id Cloudflare.cloudflared -e

# 方法 B：手動下載（非 tty 環境）
curl -skL -o $env:LOCALAPPDATA\Temp\cloudflared.exe `
  "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
copy $env:LOCALAPPDATA\Temp\cloudflared.exe C:\Users\<youruser>\bin\cloudflared.exe

# 驗證
C:\Users\<youruser>\bin\cloudflared.exe --version
```

### Step 2：建立 Cloudflare Tunnel

**方法 A：CLI（需要 cert.pem，較複雜）**

```bash
export CLOUDFLARE_API_TOKEN="cfat_xxxxxxxxxxxx"
cloudflared tunnel login          # 會開瀏覽器授權
cloudflared tunnel create my-tunnel
```

> ⚠️ `tunnel login` 在非互動環境（如 agent/CI）可能無法完成。如果 CLI 方式失敗，用方法 B。

**方法 B：REST API（推薦，可自動化）**

```bash
export CLOUDFLARE_API_TOKEN="cfat_xxxxxxxxxxxx"

# 1. 取得 Account ID
ACCOUNT_ID=$(curl -sk -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>" | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['result']['name'])")
# 注意：需要從 zone 資訊取得 account，或直接用 dashboard 看

# 2. 建立 tunnel（account-level）
curl -sk -X POST \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-tunnel"}' \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/cfd_tunnel"

# 3. 取得 tunnel credentials
TUNNEL_ID="<上面回傳的 id>"
curl -sk \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/cfd_tunnel/$TUNNEL_ID/credentials" | \
  python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin)['result'], indent=2))" \
  > ~/.cloudflared/my-tunnel.json
```

> 💡 **API Token 權限注意**：token 需要 `Account:Cloudflare Tunnel:Edit` 權限。如果只有 Zone-level token，account-level tunnel API 會回 10000 Authentication error。

### Step 3：寫 config.yml

```yaml
# C:\Users\<youruser>\.cloudflared\config.yml
tunnel: <TUNNEL_ID>
credentials-file: C:\Users\<youruser>\.cloudflared\my-tunnel.json

ingress:
  - hostname: your-subdomain.example.com
    service: http://localhost:4000
  - service: http_status:404
```

### Step 4：加 DNS 記錄

到 Cloudflare Dashboard → 你的網域 → **DNS** → **Records** → **Add record**：

| 欄位 | 值 |
|---|---|
| Type | **CNAME** |
| Name | `your-subdomain` |
| Target | `<TUNNEL_ID>.cfargotunnel.com` |
| Proxy status | 🟠 **Proxied**（必須開，橘色雲） |
| TTL | Auto |

> 如果 API token 有 DNS:Edit 權限，可以用 API：
> ```bash
> curl -sk -X POST \
>   -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
>   -H "Content-Type: application/json" \
>   -d "{
>     \"type\": \"CNAME\",
>     \"name\": \"your-subdomain.example.com\",
>     \"content\": \"$TUNNEL_ID.cfargotunnel.com\",
>     \"proxied\": true,
>     \"ttl\": 1
>   }" "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/dns_records"
> ```

### Step 5：啟動 tunnel

```bash
cd ~/.cloudflared
cloudflared tunnel run
```

成功時會看到：
```
INF Starting tunnel tunnelID=<TUNNEL_ID>
INF Registered tunnel connection connIndex=0 ... location=khh01 protocol=quic
INF Registered tunnel connection connIndex=1 ... location=tpe01 protocol=quic
...
```

### Step 6：設開機自啟（Windows）

**方法 A：Startup 資料夾（不需 admin）**

建立 `C:\Users\<youruser>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\CloudflareTunnel.bat`：

```bat
@echo off
cd /d C:\Users\<youruser>\.cloudflared
start "" /MIN C:\Users\<youruser>\bin\cloudflared.exe tunnel run
```

**方法 B：Task Scheduler（需要 admin）**

```powershell
Register-ScheduledTask -TaskName 'CloudflareTunnel' `
  -Action (New-ScheduledTaskAction -Execute 'C:\Users\<user>\bin\cloudflared.exe' `
    -Argument 'tunnel run --config C:\Users\<user>\.cloudflared\config.yml') `
  -Trigger (New-ScheduledTaskTrigger -AtStartup) `
  -User '<youruser>' -Force
```

**方法 C：Windows Service（最穩，需要 admin + NSSM 或 WinSW）**

### Step 7：驗證

```bash
# 本機測試（如果 router DNS 有快取問題，用 --resolve 繞過）
curl -sk https://your-subdomain.example.com/health/liveliness

# 或用 Cloudflare proxy IP 直接測
curl -sk --resolve your-subdomain.example.com:443:104.21.13.111 \
  https://your-subdomain.example.com/health/liveliness

# 外網測試（手機關 Wi-Fi 走 4G）
# 瀏覽器開 https://your-subdomain.example.com
```

## 故障排除

### netstat 看不到 port（正常現象）

```bash
# ❌ 不要這樣查（Windows host 看不到 WSL2 內的 listener）
netstat -ano | findstr :4000

# ✅ 正確方式
wsl -d docker-desktop -- netstat -tlnp | grep :4000
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

### tunnel 啟動後立刻退出

檢查 `~/.cloudflared/config.yml` 的 tunnel ID 和 credentials-file 路徑是否正確。

### DNS 解析不到（本機）

路由器 DNS 快取問題。解法：
- `ipconfig /flushdns`（清 Windows 快取）
- 路由器後台改 DNS 為 `1.1.1.1` 或 `8.8.8.8`
- 重啟路由器

### 外網 502/530 錯誤

- 確認 cloudflared 正在跑：`tasklist | findstr cloudflared`
- 確認容器正在跑：`docker ps`
- 確認 ingress hostname 和 DNS 記錄一致
- 看 tunnel log（如果設了 `--logfile`）

### API Token 權限不足

| 操作 | 需要的權限 |
|---|---|
| 建立/管理 tunnel | Account:Cloudflare Tunnel:Edit |
| 加/改 DNS 記錄 | Zone:DNS:Edit |
| 讀 zone 資訊 | Zone:Zone:Read |

如果 token 權限不夠，到 Cloudflare → My Profile → API Tokens → Edit Token 補上。

## 安全注意事項

1. **務必開啟 SSL**：Cloudflare proxy (🟠) 自動提供 Let's Encrypt 憑證，不要用 DNS only (🌤️)
2. **Ingress 最後一筆必須是 catch-all**：`- service: http_status:404` 防止未授權的 hostname 訪問
3. **API Token 不要 commit 到 git**：用環境變數或 `.env`（加到 `.gitignore`）
4. **litellm 等 AI gateway 建議加 API key 驗證**：tunnel 解決的是「連得到」的問題，不解決「誰都能用」的問題

## 完整檔案清單

```
C:\Users\<user>\bin\cloudflared.exe                    ← cloudflared 執行檔
C:\Users\<user>\.cloudflared\config.yml                ← ingress 設定
C:\Users\<user>\.cloudflared\<tunnel-name>.json        ← tunnel credentials
C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\CloudflareTunnel.bat  ← 開機自啟
```

## 參考

- [Cloudflare Tunnel 官方文件](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- [cloudflared GitHub](https://github.com/cloudflare/cloudflared)
- [Docker Desktop WSL2 網路架構](https://docs.docker.com/desktop/wsl/networking/)
