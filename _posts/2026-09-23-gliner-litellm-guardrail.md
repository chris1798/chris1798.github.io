---
title: "在 RHEL 9 安裝 GLiNER 並整合進 LiteLLM Guardrail 完整手冊"
date: 2026-09-23
description: 在 Red Hat Enterprise Linux 9 上安裝 GLiNER NLP 模型，建立 FastAPI guardrail 服務，並透過 Generic Guardrail API 整合進 LiteLLM Proxy 的完整實作過程。
tags: [GLiNER, LiteLLM, guardrail, RHEL9, NLP, FastAPI]
---

# 在 RHEL 9 安裝 GLiNER 並整合進 LiteLLM Guardrail 完整手冊

本文記錄在 **Red Hat Enterprise Linux 9.8** 虛擬機（192.168.1.101）上安裝 [GLiNER](https://github.com/urchade/GLiNER)（通用 NER 模型），建立自訂 guardrail 服務，並整合進既有 **LiteLLM Proxy** 的完整過程。過程中踩到不少坑（GLiNER 0.2.x API 改版、LiteLLM DB 驅動模式讓 config.yaml 設定失效、sudo 重定向問題），全部整理在內。

## 目標環境

| 項目 | 規格 |
|---|---|
| OS | Red Hat Enterprise Linux 9.8 |
| CPU | i7-12700K（4 vCPU，無 GPU，純 CPU 推論） |
| RAM | 7.5 GB |
| Python | 3.9（系統版） |
| 容器引擎 | Podman 5.8.2（`docker` 指令為其別名） |
| LiteLLM | v1.100.0，podman 容器 `litellm_litellm_1`（port 4000），`STORE_MODEL_IN_DB=True` |

## 架構總覽

```
用戶請求 ──> LiteLLM Proxy (:4000)
                │ pre_call guardrail (gliner-guardrail)
                │ host.docker.internal:5501
                ▼
        GLiNER Guardrail 服務 (FastAPI, :5501)
                │ 偵測 person/organization/location/date
                ▼
        回傳 BLOCKED / NONE
```

## 步驟 1：安裝 GLiNER

### 建立 venv 並安裝 CPU 版 PyTorch + GLiNER

```bash
python3 -m venv /home/chris/gliner-venv
/home/chris/gliner-venv/bin/pip install --upgrade pip
# CPU 版 torch（無 GPU 環境務必指定 index-url，否則會下載 CUDA 版，數 GB）
/home/chris/gliner-venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
/home/chris/gliner-venv/bin/pip install gliner fastapi uvicorn
```

### ⚠️ 坑 1：GLiNER 0.2.x API 改版

GLiNER 0.2.x 的 API 與舊版完全不同，舊文件/教學的寫法都會失敗：

| 寫法 | 結果 |
|---|---|
| `from gliner import GlinerV2`（舊版教學） | `ImportError: cannot import name 'GlinerV2'` |
| `pip install gliner-v2` | PyPI 沒有這個包 |
| **`from gliner import GLiNER`**（新版正確） | ✅ |

新版 API 的 `predict_entities` 需要**明確的 labels 列表**（不再是 task 字串）：

```python
from gliner import GLiNER

model = GLiNER.from_pretrained("gliner-community/gliner_small-v2.5")
model.eval()

labels = ["person", "organization", "location", "date"]
text = "John Smith works at Google in New York."
entities = model.predict_entities(text, labels, threshold=0.5)
for e in entities:
    print(e["text"], "=>", e["label"], round(e["score"], 2))
```

輸出：

```
John Smith => person 1.0
Google => organization 1.0
New York => location 0.99
```

模型首次載入會從 HuggingFace 下載約 240MB（`gliner-community/gliner_small-v2.5`），之後快取在 `~/.cache/huggingface`。

## 步驟 2：建立 Guardrail 服務

GLiNER 只是 NLP 函式庫，要讓 LiteLLM 呼叫它，需要包一層 HTTP API。LiteLLM 1.100 提供 **Generic Guardrail API**（Beta），讓自訂 guardrail 不用改 LiteLLM 程式碼即可接入。

### LiteLLM Generic Guardrail API 契約

| 項目 | 內容 |
|---|---|
| 端點 | `POST /beta/litellm_basic_guardrail_api`（LiteLLM 會自動把此路徑接到你的 `api_base`） |
| Request | `{"texts": ["文字"], "input_type": "request" 或 "response", ...}` |
| Response | `{"action": "BLOCKED" 或 "NONE" 或 "GUARDRAIL_INTERVENED", "blocked_reason": "...", "texts": [...]}` |
| `BLOCKED` | LiteLLM 直接擋下請求（400） |
| `NONE` | 放行 |

### 服務程式 `gliner_guardrail.py`

```python
"""LiteLLM GLiNER guardrail — 對齊 LiteLLM Generic Guardrail API。
端點: POST /beta/litellm_basic_guardrail_api
"""
import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

_LABELS = ["person", "organization", "location", "date"]
_THRESHOLD = float(os.environ.get("GLINER_THRESHOLD", "0.6"))
# 要阻擋的實體類型，逗號分隔；留空 = 只偵測不阻擋
_BLOCK_LABELS = {s.strip().lower() for s in os.environ.get("GLINER_BLOCK_LABELS", "").split(",") if s.strip()}
_MODEL_NAME = os.environ.get("GLINER_MODEL", "gliner-community/gliner_small-v2.5")

_model = None
def get_model():
    global _model
    if _model is None:
        from gliner import GLiNER
        _model = GLiNER.from_pretrained(_MODEL_NAME)
        _model.eval()
    return _model

class Request(BaseModel):
    texts: list = []
    input_type: str = "request"

@app.post("/beta/litellm_basic_guardrail_api")
def guardrail(req: Request):
    model = get_model()
    blocked, reasons = False, []
    for t in req.texts:
        if not t:
            continue
        ents = [e for e in model.predict_entities(t, _LABELS, threshold=_THRESHOLD)]
        for e in ents:
            if _BLOCK_LABELS and e["label"] in _BLOCK_LABELS:
                blocked = True
                reasons.append(f"[{req.input_type}] {e['label']}={e['text']} (score {e['score']:.2f})")
    if blocked:
        return {"action": "BLOCKED", "blocked_reason": "; ".join(reasons), "texts": req.texts}
    return {"action": "NONE", "texts": req.texts}

if __name__ == "__main__":
    port = int(os.environ.get("GLINER_PORT", "5501"))
    get_model()  # 啟動時預載模型
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### systemd user 服務（開機自啟）

`~/.config/systemd/user/gliner-guardrail.service`：

```ini
[Unit]
Description=GLiNER guardrail for LiteLLM
After=network-online.target

[Service]
WorkingDirectory=/home/chris/gliner
ExecStart=/home/chris/gliner-venv/bin/python /home/chris/gliner/gliner_guardrail.py
Restart=on-failure
Environment=GLINER_PORT=5501
Environment=GLINER_BLOCK_LABELS=

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now gliner-guardrail.service
```

### 直接測試 guardrail 端點

```bash
curl -s -X POST http://localhost:5501/beta/litellm_basic_guardrail_api \
  -H 'Content-Type: application/json' \
  -d '{"texts":["John Smith works at Google"],"input_type":"request"}'
```

只報告模式回傳：

```json
{"action":"NONE","texts":["John Smith works at Google"]}
```

設定 `GLINER_BLOCK_LABELS=person` 重啟後，同樣請求會回傳：

```json
{"action":"BLOCKED","blocked_reason":"[request] person=John Smith (score 0.99)","texts":["John Smith works at Google"]}
```

## 步驟 3：整合進 LiteLLM

### ⚠️ 坑 2：DB 驅動模式的 LiteLLM 會忽略 config.yaml 的 guardrail

LiteLLM 容器設定 `STORE_MODEL_IN_DB=True`（model 存在 PostgreSQL DB），此時 **config.yaml 裡的 `litellm_settings.guardrails` 不會被載入**。驗證方式：

1. 在 config.yaml 寫入 guardrail 並重啟容器
2. `curl /v2/guardrails/list` → 只看到 DB 裡的 guardrail，沒有 config.yaml 裡寫的
3. 發帶 `"guardrails": ["gliner-guardrail"]` 的請求 → 正常回應，guardrail 服務完全沒收到任何 POST

這是已知問題（[BerriAI/litellm#18363](https://github.com/BerriAI/litellm/issues/18363) 描述相近情形）。**解法：用 API 把 guardrail 寫進 DB。**

### 用 API 註冊 guardrail 到 DB

```bash
curl -s -X POST http://localhost:4000/guardrails \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "guardrail": {
      "guardrail_name": "gliner-guardrail",
      "litellm_params": {
        "guardrail": "generic_guardrail_api",
        "mode": "pre_call",
        "api_base": "http://host.docker.internal:5501",
        "unreachable_fallback": "fail_open"
      }
    }
  }'
```

注意事項：

- API 的 payload 格式與 config.yaml 不同：需要最外層 `{"guardrail": {...}}`，內層用 `guardrail_name` 而不是 `name`（照著 config 格式送會被 pydantic 擋下，回 missing field 錯誤）。
- `api_base` 只填 **base URL**（`http://host.docker.internal:5501`），LiteLLM 會自動接上 `/beta/litellm_basic_guardrail_api`。
- 容器內用 `host.docker.internal` 指回主機（podman 預設支援）。可先在容器內驗證：
  ```bash
  podman exec litellm_litellm_1 python -c "import urllib.request; urllib.request.urlopen('http://host.docker.internal:5501/beta/litellm_basic_guardrail_api', timeout=5)"
  ```
  （回 405 Method Not Allowed 代表已連上，GET 不被允許是正常的）
- `unreachable_fallback: fail_open` 代表 guardrail 服務掛掉時放行請求（預設 `fail_closed` 會擋全部請求，可視需求選）。

確認已註冊：

```bash
curl -s http://localhost:4000/v2/guardrails/list -H 'Authorization: Bearer sk-1234' | \
  python3 -c 'import sys,json; print([g["guardrail_name"] for g in json.load(sys.stdin)["guardrails"]])'
# ['gliner-guardrail', ...]
```

### 端到端測試

請求帶 `"guardrails": ["gliner-guardrail"]` 參數觸發：

```bash
curl -s -X POST http://localhost:4000/v1/chat/completions \
  -H 'Authorization: Bearer sk-1234' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "Qwen3.8-27B-Turbo",
    "messages": [{"role":"user","content":"Who is John Smith?"}],
    "max_tokens": 10,
    "guardrails": ["gliner-guardrail"]
  }'
```

**阻擋模式**（`GLINER_BLOCK_LABELS=person`）：

```json
{"error":{"message":"[request] person=John Smith (score 0.99)","type":"None","param":"None","code":"400"}}
```

**只報告模式**（`GLINER_BLOCK_LABELS` 留空）：正常回傳模型回應，guardrail 不阻擋。

## 步驟 4：常用管理指令

```bash
# 查看服務狀態 / 日誌
systemctl --user status gliner-guardrail
journalctl --user -u gliner-guardrail -f

# 修改阻擋規則（person/organization/location/date 逗號分隔）
sed -i 's/GLINER_BLOCK_LABELS=.*/GLINER_BLOCK_LABELS=organization,location/' \
  ~/.config/systemd/user/gliner-guardrail.service
systemctl --user daemon-reload && systemctl --user restart gliner-guardrail

# 從 LiteLLM 移除 guardrail（先拿 guardrail_id）
curl -s -X DELETE http://localhost:4000/guardrails/<guardrail_id> -H 'Authorization: Bearer sk-1234'
```

## 踩坑總表

| # | 坑 | 解法 |
|---|---|---|
| 1 | `GlinerV2` import 失敗、`gliner-v2` 包不存在 | 0.2.x 改用 `from gliner import GLiNER`，`predict_entities(text, labels_list, threshold)` |
| 2 | LiteLLM `STORE_MODEL_IN_DB=True` 時 config.yaml guardrail 不生效 | 改用 `POST /guardrails` API 寫進 DB |
| 3 | `POST /guardrails` 回 missing field | payload 要最外層 `{"guardrail": {"guardrail_name": ..., "litellm_params": {...}}}` |
| 4 | `echo pw \| sudo ... cat >> /root/...` 失敗 | 重定向是 shell（chris 身份）執行，`>>` 會 Permission denied；改用 `sudo bash -c 'cat a >> b'` 或 `sudo tee -a` |
| 5 | 無 GPU 環境裝 torch 預設下 CUDA 版 | `pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| 6 | guardrail 沒觸發難除錯 | 直接看 guardrail 服務的 access log 有沒有收到 POST，可立即判斷是「LiteLLM 沒綁定」還是「連通問題」 |

## 參數速查

| 環境變數（gliner-guardrail.service） | 預設 | 說明 |
|---|---|---|
| `GLINER_PORT` | 5501 | 服務埠 |
| `GLINER_BLOCK_LABELS` | 空 | 要阻擋的實體類型，逗號分隔 |
| `GLINER_THRESHOLD` | 0.6 | NER 置信度門檻 |
| `GLINER_MODEL` | gliner-community/gliner_small-v2.5 | HuggingFace 模型 |

| LiteLLM litellm_params | 說明 |
|---|---|
| `guardrail: generic_guardrail_api` | 使用 Generic Guardrail API |
| `mode: pre_call` | 請求前檢查（`post_call` = 回應後） |
| `api_base` | guardrail 服務 base URL（不含路徑） |
| `unreachable_fallback` | `fail_open`（放行）/ `fail_closed`（預設，全擋） |
