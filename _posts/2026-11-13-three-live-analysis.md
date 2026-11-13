---
title: "Three-Live 專案解析：Google 開源的 AI-First 原生 3D / CAD / 空間運算工具鏈"
date: 2026-11-13
description: Three-Live 是 Google 開源（Apache-2.0）的 AI-First 3D 工具鏈：把標準 Three.js 程式碼用裝置端 Rust JIT 編譯器編譯成 Android（Google Filament / Jetpack XR）、iOS / visionOS（Apple RealityKit）與 WebGL2 / WebXR 的原生場景，並附上 .glb / .usdz 匯出、空間 linter、headless 渲染與 MCP server，專為 LLM 與 AI coding agent 閉環驗證設計。本文整理其架構、能力矩陣、安裝方式與適用場景。
tags: [Three.js, 3D, WebXR, AR, XR, LLM, MCP, Rust, 開源專案, Google]
---

# Three-Live 專案解析：AI-First 原生 3D / CAD / 空間運算工具鏈

**Three-Live** 是 Google 於 2026 年 10 月開源的跨平台 3D / XR 工具鏈（注意 README 標明「This is not an officially supported Google product」，屬官方組織發布但非正式支援產品）。它的一句话定位是：

> **AI-First Native 3D, CAD & Spatial Computing** —— 一個「裝置端 JIT 編譯器」，把即時生成的 **Three.js 程式碼**直接編譯、執行在 **Android（Google Filament & Jetpack XR SceneCore）**、**iOS / visionOS（Apple RealityKit）** 與 **WebGL2 / WebXR** 上。

- 倉庫：<https://github.com/google/three-live>
- 官方網站與線上 Playground：<https://google.github.io/three-live/>
- 授權：Apache License 2.0
- 統計（2026-11-13 查詢）：約 **364 顆星**、42 forks、最新釋放 **v1.4.0（2026-11-09，Beta）**，自 2026-10-02 開源以來以每週多次釋放的速度高速推進。

## 為什麼需要 Three-Live？—— Three.js 作為「3D 中間表徵（IR）」

這是理解整個專案的鑰匙。傳統 3D 內容管線有兩條路：

1. **靜態二進位資產**（`.glb` / `.fbx` / `.usdz`）：由桌面建模軟體匯出。
2. **綁死單一引擎的命令式程式碼**（Unity C#、Unreal C++、瀏覽器 Three.js + WebGL）。

當你把 LLM、coding agent 或執行期參數化客製加進去時，兩條路都有問題：

- **LLM 無法可靠地直接產出二進位 3D 格式**——逐 token 生成顶点缓冲、四元數、位元對齊的 ZIP 封包（GLB）幾乎不可行。
- **Text-to-mesh 擴散模型的輸出缺乏場景結構**——通常是一整塊合併曲面，沒有零件層級、命名節點、機械接頭、精確參數尺寸與獨立 PBR 材質。
- **但 LLM 寫 Three.js 極其擅長**——`THREE.Mesh`、`THREE.Group`、`THREE.BoxGeometry`、`THREE.MeshStandardMaterial` 在公開訓練資料中大量存在，15～30 行 JavaScript 就能生成一個完整可互動的 3D 場景。

Three-Live 的思路因此是：**把 Three.js 當作編譯器的輸入語言（中間表徵）**，在人類或 LLM 寫好腳本後，於裝置端沙箱中編譯成各平台的原生場景圖與標準資產檔（`.glb` / `.usdz`），交給各平台的原生引擎渲染。

### 它解決的實際痛點

瀏覽器 WebXR（`navigator.xr`）覆蓋率不足，是行動 AR 的長期現實：

| 目標環境 | 純瀏覽器 WebXR / 靜態 AR 交接的限制 | Three-Live + XR-Live 能做什麼 |
| :--- | :--- | :--- |
| Android 手機 / 平板（原生 App） | `android.webkit.WebView` 不支援 WebXR；Scene Viewer 只能看靜態 `.glb` | 透過 JNI 編譯 Three.js，在 App 內用 **Google Filament + ARCore** 原生渲染 |
| Android XR / Apple Vision Pro 頭戴 | 瀏覽器 WebXR 被隔離在全螢幕 WebGL session | 掛載原生 **Jetpack XR SceneCore**（`GltfEntity`、`MovableComponent`、`Anchor`）或 **RealityKit** 實體到系統共享空間 |
| iPhone / iPad（原生 SwiftUI App） | `WKWebView` 無 WebXR；AR Quick Look 只看靜態 `.usdz` | 在 **ARKit + RealityKit**（`ARView` / `RealityView`）跑「活的」Three.js 場景、`animate()` 迴圈與互動 |
| 手機與頭戴瀏覽器 | iOS Safari 沒有 WebXR | 支援處跑 6DoF WebXR，iOS Safari 自動交接記憶體中的 `.usdz` / `.glb` 給 Quick Look |

重點：透過 Scene Viewer / AR Quick Look 交接靜態檔案會**丟失互動性**（動畫迴圈、60 Hz 物理、自訂狀態、互動插件全部消失）；Three-Live 因為編譯的是「程式碼」而非「模型」，這些都能帶進原生環境。

## 架構總覽

```
LLM / 開發者寫的 Three.js 腳本（type="text/three"）
        │
        ▼
沙箱 JIT 編譯器（Rust + Boa/QuickJS JS 引擎）
  · _android: JNI（零-copy）_ · _iOS/macOS/visionOS: C FFI_ · _Web: 隔離 Web Worker / iframe sandbox_
  · 執行逾時、記憶體上限、幾何配额、CPU 指令燃料限制、無網路無 DOM
        │
        ▼
零-copy GLB（glTF 2.0 二進位）／ .usdz（OpenUSD）
        │
        ├── Android：Google Filament 渲染 + Jetpack XR SceneCore 空間實體（XRLiveRuntimeSession，60 Hz 物理）
        ├── iOS / visionOS：Apple RealityKit（XRLiveRealityKitSession）/ Quick Look
        ├── Web：<three-live> / <xr-live> 自訂元素，WebGL2 / WebGPU / 6DoF WebXR
        └── CLI（three-live-cli，Rust，零 GPU）：headless CPU 光柵化、空間 linter、MCP server、agent gym
```

語言組成（GitHub Languages）：TypeScript 約 4.6 MB（Web runtime 與元件）、Kotlin 約 1.5 MB（Android SDK）、Rust 約 1.5 MB（編譯器核心）、Swift 約 1.3 MB（iOS / visionOS SDK）、JavaScript 約 1.2 MB（examples / evals）。

核心設計決策：

- **三平台對等（parity contract）**：Web（TypeScript）與 Rust 編譯器、Kotlin、Swift 實作以共享像素雜湊測試與結構雜湊驗證對等行為，`AGENTS.md` 明文規定跨平台對等契約。
- **沙箱安全**：網路與儲存全域物件被剝除、`Object.prototype` 凍結、CPU 指令燃料上限、場景幾何記憶體配額——讓「不可信的 LLM 輸出」可以安全地在 Android / iOS / Web 上直接執行。Web 端預設**關閉**客戶端腳本執行，需顯式 `allow-client-scripts`。
- **編譯器絕不呼叫網路模型**：所有 AI 功能（LLM 編輯、AI 質感）都是注入式 provider，編譯管線本身離線可跑。

## 四種快速上手方式

### 1. Android（Kotlin + Filament + Jetpack XR）

```kotlin
val threeJsCode = """
  const core = new THREE.Mesh(
    new THREE.IcosahedronGeometry(0.55, 3),
    new THREE.MeshStandardMaterial({ color: 0x38bdf8, metalness: 0.85, roughness: 0.15 })
  );
  core.userData.xr = { grab: '2-hand', orbit: { speed: -0.4 } };
  scene.add(core);
""".trimIndent()

// 編譯成零-copy GLB ByteBuffer，直接載入 Google Filament
val holder = FilamentHelper.loadModelZeroCopy(threeJsCode) { buffer ->
    assetLoader.createAssetFromBinary(buffer)
}

// 每幀推進 KHR_interactivity 行為圖、60 Hz 剛體物理與空間 traits
val runtime = XRLiveRuntimeSession.fromGlb(holder.byteBuffer)
runtime.step(dtSeconds = 1.0 / 60.0)
```

### 2. iOS / macOS / visionOS（Swift + RealityKit）

```swift
import ThreeLiveCompiler
import RealityKit

let glb = try ThreeCompiler.compileToGLB(script: threeJsCode)
let entity = try await RealityKitHelper.loadEntity(fromGLB: glb)
XRLiveRealityKit.installTraits(on: entity, in: arView)

let session = XRLiveRealityKitSession(glbData: glb, root: entity)
session?.start()
```

同一段 Three.js 程式碼，四處（Android、iOS、Web、CLI）執行結果一致。

### 3. CLI 與 MCP server（AI agent 的閉環驗證）

`three-live-cli` 是單一原生二進位（**不需要 GPU**），內建 headless CPU 光柵化渲染器與空間 linter：

```bash
npx three-live-cli render scene.js --view=quad --grid --annotations -o contact_sheet.png   # 4 視角接触表
npx three-live-cli render scene.js --reference=blueprint.png --view=front -o compare.png    # 對照圖 silhouette diff + IoU
npx three-live-cli from-image photo.jpg -o scene.js --visual-turns 2                        # 圖片→程式碼場景
npx three-live-cli validate scene.js --json                                                 # 結構化空間診斷
npx three-live-cli link scene.js --qr                                                       # 手機一鍵開 AR 的 QR
npx three-live-cli convert scene.js -o model.usdz

# 註冊成 MCP server（Claude Code / Gemini CLI / Cursor 等）
claude mcp add three-live -- npx -y -p three-live three-live-cli mcp
```

MCP 工具包含 `three_live_validate`、`three_live_render`、`three_live_convert`、`three_live_from_image`、`three_live_bake_textures`、`three_live_sim`、`three_live_link`，以及 **agent gym**（`three_live_gym_reset / step / close`）——讓 agent 以「act → observe → react」逐幀玩一個場景，驗證關卡是否可通（gym 一詞借自強化學習的 reset/step 環境，不涉及 ML）。這是「LLM 寫 3D 場景」後最完整的**自動化视觉＋空間驗證迴圈**：渲染接触表給視覺模型看、linter 給 JSON 幾何診斷（視錐coverage、接地、重疊錯誤碼 TL100–TL402）、參照圖疊加比對給 IoU 分數。

### 4. Web（`<three-live>` / `<xr-live>` 自訂元素）

```html
<three-live allow-client-scripts
    ai-endpoint="https://your-backend.example/chat" ai-model="gemini-2.5-flash">
  <script type="text/three">/* 標準 Three.js 場景 */</script>
</three-live>
<script type="module">
  const el = document.querySelector('three-live');
  const result = await el.editScene('make the roof red and add a chimney');
  if (!result.applied) console.warn(result.error);  // 失敗時場景不動
</script>
```

`<three-live>` 對 `<model-viewer>` 的核心 HTML 屬性（`src`、`camera-controls`、`ar`、`shadow-intensity`…）相容，還可用 `ThreeLiveElement.defineModelViewer()` 直接顶替 `<model-viewer>` 標籤註冊。AI 編輯走業界通用的 Chat Completions 協定——自家後端 proxy、Ollama / LM Studio（`http://localhost:...` 免帳號）、vLLM、OpenRouter 或 Gemini 相容端點都能接，API key 留在自己的伺服器。

## AI 能力矩陣

這是 Three-Live「AI-First」定位的具體內容，且**全部四端（Web / Android / iOS / CLI）都有對應 API**：

| 能力 | 介面 | 說明 |
| :--- | :--- | :--- |
| 自然語言場景編輯 | `el.editScene('...')` | 每次編輯先在沙箱編譯驗證、失敗自動修復一輪，通過才熱替換；`el.undoEdit()` 回滾。壞生成永不弄掛現場 |
| 圖片→場景 | `el.compileFromImage(img, {prompt, priors, visualTurns: 0..5})` | 照片／素描／藍圖→程序化 Three.js 場景；以 ARCore / Apple RoomPlan（`CapturedRoom`）空間先錨定真實尺度，並與 `REFERENCE | RENDER | OVERLAY` 渲染表閉環迭代 |
| 語音選取＋語音編輯 | `selectByVoice()`、Tap & Speak、Talk-to-Select | 兩層式：名稱／顏色／方位／尺寸／序數由**本地匹配器**解析（零模型呼叫），解析不了的关系型指令才丟給 LLM；語音走 `ai-realtime` Realtime WebSocket 或 Gemini Live |
| AI PBR 質感 | `userData.xr.material.prompt` | 以 prompt+size+seed 內容寻址的 texture pack；有 OpenAI 相容 Images 端點時生成、IndexedDB 快取、熱替換；法線圖與 ORM 圖**裝置端**推導；離線時以程式化 preset（wood/marble/brick/concrete/brushedMetal/rust/…）兜底 |
| Agent 閉環驗證 | MCP server + CLI + gym | 見上文第 3 節 |

`why-three-live.md` 還提供了給 LLM 的系统提示片段、`docs/llm-guide.md` 有嚴格的 `THREE.*` 白名單、場景配额與 few-shot 模板；倉庫根附 `llms.txt` / `llms-full.txt` 餵給模型上下文，`skills/` 內含現成的 agent 技能（`three-live-authoring`、`xr-live-plugin-dev`）——整套 repo 本身就是按「給 AI 用」的規格組織的。

## 插件體系與 Bundle 体积預算

Web 端採模組化 bundle，每個都有**CI 強制**的 gz 体积上限（這在開源 3D 引擎裡相當罕見）：

| Bundle | 上限 | 內容 |
| :--- | :--- | :--- |
| `three-live-viewer.min.js` | < 31 KB gz | 精簡 `.glb` / `.usdz` WebGL2 PBR viewer + AR 打包 |
| `three-live.min.js` | < 78 KB gz | 標准 `<three-live>` + Three.js 即時編譯器 + `KHR_interactivity` |
| `three-live-full.min.js` | < 224 KB gz | 20 個引擎插件全配（studio / CAD / procedural / animation / AI / WebGPU / TSL） |
| `xr-live.min.js` | < 90 KB gz | 標准 `<xr-live>` + 空間 traits |
| `xr-live-spatial.min.js` | < 63 KB gz | 15 個空間插件（每個約 2–5 KB gz） |
| `xr-live-sim.min.js` | < 31 KB gz | 6 個模擬插件 |
| `xr-live-full.min.js` | < 333 KB gz | 全配 |

對比 `<model-viewer>` 全套約 250 KB gz 的體量，分層策略相当克制。

**20 個 core 插件**亮點：CAD（2D Shape/`ExtrudeGeometry`/3D BSP `CSG` 布林運算/`TextGeometry`）、`KHR_interactivity` 行為圖、PBR Next（clearcoat/transmission/iridescence）、HDRI 與 9 頻球諧光照、多光源深度陰影圖、雙 Kawase bloom／outline、多級 LOD、64 關節 GPU 骨架蒙皮、morph targets、兩骨節／FABRIK 逆運動學、無迴圈 `THREE.TSL` 節點材質（一份材質定義編到 GLSL／WGSL／MaterialX／Filament／CPU 光柵器）、WebGPU `GPURenderBundle` 場景加速器、`EXT_meshopt_compression` 零 WASM 解碼器。

**15 個空間插件**（Android / iOS / WebXR 三端都有原生對應實作）：頭部跟隨 HUD、操作把手、`world-understanding` 平面追蹤與捲尺、Gemini Live 即時語音+視覺助理、空間彩繪、深度粒子（雨/雪/火花，與真實深度圖碰撞）、Gaussian Splatting 載入（百萬 splat）、3D 尺寸標註、磁吸對位、凝視停留（eye gaze）、CAD 爆炸圖與剖面切割、持久錨點（`#xr-state` URL 分享）、傳動式移動（teleport）、多人共在（`shared-room`，20 Hz 量化 avatar）、空間音訊。

**6 個模擬插件（xr-live-sim）**：角色控制器、操舵代理（patrol/chase/flee）、確定性 60 Hz 剛體物理＋機械接頭（hinge/slider/spring/ball，並匯出 USDZ PhysicsAPI）、命中區與觸發區、計分任務清單（訓練演練）、零素材程序化音效。

**5 個領域套件（Domain Kits）**：共 **57 個水密 2-manifold 參數化 CAD 零件**——機械（正齒輪、斜齒輪、螺栓 ISO 公制、軸承、帶輪…）、建築（牆/屋頂/樓梯含 IBC 規範/門窗）、工業（管線含焊接法蘭、閥門、泵、貨架、OSHA 安全籠爬梯…）、科學（分子式含 CPK 著色、蛋白質 ribbon、晶格、等值面 Marching Tetrahedra、向量場流線 RK4…）、電子（PCB、散熱片、IC 封裝含 JEDEC 規格…）。每個 12–30 KB gz 單賣，LLM 只要叫 `new THREE.Mechanical.SpurGearGeometry(...)` 就能得到標準零件。

## 與相近方案的定位比較

| 維度 | 原生 Three.js（瀏覽器） | 靜態資產 viewer（`<model-viewer>` / Quick Look） | 遊戲引擎工具鏈 | **Three-Live** |
| :--- | :--- | :--- | :--- | :--- |
| 主要輸入 | 綁死 DOM/WebGL 的 JS | 預先烘焙 `.glb` / `.usdz` | 引擎專案檔＋C#/C++ | 宣告式 HTML＋沙箱 Three.js（＋`.glb`） |
| LLM 工作流 | 無內建空間 linter／沙箱 | LLM 無法直接產二進位 | 需編輯器插＋多步編譯 | 標準語法＋linter＋silhouette 對照＋自動修復 |
| 不可信腳本安全 | 主執行緒全權限 | 安全（只解析資產） | 不適用於執行期腳本 | Boa/QuickJS 或 Worker 沙箱，CPU/記憶體/頂點上限 |
| 原生 Android / iOS | 僅瀏覽器 / WebView | 僅 Web＋iOS 靜態交接 | 離線編譯原生 binaries | **裝置端 Rust 編譯器→Filament / RealityKit** |
| 程序化著色器 | 瀏覽器限定 | 靜態貼圖 | 離線引擎著色圖 | TSL 一份圖→GLSL/WGSL/MaterialX/Filament/CPU |
| 執行期 AI 編輯 | 自建 | 不支援 | 自建 | 內建 `editScene` / `compileFromImage` / `selectByVoice` |

官方文檔也坦承**不適用場景**（少見的誠實）：只展示美術做好的靜態模型（用 `<model-viewer>` 或其精簡 viewer 就夠）；大型遊戲（GB 級串流世界、任意迴圈 compute shader、navmesh、主機管線請用完整遊戲引擎）；依賴 DOM／網路／無界迴圈的 Three.js 腳本（沙箱會擋）。

## 安裝速查

| 平台 | 管道 | 標識 |
| :--- | :--- | :--- |
| Android | JitPack（免驗證）/ GitHub Packages Maven / 預建 AAR / 原始碼 | `com.github.google.three-live:compiler:v1.4.0`（可選 `:filament`、`:firebase-ai`、`:detect-mlkit`、`:hands-*`） |
| iOS / macOS / visionOS | SwiftPM（自動解析 checksum 釘選的預建 XCFramework，本地免 Rust/Node 工具鏈） | `.package(url: "https://github.com/google/three-live.git", from: "1.0.0")` |
| Rust CLI / 函式庫 | Crates.io / 預建二進位（macOS、Linux、Windows）/ `make rust` | `cargo install three-live-compiler --bin three-live-cli` |
| Web | npm / jsDelivr / GitHub Pages CDN / `three-live-web-dist.zip` | `npm install three-live xr-live` |

開發：repo 根 `make doctor` 檢查工具鏈（NDK / Xcode / Rust / Node），`make android-demo`、`make ios-demo`、`make web-demo`（localhost:8888 遊樂場）、`make test` 跑四端對等測試。CI 由 GitHub Actions 分 CI / Pages / Release 三條管線。

## 工程品質觀察

- **釋放節奏**：1.0.0 Developer Preview（2026-10-06）→ 1.4.0 Beta（2026-11-09），約五週四個 minor，CHANGELOG 每條都寫到 API 簽名與跨平台行為細節。
- **評測體系**：`evals/` 內建 **100 條 prompts** 的 LLM 生成評測（anim / cad / mat / org / xr 五類各 20 條）＋ smoke 腳本，`run_evals.ts` 可重跑——「LLM 生成的場景品質」被當成可回歸的測試，而非 demo。
- **Agent 文檔化**：`AGENTS.md`（倉庫規則＋三端對等契約＋bundle 預算＋安全不變量）、`llms.txt` / `llms-full.txt`（16 萬字元完整參考單檔）、`skills/` 兩個 agent 技能、`.mcp.json` / `smithery.yaml` / `glama.json`（MCP 生態註冊檔）一應俱全。
- **測試**：Rust 單元＋fuzz（transcode）、WebAssembly 測試、參考影像 fixtures（像素級對等）、TypeScript/Rust 共享像素雜湊的質感生成測試、层级对等 fixtures。
- **狀態**：README 自述 **Beta**——核心 3D、行動 AR/XR、空間運算 runtime、`userData.xr` trait schema（schemaVersion: 1）、沙箱 JIT 與三端對等已功能完備；星數還少（364），社群正處於爆發前段，API 仍可能演進。

## 結語

Three-Live 是第一個把「**LLM 生成的 Three.js 程式碼**」当作一等公民的跨平台 3D/XR 執行環境：程序式代碼當 3D IR、Rust 沙箱 JIT 當安全邊界、零-copy GLB/USZD 當原生引擎交接格式、CLI/MCP 接触表與空間 linter 當 agent 的「眼睛」。對想做「AI 生成 3D 場景」「行動端 AR 產品檢視器」「Web＋原生三端一致」的团队，它提供了一條不需要 Unity/Unreal 的重管線方案；而它那套給 LLM 用的 llms.txt、白名單、few-shot、agent gym 與 100-prompt evals，也是觀察「AI-first 工具鏈该怎么設計」的現成教材。Apache-2.0 授權、預建產物齊全（AAR / XCFramework / 各平台 CLI 二進位 / npm），要評估的門檻不高——直接 `npx three-live-cli render` 一張四視角接触表，就能感受它的闭环驗證設計。

---

**參考來源**

- GitHub 倉庫與 README、`docs/why-three-live.md`、`docs/xr-live.md`、`docs/three-live.md`、`docs/llm-guide.md`、`docs/cookbook.md`、`CHANGELOG.md`（v1.4.0，2026-11-09）
- 官方網站：<https://google.github.io/three-live/>
- 統計數據查詢日期：2026-11-13
