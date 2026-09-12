# Global Rules

These apply to every skill in this package. Skills cite them by number, e.g. `global-rules.md#G3`.

---

### G1. Incremental behaviour outranks programme metrics.
Enrolment count, points issued and tier population are diagnostics, not goals. A programme is worth what
it changes about behaviour that would not have happened anyway. When two options conflict, prefer the one
with better evidence of incremental repeat rate, frequency, AOV or retention — and say so explicitly.

### G2. Every recommendation must rest on available evidence.
If the data to support a recommendation does not exist, either lower the confidence and say why, or do not
make the recommendation. Evidence means an observed value from a declared capability, with a period and a
sample size. See [../schemas/recommendation.schema.json](../schemas/recommendation.schema.json).

### G3. Never invent member, order, margin or programme data.
No illustrative numbers presented as real. No "loyalty programmes typically lift retention 20%." If a
figure is a benchmark rather than this store's data, label it as a benchmark. If nothing is known, say
nothing is known.

### G4. Points are a liability before they are a reward.
Every issued point is an obligation the store carries until it is burned or expires. Read outstanding
liability and its ageing from `loyalty.points_ledger` before recommending anything that changes issuance.
See [economics-rules.md](economics-rules.md).

### G5. Members are not a control group for themselves.
Members buy more than non-members in almost every store, and almost none of that difference is caused by
the programme — high-value customers join programmes. Any claim of programme effect states how selection
was accounted for, or states that it was not and lowers the confidence accordingly.

### G6. Inspect the existing programme before changing it.
Read the current configuration, tiers, catalogue and member distribution first. A redesign proposed
without knowing what members currently hold is a proposal to break [safety-rules.md#S2](safety-rules.md)
by accident.

### G7. Prefer the simplest structure that changes behaviour.
Complexity is only justified by measurable value. Tiers, bonus multipliers, challenges and badges each add
maintenance and confusion, and a programme members cannot explain to themselves is a programme they do not
act on. See [tier-rules.md](tier-rules.md).

### G8. Do not create a tier, reward or rule that changes nothing.
A tier is only worth having if members behave differently to reach or keep it. A reward is only worth
listing if somebody redeems it. Structure that produces no behaviour change is pure liability and
overhead.

### G9. Earn and burn are one system.
Issuance without redemption is an accumulating liability and a disappointed member. Redemption without
issuance is a discount programme. Never tune one without reading the other
([economics-rules.md](economics-rules.md)).

### G10. Deterministic business rules belong to the platform, not to the agent.
Balance arithmetic, tier qualification, expiry enforcement, redemption eligibility, consent and
suppression are enforced by TargetBay Loyalty and the commerce platform. Plan within them; never attempt
to reimplement, bypass or approximate them.

### G11. High-impact actions require explicit human approval.
Anything that changes what a member holds, reaches real members, or is hard to reverse stops for a
decision. See [safety-rules.md](safety-rules.md).

### G12. Never propose a change that reduces what members already earned without saying so plainly.
If a recommendation has that effect — directly or through repricing, expiry or tier restructuring — it is
stated as its own finding with its own approval, never folded into a larger proposal
([safety-rules.md#S2](safety-rules.md)).

### G13. Programme messaging is marketing and obeys marketing constraints.
Enrolment is not consent. Plan programme communication within consent, suppression and frequency, and
reconcile it with whatever else is contacting the same member — the loyalty product is rarely the only
system sending.

### G14. Explain material recommendations with their evidence.
Any recommendation that changes economics, structure, eligibility or messaging is stated together with the
evidence and the reasoning that produced it. An unexplained recommendation cannot be reviewed, and an
unreviewable recommendation should not be executed.

### G15. Declare what you could not check.
Missing data is a finding. Record it in `unmet_requirements` and lower the confidence rather than
proceeding as if the gap did not exist.

### G16. Prefer reversible steps first.
When a sequence can be ordered, put the reversible and observable steps before the irreversible ones — a
reward added before an earn rate changed, one segment before the whole base — so the expensive decision is
made with more information.

---

## Precedence

[safety-rules.md](safety-rules.md) overrides this file. This file overrides domain rules, playbooks and
store context. A playbook or store may tighten any rule here; neither may loosen G10, G11 or G12.
