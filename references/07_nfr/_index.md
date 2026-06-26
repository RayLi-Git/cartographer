# §07 Non-Functional Requirements (NFR) | The most-dropped section

> AirPods gave its largest space to regulation tests (7.x) — and each is quantified (drop from 1.22m, 5% salt fog for 24h). The software equivalent is NFRs, yet beginners skip the whole section. Use the same spirit as AirPods: **every NFR must be quantifiable**, no "fast, stable".
>
> Note: security and privacy are also NFRs, but given their weight and risk they get their own **§08**. This section covers performance/availability/observability/accessibility/i18n.

---

## Guiding questions

1. **Performance**: latency target for key operations? (p50/p95/p99) Peak QPS?
2. **Availability/SLA**: how many nines? Allowed downtime? Degradation strategy?
3. **Observability**: how do you know when it breaks? Which metrics, logs, traces, alerts?
4. **Accessibility**: which WCAG level? Keyboard operation, screen readers?
5. **i18n/l10n**: multiple locales? Currencies/time zones? Text expansion?

---

## NFR categories and quantified examples

| Category (code) | Unmeasurable (bad) | Quantified (good) |
|---|---|---|
| Performance PERF | "checkout should be fast" | `NFR-PERF-01: checkout submit to result p95 < 1.5s (peak 500 QPS)` |
| Availability SLA | "should be stable" | `NFR-SLA-01: payment service monthly availability ≥ 99.95%; degrade to notify-later on provider outage` |
| Observability OBS | "should be monitorable" | `NFR-OBS-01: emit checkout_* per payment; failure rate >2% for 5 min triggers PagerDuty` |
| Accessibility A11Y | "should be friendly" | `NFR-A11Y-01: full checkout completable by keyboard, WCAG 2.1 AA` |
| Internationalization I18N | "support multiple languages" | `NFR-I18N-01: support zh-TW/en; show currency and thousands separators per locale` |

> Same form as §06: `NFR-<category>-<n>` + priority + verifiable AC + (optional) source.

---

## Common traps

- **Skipping the whole section**: writing only features — the PRD's biggest pit. Tiers 🟡🔴 must do this section.
- **Adjective NFRs**: "high performance, high availability" with no numbers = nothing written. Give p95, give the nines.
- **Observability as an afterthought**: instrumenting at launch → blind when it breaks. Write metrics/alerts as requirements up front.
- **Accessibility/i18n as "later"**: retrofitting costs far more than designing it in.

---

## Quality gate (pass before §08)

- ✅ Performance has concrete latency/throughput targets (with percentiles)
- ✅ Availability has SLA numbers and a degradation strategy
- ✅ Observability specifies metrics/logs/alert thresholds
- ✅ A11Y (WCAG level) and i18n covered where the product needs them
- ✅ Every line is measurable (`prd_lint.py` shows no adjectives remaining)

---

## Format snippet

```markdown
## 7. Non-Functional Requirements

NFR-PERF-01: <latency/throughput, with p95/p99 and load> | P0 | AC: ...
NFR-SLA-01:  <availability target + degradation> | P0 | AC: ...
NFR-OBS-01:  <metrics/logs/traces/alert thresholds> | P1 | AC: ...
NFR-A11Y-01: <WCAG level + keyboard/reader> | P1 | AC: ...
NFR-I18N-01: <locales/currency/time zone> | P2 | AC: ...
```
