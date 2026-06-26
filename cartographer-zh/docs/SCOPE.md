[English](../../docs/SCOPE.md) | **繁體中文**

# 範圍邊界

> 一個 skill 的價值不只在「它能做什麼」，更在「它清楚說自己不做什麼」。本文件明文列出 Cartographer 的涵蓋邊界，避免使用者誤用或期待錯位。

---

## 涵蓋的情境

**Cartographer 適用：**

| 範疇 | 說明 |
|---|---|
| **從零起草軟體 PRD** | 逐節訪談把模糊想法變成合格 PRD（15 模組） |
| **審查 / 補強既有 PRD** | 把品質閘反過來當體檢清單，找缺漏並給修補建議 |
| **需求品質強制** | 原子＋編號＋優先級＋可驗收＋可追溯；`prd_lint` 機械化把關 |
| **非功能 / 資安 / 隱私** | 強迫面對效能、SLA、可觀測、無障礙、i18n、資料分類、法遵 |
| **可追溯矩陣** | FR ↔ persona ↔ 目標 ↔ AC ↔ 里程碑 |
| **交棒 Compass** | 轉成 Compass 能吃的 checklist 與反向審計輸入 |

**三級制縮放** — Cartographer 依任務份量調整訪談規模：

- 🟢 **輕** — 小改版微調 → 約 4 節（00 / 01 / 06 / 11）。
- 🟡 **中** — 一個功能模組 → 約 9 節。
- 🔴 **重** — 新產品、含金流 / PII / 權限 → 00–14 全程；§06 驗收條件與 §08 資安不可跳。

本 skill 附有 [`examples/`](../examples/) 裡的**示範 PRD**——一份新手寫的壞 PRD、它審查後重生的合格版、以及兩份端到端完整走查——全是虛構資料，讓你動筆前先研究品質標準。

---

## 不涵蓋的情境

明文列出範圍外，避免誤用。

**不涵蓋的工作類型（交給誰）：**

| 不做 | 交給 |
|---|---|
| 實作 PRD、照規格施工、不偏航 | **[Compass](https://github.com/RayLi-Git/compass)** |
| 怎麼想、根因診斷、資安思考習慣 | **[Sentinel](https://github.com/RayLi-Git/sentinel)** |
| 單元落地後的獨立 context code review | **[Lookout](https://github.com/RayLi-Git/lookout)** |
| 硬體 PRD（機構、電性、製造、法規測試） | 本 skill 專注軟體 |
| 商業計畫書 / 財務模型 / 募資簡報 | 非 PRD 範疇 |
| 詳細 UI 設計稿 / wireframe / 視覺規範 | 設計工具；PRD 只描述行為與狀態 |
| 專案管理排程細節（甘特圖、工時） | PM 工具；PRD 只到里程碑與切片 |

---

## 邊界與常見誤解

這些邊界是刻意畫的，不是缺陷。目前的 Cartographer（15 模組全 + 可跑 lint + 空白/填好範本 + 示範 PRD + 中英雙語）完整且可用。

- **「它會一次幫我把 PRD 寫完。」** 不會——Cartographer 逐節訪談、每節停下等確認。一次成稿*看似*完整、實則多半臆測；那些停下的點正是品質的來源。
- **「lint 保證好 PRD。」** lint 擋得住格式錯的需求（缺編號/優先級/AC/來源、不可量測形容詞），卻擋不住「根本沒編號的需求」——無編號 PRD 會得到假 PASS。這個盲點正是人驅動審查模式存在的理由。
- **「它假設藍本完美。」** 正好相反——Cartographer 的藍本（外流的 AirPods PRD）有八個具體缺點，修掉它們是設計的一半（見 [DESIGN](./DESIGN.md)）。
- **「它也設計 UI。」** 不——PRD 描述的是*行為與狀態*（空 / 載入 / 錯誤 / 離線），不是像素。wireframe 與視覺規範屬於設計工具。
- **「藍本是硬體，所以它是硬體 PRD 工具。」** 不——移植的是*結構*，但 Cartographer 為軟體調校。機構 / 電性 / 製造規格不在範圍。

---

## 工具鏈分工

Cartographer 是四件式工具鏈裡的**畫地圖**段——第一棒，每一件盯不同的事：

| Skill | 角色 | 盯什麼 |
|---|---|---|
| **Cartographer** | 畫地圖 | 把模糊想法逼成一份扎實的 PRD |
| [Compass](https://github.com/RayLi-Git/compass) | 照圖走 | 你有照 PRD 走嗎？（照規格蓋、不偏航） |
| [Sentinel](https://github.com/RayLi-Git/sentinel) | 站哨 | 你怎麼想（淺層 vs 深層、症狀 vs 根因） |
| [Lookout](https://github.com/RayLi-Git/lookout) | 在桅杆瞭望 | 獨立 context 的 code review |

**Cartographer 畫地圖 → Compass 照圖走 → Sentinel 站哨 → Lookout 瞭望。**

Cartographer 與 Compass 是最緊的一對——同一份產物上前後相接的兩段：

| 面向 | Cartographer | Compass |
|---|---|---|
| 主要產出 / 盯什麼 | 「**PRD**」本身 | 你與「**PRD**」的關係 |
| 核心信念 | 需求若不可驗收、不可追溯就不算數 | PRD 是合約，完成就是完成 |
| 核心觸發問題 | 「這個想法夠成一份可蓋的規格了嗎？」 | 「我有照 PRD 走嗎？」 |
| 關鍵動作 | 分節訪談、品質閘、prd_lint、可追溯矩陣 | DoR、追蹤文件、PRD 衝突處置、工具強制 |
| 適用範圍 | 你有想法但還沒有可用規格 | 你有 PRD、要照它蓋 |

**工具鏈典型交棒：**

1. **有想法但混亂** → [Sentinel](https://github.com/RayLi-Git/sentinel) 幫你想清楚 → Cartographer 開始分節訪談。
2. **§08 資安** → Cartographer 直接引用 Sentinel 的紅旗清單，讓資安在 PRD 階段就被面對，而不是上線後。
3. **PRD 過 lint** → §14 交棒 → [Compass](https://github.com/RayLi-Git/compass) 接手 DoR / 實作 / DoD。
4. **某個單元落地** → [Lookout](https://github.com/RayLi-Git/lookout) 做一次獨立 context 的審查。

---

## 回饋與貢獻

Cartographer 是個人作品集，但歡迎透過 GitHub Issues 貢獻：

- 範圍描述不準確的地方。
- 你遇到、但本 skill 還抓不到的 PRD 失敗模式（或不該抓的）。
- 工具鏈分工上的盲點。

---

> **記住**：Cartographer 不是萬靈丹，是**特定情境下精準的工具**。當你有想法但還沒有可用規格時用它，能省下模糊 PRD 帶來的返工；當規格已存在時，你該改用 Compass。先讀這份文件，再決定要不要用。
