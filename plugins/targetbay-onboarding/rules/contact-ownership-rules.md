# Contact Ownership Rules

Cited as `contact-ownership-rules.md#X2`.

TargetBay Email & SMS, TargetBay Reviews and TargetBay Loyalty can each decide, correctly and
independently, to contact the same customer on the same day. Each product respects its own frequency
cap, and the customer receives the sum of all three. No single product can see the problem, and no single
product can fix it.

Onboarding is where it gets fixed, because onboarding is the only moment when all four programmes are
designed at once and nothing is live yet.

---

### X1. One contact budget per customer per period, owned by the platform, not by a product.
The budget is a single number covering email, SMS, review requests and programme messages. Four products
each honouring their own cap is four products jointly exceeding the real one. Where the platform can
enforce a unified cap, plan within it and never restate it
([global-rules.md#G10](global-rules.md)).

### X2. Moments have owners, and the owner is the moment's, not the product's.

| Moment | Owner | Rationale |
|---|---|---|
| Post-purchase and delivery | Reviews | The ask belongs to the experience that just happened |
| Lifecycle and promotional | Email & SMS | The programme that owns the customer relationship over time |
| Programme state — points, tiers, rewards, referrals | Loyalty | Only Loyalty knows the member's balance and standing |
| Onsite | Personalization | Acts on a visitor already present; see [#X3](#x3-onsite-personalization-never-consumes-contact-budget) |

A product that does not own a moment does not message into it. Email & SMS does not send the first review
request; Reviews does not send the win-back.

### X3. Onsite personalization never consumes contact budget.
It acts on a visitor who is already on the site and has already chosen to be there. This is a structural
difference, not a courtesy, and it is why onsite work sequences first
([sequencing-rules.md#SQ2](sequencing-rules.md)).

### X4. When two products want the same customer in the same window, the later ask yields.
It does not compress into a shorter message, does not switch channel to dodge the cap, and does not run
the following day. It moves behind the next moment its product owns, or it does not run. Channel-hopping
to evade a cap is a violation of [safety-rules.md#S13](safety-rules.md), not a workaround.

### X5. Loyalty programme messages dispatch through Email & SMS unless the manifest says otherwise.
`loyalty.messaging` is declared in the TargetBay Loyalty registry but no implementation has been
inspected. Until the capability manifest confirms it for a given store, plan programme messaging as
Email & SMS sends owned by Loyalty's moment, so they are counted once against the one budget.

### X6. Review-request frequency reconciles against the whole budget, never a Reviews-only cap.
A review request is a message to a customer. Whether it is dispatched by Reviews or by Email & SMS, it
counts against [#X1](#x1-one-contact-budget-per-customer-per-period-owned-by-the-platform-not-by-a-product).
A Reviews-only cap that looks healthy while the customer receives six messages a week is the exact failure
this file exists to prevent.

### X7. A blueprint that cannot state the maximum weekly contact per customer is not approvable.
The number is computed across all four products, shown in the approval request, and approved on its face
([safety-rules.md#S4](safety-rules.md)). "Each product is within its own limits" is not that number.

### X8. The budget is re-checked at verify, and a change re-enters approval.
What was created is not always what was planned. If the provisioned resource set produces a different
maximum weekly contact than the approved blueprint stated, provisioning stops and the difference is
approved before anything activates.

### X9. Where the platform cannot enforce one budget, say so on the blueprint's face.
If no unified frequency and consent view exists across the four products, the budget is stated as
`provisional` with the observation that would replace it, and the blueprint says plainly that the number
is planned rather than enforced. Claiming an enforcement that does not exist is the
[safety-rules.md#S12](safety-rules.md) failure in its most damaging form.
