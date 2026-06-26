# Cartographer 教學樣本（examples/）

> 這些是用 Cartographer 跑出來的真實示範產物，**全為測試假資料**，用來示範流程與品質標準。非真實專案、非模板。
> 空白模板與標準範例請看 `../templates/`。

| 檔案 | 示範什麼 | lint |
|---|---|---|
| `example-bad-prd.md` | ❌ **反面教材**：新手常見爛 PRD（無編號、形容詞、碰價值卻零資安、無範圍）。用來示範審查模式抓問題 | 0 需求／假 PASS（凸顯 lint 盲區） |
| `example-points-after-review.md` | ✅ 由 `example-bad-prd.md` **審查→重生成**的合格版（會員集點與兌換，🔴 重級 14 節） | 11 需求／0 阻斷／PASS |
| `example-repair-app-full.md` | ✅ 互動逐節走完的完整 PRD（社區報修 App，🔴 重級 14 節，含 §14 可追溯矩陣） | 8 需求／0 阻斷／PASS |
| `example-quickpay-testrun.md` | ✅ 端到端壓測產物（QuickPay 一頁式行動結帳，🔴 重級） | 20 需求／0 阻斷／PASS |

## 怎麼用這些樣本

- **學「合格長什麼樣」**：讀 `example-points-after-review.md` 或 `example-repair-app-full.md`。
- **學「爛在哪、怎麼修」**：對照 `example-bad-prd.md`（前）與 `example-points-after-review.md`（後）。
- **驗證 lint**：
  ```
  # Windows 用 py；macOS/Linux 用 python3（直接打 python 在 Windows 可能是 Store stub 會啞掉）
  py ../scripts/prd_lint.py example-points-after-review.md   # PASS
  py ../scripts/prd_lint.py example-bad-prd.md               # 凸顯無編號=lint 失明
  ```
