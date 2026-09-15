# Transactional Email Catalog

Which messages this store actually needs, and what goes in each.

Use this when planning from scratch, or when auditing a store that grew its email set by accident.
The classification column matters: it decides consent, unsubscribe and sending domain — see
[Email Types](./email-types.md).

## Message sets by store type

Start from the set that matches the business, then add. A store that ships nothing physical does not
need a dispatch notification; a subscription box needs half a dozen messages a one-off store does
not.

### Single-product DTC

The smallest viable set. Everything else is a distraction until volume justifies it.

- Email verification (if accounts exist)
- Order confirmation
- Dispatch notification with tracking
- Delivered notification
- Review request
- Payment failed (if there is any stored-card flow)

### Multi-category retail

Adds the complexity of partial fulfilment and returns.

- Account: verification, password reset, security alert
- Order: confirmation, partial shipment, dispatch, out for delivery, delivered, delay
- Returns: return authorised, return received, refund issued
- Review request, keyed to the delivered event
- Back-in-stock alert (only for customers who requested it for that product)

### Subscription box / replenishable goods

The renewal cycle is the product, so the messages around it are load-bearing.

- Everything in the DTC set
- Upcoming renewal notice, sent before the charge, with the contents and the skip link
- Card expiring soon
- Payment failed, with a dunning ladder
- Skip / pause / resume confirmations
- Plan or frequency change confirmation
- Cancellation confirmation, with what happens to anything already paid for

### Marketplace / multi-vendor

Two audiences, so two message sets.

- Buyer: order confirmation, per-seller dispatch, dispute opened/resolved
- Seller: new order, payout initiated, payout completed, listing removed, policy notice
- Both: account verification, security alerts, message-received notification

### High-consideration / high-AOV

Where the order is large enough that silence causes anxiety.

- Everything in the retail set, plus:
- Order received but pending verification
- Proactive delay notice — before the customer asks
- Delivery appointment scheduling
- Post-delivery check-in, separate from the review request
- Warranty or registration confirmation

## The catalog

### Authentication and security

#### Email verification

**Transactional.** Sent immediately on signup.

- The code or link, prominent and above the fold
- Expiry stated in the message
- What happens if they ignore it
- A way to request a new one, with a cooldown
- No marketing content at all — this message often precedes marketing consent

#### OTP / 2FA code

**Transactional.** The most time-critical message you send.

- Code in the subject line and in the body
- Large, monospace, generously spaced, never inside an image
- Expiry in minutes
- "If you did not request this, someone has your password" — with the change-password link
- Never wrapped in click tracking

#### Password reset

**Transactional.**

- One button, one plain URL beneath it
- Single-use token, short expiry, consumed on form submit rather than page load
- "If you did not request this, you can ignore this message — your password has not changed"
- Do not reveal whether the address has an account; send the same response either way, and use the
  body to say "if you have an account with us"

#### Security alert

**Transactional.** New device, new location, password changed, email changed, payout details changed.

- What changed, when, and from roughly where
- A one-click "this was not me" that actually locks the account
- Send to the **old** address as well when the address itself changes — otherwise the notification
  goes only to the attacker

### Account

#### Welcome

**Marketing** in most cases, because its purpose is onboarding and promotion rather than completing
a transaction. If it also carries the signup incentive, treat it as marketing and require consent.

- Deliver what the signup promised — the discount code, the guide, the early access
- One next step, not five
- Set expectations: what you send and how often
- See [Ecommerce Flows](./ecommerce-flows.md) for the sequence this starts

#### Account change confirmation

**Transactional.** Address changed, preferences saved, card added, subscription modified.

- State the old and new value where it is safe to do so
- Link to undo, or to contact support
- Timestamp

### Order and fulfilment

#### Order confirmation

**Transactional.** The single highest-engagement message in ecommerce.

- Order number in the subject line
- Itemised contents with images, quantities, prices
- Totals broken out: subtotal, shipping, tax, discount, total paid
- Payment method, last four digits only
- Shipping address, so a mistake is caught while it can still be fixed
- Expected dispatch or delivery window
- How to change or cancel, and until when
- Support contact
- A cross-sell block is permitted below all of the above — see the hybrid rules in
  [Email Types](./email-types.md)

#### Partial shipment

**Transactional.** Easy to forget and a common source of "where is the rest of my order" tickets.

- Which items are in this shipment and which are not
- Tracking for this shipment
- Expected timing for the remainder
- Confirmation that they were not charged twice

#### Dispatch notification

**Transactional.**

- Carrier, tracking number, and a working tracking link
- Estimated delivery date, not just "on its way"
- What shipped, if the order was split
- Delivery address again

#### Out for delivery / delivered

**Transactional.** Often better as SMS than email — see [Ecommerce Flows](./ecommerce-flows.md).

- Delivered messages should say where it was left
- The delivered event is the correct trigger for the review request clock, not the order date

#### Delay notice

**Transactional.** Send it before the customer notices.

- What is delayed and why, in one sentence
- The new expected date
- What they can do: wait, cancel, swap
- A proactive delay notice prevents a support ticket; a reactive one follows a complaint

#### Return authorised / received / refund issued

**Transactional.** Three separate messages, because the silence between them is where anxiety lives.

- Return authorised: label, instructions, deadline
- Return received: what was received and what happens next, with a timeframe
- Refund issued: amount, method, and how long the bank will take — state the bank's timeframe
  explicitly or you will be asked about it

### Subscriptions and billing

#### Upcoming renewal notice

**Transactional.** Required by law in some jurisdictions for auto-renewing subscriptions.

- Charge date and exact amount
- What is in the upcoming order
- Links to skip, change or cancel, working without a login wall
- Sent far enough ahead to act on — a notice the same morning as the charge is not a notice

#### Card expiring

**Transactional.** Sent before the failure, which is the entire point.

- Which card, last four digits
- Which date it stops working
- One link to update it

#### Payment failed

**Transactional.** The dunning ladder, not a single message.

- Attempt 1: neutral tone, "the card was declined", update link
- Attempt 2: state the retry schedule and what happens at the end of it
- Final: what is being paused or cancelled, and how to restore it
- Each message carries the amount, the card, and one action
- Space the attempts to match your retry schedule, and stop when the payment succeeds

#### Skip, pause, resume, cancel confirmation

**Transactional.**

- What state the subscription is in now
- The next event and its date — "your next box ships 14 May"
- How to reverse it

### Requested alerts

#### Back-in-stock

**Transactional-adjacent** only when the customer explicitly asked for this product. Keep the
request record; it is the evidence.

- Which product and variant
- A direct link to the product, not the category
- Honest urgency only — do not claim scarcity you cannot substantiate
- Expire the request after a reasonable window rather than holding it forever

#### Price drop

**Marketing.** Even when requested, its purpose is promotional. Require marketing consent and
include an unsubscribe.

## Per-message checklist

Before shipping any message in this catalog:

- [ ] Classified transactional or marketing, and sent from the matching subdomain
- [ ] Unsubscribe present if marketing, absent if transactional
- [ ] Subject line states the fact, and carries the order number or code where relevant
- [ ] Preheader written, not defaulted
- [ ] Readable with images off
- [ ] One primary action
- [ ] Support route present
- [ ] Renders in dark mode
- [ ] Suppression scope correct — marketing suppression must not block a receipt

## Related

- [Transactional Emails](./transactional-emails.md) — how to write them
- [Email Types](./email-types.md) — the classification rules
- [Ecommerce Flows](./ecommerce-flows.md) — the marketing sequences around these
- [Accessibility](./accessibility.md) — making them readable
