---
name: fashion
display_name: Fashion, Apparel and Accessories
version: 1.0.0
applies_to: Apparel, footwear and accessories retail with seasonal collections, size and fit variables, and high return rates.
overrides:
  - default thresholds
  - lever priority
  - seasonal emphasis
  - lifecycle emphasis
---

# Fashion Playbook

Assumes [../ecommerce/PLAYBOOK.md](../ecommerce/PLAYBOOK.md) and states the differences.

## Vertical Signals

- Catalogue turns over by season or collection rather than persisting
- Size, fit and colour are purchase variables, and size is a durable customer attribute
- Return rates are materially higher than general e-commerce, and returns are a normal part of the
  purchase process rather than a failure
- Inventory is finite per size, so sell-out is size-specific rather than product-specific
- Repeat purchase is driven by newness and season, not by consumption

## Default Adjustments

**Replenishment is mostly inapplicable.** Fashion repeat purchase follows collection cycles and personal
occasions, not consumption intervals. Replace replenishment timing with collection-launch timing in the
automation baseline.

**Seasonality dominates the calendar.** Collection launches, end-of-season clearance and weather
transitions are the structural anchors. Plan the year around them and fit other activity between.

**Lever priority** shifts toward:

1. New-collection launches to affinity audiences
2. Size-and-fit-aware personalisation
3. Category expansion across the wardrobe
4. End-of-season clearance to price-sensitive segments
5. Retention through newness rather than through incentive
6. Win-back timed to a new collection rather than to a discount

**Thresholds.**

- Lapse point is usually collection-cycle length, not the customer's mean interval
- Clearance segments are defined by demonstrated price-band behaviour, not by lapse state
- Size availability, not product availability, is the stock check that matters

## Additional Rules

- **FA1.** Never promote a product to a customer whose size is out of stock. This is the vertical's
  signature failure, and it is worse than not sending at all.
- **FA2.** Size and fit are personalisation data only when the platform holds them for that specific
  contact. Never infer size from anything (P1, P7).
- **FA3.** Returns are normal. Do not treat a return as a churn signal, and do not exclude returners from
  marketing by default — the return often precedes a successful repurchase.
- **FA4.** Clearance goes to price-sensitive and lapsed segments, not to full-price buyers who would have
  bought the new collection anyway (C5).
- **FA5.** Collection launches use wave sequencing by category and style affinity — see
  [../../skills/product-launch/SKILL.md](../../skills/product-launch/SKILL.md). Announcing a collection to
  the whole list simultaneously wastes the information the first wave would have given.

## Lifecycle Notes

| Stage | Vertical emphasis |
|---|---|
| Prospect | Style and fit orientation; first-purchase risk is fit risk, so reduce that rather than price |
| New customer | Delivery, fit guidance and returns clarity — reassurance reduces return-driven churn |
| First-time buyer | Second purchase is usually cross-category within the wardrobe |
| Repeat buyer | Collection launches and style affinity |
| VIP | Early access to collections is the strongest available lever, and costs no margin |
| At-risk | Detect against the collection cycle, not a consumption interval |
| Dormant | Re-engage on a new collection; a discount alone rarely recovers a style-driven lapse |

## Channel Notes

- Email is strongly visual here and carries collection and lookbook content that SMS cannot.
- SMS works for drop announcements, size restocks and the last day of a clearance window — moments where
  immediacy is the entire value.
- Back-in-stock notification for a specific size is one of the highest-intent messages in this vertical and
  is worth building deliberately.

## Known Limits

- **Basics and essentials brands** behave more like general e-commerce: replenishment applies, seasonality
  is weaker. Use [../ecommerce/PLAYBOOK.md](../ecommerce/PLAYBOOK.md).
- **Luxury** operates on discount avoidance and scarcity; the clearance guidance here is actively wrong.
- **Made-to-order and bespoke** have long fulfilment cycles that invalidate the post-purchase timing.
- **Resale and consignment** have unique-item inventory, so nearly every stock and affinity assumption
  breaks.
