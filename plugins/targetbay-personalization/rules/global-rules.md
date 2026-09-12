# Global Rules

These apply to every skill in this package. Skills cite them by number, e.g. `global-rules.md#G3`.

---

### G1. Revenue per session outranks engagement.
Click-through on a widget is a diagnostic, not a goal. When two options conflict, prefer the one with
better evidence of revenue per session, conversion or AOV impact — and say so explicitly. A recommendation
carousel with excellent engagement and no revenue effect is moving clicks around, not selling more.

### G2. Every recommendation must rest on available evidence.
If the data to support a recommendation does not exist, either lower the confidence and say why, or do not
make the recommendation. Evidence means an observed value from a declared capability, with a period and a
sample size. See [../schemas/recommendation.schema.json](../schemas/recommendation.schema.json).

### G3. Never invent visitor, product, traffic or performance data.
No illustrative numbers presented as real. No "personalization typically lifts conversion 15%." If a
figure is a benchmark rather than this store's data, label it as a benchmark. If nothing is known, say
nothing is known.

### G4. Attribution to a personalised surface is a claim, not an observation.
A visitor who clicked a recommendation and bought might have bought anyway. Any revenue attributed to a
placement states its attribution method and its limits, or states that the effect is not isolated
([measurement-rules.md](measurement-rules.md)).

### G5. Consent decides what is possible before value decides what is worthwhile.
Read consent state first ([safety-rules.md#S2](safety-rules.md)). A plan built on visitor profiling and
then checked for consent is a plan that gets rewritten.

### G6. Inspect the existing surfaces before adding to them.
Read what already runs on a page and what it is doing. A second widget on the same surface competes with
the first for the same attention and frequently cannibalises it rather than adding.

### G7. Attention is the scarce resource, not screen space.
Every element added to a page costs attention that the rest of the page was using. A new placement states
what it displaces, or states why the surface genuinely had room
([surface-rules.md](surface-rules.md)).

### G8. Do not build a segment that changes nothing.
A split is only worth making if the two groups would see materially different experiences. Segmenting and
showing both halves the same thing is pure overhead — and, with personalization, overhead that also has to
be maintained and debugged.

### G9. Prefer the simplest personalization that changes behaviour.
Complexity is only justified by measurable value. A well-placed category-level recommendation frequently
beats a per-visitor model nobody can explain when it misfires.

### G10. Deterministic business rules belong to the platform, not to the agent.
Consent enforcement, inventory availability, price, eligibility and regional restrictions are enforced by
the platform and the commerce system. Plan within them; never attempt to reimplement, bypass or
approximate them.

### G11. High-impact actions require explicit human approval.
Anything that changes what live visitors see, or spends budget, stops for a decision. See
[safety-rules.md](safety-rules.md).

### G12. Anonymous and identified visitors are different problems.
Most traffic is anonymous, and the personalization available to it is contextual — entry source, current
session behaviour, referring query — rather than historical. Never plan an experience for the identified
minority and assume it degrades sensibly for everyone else; state the anonymous path explicitly.

### G13. Define the measurement before the change, not after.
A personalised surface whose success criterion is chosen after the results are in has no success
criterion. State the metric, the comparison and the horizon as part of the proposal
([measurement-rules.md#M1](measurement-rules.md)).

### G14. Explain material recommendations with their evidence.
Any recommendation that changes a surface, an audience, an offer or a traffic allocation is stated together
with the evidence and the reasoning that produced it. An unexplained recommendation cannot be reviewed, and
an unreviewable recommendation should not be executed.

### G15. Declare what you could not check.
Missing data is a finding. Record it in `unmet_requirements` and lower the confidence rather than
proceeding as if the gap did not exist.

### G16. Prefer reversible steps first.
When a sequence can be ordered, put the reversible and observable steps before the irreversible ones — one
template before the whole site, a limited traffic share before full rollout — so the expensive decision is
made with more information.

---

## Precedence

[safety-rules.md](safety-rules.md) overrides this file. This file overrides domain rules, playbooks and
store context. A playbook or store may tighten any rule here; neither may loosen G5, G10 or G11.
