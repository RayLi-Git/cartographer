# §03 Assumptions / Constraints / Risks | Put the unresolved on the table

> This section was **added** after the multi-perspective review — the AirPods PRD lumped all risk into Open Questions, so "undecided questions" and "things that could kill the project" weren't separated. A mature PRD splits three things: **assumptions (what we bet on) / constraints (boundaries I can't change) / risks (what could go wrong + how to block it)**.

---

## Guiding questions

1. What **premises** must hold for this PRD? (which, if false, collapse the whole approach?)
2. What **constraints can't change**? Tech stack, budget, deadline, existing systems, compliance, headcount.
3. Where is it **most likely to go wrong**? How likely, how big the impact, how to mitigate, who owns it?
4. Which assumptions can be **validated early**? (high-risk assumptions → schedule early validation in §12)

---

## The difference between the three

| Type | Question | Example |
|---|---|---|
| **Assumption** | "What are we betting holds?" | Payment provider SLA 99.95%; users willing to save a card |
| **Constraint** | "What can't I change?" | Must run on existing K8s; budget 800k; ship by end of June |
| **Risk** | "What could hurt us? How do we block it?" | Provider outage → degraded fallback + reconciliation |

---

## Risk register (probability × impact → mitigation)

| ID | Risk | Prob | Impact | Mitigation | Owner |
|----|------|------|--------|------------|-------|
| R-1 | Callback delay causes double charge | Med | High | Idempotency key + reconciliation retry + alert | Backend |
| R-2 | 10x peak traffic crushes checkout | Med | High | Load test + autoscale + queue page | SRE |
| R-3 | ⚠️assumption users won't save a card | High | Med | Guest checkout / third-party pay | PM |

> **High-probability × high-impact** risks → must set validation/mitigation early in §12 milestones, not deferred to pre-launch.

---

## Common traps

- **Writing a risk as an open question**: "will payments fail?" is a question, not a risk. A risk states "**what happens + probability + impact + how to block**". Pure open questions belong in §11.
- **Assumptions with no owner to validate**: a high-risk assumption needs an owner + validation time, or it's a time bomb.
- **Vague constraints**: "around June" → constraints must be exact, or §12 scheduling is empty.
- **Listing risks without mitigation**: a risk register with no mitigations is just an anxiety list.

---

## Quality gate (pass before §04)

- ✅ Assumptions, constraints, risks listed separately
- ✅ Every risk has probability, impact, **mitigation**, owner
- ✅ High-prob × high-impact risks flagged for early validation in §12
- ✅ Hypotheses moved here from §02 have landed

---

## Format snippet

```markdown
## 3. Assumptions, Constraints & Risks

**Assumptions (we bet they hold)**
- A-1: <assumption> | validation: <how/when> | owner: <who>

**Constraints (boundaries we can't change)**
- C-1: <tech/budget/deadline/compliance constraint>

**Risk register**
| ID | Risk | Prob | Impact | Mitigation | Owner |
|----|------|------|--------|------------|-------|
| R-1 | ... | High/Med/Low | High/Med/Low | ... | ... |
```
