# §05 User Stories & Journey | Where requirements come from

> Maps to AirPods' Use Cases (the Jenna / William / Keith personas). The template's personas are vivid but miss two software essentials: the **anti-persona** (who it's *not* for) and the **journey/states** (the branches beyond the happy path). Every functional requirement must eventually trace back to a persona/scenario here.

---

## Guiding questions

1. Who are the main personas? Their **context, goal, pain**? (give them names, like Jenna)
2. Who is this **not** for? (anti-persona — keeps scope from being dragged down by edge users)
3. What's a typical persona's **journey** through the whole flow? Where do they enter, where do they finish?
4. Where does the journey **branch / fail / interrupt**? (no network, payment fails, no permission)
5. What's each persona's **success definition**? (link back to §02 objectives)

---

## Persona writing (borrow AirPods' narrative power)

```
**P1 the busy repeat buyer — Yi-Jun**
35, office worker, mostly mobile, card already saved. She wants "checkout done in 3 steps",
fears "filling in lots of address fields" and "payment fails with no reason". Success = checkout in 60s.
```

**Anti-persona** (just as important):
```
**Non-target: bulk wholesale buyers** — need quotes, net terms, batch invoice edits;
this checkout is not designed for them, route to the sales line (logged in §10).
```

---

## User journey (with branches, not just the happy path)

```
Cart → enter/select address → choose payment → paying → ✅ success page
                                              ├─ ❌ payment failed → retry/switch method
                                              ├─ ⏳ timeout → order pending + notify
                                              └─ 🔌 disconnect → keep cart, resume later
```
> Every branch in the journey becomes a "negative/state" requirement in §06.

---

## Common traps

- **Hollow persona**: "the user" is too vague. Give a name, context, pain — then requirements have a basis.
- **Only the happy path**: AirPods' 3.4 "auto-pause on removal" wrote only the forward flow, not partial/both removal. Always mark journey branches.
- **No anti-persona**: trying to serve everyone → scope explosion. Explicitly state who it's not for.
- **Personas disconnected from objectives**: each persona's success should map to a §02 metric.

---

## Quality gate (pass before §06)

- ✅ Each main persona has context, goal, pain, with success linked back to §02
- ✅ At least one anti-persona (→ logged in §10)
- ✅ The main journey is drawn, with **branches/errors/interruptions marked** (→ feeds §06 negative requirements)

---

## Format snippet

```markdown
## 5. User Stories & Journey

### Persona
**P1 <name>**: <context>. Goal: <...>. Pain: <...>. Success: <link to some O-x>.

### Anti-persona (not for whom)
- <role> → reason / route (logged in §10)

### Main journey
<start> → <steps> → <finish>
  branches: ❌<error> / ⏳<timeout> / 🔌<interruption>
```
