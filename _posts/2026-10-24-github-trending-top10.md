---
layout: post
title: "本週 GitHub 熱門 Top 10 完整功能介紹（2026-10-24）"
date: 2026-10-24
description: "2026 年 10 月中旬這一週 GitHub Trending 前十名：REA、VoiceStudio、Orca、OpenCode、HyperFrames、ComfyUI、Claude Code Plugins、Ghidra、ai-memory、Ruflo——功能、架構與圖片說明。"
tags: [GitHub, Trending, AI Agent, 開源工具, 逆向工程, 語音 AI, 影片生成]
categories: [技術觀察]
permalink: /weekly-github-trending-top10-2026-10-24/
image: /assets/images/trending-morluto-rea/img0.0.png
---

## 資料來源與時間基準

以 **GitHub Trending「This week」**（`https://github.com/trending?since=weekly`）抓取，資料時間為 **2026-10-24**（台北 UTC+08:00）。排名依「本週新增 Star 數」排序，總 Star 數取自 GitHub REST API `repos/{owner}/{repo}`，以下每一項都已實際驗證。

| # | 專案 | 本週新增 ★ | 總 Star | Fork | 語言 | 授權 | 建立 |
|---|------|-----------:|--------:|-----:|------|------|------|
| 1 | **morluto/rea** | 88,243 | 375,496 | 93,866 | TypeScript | MIT | 2026-04-14 |
| 2 | **debpalash/VoiceStudio** | 12,526 | 84,059 | 9,279 | Python | AGPL-3.0 | 2026-04-09 |
| 3 | **stablyai/orca** | 9,545 | 104,370 | 6,590 | TypeScript | MIT | 2026-03-17 |
| 4 | **anomalyco/opencode** | 6,765 | 220,898 | 29,531 | TypeScript | MIT | 2025-04-30 |
| 5 | **heygen-com/hyperframes** | 5,553 | 71,098 | 6,421 | TypeScript | Apache-2.0 | 2026-03-10 |
| 6 | **Comfy-Org/ComfyUI** | 4,531 | 142,482 | 16,804 | Python | GPL-3.0 | 2023-01-17 |
| 7 | **anthropics/claude-plugins-official** | 4,250 | 44,240 | 4,649 | Python | Apache-2.0 | 2025-11-20 |
| 8 | **NationalSecurityAgency/ghidra** | 4,221 | 93,800 | 10,536 | Java | Apache-2.0 | 2019-03-01 |
| 9 | **akitaonrails/ai-memory** | 3,449 | 13,155 | 918 | Rust | MIT | 2026-05-21 |
| 10 | **ruvnet/ruflo** | 3,349 | 78,892 | 9,265 | TypeScript | MIT | 2025-06-02 |

**一句話總結這週的主題**：前十名幾乎全是「AI Agent 的基礎設施」——逆向工程 MCP、多 agent 桌面工作台、跨 agent 長期記憶、agent harness／swarm、agent 寫 HTML 直接渲染影片，再加上兩個「把模型變成產品」的本地工具（語音克隆、ComfyUI）與一個成熟的逆向工程框架（Ghidra）。純應用類的少，工具鏈與 harness 類的多。

---

## 1. morluto/rea —「Reverse Engineer Anything」

![REA 在 Hopper 中啟動分析橋，檢查原生二進位檔](/assets/images/trending-morluto-rea/img0.0.png)

**它是什麼**：一套 **MCP 逆向工程工具箱**，把逆向工程拆成「你的 agent 能呼叫的工具」，目標是「看到某個 App 有個功能，想在自己的產品裡也做一個」——讓 agent 在不需原始碼的情況下檢查目標、解釋行為、拿出證據，然後自己寫一版並測試。

**核心概念**：

- **一個 MCP**：`npx rea-agents setup` 一鍵註冊到 Claude Code、Codex、Cursor、Gemini CLI、Grok Build 等 agent，同時安裝配套的 workflow 指令；會備份原有設定。分析在本機執行。
- **證據導向**：每個結論都附證據與「限制」（unknowns），agent 可以追問、再深入。
- **可選的分析引擎**：原生二進位分析可用既有安裝的 **Hopper / Ghidra / IDA**（setup 可選擇安裝 Hopper）；純 JS / Electron 靜態分析不需要原生引擎。
- **CLI 與 MCP 共用同一套 work flow**。

**能分析什麼（README 的目標表）**：

| 目標 | REA 回傳 | 需求 |
|------|----------|------|
| 桌面安裝程式 | 執行期候選、支援檔案、元件標記、下一步探測 | 內建目錄／header 檢查 |
| 原生二進位 | 偽代碼、組譯、字串、符號、呼叫與引用 | Hopper / Ghidra / IDA |
| ELF 佈局 | sections、segments、原始符號／relocation | pwntools（Linux x64） |
| Go 二進位 | 編譯器版本、module、build 設定 | 內建 ELF/PE/Mach-O 檢查 |
| GPU 程式物件 | CUDA/HIP 目標、kernel 參數、PTX | 內建 fatbin/CUBIN/PTX 檢查 |
| 模型檔 | GGUF / safetensors metadata、tensor 宣告 | 內建 header 檢查 |
| IL2CPP metadata | Unity `global-metadata.dat` 型別與方法名 | 內建解碼 |
| Godot PCK | 封裝清單、抽取、header 事實 | 內建格式 2/3/4 |
| Rust 二進位 | cargo-auditable crate 名稱／版本／依賴 | 內建檢查 |

**注意**：Node.js 需求為 22.x（≥22.23.4）、24.x（≥24.22.1）或 26.12.1+；Linux 上部分功能需要 procps 相容的 `ps`。README 也特別提醒：**同名 repo 或複製的 README 不代表官方下載來源**，應從 morluto/rea、rea.tools 或 npm `rea-agents` 取得。授權 MIT。

---

## 2. debpalash/VoiceStudio — 全本地化的 ElevenLabs 替代品

![VoiceStudio 本地模型管理介面](/assets/images/trending-debpalash-voicestudio/img0.0.png)
![VoiceStudio 音色克隆工作區](/assets/images/trending-debpalash-voicestudio/img1.1.png)
![VoiceStudio 影片配音工作區](/assets/images/trending-debpalash-voicestudio/img2.png)

**它是什麼**：開源、**完全在本機執行**（Electron 桌面應用）的 ElevenLabs 替代品：音色克隆、音色設計、影片配音、口述轉錄、有聲書生成，官方宣稱支援 **646 種語言**。預設引擎是 `k2-fsa/OmniVoice`（VoiceStudio 引擎），也可切換其他引擎。

**四大工作區**：

| 工作區 | 功能 |
|--------|------|
| **Voice cloning** | 選一個聲音或加入乾淨的參考錄音，輸入文字即生成；缺模型時提示安裝 |
| **Voice design** | 用文字描述去「設計」一個聲音（不是複製既有錄音） |
| **Video dubbing** | 影片配上時間對齊的語音 |
| **Models** | 安裝／管理本地語音模型（PyTorch） |

**其他能力**：浮動口述小工具、故事／有聲書／批次任務、**本地 API 與 MCP（給 agent 用）**、可重用 recipe、watch folder（監看資料夾自動觸發）。

**硬體支援**：

| 硬體 | 支援 |
|------|------|
| NVIDIA GPU（Win/Linux） | CUDA 加速 |
| Apple Silicon | Metal（MPS） |
| 無獨顯（內顯／舊 PC） | 可用但慢；安裝約 5 GB 的 CPU 版 PyTorch |
| Windows on ARM | **實驗性**（ARM64 原生 app、x64 Python 在模擬下跑、僅 CPU） |
| Intel Mac | 僅 UI；需連遠端 backend |

**安裝**：macOS/Linux `curl -fsSL https://voicestudio.sh/install | sh`；Windows PowerShell `irm https://voicestudio.sh/install | iex`；也有 Releases 的 `.dmg` / `.exe` / `.AppImage` / `.deb` 與 Docker 指南。安裝器保留設定、專案與模型。

**隱私**：本機流程跑在你的硬體；遠端服務是可選的；使用分析需要你同意。授權 AGPL-3.0（注意：AGPL 對「提供網路服務」有較強的開源義務）。

---

## 3. stablyai/orca —「The AI Orchestrator for 100x builders」

![Orca 桌面版：多 agent 並行 worktree，右下角手機 companion](/assets/images/trending-stablyai-orca/img1.jpg)

**它是什麼**：一個**多 agent 工作台**（桌面 + 手機 + 遠端 runtime），讓 Codex、Claude Code、OpenCode、Pi 等**用你自己的訂閱**並排跑，每個 agent 各自在**獨立 git worktree**，全部集中在一處追蹤。核心賣點是「把一堆 agent 當成一個團隊來管」。

**主要功能**：

| 功能 | 說明 |
|------|------|
| **Parallel Worktrees** | 一個 prompt 同時分給五個 agent，各自隔離 worktree；比較結果、合併勝出的那個 |
| **Mobile Companion** | 手機監控與操控 agent，agent 完成時通知你、隨時追加指令（iOS App Store / Android APK） |
| **Terminal Splits** | Ghostty 等級的 WebGL 終端、無限分割、重啟後 scrollback 保留 |
| **Design Mode** | 在真正的 Chromium 視窗裡點任何 UI 元素，把它的 HTML、CSS 與裁切截圖直接送進 agent prompt |
| **GitHub & Linear 原生整合** | 在 app 內瀏覽 PR、issue、專案看板；從任何任務直接開 worktree，不切換上下文 |
| **SSH Worktrees** | 在遠端大機器上跑 agent，具備完整檔案編輯、git、終端；含自動重連與 port forwarding |
| **Annotate AI Diffs** | 在 diff 任何一行留言並送回 agent；在 Orca 內完成 review / edit / commit |
| **Drag Files to Agents** | VS Code 編輯器＋到處 autosave；把檔案或圖片拖進 prompt |

**平台**：macOS / Windows / Linux，README 提供中文、日文、韓文、西班牙文、法文、葡萄牙文版本。授權 MIT。

---

## 4. anomalyco/opencode — 開源 coding agent（CLI + 桌面 App）

![OpenCode landing 截圖](/assets/images/trending-anomalyco-opencode/img0.png)

**它是什麼**：老牌的開源 coding agent（2025-04 建立，總 Star 22 萬），同時有 CLI 與 **桌面 App（BETA）**。

**內建 agent**（用 `Tab` 切換）：

- **build** — 預設、全權限的開發 agent
- **plan** — 唯讀，用於分析與探索程式碼；預設拒絕檔案編輯、執行 bash 前要先問；適合探索陌生 codebase 或規劃改動
- **general** — 內部使用的子 agent，處理複雜搜尋與多步任務，訊息中用 `@general` 叫它

**安裝**：`curl -fsSL https://opencode.ai/v2/install | bash`；npm / bun / pnpm / yarn `npm i -g @opencode/cli@latest`；Homebrew `brew install anomalyco/opencode-v2`（推薦，更新最快）、`brew install opencode`（官方 formula，較慢更新）；Arch `pacman -S opencode` / `paru -S opencode-beta`；`mise use -g opencode`；`nix run github:anomalyco/opencode`。安裝腳本落在 `$HOME/.opencode/bin`。

**桌面版下載**：macOS arm64 / intel `.dmg`、Windows x64 `.exe`、Linux `.deb` / `.rpm` / `.AppImage`；macOS 也可 `brew install --cask opencode-desktop`。

**注意事項**：README 提醒先移除 0.1.x 以前的舊版本；若你的專案名稱含「opencode」（如 opencode-dashboard）需在 README 聲明**非 OpenCode 官方出品**。授權 MIT。

---

## 5. heygen-com/hyperframes —「Write HTML. Render video. Built for agents.」

![HyperFrames 設計模板：Biennale Yellow](/assets/images/trending-heygen-com-hyperframes/img0.0.png)
![HyperFrames 設計模板：BlockFrame](/assets/images/trending-heygen-com-hyperframes/img1.1.png)

**它是什麼**：把**影片定義成 HTML** 的渲染引擎。你在 HTML 裡寫 `data-*` 屬性（時間、軌道）＋ GSAP / CSS / Lottie / Three.js / Anime.js / WAAPI 的 seekable 動畫，CLI 用 headless Chrome 逐幀 seek、FFmpeg 編碼。主打「agent 本來就會寫 HTML」——所以 agent 可以直接產影片。

**範例（README 的 composition）**：

```html
<div id="stage" data-composition-id="launch" data-start="0"
     data-width="1920" data-height="1080">
  <video class="clip" data-start="0" data-duration="6"
         data-track-index="0" src="intro.mp4" muted playsinline></video>
  <h1 id="title" class="clip" data-start="1" data-duration="4"
      data-track-index="1">Launch day</h1>
  <audio data-start="0" data-duration="6"
         data-track-index="2" data-volume="0.5" src="music.wav"></audio>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.from("#title", { opacity: 0, y: 40, duration: 0.8 }, 1);
    window.__timelines = window.__timelines || {};
    window.__timelines.launch = tl;
  </script>
</div>
```

**為什麼選它**：HTML-native（不強制 React）、agent-friendly（CLI 預設非互動）、**deterministic**（同輸入同輸出，適合 CI 與回歸測試）、**無 build step**（`index.html` 直接在瀏覽器播放）、adapter 式動畫、Apache 2.0 且**沒有 per-render 費用**。

**HyperFrames vs Remotion**：

| 面向 | HyperFrames | Remotion |
|------|-------------|----------|
| 撰寫方式 | HTML + CSS + seekable 動畫 | React 元件 |
| Build step | 無；`index.html` 直接播 | 需要 bundler |
| Agent 交接 | 純 HTML 檔 | JSX / React 專案 |
| library-clock 動畫 | 可 seek、逐幀精準 | 需小心處理 wall-clock 模式 |
| 分散渲染 | 本機 + AWS Lambda | Remotion Lambda（成熟） |
| 授權 | Apache 2.0 | Remotion License（source-available） |

**Skills**：附 7 個 agent skills，核心組是 `/hyperframes`、`/hyperframes-cli`、`/hyperframes-registry`、`/media-use`（`npx hyperframes skills update`）；`/figma`、`/slideshow`、`/remotion-to-hyperframes` 按需安裝。**Frame.md** 概念：把 web 的 `design.md` 轉譯成「給鏡頭用」的設計 token，讓 agent 不必猜尺度。

---

## 6. Comfy-Org/ComfyUI — 最強模組化 diffusion GUI／API／backend

![ComfyUI 官方 README 的節點介面示意](/assets/images/trending-comfy-org-comfyui/img0.0.png)

**它是什麼**：以**節點圖**建構與重用影像／影片／音訊／3D／文字工作流的本地推理引擎，宣稱「世界最快的本地推理引擎」。特色如下：

- **視覺節點圖**，免寫程式；可重用 subgraph、workflow 模板、App Mode、本地 API。
- **效率**：async queueing、partial graph 重執行、smart VRAM/RAM 管理、model offloading、支援量化模型。
- **模型支援極廣**（README 的代表清單）：
  - 影像生成：SD1.5、SDXL、SD3.5、Flux.1 / Flux.2、Qwen Image、Z-Image、Hunyuan Image 2.1、HiDream、Lumina 2.0、Chroma、LongCat、Ideogram 4、Krea 2、MageFlow、Microsoft Lens、PixelDiT、Kandinsky 5、Ernie、Moss
  - 影像編輯：Flux Kontext、Flux.2 Klein、Qwen Image Edit、HiDream E1.1/O1、OmniGen2、Boogu、JoyImage Edit、MageFlow Edit、LongCat Edit
  - 影片：Wan 2.1/2.2、LTX-Video 2/2.3、HunyuanVideo 1.5、Kandinsky 5 Video、CogVideoX、Cosmos Predict2、Bernini-R、SCAIL 2、Mochi
  - 音訊／音影：MiniMax H3、LTX-AV；音訊生成 ACE-Step 1.5、Stable Audio 3、MiniMax Music 3、Yue 2
  - 3D／視覺：Hunyuan3D 2.1、TripoSplat、SeedVR2、SUPIR、Depth Anything 3、MoGe、SAM 3/3.1、RT-DETRv4、BiRefNet
  - 文字：Gemma 3/4、Qwen3、Qwen3.5、Qwen3-VL（含多模態輸入）
- **內建工具**：inpainting、outpainting、reference conditioning、mask/compositing、model merging、upscaling、frame interpolation、segmentation、depth estimation、media processing。
- **可存／載工作流 JSON**，也能從生成媒體反推工作流與 seed。
- **完全離線**：核心不主動下載任何東西；`--offline` 可停用可選的付費 Comfy API nodes。

授權 GPL-3.0（注意 copyleft：若你把 ComfyUI 併進商業產品，需留意授權傳染）。

---

## 7. anthropics/claude-plugins-official — Anthropic 官方 Claude Code 插件目錄

（README 無圖，僅結構說明；本節不附示意圖以免造成誤導）

**它是什麼**：Anthropic 管理的高品質 **Claude Code 插件目錄（marketplace）**，分兩類：

- `/plugins` — Anthropic 自建的內部插件
- `/external_plugins` — 合作夥伴與社群提交的第三方插件（需通過品質與安全審核）

**安裝**：`/plugin install {plugin-name}@claude-plugins-official`，或 `/plugin > Discover` 瀏覽。提交新插件走 `https://clau.de/plugin-directory-submission`。

**插件結構**：

```
plugin-name/
├── .claude-plugin/plugin.json   # 必要 metadata
├── .mcp.json                    # 選用 MCP server
├── commands/                    # 選用斜線命令
├── agents/                      # 選用 agent 定義
├── skills/                      # 選用 skills
└── README.md
```

**兩個容易踩坑的規則**：

1. **插件 `name` 是不可變的 slug**——一旦發布就不能改名，否則使用者安裝會出現 `plugin-not-found`；要改顯示名稱請改 `displayName`。真的非改不可時，在 `.claude-plugin/marketplace.json` 的 `renames` map 裡寫 `{"old-name":"new-name"}`，loader 會在下一次 sync 時自動遷移。
2. **skill-bundle plugin**：當來源 repo 只提供 `SKILL.md` 而沒有 `.claude-plugin/plugin.json` 時，marketplace 條目可用 `strict: false` 直接宣告 skills，路徑相對於 `source.path`；一個條目可跨多個子目錄挑選（如 `["./libA/skill-1","./libB/skill-2"]`），每個 skill 註冊為 `<plugin-name>:<skill-name>`。

**安全提醒**：Anthropic 明確聲明**不控制**插件內含的 MCP server、檔案或其他軟體，也無法驗證其行為，安裝前必須自行評估信任。授權 Apache-2.0（個別插件各有 LICENSE）。

---

## 8. NationalSecurityAgency/ghidra — 美國 NSA 的軟體逆向工程框架

![Ghidra 官方形象圖](/assets/images/trending-ghidra/img0.png)

**它是什麼**：NSA 釋出的 **SRE（Software Reverse Engineering）框架**，Java 寫成、Apache-2.0，2019 年起開源。它不是本週的新專案，但本週仍新增 4,221 Star——反映 REA 這類 agent 逆向工具帶動的老牌工具熱度。

**功能面**：反組譯／反編譯（decompiler）、符號與引用追蹤、腳踏分析（script）、跨平台 binaries、可擴充的使用者 script 與 extension、插件式架構。

**安裝官方預建版**：

1. 安裝 **JDK 25 64-bit**
2. 從 Releases 下載 `ghidra_<version>_<release>_<date>.zip`（Assets 下拉；**不要下載名為 "Source Code" 的檔案**）
3. 解壓（**不要解壓在既有安裝之上**）
4. 啟動 `./ghidraRun`（Windows `ghidraRun.bat`）或 `./support/pyghidraRun`（PyGhidra）

**自行建置**：需 JDK 25、Gradle 9.1.0+（或 repo 內 wrapper）、Python 3.9–3.15（含 pip）、Linux/macOS 上的 GCC/Clang + make、Windows 上的 Visual Studio 2017+ 或 C++ Build Tools（MSVC、Windows SDK、C++ ATL）。

```bash
git clone https://github.com/NationalSecurityAgency/ghidra.git
cd ghidra-master
gradle -I gradle/support/fetchDependencies.gradle
gradle buildGhidra      # 產出在 build/dist/
```

---

## 9. akitaonrails/ai-memory — 跨 agent、跨機器、跨專案的長期記憶

![ai-memory 標誌](/assets/images/trending-akitaonrails-ai-memory/img0.0.png)

**它是什麼**：Rust 寫的**單一自包含執行檔**，為 coding agent 提供「長期記憶 + 交接」。解決的是每個 agent 記憶都有的三個限制：**只在一台機器、只屬於一個 agent、切換工具就消失**。

**九個核心設計**：

| 特性 | 說明 |
|------|------|
| **跨 agent** | 20 多種 harness（Claude Code、Codex、Cursor、Gemini CLI、OpenCode、Grok、Devin、Kimi、Kiro…）共用一份記憶；交接是**typed protocol**，有 owner、只能被 claim 一次 |
| **跨 session（不只摘要）** | `ai-memory run` 啟動 agent：quit Claude Code 後 `ai-memory run codex`，Codex 會得到共享 workstream + Claude 原生可見歷史的**本機私有投影**；遠端 server 只收到 harness 與 session 身分，**從不收到本機 transcript 路徑或內容** |
| **跨專案** | 一個「你平常怎麼工作」的小 profile（套件管理器、測試佈局、架構習慣）在每次 session 開始時帶進新 repo；單人預設開啟，共享 server 上則 opt-in、每人私有 |
| **跨機器** | 記憶存在你自己跑的 server（同一台筆電、homelab、任何地方），桌面上沒做完的專案可在筆電續做 |
| **團隊可用** | 所有人指向同一 server，則某人 session 學到的知識，其他人的 agent 也能 retrieve；知識按專案共享，個人交接仍私人。多人 auth、person attribution、audit log 內建，**不是付費層** |
| **記憶是純 markdown** | 真實來源是 git-backed wiki of `.md`：可 `grep`、Obsidian 開、手改、`rsync`；資料庫只是衍生索引，可隨時從檔案重建。**沒有要維護的 vector store** |
| **靜默捕捉** | lifecycle hooks 記錄 prompts、tool calls、session 邊界，在 typed privacy boundary 上消毒後才存；server 再彙整成可讀頁。**預設路徑零 LLM 呼叫**（capture / search / handoff 都不需要 API key） |
| **不用 LLM 的老化機制** | 記憶依可調 tier 曲線衰減，但「被使用」的記憶衰減更慢（開頁、搜尋、經連結到達都算使用）；cold 的 episodic 筆記可壓縮成 durable facts（路徑、錯誤碼、決策）而非丟棄；近似重複會合併、可能矛盾會被標記——**零 API 呼叫**。硬刪除不存在：原始留在 git，`restore-page` 可還原 |
| **可選「dream」** | 若配置了 LLM，可開啟背景 pass，在你閒置時把 cold 筆記重寫成連貫頁，你一回來就取消；不刪任何來源，預設關閉，且要先通過 recall eval |

**流程**：

```
capture ──▶ consolidate ──▶ recall ──▶ handoff
hooks         session-end      search      next agent
observe       summaries as     + brief     any harness
silently      wiki pages       injection
```

**誠實性設計**：purge 命令明確說明「deleted」的含義；寫入上限（約 700/s）是**實測**而非猜測；所有變更都有 audit log。授權 MIT。

---

## 10. ruvnet/ruflo — Claude Code / Codex 的 agent meta-harness

**它是什麼**：一個 **agent harness**（執行層），環繞 Claude Code 與 Codex，加上 **100+ 專用 agent、協調 swarm、自我學習記憶、跨機器 federation、企業安全護欄**。口號：「Agent = Model + Harness」——model 負責寫，harness 給它工具、記憶、迴圈、沙箱與控制。

**三種安裝路徑**：

1. **Claude Code 插件**（需 Claude Code ≥ 2.1.287）：
```text
/plugin marketplace add ruvnet/ruflo
/plugin install ruflo-core@ruflo
/plugin install ruflo-console@ruflo
/plugin install ruflo-mods@ruflo
/reload-plugins
/ruflo
```
`core` = 基礎工具；`console` = agent cockpit；`mods` = Claude Code 內的 routing 與 policy enforcement（以你的帳號權限執行，**安裝前請先讀它們的程式碼**）。

2. **Codex / 其他 MCP 工具**：
```bash
npx ruflo@latest init wizard
# MCP stdio server 設定：command=npx, args=["-y","ruflo@latest","mcp","start"]
```

3. **純終端（可選）**：`npx ruflo tui`（加 `--plain` 只印一幀），含 Overview、Cost、Swarm、Events、Missions 與可選 AI 頁。

**能力**：`npx ruflo init` 給 Claude Code 一套「神經系統」——agent 自組織成 swarm、每次任務都學習、跨 session 記憶、並透過 federation 與其他機器上的 agent 安全溝通而不洩漏資料。另可選 **ruOS Desktop**（`https://ruos.cognitum.one` 可用 MCP 連 ChatGPT/Claude）。README 附 ruOS、RuVector 等推廣內容。授權 MIT。

---

## 橫向比較：這週前十名在「AI Agent 工具鏈」裡的位置

| 層次 | 專案 | 解決什麼 |
|------|------|----------|
| **Agent 執行（harness）** | opencode、orca、ruflo | 誰來跑 agent、怎麼並行、怎麼協作 |
| **Agent 記憶** | ai-memory | 跨 agent／機器／專案的知識延續 |
| **Agent 能力擴充（MCP／skill）** | rea、claude-plugins-official | 讓 agent 能做逆向、能裝插件 |
| **Agent 產出物** | hyperframes | agent 寫 HTML 直接渲染影片 |
| **本地模型產品化** | ComfyUI、VoiceStudio | 把擴散模型／語音模型做成可用的 GUI |
| **基礎方法論工具** | ghidra | 逆向工程的傳統骨幹（被 REA 帶動熱度） |

**觀察**：

1. **「agent 工具鏈」占 7 席**（1、3、4、5、7、9、10）——這週的主題不是單一 killer app，而是「agent 的作業系統化」。
2. **本週爆量的第一名 REA（+88,243★）** 是「把逆向工程變成 MCP」；這種「技能型 MCP」在 2026 年明顯成為 GitHub 的流量來源。
3. **新專案建立時間都非常近**（rea 2026-04、VoiceStudio 2026-04、orca 2026-03、hyperframes 2026-03、ai-memory 2026-05），顯示 2026 上半年開始有一波「agent 基礎設施」創業式開源。
4. **授權差異值得注意**：VoiceStudio AGPL-3.0、ComfyUI GPL-3.0 是 copyleft；其餘多為 MIT / Apache-2.0。若要做商業整合，前兩者需先確認授權傳染。

---

## 引用與資料出處

- GitHub Trending（weekly）：`https://github.com/trending?since=weekly`，抓取於 2026-10-24。
- Star / Fork / License / 建立時間：GitHub REST API `https://api.github.com/repos/{owner}/{repo}`。
- 功能描述均取自各 repo 的 `README.md`（raw.githubusercontent.com，main/master 分支）。
- 圖片均為各 repo README 內引用的原始圖片，已下載為本地資產（避免外部連結失效）。

> 提醒：所有數字為抓取當下的快照，Trending 排名會隨時間變動；功能敘述以 README 為準，部分專案仍在 beta（如 OpenCode 桌面版、Windows on ARM 的 VoiceStudio）。
