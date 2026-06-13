<!-- LANG SWITCH -->

[English](./README.md) | **繁體中文**

# Cartographer — 把想法畫成 PRD 的製圖師

> 一個 Claude Code skill，扮演「想法與規格之間的製圖師」——逐節訪談、逐節成稿，把模糊想法畫成一份可驗收、可追溯、可交棒的**軟體 PRD**。配 [Sentinel](https://github.com/RayLi-Git/sentinel) 思考 OS 與 [Compass](https://github.com/RayLi-Git/compass) 紀律羅盤形成完整工具鏈。

![status](https://img.shields.io/badge/status-active-success)
![license](https://img.shields.io/badge/license-MIT-blue)
![companion](https://img.shields.io/badge/companion-Sentinel%20%2B%20Compass-purple)

> 15 模組 · 中英雙語 · 附教學範例。英文版見 [cartographer-en/](./cartographer-en/)；涵蓋邊界見 [docs/SCOPE.zh-TW.md](./docs/SCOPE.zh-TW.md)。

---

## 工具鏈定位

> **Cartographer 畫出地圖（生 PRD）→ Compass 照圖施工（不偏航）→ Sentinel 全程站哨（怎麼想、防資安僥倖）。**

Cartographer 補的是 Compass 的上游缺口：Compass 假設 PRD 已存在，Cartographer 負責**把腦中想法逼成那份 PRD**。

## 它解決的問題

軟體 PRD 最常見的失敗模式：

1. **不可驗收** — 寫「結帳要快、要好用」，工程無法判斷做完沒
2. **漏掉非功能與資安** — 只寫功能，效能/隱私/法遵整段不存在（連 Apple 的 AirPods PRD 都犯：收健康資料卻零隱私）
3. **無來源的孤兒需求** — 不知道為哪個使用者、哪個目標而做
4. **範圍無限膨脹** — 沒寫「不做的事」

Cartographer 用**逐節訪談 + 品質閘 + 機械化 lint** 防住這些。

## 核心信念

1. **不是需求，除非它「原子＋編號＋優先級＋可驗收＋可追溯」**
2. **不可量測的形容詞是 PRD 的毒**（快/好/友善/無縫 → 翻成數字）
3. **非功能需求與資安要被強迫面對**
4. **誠實列開放問題 > 假裝想清楚**
5. **每條需求都要能追回它的來源**

## 15 個模組

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

## 怎麼用

1. 安裝（見 [docs/INSTALL.zh-TW.md](./docs/INSTALL.zh-TW.md)）。
2. 跟 Claude 說「幫我寫 PRD」或「幫我審查這份 PRD」。
3. Cartographer 逐節問你、逐節成稿，每節停下等你確認。
4. 完成後跑 `python scripts/prd_lint.py <你的PRD.md>`，過關即可交棒 Compass。

## 設計藍本

以外流的 Apple AirPods Pro 硬體 PRD 為骨架藍本，移植其優點（原子化編號需求、優先級、可量測、persona 驅動、開放問題、名詞表、競品分析），並修掉它的缺點（補上成功指標量測、假設/風險分家、資安升格、強制驗收條件、需求依賴、可追溯矩陣）。詳見 [docs/DESIGN.zh-TW.md](./docs/DESIGN.zh-TW.md)。

## 檔案結構

```
cartographer-main/
├── SKILL.md                     # 入口（精簡路由）
├── references/00..14/_index.md  # 15 模組細則
├── templates/
│   ├── prd-blank.md.template    # 空白模板
│   └── prd-filled-example.md    # 電商結帳填好範例
├── scripts/prd_lint.py          # PRD 機械化健檢
├── docs/{DESIGN,INSTALL,SCOPE}.zh-TW.md
└── cartographer-en/             # 英文鏡像
```

## 授權

MIT — 見 [LICENSE](./LICENSE)。
