---
title: "abogen：開源有聲書生成器功能總覽"
date: 2026-09-09
description: "abogen 是一個強大的文字轉語音（TTS）工具，能將 EPUB、PDF、純文字、Markdown 或字幕檔轉換為高品質音訊並自動產生同步字幕。本文整理其核心功能、技術架構與安裝方式。"
tags: [audiobook, text-to-speech, kokoro, open-source, python]
---

# abogen：開源有聲書生成器功能總覽

![abogen](/assets/images/abogen/main.png)

[![Star History Chart](/assets/images/abogen/star_history.svg)](https://star-history.dera.page/#denizsafak/abogen&Date)

## 專案概覽

**abogen**（audiobook generator）是一個強大的文字轉語音轉換工具，能快速將 ePub、PDF、純文字、Markdown 或字幕檔案轉換為高品質音訊，並自動產生同步字幕。它使用 [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) 作為 TTS 引擎，適用於有聲書製作、Instagram / YouTube / TikTok 配音等任何需要自然語音的場景。

| 項目 | 資訊 |
|------|------|
| **倉庫** | [denizsafak/abogen](https://github.com/denizsafak/abogen) |
| **Stars** | ⭐ 5,926 |
| **Forks** | 452 |
| **授權條款** | MIT License |
| **主要語言** | Python |
| **支援平台** | Windows / Linux / macOS |
| **TTS 引擎** | Kokoro-82M (Apache-2.0) |
| **最新版本** | v1.3.1 (2026-02) |
| **PyPI** | [abogen](https://pypi.org/project/abogen/) |
| **建立日期** | 2025-04 |

> 名稱「abogen」是 "audiobook generator" 的縮寫。作者曾收到社群回饋指出 "abo" 前綴在澳洲和新西蘭可能被理解為種族侮辱，已公開說明無此意圖。

## 核心功能

### 1. 多格式輸入支援

Abogen 接受多種檔案格式的輸入：

| 格式 | 說明 |
|------|------|
| **ePub** | 電子書格式，自動解析章節結構 |
| **PDF** | 可選擇特定章節或頁碼範圍 |
| **.TXT** | 純文字檔 |
| **.MD** | Markdown 檔案（含章節標記） |
| **.SRT / .ASS / .VTT** | 字幕檔案，保留原始時間軸 |

### 2. 同步字幕生成

Abogen 最大的特色之一是自動產生與音訊完全同步的字幕：

- **Line** — 每行一個字幕
- **Sentence** — 每個句子一個字幕
- **Sentence + Comma** — 句子加逗號分段
- **Sentence + Highlighting** — 句子加即時高亮效果
- **1 word / 2 words / 3 words** — 精確到 N 個字（僅英文）

> 注意：逐字級字幕模式僅支援英文，因為 Kokoro 目前只為英文提供時間戳記 token。非英文語言使用時長推算的 fallback 機制。

### 3. 多音訊輸出格式

| 格式 | 用途 |
|------|------|
| **.WAV** | 無損音質 |
| **.FLAC** | 無損壓縮 |
| **.MP3** | 通用有損壓縮 |
| **.OPUS** | 最佳壓縮比 |
| **M4B** | 含章節資訊，適合有聲書播放器 |

### 4. 章節管理（Chapter Markers）

處理 ePub、PDF 或 Markdown 檔案時，Abogen 自動插入章節標記：

```text
<<CHAPTER_MARKER:Chapter Title>>
```

這些標記讓你可以：
- 將文字拆分為各章節獨立音訊檔
- 出錯時只需重新處理特定章節
- 手動在純文字檔中加入相同標記

### 5. Metadata 標籤（M4B）

支援為 M4B 檔案嵌入有聲書 metadata：

```text
<<METADATA_TITLE:Title>>
<<METADATA_ARTIST:Author>>
<<METADATA_ALBUM:Album Title>>
<<METADATA_YEAR:Year>>
<<METADATA_COMPOSER:Narrator>>
<<METADATA_COVER_PATH:path/to/cover.jpg>>
```

處理 ePub/PDF 時會自動提取封面圖片並填入 `METADATA_COVER_PATH`。

### 6. Voice Mixer（語音混合器）

![Voice Mixer](/assets/images/abogen/voice_mixer.png)

可以將多個語音模型按不同權重混合，創造出獨特的自訂語音，並儲存為 profile 供日後使用。

### 7. Queue Mode（批次處理）

![Queue Mode](/assets/images/abogen/queue.png)

支援多檔案排隊處理：
- 每個檔案保留加入時設定的參數
- 可選擇「以目前設定覆蓋所有項目」
- 自動依序處理，無需手動干預

### 8. 時間戳記文字檔

Abogen 能自動偵測含 `HH:MM:SS` 格式時間戳記的文字檔，並依此控制音訊播放時間。適合需要精確控制每段說話時機的腳本或轉錄稿。

### 9. LLM 輔助文字正規化（Web UI）

Web UI 可連接 OpenAI 相容的 LLM 端點（如 Ollama），讓模型處理棘手的撇號和縮寫，使語音輸出更自然。設定路徑：**Settings → LLM**。

### 10. Audiobookshelf 整合（Web UI）

完成轉換後可直接推送至 [Audiobookshelf](https://www.audiobookshelf.org/)：
- 設定 Base URL、Library ID、目標資料夾、API Token
- 支援自動上傳或手動觸發
- 包含 Nginx Proxy Manager 反向代理完整設定指南

## 雙介面架構

Abogen 提供兩種使用介面：

| 指令 | 介面 | 特色 |
|------|------|------|
| `abogen` | PyQt6 桌面 GUI | 穩定核心功能 |
| `abogen-web` | Flask Web UI | 核心 + **Supertonic TTS**、**LLM 正規化**、**Audiobookshelf 整合** |

> Web UI 為活躍開發中，包含較新的功能。作者感謝貢獻者 @jeremiahsb 提交了超過 55,000 行程式碼實現整個 Web UI。

![Web UI](/assets/images/abogen/webui.png)

## 技術架構

```
┌─────────────────────────────────────────────┐
│              Abogen Application             │
├──────────────────┬──────────────────────────┤
│   PyQt6 Desktop  │     Flask Web UI         │
│   (abogen)       │     (abogen-web)         │
├──────────────────┴──────────────────────────┤
│           Core Processing Engine            │
│  ┌─────────┐ ┌─────────┐ ┌──────────────┐ │
│  │ File     │ │ Chapter │ │ Subtitle     │ │
│  │ Parsers  │ │ Manager │ │ Generator    │ │
│  │(ePub/PDF/│ │(markers)│ │(SRT/ASS/VTT) │ │
│  │ TXT/MD)  │ │         │ │              │ │
│  └─────────┘ └─────────┘ └──────────────┘ │
├─────────────────────────────────────────────┤
│            Kokoro-82M TTS Engine            │
│     (PyTorch / CUDA / ROCm / MPS)          │
├─────────────────────────────────────────────┤
│  spaCy (sentence segmentation)             │
│  espeak-ng (phoneme fallback)              │
│  FFmpeg (audio encoding / time-stretch)    │
└─────────────────────────────────────────────┘
```

### 支援的 GPU 加速

| 平台 | GPU 支援 |
|------|----------|
| Windows | NVIDIA CUDA (12.6 / 12.8 / 13.0) |
| Linux | NVIDIA CUDA + AMD ROCm 6.4 |
| macOS | Apple Silicon MPS (需 Kokoro dev 版) |
| CPU-only | 全平台支援（速度較慢） |

## 支援的語言

| 代碼 | 語言 | 備註 |
|------|------|------|
| `a` | 🇺🇸 American English | 預設 |
| `b` | 🇬🇧 British English | |
| `e` | 🇪🇸 Spanish | |
| `f` | 🇫🇷 French (fr-fr) | |
| `h` | 🇮🇳 Hindi | |
| `i` | 🇮🇹 Italian | |
| `j` | 🇯🇵 Japanese | 需 `pip install misaki[ja]` |
| `p` | 🇧🇷 Brazilian Portuguese | |
| `z` | 🇨🇳 Mandarin Chinese | 需 `pip install misaki[zh]` |

語音代碼規則：第一字母 = 語言，第二字母 = `m`(男) / `f`(女)。完整列表見 Kokoro [VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)。

## 安裝方式

### Windows

1. 先安裝 [espeak-ng](https://github.com/espeak-ng/espeak-ng/releases/latest)（下載 .msi）
2. **方式 A**：下載 repo → 雙擊 `WINDOWS_INSTALL.bat`（自動安裝 Python + CUDA）
3. **方式 B**：使用 uv

```bash
# NVIDIA GPU (CUDA 12.8) — 推薦
uv tool install --python 3.12 abogen[cuda] \
  --extra-index-url https://download.pytorch.org/whl/cu128 \
  --index-strategy unsafe-best-match

# AMD GPU 或無 GPU
uv tool install --python 3.12 abogen
```

### macOS

```bash
brew install espeak-ng

# Apple Silicon (M1/M2/M3)
uv tool install --python 3.13 abogen \
  --with "kokoro @ git+https://github.com/hexgrad/kokoro.git,numpy<2"

# Intel Mac
uv tool install --python 3.12 abogen \
  --with "kokoro @ git+https://github.com/hexgrad/kokoro.git,numpy<2"
```

### Linux

```bash
sudo apt install espeak-ng   # Ubuntu/Debian

# NVIDIA GPU 或 CPU
uv tool install --python 3.12 abogen

# AMD GPU (ROCm 6.4)
uv tool install --python 3.12 abogen[rocm] \
  --extra-index-url https://download.pytorch.org/whl/nightly/rocm6.4 \
  --index-strategy unsafe-best-match
```

### Docker（Web UI）

```bash
docker build -t abogen .
mkdir -p ~/abogen-data/uploads ~/abogen-data/outputs
docker run --rm \
  -p 8808:8808 \
  -v ~/abogen-data:/data \
  --name abogen \
  abogen
```

或直接用 GPU 版 Compose：

```bash
docker compose up -d --build
```

## 實際效能

![Abogen in action](/assets/images/abogen/in_action.gif)

> 在 RTX 2060 Mobile 筆記型電腦上，約 3,000 字元的文字在 **11 秒**內處理完成，產出 **3 分 28 秒**的音訊。效能因硬體而異。

## 與其他專案比較

| 專案 | 特色 | 介面 |
|------|------|------|
| **abogen** | Kokoro TTS + 同步字幕 + 章節管理 + Web UI | GUI + Web |
| [audiblez](https://github.com/santinic/audiblez) | ePub → 有聲書 | CLI + GUI |
| [autiobooks](https://github.com/plusuncold/autiobooks) | 自動 ePub 轉換 | CLI |
| [pdf-narrator](https://github.com/mateogon/pdf-narrator) | PDF/ePub → 有聲書 | Web |
| [epub_to_audiobook](https://github.com/p0n1/epub_to_audiobook) | 針對 Audiobookshelf 優化 | CLI |
| [ebook2audiobook](https://github.com/DrewThomasson/ebook2audiobook) | AI voice cloning + 章節 metadata | Web |

Abogen 的獨特優勢在於：
- **同步字幕**（非僅音訊）
- **Voice Mixer** 自訂語音混合
- **雙介面**（桌面 + Web）
- **Kokoro-82M** 高品質 TTS（Apache-2.0，可商用）

## Roadmap

| 功能 | 狀態 |
|------|------|
| OCR 掃描 PDF (docling/tesseract) | 🚧 規劃中 |
| M4A 章節 metadata | ✅ 已完成 |
| GUI 多語言介面 | 🚧 規劃中 |
| Voice formula（語音混合） | ✅ 已完成 |
| Kokoro-ONNX 支援 | 🚧 評估中 |
| Dark mode | ✅ 已完成 |

## 主要貢獻者

| 貢獻者 | Commits | 主要貢獻 |
|--------|---------|----------|
| denizsafak | 355 | 核心開發 |
| k0sm0naft | 199 | 重大功能貢獻 |
| jborza | 33 | Voice Mixer、Queue Mode、章節支援 |
| jeremiahsb | — | Web UI（>55,000 行） |

## 參考連結

- **GitHub**: https://github.com/denizsafak/abogen
- **PyPI**: https://pypi.org/project/abogen/
- **Kokoro-82M (TTS)**: https://huggingface.co/hexgrad/Kokoro-82M
- **espeak-ng**: https://github.com/espeak-ng/espeak-ng
- **Demo 指南**: https://github.com/denizsafak/abogen/tree/main/demo
- **Star History**: https://star-history.dera.page/#denizsafak/abogen&Date
