---
name: b2b
display_name: Business-to-Business and Wholesale
version: 1.1.0
applies_to: Businesses selling to other businesses — wholesale, trade accounts, and considered purchases involving multiple people, longer cycles and account-level relationships.
overrides:
  - default thresholds
  - lever priority
  - lifecycle emphasis
  - audience emphasis
  - recipe priority
---

# B2B and Wholesale Playbook

Assumes [../ecommerce/PLAYBOOK.md](../ecommerce/PLAYBOOK.md) but differs from it more than the other
playbooks do. Several general e-commerce defaults are actively wrong here.

## Vertical Signals

- The buying unit is an account, not a person — several contacts may influence one purchase
- Purchase cycles are long, and the gap between contact and order is measured in weeks or months
- Order values are high and reorder patterns are often contractual or operational rather than emotional
- Revenue is highly concentrated in a small number of accounts
- Pricing is frequently account-specific, and public promotional pricing may be inappropriate
- Seasonality follows business and fiscal cycles, not consumer holidays

## Default Adjustments

**The account is the unit, not the contact.** Lifecycle, value and lapse are computed at account level
wherever the platform can express it. A contact-level view will misread an account entirely — one person
going quiet is not an account going quiet.

**Discounting is usually the wrong lever.** Pricing is often negotiated, and public discounting can
undermine an account relationship or a contract. Reach for information, availability, lead time, service
and account management instead.

**Lever priority:**

1. Account retention and reorder reliability
2. Account expansion — additional categories or volume within an existing account
3. Reactivation of lapsed accounts, which are individually high-value
4. Lead nurture across a long consideration cycle
5. Operational messaging that is genuinely useful — stock, lead times, product changes
6. Promotion, last and rarely

**Thresholds.**

- Lapse is derived from the account's own ordering rhythm, which may be quarterly or annual. A consumer
  lapse window would flag nearly every healthy account
- Value bands are account-level, and the distribution is far more concentrated than in consumer retail
- Audience sizes are small in absolute terms, which changes what is measurable — see B4

## Additional Rules

- **BB1.** Compute lifecycle and value at account level where the platform supports it. State the
  limitation explicitly when it does not.
- **BB2.** Do not apply consumer urgency mechanics — countdowns, flash sales, artificial scarcity. They
  read as unserious to a trade buyer and can damage an account relationship.
- **BB3.** Never expose account-specific pricing in a broadcast message (P11, S11).
- **BB4.** Small audiences are normal here. Statistical testing is usually unavailable; make decisions on
  reasoning and account knowledge, and say explicitly that a recommendation is not test-backed
  ([../../knowledge/experimentation-principles.md](../../knowledge/experimentation-principles.md)).
- **BB5.** Frequency tolerance is lower. A trade contact receiving consumer-cadence marketing will
  disengage, and the loss is an account rather than a subscriber.
- **BB6.** Operational usefulness outranks promotion. Lead-time changes, stock availability and product
  updates are the messages this audience actually wants.

## Lifecycle Notes

| Stage | Vertical emphasis |
|---|---|
| Prospect | Long nurture; the objective is qualification and education, not immediate conversion |
| New account | Onboarding is operational — ordering process, terms, account contacts, support routes |
| First order placed | The second order proves the relationship; treat it as an account milestone |
| Established account | Reorder reliability and category expansion |
| High-value account | Human account management, not automated recognition. Automation supports it; it does not replace it |
| At-risk account | Detected on the account's own ordering rhythm; usually warrants a human intervention, not a campaign |
| Lapsed account | Individually high value — worth substantially more effort per account than consumer win-back |

## Channel Notes

- Email is the primary and often only appropriate channel. It suits the length, the documentation and the
  multi-person buying unit.
- SMS is rarely appropriate for promotion here. Where it is used at all, it is operational — order status,
  delivery, urgent stock or service notification — and only with explicit consent.
- Business-hours sending matters more than consumer send-time optimisation.

## Known Limits

- **Self-serve B2B with short cycles** — small-business SaaS, low-value trade supplies — behaves closer to
  consumer e-commerce. Use [../ecommerce/PLAYBOOK.md](../ecommerce/PLAYBOOK.md).
- **Platforms with no account-level modelling** cannot apply most of this playbook; contact-level
  approximations will misread the base, and the correct response is to say so.
- **Mixed B2B and B2C stores** need the two bases separated before either overlay is applied; applying
  this playbook to the consumer half will suppress legitimate activity.
- **Marketplace and distributor relationships** may mean the end customer is not reachable at all.

## Recipe Priority

A prior for [automation-recipe-selector](../../skills/automation-recipe-selector/SKILL.md), which
re-ranks it on store evidence. Each entry names the signal to check before believing it.

1. **Consent verification and inbound lead capture** — the pair that makes everything else lawful and
   useful here. *Check:* that a contact-form submission is not being treated as marketing consent;
   conflating the two is the most common failure in this vertical.
2. **Integration recipes** — CRM sync, and the event-stream recipe it depends on. *Check:* that a
   conflict rule between the CRM and the platform has been decided before the sync is built, and that
   consent state is excluded from the synced fields.
3. **Long-cycle nurture** — the click-branched pattern, at a cadence matched to the buying cycle
   rather than to a weekly calendar. *Check:* that the cycle length is derived from closed deals.
4. **Measurement** — the periodic summary, reported against pipeline rather than order revenue.
5. **List health** — as the baseline. **AI-assisted** — last, and note that generated copy reaching a
   named account carries more exposure here than a consumer send.

Usually wrong here: cart recovery, VIP tiers and most consumer lifecycle recipes. There is rarely a
cart, the relationship is with an account rather than a person, and recognition schemes do not map to
a buying committee.
