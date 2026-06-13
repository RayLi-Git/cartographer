#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prd_lint.py — Cartographer 的 PRD 機械化健檢（靠 exit code 不靠紀律）

檢查（阻斷項，exit 1）：
  1. 需求行（FR-/NFR- 開頭）缺優先級 P0–P3
  2. 需求行缺「AC:」驗收條件
  3. 需求行缺「來源:」追溯
  4. 需求行內含不可量測形容詞（快速/友善/直覺/無縫/盡量/intuitive/seamless...）
  5. 需求編號重複（同一個 FR-/NFR- ID 出現多次）

提醒（非阻斷，警告）：
  6. 非需求行卻出現 "shall" → 疑似未編號需求
  7. 「依賴:」指向的 FR-/NFR- 在本文件不存在 → 懸空依賴

用法：
  python prd_lint.py <PRD.md>
  exit 0 = 通過（可交棒 compass）；exit 1 = 有阻斷項

v2：移除散文形容詞誤報；新增重複編號（阻斷）與懸空依賴（警告）結構檢查。
"""

import sys
import re

# Windows 主控台預設 cp950，強制 UTF-8 輸出避免中文/emoji 亂碼或崩潰
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# 需求行：FR-PAY-01: / NFR-A11Y-01: （模組碼允許含數字，如 A11Y、I18N）
REQ_RE = re.compile(r'^(FR|NFR)-[A-Z0-9]+-\d+:')
PRIORITY_RE = re.compile(r'\bP[0-3]\b')
SEG_SPLIT = re.compile(r'[｜|]')                       # 需求行欄位分隔（中｜ 或 英 |）
ID_RE = re.compile(r'(?:FR|NFR)-[A-Z0-9]+-\d+')        # 任一需求編號
NULL_DEP = {"-", "無", "none", "n/a", "na", ""}

# 不可量測形容詞黑名單（中英）。只在「需求行」內判定為阻斷。
BANNED = [
    "盡量", "盡可能", "越快越好", "快速", "友善", "直覺", "無縫", "順暢",
    "好用", "易用", "簡單易懂", "簡潔好用", "人性化",
    "as possible", "seamless", "intuitive", "user-friendly",
    "easy to use", "as fast as possible", "blazing fast",
]


def find_banned(text):
    lo = text.lower()
    return [w for w in BANNED if (w in text or w.lower() in lo)]


def extract_deps(line):
    """從需求行的「依賴/Depends」欄位抽出被引用的 FR-/NFR- 編號。"""
    deps = []
    for seg in SEG_SPLIT.split(line):
        s = seg.strip()
        low = s.lower()
        if s.startswith("依賴") or low.startswith("depends"):
            # 去掉欄位標籤後再抽編號，避免誤抓
            body = re.sub(r'^(依賴[:：]?|depends[:：]?)', '', s, flags=re.I).strip()
            if body and body not in NULL_DEP:
                deps.extend(ID_RE.findall(body))
    return deps


def lint(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    errors = []
    warnings = []
    req_count = 0
    seen_ids = {}            # id -> 第一次出現行號
    dep_refs = []            # (lineno, rid, dep_id)

    in_comment = False
    in_fence = False

    for i, raw in enumerate(lines, 1):
        line = raw.rstrip("\n")
        stripped = line.strip()

        # 跳過 HTML 註解區塊 <!-- ... -->
        if not in_comment and "<!--" in stripped and "-->" not in stripped:
            in_comment = True
            continue
        if in_comment:
            if "-->" in stripped:
                in_comment = False
            continue
        if "<!--" in stripped and "-->" in stripped:
            continue

        # 跳過 ``` 程式碼圍欄
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if REQ_RE.match(stripped):
            req_count += 1
            rid = stripped.split(":", 1)[0]
            # 重複編號
            if rid in seen_ids:
                errors.append((i, f"{rid} 編號重複（首次出現於 L{seen_ids[rid]}）"))
            else:
                seen_ids[rid] = i
            # 欄位完整性
            if not PRIORITY_RE.search(line):
                errors.append((i, f"{rid} 缺優先級（需 P0/P1/P2/P3）"))
            if "AC:" not in line and "AC：" not in line:
                errors.append((i, f"{rid} 缺驗收條件（需「AC:」）"))
            if "來源:" not in line and "來源：" not in line:
                errors.append((i, f"{rid} 缺來源追溯（需「來源:」）"))
            hits = find_banned(line)
            if hits:
                errors.append((i, f"{rid} 含不可量測形容詞 {hits}，請翻成數字或可觀察行為"))
            # 收集依賴引用，迴圈結束後再驗證（容許前向引用）
            for dep_id in extract_deps(line):
                dep_refs.append((i, rid, dep_id))
        else:
            if re.search(r'\bshall\b', line):
                warnings.append((i, "出現 'shall' 卻非 FR-/NFR- 編號需求 → 疑似漏編號"))

    # 懸空依賴：依賴指向的編號在本文件查無
    for ln, rid, dep_id in dep_refs:
        if dep_id not in seen_ids:
            warnings.append((ln, f"{rid} 的依賴 {dep_id} 在本文件查無此編號 → 懸空依賴"))

    return errors, warnings, req_count


def main():
    if len(sys.argv) != 2:
        print("用法：python prd_lint.py <PRD.md>")
        sys.exit(2)

    path = sys.argv[1]
    try:
        errors, warnings, req_count = lint(path)
    except FileNotFoundError:
        print(f"找不到檔案：{path}")
        sys.exit(2)

    print("=== Cartographer PRD Lint ===")
    print(f"檔案：{path}")
    print(f"偵測到需求行：{req_count} 條")
    print(f"阻斷項：{len(errors)}　警告：{len(warnings)}")
    print("-" * 40)

    for ln, msg in warnings:
        print(f"  [警告] L{ln}: {msg}")
    for ln, msg in errors:
        print(f"  [阻斷] L{ln}: {msg}")

    print("-" * 40)
    if errors:
        print("❌ 未通過：請修正阻斷項後再交棒 compass。")
        sys.exit(1)
    print("✅ 通過：可交棒 compass。")
    sys.exit(0)


if __name__ == "__main__":
    main()
