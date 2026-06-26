# §14 Handoff to Compass ★ | Give the map to the build crew

> This is the toolchain seam. Once the PRD is drawn, it must **convert seamlessly into a Compass-ready `prd-checklist.md`**, with a **traceability matrix** attached — this is where Cartographer surpasses the AirPods template (the template had parts, no wiring). The matrix is also Compass's reverse-audit input.

---

## Guiding questions (after the PRD is complete)

1. Are all FR/NFR numbered, with AC and priority? (run `prd_lint.py` to confirm)
2. Does every requirement trace to a persona/objective? Any **orphans**?
3. Is the dependency ordering (§12) sorted?
4. Are the Compass checklist and matrix produced?

---

## Traceability matrix (FR ↔ persona ↔ objective ↔ AC ↔ milestone)

| Requirement | Source persona/scenario | Objective | AC summary | Priority | Milestone |
|---|---|---|---|---|---|
| FR-PAY-01 | P1 Yi-Jun / Scenario #1 | O-2 lower abandonment | create intent returns 200 | P0 | M1 |
| FR-PAY-03 | Scenario #2 interrupt | O-1 success rate | timeout → pending + retry | P0 | M1 |
| NFR-PRIV-01 | Compliance | Guardrail | no plaintext card number found | P0 | M1 |

**Orphan check**:
- Requirement with no source → go back to §05, or delete, or move to §11.
- An objective served by no requirement → §02 goal falls through; add a requirement or cut the goal.

---

## Convert to Compass's prd-checklist.md

Expand each FR/NFR into Compass checklist items (matching `compass/templates/prd-checklist.md.template`):

```markdown
## PRD Checklist (handoff to Compass)
- [ ] FR-PAY-01 create payment intent | P0 | AC: returns 200 with paymentId | verify: integration test
- [ ] FR-PAY-03 timeout → pending | P0 | AC: at s31 = pending, ≤3 retries in 5min | verify: integration test
- [ ] NFR-SEC-01 payment API authz | P0 | AC: missing token returns 401 | verify: security test (test-first)
- [ ] NFR-PRIV-01 no plaintext card | P0 | AC: full-text scan finds no 16-digit | verify: scan script
```

> After handoff, Compass takes over: DoR check → implement in order → complete-compare-correct → DoD. Cartographer's traceability matrix is the left half of Compass's reverse audit (PRD↔code).

---

## Common traps

- **Not running lint before handoff**: throwing a non-conforming PRD to Compass → missing AC found during the build. Pass `prd_lint.py` first.
- **Orphans in the matrix**: requirements with no source, objectives with no requirement → clean them up before handing off.
- **Checklist missing verification method**: Compass needs to know how each is verified (unit/integration/security/manual).
- **Dependencies not carried over**: Compass can't order the build. Hand over the §12 dependency graph too.

---

## Quality gate (the last gate before handoff)

- ✅ `prd_lint.py` exit code 0
- ✅ Traceability matrix has no orphan requirements, no fall-through objectives
- ✅ Each checklist item has priority + AC + verification method
- ✅ The §12 dependency ordering is delivered together

---

## Format snippet

```markdown
## 14. Handoff to Compass

### Traceability matrix
| Requirement | Source | Objective | AC summary | Priority | Milestone |

### Compass Checklist
- [ ] FR-xxx ... | Px | AC: ... | verify: ...
```
