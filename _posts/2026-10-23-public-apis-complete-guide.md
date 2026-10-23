---
title: public-apis 完整介紹 — GitHub 最大的免費 API 清單（49 萬 Stars）
date: 2026-10-23
description: public-apis/public-apis 專案完整解析：2,100+ 個免費公開 API、50 大分類、Auth/HTTPS/CORS 欄位體系、MCP Servers 新區塊與貢獻規則
tags: [API, GitHub, 免費API, 開發者工具, MCP, 開源專案]
---

# public-apis 完整介紹 — GitHub 最大的免費 API 清單

![Star 歷史](/assets/images/public-apis/star-history.svg)

## 專案總覽

**Public APIs**（[public-apis/public-apis](https://github.com/public-apis/public-apis)）是 GitHub 上最知名、星數最高的 API 目錄，自我定位只有一句話：**「A collective list of free APIs」**——由社群人手維護的免費 API 集合清單。2016 年 3 月建立，至今仍是整個開發者生態的「免費 API 百科全書」。

與付費工具目錄不同，這裡的收錄門檻明確：**必須完全免費、或至少有免費額度（free tier）**，且不能依賴購買硬體／服務才能使用。行銷性質的 PR 會被直接拒絕。

## 📊 基本資訊

| 項目 | 數值 |
|------|------|
| GitHub Stars | **491,441** ⭐（GitHub 全站前段班） |
| Forks | 54,657 |
| Open Issues | 2,322 |
| 建立時間 | 2016-03-20 |
| 最後推送 | 2026-10-21（活躍維護中） |
| License | **MIT** |
| 主要語言 | Python（僅指檢查腳本，內容為 Markdown） |
| API 條目數 | **約 2,170 個**（實數自 README 表格） |
| 分類數 | **50** |
| MCP Server 條目 | 22 個（新區塊） |

## 🗂️ 50 大分類與條目數

每條 API 以固定欄位的 Markdown 表格列呈現。以下是各分類的實際條目數（依數量排序，前 20）：

| 分類 | 條目數 | 分類 | 條目數 |
|------|-------:|------|-------:|
| Development 開發 | **216** | Health 健康 | 47 |
| Government 政府 | **126** | Weather 天氣 | 47 |
| Games & Comics | 111 | Business 商業 | 44 |
| Geocoding 地理編碼 | **111** | Email | 37 |
| Cryptocurrency 加密貨幣 | 96 | Photography 攝影 | 37 |
| Finance 金融 | 96 | Test Data 測試資料 | 37 |
| Transportation 交通 | 95 | Jobs 職缺 | 36 |
| Open Data 開放資料 | 78 | Food & Drink | 35 |
| Sports & Fitness | 66 | Music 音樂 | 35 |
| Security 資安 | 61 | Art & Design | 31 |
| Science & Math | 59 | Environment 環境 | 30 |
| Social 社群 | 58 | Shopping 購物 | 28 |
| Video 影片 | 58 | Currency Exchange 匯率 | 27 |
| Machine Learning | 54 | Books 書籍 | 26 |
| Documents & Productivity | 53 | News 新聞 | 26 |

其餘分類：Animals、Anime、Anti-Malware、Authentication & Authorization、Blockchain、Calendar、Cloud Storage & File Sharing、Continuous Integration、Data Validation、Dictionaries、Entertainment、Events、Personality、Phone、Patent、Programming、Text Analysis、Tracking、URL Shorteners、Vehicle 等。

## 📋 條目格式：五個關鍵欄位

這是在別處看不到的實用設計——每個 API 標註了整合時最需要預先知道的屬性：

```
| API | Description | Auth | HTTPS | CORS |
| [NASA](https://api.nasa.gov) | NASA data, including imagery | No | Yes | Yes |
```

| 欄位 | 意義 | 可接受值 |
|------|------|----------|
| **Auth** | 是否需要驗證 | `No` / `apiKey` / `OAuth` / `User-Agent` / `X-Mashape-Key` |
| **HTTPS** | 是否支援 HTTPS | Yes / No |
| **CORS** | 瀏覽器能否直接呼叫 | Yes / No / Unknown（無 CORS 的 API 只能 server 端用） |

`Auth: No` + `CORS: Yes` 的組合最適合前端直接試作，例如 Cat Facts、Dog CEO、HTTP Cat 這類。

## 🤖 新動態：MCP Servers 區塊（22 個）

2026 年起 README 新增獨立的 **MCP Servers** 章節，收錄可掛進 **Claude、Cursor、VS Code** 等 AI 代理客戶端的 Model Context Protocol server。因為 MCP 是「安裝進 client」而非 HTTP 呼叫，欄位改為 **Auth / Transport（stdio、HTTP）/ Install 連結**（Glama、Cursor plugin、npm、MCP Registry）。

例如：IPstack MCP（IP 地理定位）、Catastro GPS（29 國地籍查詢）、Recalls API（美國 9 機構商品召回查詢）等——對 AI 代理開發者等於一份經過社群審核的 tool 目錄。

## 💰 APILayer 贊助關係

README 頂部有持續的 **APILayer** 贊助區塊（IPstack、Serpstack、Scrapestack 等產品），repo homepage 也帶 APILayer referral 連結。APILayer 員工與社群共同維護清單，但貢獻政策明文禁止行銷型 PR、只收免費 API——贊助商產品與社群目錄在表格上是分離開的，可信度維持得不錯。

![APILayer banner](/assets/images/public-apis/apilayer-banner.png)

## 🤝 貢獻規則（CONTRIBUTING.md 重點）

1. **只收免費 API**：完全免費或至少 free tier；需先買設備才能用的 API（如智慧插座控制 API）會被拒
2. **拒絕行銷 PR**：為公司付費產品打廣告的 PR 一律不收
3. 依指定表格格式提交，Auth/CORS 欄位只能用規定值
4. 建議附 Postman collection 的「Run in Postman」按鈕
5. MCP server 走獨立格式與章節

另有配套專案 [davemachado/public-api](https://github.com/davemachado/public-api)——把這份清單本身包裝成一個 JSON API（`https://api.publicapis.org/entries`），可直接程式化查詢。

## ✅ 優點 / ⚠️ 限制

| 面向 | 評價 |
|------|------|
| 品質篩選 | 人工策展＋免費門檻＋反行銷政策，目錄可信度高 |
| 實用欄位 | Auth/HTTPS/CORS 標註省下大量試錯時間 |
| 規模與廣度 | 2,170+ 條目、50 分類，涵蓋政府、金融、地理、天氣等主流需求 |
| 生態完整 | 清單本身還有 JSON API 版可供程式查詢 |
| ⚠️ 更新速度 | 人手維護＋2,300+ open issues：死鏈與過時條目難以及時清除，使用前仍需自行驗證連結 |
| ⚠️ 無品質分級 | 不收付費 API，但免費 API 之間的穩定性、rate limit 差異不會標出來 |
| ⚠️ 英文為主 | 描述全為英文，無繁中在地資源分類（如台灣政府 Open Data 只零星出現） |

## 🆚 與 API Mega List 比較

兩份目錄定位互補（本站另有 [API Mega List 完整介紹](/api-mega-list-complete-guide/)）：

| | public-apis | API Mega List |
|---|---|---|
| Stars | 491K | 8.1K |
| 條目 | ~2,170 | 11,860 |
| 內容本質 | 免費公開 API（人工策展） | Apify Actors 為主（多為付費按次） |
| 商業模式 | APILayer 贊助（目錄本身中立） | 贊助置入＋推薦碼抽佣 |
| 適用情境 | 前端試作、side project、免費資料來源 | 爬蟲、名單生成、规模化自動化 |

## 🚀 使用建議

1. 從 README 的 Index 或分類錨點進入；表格可用瀏覽器 Ctrl+F 搜關鍵字。
2. 需要程式化存取時用 [publicapis.org](https://api.publicapis.org/entries) JSON API。
3. `CORS: No` 的 API 記得走後端 proxy。
4. 把清單當「發現層」，正式整合前驗證 rate limit、SLA 與授權條款。

## 🔗 參考連結

- 專案首頁：<https://github.com/public-apis/public-apis>
- 貢獻指南：<https://github.com/public-apis/public-apis/blob/master/CONTRIBUTING.md>
- 清單的 JSON API：<https://github.com/davemachado/public-api>
- MCP 官方文件：<https://modelcontextprotocol.io>
