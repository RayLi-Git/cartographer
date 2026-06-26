# §01 Background & Problem | Why do this now

> Maps to the AirPods PRD's Introduction. A PRD's first paragraph isn't "what we'll build" — it's "**why this problem is worth solving now**". A feature list with no problem statement is a rootless wish.

---

## Guiding questions

1. What **concrete pain** do users/the business hit now? (if you can't say it in one sentence, it isn't clear yet)
2. What's the **evidence**? Data, complaints, interviews, observation, competitor moves — not just "I feel".
3. **Why now**? Tech matured? Market shifted? Regulation? Old approach breaking down?
4. What's the **current/existing solution**? How does everyone cope today?
5. What happens **if we don't**? (can't name the cost → priority can't be high)

---

## What "good" looks like (good vs bad)

✅ **Good**:
> Checkout abandonment is 38% (last 3 months of GA). Top complaints include two related to "payment failed with no reason" and "address form too long". Competitor X shipped one-tap checkout, converting 11% higher. The current checkout is a 5-year-old monolith page that can't support multiple payment providers; not rebuilding it will block next quarter's subscription launch.

❌ **Bad** (the AirPods pattern and common faults):
> "Users want a better checkout experience." — no data, no why-now, no current state, no cost of inaction. Equivalent to writing nothing.

---

## Common traps

- **Writing the "solution" as the "problem"**: "we need one-tap checkout" is a solution; the problem is "too many checkout steps cause abandonment". Write the problem; leave the solution to §06.
- **Evidence that's speculation**: "I believe adding X will grow 15%" is a **hypothesis**, not a fact — move it to §03; keep only evidenced current state here.
- **Background as company history**: focus on *this problem*, not the whole product story.

---

## Quality gate (pass before §02)

- ✅ The problem is stated in one clear sentence, and **isn't a solution**
- ✅ At least one **verifiable** piece of evidence (data/complaints/interviews/competitors); speculation is marked `⚠️assumption` and moved to §03
- ✅ You can answer why-now and the cost of inaction

---

## Format snippet

```markdown
## 1. Background & Problem

**Problem**: <one sentence, the pain, not the solution>
**Evidence**:
- <data / source>
- <complaint / interview summary>
**Why now**: <why this point in time>
**Current/existing solution**: <how it's solved today, why it's insufficient>
**Cost of inaction**: <what the status quo loses>
```
