# Cartographer Design Decisions & Tradeoffs

> Records "why this, not that" — so future maintainers (including AI) understand the tradeoff context.

---

## 1. Why the AirPods Pro PRD as a blueprint

A leaked Apple AirPods Pro hardware PRD has excellent skeletal discipline: every requirement atomic, numbered, prioritized (P1–P10), measurable (FOB <$75, leakage <10dB), persona-driven, honest open questions, with a glossary and competitive analysis. **These disciplines have nothing to do with "hardware" — they're exactly the DNA a good software PRD needs**, so they're ported.

## 2. Six senior perspectives on the blueprint, then fixing its 8 weaknesses

Good as it is, the blueprint has flaws (also common software-PRD pits), each fixed:

| # | Blueprint weakness | Cartographer's fix |
|---|---|---|
| 1 | Objectives state hypothesis as fact ("will expand 15%") | §02 forces splitting goal/hypothesis/fact + requires measurement |
| 2 | Risks mixed into Open Questions | §03 standalone "assumptions/constraints/risks", register with prob × impact × mitigation |
| 3 | Collects health data with zero privacy | §08 security elevated to a standalone module, hooks Sentinel |
| 4 | Most functional requirements lack acceptance criteria | §06 mandatory AC per requirement, prd_lint gate |
| 5 | Only the happy path | §06 mandatory negative/edge/state (empty·loading·error·offline) |
| 6 | No requirement dependency graph | §12 adds dependency ordering, feeding Compass's build order |
| 7 | Parts but no wiring (requirements with no source) | Traceability woven throughout, produced at §14 |
| 8 | Unmeasurable bad lines (1.6/2.11/3.5) | Collected into each module as a "anti-example library" |

## 3. Key tradeoffs

### Why 15 modules, not one big SKILL.md
The official three-level progressive disclosure: metadata always loaded, SKILL.md loaded on trigger (lean, <2000 words), references loaded on demand. 15 modules let a light task touch only a few sections without blowing up context.

### Why P0–P3, not the blueprint's P1–P10
Software-industry P0(blocking)/P1/P2/P3 has lower communication cost and is universal. §13 glossary notes the mapping (P0≈P10), preserving the quantification spirit.

### Why security gets "standalone module + hooks Sentinel"
The blueprint's biggest hole is security/privacy, and it's the most-skipped software-PRD section. Hooking Sentinel's 11 security habits and red-flag list blocks "hardcoded secrets/unvalidated input/over-broad permissions" at PRD stage.

### Why the traceability matrix
This surpasses the blueprint and is the best handoff interface to Compass: every requirement tags source/objective/AC, so orphan requirements and fall-through objectives are visible at a glance.

### Why stop section by section, not generate at once
PRD quality comes from a human-machine dialog pressing on details. One-shot generation tends to produce content that looks complete but is actually speculation; stopping each section ensures every one has user input and confirmation.

### Why persona voice (both languages)
Consistent with the existing compass-en / sentinel-en ("I'm Compass" first person) for unified brand feel. The frontmatter description still uses a third-person keyword pack for triggering.

## 4. Mechanical first (exit code over discipline)
`prd_lint.py` turns "missing number/priority/AC/source/unmeasurable adjective" into blockable checks, echoing Compass's "exit code over discipline" belief.

### prd_lint v2 (iterated from real stress-test feedback)
An end-to-end stress test surfaced two problems: prose adjectives (e.g. "fast") triggered false positives — even the official example tripped them; and the lint missed structural errors. v2 fixes:
- **Removed** the prose-level adjective warning (too imprecise) — adjectives are blocking only inside requirement lines.
- **Added** two structural checks: duplicate id (blocking) and dangling dependency (a `Depends:` reference to an FR/NFR not defined in the file → warning), replacing the manual orphan check with an exit code.
> Lesson: lint catches "malformed requirements" but not "requirements that were never numbered" (an unnumbered PRD gets a false PASS) — which is exactly why the review-mode skill layer exists.
