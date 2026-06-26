# §09 資料與整合｜資料模型、契約、依賴

> AirPods 是硬體，這節幾乎空白（只在 Introduction 散提 H1 晶片、BT 5.2）。軟體則相反：**資料模型、API/事件契約、平台支援矩陣、第三方依賴**是實作的骨架，也是 compass 施工的介面。資料分類與 §08 互通。

---

## 引導問題

1. 核心**資料實體**有哪些？關鍵欄位、關聯、生命週期？
2. 對外/對內**介面契約**：哪些 API/事件？輸入輸出 schema、錯誤碼、冪等性？
3. 要支援哪些**平台**？（OS/瀏覽器/裝置/最低版本）
4. 依賴哪些**第三方**？（金流、簡訊、地圖…）它們的限制與失效行為？
5. 資料**從哪來、往哪去**？跨系統流向與一致性要求？

---

## 資料模型（關鍵實體 + 生命週期）

```
Order: { id, userId, items[], amount, currency, status, createdAt }
  status: cart → pending_payment → paid → fulfilled | failed | refunded
Payment: { id, orderId, provider, token, last4, status, idempotencyKey }
```
> 每個 status 轉移都應該對得上 §06 的某條功能需求（含負向）。

---

## 介面契約（讓 compass 能照著蓋）

```
POST /api/checkout
  req:  { orderId, paymentMethodId, idempotencyKey }
  resp: 200 { paymentId, status } | 402 付款失敗 | 409 重複 | 401 未授權
  冪等：相同 idempotencyKey 回首次結果，不重複扣款
事件：checkout_started / checkout_succeeded / checkout_failed（供 §02 量測、§07 可觀測）
```

---

## 平台支援矩陣

| 平台 | 最低版本 | 備註 |
|---|---|---|
| iOS Safari | 15+ | Apple Pay |
| Android Chrome | 最近 2 版 | Google Pay |
| Desktop | Chrome/Edge/Firefox 最近 2 版 | — |

---

## 第三方依賴

| 依賴 | 用途 | 限制 | 失效時行為 |
|---|---|---|---|
| 金流商 X | 信用卡授權 | 50 req/s；PCI 規範 | 降級為稍後通知（連 §03 R-1、§07 SLA） |
| 簡訊商 | OTP/通知 | 配額 | 改 email 備援 |

---

## 常見陷阱

- **資料模型缺生命週期**：只列欄位不列 status 轉移 → §06 負向需求無依據。
- **契約沒寫錯誤碼/冪等**：只寫 happy response → 實作各自詮釋失敗行為。
- **平台矩陣含糊**：「支援手機」→ 哪些 OS/版本？影響測試與 §07。
- **第三方沒寫失效行為**：依賴一定會掛，沒寫降級＝上線當機。

---

## 品質閘（過了才進 §10）

- ✅ 關鍵實體有欄位 + 關聯 + **生命週期狀態**
- ✅ 對外介面有 schema + 錯誤碼 + 冪等性
- ✅ 平台支援矩陣具體到版本
- ✅ 每個第三方依賴有限制 + **失效時行為**（連回 §03 風險、§07 SLA）
- ✅ 涉及 PII/敏感的資料流已與 §08 分類對齊

---

## 格式片段

```markdown
## 9. 資料與整合

### 9.1 資料模型
<實體：欄位、關聯、status 生命週期>

### 9.2 介面契約
<API：路徑、req/resp schema、錯誤碼、冪等；事件清單>

### 9.3 平台支援矩陣
| 平台 | 最低版本 | 備註 |

### 9.4 第三方依賴
| 依賴 | 用途 | 限制 | 失效時行為 |
```
