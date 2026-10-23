---
title: API Mega List 完整介紹 — GitHub 上最大的 API 目錄（8.1K Stars）
date: 2026-10-23
description: cporter202/API-mega-list 專案完整解析：11,860 個 API、24 大分類、MCP Servers、贊助合作模式與使用建議
tags: [API, GitHub, Apify, MCP, 開發者工具, AI, 爬蟲, 開源專案]
---

# API Mega List 完整介紹 — GitHub 上最大的 API 目錄

![API Mega List](/assets/images/api-mega-list/star-history.svg)

## 專案總覽

**API Mega List**（[cporter202/API-mega-list](https://github.com/cporter202/API-mega-list)）宣稱是 GitHub 上最全面的 API 收藏目錄，由開發者 **Chris Porter（cporter202）** 於 2025 年 12 月建立，收錄了 **11,860 個核心目錄 API**，外加 **200 個贊助合作夥伴條目**，涵蓋 **24 大分類**。

這是一個**純 Markdown 策展型專案**——不需要安裝任何东西，直接瀏覽 README 與各分類資料夾即可找到可用的 API。絕大多數條目指向 **Apify 平台上的 Actors**（雲端網頁抓取／自動化服務），連結均帶有推薦碼（referral code）。

## 📊 基本資訊

| 項目 | 數值 |
|------|------|
| GitHub Stars | **8,116** ⭐ |
| Forks | 1,577 |
| 建立時間 | 2025-12-09 |
| 最後推送 | 2026-10-20（持續維護中） |
| 主要語言 | JavaScript（僅指工具腳本，內容為 Markdown） |
| License | **無授權條款** |
| 核心 API 數 | 11,860 |
| 贊助條目 | 200 |
| 分類數 | 24 |
| Trendshift 成績 | 当日 / 当周 JavaScript _repo_ 第 1 名、当月第 3 名 |

> ⚠️ 注意：README 內的「Collection Statistics」表格寫的最後更新日是 2026-07-23，但 repo 實際持續推送更新（最後推送 2026-10-20），統計表可能落後於實際內容。

## 🗂️ 24 大分類一覽

每個分類是 repo 裡一個獨立資料夾（如 `ai-apis-1555/`），資料夾名稱直接標註 API 數量：

| 分類 | API 數 | 說明 |
|------|-------:|------|
| Automation（自動化） | **5,653** | 最大分類：工作流、瀏覽器自動化、排程任務 |
| Lead Generation（名單生成） | **4,431** | B2B 聯絡人、企業資料、銷售線索抓取 |
| Developer Tools（開發者工具） | **4,065** | 測試、部署、程式碼相關 API |
| Ecommerce（電商） | **2,245** | Amazon、Shopify、競品價格與評價抓取 |
| Other（其他） | 1,944 | 未歸類條目 |
| AI | **1,555** | AI 代理工具、LLM 資料源、AI 生成器 |
| Jobs（職缺） | 1,149 | 求職網站抓取、人才資料 |
| Real Estate（房地產） | 1,089 | 房產列表、市場數據 |
| SEO Tools | 903 | 關鍵字、排名、網站审计 |
| Integrations（整合） | 841 | SaaS 服務間串接 |
| Social Media（社群媒體） | **2,786** | X/Twitter、Instagram、TikTok、YouTube 抓取 |
| News（新聞） | 537 | 新聞源與輿情監控 |
| Business（商業） | 514 | 企業登記、財務資料 |
| Travel（旅遊） | 493 | 機票、飯店、評論抓取 |
| Videos（影片） | 705 | YouTube 轉錄、影片下載、字幕 |
| MCP Servers | **289** | 供 AI 代理連接的 MCP server 目錄 |
| Marketing（行銷） | 290 | 廣告文案、社群經營工具 |
| Agents（AI 代理） | 623 | 代理專用工具與資料源 |
| Open Source | 84 | 開源 API 收錄 |
| Education | 46 | 教育資源 |
| Sports | 21 | 賽事比分、統計 |
| For Creators | 16 | 創作者經濟工具 |
| Games | 6 | 遊戲資料 |

![AI 工具包横幅](/assets/images/api-mega-list/ai-toolkit-banner.png)

## 🤖 亮點：MCP Servers 分類（289 個）

這是最貼近當前 AI 開發潮流的分類——收錄可直接掛到 **Claude Desktop、Cursor、n8n、OpenAI Agents SDK、Vercel AI SDK** 的 MCP server，例如：

- ⚖️ **Legal MCP** — AI 檢索公開法院紀錄，做法律研究與盡職調查
- ⚽ **Sports MCP** — NFL/NBA/MLB/NHL 即時比分、賽程、球員數據
- ✈️ **Travel MCP** — 跨 Booking.com、Airbnb、TripAdvisor 搜尋飯店與機票（按結果計費）
- 🌤️ **Weather MCP** — AI 天氣預報與氣候數據

對正在搭 AI 代理的開發者，這個分類等於一份現成的 tool 目錄。

## 🔧 Repo 結構與維護方式

```
API-mega-list/
├── README.md                  # 主目錄（3.2 MB！所有分類的前幾十條直接內嵌）
├── 00-featured-apis/          # 贊助合作夥伴的精選 collections
├── SPONSORED_PARTNERS.md      # 贊助-placement 政策
├── FOLLOW_CREATOR.md          # 作者社群連結
├── settings/
│   ├── APIFY_ACTORS.md        # 11,663 個 Apify Actors 完整清單（9.9 MB）
│   ├── fetch_apify_actors.js  # 從 Apify 抓 actor 清單
│   ├── generate_readme_clean.js  # 自動生成 README／分類表
│   └── validate_partner_collections.js  # 驗證合作條目連結
├── agents-apis-623/ … sports-apis-21/    # 24 個分類資料夾
```

維護是**半自動化**的：`settings/` 底下的 Node.js 腳本定期從 Apify 平台拉取全部 actors，過濾測試／佔位條目（如 "My Actor"、"test crawler"），再按分類重新生成 README 與各資料夾的表格——這就是它號稱「每日更新」的機制。

## 💰 商業模式：贊助合作（務必了解）

這是評價這個 repo 時**不能忽略的一節**。`SPONSORED_PARTNERS.md` 明確定價了付費置入規則：

- 合作夥伴可**付費**取得收錄與 banner 曝光（如 APIMesa：150+ 個按次計費 API，一個 key 通用）
- 每個贊助商有**獨立 collection**、依名稱字母序排列、不宣稱「最佳／首選供應商」
- 平台會提供 30/60/90 天的推薦成效報表（造訪、註冊、轉換）給贊助商
- 主 README 與精選區均嵌入贊助横幅

![APIMesa 贊助 banner](/assets/images/api-mega-list/apimesa-promo-banner.png)

此外幾乎所有 Apify 連結都帶 `?fpr=` 推薦碼——透過它註冊／消費，作者可抽佣。這是 awesome-list 生態常見的變現方式，**內容本身仍然可用**，但「收錄順序 ≠ 品質排名」，且部分條目是付費服務（按結果／按次計價）。

## ✅ 優點 / ⚠️ 限制

| 面向 | 評價 |
|------|------|
| 規模 | 11,860 個條目、24 分類，目前 GitHub 上最大的 API 目錄之一 |
| 即時性 | 腳本驅動、持續更新（最後推送 2026-10-20） |
| 实用性 | MCP Servers、爬蟲、名單生成分類對 AI/自動化開發者直接有幫助 |
| ⚠️ 偏斜 | 絕大多數條目是 **Apify Actors**（雲端付費平台），不是免費公開 API；找傳統免費 API（天氣、金融等）應改用 `public-apis/public-apis` |
| ⚠️ 變現 | 贊助置入 + 推薦碼抽佣，排序與曝光有商業因素 |
| ⚠️ 無授權 | repo 未設 license，引用內容需注意 |
| ⚠️ 品質 | 條目由自動腳本生成，描述多為供應商行銷文案，需自行驗證連結與品質 |

## 🆚 與其他 API 目錄比較

| Repo                    | Stars | 定位                          | 費用       |
| ----------------------- | ----: | --------------------------- | -------- |
| **API Mega List**       |  8.1K | Apify Actors 為主的超大策展目錄＋贊助模式 | 多為付費按次服務 |
| public-apis/public-apis | 40 萬級 | 免費公開 API 百科（天气、金融、政府資料）     | 免費為主     |
| apis.guru               |     — | REST/GraphQL OpenAPI 規範搜尋引擎 | 混合       |

三者互補：要**免費公開 API** 去 public-apis；要**爬蟲／自動化／AI 代理工具**（願意付費按次使用）這本 mega list 是現成索引。

## 🚀 使用建議

1. **別從 3.2 MB 的主 README 讀起**——直接進分類資料夾的 `README.md`，或用 GitHub 頁面右側檔案樹跳轉。
2. AI 代理開發者先看 `mcp-servers-apis-289/`。
3. 把此目錄當「發現層」：找到候選後到供應商頁面比價、試 playground，再決定是否接入。
4. 注意 Apify 連結的 `fpr=` 參數不影響功能，只是推薦歸因。

## 🔗 參考連結

- 專案首頁：<https://github.com/cporter202/API-mega-list>
- 贊助政策：[SPONSORED_PARTNERS.md](https://github.com/cporter202/API-mega-list/blob/main/SPONSORED_PARTNERS.md)
- MCP Servers 分類：<https://github.com/cporter202/API-mega-list/tree/main/mcp-servers-apis-289>
- 免費 API 對照目錄：<https://github.com/public-apis/public-apis>
