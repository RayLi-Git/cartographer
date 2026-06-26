#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prd_lint.py — Cartographer's mechanical PRD health check (exit code over discipline).

Blocking checks (exit 1):
  1. A requirement line (FR-/NFR-) missing a priority P0–P3
  2. A requirement line missing an "AC:" acceptance criterion
  3. A requirement line missing a "Source:" trace
  4. A requirement line containing an unmeasurable adjective (fast/friendly/seamless/intuitive/as possible...)
  5. A duplicate requirement id (same FR-/NFR- id appears more than once)

Warnings (non-blocking):
  6. A non-requirement line containing "shall" -> suspected un-numbered requirement
  7. A "Depends:" reference to an FR-/NFR- id not defined in this file -> dangling dependency

Usage:
  py prd_lint.py <PRD.md>        # Windows (plain `python` may be the Store stub and silently do nothing)
  python3 prd_lint.py <PRD.md>   # macOS / Linux
  exit 0 = pass (ready to hand off to Compass); exit 1 = blocking issues

v2: removed the noisy prose-adjective warning; added duplicate-id (blocking) and dangling-dependency (warning) structural checks.
"""

import sys
import re

# Force UTF-8 output (Windows console defaults to a legacy codepage)
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Requirement line: FR-PAY-01: / NFR-A11Y-01: (module code may contain digits, e.g. A11Y, I18N)
REQ_RE = re.compile(r'^(FR|NFR)-[A-Z0-9]+-\d+:')
PRIORITY_RE = re.compile(r'\bP[0-3]\b')
SEG_SPLIT = re.compile(r'[｜|]')                       # requirement-line field separator (| or ｜)
ID_RE = re.compile(r'(?:FR|NFR)-[A-Z0-9]+-\d+')        # any requirement id
NULL_DEP = {"-", "none", "n/a", "na", "", "無"}

# Unmeasurable adjectives. Single ASCII words use word boundaries; phrases/CJK use substring.
BANNED_WORD = ["fast", "easy", "simple", "seamless", "intuitive", "friendly", "smooth"]
BANNED_SUB = [
    "user-friendly", "as possible", "as fast as possible", "blazing fast",
    "快速", "友善", "直覺", "無縫", "盡量", "順暢", "好用", "易用",
]


def banned_hits(text):
    low = text.lower()
    hits = []
    for w in BANNED_WORD:
        if re.search(r'\b' + re.escape(w) + r'\b', low):
            hits.append(w)
    for w in BANNED_SUB:
        if w.lower() in low:
            hits.append(w)
    return hits


def extract_deps(line):
    """Pull referenced FR-/NFR- ids from the requirement line's Depends field."""
    deps = []
    for seg in SEG_SPLIT.split(line):
        s = seg.strip()
        if s.lower().startswith("depends") or s.startswith("依賴"):
            body = re.sub(r'^(depends[:：]?|依賴[:：]?)', '', s, flags=re.I).strip()
            if body and body.lower() not in NULL_DEP:
                deps.extend(ID_RE.findall(body))
    return deps


def lint(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    errors = []
    warnings = []
    req_count = 0
    seen_ids = {}            # id -> first line seen
    dep_refs = []            # (lineno, rid, dep_id)
    in_comment = False
    in_fence = False

    for i, raw in enumerate(lines, 1):
        line = raw.rstrip("\n")
        stripped = line.strip()

        # Skip HTML comment blocks <!-- ... -->
        if not in_comment and "<!--" in stripped and "-->" not in stripped:
            in_comment = True
            continue
        if in_comment:
            if "-->" in stripped:
                in_comment = False
            continue
        if "<!--" in stripped and "-->" in stripped:
            continue

        # Skip ``` code fences
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if REQ_RE.match(stripped):
            req_count += 1
            rid = stripped.split(":", 1)[0]
            if rid in seen_ids:
                errors.append((i, f"{rid} duplicate id (first seen at L{seen_ids[rid]})"))
            else:
                seen_ids[rid] = i
            if not PRIORITY_RE.search(line):
                errors.append((i, f"{rid} missing priority (need P0/P1/P2/P3)"))
            if "AC:" not in line:
                errors.append((i, f"{rid} missing acceptance criteria (need 'AC:')"))
            if "Source:" not in line:
                errors.append((i, f"{rid} missing source trace (need 'Source:')"))
            hits = banned_hits(line)
            if hits:
                errors.append((i, f"{rid} contains unmeasurable adjective {hits}; turn into a number or observable behavior"))
            for dep_id in extract_deps(line):
                dep_refs.append((i, rid, dep_id))
        else:
            if re.search(r'\bshall\b', line):
                warnings.append((i, "'shall' on a non FR-/NFR- line -> suspected missing number"))

    for ln, rid, dep_id in dep_refs:
        if dep_id not in seen_ids:
            warnings.append((ln, f"{rid} depends on {dep_id}, which is not defined in this file -> dangling dependency"))

    return errors, warnings, req_count


def main():
    if len(sys.argv) != 2:
        print("Usage: py prd_lint.py <PRD.md> (Windows) / python3 prd_lint.py <PRD.md> (macOS/Linux)")
        sys.exit(2)

    path = sys.argv[1]
    try:
        errors, warnings, req_count = lint(path)
    except FileNotFoundError:
        print(f"File not found: {path}")
        sys.exit(2)

    print("=== Cartographer PRD Lint ===")
    print(f"File: {path}")
    print(f"Requirement lines detected: {req_count}")
    print(f"Blocking: {len(errors)}  Warnings: {len(warnings)}")
    print("-" * 40)

    for ln, msg in warnings:
        print(f"  [WARN]  L{ln}: {msg}")
    for ln, msg in errors:
        print(f"  [BLOCK] L{ln}: {msg}")

    print("-" * 40)
    if errors:
        print("FAIL: fix blocking issues before handing off to Compass.")
        sys.exit(1)
    print("PASS: ready to hand off to Compass.")
    sys.exit(0)


if __name__ == "__main__":
    main()
