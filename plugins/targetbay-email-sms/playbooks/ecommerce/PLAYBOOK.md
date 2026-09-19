---
name: ecommerce
display_name: General E-commerce
version: 1.1.0
applies_to: Direct-to-consumer online retail with a catalogue that supports repeat purchase. The baseline overlay that the other playbooks assume and differ from.
overrides:
  - default thresholds
  - lever priority
  - lifecycle emphasis
  - recipe priority
---

# General E-commerce Playbook

## Vertical Signals

Check these against store data before applying anything below:

- Repeat purchase is possible and common — the catalogue is not a one-time purchase
- Order-level data with products, categories and prices is available
- Purchase intervals are measurable and vary meaningfully by category
- A meaningful share of customers have bought exactly once
- Revenue concentrates in a minority of customers

If repeat purchase is structurally rare, most of this overlay does not apply — see `Known Limits`.

## Default Adjustments

**Lifecycle emphasis.** The first-to-second purchase transition is the default priority when no other
objective is stated. It is usually where the largest addressable loss sits.

**Lever priority** for revenue work, before store evidence reorders it:

1. Retention and repeat purchase
2. Replenishment timing where the catalogue supports it
3. AOV mechanics — thresholds and bundles
4. Cross-category expansion
5. Win-back of the reachable lapsed base
6. Acquisition support

**Thresholds.** Derive from the store's own distributions, not from round numbers:

- Lapse point: the customer's own interval plus a margin, per category
- Free-shipping threshold: just above the dense part of the basket-value distribution
- VIP boundary: where the value distribution actually breaks, not a fixed percentile

**Automation coverage baseline.** For a store with no automations, build in this order: welcome,
post-purchase, abandonment, second-purchase, replenishment where applicable, win-back. Coverage before
sophistication ([../../rules/automation-rules.md](../../rules/automation-rules.md)).

**Planning cadence.** Assume a monthly planning rhythm with the calendar reviewed against automation
contact load before campaigns are added.

## Additional Rules

- **E1.** Product recommendations come from observed co-purchase data, never from catalogue adjacency
  alone. Category structure is a merchandising decision, not evidence of customer behaviour.
- **E2.** Check stock and product status before promoting anything. Promoting a discontinued or
  out-of-stock product is the most common avoidable e-commerce error (P9, N3).
- **E3.** Post-purchase messaging waits for delivery before it sells again. The gap is the store's
  observed delivery time, not a fixed interval.
- **E4.** Discount depth is matched to customer value, not to campaign urgency (C5).
- **E5.** Exclude recent purchasers of a promoted product from its promotion. This is the most visible
  targeting failure to a customer.

## Lifecycle Notes

| Stage | Vertical emphasis |
|---|---|
| Prospect | Reduce first-purchase friction; avoid opening with a discount that trains dependence |
| New customer | Delivery reassurance and product usage; do not sell again yet |
| First-time buyer | The priority transition. Timing derives from the observed first-to-second gap |
| Repeat buyer | Replenishment and category expansion |
| VIP | Access and recognition; discount depth here is usually wasted margin |
| At-risk | Detect on the customer's own interval, not a store-wide number |
| Dormant | Relevance first, incentive second |
| Churned | Bounded win-back, then suppression as a deliverability decision |

## Channel Notes

- Email carries the programme. SMS is reserved for delivery-adjacent updates, real deadlines and
  high-value cart recovery.
- SMS economics require a higher bar per message — see
  [../../knowledge/sms-principles.md](../../knowledge/sms-principles.md).
- Transactional moments — order confirmation, shipping, delivery — are the highest-attention messages the
  store sends, and are frequently under-used as relationship moments. Treat any marketing content added
  to them as subject to consent and to the store's own policy.

## Known Limits

This playbook is wrong for:

- **Single-purchase categories** — high-ticket durables where repeat purchase is rare. The retention
  emphasis misallocates effort; referral and review generation matter more.
- **Subscription-first businesses** — retention is a churn and billing problem, not a campaign problem.
- **Marketplaces** — customer relationship and catalogue control are split between parties.
- **Very new stores** — nearly every threshold here is derived from history that does not exist yet. Use
  the coverage baseline, label the rest provisional, and revisit once intervals are measurable.
- **B2B** — see [../b2b/PLAYBOOK.md](../b2b/PLAYBOOK.md); the buying process is structurally different.

## Recipe Priority

A prior for [automation-recipe-selector](../../skills/automation-recipe-selector/SKILL.md), which
re-ranks it on store evidence. Each entry names the signal to check before believing it.

1. **Lifecycle recipes** — cart recovery first, then welcome, then order confirmation and the review
   request. *Check:* that an abandonment signal is distinguishable from a completed order; without it
   cart recovery cannot be built correctly and welcome moves to first.
2. **Retention sweeps** — churn-risk scoring, then dormant re-engagement. *Check:* that purchase
   intervals are measurable per contact; a store-wide interval makes every infrequent buyer look at risk.
3. **List health** — the hygiene audit before the bounce responder. *Check:* that bounce classification
   comes from the platform; nothing here should classify a bounce itself.
4. **Measurement** — the A/B cycle and the periodic summary. *Check:* that volume can resolve a
   difference at all, before automating a test that will report noise weekly.
5. **AI-assisted** — last, and only once the approval gate has an owner with time to staff it.

This is the baseline order the other four playbooks differ from; nothing in the library is
structurally inapplicable here.
