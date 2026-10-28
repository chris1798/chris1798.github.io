---
title: "text-to-cad v0.8 功能全解析：AI Agent 的本機 CAD 工作流"
date: 2026-10-28
description: earthtojake/text-to-cad 最新（v0.8.1，23.8k stars）功能整理：12 個 Agent Skills、cadgen 統一引擎、STEP/GLB/STL/3MF 輸出、DfAM/DFM 製造檢查、工程圖、G-code 切片、Bambu 列印、機器人 URDF/SRDF/SDF，以及各 Agent 平台安裝矩陣與 v0.8 重大變更。
tags: [github, ai-agents, cad, 3d-printing, mcp, build123d, robotics, cnc, step]
image: /assets/images/text-to-cad/logo-stacked.png
---

# text-to-cad v0.8 功能全解析：AI Agent 的本機 CAD 工作流

<div align="center">
  <img src="/assets/images/text-to-cad/logo-stacked.png" alt="text-to-cad" width="640">
</div>

**text-to-cad** 是一個開源的 AI Agent 外掛／技能套件，口號是「用 AI 設計實體產品」（Design physical products with AI）。它讓 Claude Code、Codex、Cursor、Gemini、Grok 等代理能在**本機**把自然語言（甚至圖片）變成真正的 3D 模型——STEP、GLB、STL、3MF 檔——並一路做到製造可行性檢查、工程圖輸出、切片產生 G-code，直接接上 3D 列印、金屬板材與 CNC 加工流程。

本文是 2026-10-15 舊文的更新版，以 **v0.8.1**（2026-10-27 發布）與當前倉庫狀態重寫，重點補上 v0.8 的架構大改與新增技能。

## 一、專案基本資料

| 專案資訊 | 數值 |
|---|---|
| 倉庫 | [github.com/earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad) |
| 官方網站 | [www.texttocad.dev](https://www.texttocad.dev) |
| Stars / Forks | 23,793 / 2,297（2026-10-28 實測） |
| 授權 | MIT |
| 主要語言 | Python（cadgen 引擎）＋ TypeScript（檢視器／UI） |
| 目前版本 | v0.8.1（2026-10-27），發版頻率極高（一週內 0.7.24→0.8.1） |
| 建立時間 | 2026-04-22 |
| PyPI 套件 | `cadgen`（代理執行時透過 [uv](https://docs.astral.sh/uv/) 安裝，Python 3.11+） |
| 倉庫規模 | 約 2,288 個檔案：`packages/`（cadgen 引擎＋檢視器核心）1,049、`skills/` 121、`tests/` 242、`models/` 547 |

<div align="center">
  <img src="/assets/images/text-to-cad/star-history.svg" alt="star history" width="720">
</div>

半年內從零衝到 2.3 萬顆星，是 2026 年 AI×硬體設計領域最熱門的開源專案之一。

## 二、核心原理：Agent 寫程式碼，CAD 內核出模型

它**不用**神經網路直接生成幾何（與學術界的 Text2CAD 路線完全不同）。流程是確定性的：

```
使用者自然語言（或圖片參考）
        │
        ▼
AI Agent（Claude / Codex / Gemini / Grok…）
        │  撰寫 build123d 參數化 Python 腳本
        ▼
cadgen 引擎（Open CASCADE / OCCT）
        │  python model.py → .xbf 文件 ＋ STEP/GLB/STL/3MF
        ▼
CAD 檢視器（Agent 應用內卡片或瀏覽器）即時跟隨每次重建
```

1. 每個模型都是一支 **build123d** Python 腳本（build123d 建立在 Open CASCADE 之上）。
2. 執行腳本後，cadgen 引擎把模型建成 `.xbf` 文件（含零件、名稱、顏色、材質、接合），並輸出腳本宣告的 STEP / GLB / STL / 3MF 檔。引擎將每個模型的工作常駐記憶體，改一行程式碼只重建變動的部分。
3. CAD 檢視器在 Agent 應用內（或瀏覽器）即時顯示模型，並跟隨每次重建更新。

因為模型是**參數化程式碼**，結果可重現、可量測、可版本控制，Agent 也能讀回檢視器中你選取的零件繼續修改——這是它比「AI 生成網格」路線更受工程界歡迎的關鍵。

## 三、v0.8 的重大變更

0.8 是一個**刻意不做向後相容**的大版本（無 shim、無別名、無 codemod），把 0.7 的檔案管線整合成**單一引擎**：

| 面向 | 0.7 舊做法 | 0.8 新做法 |
|---|---|---|
| 執行模型 | `uvx --from cadgen==0.7.x python src/model.py` | `cadgen run src/model.py`（腳本、命令、CAD 應用共用一個常駐引擎） |
| 模型宣告 | 各類裝飾器參數 | 統一 `@model` 裝飾器；執行時不寫檔 |
| 輸出 | 執行即寫出檔案＋sidecar | 檢視器頁面的下載按鈕選格式；`cadgen export <id> part.step`；專案交付物寫在 `exports.py` |
| 機構／動態 | mates、couplings、poses、JS clips | build123d 接合＋STEP AP242 機構詞彙（`cadgen.ap242`） |
| 展示動畫 | 額外機制 | GLB 自帶動畫通道（`cadgen.gltf`） |
| 快照渲染 | 依賴 Playwright 無頭瀏覽器 | 改由 OCCT 直接繪製，**移除 Playwright 依賴** |
| 顏色 | 多种規格 | 統一 sRGB hex |

官方提供[逐步遷移指南](https://github.com/earthtojake/text-to-cad/blob/main/docs/migrations/migrating-0.7-to-0.8.md)，装了 CAD skill 的 Agent 可以自己照著指南把舊專案帶過來。升級偵測機制：cadgen 每天最多向 `api.texttocad.dev/v1/versions` 發一次匿名請求（不帶 ID、路徑或任何個人資料，CI 中永不檢查），有新版時檢視器會出現藍色更新按鈕，按「Send to agent」直接把更新指令貼進對話；`CADGEN_UPDATE_CHECK=0` 可關閉。

## 四、12 個 Agent Skills 一覽

安裝後，代理取得針對 CAD、製造、機器人描述檔、模擬與本機檢視的專業工作流：

| Skill | 功能 |
|---|---|
| **CAD** | 從自然語言或圖片建立／編輯 CAD 模型，產為 Python 腳本＋XBF 文件，匯出 STEP、STL、3MF、GLB；附 build123d 建模、運動學、定位、專案結構、快照審查等參考文件 |
| **step.parts** | 搜尋現成標準件 STEP 檔：螺絲、軸承、馬達、接頭等（附下載腳本與校驗和檢查） |
| **Engineering Drawing** | 由零件產生帶標註的工程圖 PDF：多視圖、隱線、尺寸、孔位標註、標題欄 |
| **DXF** | 產生 2D DXF：擠型輪廓、板金模板、墊片、裁切排料圖 |
| **URDF** | 撰寫機器人結構檔：links、joints、極限、慣量、網格 |
| **SRDF** | 為 URDF 加上 MoveIt 規劃群組、末端效應器、姿態與碰撞規則 |
| **SDF** | 建立模擬器模型與世界：座標系、物理、感測器、燈光（Gazebo 系） |
| **SendCutSend** | 上傳 SendCutSend 前自動檢查 DXF／STEP 檔案合规性 |
| **DfAM Check** | 逐製程量測可列印性：壁厚、懸垂、支撐體積、建置方向 |
| **DFM** | 審查板金、CNC 加工或射出成型可行性；每項發現都附**實測證據**與引用的規則（從網格量測拔模角、倒勾、投影面積） |
| **G-code** | 用 OrcaSlicer＋你自己的列印機預設切片，產出列印機可用的 G-code |
| **Bambu Labs** | 經 Bambu Connect／官方 App／Bambu Studio 送印到 Bambu Lab 列印機 |

從「畫出齒輪箱」到「檢查能不能印」「產生加工圖」「切片」「按列印」，整條產品開發鏈路都在 Agent 對話裡完成。

<div align="center">
  <img src="/assets/images/text-to-cad/social-preview.png" alt="text-to-cad 模型展示" width="720">
</div>

## 五、支援的 Agent 平台與安裝矩陣

一個外掛 = skills＋CAD 伺服器（`cadgen mcp`）＋檢視器。官方建議的首選安裝法是直接把下面這段話貼給你的 Agent：

```text
Install text-to-cad from https://github.com/earthtojake/text-to-cad
```

自行安裝的平台指令矩陣：

| 平台 | 安裝指令 | 檢視器整合 |
|---|---|---|
| **Claude Code** | `claude plugin marketplace add earthtojake/text-to-cad#latest`＋`claude plugin install text-to-cad@earthtojake` | 對話內檢視器卡片；終端機則給瀏覽器連結 |
| **Claude Desktop** | 在 Settings → Developer → Edit Config 加入 `uvx … cadgen mcp` 的 mcpServers 設定 | 對話內卡片：可旋轉、加入 prompt、全尺寸開啟；Claude 能讀取你選取的零件 |
| **Codex** | 從 Codex 外掛目錄安裝，或 `codex plugin marketplace add earthtojake/text-to-cad --ref latest`＋`codex plugin add text-to-cad@earthtojake` | 側欄 CAD 面板、每個對話旁的 CAD 分頁、*Open with CAD* |
| **Cursor** | 共用 Claude Code 外掛；或 `git clone --depth 1 --branch latest … ~/.cursor/plugins/local/text-to-cad` | 同 Claude Code |
| **Grok Build** | `grok plugin install earthtojake/text-to-cad@latest --trust`＋`grok plugin enable text-to-cad` | 文字結果＋CAD Viewer 連結 |
| **Gemini CLI** | `gemini extensions install https://github.com/earthtojake/text-to-cad --ref latest --consent --auto-update` | 文字結果＋CAD Viewer 連結 |
| **其他 Agent** | `npx skills add earthtojake/text-to-cad#latest`（[skills.sh](https://skills.sh) 框架，可加 `-g -a <agent> -y` 免提問） | 瀏覽器 CAD Viewer（localhost 網頁應用） |

注意事項：

- 一個應用**只裝外掛或 skills 其中一種**，兩邊都裝會得到兩份相同的技能。
- 安裝指令帶 `#latest`／`--ref latest` 分支（只含外掛、每版上架 PyPI 後才更新）；不帶則裝開發中的 `main`。
- 更新：請 Agent 更新，或跑各平台的 update 指令後重啟；`npx skills` 路線要**重跑原 install 指令**（`skills update` 只刷新鎖檔內技能，會漏掉新版本新增的 skill）。
- 首次啟動會下載 CAD 執行時，需要網路；離線後一切功能照常。

## 六、輸出格式與文件型別

| 格式 | 用途 |
|---|---|
| **STEP**（.step/.stp，AP242） | 工業級實體模型交換，含機構詞彙，可進 SolidWorks／Fusion／板金加工 |
| **STL** | 3D 列印通用網格 |
| **3MF** | 現代列印封包格式 |
| **GLB** | 網頁／AR 展示，可含動畫通道 |
| **XBF**（.xbf） | cadgen 內部文件：零件、名稱、顏色、材質、接合，增量重建的載體 |
| **DXF** | 2D 切割／板金／雷射加工 |
| **PDF 工程圖** | 帶視圖、尺寸、孔位標註與標題欄的製造圖 |
| **G-code** | 列印機指令（OrcaSlicer 預設檔） |
| **URDF / SRDF / SDF** | 機器人結構、MoveIt 規劃、模擬世界 |

## 七、內建模型範例庫

倉庫 `models/` 目錄自帶 **405 支可執行模型腳本**（547 個檔案），全部是「腳本＝模型」的示範，涵蓋：

- **組裝類**：行星齒輪箱、六軸工業機械臂、人形機器人（研究型／雕塑型／緊湊款）、馬達機車頭連桿機器人、月球探測車轉角模組、火星車概念、渦輪扇引擎剖視模型、機械光圈快門、螺旋樓梯、肌腱驅動機械手末端
- **DFM 對比**：同一零件在 CNC／FDM／板金下的製程差異示範（附驗證腳本）
- **品牌 logo**：專案自身的 C / CAD / text-to-cad 立體 logo 模型

每支都是參數化 Python，Agent 可以直接讀取、修改、延伸——學習曲線最好的起點。

## 八、隱私與遙測

CAD 應用與瀏覽器檢視器**預設**傳送使用統計與當機報告，但官方把界線寫得很明白：

- 以隨機安裝 ID 標記；只送版本、安裝來源、OS／Agent 應用、工具呼叫次數與**固定詞彙的失敗原因**（如 "no file at that path"），絕不送訊息本文。
- **絕不**包含檔名、路徑、檔案內容或你的提示詞；使用者代碼在當機報告中僅以佔位符出現。
- 伺服器以 PostHog 儲存，來源國家由 IP 推得後即不保留 IP。
- 關閉方式：`cadgen telemetry off`、應用選單的 **Telemetry**、或請 Agent 關閉；關閉同時刪除已暫存的資料。`DO_NOT_TRACK=1`／`CADGEN_TELEMETRY=0` 為行程級開關；CI 與開發安裝預設不傳送。完整說明見[隱私政策](https://www.texttocad.dev/privacy-policy)。

## 九、已知坑：Windows 11 Smart App Control

CAD 內核 `OCP`（Open CASCADE 的 Python 綁定）的 wheel 附帶**未簽章的原生模組**。Windows 11 的 Smart App Control（全新安裝預設開啟）會攔截未簽章原生碼，導致所有 `cadgen` 命令與 `import build123d` 噴 `ImportError: DLL load failed while importing OCP`（事件檢視器 CodeIntegrity 事件 ID 3077）。`cadgen doctor` 會點名這個問題。

Smart App Control 沒有單例外許機制，只能二選一：

1. 關閉 Smart App Control（關閉後**只能重裝 Windows** 才能重新開啟）；或
2. 在 **WSL** 裡跑 CAD skills（SAC 不適用於 WSL）。

wheel 由 cadquery-ocp 專案建置，簽章不是 text-to-cad 倉庫端能解決的事。

## 十、與其他方案比較

| 方案 | 生成方式 | 可編輯性 | 製造級輸出 | 本機執行 |
|---|---|---|---|---|
| **text-to-cad** | LLM 寫 build123d 參數化程式碼，OCCT 確定性建模 | 高（程式碼即特徵樹） | STEP AP242／DXF／工程圖／G-code | ✅ 完全本機 |
| Text2CAD 系學術模型 | Transformer 直接生成 CAD 序列 | 低（黑箱輸出） | 精度有限 | 視實作 |
| Mesh 生成 AI（文生 3D） | 生成網格／高斯潑濺 | 極低（無特徵） | 不適用於工程 | 視服務 |
| CAD 廠商 Copilot（Fusion、SolidWorks 等） | 廠內 AI 輔助 | 高 | 高 | 封閉生態、綁訂閱 |

text-to-cad 的定位：**把「寫 CAD 程式碼」這件事外包給 Agent**，工具鏈（build123d、OCCT、OrcaSlicer、DXF）全部開源本機，輸出即製造級。

## 十一、參與開發

- 分支由 `main` 切出、PR 對 `main` 提出；本地開發與測試流程見 [CONTRIBUTING.md](https://github.com/earthtojake/text-to-cad/blob/main/CONTRIBUTING.md)，Agent 在倉庫內工作從 [AGENTS.md](https://github.com/earthtojake/text-to-cad/blob/main/AGENTS.md) 開始。
- 安全問題依 [SECURITY.md](https://github.com/earthtojake/text-to-cad/blob/main/SECURITY.md) 私密通報。
- 沒有你用的 Agent 外掛？[開 issue 要求](https://github.com/earthtojake/text-to-cad/issues/new?title=Plugin%20request%3A%20)。
- 專案接受 GitHub Sponsors 贊助。

## 參考連結

- 倉庫：https://github.com/earthtojake/text-to-cad
- 官方網站／安裝指引：https://www.texttocad.dev ／ https://www.texttocad.dev/install
- PyPI：https://pypi.org/project/cadgen/
- Skills 目錄：https://skills.sh/earthtojake/text-to-cad
- Codex 外掛目錄：https://chatgpt.com/plugins/plugins_6ac09476ef008191a35887b22b0d048a
- Discord：https://discord.gg/5FGB9DwJYU
- 0.7→0.8 遷移指南：https://github.com/earthtojake/text-to-cad/blob/main/docs/migrations/migrating-0.7-to-0.8.md
- 前篇（v0.7 時期）：[text-to-cad 專案完整解說](/text-to-cad-agent-cad/)
