---
name: beauty
display_name: Beauty, Skincare and Personal Care
version: 1.0.0
applies_to: Cosmetics, skincare, haircare and personal care retail with consumable products, routine-based usage and measurable replenishment intervals.
overrides:
  - default thresholds
  - lever priority
  - lifecycle emphasis
---

# Beauty Playbook

Assumes [../ecommerce/PLAYBOOK.md](../ecommerce/PLAYBOOK.md) and states the differences.

## Vertical Signals

- Products are consumable, with usage-driven reorder intervals that differ by product size and type
- Customers build routines — multi-product sets that are bought and replaced together
- Shade, skin type and concern are purchase variables, and are often held as customer attributes
- Sampling and trial sizes are a normal path into a full-size purchase
- Repeat purchase rates are structurally high compared to most retail

## Default Adjustments

**Replenishment is the primary lever, not a secondary one.** Consumables with measurable intervals make
reorder timing the highest-value automation in most beauty stores. It leads the automation baseline rather
than following abandonment.

**Lever priority:**

1. Replenishment timed per product and size
2. Routine completion — the adjacent products in a regimen
3. Retention through the routine rather than through discount
4. Trial-to-full-size conversion
5. Cross-category expansion within the regimen
6. Win-back timed to the expected run-out point

**Thresholds.**

- Reorder interval is derived per product *and* size — a large and a small format of the same product have
  different intervals
- The reminder fires ahead of run-out, not after it; the lead time is the store's observed delivery time
  plus a buffer
- Lapse detection for a consumable buyer is a missed reorder, which is a much earlier and stronger signal
  than a general engagement drop

## Additional Rules

- **B1.** Reorder timing is derived per product and size, never as a single store-wide interval. A
  store-wide reminder cadence is the most common way this vertical's largest lever is wasted.
- **B2.** Shade, skin type and concern are used only when the platform holds them for that contact
  (P1). Never infer them from anything, including from previous purchases of an adjacent product.
- **B3.** Do not make efficacy, health or clinical claims (N3). Where a store has substantiated claims,
  use the store's own approved wording rather than generating new phrasing.
- **B4.** Routine completion recommendations come from observed co-purchase data, not from assumed
  regimen logic (E1).
- **B5.** Treat sensitive inferences — skin conditions, hair loss, ageing concerns — as off-limits for
  personalisation even when purchase data implies them (P7).

## Lifecycle Notes

| Stage | Vertical emphasis |
|---|---|
| Prospect | Trial and sampling paths; concern-led rather than product-led messaging |
| New customer | Usage guidance — how to use it, how long it lasts. This sets up the reorder |
| First-time buyer | Either a reorder or the next routine step; both are strong |
| Repeat buyer | Reorder timing is the whole relationship; get it right before anything else |
| VIP | Early access to launches and limited editions; sampling of new products |
| At-risk | A missed reorder is the signal, and it fires far earlier than engagement decay |
| Dormant | Time the return to the expected run-out point of their last purchase |

## Channel Notes

- Email carries routine education, regimen content and launches.
- SMS is well suited to the reorder reminder itself, where consent exists — it is short, timely and
  genuinely useful, which is exactly the SMS profile.
- Reorder reminders are the one recurring message in this vertical customers routinely welcome. Do not
  dilute that by attaching unrelated promotion to them.

## Known Limits

- **Devices and tools** are durables, not consumables. The replenishment emphasis does not apply.
- **Fragrance** has long and highly variable intervals; treat it closer to fashion than to skincare.
- **Professional and salon supply** is closer to B2B — see [../b2b/PLAYBOOK.md](../b2b/PLAYBOOK.md).
- **Subscription-led beauty** replaces most of this with churn and billing management.
- Stores with heavy gifting seasonality will find the reorder interval polluted by gift purchases;
  separate gift orders before deriving intervals where the data allows it.
