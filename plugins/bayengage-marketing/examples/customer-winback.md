# Trace: "Win back our lapsed customers."

> Illustrative. Figures are placeholders standing in for capability output, not real store data.

## Prompt

```
Win back our lapsed customers.
```

## Skill selection

[customer-winback](../skills/customer-winback/SKILL.md), composing
[audience-discovery](../skills/audience-discovery/SKILL.md).

Not selected: [customer-retention](../skills/customer-retention/SKILL.md) — these customers have already
lapsed. Retention would have been the cheaper intervention, and the trace says so: the analysis notes that
an at-risk journey would prevent much of this cohort from reaching win-back at all, and raises it as a
follow-on recommendation.

## DISCOVER

`bayengage.order_intelligence` for purchase history and the store's own intervals;
`bayengage.customer_intelligence` for lapse state, prior value and engagement recency;
`bayengage.suppression_and_consent` for reachability and complaint history;
`bayengage.campaign_analytics` for prior win-back attempts; `bayengage.product_intelligence` for what has
changed since they left.

## ANALYZE

**Lapse is derived, not assumed.** The store's own repeat interval per category defines "late", and a
customer is lapsed relative to *their own* pattern, not a fixed store-wide number
([knowledge/customer-lifecycle.md](../knowledge/customer-lifecycle.md)).

*(illustrative)* The lapsed base splits three ways:

| Group | Prior value | Still engaging | Verdict |
|---|---|---|---|
| A | High | Yes — opens, no purchases | Worth a real sequence |
| B | Moderate | Minimal | One low-cost attempt |
| C | Low | None for a long period | **Suppress** |

Group C is large. Mailing it produces little revenue and imposes a deliverability cost on every other send
the store makes ([knowledge/email-principles.md](../knowledge/email-principles.md)).

## Decisions

**1. Reachability and prior value decide who is worth recovering — not lapse duration.** A long-lapsed
high-value customer who still opens is a better prospect than a recently lapsed low-value one who does not.

**2. Group A: three attempts, escalating relevance before incentive.** What changed since they left, then
their prior affinity, then an incentive. Opening with the deepest discount trains the behaviour and wastes
margin on customers who might have returned for a reason (C4).

**3. Group B: one attempt, then stop.** The stop condition is defined before the first send, not decided
after seeing the response.

**4. Group C: suppression, not another campaign.** Presented with the count and the prior value so the
trade-off is explicit, and with the deliverability cost of the alternative stated. This is `destructive`
and requires explicit approval after reporting what is lost (S6).

**5. Channel: try a different one, not a louder one.** For the subset of Group A with SMS consent, an SMS
attempt is stronger than a fourth email — email has already been ignored (F6). Capability availability is
checked first; `bayengage.messaging_sms` is unverified, so the plan degrades to email-only if it is
absent.

**6. Recovered customers exit immediately** and re-enter the normal lifecycle. Continuing to send win-back
messages to someone who just purchased is the sequence's signature failure.

**7. Follow-on recommendation: build an at-risk journey.** Most of this cohort would not have needed
win-back if intervention had happened when their interval first lengthened
([customer-retention](../skills/customer-retention/SKILL.md)). Recorded as a separate, higher-value
recommendation than the win-back itself.

## Output

A [skill result](../schemas/skill-result.schema.json) containing: three ranked audiences with sizes and
reachability; the attempt sequence per group with channel, offer and spacing; the stop condition; the
suppression recommendation with count and prior value; expected recovery with its evidence; risks
including complaint exposure; and the at-risk journey recommendation.

## Approval

| Action | Risk | Approval |
|---|---|---|
| Create the campaigns | `mutation` | Preview, then confirm |
| Send each attempt | `high_impact` | Explicit, per attempt, with recipient count (S4, S9) |
| SMS attempt | `high_impact` | Explicit, with count and cost |
| **Suppress Group C** | `destructive` | Explicit, after reporting count and prior value (S6) |

## What the skill refused to do

- Mail the entire lapsed base because it is technically reachable
- Open with the deepest discount (C4)
- Leave the attempt count open-ended — the stop condition is set before the first send
- Re-add unsubscribed or suppressed contacts (S7)
- Present suppression as a loss-free cleanup; the count and prior value are stated plainly
- Claim a recovery rate it could not evidence (G3)
