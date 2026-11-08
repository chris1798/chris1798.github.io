---
title: "img2threejs 專案分析：把參考圖片「寫」成可動 Three.js 模型的程式碼重構管線"
date: 2026-11-08
description: "img2threejs 用「程式碼重構」取代摄影测量与网格提取：一张参考图 → 分阶段雕塑管線 → 通过品质闸门的 TypeScript Three.js 工厂函数。本文完整解析其架构、闸门系统、Token 效率设计、插件生态与路线图。"
tags:
  - GitHub
  - Three.js
  - AI Agent
  - 3D
  - Image-to-3D
  - 开源项目分析
---

# img2threejs 專案分析

> **一句話總結**：給一張參考圖片，img2threejs 用 AI Agent（Claude Code / Codex / OpenCode / Hermes）把圖中的物件**用程式碼重建**成一個分層級、可動畫、經過視覺審閱閘門認證的 Three.js TypeScript 模型——不是摄影测量、不是網格提取、不下載任何美術素材包。

## 專案概述

| 項目 | 資料 |
|---|---|
| 倉庫 | [github.com/img2threejs/img2threejs](https://github.com/img2threejs/img2threejs) |
| 官網 / 即時展示 | [img2threejs.io](https://img2threejs.io)（每一顆模型都是程式碼，在瀏覽器即時執行） |
| Stars / Forks | ⭐ 20,744 / 1,745（2026-11-08 擷取） |
| 授權 | Apache License 2.0 |
| 主要語言 | Python（約 3.35 MB，核心腳本）＋ JavaScript ＋ Shell |
| 目前版本 | Skill 2.0.1（2026-11-05 發布）／ npm CLI 0.2.0 |
| 建立時間 | 2026-07-15（約 4 個月即衝上 2 萬星，屢登 GitHub Trending） |
| 執行需求 | Node.js ≥ 18、Git、Python ≥ 3.10、一個支援的 AI Agent |
| 主題標籤 | image-to-3d、procedural-generation、threejs、ai-agents、claude-code、webgl |

## 核心理念：Reconstruction-by-Code（程式碼重建）

市面上多數 image-to-3D 方案（photogrammetry、TRELLIS、Tripo、Rodin 等）產出的是**網格檔案**（.glb/.obj，動輒好幾 MB 的二進位黑盒）。img2threejs 走了一條完全不同的路：

- 產出物是**可 diff、可版控、可審閱的 TypeScript**：一個 `createObjectNameModel(spec, options)` 工廠函數，回傳 `THREE.Group`。
- 模型由**基元（primitives）、程序化著色器（procedural shaders）與生成幾何**組裝而成，附帶真實的執行期階層（pivot、socket、collider、破壞群組），所以生出來就「能動」，不是一整團死模型。
- 輸出附 `root.userData.sculptRuntime`（節點／socket／碰撞體／破壞群組）；角色類建置另有 `root.userData.rig`（bone、共用 `Skeleton`、bone 索引表與如實計算的 `bound` 旗標）。

## 運作架構：分階段雕塑管線

整條管線是一個「腳本把關、模型只用眼睛判分」的狀態機：

```
參考圖片
  → 探測與適用性閘門（probe + suitability gate）
  → Pre-Spec 評估：分類、複雜度計分、品質契約
  → 管線路由：object / character / weapon（信心 < 0.82 就 fail-closed 要求補圖）
  → 撰寫 ObjectSculptSpec（元件樹、材質、socket）
  → 驗證閘門（strict-quality、手性 chirality）→ 不合格就回爐
  → 鎖定式建置關卡（一次只解鎖一關）
  → 產生「當關」的 Three.js 工廠程式碼
  → 渲染前的幾何閘門（禿斑、自相交——先在點雲上抓，不浪費渲染）
  → 瀏覽器渲染截圖 → 打包成一張「參考圖 vs 渲染圖」對比表
  → 確定性評審 + Agent 視覺判分 → 不合格自我修正 / 合格解鎖下一關
  → 全部過關後：從元件樹推導骨架 → 綁定 SkinnedMesh → 可動畫模型
```

**建置關卡的固定順序**（前一關未經渲染審閱合格，下一關不解鎖）：

`blockout → structural → form-refinement → material → surface → lighting → interaction → optimization`

每一關通過的條件都很硬：真實渲染 ＋ 對比表 ＋ 視覺分數達標 ＋ 每個「身分定義特徵」各自達標。每關結束後 Agent 只能選五種動作之一：`continue`、`refine-spec`、`refine-code`、`request-input`、`stop`。

### 閘門系統（Gates）：這個專案的靈魂

| 閘門 | 類型 | 說明 |
|---|---|---|
| Suitability | 硬 | 這張圖適不適合成 3D 目標 |
| Strict-quality | 硬 | 規格太淺就擋下，**在生成第一行程式碼之前**就失敗快逃 |
| Chirality（手性） | 硬 | 每一對 `-l`/`-r` 必須是鏡像而非旋轉複製——旋轉保持手性，「兩軸取負」做出來的會變成同一隻手做兩次 |
| Scalp exposure | 硬 | 在**任何渲染之前**於幾何上找出禿頭斑塊（輪廓度量看不見內部） |
| Screenshot feedback | 硬 | 渲染＋對比表＋視覺合格分，另加「輪廓內差異」（silhouette IoU 只看約 11% 的像素格，曾把「刪掉一張臉」和「完成品」打成同分） |
| Action-ready | 硬 | 該動的零件必須暴露 pivot/socket |
| Attachment | 硬 | 子零件要宣告怎麼接上父件，不許空中浮浮 |
| Material/Lighting | 硬 | 獨立 PBR 通道、真實燈光，albedo 不得別名進 roughness |
| Rig payload | 硬 | 綁 Skeleton 前驗證 joint/parent/matrix 負載完整性 |
| VLM gate | 軟 | 校準過的最後一層視覺模型評審；硬閘門失敗時絕不啟用 |

設計哲學很講究時序：**所有能量測的幾何檢查都跑在瀏覽器之前**，絕不花一個關卡去渲染已知錯誤的幾何。

## 核心功能詳解

| 功能 | 說明 |
|---|---|
| 物件與角色雙軌 | 每個主體分類為 `object`／`character`／`hybrid`；物件走硬表面管線，角色走解剖感知軌道（頭部單位比例、臉部ランドマーク、姿態） |
| 細節優先分析 | 生成程式碼前必須先列舉 `detailInventory`：光澤、倒角、螺絲鉚釘、雕刻／彩繪線紋、污漬磨損……每項細節都要對應到真實元件或材質，strict-quality 閘門在清點完成前擋下生成 |
| 最大相似度路徑（opt-in） | 參數化模板擬合圖片ランドマーク → 去光照（delight）→ 相機匹配 → 將參考照片投影到網格；單張圖無法保證 100% 相似，管線會**回報逐區域信心**並在關鍵處要求補拍視角 |
| 多視圖輪廓雕刻（opt-in） | `geometryDescriptor.visualHull` 將至少兩張正交二元輪廓intersect成體素網格，看不見的面記錄為低信心，**不編造隱藏細節** |
| 材质参考管線 | 每個可見材質區域可裁切、分析、對照版本化 Three.js 材質註冊表、擬合進 Spec、多視角渲染，逐區域比對閘門合格才收 |
| CS2 武器重建 | 刀與 Glock-18 有家族專屬元件契約：精確度分級、塗裝區域覆蓋、逐區域信心、map-stripped blockout 證據閘門——防止「紋理過得去、結構是空的」 |
| 可中斷續作 | `forge/state.py` 記錄有證據支撐的順序檢查清單，`forge/next.py --state` 從中斷點續跑；狀態索引**不授予**過關，正式閘門仍是權威 |
| 角色綁定（Stage R） | 骨架從元件樹推導（bone 無法偏離它驅動的幾何）、測地權重（距離穿過實體量測）、綁 Skeleton 前的阻斷式負載閘門 |
| 毛髮子系統 | 五階段：Otsu 毛髮/皮膚分離、髮際線、髮根以頭皮 (u,v) 定位（絕對座標是硬錯誤）、硬式頭皮暴露閘門＋軟式coverage閘門 |
| GLB 參考路線 | 把多件式 GLB 當**量測儀器**（尺寸、比例、各帶寬度、基色、roughness/metalness 全部強制為量測值），產出的仍是純程序化 TypeScript，GLB 本身絕不進產品 |
| 選配證據層 | 隔离式外掛：SAM2 元件遮罩、Depth Anything V2 相對深度、MediaPipe 臉/姿態ランドマーク、Playwright 跨瀏覽器備援——它們**永不核發過關**，只當證據 |

## Token 效率設計（為什麼它跑得起來）

多數 image-to-3D 的 agent 迴圈把 token 燒在機械式工作上。img2threejs 的核心配方是「**腳本負責執法，模型負責評判**」：

- 驗證、閘門、Spec 撰寫、PBR 提取、對比表打包、管線狀態全部由 Python 腳本做，**零依賴**（純 Python 3.10 標準函式庫，PNG 讀寫用 `struct`＋`zlib`，無 pip／PIL／numpy／Playwright）。
- 模型的 token 只花在兩件事：看**一張**對比表判過不過、寫程式碼。
- 產生器只輸出「目前解鎖的那一關」，每輪都是小而 Scoped 的編輯，不重讀整個模型。

官方估算（工程估計，非實測基準）：

| 階段 | 估計模型 token |
|---|---|
| 確定性腳本（探測/評估/驗證/產生/同步） | 共約 2k–5k（近乎免費） |
| 撰寫評估＋細節清點＋Spec JSON | ~15k–25k |
| 撰寫與編輯 Three.js 工廠 | ~20k–45k |
| 渲染審閱迴圈（5–8 輪） | ~30k–70k（最大開銷，線性於輪數） |
| **單一物件合計** | **~80k–180k** |
| 角色重建（更多審閱輪＋ランドマーク/投影檢查） | ~150k–350k |

單輪審閱約 5k–12k token；每擋下一次「規格不足的壞渲染」就省一顆輪（~10k–20k）。

## 安裝與使用

```bash
# 1. 安裝基礎 skill（自動連結到找到的所有 agent host）
npx --yes img2threejs@latest install
npx --yes img2threejs@latest doctor    # 每個 agent 一行："managed" = 已安裝

# 2.（選配）插件 harness
npx --yes @img2threejs/img2@latest install --yes
npx --yes @img2threejs/img2@latest plugins   # 檢視即時目錄
```

在 agent 裡附圖呼叫：

```text
/img2threejs Rebuild the object in ./reference.png as a procedural Three.js model.
Keep its proportions, silhouette and colours. Follow the quality gates.
Report the output files, render-review evidence and any inferred regions.
```

README 還附了一份「施加壓力」的高階 prompt 範本：逐行對應到真實閘門（Fidelity→細節清點、Materials→從像素推 finish class、Runtime→pivot/socket＋`userData.tick` 閒置動畫、Gates→`--strict-quality`＋逐區域信心），「這不是形容詞，是改變被強制執行的東西」。

### 插件生態（v2.0 引入）

| 插件 | 新增能力 | 存取 |
|---|---|---|
| `character` | 角色綁定與動畫：GLB 骨架、皮膚調理、動作設計、12 項綁定閘門 | 公開 |
| `cs2` | Counter-Strike 2 武器/手套皮膚重建：家族契約與阻斷式審查閘門 | 公開 |
| `environment` | 環境插件（建築/室內/街景的前身） | **私有，需授權 Git 存取** |
| `hello-cube` | 圖片→確定性立方體（契約測試用） | 公開 |
| `img2glb` | 經託管 TRELLIS 空間輸出 GLB 網格（走網格路線的逃生門） | 公開 |

基礎版內含 `generic` 與 `character` 兩個 profile；profile 缺插件時**大聲失敗並說明缺什麼，絕不靜默降級**。

## 版本演進與路線圖

| 版本 | 主題 |
|---|---|
| v1.0–v1.3 | 物件管線、細節清點、人形角色產生器、Divine Eye 確定性評審、CIEDE2000 色彩閘門 |
| v1.4 | The Weapon Update：CS2 影像比對重建、家族專屬適配器 |
| v1.5 | The Character Update：元件樹推導骨架、測地蒙皮、五階段毛髮、手性閘門 |
| **v2.0（目前）** | **The Plugin Update**：域註冊表、pull-based 規格增援（quality floor 只升不降）、img2 harness |
| v2.1（Next） | The Character Split：倉內 character 域併入 plugin-character，基礎版不再命名任何域 |
| v2.2–v2.5 | 環境更新（建築/地形/多物件）→ 遊戲管線（Unity/Unreal 匯出、Blender 橋、LOD）→ 動畫（自動綁定、Mixamo、臉部骨架）→ AI Studio（Web UI、批次、雲端渲染） |
| v3.0 | The Procedural World Update：多視圖重建、程序化城市、語意世界理解 |

敘事弧很清晰：**資產 → 插件生態 → 世界 → 生產管線 → 從參考圖生成可玩世界的 AI 遊戲資產平台**。

## 坦白說 limits（README 自己承認的）

- **單張圖片無法揭露隱藏面**、無法保證精確幾何；管線會明說輸出是近似／風格化／低多邊形，未見面以鏡像推定而非假裝有信心。
- 硬表面物件最強；角色是**風格化重建**，不是照片級相似度。「以此圖片無法達到要求的精度」是被視為合法且預期的結果。
- Token 數字是工程估計，實測基準要到 v1.5 才補上。
- `environment` 插件是私有的；README 的 star-history 圖仍指向舊倉庫路徑 `hoainho/img2threejs`。

## 生態與商業模式

- **贊助商**：MiniMax、Atlas Cloud（LLM API）、Tripo、Hyper3D Rodin——後兩家是生成式 3D 服務，被定位為「量測棍」：為單张照片無法決定的輪廓/背面問題提供第二份參考。贊助模式明言「買的是算力，不是報導版面」。
- 捐購管道：Ko-fi、VietQR、MoMo、PayPal。
- 貢獻方向：程序化材質食譜、新閘門、新 agent host 支援、demo。

## 總結評價

**亮點**
1. **范式差異**：code-only 路線讓產物可 diff、可版控、可漸進編輯，天然貼近工程工作流，與網格派（TRELLIS/Tripo/Rodin）互補而非正面競爭。
2. **閘門工程異常扎實**：約 90 個模組的 `forge/`，把「什麼能測就先用測的」做到極致——手性、禿斑、自相交全在渲染前的幾何上抓，是少見的「先驗證再花錢」設計。
3. **Token 成本模型公開**：連「最大槓桿是審閱輪數」這種成本結構都寫成文件（TOKEN_COST.md），對要接進自己 agent 工作流的人非常實用。
4. **誠實文化**：fail-closed 路由、逐區域信心、不編造隱藏面——這在生成式 3D 圈是稀缺品質。
5. 對 Hermes / Claude Code / Codex / OpenCode 的使用者是**零安裝摩擦**：純 Python 標準函式庫，nothing to pip。

**潜在限制**
1. 角色是風格化重建，照片級真人相似度達不到（單圖的物理極限）。
2. 一次完整重建 80k–350k token，重度使用仍需便宜的模型 API（專案本身靠贊助商餵算力）。
3. 結果品質高度依賴宿主 agent 的視覺能力與瀏覽器渲染工具。
4. 專案很年輕（4 個月），API 與插件邊界還在移動（v2.1 就要拆 character 域）。

**適用**：把「一張圖 → 可動的程序化 3D」塞進 agent 工作流的開發者；Web 遊戲/互動原型；需要產物是程式碼而非網格資產的場景；CS2 皮膚展示類需求。
**不適用**：需要照片級掃描網格（直接找摄影测量/Tripo/Rodin）；完全沒有 vision-capable agent 的環境。

---

*資料來源：GitHub API 即時元資料、README.md、docs/ARCHITECTURE.md、docs/TOKEN_COST.md、CHANGELOG.md（2026-11-08 擷取）。Star 數為寫文當日快照。*
