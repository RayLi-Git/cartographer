# §14 交棒 compass ★｜把地圖交給施工隊

> 這是工具鏈的接縫。PRD 畫完，要能**無縫變成 Compass 能吃的 `prd-checklist.md`**，並附一張**可追溯矩陣**——這是 Cartographer 超越 AirPods 範本的地方（範本有零件、沒連線）。矩陣同時是 compass 反向審計的輸入。

---

## 引導問題（PRD 完成後）

1. 所有 FR/NFR 都編號、有 AC、有優先級了嗎？（跑 `prd_lint.py` 確認）
2. 每條需求都追得回 persona/目標嗎？有沒有**孤兒需求**？
3. 依賴排序（§12）整理好了嗎？
4. 要交給 compass 的 checklist 與矩陣產出了嗎？

---

## 可追溯矩陣（FR ↔ persona ↔ 目標 ↔ AC ↔ 里程碑）

| 需求 | 來源 persona/場景 | 服務目標 | AC 摘要 | 優先級 | 里程碑 |
|---|---|---|---|---|---|
| FR-PAY-01 | P1 怡君 / 場景#1 | O-2 降棄單 | 建立付款意圖回 200 | P0 | M1 |
| FR-PAY-03 | 場景#2 中斷 | O-1 成功率 | 逾時轉 pending+重試 | P0 | M1 |
| NFR-PRIV-01 | 法遵 | 護欄 | 查無明文卡號 | P0 | M1 |

**孤兒檢查**：
- 沒有來源的需求 → 回 §05 補，或刪、或進 §11。
- 沒有任何需求服務的目標 → §02 目標落空，補需求或砍目標。

---

## 轉成 Compass 的 prd-checklist.md

把每條 FR/NFR 展開成 compass 的勾稽項（對應 compass `templates/prd-checklist.md.template`）：

```markdown
## PRD Checklist（交棒 compass）
- [ ] FR-PAY-01 建立付款意圖 ｜P0｜AC: 回200含paymentId｜驗收方式: 整合測試
- [ ] FR-PAY-03 逾時轉 pending ｜P0｜AC: 第31秒=pending,5分內≤3重試｜驗收方式: 整合測試
- [ ] NFR-SEC-01 付款 API 授權 ｜P0｜AC: 缺token回401｜驗收方式: 安全測試(test-first)
- [ ] NFR-PRIV-01 不存明文卡號 ｜P0｜AC: 全文掃描無16碼｜驗收方式: 掃描腳本
```

> 交棒後 compass 接手：DoR 健檢 → 依序實作 → 完成-比對-修正 → DoD。Cartographer 的可追溯矩陣 = compass 反向審計（PRD↔code）的左半邊。

---

## 常見陷阱

- **交棒前沒跑 lint**：把不合格 PRD 丟給 compass → 施工期才發現缺 AC。先 `prd_lint.py` 過關。
- **矩陣有孤兒**：需求無來源、目標無需求 → 一定要清乾淨再交。
- **checklist 漏了驗收方式**：compass 需要知道每條怎麼驗（單元/整合/安全/手動）。
- **依賴沒帶過去**：compass 排不出實作順序。§12 依賴圖一起交。

---

## 品質閘（交棒前最後一關）

- ✅ `prd_lint.py` exit code 0
- ✅ 可追溯矩陣無孤兒需求、無落空目標
- ✅ checklist 每條含 優先級 + AC + 驗收方式
- ✅ §12 依賴排序一併交付

---

## 格式片段

```markdown
## 14. 交棒 compass

### 可追溯矩陣
| 需求 | 來源 | 目標 | AC摘要 | 優先級 | 里程碑 |

### Compass Checklist
- [ ] FR-xxx ... ｜Px｜AC: ...｜驗收方式: ...
```
