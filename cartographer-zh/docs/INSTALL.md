[English](../../docs/INSTALL.md) | **繁體中文**

# 安裝

> Cartographer 有三個部分：**skill 本體**（`SKILL.md` + `references/`，按需載入的 PRD 訪談知識庫）、**lint 腳本**（`scripts/prd_lint.py`，PRD 機械化健檢）、**範本**（`templates/`，空白 PRD 加一份填好的範例）。skill 本體必裝；連同 lint 與範本一起裝，體驗最完整。

---

## 前置需求

- 已安裝 [Claude Code](https://docs.claude.com)。
- 要跑 lint（`scripts/prd_lint.py`）：**Python 3.7+**（只用標準庫——它用到 `sys.stdout.reconfigure`，所以在繁中 Windows 主控台無需額外設定；腳本已強制 UTF-8 輸出）。
- 建議與工具鏈同門一起裝——Cartographer 畫地圖、[Compass](https://github.com/RayLi-Git/compass) 照圖走、[Sentinel](https://github.com/RayLi-Git/sentinel) 站哨、[Lookout](https://github.com/RayLi-Git/lookout) 瞭望。

---

## 安裝步驟

一個 skill 的本質就是「一個含 `SKILL.md` 的資料夾」。安裝＝把它放進 Claude Code 會掃描的 skills 目錄。

### 1. 安裝 skill 本體（必裝）

**方式 A — 全域安裝（推薦，所有專案生效）：**

```bash
mkdir -p ~/.claude/skills/cartographer

# 若你拿到的是打包好的 .skill / .zip
unzip cartographer.skill -d ~/.claude/skills/cartographer

# 或若你 clone 了這個 repo，直接複製內容
cp -r SKILL.md references ~/.claude/skills/cartographer/
```

**方式 B — 專案層級安裝（只在單一專案生效）：**

```bash
mkdir -p .claude/skills/cartographer
cp -r SKILL.md references .claude/skills/cartographer/
```

### 2.（推薦）安裝 lint 腳本與範本

lint 是需求品質閘的可跑形態；範本是你自己寫 PRD 的起點。把它們放進**你正在做的專案**（不是 skills 目錄）。

```bash
# 在你的專案根目錄
cp -r /path/to/cartographer/scripts ./scripts
cp -r /path/to/cartographer/templates ./templates

# 跑 PRD 健檢（exit 0 = PASS，非零 = 有阻斷項）
# Windows 用 `py`；macOS/Linux 用 `python3`
#（Windows 直接打 `python` 可能打到 Store stub、靜默不動作）
py scripts/prd_lint.py your-PRD.md
```

`templates/prd-blank.md.template` 是空白骨架；`templates/prd-filled-example.md` 是填好的完整範例可比對。本 skill 另附 `examples/` 下的示範 PRD（見 [`examples/README.md`](../examples/README.md)）。

### 3. 常駐路由層（選用）

想要工具鏈的常駐路由（`~/.claude/CLAUDE.md`，讓 Claude 自動按任務路由到對的 skill）？用 [Sentinel 的 `CLAUDE.md.example`](https://github.com/RayLi-Git/sentinel/blob/main/CLAUDE.md.example)（已支援 compass / cartographer 選用），複製到 `~/.claude/CLAUDE.md` 即可。整條工具鏈只需這**一份**共用常駐檔。

---

## 驗證

```bash
ls ~/.claude/skills/cartographer
# 必須看到：SKILL.md  references

ls ~/.claude/skills/cartographer/references
# 應看到 15 個模組資料夾：00_positioning … 14_handoff_compass
```

> ⚠️ 常見錯誤：解壓縮後多了一層巢狀 `cartographer/cartographer/SKILL.md`。
> `SKILL.md` 必須**直接**位於 `~/.claude/skills/cartographer/` 底下。若多一層，把裡層內容往上移。

**確認真的會觸發。** 開一個*新的* Claude Code session（只有全新開啟才會掃到新 skill），然後丟這個測試：

> 「幫我寫一份 PRD。」

Cartographer 應從 **§00 定位** 開始訪談，並在進下一節前停下等你確認。如果它沒問就整份倒出一份 PRD、或從沒提到定位/分節，表示 skill 沒被掃到——回去檢查安裝結構。

**PRD 存在哪。** Cartographer 把 PRD 起草成你**正在做的專案目錄**裡的一份 markdown 檔——沒有獨立的追蹤狀態。當草稿過 lint，§14 會把它轉成 Compass 能吃的 checklist，進入施工段。

---

## 疑難排解

| 症狀 | 可能原因 | 解法 |
|---|---|---|
| skill 沒觸發 | 沒開新 session | 重啟 Claude Code |
| 找不到 references 檔 | 多了一層資料夾巢狀 | 確認 `SKILL.md` 直接在 `cartographer/` 底下 |
| `prd_lint.py` 沒反應 / 無輸出 | `python` 打到 Windows Store stub | 改用 `py`（Windows）或 `python3`（macOS/Linux） |
| lint 對一份明顯很爛的 PRD 報 `PASS` | 那份 PRD 零個編號需求（lint 盲點） | 用 skill 的審查模式——訪談會抓到 lint 抓不到的「沒編號需求」 |
| 繁中 Windows 主控台 `UnicodeEncodeError` | 很舊、無 `reconfigure` 的 Python | 升到 Python 3.7+ |

### 與工具鏈搭配

Cartographer 是工具鏈的上游。典型交棒：

- **起草之前**：有想法但混亂 → [Sentinel](https://github.com/RayLi-Git/sentinel) 幫你想清楚 → Cartographer 開始訪談。
- **§08 資安**：Cartographer 直接引用 Sentinel 的紅旗清單與資安思考習慣。
- **起草之後**：PRD 過 lint → §14 交棒 → [Compass](https://github.com/RayLi-Git/compass) 接手 DoR / 實作 / DoD。某個單元落地後，[Lookout](https://github.com/RayLi-Git/lookout) 做一次獨立 context 的審查。

### 解除安裝

```bash
rm -rf ~/.claude/skills/cartographer
# 專案裡的 scripts/ templates/ 自行視需要移除
```
