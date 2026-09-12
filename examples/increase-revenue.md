# Trace: "Increase revenue this month."

> Illustrative. Figures below are placeholders that stand in for what the capabilities would return —
> they are not real store data, and the reasoning, not the numbers, is the point.

## Prompt

```
Increase revenue this month.
```

## Skill selection

[revenue-growth](../skills/revenue-growth/SKILL.md) — the objective is revenue with no instrument
specified, so the question is *where* growth can come from before anything is scheduled.

Not selected:
- [monthly-marketing-planner](../skills/monthly-marketing-planner/SKILL.md) — would produce a calendar
  before deciding what the calendar is for
- [campaign-optimization](../skills/campaign-optimization/SKILL.md) — no campaign was named

Composed: [audience-discovery](../skills/audience-discovery/SKILL.md),
[automation-strategy](../skills/automation-strategy/SKILL.md),
[campaign-optimization](../skills/campaign-optimization/SKILL.md).

## DISCOVER

| Capability | Read for |
|---|---|
| `bayengage.store_profile` | Vertical, scale, sending posture |
| `bayengage.order_intelligence` | Revenue by period, product and cohort; intervals; AOV distribution |
| `bayengage.customer_intelligence` | Lifecycle distribution, value concentration, engagement |
| `bayengage.product_intelligence` | Product performance, stock posture |
| `bayengage.campaign_analytics` | What has produced revenue before |
| `bayengage.automation` + `bayengage.automation_analytics` | Existing journey coverage and revenue |
| `bayengage.marketing_calendar` | What is already committed this month |

## ANALYZE

Revenue decomposed into its three terms
([knowledge/marketing-principles.md](../knowledge/marketing-principles.md)):

| Term | Observation *(illustrative)* |
|---|---|
| Customers | New-customer volume steady |
| Frequency | **Weak.** A large first-purchase cohort from the prior quarter has not returned |
| AOV | Flat, with a dense cluster just below a natural bundle price |

Automation coverage shows welcome, abandonment and a generic post-purchase journey — **no
second-purchase journey**. The largest leak and the largest coverage gap are the same thing.

Calendar shows two committed sends. Cadence against the engaged segment is already near the store's
normal level, so there is limited room for additional campaigns.

## Decisions

**1. Attack frequency, not acquisition.** Revenue decomposition puts the weakness in the frequency term
and the base already exists ([knowledge/marketing-principles.md](../knowledge/marketing-principles.md),
G1). Acquisition would be slower, more expensive, and would not fix the leak it feeds into.

**2. Build the second-purchase journey first.** An automation earns repeatedly where a campaign earns
once (G7, G16), it addresses the largest measurable leak, and the audience flows through it continuously.
Delegated to [automation-strategy](../skills/automation-strategy/SKILL.md) →
[automation-architect](../skills/automation-architect/SKILL.md).

**3. One win-back campaign, targeted rather than broad.**
[audience-discovery](../skills/audience-discovery/SKILL.md) returns the dormant cohort with the strongest
prior affinity as the highest-ranked audience; broader dormant segments rank lower on expected value and
would consume the limited cadence headroom (A11, F2).

**4. Add an AOV mechanic to the two committed sends rather than adding sends.** Cadence has no room
(F2, F3), and the AOV cluster suggests a threshold mechanic will work without a discount.

**5. Reject a sitewide discount.** It would move revenue forward from customers who would have bought
anyway, at a margin cost the evidence does not justify (C4, C5). Recorded as a rejected opportunity so it
is not re-proposed next month.

## Output

A [skill result](../schemas/skill-result.schema.json) with four ranked
[recommendations](../schemas/recommendation.schema.json), each carrying evidence, period, sample size,
risks and next actions. Plus the revenue decomposition, the rejected opportunities, and the cadence
constraint that shaped the plan.

```
1. Build second-purchase automation      frequency   high     → automation-strategy
2. Win-back campaign, affinity-targeted  customers   high     → audience-discovery + campaign
3. Threshold mechanic on committed sends AOV         medium   → upsell
4. Review the underperforming send       —           low      → campaign-optimization
```

## Approval

Nothing has changed yet — [revenue-growth](../skills/revenue-growth/SKILL.md) is `recommendation` risk and
mutates nothing. Approval happens downstream:

- Creating the automation → `mutation`, previewed and confirmed
- **Activating** it → `high_impact`, explicit approval (S2)
- **Sending** the win-back campaign → `high_impact`, explicit approval with recipient count (S4)

## What the skill refused to do

- Invent an expected percentage lift. Every figure traces to store data or is absent (G3)
- Fill the month with campaigns to look thorough — cadence headroom was the binding constraint (G7, F2)
- Recommend the sitewide discount, despite it being the fastest path to short-term revenue (C4)
- Assume the dormant cohort was reachable without checking consent and engagement (G4, A10)
