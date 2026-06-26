**English** | [繁體中文](../cartographer-zh/docs/INSTALL.md)

# Installation

> Cartographer has three parts: the **skill itself** (`SKILL.md` + `references/`, an on-demand PRD-interviewing knowledge base), the **lint script** (`scripts/prd_lint.py`, the mechanical PRD health check), and the **templates** (`templates/`, a blank PRD plus a canonical filled example). The skill itself is required; installing the lint and templates alongside it is recommended for the full experience.

---

## Prerequisites

- [Claude Code](https://docs.claude.com) installed.
- To run the lint (`scripts/prd_lint.py`): **Python 3.7+** (standard library only — it uses `sys.stdout.reconfigure`, so no extra setup is needed on a Traditional-Chinese Windows console; the script forces UTF-8 output).
- Recommended alongside its toolchain companions — Cartographer draws the map, [Compass](https://github.com/RayLi-Git/compass) walks it, [Sentinel](https://github.com/RayLi-Git/sentinel) stands guard, [Lookout](https://github.com/RayLi-Git/lookout) watches from the mast.

---

## Install steps

A skill is, at its core, "a folder containing a `SKILL.md`." Installing it just means putting it in a skills directory Claude Code scans.

### 1. Install the skill itself (required)

**Option A — Global install (recommended, applies to all projects):**

```bash
mkdir -p ~/.claude/skills/cartographer

# If you received a packaged .skill / .zip file
unzip cartographer.skill -d ~/.claude/skills/cartographer

# Or if you cloned this repo, copy the contents directly
cp -r SKILL.md references ~/.claude/skills/cartographer/
```

**Option B — Project-level install (applies to a single project only):**

```bash
mkdir -p .claude/skills/cartographer
cp -r SKILL.md references .claude/skills/cartographer/
```

### 2. (Recommended) Install the lint script and templates

The lint is the runnable form of the requirement-quality gate; the templates are the starting point for writing your own PRD. Put them in **the project you're working in** (not the skills directory).

```bash
# In your project root
cp -r /path/to/cartographer/scripts ./scripts
cp -r /path/to/cartographer/templates ./templates

# Run the PRD health check (exit 0 = PASS, non-zero = blockers found)
# On Windows use `py`; on macOS/Linux use `python3`
# (typing plain `python` on Windows may hit the Store stub and silently do nothing)
py scripts/prd_lint.py your-PRD.md
```

`templates/prd-blank.md.template` is the empty skeleton; `templates/prd-filled-example.md` is a fully worked example to compare against. The skill also ships demo PRDs under `examples/` (see [`examples/README.md`](../examples/README.md)).

### 3. Resident routing layer (optional)

Want the toolchain's resident routing (`~/.claude/CLAUDE.md`, so Claude auto-routes each task to the right skill)? Use [Sentinel's `CLAUDE.md.example`](https://github.com/RayLi-Git/sentinel/blob/main/CLAUDE.md.example) (it already supports compass / cartographer as optional) — copy it to `~/.claude/CLAUDE.md`. The whole toolchain needs only this **one** shared resident file.

---

## Verify

```bash
ls ~/.claude/skills/cartographer
# Must show: SKILL.md  references

ls ~/.claude/skills/cartographer/references
# Should show 15 module folders: 00_positioning … 14_handoff_compass
```

> ⚠️ Common mistake: after unzipping you end up with an extra nesting level, `cartographer/cartographer/SKILL.md`.
> `SKILL.md` must sit **directly** under `~/.claude/skills/cartographer/`. If there's an extra level, move the inner contents up.

**Confirm it actually triggers.** Open a *new* Claude Code session (only a fresh start scans the new skill), then throw this test:

> "Help me write a PRD."

Cartographer should start the interview from **§00 Positioning** and stop for your confirmation before moving on. If it just dumps a whole PRD without asking, or never mentions positioning / sections, the skill wasn't scanned — go back and check the install structure.

**Where the PRD lives.** Cartographer drafts the PRD as a markdown file in **the project directory you're working in** — there's no separate tracking state. When the draft passes lint, §14 converts it into a Compass-ready checklist for the build stage.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| skill not triggered | didn't open a new session | restart Claude Code |
| can't find references files | extra folder nesting | confirm `SKILL.md` is directly under `cartographer/` |
| `prd_lint.py` does nothing / no output | `python` hit the Windows Store stub | use `py` (Windows) or `python3` (macOS/Linux) |
| lint reports `PASS` on an obviously bad PRD | the PRD has zero numbered requirements (lint blind spot) | use review mode in the skill — the interview catches un-numbered requirements the lint can't |
| `UnicodeEncodeError` on a Chinese Windows console | very old Python without `reconfigure` | upgrade to Python 3.7+ |

### Pairing with the toolchain

Cartographer is the upstream of the toolchain. Typical hand-offs:

- **Before drafting**: idea but messy → [Sentinel](https://github.com/RayLi-Git/sentinel) to think it through → Cartographer starts the interview.
- **§08 security**: Cartographer directly cites Sentinel's red-flag list and security thinking habits.
- **After drafting**: PRD passes lint → §14 handoff → [Compass](https://github.com/RayLi-Git/compass) takes over DoR / implementation / DoD. After a unit lands, [Lookout](https://github.com/RayLi-Git/lookout) does an independent-context review.

### Uninstall

```bash
rm -rf ~/.claude/skills/cartographer
# Remove the project's scripts/ templates/ yourself as needed
```
