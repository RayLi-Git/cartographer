<!--
  Cartographer review → regenerate demo — the bad "Points feature" PRD reworked into a passing version.
  All 🔴 fictional test data; safe to delete.
-->

# Membership Points & Redemption PRD (regenerated)

| Field | Value |
|---|---|
| Author / PM | Demo |
| Version | v1.0 |
| Tier | 🔴 heavy | Mode | draft (reworked from a review) |
| Sensitive scope | [x]PII [x]value(points) [x]permissions → §8 required |

## 1. Background & Problem
**Problem**: Members have no incentive to return; repeat-purchase rate is low and there is no post-purchase attachment to the brand.
**Evidence**: 🔴 repeat-purchase rate 21% over the last 3 months; monthly active members only 12%; "no reason to buy again" ranks second in the complaint survey.
**Why now**: Competitors have shipped points programs; member churn is accelerating.
**Current state**: No accumulation mechanism after purchase whatsoever.
**Cost of inaction**: Continued member churn, rising marketing cost.

## 2. Objectives & Success Metrics
**North Star**: monthly members who redeem successfully.
| ID | Goal | Current → Target | Deadline | Measurement |
|----|------|------------------|----------|-------------|
| O-1 | Monthly active member rate | 12% → 18% | 2026 Q4 | MAU / total members |
| O-2 | Points redemption conversion | 0% → 8% | 2026 Q4 | redeem_succeeded / active_member |
| O-3 | Repeat-purchase rate | 21% → 28% | 2027 Q1 | members re-purchasing within 90 days |
**Guardrail**: points-related fraud/abuse incidents = 0.

## 3. Assumptions, Constraints & Risks
**Assumptions**: A-1 members care about a points incentive | validation: canary the redemption adoption rate post-launch | owner: PM
**Constraints**: C-1 points changes must be auditable (finance requirement); C-2 member data must comply with privacy law
**Risks**
| ID | Risk | Prob | Impact | Mitigation | Owner |
|----|------|------|--------|------------|-------|
| R-1 | Duplicate redemption / inconsistent concurrent deductions | Med | High | Idempotency key + transaction lock | Backend |
| R-2 | Points-farming arbitrage | Med | High | Earn-rate threshold + alert + manual review | Risk |
| R-3 | PII leak | Low | High | Encryption + least privilege + audit | Security |

## 4. Stakeholders & RACI
| Role | Cares about | Fears most |
|------|-------------|------------|
| Member | Easy-to-understand points, smooth redemption | Points disappearing, redemption failing |
| Marketing | Drives engagement/repeat purchase | Rules too complex, no adoption |
| Finance | Points = liability, reconcilable | Books don't balance, gets arbitraged |
| Security/privacy | Compliance, abuse prevention | PII leak, account fraud |

**RACI** (single A)
| Decision | Marketing | Eng | Finance | Security |
|----------|-----------|-----|---------|----------|
| Points rules | A | C | C | I |
| Points-change audit | I | R | A | C |
| PII / abuse prevention | I | R | I | A |

## 5. User Stories & Journey
**P1 repeat buyer — Mia**: spends often, wants to redeem points for perks. Goal: see points clearly, redeem smoothly. Links to O-2.
**P2 first-time buyer**: just joined, wants to know how to earn points. Links to O-1.
**Anti-persona**: pure points-farming arbitrageurs (not served, blocked by §8 abuse prevention).
**Journey**: spend → earn points → check points → pick a gift → redeem & deduct → receive; branches 🚫 insufficient points, ⏳ redemption timeout, 🔁 duplicate submit.

## 6. Functional Requirements
FR-PTS-01: The system shall accrue points by rule after a member completes a purchase. | P0 | AC: after a successful purchase, points accrue by ratio and the change is queryable | Source: P1 Mia / O-1 | Depends: -
FR-PTS-02: The system shall let members look up their points-transaction history. | P1 | AC: shows the last 12 months of changes with time and reason | Source: P1 Mia / O-1 | Depends: FR-PTS-01
FR-PTS-03: The system shall reflect the points balance in real time after a purchase. | P1 | AC: after a purchase, the points balance updates within p95 1 second | Source: P1 Mia / O-1 | Depends: FR-PTS-01
FR-PTS-04: The system shall let an authorized admin adjust a member's points with an audit trail. | P0 | AC: every adjustment records who/when/before/after; unauthorized access returns 403 | Source: Finance / guardrail | Depends: -
FR-RDM-01: The system shall let members redeem gifts with points and deduct the corresponding points. | P0 | AC: a successful redemption deducts points and creates a redemption record; insufficient points returns 422 | Source: P1 Mia / O-2 | Depends: FR-PTS-01
FR-RDM-02: The system shall handle duplicate redemption requests idempotently, with no double deduction. | P0 | AC: the same idempotency key deducts points only once | Source: R-1 / O-2 | Depends: FR-RDM-01

## 7. Non-Functional Requirements
NFR-PERF-01: The system shall keep the points-balance update below p95 1 second. | P1 | AC: p95 < 1s under peak | Source: O-1 | Depends: -
NFR-OBS-01: The system shall alert when the redemption failure rate exceeds threshold. | P1 | AC: redemption failure rate > 2% for 5 consecutive minutes triggers an alert | Source: O-2 | Depends: -

## 8. Security, Privacy & Compliance
### 8.1 Data classification
| Data | Class | Access control |
|------|-------|----------------|
| Member name / phone | PII | Role-authorized + audited |
| Points balance / changes | Value (equiv. liability) | Role-authorized + audited |

NFR-SEC-01: The system shall require login authorization on all points and redemption APIs. | P0 | AC: unauthenticated access returns 401 | Source: Security | Depends: -
NFR-SEC-02: The system shall block and alert when a single account's earn frequency exceeds threshold, to prevent arbitrage. | P0 | AC: over-threshold requests return 429 and log a risk event | Source: R-2 / guardrail | Depends: -
NFR-PRIV-01: The system shall allow only the member themselves and authorized support to read their PII. | P0 | AC: unauthorized access returns 403 and writes an audit log | Source: Security / PII | Depends: -

## 9. Data & Integration
### 9.1 Data model
```
PointAccount { memberId, balance, updatedAt }
PointTxn     { id, memberId, type(earn|redeem|adjust), amount, reason, operatorId, createdAt }
Redemption   { id, memberId, rewardId, cost, status, idempotencyKey }
  status: created → confirmed → fulfilled | failed
```
### 9.2 Interface contracts
```
POST /api/redemptions → 201 {id,status} | 422 insufficient points | 409 duplicate | 401
GET  /api/points/{memberId} → 200 | 403 unauthorized
```
### 9.3 Platform matrix: member iOS15+ / Android last 2 versions; back office Web
### 9.4 Third-party: gift-inventory service — on failure, pause redemption and prompt to try later

## 10. Scope Boundary
**In scope**: earn / query / redeem / admin adjustment.
**Out of scope**: gifting points to others, cross-brand universal points, buying points.
**Next (not a promise)**: points-expiry reminders, birthday double points.

## 11. Open Questions
| ID | Question | Owner | Ruling by |
|----|----------|-------|-----------|
| Q-1 | Should points have an expiry (finance liability vs experience)? | PM + Finance | before design freeze |
| Q-2 | Are points refunded after a redemption is cancelled? | Backend | before M2 |

## 12. Milestones & Release Slices
**Dependencies**: NFR-SEC-01 prerequisite; FR-PTS-01 → FR-RDM-01 → FR-RDM-02
| Milestone | Slice | Requirements | DoD | Hard date |
|-----------|-------|--------------|-----|-----------|
| M1 | Earn + query + real-time balance | FR-PTS-01,02,03; NFR-SEC-01, NFR-PRIV-01 | spend → earn → query end-to-end | — |
| M2 | Redeem + idempotency + abuse prevention + admin | FR-RDM-01,02; FR-PTS-04; NFR-SEC-02, NFR-OBS-01 | redemption end-to-end + arbitrage-block verified | — |

## 13. Glossary & Competitive Analysis
### Glossary
| Term | Definition |
|------|------------|
| Redemption conversion | members redeeming successfully / active members |
| Idempotency key | an identifier ensuring a duplicate redemption request takes effect only once |
### Competitive / current-state
| Dimension | Us | Competitor A | Current |
|-----------|----|--------------|---------|
| Points program | ✅ | ✅ | ❌ |
| Abuse prevention | ✅ | partial | — |
**Differentiation**: clear, easy-to-understand points + rigorous abuse prevention (maps to O-2 / guardrail).

## 14. Handoff to Compass
### Traceability matrix
| Requirement | Source | Objective | AC summary | Priority | Milestone |
|-------------|--------|-----------|------------|----------|-----------|
| FR-PTS-01 | P1 Mia | O-1 | accrue points after purchase | P0 | M1 |
| FR-PTS-02 | P1 Mia | O-1 | query last 12 months | P1 | M1 |
| FR-PTS-03 | P1 Mia | O-1 | balance updates in 1s | P1 | M1 |
| FR-PTS-04 | Finance | Guardrail | adjustment leaves audit trail | P0 | M2 |
| FR-RDM-01 | P1 Mia | O-2 | redeem & deduct | P0 | M2 |
| FR-RDM-02 | R-1 | O-2 | idempotent, no double deduction | P0 | M2 |
| NFR-PERF-01 | O-1 | O-1 | p95 < 1s | P1 | M1 |
| NFR-OBS-01 | O-2 | O-2 | redemption-failure alert | P1 | M2 |
| NFR-SEC-01 | Security | Guardrail | unauthenticated 401 | P0 | M1 |
| NFR-SEC-02 | R-2 | Guardrail | arbitrage 429 | P0 | M2 |
| NFR-PRIV-01 | Security / PII | Guardrail | unauthorized 403 | P0 | M1 |

**Orphan check**: all 11 requirements have a source; O-1/O-2 each have a serving requirement (O-3 is driven by reaching O-1/O-2). ✅

### Compass Checklist
- [ ] FR-PTS-01 accrue points | P0 | AC: accrue by rule after purchase | verify: integration test
- [ ] FR-RDM-01 redeem & deduct | P0 | AC: deduct + record, insufficient 422 | verify: integration test
- [ ] FR-RDM-02 idempotent redemption | P0 | AC: same key deducts once | verify: integration test
- [ ] FR-PTS-04 admin adjustment | P0 | AC: audit trail, unauthorized 403 | verify: security test
- [ ] NFR-SEC-02 abuse prevention | P0 | AC: over-threshold 429 + risk event | verify: security test
- [ ] NFR-PRIV-01 least-privilege PII read | P0 | AC: unauthorized 403 + audit | verify: security test + scan
