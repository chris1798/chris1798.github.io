---
title: "AstrBot：開源 AI Agent 聊天機器人平台功能總覽"
date: 2026-09-09
description: "AstrBot 是一個開源的一站式 AI Agent 聊天機器人平台，整合 QQ、Telegram、Discord、Slack 等主流即時通訊平台，支援 LLM 對話、MCP、Skills、知識庫、Agent Sandbox 與 1000+ 插件。"
tags: [ai-agent, chatbot, im-platform, python, plugins]
---

# AstrBot：開源 AI Agent 聊天機器人平台功能總覽

![AstrBot](/assets/images/astrbot/logo.png)

[![Star History Chart](/assets/images/astrbot/star_history.svg)](https://star-history.com/#astrbotdevs/astrbot&Date)

## 專案概覽

**AstrBot** 是一個開源的一站式 Agent 聊天機器人平台，整合主流即時通訊應用（IM），為個人、開發者和團隊提供可靠且可擴展的對話式 AI 基礎設施。無論你是在打造個人 AI 伴侶、智慧客服、自動化助手或企業知識庫，AstrBot 都能讓你在 IM 平台工作流中快速構建生產級 AI 應用。

| 項目 | 資訊 |
|------|------|
| **倉庫** | [AstrBotDevs/AstrBot](https://github.com/AstrBotDevs/AstrBot) |
| **Stars** | ⭐ 40,227 |
| **Forks** | 2,894 |
| **授權條款** | AGPL-3.0 |
| **主要語言** | Python (3.12+) |
| **支援平台** | QQ、Telegram、Discord、Slack、飛書、釘釘等 19+ IM |
| **最新版本** | v4.28.0 (2026-09) |
| **官網** | [astrbot.app](https://astrbot.app) |
| **文件** | [docs.astrbot.app](https://docs.astrbot.app) |
| **插件市場** | 1,000+ 插件 |
| **建立日期** | 2022-12 |

> 「陪伴與能力不應互相衝突。我們希望打造的是一個能理解情緒、提供真正陪伴，並可靠完成任務的機器人。」

## 核心功能

### 1. AI LLM 對話與多模態

- 支援 OpenAI、Anthropic、Google Gemini、Moonshot、智譜、DeepSeek、Ollama（自託管）、LM Studio（自託管）等
- **多模態**：圖片理解、語音轉文字（Whisper、SenseVoice、小米 MiMo Omni）
- **TTS 語音合成**：OpenAI TTS、Gemini TTS、GPT-Sovits、FishAudio、Edge TTS、Azure TTS、Minimax TTS、火山引擎 TTS 等
- **自動上下文壓縮**：長對話自動管理 token 使用
- **Persona 設定**：自訂 AI 人格與行為模式

### 2. Agent & MCP 支援

- **Agent Sandbox**：隔離、安全的程式碼執行環境，支援 shell 呼叫和會話級資源重用
- **MCP（Model Context Protocol）**：整合外部工具與服務
- **Skills**：可重複使用的技能包
- **知識庫（RAG）**：企業知識庫搜尋與引用
- **Agent 平台整合**：Dify、阿里雲百鍊、Coze 等

### 3. 多平台 IM 支援

| 平台 | 維護者 |
|------|--------|
| QQ | 官方 |
| OneBot v11 協議實現 | 官方 |
| Telegram | 官方 |
| 企業微信 & 企微 AI Bot | 官方 |
| 微信公眾號 | 官方 |
| 飛書 (Lark) | 官方 |
| 釘釘 | 官方 |
| Slack | 官方 |
| Discord | 官方 |
| LINE | 官方 |
| Satori | 官方 |
| KOOK（原開黑） | 官方 |
| Misskey | 官方 |
| Mattermost | 官方 |
| WhatsApp | 即將推出 |
| Matrix | 社群 |
| Rocket.Chat | 社群 |
| VoceChat | 社群 |

### 4. 插件系統（1000+ 插件）

- **AstrBot Cloud**：全新插件市場系統，開發者可上傳、管理和瀏覽插件
- WebUI 內的插件市場數據從 AstrBot Cloud 同步
- 一鍵安裝插件
- Per-plugin log level controls
- 插件 API 供開發者擴展功能

### 5. WebUI & ChatUI

- **WebUI**：瀏覽器管理介面，配置模型、平台、插件
- **ChatUI**：內建網頁聊天介面，含 Agent Sandbox 和 web search
- **Desktop App**：桌面版（[AstrBot-desktop](https://github.com/AstrBotDevs/AstrBot-desktop)），快速本地安裝
- **Launcher**：多實例隔離管理工具

### 6. 國際化（i18n）

支援簡體中文、繁體中文、英文、日文、法文、西班牙文、俄文等多語言介面。

## 技術架構

```
┌──────────────────────────────────────────────────────┐
│                   AstrBot Platform                    │
├──────────────────────────────────────────────────────┤
│              WebUI / ChatUI (Web)                     │
│  ┌─────────┬──────────┬──────────┬──────────────┐   │
│  │ Dashboard│ Agent    │ Plugin   │ Settings /   │   │
│  │(Logs/    │ Builder  │ Market   │ i18n         │   │
│  │ Config)  │(Skills/  │(1000+)   │              │   │
│  │          │ MCP)     │          │              │   │
│  └─────────┴──────────┴──────────┴──────────────┘   │
├──────────────────────────────────────────────────────┤
│              Core Engine (Python 3.12+)              │
│  ┌──────────┬──────────┬──────────┬─────────────┐   │
│  │ LLM      │ Agent    │ RAG /    │ TTS / STT   │   │
│  │ Manager  │ Sandbox  │ Knowledge│ Pipeline    │   │
│  │(Multi-   │(Isolated)│ Base     │(STT→LLM→TTS)│   │
│  │ Provider)│          │(Vector)  │             │   │
│  └──────────┴──────────┴──────────┴─────────────┘   │
│  ┌──────────┬──────────┬──────────┬─────────────┐   │
│  │ Plugin   │ Context  │ Persona  │ MCP         │   │
│  │ System   │ Compress │ Settings │ Integration │   │
│  │(1000+)   │          │          │             │   │
│  └──────────┴──────────┴──────────┴─────────────┘   │
├──────────────────────────────────────────────────────┤
│         IM Platform Adapters                         │
│  QQ / Telegram / Discord / Slack / 飛書 / 釘釘      │
│  LINE / KOOK / Mattermost / OneBot v11 / ...        │
└──────────────────────────────────────────────────────┘
```

## 部署方式

| 方式 | 說明 |
|------|------|
| **uv 一鍵部署** | `uv tool install astrbot --python 3.12`（推薦快速體驗） |
| **Docker / Docker Compose** | 生產級穩定部署 |
| **RainYun 雲部署** | 一鍵 24 小時線上部署，免管伺服器 |
| **Desktop App** | 桌面版，適合 ChatUI 使用 |
| **Launcher** | 多實例隔離管理 |
| **BT-Panel / 1Panel** | 面板應用市場部署 |
| **CasaOS** | NAS/家庭伺服器視覺化部署 |
| **手動部署** | 完全自訂 source-based 安裝 |

### 快速啟動（uv）

```bash
uv tool install astrbot --python 3.12
astrbot init   # 首次執行初始化環境
astrbot run
```

### Docker 部署

```bash
git clone https://github.com/AstrBotDevs/AstrBot.git
cd AstrBot
docker compose up -d
```

## v4.28.0 重要更新（2026-09）

- **AstrBot Cloud**：全新插件市場系統上線
- Per-plugin log level controls（dashboard + plugin API）
- FishAudio TTS provider 模型配置支援
- Platform log categorization + console toggle
- DashScope embedding provider（多模態模型支援）
- ChatUI workspace file browser（僅 projects）

## 主要貢獻者

| 貢獻者 | Commits |
|--------|---------|
| Soulter | 3,417 |
| Raven95676 | 211 |
| RC-CHN | 98 |
| zouyonghe | 71 |
| anka-afk | 63 |

![Contributors](/assets/images/astrbot/contributors.png)

## 與其他 AI 聊天機器人框架比較

| 特性 | **AstrBot** | Open WebUI | LibreChat |
|------|-------------|------------|-----------|
| IM 平台整合 | ✅ 19+ (QQ/Telegram/Discord...) | ❌ | ❌ |
| 插件系統 | ✅ 1000+ | 有限 | 有限 |
| Agent Sandbox | ✅ | ❌ | Code Interpreter |
| MCP 支援 | ✅ | 部分 | ✅ |
| 知識庫 (RAG) | ✅ | ✅ | ✅ (RAG API) |
| 多模態 (STT/TTS) | ✅ 10+ providers | 基本 | ✅ |
| 自託管 | ✅ | ✅ | ✅ |
| 桌面版 | ✅ | ❌ | ❌ |
| 中文生態 | ✅ 核心 | 有限 | 有限 |
| 授權 | AGPL-3.0 | BSD-3 | MIT |

## 社群

- **QQ 群**：15+ 聊天群（見[社群頁面](https://docs.astrbot.app/community.html)）
- **Discord**: https://discord.gg/hAVk6tgV36
- **Email Support**: community@astrbot.app
- **Blog**: https://blog.astrbot.app/
- **Roadmap**: https://astrbot.featurebase.app/roadmap

## 參考連結

- **GitHub**: https://github.com/AstrBotDevs/AstrBot
- **官網**: https://astrbot.app
- **文件**: https://docs.astrbot.app
- **Blog**: https://blog.astrbot.app/
- **插件市場 (AstrBot Cloud)**: https://astrbot.app/#/plugins
- **Desktop 版**: https://github.com/AstrBotDevs/AstrBot-desktop
- **Launcher**: https://github.com/Raven95676/astrbot-launcher
- **Docker Hub**: https://hub.docker.com/r/soulter/astrbot
- **Star History**: https://star-history.com/#astrbotdevs/astrbot&Date
