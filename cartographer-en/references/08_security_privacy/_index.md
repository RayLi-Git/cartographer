# §08 Security / Privacy / Compliance ★ | Hooks Sentinel deeply

> An **elevated standalone module** after the multi-perspective review. The AirPods PRD's biggest hole is right here: it collected health data (`2.9 fitness tracking`, `7.8 hearing-health dose`) with **zero privacy handling** — no data classification, retention, consent, or encryption. Health data is a special category of sensitive data under GDPR. That hole is the live teaching example: **whenever it touches PII/money/permissions/sensitive data, this section cannot be skipped.**
>
> This section directly cites Sentinel's security thinking: `05_security_thinking/` (authn attack surface, input trust boundaries, secrets & least privilege, dependency supply chain) and the `self_check.md` red-flag list.

---

## Guiding questions (ask each when sensitive data is involved)

1. What **data** does this feature touch? Classify each: public / internal / PII / sensitive (money, health, biometrics).
2. How is data **stored, for how long, who can read it**? How is it encrypted (in transit / at rest)?
3. **Who is who** (authn), **what can they do** (authz)? What's the permission model?
4. Which **inputs are untrusted**? How are injection, forgery, privilege escalation, replay blocked?
5. What **compliance** applies? GDPR/CCPA/local privacy law/PCI-DSS? How are **consent** and **deletion rights** implemented?
6. Which **third parties/dependencies** are used? Supply-chain risk? How are secrets managed?

---

## Data classification table (classify first, then know what to protect)

| Data | Class | Storage/retention | Access control | Encryption |
|---|---|---|---|---|
| Card number | Sensitive (PCI) | **Not stored**, tokenized | No one reads plaintext | TLS throughout + not stored |
| Name/address | PII | Encrypted columns, retained per policy | Role-authorized + audited | Encrypted at rest |
| Order amount | Internal | Normal | Role-authorized | Encrypted in transit |

---

## Block Sentinel red flags at PRD stage (don't wait until coding)

| Red flag (from Sentinel `self_check.md`) | What to write in the PRD to prevent it |
|---|---|
| Hardcoded secrets | NFR/SEC requirement: secrets via secret manager, rotatable |
| Unvalidated input | Validation/reject rules per external input point (trust boundary) |
| Over-broad permissions | Minimal permission model, deny by default |
| Swallowed errors | Failures must be observable and auditable, never silent |
| Plaintext sensitive data | Data classification + encryption + don't store (e.g. card numbers) |

---

## How to write security requirements (test-first scope uses NFR-SEC / NFR-PRIV)

```
NFR-SEC-01: The system shall require OAuth2 + a one-time idempotency key on all payment APIs and reject replays.
  Priority: P0 | AC: replaying the same idempotency key returns 200 but does not double-charge; missing token returns 401
NFR-PRIV-01: The system shall not store full card numbers, only the tokenized token and last four digits.
  Priority: P0 | AC: full-text scan of DB/logs finds no 16-digit card number
NFR-PRIV-02: The system shall provide a user data-deletion request, completed within 30 days with a receipt.
  Priority: P1 | AC: after deletion the user's PII is unqueryable via any interface (GDPR Art. 17)
```

> House rule: **security modules (Auth/permissions/PII) are test-first**. Write these ACs so they convert directly into tests.

---

## Common traps

- **Touches sensitive data but the section is empty** (the AirPods disease) → §00 already flagged "§08 required", so it can't be skipped.
- **"It'll be encrypted" without saying how**: at-rest/in-transit, key management, who can decrypt — all spelled out.
- **Consent/deletion as a feature afterthought**: GDPR/privacy law is hard compliance; list separately as NFR-PRIV.
- **Third parties as black boxes**: data flows and supply-chain risk of payment providers/third-party SDKs must be written in.

---

## Quality gate (pass before §09)

- ✅ All data classified (public/internal/PII/sensitive)
- ✅ Sensitive data has: encryption method + retention policy + access control + audit
- ✅ authn/authz permission model explicit, deny-by-default, least privilege
- ✅ Each of the five Sentinel red flags has a matching preventive requirement
- ✅ Applicable compliance (GDPR/PCI/privacy law) listed, including consent and deletion rights
- ✅ Security-requirement ACs are written test-first

---

## Format snippet

```markdown
## 8. Security, Privacy & Compliance

### 8.1 Data classification
| Data | Class | Storage/retention | Access control | Encryption |

### 8.2 Threats & defenses (trust boundary / authn / authz)
- <threat> → <defense requirement NFR-SEC-xx>

### 8.3 Compliance & privacy
- Applicable: GDPR / PCI-DSS / local law ...
- NFR-PRIV-xx: consent / retention / deletion rights ...
```
