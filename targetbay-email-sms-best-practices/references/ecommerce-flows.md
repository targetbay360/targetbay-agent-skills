# Ecommerce Lifecycle Flows

Automated sequences triggered by customer behaviour. They reach people in a live buying moment
rather than on your calendar, which is why they outperform campaigns per recipient and generate
fewer complaints.

Each flow below is specified as **trigger → timing → exit → channel → job**. The timings are
starting points to test against the store's own data, not settings to copy.

## The rules that apply to every flow

**Exit conditions are not optional.** The most common lifecycle bug is a flow that keeps sending
after its purpose is served — a cart reminder arriving after the order confirmation. Every flow needs
an explicit exit, checked at each step and not only at entry.

**Flows collide.** A customer can qualify for cart abandonment, browse abandonment, replenishment
and a campaign in the same 48 hours. Set a global frequency cap across flows and campaigns together,
and give transactional and dunning sequences priority over promotional ones.

**Channel split.** Email carries the explanation; SMS carries the deadline. The same content on both
channels at the same time doubles the cost, doubles the fatigue and adds nothing. Use SMS where
timing genuinely matters and the message fits one segment — see
[SMS Deliverability](./sms-deliverability.md).

**Consent is per channel and per flow type.** Almost everything here is marketing, including review
requests and replenishment reminders. See [Email Types](./email-types.md).

**Benchmarks are for sanity-checking, not targets.** Published industry figures — for example that
cart abandonment sits around 70%, or that the first message in a recovery series carries most of the
recovered revenue — are useful to tell "this is broken" from "this is normal". They are not this
store's numbers, and a flow that beats them may still be underperforming its own potential.

---

## Welcome

**Trigger:** subscription confirmed (after double opt-in, not before).
**Timing:** first message immediately; two or three more over the following days.
**Exit:** purchase — move to post-purchase rather than continuing to court them.
**Channel:** email; SMS only if they opted in to SMS separately.

**Job:** deliver what the signup promised, then establish who you are.

- Message 1 carries the incentive, immediately. If the popup said "10% off", the code is in the first
  message and nothing precedes it. Making someone wait for a promised discount is the fastest way to
  lose a new subscriber.
- Message 2 is the brand: what you sell, what makes it different, who it is for.
- Message 3 is proof — reviews, UGC, bestsellers.
- Set expectations early: what you send and how often.
- Expire the incentive, and say when. An unexpiring code has no reason to be used today.

## Abandoned cart

**Trigger:** items added, checkout not completed. Requires an identified visitor.
**Timing:** first message within the hour; then a second and a third at widening gaps over the
following days.
**Exit:** purchase, or cart cleared.
**Channel:** email; SMS for high-value carts where the cost is justified.

**Job:** remove whatever stopped them.

- The first message carries the bulk of the recovered revenue. Sending it hours later rather than
  within the hour materially reduces recovery.
- Show the actual cart contents with images, not a generic "you left something behind".
- One button straight back to a restored cart. Not to the homepage, not to the category.
- Do not lead with a discount. The first message assumes they got distracted. Discount later, if at
  all — a discount in message one teaches customers to abandon deliberately.
- Address the real objections: shipping cost, returns policy, stock availability, payment options.
- Check the cart is still purchasable before sending. A reminder for a sold-out item is worse than
  no reminder.

## Browse abandonment

**Trigger:** product page viewed repeatedly or at depth, no add-to-cart.
**Timing:** hours, not minutes.
**Exit:** added to cart (hand off to cart abandonment), or purchase.
**Channel:** email.

**Job:** help, without being unsettling.

- Lower intent than a cart, so a lighter touch and fewer messages.
- **Do not narrate the surveillance.** "We saw you looking at X for four minutes" is accurate and
  alienating. "Still thinking about X?" carries the same information and does not.
- Frame it as helpful: related products, the size guide, what reviewers say.
- Exclude anyone already in a cart or post-purchase flow.
- Requires consent for tracking in consent-regulated markets, and that consent is separate from
  email consent.

## Post-purchase

**Trigger:** order placed, then each fulfilment event.
**Timing:** driven by the fulfilment events themselves.
**Exit:** none — it runs to completion.
**Channel:** email for detail, SMS for the delivery moments.

**Job:** eliminate the silence between paying and receiving.

Sequence: order confirmation → dispatch with tracking → out for delivery → delivered → check-in →
review request.

- The transactional messages here are specified in the
  [Transactional Email Catalog](./transactional-email-catalog.md).
- Delivery-stage messages are the best case for SMS: short, time-critical, genuinely wanted.
- A check-in before the review request ("how is it going?") catches problems while they are fixable
  and keeps them out of a public review.
- Cross-sell belongs after delivery, not in the confirmation, unless it is clearly secondary.

## Review request

**Trigger:** the **delivered** event, plus a product-appropriate usage window.
**Timing:** delivered date + long enough to have formed an opinion. That window is product-specific:
a consumable gets days, a mattress or a skincare regimen gets weeks.
**Exit:** review submitted.
**Channel:** email; SMS works where the review form is genuinely one tap.

**Job:** get an honest review from someone who has actually used the product.

- **Trigger on delivery, never on order date.** An order-date trigger asks for a review of something
  still in transit — the most common review-programme mistake, and it produces both bad data and
  annoyed customers.
- One reminder at most, then stop.
- Ask for the review directly. Do not bundle it with a promotion.
- If there is an incentive, offer it for any review, not for a positive one. Conditioning a reward on
  a good rating is both a platform violation and a legal problem in several jurisdictions.
- Route low ratings to support before publication where the platform allows it.
- Ask for photos and video explicitly — visual reviews have to be requested to be received.
- This is a **marketing** message: marketing consent, unsubscribe link, marketing suppression.

## Replenishment

**Trigger:** elapsed time since purchase of a consumable.
**Timing:** derived from that product's observed repeat interval, per product, shortened slightly so
the reminder arrives before they run out.
**Exit:** repurchase of that product.
**Channel:** email; SMS for genuinely time-critical items.

**Job:** arrive just before they need it.

- Derive the interval from the store's own repeat-purchase data for that product. A single
  store-wide number is wrong for almost every product in the catalogue.
- Where there is no repeat data yet, use the pack size and a stated usage rate, and say that it is an
  estimate.
- Make reordering one click, pre-filled with the previous quantity and variant.
- Suppress if they bought it elsewhere in your catalogue, changed variant, or returned it.

## Win-back

**Trigger:** no purchase for materially longer than this customer's normal gap.
**Timing:** the threshold is per-customer, derived from their own purchase interval — a monthly buyer
is lapsed at three months; an annual buyer is not.
**Exit:** purchase, or entry into the sunset flow.
**Channel:** email; SMS as the last attempt where they have SMS consent and past value justifies it.

**Job:** find out whether there is still a relationship.

- Lead with what changed — new products, a restock, an improvement — rather than "we miss you".
- Escalate the offer across the sequence, and cap it. Not everyone is worth recovering at any price.
- Bound the attempts. A win-back that runs indefinitely is a complaint generator.
- Segment by past value: a repeat high-AOV customer justifies a different offer from a
  one-purchase discount buyer.

## Sunset

**Trigger:** no engagement across a long window, and win-back exhausted.
**Timing:** after win-back completes.
**Exit:** any engagement — open, click, purchase, preference update.
**Channel:** email.

**Job:** end the relationship deliberately instead of mailing a dead address forever.

- One or two messages: "we are about to stop emailing you — stay on the list?"
- A single obvious button to stay.
- No response means suppression from marketing, not deletion. Keep the contact and the consent
  record; stop the sending.
- This flow protects deliverability for everyone else on the list, which is why it earns its place
  despite ending in fewer contacts. Removing the unengaged portion typically raises total revenue,
  because the remaining sends land.

## VIP and loyalty

**Trigger:** crossing a value, frequency or points threshold derived from the store's own
distribution.
**Timing:** on the event.
**Exit:** none — it is an ongoing state.
**Channel:** email, plus SMS for genuinely exclusive time-boxed access.

**Job:** make the status feel like status.

- Early access and genuine exclusivity beat a larger discount.
- Points-expiring notices are marketing, even though the balance is a fact.
- Recognise the milestone itself; the reward is secondary to being noticed.

---

## Flow priority when several qualify

When a contact is eligible for more than one send in the same window, order by how close the moment
is to a decision:

1. Transactional and dunning — always, regardless of caps
2. Cart abandonment — live intent
3. Post-purchase and delivery updates
4. Browse abandonment
5. Replenishment
6. Review request
7. Campaigns
8. Win-back and sunset

Anything below the frequency cap waits for the next window rather than being dropped silently — and
if it waits past its own relevance, it should be dropped rather than sent late.

## Measuring flows

Per flow, and per message inside it:

- Revenue per recipient — the comparable metric across flows of different sizes
- Conversion rate
- Unsubscribe and complaint rate — the cost side
- Where in the sequence conversions happen, which tells you whether the later messages earn their
  place

Do not branch flows on open events. Apple Mail Privacy Protection makes "opened" unreliable — see
[Deliverability](./deliverability.md). Branch on clicks, purchases and cart state instead.

## Related

- [Marketing Emails](./marketing-emails.md) — the campaign side
- [Email Types](./email-types.md) — which of these need consent and an unsubscribe
- [SMS Compliance](./sms-compliance.md) — quiet hours apply to every SMS step above
- [List Management](./list-management.md) — where sunset ends
- [Transactional Email Catalog](./transactional-email-catalog.md) — the transactional messages these wrap around
