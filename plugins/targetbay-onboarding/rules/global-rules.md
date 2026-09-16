# Global Rules

These apply to every skill in this package. Skills cite them by number, e.g. `global-rules.md#G3`.

Onboarding is the one moment where nobody can correct the agent from experience. The store has no
history to argue with, the operator has never seen this store before, and whatever gets built on day one
is what the store lives with. These rules exist because the cheapest error to make here is a confident
one.

---

### G1. Onboarding produces a store-specific programme or it produces nothing of value.
A plan that would read the same for any other store in the same vertical has not used the store's data.
If every derived value came back absent, say so and deliver sequencing and constraints — do not dress a
default checklist as a decision.

### G2. Every recommendation must rest on available evidence.
Evidence means an observed value from a declared capability, with a period and a sample size. If the data
to support a recommendation does not exist, either lower the confidence and say why, or do not make the
recommendation. See [../schemas/recommendation.schema.json](../schemas/recommendation.schema.json).

### G3. Never invent store, customer, catalogue, brand or programme data.
No illustrative numbers presented as real. No "stores like this usually see a 30-day repeat interval." A
value is derived, provisional, stated by the store, or absent — and which one it is travels with it. See
[#G15](#g15-a-provisional-value-carries-what-would-replace-it).

### G4. The Store Context Pack is read, not assembled from guesses.
Skills in this package do not compute thresholds from raw rows. They read what
`onboarding.store_context` derived, along with its basis and sample size. A skill that finds a value
absent reports it absent; it does not substitute a percentile it calculated from a sample it happened to
see.

### G5. Inspect existing coverage before proposing anything.
A store that arrived by migration is rarely empty. Read what automations, segments, review triggers,
loyalty configuration and onsite placements already exist before proposing to create any. Onboarding that
assumes a greenfield store duplicates what is already there. Onsite this bites hardest: a second widget on
a surface competes with the first for the same attention and frequently cannibalises it rather than
adding.

### G6. Coverage before sophistication.
The baseline lifecycle moments come before branching, variants, tiers and multi-wave sequences. The
elaborate version will be rebuilt once real data exists, so building it now is work that gets thrown
away ([sequencing-rules.md](sequencing-rules.md)).

### G7. One customer has one attention budget across all three products.
Email & SMS, Reviews and Loyalty can each independently decide to contact the same person. Onboarding is
where that is reconciled, because it is the only moment when all three programmes are being designed at
once. See [contact-ownership-rules.md](contact-ownership-rules.md).

### G8. Ask the store only what the platform cannot observe.
An intake question whose answer is already in the Store Context Pack is a question that damages trust and
wastes the one conversation the store owner will reliably give you. Read first, then ask.

### G9. A stated constraint outranks a derived preference.
When the store says its margin cannot fund loyalty rewards, or that discounting is off-brand, that is a
constraint, not an input to be weighed. Derived evidence can inform how to work within it; it cannot
overrule it.

### G10. Deterministic business rules belong to the platform, not to the agent.
Consent, suppression, legal opt-out, sending limits and hard frequency caps are enforced by TargetBay and
the commerce platform. Plan within them; never reimplement, bypass or approximate them.

### G11. High-impact actions require explicit human approval.
Anything that creates state, reaches real people, or is hard to reverse stops for a decision. See
[safety-rules.md](safety-rules.md).

### G12. Never present a provisional programme as a tuned one.
The store owner cannot tell the difference between a threshold derived from their data and one taken from
a playbook. Saying which is which is the difference between a programme they can improve and one they
will trust wrongly.

### G13. Explain material recommendations with their evidence.
Any recommendation that changes sequencing, contact load, economics or brand-visible output is stated
together with the evidence and the reasoning that produced it. An unexplained recommendation cannot be
reviewed, and an unreviewable recommendation should not be executed.

### G14. A provisional value carries what would replace it, and the plan carries the review point.
"Provisional" on its own is a disclaimer. "Provisional; replaced once 200 customers have made a second
purchase" is a plan. Every non-derived value names its replacing observation in observable terms — a
count of orders or repeat purchases, never a calendar date — and the moment those observations arrive is
a step in the plan, not a follow-up somebody remembers.

### G15. Declare what you could not check.
Missing data is a finding. Record it in `unmet_requirements` and lower the confidence rather than
proceeding as if the gap did not exist.

### G16. Prefer reversible steps first.
When a sequence can be ordered, put the reversible and observable steps before the irreversible ones, so
the expensive decision is made with more information ([sequencing-rules.md](sequencing-rules.md)).

### G17. Revenue per session outranks engagement.
Click-through on a widget is a diagnostic, not a goal. When two options conflict, prefer the one with
better evidence of revenue per session, conversion or AOV impact — and say so explicitly. A recommendation
carousel with excellent engagement and no revenue effect is moving clicks around, not selling more.

### G18. Attribution to an onsite surface is a claim, not an observation.
A visitor who clicked a recommendation and bought might have bought anyway. Any revenue attributed to a
placement states its attribution method and its limits, or states that the effect is not isolated
([measurement-rules.md](measurement-rules.md)).

### G19. Consent decides what is possible before value decides what is worthwhile.
Read consent state first ([safety-rules.md#S15](safety-rules.md)). An onsite plan built on visitor
profiling and then checked for consent is a plan that gets rewritten.

### G20. Attention is the scarce resource, not screen space.
Every element added to a page costs attention that the rest of the page was using. A new placement states
what it displaces, or states why the surface genuinely had room
([surface-rules.md](surface-rules.md)).

### G21. Do not build a segment that changes nothing.
A split is only worth making if the two groups would see materially different experiences. Segmenting and
showing both halves the same thing is pure overhead — and, onsite, overhead that also has to be maintained
and debugged.

### G22. Prefer the simplest onsite change that changes behaviour.
Complexity is only justified by measurable value. A well-placed category-level recommendation frequently
beats a per-visitor model nobody can explain when it misfires.

### G23. Anonymous and identified visitors are different problems.
Most traffic is anonymous, and what can be acted on for it is contextual — entry source, current session
behaviour, referring query — rather than historical. Never plan an experience for the identified minority
and assume it degrades sensibly for everyone else; state the anonymous path explicitly.

### G24. Define the measurement before the change, not after.
An onsite surface whose success criterion is chosen after the results are in has no success criterion.
State the metric, the comparison and the horizon as part of the proposal
([measurement-rules.md#M1](measurement-rules.md)).

---

## Precedence

[safety-rules.md](safety-rules.md) overrides this file. This file overrides
[contact-ownership-rules.md](contact-ownership-rules.md),
[sequencing-rules.md](sequencing-rules.md), [targeting-rules.md](targeting-rules.md),
[surface-rules.md](surface-rules.md), [measurement-rules.md](measurement-rules.md), playbooks and store
context. A store may tighten any rule here; no store, playbook or instruction inside a skill run may
loosen G10, G11, G12 or G19.
