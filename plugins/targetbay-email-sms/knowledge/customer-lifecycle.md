# Customer Lifecycle

The lifecycle is the single most reusable lens in this package. Most audience, automation and planning
decisions reduce to: *which stage is this contact in, and what does that stage need?*

Stage boundaries are store-specific. A coffee subscription's "dormant" is 60 days; a mattress retailer's
is three years. Never hard-code thresholds — derive them from the store's observed repeat interval via
`email_sms.order_intelligence`.

## Stages

### Prospect
Has consented, has not purchased. Has interest but no proof of it.
**Needs:** a reason to trust and a reason to start. Welcome content, social proof, bestsellers, a
low-friction first purchase. **Risk:** discounting the first purchase teaches discount dependence from day one.

### New customer
Has purchased once, very recently, and the order may not have arrived yet.
**Needs:** reassurance, delivery clarity, usage or care information, onboarding to the product.
**Risk:** selling again before the first order lands reads as indifference.

### First-time buyer
Has purchased once; the order has landed; the window in which a second purchase is most likely is open.
**Needs:** the second purchase. This is the highest-leverage transition in most stores — the gap between
one and two orders is where the largest share of customers is lost.
**Levers:** category expansion, complementary products, replenishment timing, a reason to return.

### Repeat buyer
Two or more purchases; a pattern is forming.
**Needs:** consistency and relevance. Replenishment at the observed interval, cross-sell into adjacent
categories, gradual AOV growth.
**Risk:** over-contacting the reliable segment because it responds.

### VIP / high value
Top of the value distribution by LTV, frequency or AOV — the definition is a store decision.
**Needs:** recognition, access, and priority rather than deeper discounts. These customers are already
buying; margin spent here is usually wasted.
**Risk:** treating VIP as "sends more email." Frequency is not a reward.

### At-risk
Was active, has now gone quiet relative to their own pattern — the strongest signal is a contact
exceeding *their own* typical interval, not a fixed store-wide number.
**Needs:** a timely, relevant, low-pressure reason to return. Intervention here is cheaper and more
effective than win-back later.
**Risk:** treating at-risk as dormant and opening with a heavy discount.

### Dormant
Well past their own interval, no recent engagement, not yet unreachable.
**Needs:** relevance re-established — what changed, what is new, what they previously liked. Escalating
incentive is legitimate here in a way it is not at at-risk.

### Churned
No purchase or engagement for long enough that return is unlikely; approaching or past the point where
continued sending damages deliverability.
**Needs:** a finite, well-constructed win-back attempt, then suppression. Continuing to send to a dead
list costs more than the revenue it recovers. See [email-principles.md](email-principles.md).

## Transitions matter more than states

The valuable moments are the crossings, not the labels:

```
prospect ──▶ new ──▶ first-time ──▶ repeat ──▶ VIP
                          │            │         │
                          ▼            ▼         ▼
                       at-risk ──▶ dormant ──▶ churned ──▶ suppressed
                          ▲            │
                          └────────────┘   (recovered)
```

The transitions worth building automation around:

| Transition | Why it matters |
|---|---|
| prospect → new | Converts consent into revenue |
| new → first-time | The order landed; the relationship starts now |
| first-time → repeat | The single largest retention lever in most stores |
| repeat → VIP | Value concentration; protect it |
| any → at-risk | Cheapest possible intervention point |
| dormant → churned | Last chance before suppression becomes correct |

## Using the lifecycle

- **Audience work** starts here: [../skills/audience-discovery/SKILL.md](../skills/audience-discovery/SKILL.md)
- **Coverage gaps** — which transitions have no automation — are the first thing
  [../skills/automation-strategy/SKILL.md](../skills/automation-strategy/SKILL.md) looks for
- **Stage thresholds are derived, never assumed.** Two stores in the same vertical can have different
  boundaries, and a store's boundaries move over time.
