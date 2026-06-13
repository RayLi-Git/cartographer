# §13 Glossary & Competitive / Current-State Analysis | Shared language + positioning

> Maps to AirPods' Explanation of Terms (glossary) and Appendix A (competitive comparison table). The glossary builds shared team language and removes ambiguity; the competitive/current-state analysis gives positioning a reference and avoids reinventing the wheel.

---

## Guiding questions

1. Which abbreviations, terms, domain words in the PRD need defining? (so newcomers/other teams can read it)
2. Does one concept have **multiple names**? Unify to one.
3. How do **competitors/the current state** solve this problem? Where are they good/bad?
4. What's our **differentiated positioning**? (link back to §02 objectives)
5. Is there an off-the-shelf option (library/SaaS) to use instead of building?

---

## Glossary (disambiguate)

| Term | Definition |
|---|---|
| Abandonment rate | Share entering checkout but not completing = 1 − checkout_succeeded/checkout_started |
| Tokenization | Replacing the card number with a meaningless token so the system never touches plaintext (shrinks PCI scope) |
| Idempotency key | An identifier that recognizes duplicate requests, ensuring one operation takes effect once |
| P0–P3 | Requirement priority. P0 launch-blocking / P3 future. (Maps to AirPods' P1–P10: P0≈P10, P3≈P1–P3) |

---

## Competitive / current-state analysis (borrow AirPods' Appendix A table)

| Dimension | Us (target) | Competitor A | Competitor B |
|---|---|---|---|
| Checkout steps | ≤3 | 5 | 3 |
| Mobile pay | Apple/Google Pay | Card only | Apple Pay |
| Guest checkout | ✅ | ❌ | ✅ |
| Abandonment (public est.) | target 30% | ~40% | ~32% |

> Differentiated positioning: win on "fewest steps + mobile pay + guest checkout" together (maps to O-2, lower abandonment).

---

## Common traps

- **Abbreviations everywhere, undefined**: cross-team readers get stuck. Beyond `prd_lint`, manually ensure each abbreviation is defined on first use.
- **One thing, many names**: cart/basket/bag mixed → unify.
- **Competitive analysis as a copy list**: the point is "their good/bad → our differentiation", not copying features.
- **Not checking off-the-shelf options**: building what you could buy → §10 YAGNI also applies to "don't build".

---

## Quality gate (pass before §14)

- ✅ All abbreviations/terms/domain words defined, no one-thing-many-names
- ✅ P0–P3 ↔ AirPods P1–P10 mapping noted
- ✅ Competitive/current-state compared, yielding a differentiation (linked to §02)

---

## Format snippet

```markdown
## 13. Glossary & Competitive Analysis

### Glossary
| Term | Definition |

### Competitive / current-state
| Dimension | Us | Competitor A | Competitor B |
**Differentiated positioning**: <one sentence, linked to some objective>
```
