# §09 Data & Integration | Data model, contracts, dependencies

> AirPods is hardware, so this section is nearly blank (only scattered mentions of the H1 chip, BT 5.2 in the Introduction). Software is the opposite: the **data model, API/event contracts, platform support matrix, third-party dependencies** are the skeleton of implementation and Compass's build interface. Data classification interlocks with §08.

---

## Guiding questions

1. What are the core **data entities**? Key fields, relationships, lifecycle?
2. External/internal **interface contracts**: which APIs/events? Input/output schema, error codes, idempotency?
3. Which **platforms** to support? (OS/browser/device/minimum version)
4. Which **third parties** does it depend on? (payment, SMS, maps…) Their limits and failure behavior?
5. Where does data **come from and go to**? Cross-system flows and consistency requirements?

---

## Data model (key entities + lifecycle)

```
Order: { id, userId, items[], amount, currency, status, createdAt }
  status: cart → pending_payment → paid → fulfilled | failed | refunded
Payment: { id, orderId, provider, token, last4, status, idempotencyKey }
```
> Every status transition should map to a §06 functional requirement (including negatives).

---

## Interface contracts (so Compass can build to them)

```
POST /api/checkout
  req:  { orderId, paymentMethodId, idempotencyKey }
  resp: 200 { paymentId, status } | 423 locked | 409 duplicate | 402 payment failed
  idempotency: same idempotencyKey returns the first result, no double charge
events: checkout_started / checkout_succeeded / checkout_failed (for §02 metrics, §07 observability)
```

---

## Platform support matrix

| Platform | Min version | Notes |
|---|---|---|
| iOS Safari | 15+ | Apple Pay |
| Android Chrome | last 2 versions | Google Pay |
| Desktop | Chrome/Edge/Firefox last 2 | — |

---

## Third-party dependencies

| Dependency | Use | Limit | Behavior on failure |
|---|---|---|---|
| Payment provider X | Card authorization | 50 req/s; PCI | Degrade to notify-later (see §03 R-1, §07 SLA) |
| SMS provider | OTP/notify | Quota | Fall back to email |

---

## Common traps

- **Data model with no lifecycle**: listing fields without status transitions → §06 negative requirements have no basis.
- **Contracts without error codes/idempotency**: only the happy response → implementers each interpret failure behavior.
- **Vague platform matrix**: "support mobile" → which OS/versions? Affects testing and §07.
- **Third parties without failure behavior**: a dependency will go down; no degradation written = outage at launch.

---

## Quality gate (pass before §10)

- ✅ Key entities have fields + relationships + **lifecycle states**
- ✅ External interfaces have schema + error codes + idempotency
- ✅ Platform matrix is specific to versions
- ✅ Each third party has limits + **failure behavior** (link to §03 risks, §07 SLA)
- ✅ PII/sensitive data flows aligned with §08 classification

---

## Format snippet

```markdown
## 9. Data & Integration

### 9.1 Data model
<entities: fields, relationships, status lifecycle>

### 9.2 Interface contracts
<APIs: path, req/resp schema, error codes, idempotency; event list>

### 9.3 Platform support matrix
| Platform | Min version | Notes |

### 9.4 Third-party dependencies
| Dependency | Use | Limit | Behavior on failure |
```
