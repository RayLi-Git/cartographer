# §06 Functional Requirements ★ | The heart of the PRD

> The most core — and most often botched — section. The AirPods PRD made a fatal inconsistency here: its regulation tests (7.x) are each verifiable, but its features (1–5) often aren't (`1.6 as small as possible`, `3.5 intuitive for all`). **I do the opposite — every functional requirement is mandatorily verifiable, no exceptions for features.**

---

## The iron rule per requirement: atomic + numbered + priority + AC + source

```
FR-PAY-03: The system shall mark the order pending and trigger a reconciliation retry after a 30s payment-callback timeout.
  Priority: P0          # P0 launch-blocking / P1 high / P2 medium / P3 future
  AC: at second 31 order status = pending; at most 3 retries within 5 min; each retry writes an audit log
  Source: Scenario #2 interrupted checkout / Objective O-1 "checkout success ≥ 99.5%"
  Depends: FR-PAY-01 (create payment intent)
```

| Element | Rule |
|---|---|
| **Atomic** | One thing per requirement. "and/also" chaining multiple actions → split |
| **Numbered** | `FR-<module>-<n>`, unique across the PRD, referenceable by the §14 matrix |
| **shall clause** | "The system shall <observable behavior>", explicit subject, observable verb |
| **Priority** | P0/P1/P2/P3, and you can say **why** that level |
| **AC** | Verifiable: has numbers, or Given/When/Then, or explicit state transition |
| **Source** | Traces to a persona/scenario + an objective (question any requirement with no source) |

---

## Beyond the happy path: mandatory "negative / edge / state"

AirPods' 3.4 "auto-pause on removal" wrote only the forward flow. Software must add:

- **Negative**: payment failed, insufficient funds, expired card, double submit → one requirement each
- **Edge**: amount = 0, empty cart, stock hitting exactly zero, concurrent orders
- **States** (the UI five states): empty / loading / success / error / offline — for every key screen
- **Idempotency/concurrency**: retryable operations need an idempotency key and defined duplicate-request behavior

> Rule of thumb: one happy-path requirement averages 2–4 negative/edge/state requirements. After writing a main flow, ask "how does it break?"

---

## Good vs bad

✅ `FR-ADDR-02: The system shall validate postal-code format on blur and show an inline error. Priority P1 | AC: entering a non-5-digit value shows "postal code must be 5 digits" within 200ms of blur | Source: P1 Yi-Jun "address too tedious"`

❌ `Checkout should be simple, easy, and smooth.` (unmeasurable, unnumbered, no AC, no source — same disease as AirPods 3.5)

---

## Common traps

- **One line, three things** → split.
- **Adjectives as requirements** (fast/good/friendly/intuitive/seamless/as possible) → `prd_lint.py` blocks them; turn into numbers or observable behavior.
- **Only the happy path** → add negative/edge/state.
- **Everything P0** → all-highest = no priority; force yourself to tier.
- **Orphan requirement with no source** → go back to §05 for a persona; if none, delete or move to §11.

---

## Quality gate (pass before §07)

- ✅ Every requirement is "atomic + numbered + priority + AC + source" (`prd_lint.py` shows 0 blocking)
- ✅ Every main flow has negative/edge/state requirements
- ✅ Priorities are tiered, and each P0 can justify being launch-blocking
- ✅ No unmeasurable adjectives remain

---

## Format snippet

```markdown
## 6. Functional Requirements

### 6.1 <module, e.g. "Payment">
FR-PAY-01: The system shall ... | P0 | AC: ... | Source: Scenario #x / O-x | Depends: -
FR-PAY-02: The system shall ... | P1 | AC: Given... When... Then... | Source: ...
  # negative / edge / state
FR-PAY-03: The system shall, on payment failure, ... | P0 | AC: ...
```
