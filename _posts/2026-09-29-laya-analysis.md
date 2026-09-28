---
title: "Laya 功能說明:非自回歸的 System 1 決策引擎"
date: 2026-09-29
description: 整理 NandhaKishorM/laya — 多語言、非自回歸的 System 1 決策模型,一次 forward pass 在 100+ 語言上完成 typed 決策(choice/score/noul),附 Router、MCP、HTTP 伺服器、LangChain 整合、微調流程與已知限制。
tags: [nlp, decision-model, multilingual, huggingface, laya, pytorch]
---

# Laya 功能說明:非自回歸的 System 1 決策引擎

> **一句話**:Laya 是一個多語言、非自回歸的「System 1 決策引擎」。它在**一次 forward pass**(T4 GPU 約 33 ms)裡,對任何文字(郵件、ticket、JSON)回答**typed 問題**(`choice` 選項、`score` 序數評分、`noul` 是/否),支援 100+ 語言,內建 Router 自動挑選最合適的 checkpoint。

| 項目 | 內容 |
|---|---|
| 倉庫 | [NandhaKishorM/laya](https://github.com/NandhaKishorM/laya) |
| 授權 | Apache 2.0 |
| 主語言 | Python(Python ≥ 3.10) |
| Stars / Forks | 27,468 / 2,394 |
| 最新版本 | 0.3.21(PyPI `laya`) |
| 建立 | 2026-09-18 |
| 首頁 | [HuggingFace Model](https://huggingface.co/convaiinnovations/laya) / [線上 Demo](https://huggingface.co/spaces/convaiinnovations/laya-demo) |
| 文件 | [nandhakishorm.github.io/laya](https://nandhakishorm.github.io/laya/) |

## 一、核心概念

Laya 不走「文字生成 → 解析」那條路,而是把「決策」建模成一次前向分類:

- **不生成文字**,所以沒有 hallucination、沒有 parsing 問題。
- **一次 forward pass 回答所有問題**(一個 state 上同時問 10 個問題,多題共享前向)。
- 三種 **decision primitive**(決策原語):

| 原語 | 輸出 | 典型用途 |
|---|---|---|
| `choice` | 最可能標籤 + 各選項概率 + 置信度 | 部門分派、意圖分類 |
| `score` | 序數尺度上的期望值 + 分佈 | 急迫度、情緒強度 |
| `noul` | 校準後的 P(true) ∈ [0,1] | 釣魚偵測、垃圾郵件、churn risk |

- **RLCD 訓練**:以 strictly proper scoring rule 做強化學習,讓概率統計上有意義,可用於閾值決策。

## 二、三個 Checkpoint + Router

Laya 發行三個檢查點,`Router` 依文字語種在**前向之前**用 <0.5 ms 挑選最合適的:

| Checkpoint | Encoder | 參數 | Context | 適用 |
|---|---|---|---|---|
| `laya` | ModernBERT-large | 421M | 512 | 英文 |
| `laya-multilingual` | mmBERT-base | 322M | 1024(最高 8,192) | 100+ 語言,速度 2x |
| `laya-typed-decisions` | ModernBERT-large | 421M | 1024 | typed-decisions 工作流(微調後) |

**Router 為什麼重要**:英文 checkpoint 對非拉丁文會**在 0.952 置信度下輸出 0.000 準確率**(例如 Khmer),模型自己不知道錯、置信度也給不出預警。Router 在前向之前先做 script + function-word 偵測,把非英文送到 `laya-multilingual`。

## 三、快速上手

```python
from laya import Router
router = Router()  # 首次下載 checkpoint;Router(preload=True) 全部預載

state = "Hi, we were billed twice for March. Please refund the duplicate today or we will cancel our plan."
questions = {
    "department": {"type": "choice", "instructions": "Which department should handle this?",
                   "criteria": {"billing": "invoices, payments, refunds",
                                "technical": "bugs, outages, system errors",
                                "other": "everything else"}},
    "urgency": {"type": "score", "instructions": "How urgent is this?",
                "criteria": ["not urgent", "soon", "blocking"]},
    "churn_risk": {"type": "noul", "instructions": "Does the user threaten to cancel or leave?"},
}

result = router.predict(state, questions)
print(result["answers"]["department"]["choice"])  # billing
print(result["answers"]["churn_risk"]["noul"])    # P(yes)
print(result["routing"]["model"])                 # english
```

同一個 API 換成 Hindi 或西班牙文也照樣跑,Router 會自動路由到 `multilingual`。

### 安裝

```bash
python -m pip install laya
# 可選 extras:
#   laya[serve]       HTTP 伺服器(FastAPI)
#   laya[mcp]         MCP stdio server
#   laya[langchain]   LangChain / LangGraph
#   laya[llamaindex]  LlamaIndex selectors
#   laya[crewai]      CrewAI routing
#   laya[onnx]        ONNX Runtime
#   laya[fast]        TileLang GPU fast path
#   laya[structured]  pydantic schema 決策
```

TypeScript / Node.js / 瀏覽器版本在 `laya-ts/` 子目錄,`npm install laya-ts`。

## 四、完整功能面

### 4.1 決策與批處理

- **`predict(state, questions)`**:單次前向、一次回多題。
- **`predict_batch(states, questions)`**:同構問題共享前向,GPU 上可達 ~10x 加速;`sort_by_length=True` 用長度排序減少 padding。
- **`predict_long(state, questions)`**:對超長文件做滑窗掃描,`noul` 取最強窗、`choice/score` 取最自信窗,回傳 `answer["window"]` 告訴你答案來自哪個 span。
- **`decide(state, schema)` / `decide_batch`**:接受 JSON schema 或 pydantic model,回傳 schema-shaped 值。

### 4.2 內建工作流 preset

```python
agent.predict({"request": ...}, laya.router_questions())        # 模型路由器
agent.predict({"prompt": ...}, laya.guard_questions())          # prompt guardrail
agent.predict({"post": ...}, laya.moderation_questions())       # 內容安全
agent.predict({"message": ...}, laya.triage_questions())        # ticket triage
```

### 4.3 自架 HTTP 伺服器(Jev 相容)

`laya[serve]` 提供 `POST /v1/systemone` wire protocol,與 TypeSafe Jev API schema 相容,既有 Jev client(例如 Haskell `hs-jev`)改 `baseUrl` 即可。

- 環境變數:`LAYA_HOST` / `LAYA_PORT` / `LAYA_DEVICE` / `LAYA_PRELOAD` / `LAYA_MODELS` / `LAYA_THREADS` / `LAYA_AUTO_TASK` / `LAYA_MAX_LOADED` / `LAYA_API_KEY`(Bearer)。
- 支援 Nix/NixOS flake:`nix run .#laya-serve`,含 NixOS module 提供 hardened systemd unit。

### 4.4 MCP server

`laya[mcp]` 提供 stdio MCP 工具:`laya_predict` / `laya_predict_batch` / `laya_route` / `laya_route_batch` / `laya_decide` / `laya_shortlist` / `laya_preset` / `laya_status`,可直接接 Claude Desktop / Cursor / OpenClaw。

### 4.5 LangChain / LangGraph

- `LayaRouter`:LangGraph conditional edge 的 sub-35 ms 路由器,支援 `confidence_threshold` + fallback。
- `LayaGuardrail`:內嵌 prompt guardrail(`action="raise"` 直接丟 `LayaGuardrailError`)。
- `LayaDecision`:JSON schema in → schema-shaped values out。
- `batch()` / `abatch()`:整批共享前向,MPS 上 ~2.2x 加速。

### 4.6 進階能力

- **Prediction hooks**:純 callback,可在 forward 前改寫 state(`ctx.skip(...)` 直接回 cached answer)、forward 後改寫結果,用於稽核、PII 掩碼、路由覆蓋。
- **`min_confidence` opt-in**:低於門檻的答題標記 `low_confidence: True`,`decide` 直接回 `None`。
- **GPU fast path(TileLang)**:`laya[fast]` 用 fused kernel + CUDA graph,GPU 上單一問題不再付 ~200 次 kernel launch 的開銷。
- **`predict_shortlist`**:對高卡數 choice,先用 encoder 的 embedding 把 top-k 抽出來,一次前向只問 top-k。
- **`laya.evals`**:純 Python + numpy 的評估 harness,可直接丟進 CI 做閘門。

### 4.7 CLI

```bash
laya "I was charged twice"                          # routing only,不下載模型
laya "..." --predict                                # 完整答題
laya "..." --preset triage                          # 內建 preset
laya --batch tickets.txt --predict --json           # 批量 JSONL
laya "..." --questions intents.json                 # 自訂問題
laya                                                # 互動模式
```

### 4.8 本地 Web GUI + JSON API

`examples/server.py` 是 self-contained FastAPI app:雙欄 playground(表單 / JSON 輸入、Ctrl+Enter 執行、顯示完整分佈與校準置信度)+ `/predict`、`/predict/batch` REST API,不用寫程式就能試。

## 五、效能與基準

T4 GPU 實測:

| 每 call 題數 | `laya` | `laya-multilingual` |
|---|---|---|
| 1 | 39.5 ms | **32.8 ms** |
| 5 | 84.5 ms | **40.1 ms** |
| 10 | 158.6 ms (15.9 ms/q) | **72.3 ms (7.2 ms/q)** |
| 50 | 771 ms | **337 ms (6.8 ms/q)** |

- 單題 **約 6-7x 快於 TypeSafe Jev**(Jev 236–276 ms p50)。
- 51 語言 MASSIVE intent,`Router` 可讓 45/51 語言達到 3x random 以上;英文 checkpoint 只有 23/51。
- XNLI 14 種非英文:`Router` 0.731 vs 英文 0.521。

### 與 Jev 比較(Router 後)

| 指標 | Jev 1.13.0(公開) | Laya(routed) |
|---|---|---|
| typed-decisions(2,000 題) | 0.727 | **0.766** |
| AG News(4 類) | 0.910 | **0.950** |
| DAIR Emotion(6 類) | 0.480 | **0.595** |
| Banking77(>20 選項) | **0.870** | 0.425 |
| ECE(越小越好) | 0.246 | **0.081**(temperature fit 後) |
| p50 延遲,1 題 | 236–276 ms | **32.8 ms** |
| 權重 | 閉源 API | **Apache 2.0** |
| 成本 | $0.042 / 1M tokens | **$0 自架** |

## 六、微調

- 官方 notebook:`notebooks/laya_finetune_typed_decisions_2xT4_kaggle.ipynb`,Kaggle 免費 2xT4,約 4-5 小時 / 4 epoch / ~30k 題。
- 流程:建 dataset → RLCD(GRPO 風格 policy gradient)→ 校準 temperature → 評估 → push 到 Hub。
- 微調後 `laya-typed-decisions` 在 typed-decisions 基準 0.766,遠超 base 的 0.362(接近隨機 0.318、多數類基線 0.461)。
- 實例:`docs/finetune_browser_agent.md` 在 browser-agent 場景,element top-1 從 zero-shot 0.10 到 0.66,real-task success 從 0% 到 62%,每步 17-23 ms。

## 七、已知限制(誠實清單)

1. **base checkpoint zero-shot 接近隨機**(0.362 vs 隨機 0.318),主要價值在微調後。
2. **`choice` 避免 boolean 字樣標籤**(`true/false`、`yes/no` 會被標籤文字本身劫持)。
3. **negation 處理不穩**:否定句(如 "don't cancel my account")可能仍被解讀為 `cancel_account`。
4. **>20 選項的高卡數 choice**:受 `head_max_len` token 預算限制,Banking77 只有 0.425(Jev 0.870);建議提高 `head_max_len`、用 `predict_shortlist`、或拆成粗/細兩題。
5. **`noul` 可能跟随標籤而非 state**(尤其英文 checkpoint):對 positive 輸入回 confident "no";建議用 `labels` 覆寫。
6. **`laya-multilingual` 在 `score` 上有 position bias**(#131):罕選第一級。
7. **`action.act_probability` 目前無訊號**,應改 gate on `confidence`。
8. **英文 checkpoint 崩在非拉丁文**,反之 multilingual 在英文較弱 —— 用 Router 或手動選。

## 八、生態與工具

- **官方**:HuggingFace model / Space、Colab notebook、Nix flake。
- **社群**:
  - [omp-laya-judge](https://github.com/F0Rextasy/omp-laya-judge) — oh-my-pi 插件 + local MCP judge。
  - [laya-adk-toolkit](https://github.com/Ashfaqbs/laya-adk-toolkit) — Google ADK tools。
  - [laya-Ascend](https://github.com/zzhdbw/laya-Ascend) — Huawei Ascend NPU(torch-npu,34-71x 加速)。
  - [laya-apple](https://github.com/tc3oliver/laya-apple) — Apple Silicon MLX + ANE。
  - [stuntd](https://github.com/bladedevoff/stuntd) — Jev API 相容代理 + 自訓練 head。

## 九、總結

**適合**:
- 需要**低延遲**(<50 ms)的 structured decision 場景(路由、guardrail、ticket triage、內容安全)。
- **自架、開源、成本敏感**,不想付 per-token API 費用。
- **多語言**需求(100+ 語言,Router 自動分派)。
- 想**微調**到自己領域,且能接受 2xT4 級別的訓練成本。

**不適合**:
- **開放式問答或文字生成** —— Laya 只做 typed decision。
- **>20 選項的高卡數分類**,不打算調 `head_max_len` 或 shortlist。
- **需要 raw probability 分佈**做下游 softmax matching —— Jev 的 soft accuracy 更好。
- **零樣本、通用決策** —— base checkpoint 接近隨機,必須微調。

Laya 的核心價值是把「TypeSafe Jev 那類決策模型」以**開源、自架、更快、多語言**的方式重做,並用 Router + typed primitive 把「一次 forward pass 回多題」做實。對已經在 Jev 上的團隊,`laya[serve]` 提供幾乎零改遷移路徑;對新團隊,微調後的 0.766 vs base 0.362 的差距提醒:它是一個**快速底層**,不是一個開箱即用的決策引擎。

---

*資料來源:[NandhaKishorM/laya README](https://github.com/NandhaKishorM/laya/blob/main/README.md)、[BENCHMARKS.md](https://github.com/NandhaKishorM/laya/blob/main/BENCHMARKS.md)、[HuggingFace Model](https://huggingface.co/convaiinnovations/laya)。*
