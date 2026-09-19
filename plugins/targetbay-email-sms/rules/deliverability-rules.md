# Deliverability Rules

Authentication, reputation, placement and the order in which they are diagnosed. Cited as
`deliverability-rules.md#D1`.

Deliverability is the constraint that makes every other decision in this package conditional. A
correctly targeted, well-written, perfectly timed campaign that does not reach the inbox produces
nothing, and the damage is not confined to that campaign — reputation is shared by every send the
store makes afterwards.

These rules bound what a skill may conclude from sending data. They do not restate how
authentication works; that is
[../knowledge/deliverability-principles.md](../knowledge/deliverability-principles.md) and the
operational detail linked from it.

---

### D1. Authentication alignment is a precondition for volume, not an optimisation.
Diagnose alignment before anything else, and before recommending any increase in sending. A store
whose authentication does not align is not a store with a content problem. Note also that these
records live in the store's own DNS, outside the platform: a skill recommends the change and names
who must make it, and never reports it as something it can execute.

### D2. Reputation is earned per sending domain and per IP, and it is shared.
Every send contributes to the same pool. A decision that looks locally cheap — one blast to a
dormant cohort — is charged against every campaign that follows it. State the shared cost when it
applies.

### D3. Derive the threshold from this store's own trend.
A bounce or complaint rate is meaningful against this store's recent variance, not against a
published figure. A benchmark says whether a number is unusual for the industry; it does not say
whether it is unusual here ([global-rules.md#G2](global-rules.md)). This package ships no
benchmarks.

### D4. Engagement is the reputation input the programme can actually move.
Authentication is binary and infrastructure is slow. Who is mailed, how often, and whether they
respond is the lever available this week. Route a reputation problem to the audience and cadence
decisions before the content ones.

### D5. Changing the sending pattern is itself a deliverability event.
Volume, frequency and audience composition are part of what is being judged. A plan that materially
changes any of them states the change and its ramp, rather than treating the new level as the
starting point.

### D6. Separate the receiving domains before diagnosing the programme.
A problem concentrated at one mailbox provider is a different problem from a programme-wide one, and
it has a different remedy. A list-wide conclusion drawn from a single provider's numbers sends the
fix to the wrong place ([audience-rules.md#A8](audience-rules.md)).

### D7. Inbox placement is not observable from sending data. Do not infer it.
Delivery, opens and clicks do not distinguish the inbox from the spam folder. Where the platform
provides no placement signal, say that placement is unknown and reason from the proxies that do
exist — engagement, bounce and complaint movement by receiving domain — labelled as proxies
([global-rules.md#G15](global-rules.md)).

### D8. A deliverability remedy that does not change who is mailed is not a remedy.
Rewriting subject lines, changing send times or redesigning a template do not alter the behavioural
signal that created the problem. Where the diagnosis is reputation, the plan changes the population,
the cadence, or both, and says so plainly.

### D9. Warm-up is a constraint on the plan, not a setting.
A new domain, a new IP or a long dormant period bounds how much may be sent and to whom, ahead of
any campaign the store wants to run. Derive that bound from the store's own current sending level
and state it as a dependency, never as a fixed schedule.

### D10. Never trade a permanent reputation cost for a one-off revenue gain.
A send that would raise complaints to a level risking a block is refused even when the campaign's
expected revenue is positive, because the cost lands on every later send
([safety-rules.md#S2](safety-rules.md), [global-rules.md#G1](global-rules.md)).
