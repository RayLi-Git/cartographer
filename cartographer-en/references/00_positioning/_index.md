# §00 Positioning & Mode | Decide "which kind, how heavy" first

> This is the first section every time. Pick the **mode** (draft / review), then set the **tier** (🟢🟡🔴, how many sections) — don't rush into content. Wrong mode or wrong tier skews the whole document.

---

## Guiding questions (ask these first)

1. Are you **creating a new PRD from scratch**, or do you **have a PRD you want me to review/strengthen**?
2. What scale is this? ① minor revision ② one complete feature module ③ new product/system/cross-team
3. Does it touch **money, PII, permissions, or health/sensitive data**? (If yes → security §08 cannot be skipped)
4. Any **hard deadlines or constraints** (launch date, budget, compliance, existing systems)?
5. Once written, **who builds it and who signs off**?

---

## Mode decision

| Your situation | Mode | Next |
|---|---|---|
| From scratch, idea without spec | **Draft mode** | Interview section by section (01→14) by tier |
| Have a PRD, want gaps found/strengthened | **Review mode** | Run the "PRD health check" (below) |

### Review mode: turn the quality gates into a health checklist
Scan the existing PRD chapter by chapter; for each requirement check the seven questions and list failures + fixes:
- [ ] Does every requirement have a **number**? (no number → not trackable)
- [ ] Does every one have a **priority**? (none → no basis for cutting scope)
- [ ] Is every one **verifiable**, with concrete AC or numbers? (sees "fast/good/friendly/seamless" → flag as poison)
- [ ] Are there **non-functional requirements**? (perf/availability/observability)
- [ ] Is there a **security/privacy** section? (touches PII/money but none → red flag)
- [ ] Can every one **trace back to a source** (persona/objective)?
- [ ] Is there an explicit list of **what's not done**?
> Output: a "health report" — mark each item ✅/⚠️/❌ + fix suggestion, then ask whether to patch them one by one.

---

## Tier decision (matches the SKILL.md three tiers)

| Tier | Trigger | Sections |
|---|---|---|
| 🟢 light | minor revision, single small feature | 00 → 01 → 06 → 11 (§06's "source" traces back to the §01 pain point) |
| 🟡 medium | one complete feature module, one integration | 00–02, 05–11 (integrating a service must include §09 contracts/third-party failure) |
| 🔴 heavy | new product/system/cross-team; money/PII/permissions | full 00–14 |

**Escalate, don't downgrade**: if the user says "just write something simple" but the task touches money/PII, cite this table — §06 acceptance criteria and §08 security **cannot be skipped**.

---

## Common traps

- **Asking about features immediately**: skip positioning and you write only the happy path for something that "goes live to take money". Ask questions 3 and 4 first.
- **Treating review as draft**: the user already has a PRD but you re-interview from scratch → wasteful. Confirm the mode.
- **Tier inflation/deflation**: a small revision forced through 14 sections = noise; a big system squeezed into 4 = missing security. Judge by the trigger table.

---

## Quality gate (pass before §01)

- ✅ Mode chosen (draft / review)
- ✅ Tier set, and the user knows which sections come next
- ✅ Question 3 resolved — if it touches PII/money/permissions, "§08 required" is flagged

---

## Format snippet (the PRD's opening metadata)

```
Product/feature name:
Author / PM:
Version: v0.1   Created: YYYY-MM-DD
Tier: 🔴 heavy   Mode: draft
Sensitive scope: [x]PII [x]money [ ]health data [x]permissions   → §08 required
```
