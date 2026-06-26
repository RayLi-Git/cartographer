# Cartographer teaching samples (examples/)

> These are real demo artifacts produced by running Cartographer. **All data is fictional test data**, used to demonstrate the flow and the quality bar. Not real projects, not templates.
> For the blank template and the canonical filled example, see `../templates/`.

| File | What it demonstrates | lint |
|---|---|---|
| `example-bad-prd.md` | ❌ **Anti-example**: the kind of bad PRD beginners write (no numbering, adjectives, touches value but zero security, no scope). Used to demonstrate review mode catching problems | 0 requirements / fake PASS (highlights the lint blind spot) |
| `example-points-after-review.md` | ✅ The passing version **reviewed → regenerated** from `example-bad-prd.md` (membership points & redemption, 🔴 heavy, 14 sections) | 11 requirements / 0 blockers / PASS |
| `example-repair-app-full.md` | ✅ A complete PRD walked through section by section interactively (a community maintenance-request app, 🔴 heavy, 14 sections, incl. §14 traceability matrix) | 8 requirements / 0 blockers / PASS |
| `example-quickpay-testrun.md` | ✅ An end-to-end stress-test artifact (QuickPay one-page mobile checkout, 🔴 heavy) | 20 requirements / 0 blockers / PASS |

## How to use these samples

- **Learn "what a passing PRD looks like"**: read `example-points-after-review.md` or `example-repair-app-full.md`.
- **Learn "what's wrong and how to fix it"**: compare `example-bad-prd.md` (before) with `example-points-after-review.md` (after).
- **Verify lint**:
  ```
  # On Windows use py; on macOS/Linux use python3 (typing python on Windows may hit the Store stub and silently do nothing)
  py ../scripts/prd_lint.py example-points-after-review.md   # PASS
  py ../scripts/prd_lint.py example-bad-prd.md               # highlights how un-numbered requirements = lint blindness
  ```
