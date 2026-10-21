---
title: "FreeIDX：完全跑在 Cloudflare 免費層上的現代化論壇"
date: 2026-10-21
description: 一個基於 Cloudflare Workers + D1 + KV + R2 的免費開源論壇，前端後端同一個 Worker，_posts/留言/附件/會員/SEO 多語全內建，零成本零維運。
tags: [github, cloudflare, forum, workers, d1, r2, opensource, self-hosted]
---

# FreeIDX：完全跑在 Cloudflare 免費層上的現代化論壇

**FreeIDX** 是一個「完全建立在 Cloudflare 上」的免費開源現代化論壇。前端 React 19 SPA 與後端 Hono Worker 打包成**單一 Worker 專案**部署，資料庫用 D1（SQLite）、附件用 R2、快取用 KV + Cache API——全部落在 Cloudflare 免費額度內，**零成本、零伺服器、零維運**。

⚠️ 專案自帶法律免責聲明：僅限合法合規的學習、研究與技術交流用途，部署前請先閱讀 [LEGAL_DISCLAIMER](https://github.com/FreeIDX/FreeIDX/blob/main/docs/LEGAL_DISCLAIMER.md)。

## 專案概況

| 項目 | 資料 |
|---|---|
| 倉庫 | [github.com/FreeIDX/FreeIDX](https://github.com/FreeIDX/FreeIDX) |
| 語言 | TypeScript |
| 授權 | AGPL-3.0（SaaS 修改也必須開源，第 13 條） |
| 建立時間 | 2026-10-12（非常新） |
| 技術棧 | Cloudflare Workers · React 19 · Tailwind CSS 4 · Hono · D1 · KV · R2 |
| 官網 / Demo | [www.freeidx.com](https://www.freeidx.com) |
| 支援語言 | 簡中/繁中/英/日/韓/法/德/西/俄/泰 共 10 種 |

> 專案剛創立不到兩週（star 數還很少），但代碼-complete度與文件密度遠超同階段專案——repo 內含 596 個檔案、6.4 萬字元的中文架構設計書、10 語 README 與 CI/CD 部署流水線，是一個「設計先行」的工程化專案。

## 為什麼特別：單一 Worker 全棧架構

一般自架論壇需要 VPS + Nginx + MySQL + 對象存儲；FreeIDX 把整站塞進**一個 Cloudflare Worker**：

```
使用者訪問 forum.example.com
        ↓
  Cloudflare Worker「freeidx-api」（Edge 節點）
        ↓
  ┌─ 路由匹配
  ├─ /assets/*  → Workers Assets 直接服務靜態檔（不耗 Worker 請求數）
  ├─ /api/* /files/* → Hono 處理業務邏輯
  │     ├ JWT + Session 雙軌認證
  │     ├ 許可權引擎（使用者群組 × 板塊 × 版主）
  │     └ JSON / R2 附件串流代理
  └─ 其他 → 爬蟲預渲染 HTML / SPA index.html（React Router）
```

### 技術選型

| 層 | 選擇 |
|---|---|
| 前端 | React 19 + React Router 7 + Tailwind CSS 4 + TanStack Query + Zustand + Vite |
| 後端 | Hono + TypeScript + Zod（Cloudflare Workers） |
| 資料庫 | D1（SQLite）、KV 低頻寫入快取、Cache API 邊緣快取 |
| 儲存 | R2（附件/頭像，經 Worker 代理 `/files/:key` 串流） |
| 認證 | JWT（httpOnly Cookie）+ D1 session 表，PBKDF2-SHA256 |
| 驗證碼 | Cloudflare Turnstile |
| 排程 | Cron Triggers（5 分鐘 / 每小時對帳 / 每日三級） |
| 工程 | pnpm workspace + Turborepo monorepo |

附件走 R2 串流代理的細節很講究：R2 **沒有出口流量費**，而透過 Worker 代理可避開 Cloudflare Storage Class B 操作配額——免費層思維貫穿每個設計決策。

## 核心功能

### 論壇核心
- **文章管理**：發布、編輯、刪除、置頂、關閉、移動板塊、精華；cursor 分頁 + 無限捲動；TanStack Query 樂觀更新（閱讀數/回覆數即時反饋）
- **留言系統**：回覆、引用、關鍵字突顯、已讀標記、多層回覆
- **附件上傳**：圖片/檔案直傳 R2，內建 **TipTap 富文本編輯器**，支援代碼插入與貼圖上傳
- **搜尋**：板塊內關鍵字搜尋，命中片段突顯

### 使用者與許可權
- **雙軌認證**：JWT（httpOnly Cookie）+ session 表，全站 CSRF 防護；註冊、登入、電子郵件驗證碼、找回密碼
- **三級許可權系統**：使用者群組 × 板塊存取 × 版主規則引擎，讀寫與版務授權可細到單一板塊
- **自動升等**：發文數 + 主題數落在積分區間自動切換群組，無需人工
- **版務操作**：置頂/關閉/刪除/移動/封使用者，支援批次處理

### 會員與變現
- **完整閉環**：積分 + 等級 + VIP + 付費附件 + 訂單支付
- **可插拔支付通道**：card / paypal / stripe / alipay 各為獨立外掛；支付核心只保留介面 + 登錄表 + 訂單狀態機，後台可啟用/停用通道、輪換金鑰，**零部署生效**
- **廣告系統**：自訂廣告位 + Google AdSense 多位置彈性配置

### SEO / GEO（AI 搜尋引擎最佳化）
- **爬蟲預渲染**：寫入時預先產生 SEO HTML 存 R2 + Cache API，只對爬蟲 UA 服務，請求時渲染 CPU 結構性降為零
- **完整索引工具包**：sitemap、JSON-LD 結構化資料、**llms.txt**、AI 爬蟲政策、robots；偽靜態 `.htm` URL 相容舊連結
- **邊緣快取**：Cache API 讀取屏障，熱門接口第二次命中 `x-edge-cache: HIT`，大幅節省 D1 讀取配額

### 免費層深度適配（最硬核的部分）
Cloudflare 免費層限制：10 萬請求/日、D1 500 萬行讀/10 萬行寫、Worker 10ms CPU。FreeIDX 的應對：

| 限制 | 对策 |
|---|---|
| D1 行讀配額 | 四層快取（Isolate 內 LRU 記憶體 + KV + D1 cache 表 + Cache API）；`thread` 表反正規化作者名/最後回覆人，列表頁**單表掃描零 JOIN**，rows_read 減半 |
| D1 行寫配額 | `DB.batch()` 合併查詢、`waitUntil` 非同步計數合并 |
| Worker 10ms CPU | 密碼哈希用 PBKDF2-SHA256 並按 10ms 上限調迭代次數；`post` 表存 `message_fmt` 寫入時預格式化，讀帖免渲染開銷 |
| 舊密碼相容 | 新格式 `argon2id$…`，遺留 md5 懶升級；`token_version` 改密即吊銷 JWT |

### 排程與維運自動化
Cron Triggers 三級排程自動處理：session 回收、每日統計重置、附件 GC（暫存未關聯的 R2 對象清理）、孤單訂單對帳。另有一張 D1 `queue` 表做非同步任務佇列。

## 資料層設計亮點

架構書（`docs/开发架构文档.md`）定義了 20+ 張 D1 表，幾個值得學習的取捨：

- **反正規化取捨**：`thread` 表額存 `username`/`lastusername`/`avatar` 時間戳，列表頁免去 JOIN user 或二次查詢；改名時 `waitUntil` 非同步批次回寫——「改名極低頻、讀多寫少」的標準取捨
- **站點設置唯一存在 D1 的 `kv` 表**（不是 Cloudflare KV 產品），後台改設定即時生效不踩 KV 寫入配額
- **附件狀態機**：`attach.status` 0=暫存待關聯 / 1=已入库，配合附件 GC 防止 R2 垃圾堆積

## 部署：三分支路徑

### 方式一：GitHub Actions 自動部署（推薦）

Fork 後只要設兩個 Secret + 跑一次 workflow：

| Secret | 用途 |
|---|---|
| `CLOUDFLARE_API_TOKEN` | Cloudflare API Token（Developer Services 範本） |
| `CLOUDFLARE_ACCOUNT_ID` | 帳戶 ID |

Pipeline 會**依名稱自動查找並建立缺少的 D1 / KV**，首次執行勾選 `apply_migrations`（建表）+ `run_seed`（初始板塊 + 首个管理員）即上線。之後 push main 自動重新部署，預設不再動資料庫。

![建立 API Token](/assets/images/freeidx/img-01.png)
![設定 GitHub Secrets](/assets/images/freeidx/img-02.png)

首次部署後到 Worker 的 **Variables and secrets** 補三個執行期 Secret：

| 名稱 | 用途 | 必要 |
|---|---|---|
| `JWT_SECRET` | 登入 token / CSRF 簽章 | ✅ |
| `TURNSTILE_SECRET` | 驗證碼服務端校驗 | 選 |
| `SECRETS_MASTER_KEY` | 支付金鑰的 AES-GCM 主鑰 | 選 |

> 預設管理員帳號寫在部署文件裡（`admin@admin.com`），**首次登入務必立即修改密碼**。

![設定 Worker Secrets](/assets/images/freeidx/img-03.png)

### 方式二：本地開發

```bash
pnpm install
pnpm --filter @freeidx/web build
pnpm --filter @freeidx/api dev   # miniflare 本地模擬，免真實資源 ID
pnpm db:apply && pnpm db:seed    # 建表 + 初始資料
```

### 方式三：Cloudflare Dashboard 視覺化建置

Workers & Pages → Continue with GitHub，但需手動把真實 D1/KV ID 填進 `wrangler.toml`（repo 內是佔位值），專案名必須為 `freeidx-api`。

### 自訂網域

把網域託管到 Cloudflare 改 NS → Worker 綁 Custom Domain → 更新 `SITE_URL` 變數 push 生效。`/api/*`、`/files/*`、頁面同屬一個 Worker 免 Route 設定，綁域後邊緣快取自動生效；記得停用 `*.workers.dev` 預覽域避免搜尋引擎重複收錄。

## 與其他開源論壇方案比較

| | FreeIDX | Discourse | Flarum | 傳統 PHP 論壇 |
|---|---|---|---|---|
| 託管需求 | Cloudflare 免費層 | VPS ≥1GB RAM + Redis + PostgreSQL | PHP + MySQL | PHP + MySQL |
| 月度成本 | $0 | $10-20+ | $5+ | $5+ |
| 維運負擔 | 幾乎零（Serverless） | 重（Ruby 全棧） | 中 | 中（安全更新頻繁） |
| 附件出口流量 | $0（R2） | 計費 | 計費 | 計費 |
| 行動端 | 響應式 SPA | 原生級體驗 | 響應式 | 參差 |
| 變現機制 | 內建會員/支付/廣告 | 付費插件 | 外掛 | 外掛生態老 |
| 適合規模 | 中小站、個人站 | 大型社群 | 中型社群 | 存量遷移 |

FreeIDX 的定位非常清楚：**個人/中小論壇的「零成本極限部署」**，代價是所有資源被 Cloudflare 綁定、且免費層配額決定了流量天花板（每日 10 萬請求級別）。

## Repo 結構

```
FreeIDX/
├── apps/
│   ├── web/          # 前端 React 19 SPA → Worker Static Assets
│   └── api/          # 後端 Hono Worker（含 migrations/）
├── packages/
│   └── shared/       # 前後端共用型別、錯誤碼、i18n 資源
├── scripts/          # i18n 產生與校驗腳本
├── docs/             # 架構設計書 / 前後端頁面設計 / 部署手冊（10 語）
└── .github/workflows/  # CI / Cloudflare 部署流水線
```

多語不是裝飾：10 種語言文案由腳本生成 + pre-commit 全鏈校驗，從機制上消除硬編碼文案。

## 授權與注意事項

- **AGPL-3.0**：修改後以網路服務（SaaS）提供，必須依第 13 條向服務使用者公開完整修改源碼
- **法律免責聲明**：專案明確要求僅限合法用途，使用前須完整閱讀免責聲明
- 專案極新（2026-10 建立），功能面以架構書 + migrations + 代碼為準，生產使用建議先觀察一段時間

## 參考資料

- 專案主頁：[https://www.freeidx.com](https://www.freeidx.com)
- GitHub：[https://github.com/FreeIDX/FreeIDX](https://github.com/FreeIDX/FreeIDX)
- 架構設計書：[docs/开发架构文档.md](https://github.com/FreeIDX/FreeIDX/blob/main/docs/%E5%BC%80%E5%8F%91%E6%9E%B6%E6%9E%84%E6%96%87%E6%A1%A3.md)
- 繁中 README：[docs/README-zh-tw.md](https://github.com/FreeIDX/FreeIDX/blob/main/docs/README-zh-tw.md)
- 免責聲明：[docs/LEGAL_DISCLAIMER.md](https://github.com/FreeIDX/FreeIDX/blob/main/docs/LEGAL_DISCLAIMER.md)
- Cloudflare Workers / D1 / KV / R2 免費層额度：[cloudflare.com/pricing](https://www.cloudflare.com/pricing/)
