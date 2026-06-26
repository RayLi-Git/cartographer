<!--
  Cartographer interactive demo artifact — "Community Resident Maintenance-Request App" (🔴 heavy, all 14 sections walked through)
  All 🔴 fictional test data, demonstrating the section-by-section flow and lint verification only; safe to delete.
-->

# Community Maintenance-Request App PRD (demo)

| Field | Value |
|---|---|
| Author / PM | Demo |
| Version | v0.2 |
| Tier | 🔴 heavy | Mode | draft |
| Sensitive scope | [x]PII → §8 required |

## 1. Background & Problem
**Problem**: Residents file maintenance requests over a group chat plus phone calls; tickets get dropped and progress can't be tracked.
**Evidence**: 🔴 last month, 9 of 47 requests were "seen but unhandled".
**Why now**: The new management committee wants to go digital.
**Cost of inaction**: dropped tickets → resident dissatisfaction → the committee gets blamed.

## 2. Objectives & Success Metrics
**North Star**: maintenance requests successfully closed per month.
| ID | Goal | Current → Target | Deadline | Measurement |
|----|------|------------------|----------|-------------|
| O-1 | Drop rate | 19% → 5% | 2026 Q4 | read → assigned ratio |
| O-2 | Average time to close | 🔴 unknown → 3 days | 2026 Q4 | closed_at − created_at |
**Guardrail**: resident-side step count must not increase.

## 3. Assumptions, Constraints & Risks
**Assumptions**: A-1 residents have a smartphone and are willing to use an app | validation: canary the adoption rate post-launch | owner: PM
**Constraints**: C-1 runs on the committee's existing low-cost host; C-2 must comply with privacy law
**Risks**
| ID | Risk | Prob | Impact | Mitigation | Owner |
|----|------|------|--------|------------|-------|
| R-1 | Residents keep using group chat instead of the app | High | Med | Group-chat entry point routes into the app | PM |
| R-2 | Photos blow up storage | Med | Med | Compression + retention period | Eng |
| R-3 | PII leak | Low | High | Encryption + least privilege + audit | Security |

## 4. Stakeholders & RACI
| Role | Cares about | Fears most |
|------|-------------|------------|
| Resident | Request gets handled, knows progress | Seen but ignored |
| Committee | No dropped tickets, trackable | Getting blamed by residents |
| Maintenance staff | Clear dispatch | Duplicate / missed dispatch |
| Privacy officer | Compliance | PII leak |

**RACI** (single A)
| Decision | Committee | Eng | Security |
|----------|-----------|-----|----------|
| Feature scope | A | C | C |
| PII handling | C | R | A |

## 5. User Stories & Journey
**P1 resident Mrs. Carter**: doesn't know progress after filing a request. Links to O-2.
**P2 committee clerk**: needs no dropped tickets and the ability to assign. Links to O-1.
**Anti-persona**: large cross-community maintenance contractors (not served).
**Journey**: photograph & file → assign → repair → close; branches 🚫 upload failed / ⏳ unassigned past timeout.

## 6. Functional Requirements
FR-RPT-01: The system shall let a resident create a maintenance request with description, photo, and location. | P0 | AC: after submit, returns a case id and status = new | Source: P1 Mrs. Carter / O-1 | Depends: -
FR-RPT-02: The system shall let the committee assign a case to maintenance staff. | P0 | AC: after assignment, status = assigned and the assignee is notified | Source: P2 clerk / O-1 | Depends: FR-RPT-01
FR-RPT-03: The system shall let a resident view the real-time status of their case. | P1 | AC: after a status change, the resident side updates within 60 seconds | Source: P1 "don't know if it's fixed" / O-2 | Depends: FR-RPT-01
FR-RPT-04: The system shall preserve entered content and allow retry when a photo upload fails. | P2 | AC: on upload failure, show a hint and do not lose the draft | Source: edge / O-1 | Depends: FR-RPT-01

## 7. Non-Functional Requirements
NFR-PERF-01: The system shall keep the case-list load below p95 2 seconds at 200 cases. | P1 | AC: p95 < 2s at 200 cases | Source: O-2 | Depends: -
NFR-OBS-01: The system shall remind the committee when a case is unassigned for over 48 hours. | P1 | AC: notification sent when unassigned for 48h | Source: O-1 drop | Depends: FR-RPT-02

## 8. Security, Privacy & Compliance
### 8.1 Data classification
| Data | Class | Access control |
|------|-------|----------------|
| Name / unit number / phone | PII | Role-authorized + audited |
| Maintenance photos | May contain PII | Role-authorized |

NFR-PRIV-01: The system shall allow only the case's associated resident and the committee to read that case's PII. | P0 | AC: access from a non-associated account returns 403 and writes an audit log | Source: Security / PII | Depends: -
NFR-SEC-01: The system shall require login authorization on all APIs. | P0 | AC: unauthenticated access returns 401 | Source: Security | Depends: -

## 9. Data & Integration
### 9.1 Data model
```
Case { id, residentId, desc, photos[], location, status, assigneeId, createdAt, closedAt }
  status: new → assigned → in_progress → closed | reopened
```
### 9.2 Interface contracts
```
POST  /api/cases            → 201 {caseId, status} | 401
PATCH /api/cases/{id}/assign → 200 | 403 not committee | 404
GET   /api/cases/{id}        → 200 | 403 not associated
```
### 9.3 Platform matrix: resident iOS15+ / Android last 2 versions; committee Web (Chrome/Edge last 2 versions)
### 9.4 Third-party: push FCM fails → email; object storage (photos) fails → defer upload

## 10. Scope Boundary
**In scope**: request creation / assignment / status tracking.
**Out of scope**: paid online repairs, equipment warranty, cross-community sharing.
**Next (not a promise)**: resident satisfaction rating.

## 11. Open Questions
| ID | Question | Owner | Ruling by |
|----|----------|-------|-----------|
| Q-1 | How long to retain maintenance photos (privacy vs evidence)? | PM + Security | before design freeze |

## 12. Milestones & Release Slices
**Dependencies**: NFR-SEC-01 prerequisite; FR-RPT-01 → FR-RPT-02 → FR-RPT-03
| Milestone | Slice | Requirements | DoD | Hard date |
|-----------|-------|--------------|-----|-----------|
| M1 | Request + assign + status end-to-end | FR-RPT-01,02,03; NFR-SEC-01, NFR-PRIV-01 | one request runs from filing to close on a real device | — |
| M2 | Notify + timeout reminder + photo retry | FR-RPT-04; NFR-OBS-01, NFR-PERF-01 | 48h reminder fires, upload failure resumable | — |

## 13. Glossary & Competitive Analysis
### Glossary
| Term | Definition |
|------|------------|
| Drop rate | ratio of cases seen but not assigned |
| Close | case status = closed |
### Competitive / current-state
| Dimension | Us | Group chat (current) | Generic ticketing |
|-----------|----|---------------------|-------------------|
| Case status | ✅ | ❌ | ✅ |
| Community context | ✅ | partial | ❌ |
**Differentiation**: community context + zero learning curve for residents + an assignment board for the committee (maps to O-1).

## 14. Handoff to Compass
### Traceability matrix
| Requirement | Source | Objective | AC summary | Priority | Milestone |
|-------------|--------|-----------|------------|----------|-----------|
| FR-RPT-01 | P1 Mrs. Carter | O-1 | create case → id, status new | P0 | M1 |
| FR-RPT-02 | P2 clerk | O-1 | assign → assigned + notify | P0 | M1 |
| FR-RPT-03 | P1 | O-2 | status updates in 60s | P1 | M1 |
| FR-RPT-04 | edge | O-1 | upload failure keeps draft | P2 | M2 |
| NFR-PERF-01 | O-2 | O-2 | p95 < 2s | P1 | M2 |
| NFR-OBS-01 | O-1 drop | O-1 | 48h unassigned reminder | P1 | M2 |
| NFR-PRIV-01 | Security / PII | Guardrail | non-associated 403 | P0 | M1 |
| NFR-SEC-01 | Security | Guardrail | unauthenticated 401 | P0 | M1 |

**Orphan check**: all 8 requirements have a source; O-1/O-2 each have a serving requirement. ✅ No orphans.

### Compass Checklist
- [ ] FR-RPT-01 create request | P0 | AC: returns id + status new | verify: integration test
- [ ] FR-RPT-02 assign case | P0 | AC: assigned + notify | verify: integration test
- [ ] FR-RPT-03 view status | P1 | AC: updates within 60s | verify: integration test
- [ ] FR-RPT-04 upload retry | P2 | AC: failure keeps draft | verify: integration test
- [ ] NFR-PERF-01 list performance | P1 | AC: p95 < 2s | verify: load test
- [ ] NFR-OBS-01 timeout reminder | P1 | AC: 48h unassigned notify | verify: integration test
- [ ] NFR-PRIV-01 least-privilege PII read | P0 | AC: non-associated 403 + audit | verify: security test + scan
- [ ] NFR-SEC-01 API authz | P0 | AC: unauthenticated 401 | verify: security test (test-first)
