<!--
  Cartographer filled example — e-commerce "Checkout & Payment" flow
  A demo PRD showing how the 15 modules work together, and a requirement style that passes prd_lint.py.
  Requirement line format: FR/NFR-<module>-<n>: The system shall <behavior>. | P0 | AC: <verifiable> | Source: <persona/objective> | Depends: <FR-x or ->
-->

# Checkout & Payment PRD

| Field | Value |
|---|---|
| Author / PM | Pei-Shan Lin |
| Version | v1.0 |
| Created | 2026-06-13 |
| Tier | 🔴 heavy |
| Mode | draft |
| Sensitive scope | [x]PII [x]money [ ]health data [x]permissions → §8 required |

### Changelog
| Version | Date | Summary | Author |
|---|---|---|---|
| v0.1 | 2026-06-10 | Initial draft: background & objectives | Pei-Shan Lin |
| v1.0 | 2026-06-13 | Completed functional/NFR/security/handoff, passes lint | Pei-Shan Lin |

---

## 1. Background & Problem

**Problem**: The current checkout has too many steps, driving high abandonment, and can't support multiple payment methods.
**Evidence**:
- Checkout abandonment 38% (GA, 2026/03–05); biggest funnel drop at "enter address" and "payment result".
- Top complaints include two on "payment failed with no reason" and "too many address fields" (support system, ~1,240 last quarter).
- Competitor B shipped 3-step checkout + mobile pay, externally estimated ~32% abandonment.
**Why now**: The current checkout is a 5-year-old monolith page that can't extend to multiple providers; it will block next quarter's subscription launch.
**Current/existing solution**: Single credit card, 5-step form, no guest checkout.
**Cost of inaction**: Sustained 38% abandonment, estimated ~NT$4.2M monthly revenue lost; blocks the subscription roadmap.

## 2. Objectives & Success Metrics

**North Star**: monthly "successful checkout orders".

| ID | Goal | Current → Target | Deadline | Measurement |
|----|------|------------------|----------|-------------|
| O-1 | Checkout success rate | 99.2% → 99.5% | 2026 Q3 | `checkout_succeeded / checkout_started` |
| O-2 | Checkout abandonment | 38% → 30% | 2026 Q3 | funnel events `cart→address→pay→done` |
| O-3 | Mobile-pay share | 0% → 25% | 2026 Q4 | `payment_method` dimension |

**Guardrails**: payment-related complaints must not rise > 5% vs last quarter; double-charge events = 0.
**Hypotheses (unvalidated, see §3)**: ⚠️assumption one-tap mobile pay cuts abandonment ~8%.

## 3. Assumptions, Constraints & Risks

**Assumptions**
- A-1: Most customers already use Apple/Google Pay. | validation: 5% canary measuring adoption before launch | owner: PM
- A-2: Payment provider X monthly SLA ≥ 99.95%. | validation: contract SLA + post-launch monitoring | owner: Backend

**Constraints**
- C-1: Must run on the existing Kubernetes cluster, no new cloud vendor.
- C-2: Card-data handling must comply with PCI-DSS; the system must not touch plaintext card numbers.
- C-3: Complete before peak season (Double 11), hard deadline 2026/10/15.

**Risk register**
| ID | Risk | Prob | Impact | Mitigation | Owner |
|----|------|------|--------|------------|-------|
| R-1 | Callback delay causes double charge | Med | High | Idempotency key + reconciliation retry + alert | Backend |
| R-2 | 10x peak traffic crushes checkout | Med | High | Load test + autoscale + queue page | SRE |
| R-3 | Users won't save a card (A-1 false) | High | Med | Guest checkout + third-party pay | PM |

## 4. Stakeholders & RACI

| Role | Cares about | Fears most |
|------|-------------|------------|
| End user | Quick, safe checkout | Failed charge, leaked PII |
| Support | Self-serviceable, traceable | A flood of "payment failed" tickets |
| Security/compliance | Compliance, auditability | Mishandled card/PII |
| Finance/ops | Correct reconciliation | Double charge, unbalanced books |
| Payment provider X (external) | Spec-compliant integration | Over-quota, PCI violation |

**RACI**
| Decision | PM | Eng | Design | Security | Compliance |
|----------|----|----|--------|----------|-----------|
| Feature scope & priority | A | C | C | C | I |
| Payment provider selection | C | R | I | C | A |
| PII / card handling | C | R | I | A | C |

## 5. User Stories & Journey

### Persona
**P1 repeat buyer — Yi-Jun**: 35, office worker, mostly mobile, card saved. Goal: checkout in 3 steps. Pain: tedious address, payment failures with no hint. Success: completes in 60s (links to O-2).
**P2 first-time guest — Da-Wei**: 28, first purchase, doesn't want to register. Goal: register-free quick checkout. Pain: forced registration makes him quit. Success: guest checkout succeeds (links to O-2).

### Anti-persona (not for whom)
- Bulk wholesale buyers (need quotes/net terms/batch invoice edits) → route to the sales line (logged in §10).

### Main journey
Cart → enter/select address → choose payment → paying → ✅ success page
　branches: ❌ payment failed (retry/switch) / ⏳ timeout (order pending + notify) / 🔌 disconnect (keep cart, resume)

## 6. Functional Requirements

### 6.1 Address
FR-ADDR-01: The system shall pre-fill the user's default address when logged in. | P1 | AC: when logged in with a default address, the field is pre-filled and editable | Source: P1 Yi-Jun / O-2 | Depends: -
FR-ADDR-02: The system shall validate postal-code format on blur and show an inline error. | P1 | AC: a non-5-digit value shows "postal code must be 5 digits" within 200ms of blur | Source: P1 Yi-Jun "tedious address" / O-2 | Depends: -

### 6.2 Payment
FR-PAY-01: The system shall create a payment intent and return a payment id on checkout confirmation. | P0 | AC: returns 200 with paymentId and order status = pending_payment | Source: Scenario #1 / O-1 | Depends: -
FR-PAY-02: The system shall support credit card and mobile pay (Apple/Google Pay). | P0 | AC: both methods complete one sandbox authorization | Source: P1 Yi-Jun / O-3 | Depends: FR-PAY-01
FR-PAY-03: The system shall mark the order pending and trigger a reconciliation retry after a 30s callback timeout. | P0 | AC: at second 31 order status = pending; at most 3 retries within 5 minutes; each retry writes an audit log | Source: Scenario #2 interrupt / O-1 | Depends: FR-PAY-01
FR-PAY-04: The system shall provide register-free guest checkout. | P0 | AC: a non-logged-in user can complete checkout with email + address and receive an order confirmation email | Source: P2 Da-Wei / O-2 | Depends: FR-PAY-01

### 6.3 Negative / edge / state
FR-PAY-05: The system shall, on payment failure, show a comprehensible reason and offer retry or switch method. | P0 | AC: on card decline, show "issuer declined, try another card or contact your issuer" and keep the cart | Source: P1 Yi-Jun "no hint on failure" / O-1 | Depends: FR-PAY-02
FR-PAY-06: The system shall handle duplicate checkout requests idempotently, creating no duplicate order or charge. | P0 | AC: the same idempotency key returns the first result; order and charge happen once each | Source: R-1 / O-1 | Depends: FR-PAY-01
FR-CART-01: The system shall preserve the cart after a disconnect so the user can resume checkout on return. | P1 | AC: after reconnect, cart contents and checkout progress are not lost | Source: Scenario disconnect / O-2 | Depends: -
FR-CART-02: The system shall block entering checkout when the cart is empty or the amount is 0. | P2 | AC: clicking checkout on an empty cart shows a hint and creates no payment intent | Source: edge / O-1 | Depends: -

## 7. Non-Functional Requirements

NFR-PERF-01: The system shall keep p95 latency from checkout submit to result below 1.5 seconds. | P0 | AC: at peak 500 QPS, p95 < 1.5s and p99 < 3s | Source: P1 Yi-Jun / O-2 | Depends: -
NFR-SLA-01: The system shall maintain payment-service monthly availability of at least 99.95%, degrading to notify-later on provider outage. | P0 | AC: monthly downtime < 22 minutes; on provider outage, order moves to pending and notifies | Source: A-2 / guardrail | Depends: -
NFR-OBS-01: The system shall emit checkout_* events per payment and alert when the failure rate exceeds threshold. | P1 | AC: failure rate > 2% for 5 consecutive minutes triggers PagerDuty | Source: O-1 / R-2 | Depends: -
NFR-A11Y-01: The system shall make the full checkout keyboard-operable and WCAG 2.1 AA compliant. | P1 | AC: checkout completable by keyboard; contrast and labels pass an axe scan | Source: accessibility compliance | Depends: -
NFR-I18N-01: The system shall support zh-TW and en, showing currency and thousands separators per locale. | P2 | AC: switching locale renders correct money format and copy | Source: market expansion | Depends: -

## 8. Security, Privacy & Compliance

### 8.1 Data classification
| Data | Class | Storage/retention | Access control | Encryption |
|------|-------|-------------------|----------------|------------|
| Card number | Sensitive (PCI) | Not stored, tokenized | No one reads plaintext | TLS throughout + not stored |
| Name/address/email | PII | Encrypted columns, retained 2 years | Role-authorized + audited | Encrypted at rest |
| Order amount/status | Internal | Normal | Role-authorized | Encrypted in transit |

### 8.2 Threats & defenses
- Replay/double charge (trust boundary) → FR-PAY-06 idempotency + NFR-SEC-01 authz
- Unauthorized access to payment API → NFR-SEC-01
- Card-number leak → NFR-PRIV-01 not stored

NFR-SEC-01: The system shall require OAuth2 authorization and a one-time idempotency key on all payment APIs and reject replays. | P0 | AC: missing token returns 401; replaying the same idempotency key returns 200 but does not double-charge | Source: R-1 / security | Depends: -

### 8.3 Compliance & privacy
NFR-PRIV-01: The system shall not store full card numbers, only the token and last four digits. | P0 | AC: full-text scan of DB and logs finds no 16-digit card number | Source: C-2 PCI | Depends: -
NFR-PRIV-02: The system shall provide a user data-deletion request completed within 30 days. | P1 | AC: after deletion the user's PII is unqueryable via any interface (GDPR Art. 17) | Source: compliance | Depends: -

## 9. Data & Integration

### 9.1 Data model
```
Order:   { id, userId|null, items[], amount, currency, status, createdAt }
  status: cart → pending_payment → paid → fulfilled | failed | refunded
Payment: { id, orderId, provider, token, last4, status, idempotencyKey }
```
(Each status transition maps to a §6 functional/negative requirement.)

### 9.2 Interface contracts
```
POST /api/checkout
  req:  { orderId, paymentMethodId, idempotencyKey }
  resp: 200 {paymentId, status} | 402 payment failed | 409 duplicate | 401 unauthorized
  idempotency: same idempotencyKey returns the first result (FR-PAY-06)
events: checkout_started / checkout_succeeded / checkout_failed (for O-1/O-2 metrics, NFR-OBS-01)
```

### 9.3 Platform support matrix
| Platform | Min version | Notes |
|----------|-------------|-------|
| iOS Safari | 15+ | Apple Pay |
| Android Chrome | last 2 versions | Google Pay |
| Desktop | Chrome/Edge/Firefox last 2 | — |

### 9.4 Third-party dependencies
| Dependency | Use | Limit | Behavior on failure |
|------------|-----|-------|---------------------|
| Payment provider X | Card/mobile-pay authorization | 50 req/s; PCI | Degrade to notify-later (R-1, NFR-SLA-01) |
| SMS provider | Order notifications | Quota | Fall back to email |

## 10. Scope Boundary

**In scope**: guest checkout, saved-card pay, credit card + Apple/Google Pay, zh-TW/en.
**Out of scope (this cycle)**: wholesale quotes/net terms (→ sales line), crypto payment, installments, other locales. Reason: off the O-1/O-2 cycle objectives, and adds PCI and schedule risk.
**Next (maybe, not a promise)**: installments, convenience-store codes, Japanese.

## 11. Open Questions

| ID | Question | Impact | Owner | Ruling by |
|----|----------|--------|-------|-----------|
| Q-1 | Should guest checkout require email verification (conversion vs fraud)? | FR-PAY-04 | PM + risk | before design freeze |
| Q-2 | Should refunds go through the original channel? | refund flow | Backend | before M2 |

## 12. Milestones & Release Slices

**Dependencies**: NFR-SEC-01 → (prerequisite for all PAY); FR-PAY-01 → FR-PAY-02 → FR-PAY-03; FR-PAY-01 → FR-PAY-06

| Milestone | Slice content | Requirements | DoD | Hard date |
|-----------|---------------|--------------|-----|-----------|
| M1 | Guest credit-card checkout end-to-end | FR-PAY-01,03,04,05,06; NFR-SEC-01; NFR-PERF-01 | Real sandbox payment succeeds + load test 500 QPS passes | — |
| M2 | Saved card + mobile pay + address polish | FR-PAY-02; FR-ADDR-01,02; NFR-I18N-01 | Apple/Google Pay pass, A11Y scan passes | 2026/10/15 before peak |

## 13. Glossary & Competitive Analysis

### Glossary
| Term | Definition |
|------|------------|
| Abandonment rate | Share entering checkout but not completing = 1 − checkout_succeeded/checkout_started |
| Tokenization | Replacing the card number with a meaningless token so the system never touches plaintext (shrinks PCI scope) |
| Idempotency key | An identifier recognizing duplicate requests, ensuring one operation takes effect once |
| P0–P3 | Priority. P0 launch-blocking / P3 future. (Maps to AirPods P1–P10: P0≈P10) |

### Competitive / current-state
| Dimension | Us (target) | Competitor A | Competitor B |
|-----------|-------------|--------------|--------------|
| Checkout steps | ≤3 | 5 | 3 |
| Mobile pay | Apple/Google Pay | Card only | Apple Pay |
| Guest checkout | ✅ | ❌ | ✅ |
| Abandonment (est.) | target 30% | ~40% | ~32% |
**Differentiated positioning**: fewest steps + mobile pay + guest checkout together (maps to O-2).

## 14. Handoff to Compass

### Traceability matrix
| Requirement | Source | Objective | AC summary | Priority | Milestone |
|-------------|--------|-----------|------------|----------|-----------|
| FR-PAY-01 | Scenario #1 | O-1 | returns 200 with paymentId | P0 | M1 |
| FR-PAY-04 | P2 Da-Wei | O-2 | guest can complete checkout | P0 | M1 |
| FR-PAY-06 | R-1 | O-1 | idempotent, no double charge | P0 | M1 |
| NFR-SEC-01 | Security | Guardrail | missing token returns 401 | P0 | M1 |
| NFR-PRIV-01 | C-2 PCI | Guardrail | no plaintext card found | P0 | M1 |
| FR-PAY-02 | P1 Yi-Jun | O-3 | both methods succeed | P0 | M2 |

**Orphan check**: every requirement has a source; O-1/O-2/O-3 each have a serving requirement. ✅

### Compass Checklist
- [ ] FR-PAY-01 create payment intent | P0 | AC: returns 200 with paymentId | verify: integration test
- [ ] FR-PAY-03 timeout → pending | P0 | AC: s31 = pending, ≤3 retries in 5min | verify: integration test
- [ ] FR-PAY-04 guest checkout | P0 | AC: email+address completes | verify: integration test
- [ ] FR-PAY-06 idempotent handling | P0 | AC: same key no double charge | verify: integration test
- [ ] NFR-SEC-01 payment API authz | P0 | AC: missing token returns 401 | verify: security test (test-first)
- [ ] NFR-PRIV-01 no plaintext card | P0 | AC: full-text scan finds no 16-digit | verify: scan script
