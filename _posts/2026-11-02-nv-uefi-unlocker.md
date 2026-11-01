---
title: "NV-UEFI-Unlocker：在 UEFI 預驅動層解鎖 NVIDIA GeForce 的 Tensor 算力"
date: 2026-11-02
description: 一個 Rust 寫的 UEFI 開機工具，在驅動載入前解開 RTX 20/30/40 系列被鎖住的 Tensor 發射速率，FP16/BF16 最高約 2.6 倍，不刷 VBIOS、斷電即恢復原狀。
tags: [NVIDIA, GPU, UEFI, AI, 開源, 硬體解鎖]
---

# NV-UEFI-Unlocker：在 UEFI 預驅動層解鎖 NVIDIA GeForce 的 Tensor 算力

> 專案位址：<https://github.com/physicsdolphin/nv-uefi-unlocker>

你的 GeForce 顯示卡跑 AI 工作負載時，很可能正以「半速」運行——這不是散熱問題，而是 NVIDIA 在驅動層對 GeForce 產品線施加的 Tensor 核心發射速率限制。[NV-UEFI-Unlocker](https://github.com/physicsdolphin/nv-uefi-unlocker) 是一個開源的 UEFI 預驅動工具，在 NVIDIA 驅動載入**之前**直接對 GPU 韌體執行簽名引導鏈，把這個鎖打開。

它於 2026-10-26 開源，一週內衝到 950+ 顆星，被 Tom's Hardware、TechPowerUp、Wccftech 等媒體相間報導，是目前 RTX 20/30/40 系列少見的「系統級別、免刷寫」算力解鎖方案。

## 基本資料

| 項目 | 內容 |
| --- | --- |
| 倉庫 | [physicsdolphin/nv-uefi-unlocker](https://github.com/physicsdolphin/nv-uefi-unlocker) |
| 語言 | Rust（`x86_64-unknown-uefi` 目標） |
| 授權 | GPL-2.0-only |
| 最新版本 | v2.1.8（2026-10-31） |
| 支援系統 | Windows / Linux / Hackintosh 等任何 UEFI 開機系統 |
| 支援顯示卡 | GTX 16（理論）、RTX 20 / 30 GA10x / 40 全系（筆電與桌機） |
| 不支援 | Pascal 及更早、GA100（A100/A30）、Hopper、RTX 50（Blackwell） |

## 為什麼 GeForce 的 AI 效能被「砍半」？

NVIDIA 在資料中心卡（Tesla/Quadro 系）與 GeForce 消費卡之間有明確的產品區隔。GeForce 卡上的 Tensor Core 硬體本身支援完整的 FP16/BF16/TF32 發射速率，但驅動與韌體層的 **PLM（Power Limit Management）控制暫存器**會寫入一組「速率覆蓋值」（SS0/SS1 selector），把 AI 路徑的發射率壓到約一半。

關鍵在於：**這些受保護的覆蓋值，主機端（OS 裡的驅動、超頻工具）不能直接改寫**——PLM 寫權限被鎖住，所以傳統的軟體超頻工具對這個限制完全無能為力。

## 解鎖原理：簽名韌體引導鏈

NV-UEFI-Unlocker 的做法是繞過 OS，在 UEFI 環境（NVIDIA 驅動尚未載入、PLM 門尚未完全鎖死時）對 GPU 執行一條完整的事務鏈：

```text
SEC2 scrubber → FWSEC/WPR2 解除 → 簽名 Booter 點火 → V67 四寫負載 → 讀回驗證 → 交棒系統開機機
```

1. **SEC2 scrubber**：清除 SEC2 安全核心的阻擋狀態（Ampere/Ada）。
2. **FWSEC / WPR2**：解除寫保護區域，讓簽名韌體可被載入。
3. **簽名 Booter**：載入 NVIDIA 原廠簽名的 GSP-RM 韌體段（簽名在交棒前會恢復原狀），透過 Booter 中的 V67/ROP 路徑打開 PLM 寫權限。
4. **V67 四寫負載**：寫入速率覆蓋值（SS0=`0x88888888`、SS1 低四位 `0x8`）。
5. **讀回驗證**：每一步都以讀回為驗收依據，寫入狀態碼不算數；完成後寫 `loader.log` 並自動鏈回 Windows Boot Manager / Linux shim / systemd-boot 等。

三个重要安全特性：

- **不刷寫 VBIOS**：所有修改都是易失性的，**斷電即恢復原廠狀態**；
- **不寫系統 ESP**：只從 U 盤一次性開機選單進入，不動永久開機順序；
- **韌體不隨包分發**：NVIDIA 韌體由腳本從釘選版本的公開包下載、逐位元組校驗後本地再生，下載校驗失敗即停止。

各家族的執行判據略有不同：Ada 檢查 marker、HALT 與 FLR 後 AON 狀態；Ampere 以 PLM 翻轉驗證執行；Turing 的 FEAT 位在 `0x4096xx`，寫完選擇器後會重鎖 PLM 並跳過 FLR。

## 實測增益

README 標稱（逐卡數據見官方[兼容性矩陣](https://github.com/physicsdolphin/nv-uefi-unlocker/blob/main/docs/compatibility.md)）：

| 負載 | 增益 |
| --- | --- |
| FP16 / BF16 / TF32 張量吞吐 | 最高約 **2.6×** |
| FP8 | 最高約 **1.9×** |
| 圖像 / 影片生成（Stable Diffusion、ComfyUI 類） | **+14–75%** |
| DirectML 推論算子 | 最高 **+94%** |

官方歸檔的代表性實測：

- **RTX 2080（TU104）**：v2.1.8 修掉 0x91 競態後，FP16 從 34.9 → **69 TFLOPS**（約 2 倍）；
- **RTX 4090 Laptop / Alienware m18 R1**：FP16/BF16/FP8 約 **2 倍**，控制組持平；
- **RTX 3060（2504）** 等多款卡通過全鏈＋系統側效能驗證。

官方同時提醒：增益受**功耗牆、頻率、散熱與負載精度路徑**制約，微基準倍率不能直接當做所有應用的倍率。桌機高階卡（如 4090）本來就有功耗牆，解鎖後被功耗牆吃掉的部分收益會縮小。

## 兼容性速覽

| 系列 | 支援情況 | 前置條件 |
| --- | --- | --- |
| GTX 16（Turing） | 理論相容，待實機驗證 | GSP-RM |
| RTX 20（Turing） | 全系相容，部分型號有已知問題 | Windows 需先啟用 GSP-RM 並重啟 |
| RTX 30 GA10x | 全系相容（筆電＋桌機） | 無特殊前置 |
| RTX 40（Ada） | 全系相容（筆電＋桌機） | 入口時 GPU 有電且完成初始化 |
| Pascal 及更早 / GA100 / RTX 50 | ❌ 不支援 | — |

證據分級做得很嚴謹：✅＝本工具實機證據、🟢＝上游/社區同鏈矽驗證、🟡＝程式碼路徑存在待驗證。例如 4060 Ti（2803/2805）、4070 Super（2783）、3080（2206）、2070（1f07）都有全鏈實測；4090D（2685）則是上游硅驗證層級。

## 使用流程

### 1. 下載與前置

從 [Releases](https://github.com/physicsdolphin/nv-uefi-unlocker/releases) 下載發佈包並解壓。準備一支 **FAT32 U 盤**（先備份）。目標機器須 UEFI 開機、**關閉 Secure Boot**（或為 EFI 自簽憑證並信任）。筆電優先使用獨顯直連，從系統選「重啟」進一次性開機選單。

**Turing（RTX 20 / GTX 16）用戶**先在目標機的系統管理員 PowerShell 跑一次，再重啟：

```powershell
.\enable-turing-unlock.ps1
```

這會為顯示設備設定 `EnableGpuFirmware=1`（GSP-RM 模式）。沒有它，Windows 驅動接管解鎖狀態時可能 TDR / Code 43。

### 2. 製作開機 U 盤

在**目標機**的解壓目錄直接執行（腳本自動識別顯卡世代，只下載對應韌體並校驗）：

```powershell
# Windows PowerShell
.\make-usbroot.ps1
```

```bash
# Linux / WSL / Git Bash
bash make-usbroot.sh
```

跨機製作時顯式指定世代：40 系 `-Family 40`、30 系 `30`、20/16 系 `20`，`-Family all` 把三代韌體全打進同一支 U 盤。產物複製到 U 盤：

```text
U 盤（FAT32）
├── EFI/BOOT/BOOTX64.EFI   ← 開機程式（替換前備份原檔）
└── 韌體檔案（腳本末尾列出的 .bin）
    booter_load_F.bin / gsp_boot_F.bin / fwimage_F.bin
    v67-F-four-plm.bin（解鎖負載）/ scrubber_ad10x.bin ...
```

### 3. 開機執行與驗證

1. 從一次性開機選單選 U 盤；
2. 版本畫面按**空白鍵或 Enter** 執行（其他鍵或 30 秒無操作會中止）；目標 GPU 短暫黑屏屬正常；
3. 工具完成後自動鏈回系統，日誌在 U 盤根目錄 `loader.log`；
4. 進系統後驗證：Windows 用發佈包的 `ssdiag-x86_64-windows.exe`（唯讀診斷，`--reapply` 可在門仍開放時重寫選擇器）；Linux 在原始碼樹跑 `sudo python3 tools/diag-unlock.py`。

**每次冷啟動都需要重放**——解鎖是易失的，斷電就沒了。

## 常見坑與排障要點

官方 FAQ 把踩過的坑全部歸檔，以下是最實用的幾條：

| 症狀 | 原因與處置 |
| --- | --- |
| booter 狀態碼 `0x89` | GPU 上游 PCI 橋未開 Bus Master，DMA 讀不到 WPR 描述元。loader 已自動開橋 BME 並在日誌記 `DMA-PATH`/`BRIDGE-BME`；AMI 主板的 "BME DMA Mitigation" 保持預設即可 |
| Turing 回 `0x91` | FWSEC 尾聲競態——v2.1.8 已把「等 FWSEC 真正收尾再點火」的根因修復轉正 |
| 事務成功後黑屏/復位 | 部分 AMI 韌體在 GOP 重連卡死；斷電後在 U 盤根放 `no-reconnect.txt` 跳過重連 |
| Linux 日誌全綠但無增益 | RTD3 讓閒置 GPU 進 D3cold 清掉易失解鎖；設 `NVreg_DynamicPowerManagement=0x00` 後 `update-initramfs -u` 重啟 |
| 休眠喚醒後失效 | 休眠/D3 門控入口會掉狀態，一律用「重啟」進入，並用 ssdiag 讀回確認 |
| 雷電 eGPU | 不保證保留；隧道重建、hot reset 可能清掉解鎖，門若仍開可用 `--reapply` 寫回 |

**黑屏 / STOP 後的恢復鐵律：同一個開機會話內不要重試。** 完全斷電（筆電做 EC 放電）→ 拔 U 盤 → 走原開機項啟動 → 保留 `loader.log` 排障，必要時 DDU 重裝驅動。黑屏不等於硬體永久損壞——解鎖本來就斷電即恢復。

## 安全約束與風險邊界

專案自己列明的實現邊界（值得全部讀一遍再上手）：

- 寫入以**讀回**為驗收依據，「執行完成」提示不構成獨立執行證明；
- 只從 U 盤一次性開機選單進入，不覆寫系統 ESP、不設常駐 BootOrder；
- NVIDIA 韌體從釘選版本輸入本地生成，校驗失敗即停止，不隨倉庫分發；
- 尚未實現逐卡 ROM SHA-256 強制比對（只有家族 PROM CRC32 路由）；
- Falcon DMA 仍屬實驗代碼；描述符解析 V1 未實現；
- 與 [nvoc](https://github.com/Skyworks-Neo/nvoc)（系統內功耗/電壓/超頻控制）疊加後，功耗與溫度可能大幅超出原廠包絡，散熱與供電餘量自負責任。

這是一個「韌體級寫操作」工具，官方在 README 裡對中止語義、日誌判讀、失敗路徑都寫得異常謹慎——這種證據等級的文檔品質在開源硬體工具裡相當少見。

## 開發者資訊

Rust 工具鏈自行構建：

```bash
rustup target add x86_64-unknown-uefi
cargo build --release   # 宿主 assets/sim
cargo efi-tx            # 事務版 loader.efi（cargo efi 為唯讀採樣版）
```

倉庫結構：`loader/`（UEFI 應用）、`assets/`（下載/校驗/負載生成）、`sim/`（宿主模擬器與事務測試）、`tools/`（系統內診斷）、`docs/evidence/`（原始實驗證據）。

專案自述是「社區工作的直接受益者與衍生者」，[credits.md](https://github.com/physicsdolphin/nv-uefi-unlocker/blob/main/docs/credits.md) 把上游血緣整理成圖譜：事務鏈母本 [gpu-unlock](https://github.com/Zagitta/gpu-unlock)、AD10x 四寫鏈源頭 [gpu-unlock-ada](https://github.com/JustAResearcher/gpu-unlock-ada)、Turing 譜系 [cmp50hx-unlock](https://github.com/xrip/cmp50hx-unlock) / [turing-unlock](https://github.com/nlzy/turing-unlock)、引導路徑考據權威 [open-gpu-kernel-modules](https://github.com/NVIDIA/open-gpu-kernel-modules)，以及 ReBarUEFI、envytools 等寄存器與逆向工具鏈。

值得一提的是，README 附了一份 [AGENTS.deploy.md](https://github.com/physicsdolphin/nv-uefi-unlocker/blob/main/AGENTS.deploy.md) 部署指南，直接丟給 AI Agent 就能幫你完成安裝——專案主動擁抱 agent 部署流程，相當新穎。

## 小結

NV-UEFI-Unlocker 填補了一個長期空白：GeForce 的 Tensor 速率鎖在 OS 層完全不可觸及，而它在 UEFI 預驅動視窗期內是可解的。這個方案以「簽名韌體引導鏈＋讀回驗證＋斷電還原」把風險壓到可複審的範圍，文件與證據鏈的嚴謹度遠超同類工具。

適合誰：手上有 RTX 20/30/40（尤其筆電卡、4060/4070 系）、跑 Stable Diffusion / ComfyUI / LLM 推論、且不介意每次冷啟動重放 U 盤事務的人。RTX 50 與 GA100 系列不在支援範圍，Pascal 及更舊卡同樣無解。

## 延伸閱讀

- 官方文件：[兼容性矩陣](https://github.com/physicsdolphin/nv-uefi-unlocker/blob/main/docs/compatibility.md) · [FAQ](https://github.com/physicsdolphin/nv-uefi-unlocker/blob/main/docs/faq.md) · [致謝圖譜](https://github.com/physicsdolphin/nv-uefi-unlocker/blob/main/docs/credits.md)
- 原理科普（Bilibili，簡中）：[專業用戶版](https://www.bilibili.com/opus/1264436370549506065) · [入門用戶版](https://www.bilibili.com/opus/1264493051219279872)
- 媒體報導：[Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/open-source-usb-tool-unlocks-nvidias-half-speed-gpu-ai-limiter-on-windows-lifts-gpus-fp16-math-performance-up-to-65-percent-uefi-unlocker-covers-rtx-20-30-and-40-series-desktops-and-laptops) · [TechPowerUp](https://www.techpowerup.com/354316/new-uefi-tool-lifts-nvidias-tensor-cap-on-rtx-20-to-40-series-cards-in-windows?type=Tools) · [Wccftech](https://wccftech.com/new-nvidia-uefi-gpu-unlocker-brings-up-to-75-higher-ai-compute-performance-to-rtx-20-30-40-series-gpus-on-windows/) · [HKEPC](https://www.hkepc.com/27140/)
- 搭配工具：[nvoc](https://github.com/Skyworks-Neo/nvoc)（系統內功耗/電壓控制）、[cli-stressor-cuda-rs](https://github.com/Skyworks-Neo/nvoc/tree/main/cli-stressor-cuda-rs)（吞吐測試）

![Star History](https://api.star-history.com/svg?repos=physicsdolphin/nv-uefi-unlocker&type=date&legend=top-left)
