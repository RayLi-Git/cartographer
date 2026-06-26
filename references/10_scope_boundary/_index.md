# §10 Scope Boundary | "What we won't do" matters as much as "what we will"

> The AirPods template had no explicit out-of-scope section — a common gap. **Without writing down what's not done, scope grows forever.** This section formally folds the §05 anti-personas and the §02 ideas that matched no objective into a "not this cycle" list.

---

## Guiding questions

1. Which features are **explicitly not done this cycle**? Why (time/priority/off-objective)?
2. Which are **maybe later** (next) vs **never** (won't)?
3. Ideas that surfaced in §06 but matched **no §02 objective** — cut, or move to next?
4. Where do the anti-persona (§05) needs route?
5. Things on the boundary that are **easily assumed "should be included"** — explicitly exclude?

---

## YAGNI discipline (echoing Compass)

> Don't write what the PRD doesn't call for; an idea that surfaces but maps to no objective defaults to **out of scope**, not added on a whim. Exception: the "missing but the implementation is better" path — keep + annotate + await ruling (see §11), don't silently do it or silently cut it.

---

## Three columns of scope

| In scope (this cycle) | Out of scope (this cycle) | Next (maybe) |
|---|---|---|
| Guest checkout, saved-card pay | Wholesale quotes, net terms | Installments |
| Credit card + Apple/Google Pay | Crypto payment | Convenience-store codes |
| zh-TW / en | Other locales | Japanese |

---

## Common traps

- **Listing only "will", not "won't"**: blurry boundary → eng and PM each imagine their own → scope creep.
- **Treating "won't" as failure**: an explicit "won't" is focus, not a defect.
- **"Next" becomes a promise**: next means "maybe", don't write it as a guarantee or it becomes an implicit contract.
- **Boundary off-objective**: the in/out criterion is §02 objectives, not "convenience".

---

## Quality gate (pass before §11)

- ✅ There's an explicit out-of-scope list
- ✅ Anti-personas (§05) and off-objective ideas are placed
- ✅ The in/out criterion aligns with §02 objectives
- ✅ Next ≠ promise; wording stays tentative

---

## Format snippet

```markdown
## 10. Scope Boundary

**In scope**: ...
**Out of scope (this cycle)**: ... | reason: ...
**Next (maybe, not a promise)**: ...
```
