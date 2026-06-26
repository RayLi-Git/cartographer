# §04 Stakeholders & RACI | Who cares, who decides

> Maps to AirPods' Stakeholders (it listed target group, customer service, marketing, senior management, retailers, regulators). Software needs one more layer AirPods lacked: **who's responsible/accountable for each decision** (RACI), or nobody can adjudicate a PRD conflict.

---

## Guiding questions

1. Who does this product/feature **affect**? (users, business, support, compliance, ops, partners…)
2. What does each group **care about**? (what success looks like for them, what they fear most)
3. Who can **decide** scope and priority? (Accountable — exactly one)
4. Who must be **consulted** before it's settled? (compliance, security, design, SRE)
5. Any **external dependencies** (payment provider, third-party API, upstream team)?

---

## Stakeholder inventory

| Role | Cares about | Fears most |
|---|---|---|
| End user | Fast, safe checkout | Failed charge, leaked PII |
| Customer support | Self-serviceable, traceable issues | A flood of "payment failed" tickets |
| Security/compliance | Compliance, auditability | Mishandled PII/card numbers |
| Ops/finance | Correct reconciliation | Double charges, books that don't balance |
| Payment provider (external) | Spec-compliant integration | Over-quota requests, PCI violations |

---

## RACI (one row per key decision)

> R = Responsible | A = Accountable (exactly one) | C = Consulted | I = Informed

| Decision | PM | Eng | Design | Security | Compliance |
|----------|----|----|--------|----------|-----------|
| Feature scope & priority | A | C | C | C | I |
| Payment provider selection | C | R | I | C | A |
| PII handling | C | R | I | A | C |

---

## Common traps

- **Two Accountables**: there can be only one, or no one adjudicates a conflict.
- **Missing "silent" stakeholders**: support, compliance, SRE often aren't asked and blow up at launch. AirPods listing retailers/regulators is worth emulating.
- **Listing roles without what they care about**: a row of titles is useless; write each group's success and fear so requirements have a source.
- **External dependencies omitted**: payment-provider/third-party limits constrain §06 and §09 in reverse.

---

## Quality gate (pass before §05)

- ✅ Stakeholders complete, including "silent" roles (support/compliance/security/SRE) and external dependencies
- ✅ Each has "cares about / fears most"
- ✅ Key decisions have RACI, and each row has **exactly one A**

---

## Format snippet

```markdown
## 4. Stakeholders & RACI

| Role | Cares about | Fears most |
|------|-------------|------------|
| ... | ... | ... |

**RACI** (R Responsible / A Accountable / C Consulted / I Informed)
| Decision | PM | Eng | Design | Security | Compliance |
|----------|----|----|--------|----------|-----------|
| ... | A | R | C | C | I |
```
