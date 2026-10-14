---
title: "text-to-cad 專案完整解說：讓 AI Agent 具備 CAD 超能力"
date: 2026-10-15
description: earthtojake/text-to-cad（20k+ stars）完整分析：11 個 CAD Skills、cadgen 引擎、build123d/OpenCascade 架構、製造檢查、3D 列印與 CNC 整合，以及各 Agent 平台的安裝方式。
tags: [github, ai-agents, cad, 3d-printing, mcp, build123d, robotics, cnc]
image: /assets/images/text-to-cad/logo.svg
---

# text-to-cad 專案完整解說：讓 AI Agent 具備 CAD 超能力

<div align="center">
  <img src="/assets/images/text-to-cad/logo.svg" alt="text-to-cad" width="700">
</div>

**text-to-cad** 是一個開源的「Agent 外掛套件」，口號是 *Give your agent CAD superpowers*（給你的 AI 代理 CAD 超能力）。它讓 Claude Code、Codex、Cursor、Gemini、Grok 等 AI 代理能在**本機**生成 3D 模型（STEP / GLB / STL / 3MF），並進一步做製造可行性檢查（DfAM/DFM）、產生工程圖、切片輸送 G-code，甚至直接連接到 3D 列印、金屬板材與 CNC 加工服務。

| 專案資訊 | 數值 |
|---|---|
| 倉庫 | [github.com/earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad) |
| 官方文件 | [www.texttocad.dev](https://www.texttocad.dev) |
| Stars / Forks | 約 20,258 / 1,994（2026-10 實測） |
| 授權 | MIT |
| 主要語言 | Python（cadgen 引擎）+ TypeScript（UI/核心） |
| 目前版本 | v0.7.21（2026-10-11 發布，幾乎每日發版） |
| 核心依賴 | build123d 0.11、Open CASCADE 7.9（cadquery-ocp-novtk）、ezdxf、Playwright |
| PyPI 套件 | `cadgen` |
| 建立時間 | 2026-04-22 |

> 注意：此專案與 2024 年 NeurIPS 的學術研究 [SadilKhan/Text2CAD](https://github.com/SadilKhan/Text2CAD)（用 Transformer 從文字生成 CAD 序列）是**完全不同的東西**。text-to-cad 不用深度學習模型生成幾何，而是讓 LLM Agent 撰寫 **build123d Python 參數化程式碼**，再由確定性的 CAD 内核（Open CASCADE）編譯成實體模型——結果可重現、可量測、可修改。

## 一、它到底做什麼？

傳統「text-to-CAD」研究走的是神經網路直接生成幾何的路線，精度與可編輯性都有限。text-to-cad 的哲學不同：

```
使用者自然語言（或圖片）
        │
        ▼
AI Agent（Claude / Codex / Gemini…）
        │  撰寫參數化 Python 模型（@step / @dxf 裝飾器）
        ▼
cadgen 引擎（build123d + Open CASCADE）
        │  確定性編譯
        ▼
STEP / STL / 3MF / GLB / DXF / PDF 工程圖 / G-code
        │
        ▼
CAD Viewer 本機網頁預覽 → 3D 列印 / CNC / 水刀加工
```

三個關鍵設計：

1. **模型就是程式碼**：每個 CAD 模型是一個純 Python 檔，裡面一個帶裝飾器的無參數函數回傳 build123d 形狀。改尺寸＝改參數重跑，天然參數化、可版本控制。
2. **生成檔與原始碼完全脫鉤**（cadgen 的「第一定律」）：STEP/STL 等產物加上一個 sidecar JSON 可獨立被檢視、量測、快照，刪掉所有 `.py` 也不影響渲染。
3. **本地優先**：整個流程離線可跑（首次下載 runtime 除外），檔案、路徑、prompt 都不上傳。

## 二、倉庫架構

這是個 monorepo，同時是「Agent 插件市場包」+「Python 引擎」+「Web 應用」：

```
text-to-cad/
├── .claude-plugin/ .codex-plugin/ .cursor-plugin/   ← 各 Agent 平台的插件清單
├── mcp.json / claude.mcp.json / codex.mcp.json      ← MCP 伺服器設定
├── gemini-extension.json                            ← Gemini 擴充套件
├── skills/                    ← 11 個 Agent Skills（核心資產）
│   ├── cad/  dxf/  step-parts/  engineering-drawing/
│   ├── urdf/ srdf/ sdf/         ← 機器人描述檔
│   ├── dfam-check/ dfm/         ← 製造可行性檢查
│   ├── gcode/ bambu-labs/       ← 切片與列印
│   └── sendcutsend/             ← 板材加工驗證
├── packages/
│   ├── cadgen/                ← PyPI 發布的 Python 引擎（含原生 file tracer）
│   ├── core/                  ← @text-to-cad/core（TypeScript）
│   └── ui/                    ← @text-to-cad/ui
├── apps/
│   ├── web/                   ← CAD Viewer 前端
│   ├── mcp/                   ← MCP App 伺服器（cadgen mcp）
│   ├── api/                   ← api.texttocad.dev（更新檢查）
│   └── docs/                  ← texttocad.dev 文件站
├── models/                    ← 示範模型庫（F1 賽車、獵鷹九火箭、機械手…）
├── scripts/                   ← 建置、發版、測試、安裝腳本
└── tests/
```

### cadgen 引擎（packages/cadgen）

發布到 PyPI 的單一套件，承載：

- **模型執行器**：跑 `@step`/`@dxf` 模型腳本，編譯成文件
- **本機 store**（`~/.cache/cadgen`）：增量建置、快取、warm build daemon（常駐建置池，加速重複建置）
- **CAD Viewer**（`cadgen viewer`）：本機 HTTP 伺服器（port 3245），任何 CAD 檔依絕對路徑就能開
- **MCP App 伺服器**（`cadgen mcp`）：給 Agent 宿主啟動；在 Codex 裡是側欄 + 對話頁籤，在其他 MCP Apps 宿主裡是聊天中的 viewer card（可旋轉模型、把選取內容回傳給 Agent）
- **快照渲染**：用 Playwright 驅動無頭瀏覽器，把模型/機器人/工程圖渲染成圖片給 Agent「看」

依賴上刻意封頂：`build123d>=0.11.1,<0.12`、`cadquery-ocp-novtk>=7.9,<8`，因為 cadgen 會「伸手進」build123d 內部做確定性修正（shim）與 lazy store 攔截，minor 升級可能無聲失效。工程圖 PDF 走 ezdxf 的 drawing add-on（matplotlib 渲染）。

## 三、11 個 Skills 詳解

安裝後 Agent 獲得 11 個專業工作流：

| Skill | 功能 | 產出格式 |
|---|---|---|
| **CAD** | 從自然語言或圖片建立/編輯參數化 CAD 模型、組裝、量測幾何、修復迴圈 | STEP（主）、STL、3MF、GLB |
| **step.parts** | 尋找現成標準件：螺絲、軸承、馬達、接頭 | STEP |
| **Engineering Drawing** | 從零件產生標註工程圖：多視圖、隱藏線、尺寸、孔位標註、標題欄 | PDF |
| **DXF** | 2D 圖紙：輪廓、模板、墊片、切割排版 | DXF |
| **URDF** | 機器人結構檔：link、joint、極限、慣量、mesh | URDF |
| **SRDF** | 為 URDF 加上 MoveIt 規劃群、末端執行器、碰撞規則 | SRDF |
| **SDF** | 模擬器模型與世界：座標系、物理、感測器、燈光 | SDF |
| **SendCutSend** | 上傳前驗證 DXF/STEP 是否符合 SendCutSend 板材加工規範 | 檢查報告 |
| **DfAM Check** | 列印可行性：壁厚、懸垂、支撐體積、建置方向（程序化量測） | 檢查報告 |
| **DFM** | 金屬板材 / CNC 加工 / 射出成型審查，每項發現附實測證據與引用規範；從 mesh 量拔模角、倒鉤、投影面積 | 審查報告 |
| **G-code** | 用 OrcaSlicer + 自己的列印機预设切片 | G-code |
| **Bambu Labs** | 透過 Bambu Connect / Bambu Studio 送印到 Bambu Lab 列印機 | 送印 |

（表格 12 列是因為 CAD 與 viewer 功能合併計算；官方 README 列 11 個 skill 目錄。）

值得注意的深度：DfAM/DFM 不是「給建議」，而是**從幾何實測**——量出壁厚毫米數、懸垂角度、拔模角，再引用製程規範逐條對照。這正是「模型即程式碼」路線的優勢：Agent 可以呼叫 `cadgen.geometry` 做真實量測，而不是憑空猜。

## 四、安裝方式

### 最簡單：叫 Agent 自己裝

對你的 Agent 說：

```text
Install text-to-cad from https://github.com/earthtojake/text-to-cad
```

### 各平台手動安裝

| 平台 | 指令 |
|---|---|
| Claude Code | `claude plugin marketplace add earthtojake/text-to-cad#latest` → `claude plugin install text-to-cad@earthtojake` |
| Claude Desktop | 在 Settings → Developer → Edit Config 加入 `uvx ... cadgen mcp` MCP server |
| Codex | 從 ChatGPT Plugins 目錄安裝，或 `codex plugin marketplace add earthtojake/text-to-cad --ref latest` |
| Cursor | `git clone --depth 1 --branch latest … ~/.cursor/plugins/local/text-to-cad`（已裝 Claude Code 版則自動可用） |
| Gemini | `gemini extensions install https://github.com/earthtojake/text-to-cad --ref latest --consent --auto-update` |
| Grok Build | `grok plugin install earthtojake/text-to-cad@latest --trust` |
| 其他 Agent | `npx skills add earthtojake/text-to-cad#latest`（skills.sh 框架） |

前置需求：[uv](https://docs.astral.sh/uv/)（Python 執行器）+ Node 20+（開發時）。首次啟動會下載 CAD runtime 與無頭瀏覽器，需要網路。

### ⚠️ Windows 11 使用者注意：Smart App Control

CAD 内核 `OCP`（OpenCascade 的 Python 綁定）的 wheel 內含**未簽章的原生模組**。Windows 11 的 Smart App Control（全新安裝預設開啟）會擋下它，導致所有 `cadgen` 指令與 `import build123d` 噴 `ImportError: DLL load failed while importing OCP`。Smart App Control 沒有單例外白名單，解法只有兩個：

1. 關閉 Smart App Control（關了之後只能重裝 Windows 才能再開啟），或
2. 在 **WSL** 裡跑 CAD skills（SAC 不適用於 WSL）。

`cadgen doctor` 會自動診斷出這個問題。

## 五、遙測與隱私

預設會傳送**匿名使用統計與當機報告**（隨機 ID，不含檔案、路徑、prompt；錯誤只送固定類別詞如 "no file at that path"，不送訊息本身；自有程式碼一律以佔位符取代），後端是 PostHog。關閉方式：

```bash
uvx cadgen telemetry off     # 關閉並刪除已送資料
```

或環境變數 `DO_NOT_TRACK=1` / `CADGEN_TELEMETRY=0`。CI 與開發安裝預設不送。離線時不送、功能不受影響。更新檢查（`api.texttocad.dev/v1/versions`）每天最多一次匿名請求，`CADGEN_UPDATE_CHECK=0` 可關。

## 六、示範模型庫

`models/` 內有一整套展示用專案（Git LFS），可直接看「文字生成 CAD」能做到什麼程度：

- **f1/** — F1 賽車、**f14d/** — F-14 戰機、**hypercar/** — 超跑、**motorbike/** — 摩托車
- **falcon_heavy/** — SpaceX 獵鷹重型火箭（公開資料重建）
- **tendon_hand/** — 腱驅動研究機械手
- **juno/**、**lyra/** — 機器人描述套件（URDF/SRDF）
- **qdd_actuator/**、**radial/**、**w16/** — 馬達與引擎類零件
- **moonwatch/** — 手錶；**assemblies/**、**drawings/**、**examples/** — 組裝件、2D 圖、單檔範例

每個專案遵循統一結構：`src/`（模型腳本）+ `STEP/`、`DXF/`、`3MF/`、`GLB/`、`STL/` 輸出資料夾。

## 七、開發生態

- **發版節奏**：極快——v0.7.17～v0.7.21 在 2026-10-08～10-11 四天內連發，幾乎每日 release；`latest` 分支只放已上 PyPI 的穩定插件版，`main` 是開發分支。
- **貢獻者**：主要作者 earthtojake（1,130 commits）佔絕大多數，另有 warun7、amywork777 等社群貢獻，以及 claude（87 commits）與 github-actions bot——開發流程本身高度 Agent 化（repo 內有 `AGENTS.md`、`.claude-plugin`、git hooks）。
- **測試**：GitHub Actions CI（test.yml badge）、`scripts/test/`、依賴邊界檢查腳本（`check-dependencies.mjs`）。
- **文件**：[texttocad.dev](https://www.texttocad.dev) + 各 skill 的 `references/` 深度文件（model contract、build123d modeling、repair loop、kinematics…）。
- **社群**：Discord、skills.sh 排行榜。

## 八、總結評價

### 亮點

- **確定性 + LLM 的正確組合**：LLM 寫參數化程式碼、Open CASCADE 做幾何，避開了純生成式 CAD 的精度與不可編輯問題；Agent 還能用 `read_scene`/`scene.resolve()` 反讀模型做迭代修正。
- **覆蓋完整製造鏈**：設計 → 工程圖 → DfAM/DFM 檢查 → 切片 → 送印 / CNC / 板材外包，這是其他 CAD AI 專案幾乎沒做到的。
- **機器人工程友善**：URDF/SRDF/SDF 三個 skill 直接接 ROS/MoveIt/Gazebo 生態。
- **真正的本地優先**：除了更新檢查與遙測（可關），幾何運算全在本機。
- **跨平台通吃**：Claude Code/Desktop、Codex、Cursor、Gemini、Grok、任何支援 skills.sh 或 MCP 的 Agent。

### 限制

- **不是「AI 生成幾何」**：品質取決於底層 LLM 寫 build123d 程式碼的能力；複雜自由曲面（organic surface）仍是 build123d 的弱項。
- **Windows 11 Smart App Control 衝突**（見上文），需要 WSL 或關閉 SAC。
- **高度單人專案**：超過 90% commits 來自一位作者，bus factor 低；但發版活躍度目前極高。
- **依賴版本封頂**：build123d/OCP 被釘死在小版本區間，升級需等待官方適配。

### 適合誰？

| 適合 | 不適合 |
|---|---|
| 想把 AI Agent 變成機械設計助手的工程師 | 需要純 AI 端到端生成複雜曲面的人 |
| 3D 列印 / CNC / 板材外包的個人製造者 | 期待封閉商業 CAD（SolidWorks 級）體驗的企業 |
| ROS/機器人開發者（URDF/SRDF/SDF） | Windows 11 不願關 SAC 也不用 WSL 的使用者 |
| 想要「模型即程式碼」可版本化工作流的人 | — |

一句話總結：**text-to-cad 把「AI 畫 3D」變成「AI 寫 CAD 程式」，用確定性内核換來可量測、可製造、可迭代的真實工程產出**——這是目前（2026 年）把 LLM Agent 接進實體製造工作流最完整的開源方案。

---

*資料來源：[earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad) README、AGENTS.md、skills/、packages/cadgen 原始檔與 GitHub API，數據以 2026-10-15 實測為準。*
