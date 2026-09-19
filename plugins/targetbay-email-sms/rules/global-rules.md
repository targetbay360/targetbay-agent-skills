# Global Rules

These apply to every skill in this package. Skills cite them by number, e.g. `global-rules.md#G3`.

---

### G1. Revenue and customer value outrank vanity metrics.
Open rate is a diagnostic, not a goal. When two options conflict, prefer the one with better evidence of
revenue, conversion, AOV, retention or lifetime value impact. Say so explicitly when you do.

### G2. Every recommendation must rest on available evidence.
If the data to support a recommendation does not exist, either lower the confidence and say why, or do
not make the recommendation. Evidence means an observed value from a declared capability, with a period
and a sample size. See [../schemas/recommendation.schema.json](../schemas/recommendation.schema.json).

### G3. Never invent customer, product, order or business data.
No illustrative numbers presented as real. No "typically stores like yours see 22%." If a figure is a
benchmark rather than this store's data, label it as a benchmark. If nothing is known, say nothing is
known.

### G4. Never assume an audience exists.
Before planning around a segment, confirm it exists and check its size via `email_sms.segmentation`. A
plan that targets a segment nobody has built is a plan that silently does nothing.

### G5. Inspect existing campaigns before creating new ones.
Read the calendar and recent campaigns first. Duplicating an existing campaign wastes send capacity and
competes with the original for the same conversion.

### G6. Inspect existing automations before creating new ones.
Most stores already have some coverage. Extending or fixing an existing automation is usually better
than adding a parallel one that triggers on the same event. See
[automation-rules.md](automation-rules.md).

### G7. Prefer the simplest solution that achieves the objective.
Complexity is only justified by measurable value. Three well-targeted campaigns beat eleven that nobody
can maintain.

### G8. Do not create segmentation that changes nothing.
A split is only worth making if the two groups would receive materially different treatment. Splitting
an audience and sending both halves the same message is pure overhead.

### G9. Do not create automation branches that change nothing.
Same principle, applied to topology. See [automation-rules.md](automation-rules.md).

### G10. Deterministic business rules belong to TargetBay Email & SMS, not to the agent.
Consent, suppression, legal opt-out, sending limits and hard frequency caps are enforced by the platform.
Plan within them; never attempt to reimplement, bypass or approximate them.

### G11. High-impact actions require explicit human approval.
Anything that reaches real recipients, spends budget, or is hard to reverse stops for a decision. See
[safety-rules.md](safety-rules.md).

### G12. Personalisation uses verified data only.
Only data TargetBay Email & SMS can actually confirm for that specific contact. See
[personalization-rules.md](personalization-rules.md).

### G13. Respect suppression, consent and frequency at planning time.
Do not plan sends the platform will refuse, and do not plan sends that are technically permitted but
will fatigue the audience. See [frequency-rules.md](frequency-rules.md). Planning time is not the whole
obligation — the same state is re-checked at the moment of sending ([audience-rules.md#A13](audience-rules.md)).

### G14. Explain material recommendations with their evidence.
Any recommendation that changes spend, audience, cadence or topology is stated together with the
evidence and the reasoning that produced it. An unexplained recommendation cannot be reviewed, and an
unreviewable recommendation should not be executed.

### G15. Declare what you could not check.
Missing data is a finding. Record it in `unmet_requirements` and lower the confidence rather than
proceeding as if the gap did not exist.

### G16. Prefer reversible steps first.
When a sequence can be ordered, put the reversible and observable steps before the irreversible ones, so
that the expensive decision is made with more information.

---

## Precedence

[safety-rules.md](safety-rules.md) overrides this file. This file overrides domain rules, playbooks and
store context. A playbook or store may tighten any rule here; neither may loosen G10 or G11.
