# §11 Open Questions | Honestly list the undecided, don't pretend

> Maps to AirPods' Open Questions (it honestly listed 5 — battery, Android connectivity, etc.). A mark of a mature PRD. But keep it **separate from §03 risks**: a risk is "what could go wrong + how to block it"; an open question is "no answer yet, needs someone to investigate/decide".

---

## Guiding questions

1. What has **no answer yet** but doesn't block starting other parts?
2. For each, **who finds the answer** and **by when**?
3. Which need a **user/management ruling** (not something engineering decides alone)?
4. Requirements marked `⏭ skip` in §06 — should they be collected here?

---

## Open question vs risk vs gap (route the three)

| Type | Trait | Where |
|---|---|---|
| Open question | No answer yet, to investigate/decide | **§11 here** |
| Risk | Could go wrong + probability/impact/mitigation | §03 |
| PRD gap but implementation is better | Spec didn't say, but doing it is better | Keep + annotate, await ruling (Compass §5) |

---

## How to write (each needs an owner and a time)

```
Q-1: Should guest checkout require email verification? Conversion vs fraud risk.
     owner: PM + risk | needs ruling before design freeze
Q-2: Should refunds go through the original payment channel? Depends on provider capability.
     owner: Backend | confirm before §12 M2
```

---

## Common traps

- **Hiding open questions**: pretending it's all figured out → blows up during implementation. Listing honestly is more professional.
- **Questions with no owner/time**: become eternal to-dos. Assign a person + deadline each.
- **Mixing with risks** (the AirPods pattern): anything you can state with probability/impact/mitigation moves to §03.
- **Using open questions as procrastination**: investigate what's investigable now; don't dump everything here.

---

## Quality gate (pass before §12)

- ✅ Each open question has an owner + a time it needs a ruling
- ✅ Separated from §03 risks (here only "no answer, to investigate/decide")
- ✅ §06 skipped requirements are collected here

---

## Format snippet

```markdown
## 11. Open Questions

| ID | Question | Impact | Owner | Ruling by |
|----|----------|--------|-------|-----------|
| Q-1 | ... | ... | PM/risk | before design freeze |
```
