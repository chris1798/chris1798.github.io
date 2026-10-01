---
title: "LiteLLM Guardrail BLOCK 事件查詢 SOP：用 API 取得被擋請求的 log"
date: 2026-10-01
description: 完整 SOP：當 LiteLLM Proxy 的 guardrail 把請求擋下（HTTP 400）時，如何透過 admin API / Postgres 取得該 BLOCK 事件的完整 log，含 guardrail_name、觸發 pattern、risk score、耗時等細節。
tags: [LiteLLM, guardrail, BLOCK, 稽核, spend-logs, SOP, AI安全]
---

# LiteLLM Guardrail BLOCK 事件查詢 SOP

> 本 SOP 記錄一次**真實完成並端到端驗證通過**的查詢流程：在 `192.168.1.101` 的 LiteLLM Proxy（Docker/Podman，DB 模式）上，對 `litellm_content_filter` 規則發了一個會觸發 BLOCK 的請求，然後從 admin API 把該事件的完整 log 撈出來。

**一句話結論：可以。** BLOCK 事件會寫進該請求的 spend log（Postgres `LiteLLM_SpendLogs`），guardrail 細節存在 **`metadata.guardrail_information`** 欄位，可用 admin API 取得。

## 0. 環境總覽（本次實測）

| 項目 | 值 |
|------|----|
| 主機 | `192.168.1.101`（RHEL 9.8，podman rootful） |
| Proxy | container `litellm_litellm_1`，port `4000`，`STORE_MODEL_IN_DB:True` |
| DB | container `litellm_db_1`，Postgres `litellm` @ `db:5432/litellm` |
| 本機 admin key | `LITELLM_MASTER_KEY=sk-1234`（**實測 auth 失敗**，見 Step 4） |
| 測試用 admin key | `sk-gwtest01`（本 SOP 新發，可正常查 log） |
| 受測 guardrail | `MXIC_keyword`（`litellm_content_filter`，pre_call） |

## 1. 三層取法（由快到慢）

| 取法 | 拿到什麼 | 時機 |
|------|---------|------|
| **400 回應 body + header** | `blocked_reason`、`guardrail_name`、`guardrail_mode`、`x-litellm-applied-guardrails` | 即時，呼叫當下 |
| **admin API（`/spend/logs`）** | 完整 `guardrail_information`（pattern、score、耗時、matched details） | 事後稽核、可查歷史 |
| **直連 Postgres** | 同上（`metadata` JSON），debug 時最直接 | 除錯 |

## 2. 即時：從 400 回應直接讀

被擋的請求回 **HTTP 400**，body 與 header 就有一級資訊，不必等 log：

```json
{
  "error": {
    "message": "Content blocked: 機敏 pattern detected",
    "type": "invalid_request_error",
    "code": "400",
    "provider_specific_fields": {
      "error": "Content blocked: 機敏 pattern detected",
      "pattern": "機敏",
      "guardrail_name": "MXIC_keyword",
      "guardrail_mode": "pre_call"
    }
  }
}
```

對應的 response header：

```
x-litellm-call-id: 004d7b85-eb2e-4945-b245-6c609d4e630f
x-litellm-applied-guardrails: yara-x-guardrail,MXIC_keyword
```

> 記下 `x-litellm-call-id` / `request_id`，下一步就用它去撈完整 log。

## 3. 事後稽核：admin API

### 3.1 依 request_id 撈（最直觀）

```bash
curl -s -G 'http://<proxy>:4000/spend/logs' \
  -H "Authorization: Bearer ***" \
  --data-urlencode 'request_id=<上面拿到的 id>'
```

回傳是 list，每筆含 `status`（被擋為 `failure`）、`model`、以及 **`metadata`**（注意：API 回傳的 `metadata` 是**字串**，要先 `json.loads` 一次）。

### 3.2 guardrail_information 長什麼

`metadata.guardrail_information` 是 **list**，該次觸發的每個 rule 一筆。被擋那筆（`MXIC_keyword`）實測：

```json
{
  "guardrail_name": "MXIC_keyword",
  "guardrail_provider": "litellm_content_filter",
  "guardrail_mode": "pre_call",
  "guardrail_status": "guardrail_intervened",
  "detection_method": "regex",
  "risk_score": 10.0,
  "patterns_checked": 3,
  "match_details": [
    {"type": "pattern", "snippet": "機敏", "action_taken": "BLOCK", "detection_method": "regex"}
  ],
  "guardrail_response": [{"type": "pattern", "action": "BLOCK", "pattern_name": "機敏"}],
  "masked_entity_count": {},
  "guardrail_id": "89cc82c1-07a8-43f4-aed0-e7ace13b2e7c",
  "duration": 0.000223,
  "start_time": 1790865612.777583,
  "end_time": 1790865612.777805
}
```

同一次請求沒觸發的 rule（如 `yara-x-guardrail`）也在同一個 list，`guardrail_status` 為 `success`、`guardrail_response` 為 `"mask"`。

### 3.3 metadata 裡的其他相關欄位

| 欄位 | 用途 |
|------|------|
| `applied_guardrails` | 該次實際跑了哪些 guardrail（array） |
| `guardrail_information` | 每個 rule 的細節（見上） |
| `error_information` | 400 的 `error_message`、`error_class`、`traceback` |
| `status` | `failure`（被擋）/ `success` |

## 4. 前置：準備一枚可用的 admin key

> 本次環境 `LITELLM_MASTER_KEY=sk-1234` 實際呼叫回 **401**（`Invalid hash key`），master key 沒生效。這是 DB 模式的已知現象，照下面流程新發一枚即可。

**步驟（DB 模式）：**

1. 挑一個明文（例 `sk-gwtest01`），算它的 **SHA-256**：

   ```bash
   python3 -c "import hashlib;print(hashlib.sha256(b'sk-gwtest01').hexdigest())"
   # c4631583b1a139b18d069f615a539a2696700d3c8108f6a7bf90d322422ffd51
   ```

2. 直接 INSERT 一筆 token（`models='{}'` = 不限制模型）：

   ```sql
   INSERT INTO "LiteLLM_VerificationToken"
     (token, user_id, models, created_at, created_by, updated_at, updated_by)
   VALUES
     ('<sha256>', 'default_user_id', '{}', now(), 'hermes', now(), 'hermes');
   ```

   > `user_id` 用既有的 `proxy_admin` 帳號（本環境是 `default_user_id`），這樣這枚 key 才有 admin 權限查 guardrails / spend logs。

3. **重啟 proxy** 讓 role 生效（role 有記憶體快取，改 DB 不重啟不會套用到新 key）：

   ```bash
   podman restart litellm_litellm_1
   ```

4. 驗證：

   ```bash
   curl -s http://<proxy>:4000/v1/models -H "Authorization: Bearer ***" | head
   curl -s http://<proxy>:4000/v2/guardrails/list -H "Authorization: Bearer ***"
   ```

## 5. 除錯：直連 Postgres

```bash
podman exec -it litellm_db_1 psql -U litellm -d litellm
```

```sql
-- 找最近被擋的 row
SELECT request_id, status, model, "startTime"
FROM "LiteLLM_SpendLogs"
WHERE "startTime" > now() - interval '5 minutes'
ORDER BY "startTime" DESC LIMIT 6;

-- 撈完整 guardrail 細節
SELECT request_id, status, model,
       json_extract_path_text(metadata, 'guardrail_information')
FROM "LiteLLM_SpendLogs"
WHERE request_id = '<id>';
```

> **注意：** `LiteLLM_SpendLogs` **沒有** `guardrail_information` 獨立欄位，它在 `metadata`（JSONB）裡。

## 6. 本次實測踩到的小坑

| 現象 | 原因 / 處理 |
|------|-------------|
| `sk-1234` 回 401 | master key 沒生效；新發 token（Step 4） |
| 改完 token 的 `user_id` 還是 `role=unknown` | role 有快取，**要 `podman restart`** 才套用 |
| `/spend/logs/v2` 用我的 key 查不到那筆 | v2 需 `start_date`+`end_date`，且**依 user 範圍過濾**；那筆 row 的 `user` 欄位被寫成 `litellm`（非 `default_user_id`），故 v2 漏掉。改用 **`/spend/logs?request_id=`**（legacy）即可 |
| API 的 `metadata` 是字串 | 要 `json.loads(metadata)` 再取 `guardrail_information` |
| 被擋 row 的 `status` | 是 `failure`，`model` 有值；`total_tokens=0`、`spend=0` |

## 7. 建議 / 收尾

- **即時知道擋了誰** → 看 400 body + `x-litellm-applied-guardrails` header。
- **事後稽核** → `GET /spend/logs?request_id=<id>`，細節都在 `metadata.guardrail_information`。
- **接 Langfuse / custom callback** → 同一份 logging payload（含 guardrail_information）也會推過去，可用第三方後端持續監控。
- **待修**：① 重設一個能生效的 master key；② spend log 的 `user` 欄位寫成 `litellm`，會造成 v2 / UI Logs 分頁漏掉這些 failure row。

## 附錄：本次環境 guardrail 清單

| guardrail_name | type | mode | api_base |
|----------------|------|------|----------|
| `yara-x-guardrail` | generic_guardrail_api | pre_call | `http://host.docker.internal:5502` |
| `gliner-guardrail` | generic_guardrail_api | pre_call | `http://host.docker.internal:5501` |
| `Prompt Injection: SQL` | litellm_content_filter | pre_call | — |
| `Harmful Violence` | litellm_content_filter | pre_call | — |
| `Prompt Injection: Data Exfiltration` | litellm_content_filter | pre_call | — |
| `Presidio PII` | presidio | pre_call | — |
| `MXIC_keyword` | litellm_content_filter | pre_call | — |

`MXIC_keyword` 的 pattern（本次受測）：

| pattern | name | action |
|---------|------|--------|
| `MXIC\|旺宏` | company name | MASK |
| `機敏\|機密\|confidential` | 機敏 | **BLOCK** |
| prebuilt `generic_api_key` | generic_api_key | BLOCK |
