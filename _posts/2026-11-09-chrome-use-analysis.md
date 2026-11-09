---
title: "chrome-use 功能介紹：讓 AI Agent 直接驅動你「已登入的真實 Chrome」"
date: 2026-11-09
description: "chrome-use 是一個 Rust 寫的 CLI + MCP 瀏覽器自動化專案：透過原生訊息扩展驅動你日常使用的 Chrome，免重登、免除錯端口、CreepJS 實測 0% bot，支援 Claude Code / Codex / Cursor 等任何 Agent。"
tags:
  - AI Agent
  - 瀏覽器自動化
  - MCP
  - Rust
  - Chrome
---

# chrome-use 功能介紹：讓 AI Agent 直接驅動你「已登入的真實 Chrome」

> 專案：<https://github.com/leeguooooo/chrome-use> ｜ 官方文件：<https://chrome-use.leeguoo.com>
> 授權 Apache-2.0 ｜ ⭐ 約 240 Stars（分析當日）｜ 最新版本 v1.5.290（發布於 2026-11-09，幾乎每天發版）

## 一、專案概述

**chrome-use** 的定位只有一句話：**讓任何 AI Agent（Claude Code、Codex、Cursor、你自己寫的腳本）操作你「已經登入一切的那個 Chrome」**。

它解決的是瀏覽器自動化長期以來的三大痛點：

1. **不用開全新瀏覽器、不用重新登入** —— Playwright / Puppeteer 的新 contexts 是空的，cookie、session 全部要重來；
2. **不會被網站判定為機器人** —— 因為驅動的就是你本人的真實瀏覽器，官方實測 CreepJS 得分 **0% bot / 0% stealth**（完全沒有任何指紋覆蓋痕跡）；
3. **不彈「允許遠端偵錯嗎？」視窗** —— 走 Chrome 原生訊息（native messaging）擴充通道，不用 `--remote-debugging-port`、不用 token、安裝擴充功能後零逐次確認。

技術本體以 **Rust** 撰寫（佔比約 72%），另有 JavaScript（Chrome 擴充）、Python、Swift 等。專案原本是 [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) 的分支，現已獨立發展，隱身/擴充中繼架構、反偵測、人類化輸入、多 Agent 隔離與 CLI 都已大幅分岔。跨平台支援 **macOS / Linux / Windows**。

## 二、運作架構

```
你的 AI Agent (Claude Code / Codex / Cursor / MCP client)
        │  CLI 指令 或 MCP stdio
        ▼
chrome-use CLI (Rust, 本機常駐 daemon)
        │  Chrome Native Messaging（本機程序間通道）
        │  ※ 無網路 socket、無 token、無遠端伺服器
        ▼
chrome-use 瀏覽器擴充功能 (Chrome Web Store 一鍵安裝)
        │  chrome.debugger API
        ▼
你日常使用、已登入一切的真實 Chrome
```

幾個關鍵設計：

- **每個 `--session` 獲得自己顏色的分頁群組（tab group）**：多個 Agent 可以同時共用一個真實 Chrome 而互不干擾，也不會動到你自己的分頁。省略 `--session` 時會從 Codex 的 `CODEX_THREAD_ID` 等 runner ID 推導出穩定 session。
- **Agent 在你眼前工作**：你親眼看到分頁開啟、點擊發生；遇到 2FA 或 CAPTCHA 隨時可以接手，處理完再交還給 Agent。
- **所有資料留在本機**，擴充權限footprint 為 15 項且**不授予任何 host 權限**（`http/https` 為选用）。

## 三、與競品比較（README 官方對照表整理）

| 能力 | Playwright / Puppeteer / browser-use | 裸 CDP 端口 | Claude in Chrome | **chrome-use** |
|---|:-:|:-:|:-:|:-:|
| 支援任意 Agent / CLI | ✅ | ✅ | ❌ 僅 Claude | ✅ |
| 驅動你已登入的真實 Chrome | 需設定，新 context 是空的 | ✅ | ✅ | ✅ |
| 連線方式不彈「遠端偵錯」視窗 | —（自開瀏覽器） | 依版本彈窗 | 不彈 | **原生訊息，永不彈窗** |
| 真實瀏覽器指紋（CreepJS ~0%） | ❌ 有自動化標記 | ✅ | ✅ | ✅ 實測 0% |
| 無 `Runtime.enable` CDP 洩漏 | ❌ 洩漏 | ❌ 洩漏 | ✅ 實測乾淨 | ✅ **預設關閉** |
| 多 Agent 共用一個 Chrome + session 隔離 | ❌ | ⚠️ 無隔離 | ❌ | ✅ 彩色分頁群組 |

## 四、安裝與接接

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/leeguooooo/chrome-use/main/install.sh | sh

# Windows (PowerShell)
irm https://raw.githubusercontent.com/leeguooooo/chrome-use/main/install.ps1 | iex
```

預編譯二進位檔，**無 npm、無 token、Windows 不需管理員權限**；也支援 Nix（flake + home-manager/NixOS module）。接上 Chrome 只要兩步：

1. 從 Chrome Web Store 安裝 chrome-use 擴充功能；
2. `chrome-use extension install` 註冊原生訊息主機（一次性），之後直接 `chrome-use open <url>`。

**Agent 技能（skill）安裝**：安裝腳本會自動把內附 skill 裝進 Claude Code、Codex、Cursor 等；Claude Code 推薦走 plugin marketplace：

```
/plugin marketplace add leeguooooo/plugins
/plugin install chrome-use@leeguooooo-plugins
```

**MCP 模式**（給 Claude Desktop、ChatGPT connectors、n8n/Dify 這類跑不了 shell 的宿主）：

```json
{ "mcpServers": { "chrome-use": { "command": "chrome-use", "args": ["mcp"] } } }
```

## 五、核心功能詳解

### 1. 核心操作迴圈：open → snapshot → act → diff

```bash
chrome-use open https://example.com    # 連上你的 Chrome 並導覽
chrome-use snapshot -i                 # 互動元素 + @refs 快照（一切互動的起點）
chrome-use click @e3 --observe         # 動作，並觀察頁面反應
chrome-use snapshot -i --diff          # 只回傳與上次快照的差異
```

設計上非常講究**省 token**：`--diff` 增量快照、範圍快照、`--max-bytes` 預算、`observed.changes` 只列增刪行；`observed.announced` 會抓到動作期間出現過的 toast / aria-live 提示文字（例如「影片審核中，未儲存」這種來不及看到的訊息）。

### 2. 語意化定位與嚴格唯一性

- `find role/text/label/placeholder/testid` 走 Chrome 無障礙樹（含 `aria-labelledby`）；**必須恰好命中一個可見元素**，模糊時回傳最多 8 個候補讓你縮範圍，絕不亂點。
- 普通 CSS/XPath 給動作指令時同樣要求唯一，多中直接以 `selector_ambiguous` 拒絕。
- `click "Post"` 可直接按文字點擊；`--observe` 附帶完整的頁面反應觀察。

### 3. 結構化抽取與網站適配器（Site Adapters）

```bash
chrome-use extract --schema '{"rows":".item","fields":{"title":"a","url":{"sel":"a","get":"@href"}}}'
chrome-use site github/issues epiral/bb-browser --json
```

`extract` 一次呼叫就拿到結構化列資料；`site` 把網站變成「結構化資料 CLI」，直接吃網站自己的 API 回傳乾淨 JSON。

### 4. 登入自動化：接 Bitwarden / 1Password

```bash
chrome-use auth login --bwu            # 從 Bitwarden 填充目前登入頁（含 TOTP、passkey）
chrome-use auth login --1password      # 從 1Password（官方 op CLI，密碼不過手）
```

亮點是**誠實的回報語意**：只有網站真的接受登入才回 `signedIn: true` 並附證據；被導到驗證頁/2FA 頁會明確失敗並點名該頁面。遇到登入牆會先問你要不要從密碼庫自動登入（可選「這一次 / 這個站永遠 / 永不」）。1Password 走 `op run` 注入環境變數，本進程從頭到尾看不到明文密碼。

### 5. 示范教學（Teach by Demonstration）：錄一次，之後零模型重播

```bash
chrome-use open https://shop.example/cart && chrome-use teach start --name checkout
# ...你在該分頁手動走一遍流程...
chrome-use teach stop                  # 產生 ~/.chrome-use/teach/checkout.json
chrome-use teach replay ~/.chrome-use/teach/checkout.json --arg-env password=SHOP_PW
```

`teach stop` 會把你的人工操作轉成語意定位優先、按鍵合併、含等待與最終 URL 檢查的 op-list；**密碼、卡號、一次性代碼絕不被錄入**，一律變成 `--arg-env` 參數。之後重播不需要任何模型。

### 6. Inspect & Ask：點一個元素，讓 Agent 改它

按 **Alt+Shift+C** → 點選網頁元素 → 輸入你想改什麼 → Enter。chrome-use 把你的話、元素的原始碼 `file:line`（來自 code-inspector-plugin）、截圖與樣式送進該專案已執行的 Claude Code / Codex / Pi session。支援 Shift+多選最多 8 個元素、箭頭升降層級、P 暫停動畫、每張截圖畫筆標註。注入預設關閉、用完即除，輸入框跑在擴充自己的 frame 裡，頁面腳本讀不到你打的字。

### 7. 瀏覽器內 Agent 側邊面板

點工具列圖示開啟 side panel，直接選 **Codex / Claude Code / OpenCode / Pi** 當 Agent（沿用 CLI 已有登入與模型設定），在 Chrome 裡跟 Agent 對話：

- 目前網頁以 tag 附在訊息上，Agent 直接針對該分頁工作；
- 支援 `/` 選 skill、貼圖（最多 5 張，HEIC 自動轉 JPEG 並剝除 GPS EXIF）、排程提示（cron / 每日定時）、任務完成通知；
- `/resume` 可以接續你在終端開的 Claude Code / Codex session。

### 8. 反偵測：零 JS 注入的原生路線

指導原則是「**原生 CDP/Chrome 覆寫勝過 JS 說謊**」——重新定義 getter 本身就是可被偵測的謊言，原生覆寫不是：

- `navigator.webdriver = false` 透過 `Emulation.setAutomationOverride`（原生、不可被 CreepJS 式謊言檢測抓到）；
- **`Runtime.enable` 預設保持關閉**，堵掉 rebrowser 著名的 runtime-enable CDP 洩漏；
- 連你的真實 Chrome 時**注入零 JS 補丁**，指紋完全真實。

官方實測成績（連真實 Chrome）：

| 檢測站 | 結果 |
|---|---|
| CreepJS | **0% stealth · 0% headless**（無任何覆蓋痕跡） |
| bot.incolumitas.com | 全項通過 |
| bot.sannysoft.com | 全綠 |
| BrowserScan | Webdriver / UA / CDP 全乾淨 |
| Cloudflare 受管挑戰 | 通過，無需互動 |

人類化輸入：`--humanize off|fast|human`（預設 fast；human 模式帶種子化 60–200ms 停頓與落點複查）；`--show-position` 用 Chrome 自己的 overlay 畫橙色小方塊讓你追蹤 Agent 點哪裡，頁面 DOM/腳本/請求零痕跡。README 也誠實聲明：偵測站通過不代表每站通關、不保證帳號安全。

### 9. 提示注入防護（Prompt Injection）

網頁可以在人看不到的地方藏指令對付 Agent。chrome-use 預設：

- `snapshot` / `get text` / `read` **自動剔除人類不可見文字**（離屏、透明、裁切、零尺寸、與背景同色）並聲明剔除了多少；
- MCP 輸出與側邊面板把每個瀏覽器結果用 per-call nonce 包成「不可信網頁內容」欄位；
- 內測數據：隱藏假資訊命中 5/5 → 0/5，隱藏誘導指令遵循 6/6 → 0/6。

### 10. 權限與安全閘門

在自己的 Chrome 上，每個 Agent 動作會先對照落地網站檢查：**銀行、券商、加密交易所、政府身分網站預設先問你**（維護清單），刷卡欄位與下單前也會先問。你在側邊面板選「允許一次 / 這個站永遠允許 / 拒絕」；被攔的指令以 exit code 3 退出，Agent 執行 `chrome-use confirm <id>` 等你表決。企業可用 Chrome enterprise policy 釘選允許/封鎖網域與動作策略。

### 11. 其他能力速覽

| 功能 | 指令 |
|---|---|
| 批次動作 | `batch "fill @e1 Ada" "click @e2 --observe"` |
| 有界腳本流程 | `script`（observe/decide/act/verify，支援 JSON op-list 與 JS） |
| 網路攔截 | `network route "*/api/me" --body '...'`（mock／改寫／封鎖）、讀取跨域 frame 的 response body |
| 下載 | `download @e2 ./video.mp4`（沿用登入 cookie，不動目前分頁） |
| 裝置模擬 | `set device "iPhone 13"` / `set device off` |
| 原生對話框 | `dialog accept|dismiss` |
| 分頁收養 | `tab adopt <url>` 把已開的分頁掛進 session；`--follow` 跟隨點擊新開的分頁 |
| 截圖標註 | `screenshot --annotate`（編號標籤畫在 CLI 端，不碰頁面 DOM） |
| CAPTCHA 嘗試 | `solve-slider`（滑塊/旋轉驗證碼）、截圖引導的圖示點選；解不了明確交接給你 |
| 多 profile 路由 | 搭配作者的另一個 macOS 工具 ChooseBrowser：依站點規則自動選 Chrome profile |
| 測試與稽核 | `chrome-use test`（YAML 可重跑套件）、`chrome-use a11y`（axe-core 無障礙稽核） |
| HTTP API | 每個 session 的 stream port 上有版本化 `/api/v1` |
| 實驗性 Agent loop | `jev run --goal "..."`：TypeSafe Jev 驅動目標到完成，附各階段計時剖析 |

## 六、`*-use` 家族

chrome-use 屬於一組「給 AI Agent 一隻手」的小 CLI 家族，全部同樣形態：`install.sh` 安裝、`npx skills add` 教會 Agent、stdout 輸出 JSON：

| Repo | 給 Agent 的能力 |
|---|---|
| mail-use | Gmail / QQ / 163 / 任意 IMAP 的收發與分類 |
| iphone-use | 真實 iPhone：點擊、輸入、截圖、抓裝置資料 |
| wechat-use / discord-use | 微信（macOS）/ Discord 訊息操作 |
| cookie-use | 一站多帳號：捕捉、切換、套用 session |
| bitwarden-use | Bitwarden/Vaultwarden headless passkey 登入 |
| chatgpt-use | 用 ChatGPT 訂閱當 coding agent 後端，免 API key |
| computer-use | macOS 桌面本身 |

## 七、開發與維運面向

- **發布節奏極快**：CHANGELOG 從 1.5.283 到 1.5.290，近期幾乎每天發版；`chrome-use upgrade` 會同時更新二進位與各 runner 裡已安裝的 skill 複本（可 `CHROME_USE_AUTO_UPGRADE=0` 關閉）。
- **文件極其完整**：官方站有中英雙語 40+ 頁（commands、sessions、stealth、permissions、mcp、teach、inspect…），README 本身 105 KB，連「視窗最小化時截圖如何處理」這種細節都有規格化行為描述。
- **工程紀律**：`AGENTS.md` 明文兩條鐵律——「絕不發布靜默成功」（每個失敗都要有明確錯誤碼與 `retryable` 標記）與「誠實量測效能」。JSON 回覆附 `cdpMs/cdpBusyMs/nonCdpMs` 計時剖析。
- **商業模式**：Apache-2.0 開源 + README 廣告位 + 付費設定服務 + 贊助；本體無付费功能分割。

## 八、總結評價

**亮點**

1. 「真實已登入瀏覽器 + 零彈窗 + 零注入指紋」這個組合，目前只有它與 Claude in Chrome 做到，而它不綁定單一 App——任何 Agent 都能用；
2. 安全設計成熟：敏感站點閘門、提示注入過濾、密碼庫整合（明文不過手）、per-session 分頁隔離；
3. 「示範教學零模型重播」與「Inspect & Ask 點元素改程式碼」是兩個非常有創意的差異化功能；
4. 文檔品質與工程誠實度（失敗語意、計時剖析、實測數據附證據連結）遠超多數同類專案。

**限制與注意**

1. 擴充仍走 `chrome.debugger`，Chrome 會顯示「開始偵錯此瀏覽器」黃色橫條（`extension connect --silent` 可移除，需重啟一次 Chrome）；
2. 反偵測是「實測數據、非保證」——README 自己反覆聲明 Cloudflare 通關與帳號安全取決於站點、主機的顯示卡、網路與瀏覽器版本；
3. 多 profile 路由（ChooseBrowser）與部分原生整合僅限 macOS；Windows 功能面靠持續發版追平中；
4. 專案極年輕（2026-01 創建）、發版快，API 行為細節非常多，依賴時建議鎖版本。

**適合**：要讓 coding agent / 自動化腳本操作「需要登入的真實網站」的開發者；在意指紋與反爬牆的抓取場景；想把瀏覽器能力以 MCP 掛進 Claude Desktop / n8n 的團隊。
**不適合**：需要無頭大規模平行爬蟲（數百實例）的場景——那仍是 Playwright cluster 的地盤；chrome-use 的定位是「一個 Agent 一隻手，看著它工作」。

---

*資料來源：GitHub API、README.md（105 KB）、CHANGELOG.md、docs/en 目錄與官方文件站，分析日期 2026-11-09。Star 數為當日快照。*
