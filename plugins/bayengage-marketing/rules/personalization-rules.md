# Personalisation Rules

What may be used to personalise a message, and what may not. Cited as `personalization-rules.md#P1`.

---

### P1. Never personalise using data BayEngage cannot verify for that contact.
This is the rule the others elaborate. If the platform cannot confirm the value for this specific person,
it does not go in the message. Inferred, assumed, averaged or guessed attributes are not personalisation;
they are a visible error waiting for the one recipient it is wrong about.

### P2. Every personalised element needs a fallback.
If the value can be missing for any contact in the audience, the message must still read correctly
without it. "Hi ," is worse than "Hi."

### P3. Personalisation must earn its place.
Inserting a first name into a subject line is not a strategy. Personalisation is worth using when it
changes what the customer sees — the product, the offer, the timing, the reason for the message — not
when it only changes the salutation.

### P4. Personalise on the strongest verified signal available.
Roughly in order of usefulness:

1. What they bought, and when
2. What they repeatedly buy (replenishment interval, category affinity)
3. Their value band (AOV, LTV) where it changes the offer
4. Lifecycle stage
5. Engagement recency and channel preference
6. Price band affinity
7. Location, where it genuinely changes relevance (delivery, store, season, timezone)
8. First name

### P5. Recommended products must come from platform data.
Product recommendations are drawn from `bayengage.product_intelligence` and the contact's own history.
Never assemble a recommendation from assumption or from what "similar stores" sell.

### P6. Do not reference behaviour the customer would find surprising.
There is a difference between useful and unsettling. Referencing a purchase is fine. Narrating browsing
behaviour in detail is not, even when the data exists.

### P7. Do not personalise on sensitive or inferred-sensitive attributes.
Health, financial status, inferred gender, inferred life events, inferred pregnancy or bereavement. Even
when a correlation exists in the data, the failure mode is severe and the upside is small.

### P8. Timing is personalisation.
Sending at the individual's observed engagement time, or at their replenishment interval, is usually
worth more than any token in the copy.

### P9. Stale data must not be presented as current.
Inventory, price and product availability change. If the message asserts a current state, the plan must
say how that state is confirmed at send time.

### P10. Personalisation depth follows data depth.
A store with thin behavioural data gets simpler messages, not fabricated specificity. Say so rather than
degrading silently.

### P11. Never leak one customer's data into another's message.
Recommendations, counts and references are per-recipient. This is a correctness rule, not a style rule.

### P12. Test the empty case.
Before a personalised campaign is approved, state what a contact with none of the referenced data will
receive.

See also [../knowledge/personalization-principles.md](../knowledge/personalization-principles.md) for the
reasoning behind these rules.
