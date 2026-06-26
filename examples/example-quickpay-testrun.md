<!--
  Cartographer test run — custom topic "QuickPay one-page mobile checkout"
  Purpose: stress-test the whole Cartographer flow (14 sections + lint), not a real project.
  Requirement line format: FR/NFR-<module>-<n>: The system shall <behavior>. | Px | AC: <verifiable> | Source: <persona/objective> | Depends: <FR-x or ->
-->

# QuickPay One-Page Mobile Checkout PRD

| Field | Value |
|---|---|
| Author / PM | (test run, filled by Cartographer) |
| Version | v1.0 |
| Created | 2026-06-13 |
| Tier | 🔴 heavy |
| Mode | draft |
| Sensitive scope | [x]PII [x]money [ ]health data [x]permissions → §8 required |

### Changelog
| Version | Date | Summary | Author |
|---|---|---|---|
| v1.0 | 2026-06-13 | Test run: completed all 14 sections in one pass and passes lint | Cartographer |

---

## 1. Background & Problem

**Problem**: Mobile checkout on the DTC brand site spans 4 pages; users repeatedly switch keyboards and scroll on mobile, with heavy drop-off before payment.
**Evidence**: ⚠️assumption (test data)
- Mobile checkout abandonment 52%, desktop 31% (the 21pp gap is concentrated on mobile).
- Top three support tickets: "can't see the monthly amount for installments", "the card-number page resets and I have to start over", "don't know whether the charge went through".
- Competitor C has shipped one-page + Apple Pay, mobile abandonment externally estimated ~40%.
**Why now**: We need to lift mobile conversion before peak season; the current checkout is a rented third-party hosted page that can't do one-page or installments, blocking the owned-membership and subscription roadmap.
**Current/existing solution**: third-party hosted checkout, credit card only, 4-page flow, no installments, no guest checkout.
**Cost of inaction**: keeping 52% mobile abandonment, estimated ~NT$2.8M lost per month; and the owned-membership/subscription roadmap can't start.

## 2. Objectives & Success Metrics

**North Star**: monthly "successful mobile checkout orders".

| ID | Goal | Current → Target | Deadline | Measurement |
|----|------|------------------|----------|-------------|
| O-1 | Mobile checkout abandonment | 52% → 40% | 2026 Q3 | funnel `mobile: cart→pay→done` |
| O-2 | Checkout completion p95 time | 110s → 70s | 2026 Q3 | `checkout_started→succeeded` time distribution |
| O-3 | Installment-payment adoption | 0% → 15% | 2026 Q4 | `payment_method=installment` share |

**Guardrails**: payment complaint volume must not rise > 5% vs last quarter; double-charge events = 0; refund-handling time must not worsen.
**Hypothesis (unvalidated, see §3)**: ⚠️assumption one-page can cut mobile abandonment by ~10pp.

## 3. Assumptions, Constraints & Risks

**Assumptions**
- A-1: The primary mobile audience's devices support Apple/Google Pay. | validation: 5% canary measuring adoption before launch | owner: PM
- A-2: Installment provider monthly SLA ≥ 99.9%. | validation: contract SLA + post-launch monitoring | owner: Backend
- A-3: One-page won't reduce conversion due to an over-long form. | validation: A/B control group | owner: PM

**Constraints**
- C-1: Card data must comply with PCI-DSS; the system must not touch plaintext card numbers (reuse tokenization).
- C-2: Reuse the existing cloud environment, no new cloud vendor.
- C-3: Complete before peak season, hard deadline 2026/10/15.

**Risk register**
| ID | Risk | Prob | Impact | Mitigation | Owner |
|----|------|------|--------|------------|-------|
| R-1 | Payment callback delay causes double charge | Med | High | Idempotency key + reconciliation retry + alert | Backend |
| R-2 | Over-long one-page form reduces conversion (A-3 false) | Med | Med | A/B test + progressive disclosure | PM |
| R-3 | High installment-rejection rate, broken experience | Med | Med | Immediate fallback to one-time payment on rejection | Backend |

## 4. Stakeholders & RACI

| Role | Cares about | Fears most |
|------|-------------|------------|
| End user | Fill once on mobile, see the monthly amount | Failed charge, leaked PII |
| Support | Self-serviceable payment status, traceable | A flood of "did the charge go through" tickets |
| Security/compliance | PCI compliance, auditability | Card/PII violation |
| Finance/ops | Correct reconciliation, installment payouts match | Double charge, unbalanced books |
| Installment provider (external) | Spec-compliant integration | Over-quota, risk-control violation |

**RACI** (R execute / A accountable / C consulted / I informed)
| Decision | PM | Eng | Design | Security | Compliance |
|----------|----|----|--------|----------|-----------|
| Feature scope & priority | A | C | C | C | I |
| Installment-provider selection | C | R | I | C | A |
| PII / card handling | C | R | I | A | C |

## 5. User Stories & Journey

### Persona
**P1 mobile repeat buyer — Sophie**: 30, orders on mobile during her commute, card saved. Goal: fill one page, finish in 60 seconds. Pain: the page resets and she has to refill. Success: completes on one mobile page (links to O-1, O-2).
**P2 first-time buyer who wants installments — Alex**: 26, buying a high-ticket item and wants installments, first purchase and doesn't want to register. Goal: see the monthly amount, check out without registering. Pain: installment info is opaque. Success: guest + installment complete (links to O-3).

### Anti-persona (not for whom)
- B2B bulk procurement (needs quotes / net terms) → route to the sales line (logged in §10).

### Main journey
Cart → one-page checkout (address + payment method + installment choice on the same page) → paying → ✅ success page
 branches: ❌ payment failed (retry / switch method) / ⏳ timeout (order pending + notify) / 🔌 disconnect (keep progress, resume) / 🚫 installment rejected (fallback to pay in full)

## 6. Functional Requirements

### 6.1 One-page checkout
FR-CHK-01: The system shall present address, payment method, and installment options together on a single page, completing input with no page change. | P0 | AC: from cart entry to submittable, 0 full-page navigations throughout | Source: P1 Sophie / O-1 | Depends: -
FR-CHK-02: The system shall auto-fill the default address and saved card when logged in. | P1 | AC: when logged in with defaults, address and card are pre-filled and editable | Source: P1 Sophie / O-2 | Depends: FR-CHK-01

### 6.2 Payment
FR-PAY-01: The system shall create a payment intent and return a payment id when the user submits checkout. | P0 | AC: returns 200 with paymentId and order status = pending_payment | Source: Scenario #1 / O-1 | Depends: -
FR-PAY-02: The system shall support three payment methods: credit card, mobile pay (Apple/Google Pay), and installments. | P0 | AC: all three methods complete one sandbox authorization | Source: P1/P2 / O-3 | Depends: FR-PAY-01
FR-PAY-03: The system shall mark the order pending and trigger a reconciliation retry after a 30s payment-callback timeout. | P0 | AC: at second 31 order status = pending; at most 3 retries within 5 minutes; each retry writes an audit log | Source: Scenario timeout / O-1 | Depends: FR-PAY-01
FR-PAY-04: The system shall provide register-free guest checkout. | P0 | AC: a non-logged-in user can complete checkout with email + address and receive an order confirmation email | Source: P2 Alex / O-1 | Depends: FR-PAY-01

### 6.3 Installments
FR-INST-01: The system shall show the per-term amount, number of terms, and total cost in real time when installments are selected. | P0 | AC: selecting any of 3/6/12 terms shows the corresponding monthly amount and total within 500ms | Source: P2 Alex "installments opaque" / O-3 | Depends: FR-PAY-02
FR-INST-02: The system shall offer a pay-in-full fallback when an installment application is rejected, without clearing the cart. | P0 | AC: after rejection, show a pay-in-full option and preserve cart and form content | Source: R-3 / O-3 | Depends: FR-INST-01

### 6.4 Negative / edge / state
FR-PAY-05: The system shall, on payment failure, show a comprehensible reason and offer retry or switch method. | P0 | AC: on card decline, show "issuer declined, try another card or contact your issuer" and keep the cart | Source: P1 Sophie / O-1 | Depends: FR-PAY-02
FR-PAY-06: The system shall handle duplicate checkout requests idempotently, creating no duplicate order or charge. | P0 | AC: the same idempotency key returns the first result; order and charge happen once each | Source: R-1 / O-1 | Depends: FR-PAY-01
FR-CHK-03: The system shall preserve checkout progress after a disconnect so the user can resume on return. | P1 | AC: after reconnect, form content and cart are not lost | Source: Scenario disconnect / O-1 | Depends: FR-CHK-01
FR-CHK-04: The system shall block entering checkout when the cart is empty or the amount is 0. | P2 | AC: clicking checkout on an empty cart shows a hint and creates no payment intent | Source: edge / O-1 | Depends: -

## 7. Non-Functional Requirements

NFR-PERF-01: The system shall keep p95 latency from checkout submit to result page below 1.5 seconds. | P0 | AC: at peak 400 QPS, p95 < 1.5s and p99 < 3s | Source: P1 Sophie / O-2 | Depends: -
NFR-SLA-01: The system shall maintain payment-service monthly availability of at least 99.95%, degrading to notify-later on provider outage. | P0 | AC: monthly downtime < 22 minutes; on provider outage, order moves to pending and notifies | Source: A-2 / guardrail | Depends: -
NFR-OBS-01: The system shall emit checkout_* events per payment and alert when the failure rate exceeds threshold. | P1 | AC: failure rate > 2% for 5 consecutive minutes triggers PagerDuty | Source: O-1 / R-1 | Depends: -
NFR-A11Y-01: The system shall make the one-page checkout keyboard-operable and WCAG 2.1 AA compliant. | P1 | AC: checkout completable by keyboard; contrast and labels pass an axe scan | Source: accessibility compliance | Depends: -
NFR-I18N-01: The system shall support zh-TW and en, showing currency and thousands separators per locale. | P2 | AC: switching locale renders correct money format and copy | Source: market expansion | Depends: -

## 8. Security, Privacy & Compliance

### 8.1 Data classification
| Data | Class | Storage/retention | Access control | Encryption |
|------|-------|-------------------|----------------|------------|
| Card number | Sensitive (PCI) | Not stored, handed to tokenization | No one reads plaintext | TLS throughout + not stored |
| Name/address/email | PII | Encrypted columns, retained 2 years per policy | Role-authorized + audited | Encrypted at rest |
| Installment application data | Sensitive (PII) | Encrypted, retained per provider spec | Role-authorized + audited | Encrypted at rest |
| Order amount/status | Internal | Normal | Role-authorized | Encrypted in transit |

### 8.2 Threats & defenses
- Replay/double charge (trust boundary) → FR-PAY-06 idempotency + NFR-SEC-01 authz
- Unauthorized access to payment API → NFR-SEC-01
- Card-number leak → NFR-PRIV-01 not stored

NFR-SEC-01: The system shall require OAuth2 authorization and a one-time idempotency key on all payment APIs and reject replays. | P0 | AC: missing token returns 401; replaying the same idempotency key returns 200 but does not double-charge | Source: R-1 / security | Depends: -

### 8.3 Compliance & privacy
NFR-PRIV-01: The system shall not store full card numbers, only the token and last four digits. | P0 | AC: full-text scan of DB and logs finds no 16-digit card number | Source: C-1 PCI | Depends: -
NFR-PRIV-02: The system shall provide a user data-deletion request completed within 30 days. | P1 | AC: after deletion the user's PII is unqueryable via any interface (GDPR Art. 17) | Source: compliance | Depends: -

## 9. Data & Integration

### 9.1 Data model
```
Order:   { id, userId|null, items[], amount, currency, status, createdAt }
  status: cart → pending_payment → paid → fulfilled | failed | refunded
Payment: { id, orderId, provider, method, token, last4, status, idempotencyKey }
  method: card | wallet | installment
Installment: { id, paymentId, terms, perTermAmount, totalCost, approvalStatus }
```
(Each status transition maps to a §6 functional/negative requirement.)

### 9.2 Interface contracts
```
POST /api/checkout
  req:  { orderId, paymentMethodId, installmentTerms|null, idempotencyKey }
  resp: 200 {paymentId, status} | 402 payment failed | 409 duplicate | 401 unauthorized | 422 installment rejected
  idempotency: same idempotencyKey returns the first result (FR-PAY-06)
events: checkout_started / checkout_succeeded / checkout_failed / installment_selected
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
| Card payment provider | Card/mobile-pay authorization | 50 req/s; PCI | Degrade to notify-later (R-1, NFR-SLA-01) |
| Installment provider | Installment review and disbursement | Risk rules; quota | Fallback to pay in full (FR-INST-02, R-3) |
| SMS provider | Order notifications | Quota | Fall back to email |

## 10. Scope Boundary

**In scope**: one-page mobile checkout, guest checkout, credit card + Apple/Google Pay + installments, zh-TW/en.
**Out of scope (this cycle)**: B2B quotes/net terms (→ sales line), cryptocurrency, convenience-store codes, subscription billing, other locales. Reason: off this cycle's O-1/O-2/O-3 objectives, and adds schedule and risk-control risk.
**Next (maybe, not a promise)**: subscriptions, convenience-store codes, Japanese.

## 11. Open Questions

| ID | Question | Impact | Owner | Ruling by |
|----|----------|--------|-------|-----------|
| Q-1 | Should guest checkout require email verification (conversion vs fraud)? | FR-PAY-04 | PM + risk | before design freeze |
| Q-2 | Should installment applications be retained for retry after rejection? | FR-INST-02 | Backend + compliance | before M2 |
| Q-3 | Should refunds go through the original channel (including installments)? | refund flow | Backend | before M2 |

## 12. Milestones & Release Slices

**Dependencies**: NFR-SEC-01 → (prerequisite for all PAY); FR-CHK-01 → FR-PAY-01 → FR-PAY-02 → FR-INST-01; FR-PAY-01 → FR-PAY-06

| Milestone | Slice content | Requirements | DoD | Hard date |
|-----------|---------------|--------------|-----|-----------|
| M1 | One-page guest credit-card checkout end-to-end | FR-CHK-01,03,04; FR-PAY-01,03,04,05,06; NFR-SEC-01; NFR-PERF-01 | real sandbox payment succeeds + load test 400 QPS passes | — |
| M2 | Saved card + mobile pay + installments + accessibility | FR-CHK-02; FR-PAY-02; FR-INST-01,02; NFR-A11Y-01; NFR-I18N-01 | three payment methods pass, installment fallback verified, A11Y scan passes | 2026/10/15 before peak |

## 13. Glossary & Competitive Analysis

### Glossary
| Term | Definition |
|------|------------|
| Abandonment rate | share entering checkout but not completing payment = 1 − checkout_succeeded/checkout_started |
| One-page checkout | address/payment/installments completed on a single page, no full-page navigation |
| Tokenization | replacing the card number with a meaningless token so the system never touches plaintext (shrinks PCI scope) |
| Idempotency key | an identifier recognizing duplicate requests, ensuring one operation takes effect once |
| Fallback | the alternative path offered automatically when the main path fails (here, installment rejection → pay in full) |
| P0–P3 | Priority. P0 launch-blocking / P3 future. |

### Competitive / current-state
| Dimension | Us (target) | Competitor A | Competitor C |
|-----------|-------------|--------------|--------------|
| Checkout pages | 1 | 4 | 1 |
| Mobile pay | Apple/Google Pay | Card only | Apple Pay |
| Transparent installment display | ✅ real-time monthly amount | ❌ | partial |
| Guest checkout | ✅ | ❌ | ✅ |
| Mobile abandonment (est.) | target 40% | ~55% | ~40% |
**Differentiated positioning**: one-page + transparent installment monthly amount + guest checkout, all three together (maps to O-1/O-3).

## 14. Handoff to Compass

### Traceability matrix
| Requirement | Source | Objective | AC summary | Priority | Milestone |
|-------------|--------|-----------|------------|----------|-----------|
| FR-CHK-01 | P1 Sophie | O-1 | 0 full-page navigations to complete input | P0 | M1 |
| FR-PAY-01 | Scenario #1 | O-1 | returns 200 with paymentId | P0 | M1 |
| FR-PAY-04 | P2 Alex | O-1 | guest can complete checkout | P0 | M1 |
| FR-PAY-06 | R-1 | O-1 | idempotent, no double charge | P0 | M1 |
| NFR-SEC-01 | Security | Guardrail | missing token returns 401 | P0 | M1 |
| NFR-PRIV-01 | C-1 PCI | Guardrail | no plaintext card found | P0 | M1 |
| FR-INST-01 | P2 Alex | O-3 | real-time monthly amount shown | P0 | M2 |
| FR-PAY-02 | P1/P2 | O-3 | three payment methods succeed | P0 | M2 |

**Orphan check**: every requirement has a source; O-1/O-2/O-3 each have a serving requirement. ✅

### Compass Checklist
- [ ] FR-CHK-01 one-page input | P0 | AC: 0 full-page navigations | verify: end-to-end test
- [ ] FR-PAY-01 create payment intent | P0 | AC: returns 200 with paymentId | verify: integration test
- [ ] FR-PAY-03 timeout → pending | P0 | AC: s31 = pending, ≤3 retries in 5min | verify: integration test
- [ ] FR-PAY-04 guest checkout | P0 | AC: email+address completes | verify: integration test
- [ ] FR-PAY-06 idempotent handling | P0 | AC: same idempotency key no double charge | verify: integration test
- [ ] FR-INST-01 transparent installment monthly amount | P0 | AC: monthly amount shown within 500ms | verify: end-to-end test
- [ ] FR-INST-02 installment fallback | P0 | AC: after rejection keep cart, switch to pay in full | verify: integration test
- [ ] NFR-SEC-01 payment API authz | P0 | AC: missing token returns 401 | verify: security test (test-first)
- [ ] NFR-PRIV-01 no plaintext card | P0 | AC: full-text scan finds no 16-digit | verify: scan script
