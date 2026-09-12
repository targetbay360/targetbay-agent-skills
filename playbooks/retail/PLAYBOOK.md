---
name: retail
display_name: Multi-channel Retail
version: 1.0.0
applies_to: Retailers operating physical locations alongside online sales, where customer behaviour and inventory are split across channels.
overrides:
  - default thresholds
  - lever priority
  - audience emphasis
---

# Multi-channel Retail Playbook

Assumes [../ecommerce/PLAYBOOK.md](../ecommerce/PLAYBOOK.md) and states the differences.

## Vertical Signals

- A meaningful share of revenue happens in physical locations
- Customer identity is only partially resolved across channels — some in-store purchases are anonymous
- Inventory is location-specific, so availability depends on where the customer is
- Location proximity is a genuine relevance factor, not a demographic proxy
- Store events, local trading hours and regional conditions affect timing

## Default Adjustments

**Attribution is structurally incomplete.** Online marketing frequently drives in-store purchases that
never attribute back. Plan and measure with that stated, and avoid decisions that depend on a clean
online-only attribution picture.

**Lever priority:**

1. Local relevance — location-aware targeting and store-linked messaging
2. Retention across channels rather than within one
3. Store events and local occasions as calendar anchors
4. Cross-channel journeys — online research to in-store purchase, and the reverse
5. AOV mechanics that work in both channels
6. Win-back, with the caveat that a "lapsed" online customer may be an active in-store one

**Thresholds.**

- Lapse must account for unattributed in-store activity. A customer with no online orders may not be
  lapsed at all — be more conservative before suppressing
- Proximity windows are derived from the store's own catchment behaviour, not a fixed radius
- Location-level audiences are checked for size individually; a segment that works nationally may be too
  small per location

## Additional Rules

- **R1.** Never treat online inactivity as churn without checking whether in-store activity is visible. If
  it is not visible, say so and be conservative — suppressing an active in-store customer is a real loss.
- **R2.** Location-based targeting uses the platform's verified location data only, never inferred
  location (P1, A9).
- **R3.** Check location-level stock before promoting a product as available in store (P9, N3).
- **R4.** Respect local time and local trading hours for send timing, particularly for SMS (F9).
- **R5.** Where identity resolution across channels is partial, state the limitation in the plan rather
  than presenting cross-channel figures as complete.

## Lifecycle Notes

| Stage | Vertical emphasis |
|---|---|
| Prospect | Local relevance and store discovery alongside online conversion |
| New customer | Channel preference is unknown early; observe rather than assume |
| First-time buyer | The second purchase may occur in the other channel — measure both |
| Repeat buyer | Cross-channel behaviour is a value signal; multi-channel customers are usually worth more |
| VIP | Store-linked recognition and local event access |
| At-risk | Verify against in-store activity before acting |
| Dormant | Local events and store-specific reasons to return often outperform generic offers |

## Channel Notes

- Email carries the programme and local content well.
- SMS suits store-proximity and same-day messages — pickup ready, local event today, store-specific
  restock — where immediacy and location both matter.
- Location and local time govern SMS send windows more strictly here than in pure online retail.

## Known Limits

- **Franchise or independently operated locations** may not share customer or inventory data, which
  invalidates most cross-channel guidance here.
- **Pure online retailers** should use [../ecommerce/PLAYBOOK.md](../ecommerce/PLAYBOOK.md) instead.
- **Single-location stores** need the local emphasis but not the cross-location segmentation.
- Stores with no in-store identity capture cannot apply the attribution caveats usefully — the data to
  check simply is not there, and the correct response is to say so rather than to assume.
