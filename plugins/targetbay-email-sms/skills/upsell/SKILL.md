---
name: upsell
description: Use when the objective is increasing order value rather than order count — moving customers to higher-value versions, larger sizes, bundles or subscriptions, or raising average order value through thresholds and merchandising. Use cross-sell when the goal is a purchase in a different category.
license: MIT
metadata:
  targetbay.display_name: Upsell
  targetbay.version: "1.0.0"
  targetbay.category: revenue
  targetbay.requires: email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.campaign_analytics
  targetbay.composes: audience-discovery
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Upsell

## Purpose

Raise average order value by moving customers to higher-value options they would plausibly choose —
based on observed price-band behaviour rather than on the assumption that everyone can be moved upward.

AOV is the third term of the revenue equation and often the least worked. It is also the easiest to
damage: pushing premium options at price-sensitive customers suppresses conversion, and the loss shows up
as fewer orders rather than as an obvious upsell failure.

## When to Use

- AOV is flat or has declined
- A premium tier, bundle or subscription needs adoption
- Deciding threshold mechanics such as free-shipping or gift levels
- Post-purchase or pre-checkout value-raising messaging
- Identifying customers whose price-band behaviour suggests headroom

## When Not to Use

- The goal is more orders. Use [customer-retention](../customer-retention/SKILL.md).
- The goal is a different category. Use [cross-sell](../cross-sell/SKILL.md).
- The store's pricing strategy itself is the question — that is outside this package.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| AOV distribution, not just the average | The average hides the distribution that matters | Blocked |
| Per-customer price-band behaviour | Who has demonstrated headroom | Blocked |
| Product tiers, bundles, sizes, subscription options | What there is to move customers to | Blocked |
| Discount dependence per customer | Who is price-sensitive and must not be pushed | Partial |
| Threshold response history | Whether threshold mechanics work here | Partial |
| Margin posture by tier | Whether a higher order value is actually worth more | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.order_intelligence` | AOV distribution, basket composition, threshold behaviour |
| `email_sms.customer_intelligence` | Price-band behaviour, value, discount dependence |
| `email_sms.product_intelligence` | Tiers, bundles, sizes, subscriptions, margin signals |
| `email_sms.segmentation` | Sizing candidate audiences |
| `email_sms.campaign_analytics` | Prior upsell and threshold results |

## Inputs

| Input | Required | Notes |
|---|---|---|
| `target_products_or_tiers` | no | If the store wants specific options promoted |
| `mechanism` | no | Tier, bundle, size, subscription, threshold |
| `aov_target` | no | Shapes ambition; never overrides evidence |
| `constraints` | no | Margin floors, discount policy, brand positioning |
| `playbook` | no | Vertical overlay |

## Decision Process

```
1. Read the AOV distribution, not the average
2. Identify customers with demonstrated headroom   ← prior higher-band purchases, rising basket value
3. Identify price-sensitive customers              ← exclude them from premium pushes
4. Match mechanism to segment                      ← tier, bundle, size, subscription, threshold
5. Decide the moment                               ← pre-purchase, in-basket, post-purchase, replenishment
6. Delegate audience definition
7. Size the effect on revenue and on margin
```

## Decision Rules

Binding: [../../rules/personalization-rules.md](../../rules/personalization-rules.md),
[../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../knowledge/marketing-principles.md](../../knowledge/marketing-principles.md).

- Work from the distribution. A single average AOV conceals the bands where movement is possible.
- Only target customers whose behaviour shows headroom. Pushing premium at the price-sensitive costs
  conversion (C5).
- Thresholds are usually the lowest-risk mechanism: they raise value without repositioning the customer,
  and they are set from the observed distribution — just above the common basket value, not at a round
  number.
- Bundles must offer genuine value at protected margin, not a discount wearing a different name (C4).
- Subscription upsell is a retention mechanism as much as an AOV one; evaluate it on both.
- Check margin, not only revenue. A higher order value at a lower margin can be a loss.
- Never misrepresent the value of the higher option (N3, N7).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read AOV distribution, price-band behaviour, product tiers, margin | `read_only` |
| ANALYZE | Locate headroom, exclude price-sensitive, match mechanisms | `analysis` |
| PLAN | Choose mechanism, audience, moment and content direction | `recommendation` |
| PREVIEW | Present ranked opportunities with revenue and margin effect | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human selects what proceeds | — |
| EXECUTE | Built by the owning skill | `mutation` |
| MEASURE | AOV by targeted segment, and conversion rate alongside it | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) with recommendations conforming to
[../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json): the mechanism, the
audience and size, the moment, expected AOV effect with evidence, margin effect, and risks — including
the conversion risk of pushing value at the wrong segment.

## Validation

- [ ] AOV distribution examined, not just the average
- [ ] Headroom evidenced per targeted segment (G2)
- [ ] Price-sensitive customers excluded from premium pushes (C5)
- [ ] Threshold levels derived from the observed distribution, not rounded
- [ ] Margin effect stated alongside revenue effect
- [ ] Conversion risk stated
- [ ] Audiences resolved and sized (A1)
- [ ] No misrepresented value claims (N3)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend | `recommendation` | None |
| Build a campaign or journey | `mutation` | Preview, then confirm |
| Send or activate | `high_impact` | Explicit |

## Examples

**"Raise our average order value."**
The distribution is bimodal: a large cluster just below a natural bundle price and a smaller premium
cluster. Recommends a free-shipping threshold set just above the lower cluster's typical basket, and a
bundle aimed at that same group — explicitly not a premium-tier push, because that group's price-band
history shows no headroom.

**"Promote our premium tier."**
Identifies the subset with prior higher-band purchases or rising basket values as the only audience with
evidenced headroom, and recommends targeting them rather than the whole base. States that a broad push
would likely depress conversion among the price-sensitive majority.

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.order_intelligence` unavailable | **Blocked.** AOV work needs the distribution |
| No higher-value options in the catalogue | Report it. This is a merchandising problem, not a messaging one |
| No evidenced headroom in any segment | Recommend threshold mechanics only, and say why tier pushes are not supported |
| Margin data unavailable | **Partial.** State that the recommendation optimises revenue, and that margin is unverified |
| Store insists on a broad premium push | Plan it, state the conversion risk explicitly, and recommend testing on a subset first |

Degraded outcomes set `status` and populate `unmet_requirements`.
