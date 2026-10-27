---
title: "LinkSwift：九大网盘直链抓取，餵飽 IDM / Aria2 / Motrix 的油猴腳本"
date: 2026-10-27
description: 31k stars 的開源用戶腳本：在百度/阿里/夸克/123 等九大网盘網頁版注入「下載助手」按鈕，透過官方公開 API 取得真實直鏈，一鍵推送 IDM、Aria2 RPC、Motrix、比特彗星、cURL、AB Download Manager。
tags: [github, userscript, tampermonkey, netdisk, idm, aria2, motrix, opensource]
---

# LinkSwift：九大网盘直链抓取，餵飽 IDM / Aria2 / Motrix 的油猴腳本

**LinkSwift**（原名「（改）網盤直鏈下載助手」）是一個純 JavaScript 的瀏覽器用戶腳本：**打開任何网盘網頁版時注入一顆「下載助手」按鈕，點擊即透過各网盘官方公開 API 解析出真實下載直鏈**，再一鍵推送給你熟悉的下載器——IDM、Aria2、Motrix、比特彗星、cURL、AB Download Manager。不用裝任何客戶端程式，掛在 Tampermonkey / 腳本貓裡就跑。

## 專案概況

| 項目 | 資料 |
|---|---|
| 倉庫 | [github.com/hmjz100/LinkSwift](https://github.com/hmjz100/LinkSwift) |
| Star / Fork | **~31,000 / ~2,150**（2026-10-27 查證，Trendshift 上榜專案） |
| 語言 / 授權 | JavaScript / **AGPL-3.0** |
| 建立時間 | 2022-08-10，持續維護中（最後推送 2026-10-23） |
| 最新版本 | 正式版 v1.1.3（2026-02-16）、測試版 v1.1.4（2026-09-09，新增光鴨雲盤支援） |
| 貢獻者 | 8 位（主要為作者 hmjz100 一人維護） |
| 血統 | 基於油小猴的【網盤直鏈下載助手】（[syhyz1990/baiduyun](https://github.com/syhyz1990/baiduyun)）修改擴充 |
| 運行環境 | Chrome ≥76 / Edge ≥88 + Tampermonkey；Windows / Mac / Linux / Android 皆可用 |

## 支援的九大网盘

百度網盤、阿里雲盤、中國移動雲盤、天翼雲盤、迅雷雲盤、**光鴨雲盤**（v1.1.4 新增）、夸克網盤、UC 網盤、123 雲盤。

每次各家网盘改版（123 雲盤尤其「變來變去」），作者都會跟进適配——這正是這類腳本最核心的維護成本，也是它活了四年多、累積 31k 星的原因。

## 五種下載方式

安裝後在网盘頁面點選檔案 →「下載助手」→ 彈出視窗提供五條路徑：

| 按鈕 | 用途 |
|---|---|
| **API 下載** | 解析直鏈後呼叫 IDM / NDM / 瀏覽器下載；v1.1.2.1 起支援直接推送 IDM，v1.1.3 加入 IDM 客戶端設定（多實例選 client） |
| **Aria 下載** | 複製 aria2 命令列（含 Token、RPC 設定），可貼給 XDown / aria2 命令行 |
| **RPC 下載** | 直接推送到 Motrix / AriaNg / Aria2 Tools / NAS 上的 Aria2 佇列，多線程多塊下載 |
| **cURL 下載** | 複製完整 cURL 指令到終端機跑 |
| **BC 下載** | 推送比特彗星（BitComet）；v1.1.1 起 RPC 併入 Aria2、BC 獨立按鈕 |

另有 **AB Download Manager 推送**（v1.1.1.5 新增）、一鍵複製全部連結、從設置頁一鍵返回下載視窗不必重新取鏈。

## 附加功能：不只取直鏈

- **網盤介面美化/綠化**：精簡各网盘網頁的廣告與冗餘元素，支持深色模式（隨設置熱切換）、自訂主題色、適配 Dark Reader
- **多服務配置檔**：Aria2 RPC 可存多組（本機 NAS 雲端的），自由新增/刪除/切換
- **鏈接緩存**：取過的直鏈快取起來，重複下載不用重新解析
- **百度資料夾下載**：可在分享頁選資料夾整包取鏈
- **安全取向**：v1.1.1.6 起棄用百度网盘 BDUSS Cookie（等於交出帳號），改用權限較小的 AccessToken——這是全專案很重要的一次安全性重構
- **搭配腳本**：作者另有「123 雲盤會員青春版」「百度網盤會員青春版」「阿里雲盤會員青春版」等精簡版擴充腳本

## 安裝

需要 Tampermonkey（Chrome 線上商店有正式版與 BETA 版）或腳本貓，然後選一個來源一鍵安裝：

- **GitHub 國際**（正式版）：[（改）网盘直链下载助手.user.js](https://github.com/hmjz100/LinkSwift/raw/main/%EF%BC%88%E6%94%B9%EF%BC%89%E7%BD%91%E7%9B%98%E7%9B%B4%E9%93%BE%E4%B8%8B%E8%BD%BD%E5%8A%A9%E6%89%8B.user.js)
- **GitHub 金絲雀版**（dev 分支，最新功能但不穩定）：[raw/dev 版本](https://github.com/hmjz100/LinkSwift/raw/dev/%EF%BC%88%E6%94%B9%EF%BC%89%E7%BD%91%E7%9B%98%E7%9B%B4%E9%93%BE%E4%B8%8B%E8%BD%BD%E5%8A%A9%E6%89%8B.user.js)
- **腳本貓 國內**：[scriptcat.org/scripts/code/1604](https://scriptcat.org/scripts/code/1604/LinkSwift.user.js)
- **OpenUserJS**（更新較慢）：[openuserjs.org/install/hmjz100/LinkSwift.user.js](https://openuserjs.org/install/hmjz100/LinkSwift.user.js)

⚠️ 作者明確提醒：**不要從 GreasyFork 安裝**（黑產仿冒與刷子氾濫，可能拿到被動手腳且無法及時更新）；官方僅發布於 GitHub、Gitee、腳本貓、OpenUserJS 四處。Bug 回饋僅受理 GitHub Issues。

## 重要免責與合規立場

README 開頭两段 IMPORTANT 值得全文化理解：

- 所有下載鏈接**均基於各大网盘服務商公開的 API 接口**取得；專案未承諾、宣傳或實現任何「破解限速」
- 實際速度快慢取決於服務商策略、頻寬調整與本地網路，**不是腳本破解了什麼**
- 第三方行銷文案（「加速下載」「速度起飛」「限速破解」等）不代表本專案立場

技術中立 + 官方公開接口 + 放棄 BDUSS 改用 AccessToken，是這個專案能長期存在的合規基礎。

## 與同類產品比較

| | LinkSwift | 原網盤直鏈下載助手（syhyz1990/baiduyun） | 各网盘官方客戶端 |
|---|---|---|---|
| 支援网盘 | **9 家**（含光鴨、UC、123） | 數家，更新停滯 | 僅自家 |
| 下載器整合 | IDM / Aria2 RPC / Motrix / BC / cURL / ABDM | 基本取鏈為主 | 內建下載（限速） |
| 介面美化 | ✅ 綠化、深色、主題色 | 部分 | — |
| 多 RPC 配置 | ✅ | ❌ | — |
| 維護狀態 | 活躍（2026-10 仍在推） | 停更，由 LinkSwift 接手生態 | — |
| 需裝客戶端 | ❌（瀏覽器腳本） | ❌ | ✅ |

## 誰適合用

- 有大檔下載需求、受夠官方客戶端限速的人（配合 IDM/Aria2 多線程拉滿自己的頻寬）
- NAS 玩家：RPC 推送直鏈給群暉 / 威聯通的 Aria2 / Motrix，離線下載网盘資源
- 不想開官方客戶端、只想在瀏覽器解決的下載者
- 注意：需登入网盘帳號；解析依賴各家公開接口，**网盘改版期間可能短暫失效**，跟緊正式版更新即可

## 參考資料

- GitHub：[https://github.com/hmjz100/LinkSwift](https://github.com/hmjz100/LinkSwift)
- 上游原專案：[syhyz1990/baiduyun（網盤直鏈下載助手）](https://github.com/syhyz1990/baiduyun)
- 腳本貓頁面：[https://scriptcat.org/script-show-page/1604](https://scriptcat.org/script-show-page/1604)
- OpenUserJS：[https://openuserjs.org/scripts/hmjz100/LinkSwift](https://openuserjs.org/scripts/hmjz100/LinkSwift)
- 第三方評測：[異次元軟體世界介紹文](https://www.iplaysoft.com/linkswift.html)
