# §02 Objectives & Success Metrics | Measurable, or it's not an objective

> Maps to AirPods' Objectives. The biggest trap here is exactly the one the AirPods PRD fell into: **stating a hypothesis as fact** ("adding smart interactions **will** expand user base by 15%"). I force three things apart: **goal / hypothesis / fact**, and every goal must be measurable.

---

## Guiding questions

1. What is the single most important metric (**North Star**) for this product/feature?
2. What **supporting KPIs** surround it? For each, what's the **current → target → deadline**?
3. **How is each measured** — which event/instrumentation/report? (a metric you can't measure doesn't exist)
4. What do you **believe but haven't validated** (hypotheses)? (move them out, don't mix into goals)
5. Any **counter/guardrail metrics**? (e.g. "lift conversion but complaints must not rise > 5%")

---

## Keep goal / hypothesis / fact apart

| Type | Definition | How to write |
|---|---|---|
| **Goal** | What we aim for, and measurable | "checkout success 99.2% → 99.5% by 2026 Q3" |
| **Hypothesis** | Believed, unvalidated (→ also log in §03) | "⚠️assumption one-tap checkout cuts abandonment 10%" |
| **Fact** | Verified (from §01 evidence) | "abandonment is 38% (GA, last 3 months)" |

---

## What "good" looks like (good vs bad)

✅ **Good**:
> **North Star**: monthly successful checkout orders.
> **O-1 checkout success** 99.2% → **99.5%** by 2026/09 | measure: `checkout_succeeded / checkout_started`
> **O-2 abandonment** 38% → **30%** by 2026/09 | measure: funnel events `cart→address→pay→done`
> **Guardrail**: payment-related complaints must not rise > 5% vs last quarter.

❌ **Bad** (AirPods style):
> "Expand the user base, improve experience, and we believe new features will bring 15% growth." — no current value, no deadline, no measurement, and a hypothesis stated as a conclusion.

---

## Common traps

- **Unmeasurable goal**: "improve satisfaction" → make it "NPS 32 → 40" or "checkout complaint rate X% → Y%".
- **No measurement mechanism**: a metric set with nobody knowing where to read it → can't judge success after launch. Bind each metric to an event/report.
- **Hypothesis disguised as goal**: anything "I believe / should / expected to bring" → mark `⚠️assumption`, move to §03.
- **Benefits with no guardrail**: optimizing one number often sacrifices another; add counter-metrics.

---

## Quality gate (pass before §03)

- ✅ One clear North Star
- ✅ Every KPI has "current → target → deadline" **and** a bound measurement mechanism
- ✅ Goal / hypothesis / fact separated; hypotheses marked and ready to move to §03
- ✅ At least one guardrail/counter-metric

---

## Format snippet

```markdown
## 2. Objectives & Success Metrics

**North Star**: <single most important metric>

| ID | Goal | Current → Target | Deadline | Measurement (event/report) |
|----|------|------------------|----------|----------------------------|
| O-1 | ... | 99.2% → 99.5% | 2026 Q3 | checkout_succeeded/started |

**Guardrails**: <metric that must not degrade>
**Hypotheses (unvalidated, see §03)**: ⚠️assumption ...
```
