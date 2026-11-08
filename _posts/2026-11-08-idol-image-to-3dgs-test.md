---
title: "Idol 實測：單張圖片生成 3D Gaussian Splat（Windows + RTX 3090 完整測試筆記）"
date: 2026-11-08
description: speridlabs/idol 是 Apache 2.0 的 image-to-3D 模型，600M 參數、7.2 GB VRAM、產出標準 .ply。本文記錄 Windows 上的完整安裝、CUDA 版 PyTorch 陷阱、triton 缺解與實測結果。
tags: [AI, 3D, Gaussian-Splatting, HuggingFace, Windows, PyTorch]
---

# Idol 實測：單張圖片生成 3D Gaussian Splat

[Speridlabs 的 Idol](https://huggingface.co/speridlabs/idol) 是一個完全開放（Apache 2.0）的 image-to-3D 模型：**一張物件照片 → 最多 1,048,576 個 3D Gaussian**，連照片沒拍到的背面都能生成，輸出為標準 3DGS `.ply` 檔。

核心規格：

| 項目 | 數值 |
|---|---|
| 參數量 | ~600M（DiT 370M + Octree decoder 51M + Gaussian decoder 237M） |
| VRAM 峰值 | 7.2 GB（消費者顯示卡可跑） |
| 生成速度 | 官方 3.4s（262k splats）；本機 RTX 3090 約 61s（未開快速採樣） |
| 輸入 | 渲染圖、AI 生成圖、實拍照片皆可（自動去背 + 裁切） |
| 輸出 | 標準 3DGS `.ply`，任何 Gaussian Splatting 檢視器可開 |

![扶手椅範例](/assets/images/idol/armchair.webp)
![燈具範例](/assets/images/idol/lamp.webp)

## 安裝前提：兩個被限制的影像編碼器

Idol 讀圖時要用兩個 HuggingFace gated 模型，**必須先用 HF 帳號同意授權條款**，否則第一次執行就會停住：

1. [facebook/dinov3-vith16plus-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vith16plus-pretrain-lvd1689m)
2. [black-forest-labs/FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev)（只會下載它的 VAE）

同意後登入一次即可：

```bash
hf auth login     # 或設定環境變數 HF_TOKEN
```

程式碼與權重沒有獨立下載步驟，第一次執行會自動抓進 HuggingFace cache（Idol 權重約 3 GB）。

```bash
git clone https://github.com/speridlabs/idol-sdk.git
cd idol-sdk
pip install -e .          # Python 3.10+, PyTorch 2.5+, NVIDIA GPU
```

## Windows 環境的兩個坑（實測必踩）

### 坑一：PyPI 裝到 CPU 版 PyTorch → deform_conv2d CUDA 錯誤

`pip install torch` 在 Windows 預設抓到的是 **CPU build**，模型跑到 BiRefNet 去背網路時會噴：

```
NotImplementedError: Could not run 'torchvision::deform_conv2d'
with arguments from the 'CUDA' backend.
```

解法：從 PyTorch 官方 cu126 index 強制重裝 GPU 版（torch 與 torchvision 要同 index、版本配對）：

```bash
pip install --index-url https://download.pytorch.org/whl/cu126 \
    --force-reinstall --no-deps torch
pip install --index-url https://download.pytorch.org/whl/cu126 \
    --force-reinstall --no-deps "torchvision==0.29.1+cu126"

# 驗證
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
# 2.14.1+cu126 True
```

### 坑二：Windows 沒有 triton → torch.compile 噴 TritonMissing

Idol 預設開啟「快速採樣」（torch.compile + cuDNN attention，約 1.7x），但 **triton 在 Windows 上裝不起來**（`pip download triton` 找不到任何發行版），取樣第一步就噴：

```
torch._inductor.exc.TritonMissing: Cannot find a working triton installation.
```

解法很簡單：**加 `--no_optimize` 旗標**關掉編譯快速採樣，品質完全相同、速度慢約 1.7 倍。Linux 使用者不受這個坑影響。

順帶一裝 `pip install accelerate`，模型載入省記憶體（沒裝會有一條警告但不影響結果）。

## 實測命令與結果

```bash
cd F:/AI/idol-sdk
HF_TOKEN=$(cat ~/.cache/huggingface/token) \
  python -m idol.sample --image t1.jpg --mode real --no_optimize
```

RTX 3090 實測：**50 steps 約 61 秒**，exit code 0，產出三個檔案：

| 檔案 | 內容 |
|---|---|
| `outputs/t1.ply` | 17.8 MB，262,144 個 Gaussian（x/y/z、SH 色係數、opacity、scale、rotation） |
| `outputs/t1_input.png` | 模型實際看到的圖（去背 + 裁切後） |
| `outputs/t1_camera.json` | 預測的輸入相機參數 |

![測試輸入圖](/assets/images/idol/t1_input.png)

用 plyfile 驗證 `.ply` 內容：

```python
from plyfile import PlyData
p = PlyData.read('outputs/t1.ply')
print(p['vertex'].count)   # 262144
```

## 模式選擇與常用旗標

| `--mode` | 適用輸入 | 裁切留白 |
|---|---|---|
| `synthetic`（預設） | 渲染圖、AI 生成圖 | 物件佔畫面 1/1.2 |
| `real` | 實拍照片 | 物件佔畫面 1/1.7 |

| 旗標 | 預設 | 說明 |
|---|---|---|
| `--seed` | 42 | 固定可重現同一個物件 |
| `--steps` | 50 | 越少越快但細節流失（25 步約省一半時間） |
| `--cfg_strength` | 3.0 | 物件貼圖的精確度 |
| `--num_gaussians` | 262144 | 32,768 ~ 1,048,576（32 的倍數） |
| `--no_optimize` | 關 | Windows 必開（見坑二） |

Python API 版：

```python
from idol import IdolPipeline

pipeline = IdolPipeline.from_pretrained("speridlabs/idol")
output = pipeline("photo.jpg", mode="real", seed=42, num_gaussians=1_048_576)
output.gaussian.save_ply("photo.ply")
```

## 怎麼看 .ply 結果

- **線上免安裝**：[SuperSplat 編輯器](https://superspl.at/editor)、gsplat.tech —— 拖入檔案即開
- **桌面**：Blender 裝 3DGS 插件、Polycam
- **零成本試玩**：官方 [HuggingFace Space demo](https://huggingface.co/spaces/speridlabs/idol)，上傳照片直接看效果

## 官方效能參考（50 steps，262k splats）

| GPU | 請求時間 |
|---|---|
| B300 | 3.4 s |
| RTX 5090 (32 GB) | 14.1 s |
| RTX 4090 (24 GB) | 19.1 s |
| RTX 3080 (10 GB) | 46.2 s |

對比的 LGM 只要 1.1s，但 PSNR 高分來自「模糊結果平均平方誤差低」的統計假象；Idol 在 SSIM、LPIPS、IoU、DINOv2、CLIP、銳度六項都是最佳。

## 小結

Idol 是目前最親民的開放 image-to-3D 方案之一：Apache 2.0、7.2 GB VRAM、標準 .ply 輸出，一張照片兩秒到一分鐘就能變成可檢視的 3D 物件。Windows 使用者只要記住兩件事：**torch 要從 cu126 index 裝 GPU 版**、**加 `--no_optimize` 避開 triton**，其餘照官方 README 一路直走即可。
