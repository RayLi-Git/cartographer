**English** | [繁體中文](../cartographer-zh/docs/SCOPE.md)

# Scope

> A skill's value lies not only in "what it can do," but in clearly stating "what it does not do." This document lists Cartographer's coverage boundaries explicitly, to prevent misuse or mismatched expectations.

---

## In scope

**Situations Cartographer covers:**

| Area | Notes |
|---|---|
| **Drafting a software PRD from scratch** | Section-by-section interview turning a fuzzy idea into a solid PRD (15 modules) |
| **Reviewing / strengthening an existing PRD** | Turn the quality gates into a health checklist, find gaps, suggest fixes |
| **Requirement-quality enforcement** | Atomic + numbered + prioritized + verifiable + traceable; `prd_lint` mechanical gate |
| **Non-functional / security / privacy** | Forces confronting performance, SLA, observability, a11y, i18n, data classification, compliance |
| **Traceability matrix** | FR ↔ persona ↔ objective ↔ AC ↔ milestone |
| **Handoff to Compass** | Convert into a Compass-ready checklist and reverse-audit input |

**Three-tier scaling** — Cartographer right-sizes the interview to the task:

- 🟢 **light** — a minor revision → ~4 sections (00 / 01 / 06 / 11).
- 🟡 **medium** — one feature module → ~9 sections.
- 🔴 **heavy** — a new product touching money / PII / permissions → the full 00–14; §06 acceptance criteria and §08 security cannot be skipped.

The skill ships **example PRDs** under [`examples/`](../examples/) — a beginner's bad PRD, its reviewed-and-regenerated passing version, and two full end-to-end runs — all with fictional data, so you can study the quality bar before drafting your own.

---

## Out of scope

Explicitly out of scope, to avoid misuse.

**Work types not covered (and who does them):**

| Not this | Use |
|---|---|
| Implementing the PRD, building to spec, no drift | **[Compass](https://github.com/RayLi-Git/compass)** |
| How to think, root-cause diagnosis, security thinking habits | **[Sentinel](https://github.com/RayLi-Git/sentinel)** |
| Independent-context code review after a unit lands | **[Lookout](https://github.com/RayLi-Git/lookout)** |
| Hardware PRD (mechanical, electrical, manufacturing, regulatory tests) | This skill focuses on software |
| Business plan / financial model / fundraising deck | Not a PRD concern |
| Detailed UI design / wireframes / visual specs | Design tools; the PRD describes behavior and states |
| Project-management scheduling detail (Gantt charts, hours) | PM tools; the PRD goes only as far as milestones and slices |

---

## Boundaries & common misconceptions

These boundaries are drawn on purpose, not gaps. The current Cartographer (all 15 modules + runnable lint + blank/filled templates + example PRDs + EN/ZH bilingual) is complete and usable.

- **"It writes the PRD for me in one shot."** No — Cartographer interviews you section by section and stops for confirmation each time. A one-shot draft *looks* complete but is mostly speculation; the stops are exactly where quality comes from.
- **"The lint guarantees a good PRD."** The lint catches malformed requirements (missing number / priority / AC / source, unmeasurable adjectives), but it cannot catch "requirements that were never numbered" — an un-numbered PRD gets a false PASS. That blind spot is why the human-driven review mode exists.
- **"It assumes a perfect blueprint."** The opposite — Cartographer's blueprint (the leaked AirPods PRD) had eight concrete weaknesses, and fixing them is half the design (see [DESIGN](./DESIGN.md)).
- **"It also designs the UI."** No — the PRD describes *behavior and states* (empty / loading / error / offline), not pixels. Wireframes and visual specs belong in design tools.
- **"It's a hardware PRD tool because the blueprint was hardware."** No — the *structure* was ported, but Cartographer is tuned for software. Mechanical / electrical / manufacturing specs are out of scope.

---

## Toolchain split

Cartographer is the **draw-the-map** stage — the first leg of a four-skill toolchain, each watching a different thing:

| Skill | Role | Watches |
|---|---|---|
| **Cartographer** | draws the map | turning a fuzzy idea into a solid PRD |
| [Compass](https://github.com/RayLi-Git/compass) | walks the map | are you following the PRD? (build to spec, no drift) |
| [Sentinel](https://github.com/RayLi-Git/sentinel) | stands guard | how you think (shallow vs. deep, symptom vs. root cause) |
| [Lookout](https://github.com/RayLi-Git/lookout) | watches from the mast | independent-context code review |

**Cartographer draws the map → Compass walks it → Sentinel stands guard → Lookout watches.**

Cartographer and Compass are the closest pair — back-to-back stages on the same artifact:

| Dimension | Cartographer | Compass |
|---|---|---|
| Primarily produces / watches | The "**PRD**" itself | Your relationship with the "**PRD**" |
| Core belief | A requirement isn't real unless it's verifiable & traceable | The PRD is a contract, done means done |
| Core trigger question | "Is this idea a buildable spec yet?" | "Am I following the PRD?" |
| Key actions | Section interview, quality gates, prd_lint, traceability matrix | DoR, tracking docs, PRD conflict handling, tool enforcement |
| Applicable scope | You have an idea but no usable spec | You have a PRD and must build to it |

**Typical hand-offs across the toolchain:**

1. **Idea but messy** → [Sentinel](https://github.com/RayLi-Git/sentinel) helps you think it through → Cartographer starts the section interview.
2. **§08 security** → Cartographer cites Sentinel's red-flag list directly, so security is confronted at PRD stage, not after launch.
3. **PRD passes lint** → §14 handoff → [Compass](https://github.com/RayLi-Git/compass) takes over DoR / implementation / DoD.
4. **A unit lands** → [Lookout](https://github.com/RayLi-Git/lookout) does an independent-context review.

---

## Feedback & contribution

Cartographer is a personal portfolio piece, but contributions are welcome via GitHub Issues:

- Spots where the scope description is inaccurate.
- PRD failure modes you hit that this skill doesn't yet catch (or shouldn't).
- Blind spots in the division of labor across the toolchain.

---

> **Remember**: Cartographer is not a panacea; it's a **tool that's precise in specific situations**. Use it when you have an idea but no usable spec, and it saves you the rework of a vague PRD; use it when the spec already exists, and you should reach for Compass instead. Read this document first, then decide whether to use it.
