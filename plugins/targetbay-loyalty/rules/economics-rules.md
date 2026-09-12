# Economics Rules

Constraints on points value, issuance, redemption and liability. Cited as `economics-rules.md#E3`.

---

### E1. State the point's monetary value explicitly.
Every economics recommendation names what one point is worth on redemption, derived from the reward
catalogue rather than asserted. A programme whose point value nobody can state is a programme nobody can
price.

### E2. Earn rate is a margin decision, not a marketing one.
The cost of issuance is the point value multiplied by expected redemption, carried against gross margin.
Read margin posture from `loyalty.store_profile` and redemption behaviour from `loyalty.redemption`
before proposing a rate. Where margin data is unavailable, say the rate cannot be responsibly set and
report the gap.

### E3. Never recommend an earn rate without its liability projection.
Issuance changes the balance sheet. State the projected outstanding liability under the proposed rate,
against the current one, over a stated horizon ([safety-rules.md#S3](safety-rules.md)).

### E4. Redemption rate is the health metric, not issuance.
A low redemption rate means members are accumulating something they never use — an ageing liability and a
promise quietly not kept. Read it from `loyalty.redemption` and treat a falling rate as a finding, not a
saving.

### E5. Breakage is not a business model.
Planning around points that will never be redeemed is planning for members to be disappointed, and in
several jurisdictions it is also a regulatory exposure. Expiry may exist as a liability control; it may
not be the mechanism by which the programme's economics work.

### E6. A reward must be reachable in a plausible time.
Derive the time to the cheapest meaningful reward from this store's actual AOV and purchase frequency. A
reward that takes a typical customer years to reach produces no behaviour change and considerable
resentment (G8).

### E7. Check redemption capacity before listing a reward.
Cost, stock and fulfilment capacity are checked against expected demand before a reward is proposed
([safety-rules.md#S11](safety-rules.md)). A reward the store cannot honour is worse than no reward.

### E8. Expiry is a policy change, not a cleanup.
Expiring points removes something members hold. It is `destructive`, requires inspection of how many
members and how much value are affected, requires notice, and requires explicit approval
([safety-rules.md#S8](safety-rules.md)).

### E9. Never compare members to non-members without naming the selection problem.
Members were already better customers before they joined (G5). Where a like-for-like comparison is
possible — pre-enrolment behaviour, matched cohorts, enrolment-date discontinuity — use it and say which.
Where it is not, report the raw difference as raw and state that the programme effect is not isolated.

### E10. Price rewards against margin, not against points.
The constraint is what the reward costs the store, not what it costs the member. Two rewards at the same
point price with different margin impact are not interchangeable.
