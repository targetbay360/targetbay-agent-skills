# Trace: "Improve our post-purchase marketing."

> Illustrative. Figures are placeholders standing in for capability output, not real store data.

## Prompt

```
Improve our post-purchase marketing.
```

## Skill selection

[automation-strategy](../skills/automation-strategy/SKILL.md) assesses whether post-purchase is the right
place to spend effort at all, then [automation-architect](../skills/automation-architect/SKILL.md) designs
the topology. [audience-discovery](../skills/audience-discovery/SKILL.md) sizes every candidate variant.

Not selected: [automation-optimization](../skills/automation-optimization/SKILL.md) — the question is
whether the *shape* is right, not whether an existing journey needs tuning. If analysis had shown the
structure was sound, the work would have handed over to that skill instead.

## DISCOVER

`bayengage.automation` for the existing portfolio and topology; `bayengage.automation_analytics` for
per-node performance; `bayengage.customer_intelligence` for lifecycle distribution;
`bayengage.order_intelligence` for repeat intervals and AOV; `bayengage.product_intelligence` for
categories and attributes; `bayengage.segmentation` for sizing.

## ANALYZE

*(illustrative)*

- One generic post-purchase journey exists: three nodes, fires on every order, identical for everyone
- Per-node data shows healthy engagement on node one and a sharp drop at node two
- First-time buyers convert to a second purchase at a materially different rate than repeat buyers
- The catalogue splits into consumables with measurable reorder intervals and durables without
- VIP orders are a small share of volume

## Candidate variants

Generated broadly, then eliminated against
[rules/automation-rules.md#R4](../rules/automation-rules.md) — size, difference, value, coverage:

| Candidate | Size | Difference | Value | Coverage | Verdict |
|---|---|---|---|---|---|
| First-time buyer | ✓ | ✓ different objective — the second purchase | ✓ | gap | **Build** |
| Repeat buyer | ✓ | ✓ replenishment and expansion, not conversion | ✓ | partial | **Build** |
| Consumable purchase | ✓ | ✓ reorder timing exists | ✓ | gap | **Build** |
| Durable purchase | ✓ | ✓ usage and care, no reorder | ✓ | gap | folded into repeat-buyer branch |
| VIP | ✗ too small to measure | ✓ | — | — | **Fold in as a branch** |
| High-AOV | ✓ | ✗ treatment would be the same | — | — | **Reject** |
| Discount-led purchase | ✓ | ✗ no commercially meaningful difference | — | — | **Reject** |
| Category-specific | ✗ per category | ✓ | ✗ | — | **Reject** — personalise instead |

Rejected candidates are recorded in `rejected_variants`
([rules/automation-rules.md#R5](../rules/automation-rules.md)) so the same splits are not re-proposed at
the next review.

**Three journeys, not eight, and not one.** The assumption "one objective = one automation" (R1) would
have produced one; the assumption that every technically possible split is worth making (R3) would have
produced eight.

## Topology

Node counts differ per variant because the journeys differ — there is no shared template
([rules/automation-rules.md#R7](../rules/automation-rules.md)).

**First-time buyer journey** — objective: the second purchase.
Trigger on first order → wait until delivery (derived from observed delivery time, R13) → usage and
reassurance → wait to just before the observed first-to-second purchase gap → affinity-based next-purchase
message → goal: second order → exit on purchase.

**Consumable journey** — objective: reorder.
Trigger on consumable order → wait to the product-and-size reorder interval minus a lead buffer → reorder
message → conditional follow-up only if no order → goal: reorder → exit on purchase.

**Repeat-buyer journey** — objective: expansion.
Trigger on order from a repeat buyer → delivery wait → branch on durable vs consumable → category
expansion message, affinity-selected → VIP branch adds recognition, not discount → goal: next order.

Every node states its purpose (R8). A fourth node was proposed for the first-time journey and removed —
it repeated the third node's message and could not justify itself (R9).

## Decisions with their rules

| Decision | Rule |
|---|---|
| Fold VIP in as a branch rather than a variant | R4 — fails the size test |
| Reject high-AOV and discount-led variants | R4 — fail the difference test |
| Reject per-category variants | R4, and segmentation-vs-personalisation |
| Derive every wait from observed intervals | R13 |
| Give each journey a goal and an exit | R15 |
| Set precedence against the existing abandonment journey | R16 |
| Replace the generic journey rather than adding beside it | R6, G6 |

## Output

A [workflow](../schemas/workflow.schema.json) with three variants, each with audience, size, rationale,
nodes with purpose and timing, edges with branch conditions, exit criteria and success metric — plus
`rejected_variants`, the precedence decision against existing journeys, and the cadence impact.

## Approval

Creating the journeys is `mutation`, previewed and confirmed. **Activating each is `high_impact` and
approved individually** (S2). Retiring the existing generic journey is `destructive` and requires reporting
what is lost and what happens to contacts currently inside it (S6).

## What the skill refused to do

- Assume one objective meant one automation (R1)
- Build all eight candidate variants because the platform would allow it (R3)
- Use a uniform node count across the three journeys (R7)
- Keep the fourth node that repeated the third (R9)
- Add a new journey beside the existing one without deciding what happens to it (G6, R6)
- Set wait intervals to round numbers rather than deriving them (R13)
