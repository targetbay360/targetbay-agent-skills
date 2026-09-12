# Targeting Rules

Constraints on who sees what. Cited as `targeting-rules.md#T3`.

---

### T1. Start from the decision, not from the data.
Segment because two groups should see different things, not because the platform can tell them apart. A
targeting scheme derived from available attributes rather than from intended differences produces
segments nobody can act on ([global-rules.md#G8](global-rules.md)).

### T2. State the anonymous path for every scheme.
Most visitors are not identified. Every targeting scheme names what an anonymous visitor sees, and that
path is designed rather than inherited as a fallback
([global-rules.md#G12](global-rules.md)).

### T3. Size every segment before proposing it.
A segment too small to produce a measurable result is a maintenance cost with no evidence attached. State
the traffic share and say plainly when a segment cannot be evaluated at this store's volume.

### T4. Exclusions are part of the targeting, not an afterthought.
Who must not see an offer is as much a design decision as who should: customers who already bought the
item, members in an active flow from another system, visitors who dismissed it, out-of-region traffic.
State exclusions explicitly.

### T5. Never target on a sensitive attribute or its proxy.
Health, pregnancy, sexuality, religion, ethnicity, immigration status, financial distress and political
affiliation are out of bounds, including when inferred from browsing behaviour. Name the proxy when
rejecting a proposal that uses one ([safety-rules.md#S3](safety-rules.md)).

### T6. Session intent outranks historical profile for anonymous traffic.
What a visitor is doing right now — entry query, category viewed, cart state — predicts better than a thin
historical profile and requires less of them. Prefer it where both are available.

### T7. Do not personalise a surface whose default already works.
Replacing a well-performing default with a personalised variant risks a loss for an unproven gain. The
default is the baseline, and the burden is on the variant
([measurement-rules.md#M2](measurement-rules.md)).

### T8. Frequency caps are per visitor, across all surfaces.
Offers, popups and interstitials compete for the same tolerance. A cap that applies per-campaign rather
than per-visitor is not a cap ([safety-rules.md#S5](safety-rules.md)).
