---
title: "Tailscale 完整解析：原理、功能與安裝設定步驟（內網穿透 VPN 教學）"
date: 2026-08-31
description: Tailscale 是一款基於 WireGuard 的 SD-WAN 組網工具，讓你把分散各地的電腦、NAS、手機連成一張加密的私密虛擬網路（Tailnet），使用 100.x.x.x IP 與 MagicDNS 名稱即可互通。本文詳細拆解其運作原理、核心功能與各平台設定步驟。
tags:
  - networking
  - vpn
  - wireguard
  - tailnet
  - sd-wan
  - homelab
cover: /assets/images/tailscale/tailscale-logo.png
---

# Tailscale 完整解析：原理、功能與設定步驟

> **把分散各地的裝置，連成一張加密的私密虛擬網路。**
> 用 `100.x.x.x` IP 與 MagicDNS 名稱即可互通，出門在外也像在家。

---

## 📊 專案速覽

| 項目 | 資料 |
|------|------|
| **名稱** | Tailscale |
| **類型** | SD-WAN 組網工具 / 私密 VPN |
| **底層技術** | WireGuard |
| **授權** | MIT（開源，控制面板為商業服務） |
| **免費額度** | 5 使用者、20 裝置（含 1 個子網路由、1 個 Exit Node） |
| **平台** | Windows / macOS / Linux / iOS / Android / router |
| **官網** | [tailscale.com](https://tailscale.com) |

---

## 🎯 什麼是 Tailscale？

### 一句話說明

> **Tailscale 把分散在全世界的裝置，透過加密隧道連成一張虛擬內網（Tailnet）。**

你不需要：
- ❌ 固定 IP（public IP）
- ❌ 路由器轉發（port forwarding）
- ❌ 手動設定 IP 表
- ❌ 懂複雜防火牆

你只需要：
- ✅ 在每個裝置上安裝 Tailscale
- ✅ 用同一個帳號登入
- ✅ 各裝置就自動連成一張網

### 核心概念：Tailnet

```text
你的使用者帳號
        ↓
    Tailnet（私密虛擬區網）
        ↓
  把所有裝置加進去
```

每個加入的裝置都會獲得：
- 一個 **100.x.y.z 格式的虛擬 IP**
- 一個 **`*.ts.net` 的 MagicDNS 名稱**（例如 `my-nas.tailnet-xxxx.ts.net`）

---

## ⚙️ 運作原理

### 三大核心架構

| 元件 | 說明 |
|------|------|
| **Control Plane（控制平面）** | 協調伺服器，負責交換金鑰與路由資訊 |
| **Data Plane（資料平面）** | 實際轉發加密資料（WireGuard 隧道） |
| **DERP（中繼網路）** | NAT 穿透失敗時的保底加密中繼 |

### 詳細流程

```text
┌──────────────┐
│  裝置 A        │
│  本地生成私鑰   │
└──────┬───────┘
       ↓ 登入
┌──────────────┐
│  Control Server│  ← 交換公鑰、端點、狀態
└──────┬───────┘
       ↓ 拿到對端公鑰
┌──────────────┐
│  NAT 穿透      │
│  （直接直連 P2P）│
└──────┬───────┘
       ↓ 成功？
   ┌───┴───┐
   是      否
   │        │
┌──┴───┐  ┌───┴────────┐
│ 直連  │  │  DERP 中繼   │
│(最快) │  │（保底轉發）  │
└───────┘  └────────────┘
```

### 重點機制

| 機制 | 原理 |
|------|------|
| **P2P 直連** | 兩端透過 NAT 穿透直接連線，延遲最低、 bandwidth 最高 |
| **DERP 中繼** | 直連失敗時，由 Tailscale 營運的加密中繼轉發（只轉發加密後的資料，拿不到私鑰） |
| **MagicDNS** | 用主機名解析設備，不用記 100.x.x.x IP（例如 `my-nas.tailnet.ts.net`） |
| **身份為本位** | 每台設備有自己的私鑰，IP 或網路變化時自動重協調路徑 |

---

## 🆚 Tailscale vs WireGuard

| 項目 | WireGuard | Tailscale |
|------|-----------|-----------|
| **本質** | 底層 VPN 工具（building block） | 完整組網解決方案 |
| **NAT 穿透** | 需手動設定 | 自動（P2P + DERP） |
| **設定複雜度** | 較高（手動配金鑰、endpoint） | 極低（一鍵登入） |
| **MagicDNS** | 無 | ✅ 有 |
| **管理介面** | 無 | ✅ 控制面板（Admin Console） |
| **Access Control** | 基礎 | ✅ ACLs（節點級權限） |
| **額外的功能** | 無 | Taildrop、Exit Node、Funnel、子網路由 |

> **重點**：WireGuard 是「磚塊」，Tailscale 是「整栋房子」——內建了 MagicDNS、ACL、Taildrop 等一整套功能。

---

## ✨ 核心功能一覽

### 📁 1. Taildrop（檔案傳輸）

- 在你自己的裝置間傳檔案（類似 AirDrop，但跨裝置、跨網路）
- 支援大檔案、背景傳輸

### 🌐 2. MagicDNS（自動 DNS）

| 功能 | 說明 |
|------|------|
| **主機名解析** | 用 `my-nas` 即可連到設備，不用記 IP |
| **Split DNS** | 可設定特定網域的 DNS 解析（例如 `internal.example.com` → 特定伺服器） |
| **Extra Records** | 可手動加入自訂 DNS 記錄 |

### 🚪 3. Exit Node（出口節點）

- 讓一台裝置當「出口」，其他裝置的流量都從它出去
- 適合：在家用 NAS 當出口，讓手機流量走 home IP

```bash
sudo tailscale up --advertise-exit-node   # 讓這台成為出口
# 其他設備：sudo tailscale up --exit-node=my-nas
```

### 🏠 4. Subnet Routing（子網路由）

- 把一台裝置所在的區域網（LAN）公布到 Tailnet
- 讓 tailnet 內所有裝置都能連到那張區域網

```bash
sudo tailscale up --advertise-routes=192.168.100.0/24
```

### 🔌 5. Tailnet Funnel（公開服務）

- 把你本地的服務（例如 Home Assistant、NAS 管理頁）安全地暴露到網際網路
- 只讓授權的人訪問，不需要 port forwarding

### 🧩 6. ACLs（存取控制列表）

- 精細控制「哪些裝置可以連到哪些服務」
- 不需要複雜防火牆規則

### 📡 7. Peer Relay（節點中繼）

- 在 tailnet 內部署中繼設備
- 適合严格 NAT 或大流量場景

### 🔐 8. Tailnet Lock（節點鎖定）

- 用 TKA（Tailnet Key Authority）驗證節點身分
- 所有通訊都經過加密金鑰驗證

### 📂 9. Drop（檔案分享）

- 把檔案放到裝置的 Drop 資料夾，自動同步到其他裝置

---

## 🛠️ 安裝設定步驟

### 步驟 1：到官網安裝客户端

| 平台 | 安裝方式 |
|------|---------|
| **Windows** | 下載 `.exe` 安裝檔 |
| **macOS** | 官網下載或 App Store |
| **Linux** | 用官方 shell script 或 package manager |
| **iOS/Android** | App Store / Google Play |
| **Router** | 透過 OpenWrt、pfSense 等 |

### 步驟 2：登入帳號

- 用同一個帳號（Google / Microsoft / 密碼等）在所有裝置登入
- 登入即加入 Tailnet

### 步驟 3：在 Admin Console 核准設備

1. 到 [tailscale.com/admin/machines](https://tailscale.com/admin/machines)
2. 核准每個裝置的權限（Auth Key）

### 步驟 4：使用 MagicDNS 互相連接

```bash
# 測試連接（用主機名）
ping my-nas

# 或用 IP
ping 100.x.x.x
```

---

## 🐧 Linux 終端設定（tailctl）

### 基本指令

| 指令 | 功能 |
|------|------|
| `tailscale status` | 查看裝置狀態 |
| `tailscale up` | 啟動並登入 |
| `tailscale down` | 停止連線 |
| `tailscale ip` | 查看本機 IP |
| `tailscale ping <host>` | 測試連接 |
| `tailscale netcheck` | 檢查網路穿透能力 |
| `tailscale debug` | 除錯資訊 |

### 進階設定

```bash
# 讓本機成為子網路由
sudo tailscale up --advertise-routes=192.168.1.0/24

# 讓本機成為出口節點
sudo tailscale up --advertise-exit-node

# 指定特定 DNS
sudo tailscale up --accept-dns=false

# 加入 Tailnet（使用 Auth Key）
sudo tailscale up --authkey=tskey-auth-xxxxx
```

---

## 📱 各平台重點設定

### Windows / macOS（桌面版）

1. 下載安裝 → 2. 登入 → 3. 核准 → 4. 開始使用

### Linux（伺服器）

```bash
# 安裝（官方 script）
curl -fsSL https://tailscale.com/install.sh | sh

# 啟動
sudo tailscale up
```

### Router（如 pfSense / OpenWrt）

1. 安裝 Tailscale 套件
2. 登入後在路由設定中開啟「子網路由」
3. 讓所有透過路由的裝置都加入 Tailnet

---

## 🔒 安全性

| 面向 | 說明 |
|------|------|
| **加密** | 底層用 WireGuard，所有通訊加密 |
| **金鑰管理** | 每台設備有自己的私鑰，分散式管理 |
| **身份為本位** | 憑身份（identity）決定存取，而非僅憑 IP |
| **Tailnet Lock** | 可選用 TKA 驗證所有節點 |
| **ACLs** | 節點級存取控制 |

> **重要**：DERP 中繼只轉發加密後的資料，拿不到你的私鑰。

---

## 💰 收費比較

| 方案 | 價格 | 適合 |
|------|------|------|
| **Free** | 免費 | 5 使用者、20 裝置（含 1 subnet、1 exit node） |
| **Pro** | $3/人/月 | 更多子網路由、Exit Node、多出口 |
| **Team** | $6/人/月 | 團隊管理、多個子網、多個出口 |
| **Enterprise** | 訂製 | 高階功能、SLA |

> **個人/家庭使用**：Free 方案通常夠用！

---

## 🎯 適合場景

| 場景 | 說明 |
|------|------|
| **NAS 遠端存取** | 出門在外也能連回家 NAS |
| **家庭自動化** | Home Assistant 安全暴露到網際網路 |
| **團隊協作** | 分散式團隊連成私密網路 |
| **遠端辦公** | 安全連回公司內網 |
| **開發者測試** | 把本地服務安全公開測試 |

---

## 📝 常見問題（FAQ）

### Tailscale 需要固定 IP 嗎？

不需要。它透過 NAT 穿透自動連接，即使 IP 改變也會自動重協調路徑。

### 免費方案有哪些限制？

- 5 使用者、20 裝置
- 1 個子網路由、1 個 Exit Node
- 通常足夠個人/家庭使用

### Tailscale 會拖慢速度嗎？

P2P 直連時幾乎無影響；DERP 中繼時會有輕微延遲，但通常可接受。

### 可以自架 Control Server 嗎？

可以，有 [Headscale](https://headscale.n8.io) 等開源自架方案。

---

## 總結

Tailscale 是一款設計精巧的組網工具，核心亮點：

| 亮點 | 說明 |
|------|------|
| **零設定** | 一鍵登入，自動 NAT 穿透 |
| **加密安全** | WireGuard + 身份為本位 |
| **MagicDNS** | 用主機名連接，不用記 IP |
| **功能豐富** | Taildrop、Exit Node、子網路由、Funnel |
| **跨平台** | Windows/macOS/Linux/手機/路由 |
| **免費可用** | 5 人 20 裝置 |

如果你需要「把分散各地的裝置連成一張私密加密網路」，Tailscale 是目前**最簡單好用的選擇**！

---

*本文於 2026-08-31 整理自 Tailscale 官方文件與社群資料*
