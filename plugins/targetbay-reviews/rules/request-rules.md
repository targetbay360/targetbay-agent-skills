# Request Rules

Constraints on asking a customer for a review. Cited as `request-rules.md#R3`.

---

### R1. Anchor the delay to possession, not to purchase.
The clock starts when the customer has the product. Use fulfilment or delivery timing from
`reviews.order_intelligence`. Where that is unavailable, say the delay is anchored to order date, mark the
confidence lower, and record the gap in `unmet_requirements`.

### R2. Derive the delay from the product, not from a default.
How long it takes to form an opinion differs by what was bought — a consumable that is used immediately,
an appliance that is judged after a month, a garment judged on first wear. Derive the window from
category, price band and repeat interval where the data exists. Never assert a fixed number of days as a
universal.

### R3. One order, one ask.
A customer who bought five items receives one request, covering the order. Sending five requests against
one order is the most common cause of review-request opt-out, and it produces fewer reviews, not more.

### R4. A follow-up is a reminder, not a second campaign.
At most one reminder to a non-responder, and it does not restate the whole ask. A second reminder needs
evidence from `reviews.request_analytics` that the first reminder converted, not an assumption that more
asking produces more reviews.

### R5. Do not ask a customer whose experience is known to be bad.
If a return, refund, cancellation or open support issue is visible on the order, the request is suppressed
and the problem is routed to a human. Asking for a review in the middle of an unresolved complaint is how
a private problem becomes a public one.

### R6. Prioritise the ask by coverage gap, not by order volume.
The next request is worth most on a product with no reviews and real traffic. Rank by what
`reviews.product_coverage` says is missing, not by whatever sold most this week.

### R7. Ask on the channel the customer actually uses.
Channel selection follows consent and engagement from `reviews.suppression_and_consent`, not store
preference. Where only one channel has consent, that is the channel; where none does, there is no request.

### R8. Requesting media is a separate, later ask.
Asking for a photo or video at the same time as the review lowers submission of both. Request media from
customers who have already reviewed, and only where `reviews.ugc_media` shows the product is short of it.

### R9. Never vary the ask by expected sentiment.
Do not route likely-satisfied customers to a public review and likely-dissatisfied customers to a private
form. That is review gating, and it is prohibited by [safety-rules.md#S3](safety-rules.md).
