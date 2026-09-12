# Trace: "Plan next month's marketing."

> Illustrative. Figures are placeholders standing in for capability output, not real store data.

## Prompt

```
Plan next month's marketing.
```

## Skill selection

[monthly-marketing-planner](../skills/monthly-marketing-planner/SKILL.md) — a period, no stated objective,
and a request for a calendar.

Composed: [revenue-growth](../skills/revenue-growth/SKILL.md) (what the month should be for),
[audience-discovery](../skills/audience-discovery/SKILL.md) (per campaign),
[holiday-marketing](../skills/holiday-marketing/SKILL.md) (one date in the window),
[product-launch](../skills/product-launch/SKILL.md) (a launch mid-month),
[campaign-optimization](../skills/campaign-optimization/SKILL.md) (what worked last time).

## DISCOVER

| Capability | Read for |
|---|---|
| `email_sms.marketing_calendar` | What is already committed in the window |
| `email_sms.campaign_analytics` | Which campaign types have produced revenue here |
| `email_sms.order_intelligence` | Seasonality, revenue concentration by category |
| `email_sms.customer_intelligence` | Audience availability, engagement, lifecycle mix |
| `email_sms.product_intelligence` | Launches, stock posture, what there is to say |
| `email_sms.automation` | Contact load already committed to each audience |
| `email_sms.suppression_and_consent` | Channel eligibility, frequency caps |

## ANALYZE

*(illustrative)*

- Calendar: two sends already committed; a product launch confirmed for mid-month
- One holiday falls in the window. [holiday-marketing](../skills/holiday-marketing/SKILL.md) assesses
  relevance from prior-period revenue and catalogue fit, and returns **participate, modestly** — there is a
  consistent but small lift, so the recommendation is one send, not a sequence
- Automations contact the engaged segment roughly weekly already
- Seasonality: one category carries a disproportionate share of revenue in this month historically
- The dormant segment has not been contacted in several weeks — headroom exists there that does not exist
  for the engaged segment

## Decisions

**1. Establish capacity before selecting campaigns.** Automation contact is counted first
([rules/frequency-rules.md#F2, #F3](../rules/frequency-rules.md)). The engaged segment has room for
roughly two additional sends; the dormant segment has more. Capacity is a constraint on the plan, not a
discovery made after the calendar is full.

**2. Six campaigns, and the number is justified.** Derived from: two committed, one launch requiring two
sends of its own, one holiday send, and one win-back into the quiet first week. Not a default cadence —
the [Decision Rules](../skills/monthly-marketing-planner/SKILL.md) forbid a fixed count, and the plan
states this derivation.

**3. The launch anchors the middle of the month.** Delegated to
[product-launch](../skills/product-launch/SKILL.md), which sequences by affinity: early access to the
prior-category cohort, then a broader send **contingent on first-wave response and remaining stock**. The
second wave is planned, not committed.

**4. Win-back goes in the first week.** The quiet week has cadence headroom and the dormant segment has
not been contacted. Placing it later would collide with the launch (C7, F8).

**5. The final week is deliberately light.** The following month opens with a larger period, and
[frequency-rules.md#F12](../rules/frequency-rules.md) calls for recovery before intensity. An empty slot
is a valid output.

**6. Rejected: a second holiday send.** The holiday's evidenced lift does not justify the cadence it would
consume, and the launch is the higher-value use of that week (G7, F2).

## Output

A calendar. Each row carries `date`, `campaign`, `objective`, `audience` with size and exclusions,
`channel`, `product`, `offer`, `content_direction`, `expected_outcome`, `dependencies`, `risk`.

```
Week 1   Win-back            frequency    dormant + affinity     email
Week 2   Holiday send        revenue      engaged + relevant     email
Week 3   Launch: early access acquisition prior-category, high value  email
Week 3   Launch: broad       acquisition  full affinity cohort   email + SMS   [contingent]
Week 4   Category push       revenue      engaged + category     email
Week 4   —                   recovery window, deliberately empty
Week 5   Committed send      (existing)
```

Plus: the cadence summary per audience, the campaigns considered and rejected, and the derivation of the
campaign count.

## Approval

The calendar itself is `plan` risk and changes nothing. Creating drafts is `mutation`, previewed and
confirmed. **Each send is approved separately** (S2, S9) — approving a calendar is not approving its
sends, and the contingent launch wave is approved only after the first wave's response is read.

## What the skill refused to do

- Produce a fixed number of campaigns because a month "usually has" that many
- Fill the empty week (G7)
- Plan the engaged segment up to its frequency cap, leaving no room for mid-month opportunities (F1)
- Commit the broad launch wave before the first wave provided evidence
- Assume the holiday mattered without checking prior-period revenue (G2, G3)
