# Audience Rules

Targeting decisions. Cited as `audience-rules.md#A1`.

---

### A1. Confirm the audience exists before planning around it.
Resolve every audience against `email_sms.segmentation` and record its size. An audience that cannot be
resolved is a requirement, not an assumption. See [global-rules.md#G4](global-rules.md).

### A2. Size the audience before recommending a split.
Splitting is a cost: more content, more QA, more measurement noise. If a resulting group is too small to
produce a readable result, do not split it — treat the reason for the split as a personalisation problem
instead.

### A3. A split must change the treatment.
If two groups would receive the same message, same offer, same timing and same channel, they are one
audience. See [global-rules.md#G8](global-rules.md).

### A4. Exclusions are part of the audience definition.
State who is deliberately excluded and why — recent purchasers of the promoted product, contacts already
in a competing automation, contacts who just received a message, suppressed contacts, non-consented
contacts on that channel. An audience defined only by inclusion is under-specified.

### A5. Prefer behaviour over attributes.
Recent behaviour predicts response better than static attributes. Reach for purchase recency, browse and
purchase history, engagement recency and product affinity before demographics or location.

### A6. Recency decays. Say how far back you looked.
Every behavioural audience carries a lookback window, and the window is a decision. A 24-month "engaged"
window and a 90-day one describe different people.

### A7. Do not stack conditions until the audience disappears.
Each additional condition reduces reach. Add conditions only while each one improves expected outcome
more than the reach it costs, and check the resulting size after each.

### A8. Overlapping audiences must be prioritised, not ignored.
When a contact qualifies for several audiences in the same period, decide which takes precedence and say
so. Unresolved overlap means someone gets three messages in a day.

### A9. Do not target on unverified inference.
Propensity and affinity scores are usable when the platform produces them. Guessed attributes —
inferred gender, inferred income, inferred intent with no supporting signal — are not.

### A10. Respect consent per channel.
Email consent is not SMS consent. Build and check audiences per channel, and never plan an SMS audience
without confirming SMS consent through `email_sms.suppression_and_consent`.

### A11. Rank audiences when there is more than one.
When a skill returns multiple audiences, order them by expected value and say what drives the order.
An unordered list of six audiences defers the decision back to the user.

### A12. Very small audiences need a different instrument.
Below the point where a campaign is worth building, prefer adding the group to an existing automation, or
a one-to-one action, over a dedicated send.
