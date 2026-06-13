# What Cartographer Covers / Doesn't

> Read this first to avoid misuse. Cartographer is one link in a toolchain; it deliberately doesn't do what others do.

---

## ✅ Covers

| Area | Notes |
|---|---|
| Drafting a software PRD from scratch | Section-by-section interview turning a fuzzy idea into a solid PRD (15 modules) |
| Reviewing/strengthening an existing PRD | Turn the quality gates into a health checklist, find gaps, suggest fixes |
| Requirement-quality enforcement | Atomic + numbered + priority + verifiable + traceable; prd_lint mechanical gate |
| Non-functional / security / privacy | Forces confronting performance, SLA, observability, a11y, i18n, data classification, compliance |
| Traceability matrix | FR ↔ persona ↔ objective ↔ AC ↔ milestone |
| Handoff to Compass | Convert into a Compass-ready checklist and reverse-audit input |

## ❌ Doesn't cover (who does)

| Not this | Use |
|---|---|
| Implementing the PRD, building to spec, no drift | **Compass** |
| How to think, root-cause diagnosis, security thinking habits | **Sentinel** |
| Hardware PRD (mechanical, electrical, manufacturing, regulatory tests) | This skill focuses on software |
| Business plan / financial model / fundraising deck | Not a PRD concern |
| Detailed UI design / wireframes / visual specs | Design tools; the PRD describes behavior and states |
| Project-management scheduling detail (Gantt, hours) | PM tools; the PRD goes to milestones and slices |

## 🤝 The seams with Sentinel / Compass

- **Before entering**: idea but messy → Sentinel to think it through → Cartographer starts drafting.
- **§08 security**: directly cites Sentinel's red-flag list and security thinking.
- **After leaving**: PRD done → §14 handoff → Compass takes over DoR/implementation/DoD.

## Three-tier scaling

- 🟢 light: minor revision → 4 sections (00/01/06/11)
- 🟡 medium: one feature module → ~9 sections
- 🔴 heavy: new product, money/PII/permissions → full 00–14; §06 AC and §08 security cannot be skipped.
