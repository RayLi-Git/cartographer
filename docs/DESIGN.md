**English** | [繁體中文](../cartographer-zh/docs/DESIGN.md)

# Design

> The value of a portfolio piece isn't *what* was built — it's *why it was built this way*. This document records the design philosophy and key decisions behind Cartographer: how a leaked hardware PRD became the blueprint for a reusable PRD-drafting skill.
> Coverage boundaries and future directions live in [SCOPE](./SCOPE.md); this doc is only about the *why*.

---

## Design philosophy

Cartographer's raw material wasn't conjured from nothing — it started from a leaked **Apple AirPods Pro hardware PRD**. That document has excellent skeletal discipline: every requirement is atomic, numbered, prioritized (P1–P10), measurable (FOB <$75, leakage <10dB), persona-driven, with honest open questions, a glossary, and competitive analysis. The first key insight set the tone for the whole project:

> **These disciplines have nothing to do with "hardware" — they are exactly the DNA a good software PRD needs.** So port the skeleton, then fix what the blueprint got wrong.

Five core beliefs fall out of that:

1. **It's not a requirement unless it's atomic + numbered + prioritized + verifiable + traceable.**
2. **Unmeasurable adjectives are poison** — fast / good / friendly / seamless must become numbers.
3. **NFRs and security must be confronted, not skipped.**
4. **Honestly listing open questions beats pretending it's all figured out.**
5. **Every requirement must trace back to its source.**

The architecture mirrors that of its companions: **pointers always on, detail on demand.** `SKILL.md` stays lean (its description is also bound by a ~1024-character limit) to guarantee triggering, while the real interviewing detail loads on demand from `references/` per module — never blowing up the context.

| Layer | Role | Analogy |
|---|---|---|
| `SKILL.md` | always-on pointers + trigger protocol | doorpost sign (lean, loads references on demand) |
| `references/` | detailed interviewing guidance across 15 topic modules | library stacks (visited when needed) |
| `scripts/` + `templates/` | runnable lint + blank/filled PRD templates | toolbox (the physical form of mechanical enforcement) |

---

## Key decisions

### Decision 1: The AirPods Pro PRD as a blueprint

- **Problem**: What does a "good PRD" actually look like? Abstract advice ("be clear, be complete") teaches nobody. A concrete, disciplined exemplar does.
- **Choice**: Adopt the leaked AirPods Pro hardware PRD as the skeletal blueprint, porting its strengths — atomic numbered requirements, priorities, measurable acceptance, persona-driven stories, honest open questions, glossary, competitive analysis.
- **Trade-off**: A hardware PRD carries hardware-specific noise (BOM cost, acoustic leakage) that must be filtered out. But the *structure* transfers cleanly, and a real exemplar beats invented advice every time.

### Decision 2: Six senior perspectives, then fixing the blueprint's 8 weaknesses

- **Problem**: Good as it is, the blueprint has flaws — and they happen to be the most common software-PRD pits too. Porting it uncritically would inherit those holes.
- **Choice**: Review the blueprint from six senior perspectives and fix eight concrete weaknesses, each mapped to a module.

  | # | Blueprint weakness | Cartographer's fix |
  |---|---|---|
  | 1 | Objectives state hypothesis as fact ("will expand 15%") | §02 forces splitting goal / hypothesis / fact + requires a measurement mechanism |
  | 2 | Risks mixed into Open Questions | §03 standalone "assumptions / constraints / risks", register with probability × impact × mitigation |
  | 3 | Collects health data with zero privacy | §08 security elevated to a standalone module, hooks Sentinel |
  | 4 | Most functional requirements lack acceptance criteria | §06 mandatory AC per requirement, prd_lint gate |
  | 5 | Only the happy path | §06 mandatory negative / edge / state (empty · loading · error · offline) |
  | 6 | No requirement dependency graph | §12 adds dependency ordering, feeding Compass's build order |
  | 7 | Parts but no wiring (requirements with no source) | Traceability woven throughout, produced at §14 |
  | 8 | Unmeasurable bad lines | Collected into each module as an "anti-example library" |

- **Trade-off**: More modules and more discipline than a bare template. But each fix closes a hole that otherwise surfaces as rework once engineering starts.

### Decision 3: 15 modules, not one big SKILL.md

- **Problem**: Should all the interviewing guidance live in one file, or be split?
- **Choice**: Follow the official three-level progressive disclosure — metadata always loaded, `SKILL.md` loaded on trigger (lean, <2000 words), `references/` loaded on demand. 15 modules let a light task touch only a few sections without blowing up the context.
- **Trade-off**: More files to navigate. In exchange, a minor revision (4 sections) never drags in the full security/NFR machinery, and the trigger stays reliable.

### Decision 4: P0–P3, not the blueprint's P1–P10

- **Problem**: The blueprint's ten priority levels are precise but carry high communication cost and aren't how software teams talk.
- **Choice**: Use the software-industry standard P0 (blocking) / P1 / P2 / P3 — lower communication cost, universally understood. §13 glossary notes the mapping (P0 ≈ P10), preserving the quantification spirit.
- **Trade-off**: Coarser granularity. But priority is a communication tool, and a scale the whole team reads the same way beats a finer one nobody shares.

### Decision 5: Security gets "standalone module + hooks Sentinel"

- **Problem**: The blueprint's biggest hole is security/privacy, and it's the single most-skipped software-PRD section. Folding it into a generic "NFR" line guarantees it gets glossed over.
- **Choice**: Elevate §08 to a standalone module and hook Sentinel's security thinking habits and red-flag list — so "hardcoded secrets / unvalidated input / over-broad permissions" get blocked at the *PRD* stage, before any code exists.
- **Trade-off**: A heavier security section that a 🟢 light task can skip but a 🔴 money/PII/permissions task cannot. The asymmetry is deliberate: a privacy gap discovered post-launch costs far more than the interview time.

### Decision 6: The traceability matrix as the handoff interface

- **Problem**: A PRD full of well-formed requirements can still have "parts but no wiring" — requirements with no traceable source, objectives with no requirement serving them.
- **Choice**: Weave traceability throughout and produce a matrix at §14 — every requirement tagged with source / objective / AC / milestone. This surpasses the blueprint and is the cleanest handoff interface to Compass: orphan requirements and fall-through objectives are visible at a glance.
- **Trade-off**: Extra bookkeeping while drafting. But it's exactly what Compass's reverse audit consumes, so the cost is paid once and reused downstream.

### Decision 7: Stop section by section, not generate at once

- **Problem**: One-shot PRD generation produces content that *looks* complete but is actually speculation — the model fills gaps with plausible guesses the user never confirmed.
- **Choice**: Interview section by section, stopping for confirmation each time. PRD quality comes from a human-machine dialog that presses on details; each stop ensures every section has real user input.
- **Trade-off**: Slower than a one-shot draft. But a fast draft full of unconfirmed assumptions isn't a contract — it's a liability.

### Decision 8: Mechanical first — exit code over discipline

- **Problem**: "Remember to number every requirement, add acceptance criteria, avoid vague adjectives" is advice that erodes under deadline pressure, exactly like every other rule that depends on a human to self-enforce.
- **Choice**: `prd_lint.py` turns "missing number / priority / AC / source / unmeasurable adjective" into blockable checks with a non-zero exit code — echoing Compass's "exit code over discipline" belief. A real stress test then iterated it to v2: the prose-level adjective warning was removed (too imprecise — even the official example tripped it; adjectives now block only inside requirement lines), and two structural checks were added (duplicate id = blocking, dangling `Depends:` reference = warning).
- **Trade-off**: A lint catches "malformed requirements" but not "requirements that were never numbered" — an un-numbered PRD gets a false PASS. That blind spot is exactly why the review-mode skill layer exists: the human-driven interview catches what the mechanical gate can't.

---

## What it deliberately doesn't do

These are boundaries drawn on purpose, not gaps. The full reasoning lives in [SCOPE](./SCOPE.md); the short version:

- **It does not implement the PRD.** Cartographer stops at a hand-off-ready spec; building to that spec without drift is [Compass](https://github.com/RayLi-Git/compass)'s job.
- **It does not govern how you think.** Root-cause diagnosis and security thinking habits are [Sentinel](https://github.com/RayLi-Git/sentinel)'s scope — §08 cites them rather than re-teaching them.
- **It does not write hardware PRDs.** The blueprint was hardware, but Cartographer is tuned for software behavior and states — mechanical/electrical/manufacturing specs are out.
- **It does not pretend a one-shot draft is a contract.** The section-by-section stops are the point; skipping them to "just generate it" defeats the entire design.

---

> Cartographer isn't a silver bullet — it's a **precise tool for a specific situation**. It explores "how to encode the discipline of turning a fuzzy idea into a verifiable PRD into an AI coding partner." Its companions explore the rest: [Compass](https://github.com/RayLi-Git/compass) builds to the map, [Sentinel](https://github.com/RayLi-Git/sentinel) governs how you think, [Lookout](https://github.com/RayLi-Git/lookout) watches from the mast.
