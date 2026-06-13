<!-- LANG SWITCH -->

**English** | [繁體中文](../README.zh-TW.md)

# Cartographer — the cartographer that draws your ideas into a PRD

> A Claude Code skill that acts as the cartographer between idea and spec — interviewing you section by section, drafting as it goes, turning fuzzy ideas into a verifiable, traceable, hand-off-ready **software PRD**. Pairs with the [Sentinel](https://github.com/RayLi-Git/sentinel) thinking OS and the [Compass](https://github.com/RayLi-Git/compass) PRD-discipline compass to form a complete toolchain.

![status](https://img.shields.io/badge/status-active-success)
![license](https://img.shields.io/badge/license-MIT-blue)
![companion](https://img.shields.io/badge/companion-Sentinel%20%2B%20Compass-purple)

> This is the English mirror skill. The Chinese package is one level up at [../](../).

---

## Toolchain position

> **Cartographer draws the map (creates the PRD) → Compass builds to the map (no drift) → Sentinel stands guard throughout (how to think, no security shortcuts).**

Cartographer fills Compass's upstream gap: Compass assumes the PRD already exists; Cartographer is what **forces the idea in your head into that PRD**.

## The problem it solves

The most common failure modes of a software PRD:

1. **Not verifiable** — "checkout should be fast and friendly" gives engineering nothing to test against
2. **NFR and security dropped** — only features get written (even Apple's AirPods PRD collected health data with zero privacy handling)
3. **Orphan requirements** — no idea which user or which goal they serve
4. **Unbounded scope** — never wrote down what's *not* being done

Cartographer prevents these with **section-by-section interviewing + quality gates + a mechanical lint**.

## Core beliefs

1. **Not a requirement unless it's atomic + numbered + prioritized + verifiable + traceable**
2. **Unmeasurable adjectives are poison** (fast / good / friendly / seamless → turn into numbers)
3. **NFRs and security must be confronted, not skipped**
4. **Honestly listing open questions beats pretending it's all figured out**
5. **Every requirement must trace back to its source**

## The 15 modules

```
00 Positioning & mode    08 Security/Privacy/Compliance ★ (hooks Sentinel)
01 Background & problem   09 Data & integration
02 Objectives & metrics   10 Scope boundary
03 Assumptions/risks      11 Open questions
04 Stakeholders + RACI    12 Milestones & release slices
05 User stories & journey 13 Glossary & competitive
06 Functional reqs ★      14 Handoff to Compass ★
07 Non-functional reqs
```

Each module is a `references/NN_*/_index.md` with a five-part shape: guiding questions → good/bad contrast → traps → quality gate → format snippet.

## How to use

1. Install (see [docs/INSTALL.md](./docs/INSTALL.md)).
2. Tell Claude "help me write a PRD" or "review this PRD".
3. Cartographer interviews you section by section, drafting and stopping for confirmation each time.
4. Run `python scripts/prd_lint.py <your-PRD.md>`; once it passes, hand off to Compass.

## Design blueprint

Built on the leaked Apple AirPods Pro hardware PRD as a skeleton — porting its strengths and fixing its weaknesses (added success-metric instrumentation, split assumptions/risks, elevated security, mandatory acceptance criteria, requirement dependencies, a traceability matrix). See [docs/DESIGN.md](./docs/DESIGN.md) and [docs/SCOPE.md](./docs/SCOPE.md).

## License

MIT — see [../LICENSE](../LICENSE).
