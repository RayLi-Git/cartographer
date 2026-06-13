# Cartographer 安裝指南

> Cartographer 是一個 Claude Code skill。安裝＝把資料夾放到 Claude Code 會掃描的 skills 目錄。

---

## 方式一：個人 skills 目錄（最簡單）

把 `cartographer-main/` 整個資料夾複製到你的個人 skills 目錄，並改名為 `cartographer`：

```
# macOS / Linux
cp -r cartographer-main ~/.claude/skills/cartographer

# Windows (PowerShell)
Copy-Item -Recurse cartographer-main "$env:USERPROFILE\.claude\skills\cartographer"
```

英文版同理（放成另一個 skill）：

```
cp -r cartographer-main/cartographer-en ~/.claude/skills/cartographer-en
```

> Claude Code 會自動掃描 `~/.claude/skills/` 下含 `SKILL.md` 的子資料夾，載入 name + description。

## 方式二：專案內 skills 目錄

放到專案的 `.claude/skills/cartographer/`，只在該專案可用。

## 驗證安裝

1. 重啟 Claude Code（或開新 session）。
2. 說「幫我寫一份 PRD」。
3. 應觸發 Cartographer，從 §00 定位開始問你。

## 需求

- `prd_lint.py` 需要 Python 3.7+（用到 `sys.stdout.reconfigure`）。
- Windows 主控台無需額外設定，script 已內建 UTF-8 輸出。

## 目錄結構

```
cartographer/
├── SKILL.md
├── references/00..14/_index.md
├── templates/{prd-blank.md.template, prd-filled-example.md}
├── scripts/prd_lint.py
└── docs/{DESIGN,INSTALL,SCOPE}.zh-TW.md
```

## 搭配 Sentinel / Compass

三者建議一起裝，形成完整工具鏈：

```
~/.claude/skills/
├── sentinel/
├── compass/
└── cartographer/
```

### 常駐層（選用）

想要三件式的常駐分工（`~/.claude/CLAUDE.md`，讓 Claude 自動按任務路由到對的 skill）？用 [sentinel 的 `CLAUDE.md.example`](https://github.com/RayLi-Git/sentinel/blob/main/CLAUDE.md.example)（已支援 compass / cartographer 選用），複製到 `~/.claude/CLAUDE.md` 即可。整條工具鏈只需這**一份**共用常駐檔。
