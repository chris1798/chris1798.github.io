---
title: "LibreChat：開源自託 AI 聊天平台功能總覽"
date: 2026-09-09
description: "LibreChat 是一個開源、自託管的 AI 聊天平台，整合 OpenAI、Anthropic、Google、AWS 等主流 AI 供應商，支援 Agents、MCP、Code Interpreter、Artifacts、Web Search 與多用戶管理。"
tags: [ai-chat, self-hosted, open-source, chatgpt-clone, agents]
---

# LibreChat：開源自託 AI 聊天平台功能總覽

![LibreChat](/assets/images/librechat/logo.svg)

[![Star History Chart](/assets/images/librechat/star_history.png)](https://www.star-history.com/?type=date&repos=danny-avila%2FLibreChat)

## 專案概覽

**LibreChat** 是一個開源、自託管的 AI 聊天平台，在單一隱私導向的介面中整合所有主流 AI 供應商。除了基本對話，還提供 AI Agents、MCP 支援、Artifacts、Code Interpreter、自訂 Actions、對話搜尋和企業級多用戶認證。

| 項目 | 資訊 |
|------|------|
| **倉庫** | [danny-avila/LibreChat](https://github.com/danny-avila/LibreChat) |
| **Stars** | ⭐ 42,926 |
| **Forks** | 8,899 |
| **授權條款** | MIT License |
| **主要語言** | TypeScript (Next.js + React) |
| **支援平台** | Web（自託管 Docker / Railway / Zeabur / Sealos） |
| **最新版本** | v0.8.8-rc2 (2026-09) |
| **官網** | [librechat.ai](https://librechat.ai) |
| **文件** | [docs.librechat.ai](https://docs.librechat.ai) |
| **建立日期** | 2023-02 |

> LibreChat 是 GitHub 上成長最快的開源 AI 專案之一，曾入選 Runa Capital ROSS Index Q1 2024「最快成長開源新創」。

## 核心功能

### 1. 多 AI 模型整合

LibreChat 支援的 AI 供應商：

| 類別 | 供應商 |
|------|--------|
| **OpenAI 系** | OpenAI、Azure OpenAI、OpenAI Responses API（含 Azure） |
| **Anthropic** | Claude (Fable 5.1, Opus 5, Sonnet 5) |
| **Google** | Gemini 3.8/3.7/3.6 Flash、Gemini 3.5 Flash-Lite、Vertex AI |
| **AWS** | AWS Bedrock |
| **其他商業** | DeepSeek、Mistral、Groq、Cohere、Perplexity、together.ai |
| **本地/開源** | Ollama、AMD Lemonade、Apple MLX、koboldcpp、Qwen |
| **路由/代理** | OpenRouter、Helicone、ShuttleAI |
| **自訂端點** | 任何 OpenAI 相容 API（無需 proxy） |

### 2. AI Agents & Tools

LibreChat 的 Agent 系統是其最強大的功能之一：

- **無代碼自訂助理**：建立專用的 AI 助手
- **Agent Marketplace**：發現和部署社群建立的 agents
- **協作分享**：與特定用戶或群組分享 agents
- **MCP 支援**：透過 [Model Context Protocol](https://modelcontextprotocol.io/clients#librechat) 整合外部工具
- **Skills**：建立可重複使用的 `SKILL.md` 指令包，支援手動、自動或常駐 agent 工作流
- **Agent Plugins**：實驗性捆綁部署 Skills 和 MCP 伺服器為啟動載入套件
- **Subagents**：將聚焦工作委派給隔離的子 agent 執行，各自擁有獨立上下文窗口
- **Human-in-the-loop**：串流最多四個相關問題、暫停等待輸入或工具批准、持久恢復
- **Background tools**：Code Interpreter、MCP、Plugin、Action 工具可在 Agent 持續工作時背景執行
- **Scheduled Chats（實驗性）**：以 cron 排程執行保存的 Agents，支援多日週期

### 3. Code Interpreter API

安全沙箱化程式碼執行：

| 特性 | 說明 |
|------|------|
| **支援語言** | Python、Node.js (JS/TS)、Go、C/C++、Java、PHP、Rust、Fortran |
| **檔案處理** | 上傳、處理和直接下載檔案 |
| **安全性** | 完全隔離的安全執行環境 |
| **沙箱輸出** | Sandbox 圖片返回為可預覽的 artifacts |
| **狀態化會話** | 實驗性支援 scoped managed / attached / personal 環境 |
| **基礎** | 由 [ClickHouse/code-interpreter](https://github.com/ClickHouse/code-interpreter) 驅動 |

### 4. Web Search

- 搜尋網路並擷取相關資訊增強 AI 上下文
- 結合搜尋提供者、內容爬蟲和結果重排序器
- **Keenable**：免金鑰搜尋和頁面抓取
- **SearXNG / Tavily**：更豐富的控管選項
- **Jina Reranking**：可自訂 Jina API URL 進行重排序
- 所有 web-tool egress 使用更強的 SSRF 保護

### 5. Code Artifacts（生成式 UI）

- 在聊天中直接創建 React、HTML 和 Mermaid 內容
- 全螢幕預覽 artifacts
- Mermaid 圖表可導出為 SVG 或 PNG
- PowerPoint 模板、shell scripts 和原始 Office 下載擴展檔案工作流

### 6. 圖片生成與編輯

| 引擎 | 模式 |
|------|------|
| **GPT-Image-1** | Text-to-image + Image-to-image（推薦） |
| **DALL-E (3/2)** | Text-to-image（legacy） |
| **Stable Diffusion** | 本機 text-to-image |
| **Flux** | Text-to-image |
| **MCP Server** | 任何 MCP 圖片生成服務 |

### 7. Presets & Context Management

- 建立、保存和分享自訂 Presets
- 對話中切換 AI Endpoints 和 Presets
- 編輯、重新提交和繼續訊息，支援對話分支（branching）
- Fork Messages & Conversations 進階上下文控管
- 與特定用戶或群組分享 prompts

### 8. 多模態與檔案互動

- **圖片分析**：Claude 3、GPT-4.5、GPT-4o、o1、Llama-Vision、Gemini
- **Chat with Files**：支援 Custom Endpoints、OpenAI、Azure、Anthropic、AWS Bedrock、Google
- **可編輯長貼文**：長貼文字變成可編輯附件，可移回輸入框
- **Attachment-only turns** 和可靠的 Upload as Text 下載

### 9. Resumable Streams（可恢復串流）

- AI 回應在連線中斷時自動重新連接和恢復
- 多分頁與多裝置同步：同一對話可在多個分頁開啟或切換裝置繼續
- 從單伺服器到水平擴展部署（Redis）皆可用

### 10. Speech & Audio

- Speech-to-Text 和 Text-to-Speech 免手操作聊天
- 自動發送和播放音訊
- 支援 OpenAI、Azure OpenAI、Elevenlabs

### 11. 多語言 UI

支援 25+ 種介面語言：英文、簡體中文、繁體中文、阿拉伯文、德文、西班牙文、法文、義大利文、波蘭文、葡萄牙文（PT/BR）、俄文、日文、瑞典文、韓文、越南文、土耳其文、荷蘭文、希伯來文、加泰隆尼亞文、捷克文、丹麥文、愛沙尼亞文、波斯文、芬蘭文、匈牙利文、亞美尼亞文、印尼文、喬治亞文、拉脫維亞文、泰文、維吾爾文

### 12. Reasoning UI

- DeepSeek-R1 等 Chain-of-Thought/Reasoning AI 模型的動態推理 UI
- GPT-5.6 含 Responses reasoning controls

### 13. 多用戶與安全認證

- **OAuth2、LDAP、Email Login** 支援
- SAML identity binding、live-session OpenID token refresh
- 內建 Moderation 和 Token spend tools
- 預設 HTTP security headers、opt-in nonce CSP
- Per-user Code Interpreter JWTs
- Source-aware content filters（稽核或阻擋 model-bound data）

### 14. Admin Panel

- 瀏覽器 UI 管理用戶、群組、角色和設定覆寫
- 即時編輯設定和 per-role/group 權限，無需重新部署
- Tenant Insights、delegated configuration、encrypted secrets
- 隨 Docker Compose stacks 一鍵部署

### 15. 匯入與匯出

| 方向 | 支援 |
|------|------|
| **匯入** | LibreChat、ChatGPT、Chatbot UI |
| **匯出** | Screenshots、Markdown、Text、JSON |
| **分享** | 穩定共享連結（個人副本）、全螢幕預覽 |

## 技術架構

```
┌──────────────────────────────────────────────────────┐
│                  LibreChat Platform                   │
├──────────────────────────────────────────────────────┤
│              Next.js + React (TypeScript)            │
│  ┌─────────┬──────────┬──────────┬──────────────┐   │
│  │ Chat UI  │ Agent    │ Admin    │ Settings /   │   │
│  │(Artifacts│ Builder  │ Panel    │ Presets      │   │
│  │/Search)  │(Skills/  │(Users/   │(Models/     │   │
│  │          │ MCP/Sub) │ Roles)   │ Endpoints)   │   │
│  └─────────┴──────────┴──────────┴──────────────┘   │
├──────────────────────────────────────────────────────┤
│              Backend API (Node.js)                   │
│  ┌──────────┬──────────┬──────────┬─────────────┐   │
│  │ AI       │ Code     │ Web      │ Image       │   │
│  │ Endpoints│ Interpreter│ Search │ Generation  │   │
│  │(Multi-   │(ClickHouse)│(SearXNG/│(GPT-Image/ │   │
│  │ Provider)│          │ Tavily/  │ SD/Flux/MCP)│   │
│  │          │          │ Jina)    │             │   │
│  └──────────┴──────────┴──────────┴─────────────┘   │
│  ┌──────────┬──────────┬──────────┬─────────────┐   │
│  │ Auth     │ MCP      │ Speech   │ RAG API     │   │
│  │(OAuth2/  │ Server   │(STT/TTS) │(Vector DB)  │   │
│  │ LDAP/SAML)│ Registry │          │             │   │
│  └──────────┴──────────┴──────────┴─────────────┘   │
├──────────────────────────────────────────────────────┤
│         Infrastructure                               │
│   MongoDB / PostgreSQL / DocumentDB                 │
│   Redis (streams, caching, horizontal scaling)      │
│   S3 + CloudFront (media, CDN, signed URLs)         │
│   Docker Compose / Railway / Zeabur / Sealos        │
└──────────────────────────────────────────────────────┘
```

## 部署方式

| 方式 | 說明 |
|------|------|
| **Docker Compose** | 一鍵部署（含 Admin Panel） |
| **Railway** | [Deploy on Railway](https://railway.com/deploy/librechat-official) |
| **Zeabur** | [Deploy on Zeabur](https://zeabur.com/templates/0X2ZY8) |
| **Sealos** | Cloud Sealos template |
| **本地** | 完全本機運行或雲端部署 |
| **S3 + CloudFront** | 穩定媒體連結、邊緣交付、簽名 cookie |

### 快速啟動（Docker）

```bash
git clone https://github.com/danny-avila/LibreChat.git
cd LibreChat
cp .env.example .env
# 編輯 .env 填入 API keys
docker compose up -d
```

## v0.8.8-rc2 重要更新（2026-09）

- **Agent run control**：中斷 Agent、以檔案和引用摘要引導執行、持久排隊後續任務
- **Human-in-the-loop Agents**：串流相關問題、暫停等待輸入/工具批准
- **Unified Agent Builder**：一個 Tools marketplace 配置 Skills、MCP、Code Interpreter、orchestration
- **Durable Agent automation**：Authenticated Agent Events、bound child actors、per-actor mailboxes
- **Background tools**：工具可在 Agent 持續工作時背景執行
- **Scheduled Chats（實驗性）**：Cron 排程執行 Agents
- **Web search**：Keenable 免金鑰搜尋、SearXNG/Tavily 更豐富控管
- **Security**：預設 HTTP headers、nonce CSP、per-user Code Interpreter JWTs
- **Models**：GPT-5.6、Claude Fable 5.1/Opus 5/Sonnet 5、Gemini 3.8/3.7/3.6 Flash

## 主要貢獻者

| 貢獻者 | Commits |
|--------|---------|
| danny-avila | 3,577 |
| berry-13 | 312 |
| wtlyu | 159 |
| dustinhealy | 142 |
| fuegovic | 116 |

![Contributors](/assets/images/librechat/contributors.png)

## 與其他 AI 聊天平台比較

| 特性 | **LibreChat** | ChatGPT | Open WebUI |
|------|---------------|---------|------------|
| 自託管 | ✅ | ❌ | ✅ |
| 多供應商整合 | ✅ 20+ | ❌ (僅 OpenAI) | ✅ |
| AI Agents + MCP | ✅ | 部分 | 有限 |
| Code Interpreter | ✅ (8 語言) | ✅ | ❌ |
| Artifacts | ✅ | ✅ | ❌ |
| Web Search | ✅ | ✅ | 有限 |
| 多用戶認證 | OAuth2/LDAP/SAML | ❌ | 基本 |
| Admin Panel | ✅ | ❌ | 有限 |
| Resumable Streams | ✅ | N/A | ❌ |
| PPTX/Office 導出 | ✅ (Artifacts) | ❌ | ❌ |
| 多語言 UI | 25+ | 30+ | 10+ |
| 授權 | MIT | Proprietary | BSD-3 |

## 參考連結

- **GitHub**: https://github.com/danny-avila/LibreChat
- **官網**: https://librechat.ai
- **文件**: https://docs.librechat.ai
- **Blog**: https://librechat.ai/blog
- **RAG API**: https://github.com/danny-avila/rag_api
- **Changelog**: https://www.librechat.ai/changelog
- **Discord**: https://discord.librechat.ai
- **YouTube**: https://www.youtube.com/@LibreChat
- **Star History**: https://www.star-history.com/?type=date&repos=danny-avila%2FLibreChat
