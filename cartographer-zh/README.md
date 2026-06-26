[English](../README.md) | **繁體中文**

# Cartographer — 把想法畫成 PRD 的製圖師

> 一個 Claude Code skill，把模糊想法逼成一份扎實的軟體 PRD——**逐節訪談、逐節成稿，直到每條需求都可驗收、可追溯、可交棒。** 四件式工具鏈的一環：**Cartographer 畫地圖 → Compass 照圖走 → Sentinel 站哨 → Lookout 瞭望。**

![status](https://img.shields.io/badge/status-active-success)
![license](https://img.shields.io/badge/license-MIT-blue)
![toolchain](https://img.shields.io/badge/toolchain-Cartographer·Compass·Sentinel·Lookout-purple)

---

## 它解決的問題

一份軟體 PRD，在還沒寫半行 code 前最常見的失敗模式：

1. **不可驗收** — 寫「結帳要快、要好用」，工程無從判斷做完了沒。
2. **漏掉非功能與資安** — 只寫功能，效能/隱私/法遵整段不存在（連 Apple 外流的 AirPods PRD 都犯：收健康資料卻零隱私）。
3. **無來源的孤兒需求** — 不知道為哪個使用者、哪個目標而做。
4. **範圍無限膨脹** — 從沒寫下「不做的事」。

Cartographer 用**逐節訪談 + 品質閘 + 機械化 lint**（靠 exit code，不靠意志力）把這四點全擋住。

## 運作方式

**五個核心信念：**

1. **不是需求，除非它「原子＋編號＋優先級＋可驗收＋可追溯」。**
2. **不可量測的形容詞是毒** — 快/好/友善/無縫 都要翻成數字。
3. **非功能需求與資安要被強迫面對，不可跳過。**
4. **誠實列開放問題 > 假裝想清楚。**
5. **每條需求都要能追回它的來源。**

**15 個主題模組**（按需從 `references/` 載入）：

```
00 定位與模式        08 資安·隱私·法遵 ★（深掛 Sentinel）
01 背景與問題        09 資料與整合
02 目標與成功指標     10 範圍邊界
03 假設·約束·風險     11 開放問題
04 利害關係人+RACI    12 里程碑與發布切片
05 使用者故事與旅程   13 名詞表與競品分析
06 功能需求 ★        14 交棒 compass ★
07 非功能需求
```

每個模組是一個 `references/NN_*/_index.md`，五段式：引導問題 → 好/壞對照 → 陷阱 → 品質閘 → 格式片段。

## 快速開始

```bash
# 安裝為使用者層級 skill（所有專案生效）
mkdir -p ~/.claude/skills/cartographer
cp -r SKILL.md references scripts templates ~/.claude/skills/cartographer/

# 驗證
ls ~/.claude/skills/cartographer   # → SKILL.md  references  scripts  templates
```

接著跟 Claude 說 **「幫我寫一份 PRD」**（或「幫我審查這份 PRD」）。Cartographer 逐節問你、每節停下等你確認；完成後跑 `python scripts/prd_lint.py <你的PRD.md>`，過關即可交棒 Compass。完整指南見 **[docs/INSTALL.md](./docs/INSTALL.md)**。

## 工具鏈

Cartographer 是四件式工具鏈裡的**畫地圖**段——第一棒，每一件盯不同的事：

| Skill | 角色 | 盯什麼 |
|---|---|---|
| **Cartographer** | 畫地圖 | 把模糊想法逼成一份扎實的 PRD |
| [Compass](https://github.com/RayLi-Git/compass) | 照圖走 | 你有照 PRD 走嗎？（照規格蓋、不偏航） |
| [Sentinel](https://github.com/RayLi-Git/sentinel) | 站哨 | 你怎麼想（淺層 vs 深層、症狀 vs 根因） |
| [Lookout](https://github.com/RayLi-Git/lookout) | 在桅杆瞭望 | 獨立 context 的 code review |

**Cartographer 畫地圖 → Compass 照圖走 → Sentinel 站哨 → Lookout 瞭望。** Cartographer 補的是 Compass 的上游缺口：Compass 假設 PRD 已存在，而 Cartographer 負責把腦中想法逼成那份 PRD。完整分工見 [docs/SCOPE.md](./docs/SCOPE.md)。

## 目錄結構

```
cartographer/
├── SKILL.md            skill 入口（Claude Code 載入）
├── references/         15 個模組，按需載入
├── scripts/            prd_lint.py — PRD 機械化健檢
├── templates/          空白 PRD 模板 + 填好的範例
├── examples/           四份真實示範 PRD（虛構資料）—— 壞例/審前/審後、兩份完整走查
├── docs/               DESIGN · INSTALL · SCOPE
└── cartographer-zh/    繁體中文鏡像
```

## 文件

- **[DESIGN](./docs/DESIGN.md)** — 設計理念、關鍵決策與取捨
- **[INSTALL](./docs/INSTALL.md)** — 完整安裝（skill + lint 腳本 + 範本）與驗證
- **[SCOPE](./docs/SCOPE.md)** — 涵蓋什麼、不涵蓋什麼、以及工具鏈分工

本 skill 附有 [`examples/`](./examples/) 裡的**示範 PRD**——一份新手寫的壞 PRD、它審查後重生的合格版、以及兩份端到端完整走查——讓你動筆前先看到品質標準。

## 授權

[MIT](../LICENSE) © Ray_Li

> 本專案是一個作品集，探索「如何把『將模糊想法逼成可驗收 PRD』的紀律，編碼成 AI 寫程式的搭檔」。同一工具鏈的 [Compass](https://github.com/RayLi-Git/compass) 探索「如何讓實作忠於那份 PRD」。
