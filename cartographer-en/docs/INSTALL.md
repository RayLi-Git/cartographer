# Cartographer Install Guide

> Cartographer is a Claude Code skill. Installing = placing the folder in a skills directory Claude Code scans.

---

## Option 1: personal skills directory (simplest)

Copy the `cartographer-en/` folder into your personal skills directory as `cartographer-en`:

```
# macOS / Linux
cp -r cartographer-en ~/.claude/skills/cartographer-en

# Windows (PowerShell)
Copy-Item -Recurse cartographer-en "$env:USERPROFILE\.claude\skills\cartographer-en"
```

> Claude Code auto-scans subfolders containing `SKILL.md` under `~/.claude/skills/`, loading name + description.

## Option 2: project skills directory

Place it in your project's `.claude/skills/cartographer-en/`, available only in that project.

## Verify install

1. Restart Claude Code (or open a new session).
2. Say "help me write a PRD".
3. Cartographer should trigger and start from §00 Positioning.

## Requirements

- `prd_lint.py` needs Python 3.7+ (uses `sys.stdout.reconfigure`).
- No extra setup on Windows consoles; the script forces UTF-8 output.

## Directory structure

```
cartographer-en/
├── SKILL.md
├── references/00..14/_index.md
├── templates/{prd-blank.md.template, prd-filled-example.md}
├── scripts/prd_lint.py
└── docs/{DESIGN,INSTALL,SCOPE}.md
```

## Pairing with Sentinel / Compass

Install all three together for the complete toolchain:

```
~/.claude/skills/
├── sentinel/
├── compass/
└── cartographer/   (or cartographer-en/)
```

### Resident layer (optional)

Want the three-skill resident routing (`~/.claude/CLAUDE.md`, so Claude auto-routes each task to the right skill)? Use [sentinel's `CLAUDE.md.example`](https://github.com/RayLi-Git/sentinel/blob/main/CLAUDE.md.example) (it already supports compass / cartographer as optional) — copy it to `~/.claude/CLAUDE.md`. The whole toolchain needs only this **one** shared resident file.
