**English** | [繁體中文](./cartographer-zh/README.md)

# Cartographer — The Cartographer That Draws Ideas into a PRD

> A Claude Code skill that turns a fuzzy idea into a solid software PRD — **interviewing you section by section, drafting as it goes, until every requirement is verifiable, traceable, and ready to hand off.** Part of a four-skill toolchain: **Cartographer draws the map → Compass walks it → Sentinel stands guard → Lookout watches from the mast.**

![status](https://img.shields.io/badge/status-active-success)
![license](https://img.shields.io/badge/license-MIT-blue)
![toolchain](https://img.shields.io/badge/toolchain-Cartographer·Compass·Sentinel·Lookout-purple)

---

## The problem it solves

The most common ways a software PRD fails before a single line of code is written:

1. **Not verifiable** — "checkout should be fast and friendly" gives engineering nothing to test against.
2. **NFR and security dropped** — only features get written; performance, privacy, and compliance never appear (even Apple's leaked AirPods PRD collected health data with zero privacy handling).
3. **Orphan requirements** — no idea which user or which goal a requirement serves.
4. **Unbounded scope** — nobody ever wrote down what is *not* being built.

Cartographer blocks all four with **section-by-section interviewing + quality gates + a mechanical lint** (exit codes, not willpower).

## How it works

**Five core beliefs:**

1. **It's not a requirement unless it's atomic + numbered + prioritized + verifiable + traceable.**
2. **Unmeasurable adjectives are poison** — fast / good / friendly / seamless must become numbers.
3. **NFRs and security must be confronted, not skipped.**
4. **Honestly listing open questions beats pretending it's all figured out.**
5. **Every requirement must trace back to its source.**

**15 topic modules** (loaded on demand from `references/`):

```
00 Positioning & mode      08 Security/Privacy/Compliance ★ (hooks Sentinel)
01 Background & problem     09 Data & integration
02 Objectives & metrics     10 Scope boundary
03 Assumptions/risks        11 Open questions
04 Stakeholders + RACI      12 Milestones & release slices
05 User stories & journey   13 Glossary & competitive
06 Functional reqs ★        14 Handoff to Compass ★
07 Non-functional reqs
```

Each module is a `references/NN_*/_index.md` with a five-part shape: guiding questions → good/bad contrast → traps → quality gate → format snippet.

## Quick start

```bash
# Install as a user-level skill (applies to all projects)
mkdir -p ~/.claude/skills/cartographer
cp -r SKILL.md references scripts templates ~/.claude/skills/cartographer/

# Verify
ls ~/.claude/skills/cartographer   # → SKILL.md  references  scripts  templates
```

Then tell Claude **"help me write a PRD"** (or "review this PRD"). Cartographer interviews you section by section, stopping for confirmation each time; when done, run `python scripts/prd_lint.py <your-PRD.md>` and hand off to Compass. Full guide in **[docs/INSTALL.md](./docs/INSTALL.md)**.

## The toolchain

Cartographer is the **draw-the-map** stage — the first leg of a four-skill toolchain, each watching a different thing:

| Skill | Role | Watches |
|---|---|---|
| **Cartographer** | draws the map | turning a fuzzy idea into a solid PRD |
| [Compass](https://github.com/RayLi-Git/compass) | walks the map | are you following the PRD? (build to spec, no drift) |
| [Sentinel](https://github.com/RayLi-Git/sentinel) | stands guard | how you think (shallow vs. deep, symptom vs. root cause) |
| [Lookout](https://github.com/RayLi-Git/lookout) | watches from the mast | independent-context code review |

**Cartographer draws the map → Compass walks it → Sentinel stands guard → Lookout watches.** Cartographer fills Compass's upstream gap: Compass assumes the PRD already exists — Cartographer is what forces the idea in your head into that PRD. Full division of labor in [docs/SCOPE.md](./docs/SCOPE.md).

## Structure

```
cartographer/
├── SKILL.md            skill entry (loaded by Claude Code)
├── references/         15 modules, loaded on demand
├── scripts/            prd_lint.py — mechanical PRD health check
├── templates/          blank PRD template + canonical filled example
├── examples/           four real demo PRDs (fictional data) — bad/before/after, two full runs
├── docs/               DESIGN · INSTALL · SCOPE
└── cartographer-zh/    Traditional Chinese mirror
```

## Docs

- **[DESIGN](./docs/DESIGN.md)** — design philosophy, key decisions & trade-offs
- **[INSTALL](./docs/INSTALL.md)** — full install (skill + lint script + templates) & verification
- **[SCOPE](./docs/SCOPE.md)** — what it covers, what it doesn't, and the toolchain split

The skill ships with **example PRDs** under [`examples/`](./examples/) — a beginner's bad PRD, its reviewed-and-regenerated passing version, and two full end-to-end runs — so you can see the quality bar before writing your own.

## License

[MIT](./LICENSE) © Ray_Li

> A portfolio piece exploring "how to encode the discipline of turning a fuzzy idea into a verifiable PRD into an AI coding partner." Its companion [Compass](https://github.com/RayLi-Git/compass) explores "how to keep implementation true to that PRD."
