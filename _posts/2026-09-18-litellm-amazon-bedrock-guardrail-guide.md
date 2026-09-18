---
title: "LiteLLM 串接 Amazon Bedrock Guardrail：精準檢查輸入並保留輸出流式延遲"
date: 2026-09-18
description: "整理 AWS 實測結論：LiteLLM 內建 Guardrail 為何無法同時滿足輸入精準檢查與輸出零延遲，以及如何用 ApplyGuardrail 加無 Guardrail 的模型呼叫完成兩步式安全檢查。"
tags: [AWS-Bedrock, LiteLLM, Guardrail, LLM-Security, Agent]
---

# LiteLLM 串接 Amazon Bedrock Guardrail：精準檢查輸入並保留輸出流式延遲

> 本文整理自 [AWS 官方中文文章：〈一站式搞懂如何在 LiteLLM 上配置 Amazon Bedrock Guardrail〉](https://aws.amazon.com/cn/blogs/china/one-stop-how-to-litellm-configuration-amazon-bedrock-guardrail/)，由 AWS 架構師白雪堯撰寫。原文發表於 2026 年 9 月 17 日，文中測試日期為 2026 年 8 月 26 日。本文以繁體中文重組重點、實作步驟與決策建議，並非逐字翻譯。

## 摘要

給 Agent 或工具呼叫型應用程式加上 LLM Guardrail 時，常見需求其實相當精細：

1. **只檢查最新使用者輸入**：排除 system prompt、歷史訊息與 tool result，避免固定內容造成誤報。
2. **完全不檢查模型輸出**：輸出必須即時流式送回客戶端，不緩衝、不增加輸出檢查延遲。

AWS 的實測顯示，LiteLLM 現有的兩種 Guardrail 整合方式各只能滿足一半：

- `pre_call` 模式能在模型呼叫前檢查，但會把整組 messages 或最後一則訊息送給 `ApplyGuardrail`。
- 模型層級的 `guardrailConfig` 能精準標記最新使用者輸入，但 Bedrock 仍會建立 output assessment；即使所有 output policy 都設為 `NONE`，仍會產生流式緩衝。

真正穩定的作法，是自行完成兩步呼叫：

1. 只將 `user_input` 交給 `ApplyGuardrail`。
2. 若未被攔截，再以**不包含 `guardrailConfig`** 的普通 `converse_stream` 呼叫模型。

這不是把 Guardrail 關掉，而是讓輸入檢查與模型流式輸出成為兩個彼此解耦的流程。

## 三個核心角色

### Amazon Bedrock

Amazon Bedrock 是 AWS 的托管 LLM 服務。透過 API 可以呼叫 Claude、GPT、Llama 等模型，常見的兩種呼叫方式是：

- `converse`：一次取得完整回應。
- `converse_stream`：逐段流式回傳，適合聊天與 Agent 應用。

### Amazon Bedrock Guardrail

Guardrail 是 Bedrock 提供的內容安全能力。先在控制台設定政策，例如：

- 攔截暴力或危險內容。
- 偵測到 email 時執行 `BLOCK`。
- 偵測提示詞注入。

設定完成後會取得 Guardrail ID 與版本，之後可透過兩種方式使用：

1. **模型內建檢查**：在模型呼叫中加入 `guardrailConfig`，由 Bedrock 自動執行 input/output assessment。
2. **獨立檢查**：呼叫 `ApplyGuardrail`，自行決定要檢查哪些文字，再另外呼叫模型。

### LiteLLM

LiteLLM 是開放原始碼 LLM 閘道，可將不同模型抽象成統一的 OpenAI 格式 API。它內建 Bedrock Guardrail 整合，但也正是下列實測差異的主要來源。

## 需求：只查使用者輸入，完全不查輸出

以工具呼叫型 Agent 為例，一次模型請求可能包含：

```text
system prompt
歷史 user messages
tool result
最新 user message
```

安全團隊可能要求：

- **Input**：只檢查最新 user message。
- **Output**：模型回應原速流式送出，不做 output 檢查。

這個需求直覺上很簡單，但 LiteLLM 的標準配置無法完整達成。

## LiteLLM 的兩種標準玩法為何都不夠

### 做法一：Proxy `pre_call` 模式

典型設定如下：

```yaml
guardrails:
  - guardrail_name: input-guard
    litellm_params:
      guardrail: bedrock
      mode: pre_call
      default_on: true
```

`pre_call` 會在模型呼叫前啟動 `ApplyGuardrail`。它確實能達成「模型輸出不檢查」，但 LiteLLM 送給 Guardrail 的內容可能包含：

```text
system prompt
歷史 user messages
tool result
最新 user message
```

若 system prompt 或 tool result 命中政策，模型呼叫會直接失敗，例如收到：

```text
HTTP 400
Violated guardrail policy
```

LiteLLM 提供的補救參數是：

```yaml
experimental_use_latest_role_message_only: true
```

但其實測語義不是「找出最後一則 role=user」，而是：

> **只檢查 messages 列表中的最後一則內容，不判斷它是誰寫的。**

在標準 Agent 工具循環中：

```text
user message
→ 模型產生 tool call
→ 工具回傳 role=tool
→ 再次呼叫模型
```

如果最後一則是 `tool result`，Guardrail 檢查的就會是 tool result，而不是使用者輸入。因此，`pre_call` 加 `latest` 參數仍無法可靠達成輸入側需求。

### 做法二：模型層級 `guardrailConfig`

另一種方式是在 LiteLLM 模型配置中直接加入 `guardrailConfig`：

```yaml
model_list:
  - model_name: my-model
    litellm_params:
      model: bedrock/us.anthropic.claude-haiku-4-5-20251001-v1:0
      guardrailConfig:
        guardrailIdentifier: "xxxx"
        guardrailVersion: "1"
        trace: enabled
```

這種方式使用 Bedrock 的 `guardContent` 標記，把最新使用者輸入包裝成 Guardrail 的檢查內容。AWS 的 trace 顯示：

```text
input guardrailCoverage:
  guarded = 58
  total   = 213
```

代表全部 213 個字元中，只有被標記的 58 個使用者字元被檢查；system prompt 與 tool result 沒有送檢，符合 input 需求。

問題出在輸出端。即使所有 output policy 都設為 `NONE`，trace 仍顯示：

```text
outputAssessments:
  guardrailCoverage:
    guarded = 40
    total   = 40
  contentPolicyUnits = 0
```

這表示：

- 40 個輸出字元仍被送進 Guardrail 處理流程。
- `contentPolicyUnits = 0` 只代表沒有任何 output policy 實際命中。
- 流式輸出仍會先緩衝，再檢查後放行，延遲並未消失。

換句話說，模型內建模式是「出門安检的門還在，只是檢查儀沒有開」。

### 兩種方式同時開啟

若同時使用 Proxy `pre_call` 與模型層級 `guardrailConfig`，實際流程會變成：

```text
ApplyGuardrail(INPUT)
→ ConverseStream(guardrailConfig)
→ Bedrock input assessment
→ Bedrock output assessment
```

同一份使用者輸入會被檢查兩次，output 仍會被緩衝，而且成本和延遲都增加，不建議這樣組合。

## 建議架構：自訂兩步呼叫

要同時達成「只查使用者輸入」與「輸出零 Guardrail 延遲」，最穩定的方式是繞過模型內建 Guardrail，自行呼叫兩個 Bedrock API。

### 完整範例

```python
import boto3

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-west-2",
)

# 第一步：只檢查使用者輸入
guard = bedrock.apply_guardrail(
    guardrailIdentifier="xxxx",
    guardrailVersion="1",
    source="INPUT",
    content=[
        {
            "text": {
                "text": user_input
            }
        }
    ],
)

# 若 Guardrail 介入，模型不會被呼叫
if guard["action"] == "GUARDRAIL_INTERVENED":
    return guard["outputs"][0]["text"]

# 第二步：普通模型呼叫，不加入 guardrailConfig
stream = bedrock.converse_stream(
    modelId="us.anthropic.claude-haiku-4-5-20251001-v1:0",
    system=[
        {"text": system_prompt}
    ],
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "text": user_input
                }
            ]
        }
    ],
)

# 輸出直接流式傳回，Guardrail 不會阻斷輸出流程
```

### 為何這樣可行

這個架構的關鍵不是某個參數，而是呼叫結構：

- 第一步只把 `user_input` 交給 `ApplyGuardrail`。
- 第二步的模型請求不包含 `guardrailConfig`。
- 因此 system prompt、tool result 不會送檢，輸出也不會經過 Guardrail。
- 如果 Guardrail 攔截輸入，Python 控制流程會提前回傳，模型不會被呼叫。

兩個 API 本身沒有資料關聯；它們的唯一關聯就是上面的 `if`。生產環境應透過 IAM 限制，只允許閘道角色直接呼叫模型，避免業務端繞過輸入檢查。

### 可選方案：LiteLLM CustomGuardrail hook

如果不想完全繞過 LiteLLM，可以實作自訂 `CustomGuardrail` hook：

1. 在 `pre_call` 中檢查完整 messages。
2. 找出最後一則 `role=user` 的訊息。
3. 只把該內容交給 `ApplyGuardrail(source="INPUT")`。
4. 若被攔截則停止模型呼叫。
5. 放行後，以不含 `guardrailConfig` 的普通模型設定呼叫 LiteLLM。

這約需百行左右的 Gateway 程式碼，但能保留 LiteLLM 的配置與路由能力。

## 為什麼輸出檢查會造成延遲

流式回應不是把完整結果一次交給程式，而是：

```python
for event in stream["stream"]:
    yield event
```

模型會逐段產生內容，程式收到一段、轉發一段。若要在放行前檢查輸出，就必須：

1. 先扣住一段內容。
2. 呼叫 Guardrail。
3. 檢查完成後才交給客戶端。

AWS 實測中，`ApplyGuardrail` 單次檢查約需 150 ms。因此，streaming 不等於可以邊產生邊檢查而不延遲；只要檢查結果影響是否放行，就必須緩衝至少一個檢查週期。

若合規需求只是「事後知道結果」，而不是「輸出前攔截」，可以改成：

- 模型輸出即時流式傳回。
- 完成後將全文送至 Guardrail 做异步稽核。
- 稽核結果只寫入日誌、儀表板或告警。

這種「流式放行＋事後稽核」才能兼顧即時性與安全可追溯性。

## GPT-5.6 的例外：暫時繞過 output 檢查

AWS 的實測另外發現一項值得注意的例外：部分 GPT-5.6 模型的 `guardrailConfig` 雖然執行 input 檢查，卻沒有執行 output 檢查。

### 實測結果

以 `EMAIL → BLOCK` 政策測試，讓模型固定輸出 `audit@example.com`：

| 模型 | 帶 `guardrailConfig` 的輸出結果 | 結論 |
|---|---|---|
| Claude Haiku 4.5 | 收到 `OUTPUT_BLOCKED_BY_GUARDRAIL` | output 檢查正常 |
| GPT-5.6 Sol / Terra / Luna | 收到原始 `audit@example.com` | output 檢查未執行 |
| GPT-OSS 120B | 被 Guardrail 攔截 | output 檢查正常 |

GPT-5.6 的 input 檢查仍正常：發送提示詞注入文本時，會回傳 `guardrail_intervened`，且 `inputTokens = 0`，代表模型尚未開始產生就被攔截。

非流式呼叫 GPT-5.6 時，trace 顯示：

```text
modelOutput: []
inputAssessment:
  coverage: 37/37
```

沒有 `outputAssessments`，但 input assessment 正常存在。

### 可能的技術原因

合理的解釋是，GPT-5.6 使用 Bedrock 較新的專有 serving 路徑。input 檢查發生在統一入口，因此仍會執行；output 檢查則需要把模型回應導向 Guardrail 流程，這個出口鉤子可能尚未完整串接至 GPT-5.6 的新路徑。

重點不是模型供應商，而是模型實際使用的 Bedrock serving pipeline。

### 能否直接採用這個例外？

目前這個組合確實可能同時滿足：

- input 精準檢查。
- output 沒有被送檢。

但這是**當時實測下偶然出現的行為**，不是 AWS 文件承諾的穩定保證。若暫時採用，至少應建立 canary 監控：

1. 定期讓模型輸出固定的可攔截內容，例如 `audit@example.com`。
2. 驗證客戶端仍收到原始內容，確認 output 尚未送檢。
3. 一旦 canary 被攔截，代表 output 檢查已啟用，應立即切換至自訂兩步呼叫。
4. 預先保留 `CustomGuardrail` 或直調 Bedrock 的切換方案。

另外，GPT-5.6 在 Bedrock 實測時不接受 `temperature` 參數，重現測試時需要移除。

## 方案比較

| 方案 | 只查真實使用者輸入 | 輸出完全不送檢 | 性質 |
|---|---:|---:|---|
| `ApplyGuardrail`＋無 `guardrailConfig` 的模型呼叫 | ✅ | ✅ | 架構上穩定，推薦 |
| LiteLLM Proxy `pre_call` | ❌ | ✅ | 可能檢查 system prompt 或 tool result |
| `pre_call`＋`latest` 參數 | ❌ | ✅ | 可能檢查最後一則 tool result |
| 模型層級 `guardrailConfig`＋Claude | ✅ | ❌ | output 仍會被緩衝 |
| 模型層級 `guardrailConfig`＋GPT-5.6 | ✅ | ✅（目前實測） | 偶然行為，需要 canary |
| LiteLLM 自訂 `CustomGuardrail` hook | ✅ | ✅ | 需少量 Gateway 開發 |

## 生產環境檢查清單

部署前建議確認：

- [ ] Guardrail ID、版本與 region 正確。
- [ ] `ApplyGuardrail` 只收到最新使用者輸入。
- [ ] system prompt、tool result、歷史訊息沒有送進 Guardrail。
- [ ] 模型呼叫設定中沒有 `guardrailConfig`。
- [ ] Guardrail 攔截時，模型絕對不會被呼叫。
- [ ] 輸出 streaming 沒有額外的 output assessment 緩衝。
- [ ] 只有閘道 IAM role 擁有 `bedrock:InvokeModel` 權限。
- [ ] 業務程序沒有能力繞過輸入檢查直接呼叫模型。
- [ ] 對可能改變的 Bedrock 模型路由建立 canary 監控。
- [ ] 若需要輸出稽核，採用完成後异步送檢，而不是輸出前攔截。

## 實測環境與關鍵資料

AWS 原文使用的實測環境：

- 測試日期：2026-08-26
- LiteLLM：1.81.14
- Region：`us-west-2`
- Claude：`us.anthropic.claude-haiku-4-5-20251001-v1:0`
- OpenAI：GPT-5.6 Sol / Terra / Luna
- 開源模型：GPT-OSS 120B

關鍵結果：

- Proxy 預設模式會送檢 system、歷史訊息、tool result 與最新 user。
- `latest` 模式在請求以 tool result 結尾時，會檢查 tool result 本身。
- 模型層級模式 input coverage 為 `guarded=58/total=213`。
- 所有 output policy 設為 `NONE` 時，仍有 `guarded=40/40` 的 `outputAssessments`。
- GPT-5.6 非流式 trace 中 `modelOutput` 為空，也沒有 `outputAssessments`。
- `ApplyGuardrail` 單次檢查延遲約 150 ms。

## 結論

Bedrock Guardrail 可以分成兩種模式：

- **模型內建模式**：設定簡單，input 標記精準，但 output 檢查流程無法完全移除。
- **獨立 `ApplyGuardrail` 模式**：檢查對象與時機完全由程式控制，能與模型 streaming 解耦。

當需求是「只檢查最新使用者輸入，同時完全不檢查輸出」時，自訂兩步呼叫是最可靠的架構。LiteLLM 若沒有內建能精確拆開 messages 的 Guardrail 模式，就應使用 `CustomGuardrail` hook 或直接在 Gateway 中實作。

對於 GPT-5.6 暫時沒有 output 檢查的現象，可以作為短期選項，但必須視為未承諾行為，並搭配 canary 監控與可切換方案。

## 原文資訊

- 原文標題：[一站式搞懂如何在 LiteLLM 上配置 Amazon Bedrock Guardrail](https://aws.amazon.com/cn/blogs/china/one-stop-how-to-litellm-configuration-amazon-bedrock-guardrail/)
- 原文作者：白雪堯，亞馬遜雲科技解決方案架構師
- 原文發表日期：2026-09-17
- 原文測試日期：2026-08-26
- 原文分類：Artificial Intelligence

> 原文提醒：部分特定 AWS 生成式 AI 服務當時在海外區域可用；中國區域的相關雲端服務由西雲數據與光環新網營運，實際可用性以中國區域官方資訊為準。
