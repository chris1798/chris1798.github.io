---
title: "LiteLLM 共用 Virtual Key 多人使用時，如何追蹤每個使用者的用量？"
date: 2026-08-03
description: 解答 LiteLLM 共用 Virtual Key 的 end_user_id 追蹤機制、個人用量查詢方法、預算限制與推薦架構
tags: [litellm, virtual-key, cost-tracking, end-user, multi-user, budget-control]
---

# LiteLLM 共用 Virtual Key 多人使用時，如何追蹤每個使用者的用量？

許多企業會為部門建立共用的 Virtual Key，讓多個成員共用。但這引發了一個關鍵問題：**共用 Key 時，能否追蹤每個使用者的實際用量和成本？**

**答案：可以，但有條件。** LiteLLM 支援通過 `end_user_id` 實現共享 Key 的個人用量追蹤。

---

## 📊 end_user_id 追蹤機制

當多人共用同一個 Virtual Key 時，LiteLLM 會將每筆請求的 `end_user_id` 作為追蹤維度。

### 請求範例

```bash
# 張偉使用共享 Key 發送請求
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-shared-team-key-xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "分析這週銷售數據"}],
    "user": "zhang.wei@company.com"   ← 關鍵：設定 end_user_id
  }'

# 李華使用同一個共享 Key 發送請求
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-shared-team-key-xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "撰寫行銷文案"}],
    "user": "li.hua@company.com"      ← 不同的 end_user_id
  }'
```

**關鍵規則**：必須在請求的 JSON body 中傳遞 `user` 欄位，LiteLLM 才會將該請求歸檔到對應的使用者。如果不傳 `user` 欄位，所有請求只會計在 Key 的總層級，無法區分個人。

---

## 🔍 查詢個人用量

### 透過 API 查詢

```bash
# 查詢特定使用者的花費
curl -X GET "http://localhost:4000/user/info?user_id=zhang.wei@company.com" \
  -H "Authorization: Bearer sk-master-key-xxx"

# 查詢所有使用者的花費排名
curl -X GET "http://localhost:4000/spend/users?start_time=2026-08-01&end_time=2026-08-03" \
  -H "Authorization: Bearer sk-master-key-xxx"

# 查詢 Global Spend Report（全公司花費報告）
curl -X GET "http://localhost:4000/global/spend/report" \
  -H "Authorization: Bearer sk-master-key-xxx"
```

### 透過 Admin UI 查詢

訪問 `http://your-server:4000/ui`，在儀表板中可以看到：

- **Spend by User**：按使用者統計花費
- **User Activity Log**：每個使用者的活動記錄
- **Per-User Spend Report**：個人花費明細報表

### 查詢結果範例

```json
[
  {
    "user_id": "zhang.wei@company.com",
    "total_spend": 12.50,
    "total_requests": 150,
    "total_tokens": 125000,
    "avg_tokens_per_request": 833
  },
  {
    "user_id": "li.hua@company.com",
    "total_spend": 8.30,
    "total_requests": 95,
    "total_tokens": 83000,
    "avg_tokens_per_request": 874
  },
  {
    "user_id": "wang.qiang@company.com",
    "total_spend": 15.75,
    "total_requests": 200,
    "total_tokens": 157500,
    "avg_tokens_per_request": 788
  }
]
```

---

## ⚠️ 重要注意事項

### 1. `user_id` 與 `user`（end_user_id）的區別

| 欄位 | 設定位置 | 追蹤層級 | 用途 |
|------|----------|----------|------|
| `user_id` | 建立 Key 時（Key 層級） | Key 層級 | Key 的所有者，不隨請求改變 |
| `user` / `end_user_id` | 每筆請求的 JSON body | 個人層級 | 實際發起請求的使用者 |

**常見誤區**：許多人誤以為設定 Key 的 `user_id` 就能追蹤個人用量。實際上 `user_id` 是 Key 的所有者（通常是部門或服務帳號），而真正的個人追蹤需要每筆請求都傳遞 `user` 欄位。

### 2. 預算控制的限制

共用 Key 的預算控制有以下限制：

```
共用 Key 的請求流程：
使用者請求 → Key 層級預算檢查 → end_user_id 追蹤
              ↓
         任何一層超支即拒絕
```

- **Key 層級預算**：共享 Key 的總預算會限制所有使用者的合計用量
- **個人層級預算**：共用 Key 下**無法**設定個人預算上限
- **已知 Bug**：GitHub Issue [#29142](https://github.com/BerriAI/litellm/issues/29142) 報告了共享 Key 下 `end_user_max_budget` 繼承的問題（緩存遺留）

### 3. 後端服務的注意事項

如果通過後端服務呼叫 LiteLLM，必須確保後端在每個請求中都傳遞正確的使用者資訊：

```python
import openai

# 後端服務代碼範例
def call_llm(user_email: str, prompt: str):
    client = openai.OpenAI(
        base_url="http://litellm:4000/v1",
        api_key="sk-shared-team-key-xxx"  # 共用 Key
    )
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        user=user_email  # ← 必須傳遞使用者 ID！
    )
    
    return response.choices[0].message.content
```

---

## 🏗️ 三種架構方案比較

### 方案 A：共用 Key + end_user_id（適合追蹤，不適合預算控制）

```
┌─────────────────────────────────────────┐
│        共享 Team Key                     │
│  (user_id: engineering@company.com)     │
└────────────────┬────────────────────────┘
                 │ 每筆請求設定 user 欄位
    ┌────────────┼────────────┐
    ▼            ▼            ▼
  張偉         李華         王強
  $12.50      $8.30       $15.75
```

| 優點 | 缺點 |
|------|------|
| ✅ Key 管理簡單，只需維護一個 Key | ❌ 無法設定個人預算上限 |
| ✅ 可以精確追蹤每個人的用量和成本 | ❌ 一個人超支會影響其他人（Key 層級預算） |
| ✅ 適合預算控制不嚴格的公司 | ❌ 已知 Bug：end_user_max_budget 繼承問題 |

**適合場景**：
- 公司允許部門內自由使用 AI
- 只需要追蹤用量進行成本分配
- 不想為每個使用者維護 Key

### 方案 B：個人 Virtual Key（適合預算控制）

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  張偉的 Key   │  │  李華的 Key   │  │  王強的 Key   │
│  budget: $50 │  │  budget: $50 │  │  budget: $50 │
│  RPM: 50     │  │  RPM: 50     │  │  RPM: 50     │
└──────────────┘  └──────────────┘  └──────────────┘
```

| 優點 | 缺點 |
|------|------|
| ✅ 可以設定個人預算上限 | ❌ Key 管理複雜，需為每個使用者維護 Key |
| ✅ 一個人超支不影響其他人 | ❌ Key 數量隨人數增長 |
| ✅ 更精細的訪問控制 | ❌ 需要額外的 Key 生成流程 |

**適合場景**：
- 公司有嚴格的 AI 使用預算
- 需要防止個人大量消耗
- 不同角色有不同的模型權限

### 方案 C：混合方案（⭐ 推薦）

```
┌─────────────────────────────────────┐
│  共享 Team Key                       │
│  （用於追蹤用量，設定 Team 總預算）    │
└────────────────┬────────────────────┘
                 │ end_user_id 追蹤
    ┌────────────┼────────────┐
    ▼            ▼            ▼
  張偉         李華         王強
  (個人 Key)   (個人 Key)   (個人 Key)
  budget: $50  budget: $50  budget: $50
```

**實施步驟**：

1. 建立共享 Team Key，設定部門總預算（如 $2,000/月）
2. 為每個使用者建立個人 Key，設定個人預算（如 $50/月）
3. 前端或後端服務在發送請求時使用個人 Key，但同時記錄 `user` 欄位
4. 透過 Team Key 的 end_user_id 進行用量追蹤和成本分配

| 優點 | 缺點 |
|------|------|
| ✅ 兼具追蹤和預算控制 | ❌ 需要維護兩層 Key |
| ✅ Team 層級有總預算，個人層級有上限 | ❌ 配置較複雜 |
| ✅ 可以進行部門成本分配 | |

**適合場景**：
- 公司同時需要追蹤用量和嚴格預算控制
- 需要進行部門成本分配
- 有專門的 IT 團隊管理

---

## 📈 實作建議

### Step 1：在 config.yaml 中啟用相關功能

```yaml
general_settings:
  master_key: sk-master-key-xxx
  store_model_in_db: true

  # 啟用 spend tracking
  litellm_settings:
    # 允許追蹤 end_user
    end_user_tracking: true

    # 為沒有個人預算的使用者設定預設預算
    max_end_user_budget_id: "default-end-user-budget"

litellm_settings:
  # 全域預算
  max_budget: 5000
  budget_duration: "30d"
```

### Step 2：建立部門共用 Key

```bash
# 建立技術部共用 Key
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer sk-master-key-xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "eng-team",
    "models": ["gpt-4o", "gpt-4o-mini", "claude-sonnet-4"],
    "max_budget": 2000,
    "budget_duration": "30d",
    "duration": "30d",
    "user_email": "engineering@company.com",
    "metadata": {
      "department": "engineering",
      "key_type": "department-shared"
    }
  }'
```

### Step 3：建立個人 Key（可選，混合方案用）

```bash
# 為每個使用者建立個人 Key
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer sk-master-key-xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "eng-team",
    "user_email": "zhang.wei@company.com",
    "models": ["gpt-4o", "gpt-4o-mini", "claude-sonnet-4"],
    "max_budget": 50,
    "budget_duration": "30d",
    "duration": "30d",
    "rpm_limit": 50,
    "metadata": {
      "name": "張偉",
      "department": "engineering",
      "role": "senior-developer"
    }
  }'
```

### Step 4：前端/後端服務傳遞 user 欄位

```python
# 後端服務範例
@app.post("/chat")
async def chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    response = llm_client.chat.completions.create(
        model=request.model,
        messages=request.messages,
        user=current_user.email,  # ← 必須傳遞！
        api_key=SHARED_TEAM_KEY
    )
    return response
```

### Step 5：定期審查用量

```bash
# 每週查詢部門用量排名
curl -X GET "http://localhost:4000/spend/users?start_time=2026-08-01&end_time=2026-08-07" \
  -H "Authorization: Bearer sk-master-key-xxx" | jq '.[] | {user_id, total_spend, total_requests}'
```

---

## ⚡ 已知問題與解決

### Issue #29142：end_user_max_budget 繼承 Bug

**問題**：當使用共享 Key 時，後一個使用者的預算限制可能會繼承前一個使用者的設定（緩存遺留）。

```
請求順序：
1. 張偉請求 → 預算檢查通過 ✓
2. 李華請求 → 預算檢查通過 ✓
3. 王強請求 → 預算檢查錯誤：使用了張偉的預算 ✗
```

**目前解決方案**：
- 定期重啟 LiteLLM Proxy 以清除緩存
- 或使用個人 Key 代替共享 Key
- 關注官方修復進度

**GitHub Issue**：https://github.com/BerriAI/litellm/issues/29142

---

## ✅ 最佳實踐總結

| 實踐 | 說明 |
|------|------|
| **始終設定 `user` 欄位** | 每個請求都必須包含 `user` 欄位，否則無法區分個人 |
| **使用一致的 user_id 格式** | 建議使用電子郵件地址，如 `zhang.wei@company.com` |
| **定期審查用量** | 透過 Admin UI 或 API 定期檢查每個人的用量 |
| **設定預算警報** | 配置預算警報，當個人用量超過預設閾值時通知 |
| **考慮個人 Key** | 如果需要嚴格的預算控制，為每個使用者建立個人 Key |
| **後端服務統一管理** | 確保所有後端服務在呼叫時都傳遞正確的 user 欄位 |

---

## 📋 決策流程

```
需要追蹤個人用量？
│
├─ 是 → 需要個人預算控制？
│        │
│        ├─ 是 → 使用方案 B（個人 Key）或方案 C（混合方案）
│        │
│        └─ 否 → 使用方案 A（共用 Key + end_user_id）
│
└─ 否 → 不需要追蹤個人用量，共用 Key 即可
```

---

## 相關資源

- **LiteLLM Virtual Keys 文檔**：https://docs.litellm.ai/docs/proxy/virtual_keys
- **LiteLLM Spend Tracking 文檔**：https://docs.litellm.ai/docs/proxy/cost_tracking
- **LiteLLM End Users 文檔**：https://docs.litellm.ai/docs/proxy/customers
- **GitHub Issue #29142**：https://github.com/BerriAI/litellm/issues/29142

---

**最後更新**: 2026-08-03  
**作者**: Hermes Agent 整理  
**原始專案**: [LiteLLM](https://github.com/BerriAI/litellm)
