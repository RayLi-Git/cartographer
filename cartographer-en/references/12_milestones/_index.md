# §12 Milestones & Release Slices | Independently shippable slices, ordered by dependency

> Maps to AirPods' Milestones (concept → design → freeze → release). Software adds two things the template lacked: **vertical slices** (each end-to-end usable and verifiable) and **requirement dependency ordering** (Compass's build order). Echoing the house rule: done means done — ship in small slices, but leave no half-finished phases.

---

## Guiding questions

1. Into which **end-to-end, independently shippable** milestones can it be sliced? (not "backend first, then frontend" — that's horizontal)
2. What are the **dependencies** among §06 requirements? Which must come first?
3. Which **high-risk assumptions** (§03) validate in which early milestone?
4. What's each milestone's **definition of done (DoD)** and demo bar?
5. Any **hard dates** (deadline, compliance, campaign window)?

---

## Vertical slice ≠ horizontal phase

| ✅ Vertical slice (each usable) | ❌ Horizontal phase (half-finished) |
|---|---|
| M1: guest single-card checkout, end-to-end payment success | Phase 1: finish all backend APIs (frontend unusable) |
| M2: add saved card + Apple Pay | Phase 2: finish all frontend (can't connect) |

> Each slice contains the features/NFR/security it needs, works end-to-end, and is verifiable.

---

## Requirement dependency ordering (Compass's build order on handoff)

```
FR-PAY-01 create intent  ──▶ FR-PAY-02 submit payment ──▶ FR-PAY-03 timeout handling
NFR-SEC-01 API authz     ──▶ (prerequisite for all PAY requirements)
```
> The dependency graph becomes Compass's implementation-order input at §14 handoff. The validation requirements for high-risk assumptions (§03) go first.

---

## Milestone table

| Milestone | Content (slice) | Requirements | DoD | Hard date |
|---|---|---|---|---|
| M1 | Guest card checkout | FR-PAY-01..03, NFR-SEC-01 | Real sandbox payment succeeds + load test passes | — |
| M2 | Saved card + mobile pay | FR-PAY-04.., FR-ADDR-* | Apple/Google Pay pass | before peak season |

---

## Common traps

- **Horizontal phases leaving half-products**: violates "no half-finished". Use vertical slices.
- **Scheduling dates ignoring dependencies**: order without dependency → later blocks earlier. Draw the dependency graph before scheduling.
- **High-risk assumptions deferred to the end**: §03 high-prob × high-impact assumptions validate earliest, lest you find the direction wrong halfway.
- **Milestones with no DoD**: "M1 done" undefined → unverifiable.

---

## Quality gate (pass before §13)

- ✅ Milestones are **vertical slices**, each end-to-end verifiable
- ✅ The dependency graph is drawn; scheduling respects dependencies
- ✅ High-risk assumptions (§03) scheduled for early-milestone validation
- ✅ Each milestone has a DoD and demo bar

---

## Format snippet

```markdown
## 12. Milestones & Release Slices

**Dependencies**: FR-PAY-01 → FR-PAY-02 → FR-PAY-03; NFR-SEC-01 is prerequisite

| Milestone | Slice content | Requirements | DoD | Hard date |
|-----------|---------------|--------------|-----|-----------|
| M1 | ... | FR-..., NFR-... | ... | ... |
```
