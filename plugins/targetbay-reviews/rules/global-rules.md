# Global Rules

These apply to every skill in this package. Skills cite them by number, e.g. `global-rules.md#G3`.

---

### G1. Proof that converts outranks proof that accumulates.
Review count is a diagnostic, not a goal. When two options conflict, prefer the one with better evidence
of impact on conversion, AOV, return rate or repeat purchase. A product page that gained forty reviews and
no conversion did not gain anything. Say so explicitly when you conclude it.

### G2. Every recommendation must rest on available evidence.
If the data to support a recommendation does not exist, either lower the confidence and say why, or do not
make the recommendation. Evidence means an observed value from a declared capability, with a period and a
sample size. See [../schemas/recommendation.schema.json](../schemas/recommendation.schema.json).

### G3. Never invent review, customer, product or order data.
No illustrative numbers presented as real. No "stores in your category usually sit at 4.6." If a figure is
a benchmark rather than this store's data, label it as a benchmark. If nothing is known, say nothing is
known. Never paraphrase a review you have not read.

### G4. A rating is a distribution, not a number.
Never plan against an average alone. A 4.4 built from thirty fives and ten ones is a different problem
from a 4.4 built from consistent fours, and the second is not a problem at all. Read the distribution via
`reviews.ratings_analytics` before concluding anything about a rating.

### G5. Review coverage is a per-product property, not a store property.
A store average hides the products that carry nothing. Locate the gap through
`reviews.product_coverage` before proposing programme-wide changes, because the fix for "sixty products
have no reviews" is not the fix for "the rating is drifting down."

### G6. Request timing is a function of the product, not of the order.
Ask after the customer has had the product long enough to have an opinion, which depends on delivery date
and on what the product is. Never anchor a request delay to order date when
`reviews.order_intelligence` can supply fulfilment timing. See
[request-rules.md](request-rules.md).

### G7. Inspect the existing programme before adding to it.
Read current request configuration, placements and moderation policy first. A second request flow on the
same trigger competes with the first and doubles the fatigue without doubling the submissions.

### G8. Prefer the simplest change that closes the gap.
Complexity is only justified by measurable value. Fixing the delay on one existing request usually beats
designing a four-stage programme nobody will maintain.

### G9. Negative reviews are information before they are a problem.
A falling rating is first diagnosed — which products, which attributes, which period, which change
preceded it — and only then responded to. A response strategy built before the cause is known is a guess.
See [response-rules.md](response-rules.md).

### G10. Deterministic business rules belong to the platform, not to the agent.
Consent, suppression, request frequency caps, moderation policy enforcement and verified-buyer
determination are enforced by TargetBay Reviews and the commerce platform. Plan within them; never
attempt to reimplement, bypass or approximate them.

### G11. High-impact actions require explicit human approval.
Anything that reaches real recipients, is published under the store's name, or is hard to reverse stops
for a decision. See [safety-rules.md](safety-rules.md).

### G12. Only claim what the platform can verify.
"Verified buyer" is a platform determination, not an inference. Do not label, badge or describe a review
as verified unless `reviews.review_content` says it is. The same holds for media rights: do not plan to
reuse UGC whose rights status is unknown.

### G13. Respect consent and request frequency at planning time.
Do not plan requests the platform will refuse, and do not plan requests that are technically permitted but
will fatigue the customer — particularly across several products from one order.

### G14. Explain material recommendations with their evidence.
Any recommendation that changes outreach, moderation posture, placement or distribution is stated together
with the evidence and the reasoning that produced it. An unexplained recommendation cannot be reviewed,
and an unreviewable recommendation should not be executed.

### G15. Declare what you could not check.
Missing data is a finding. Record it in `unmet_requirements` and lower the confidence rather than
proceeding as if the gap did not exist.

### G16. Prefer reversible steps first.
When a sequence can be ordered, put the reversible and observable steps before the irreversible ones — a
placement change before a syndication switch, one request cohort before the whole backlog — so the
expensive decision is made with more information.

---

## Precedence

[safety-rules.md](safety-rules.md) overrides this file. This file overrides domain rules, playbooks and
store context. A playbook or store may tighten any rule here; neither may loosen G10, G11 or G12.
