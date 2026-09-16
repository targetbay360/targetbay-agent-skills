# Email Types: Transactional vs Marketing

## Why the distinction matters

It decides three things: whether you need marketing consent, whether the message needs an
unsubscribe link, and which sending domain it goes out on. Getting it wrong means either mailing
people who did not consent, or suppressing a password reset because someone unsubscribed from a
newsletter.

The test is not how operational the message feels. It is **what triggered it and what it is for**.

## Transactional

Triggered by an individual's own action, expected by them, and containing information they need to
complete or understand a transaction they initiated.

- Sent one-to-one, in response to an event
- Primary purpose is informational, not promotional
- Goes to anyone who takes the action, regardless of marketing consent
- Does not require an unsubscribe link — and generally should not have one, because unsubscribing
  from receipts is not something you want to offer
- Sent from the transactional subdomain

Examples: email verification, OTP and 2FA codes, password reset, security alerts, order
confirmation, shipping and delivery notifications, invoices and receipts, payment failure notices,
subscription renewal notices, account change confirmations.

## Marketing

Sent to promote, at a time you choose, to an audience you selected.

- Sent to a segment on your schedule
- Primary purpose is commercial
- Requires marketing consent on that channel under opt-in regimes, and requires opt-out handling
  everywhere
- Requires a visible unsubscribe plus the `List-Unsubscribe` headers
- Requires a physical postal address under CAN-SPAM
- Sent from the marketing subdomain

Examples: newsletters, promotions and sales, product launches, abandoned cart recovery, browse
abandonment, review requests, replenishment reminders, win-back, back-in-stock alerts, price-drop
alerts.

## The ecommerce calls people get wrong

These feel operational and are legally marketing in most jurisdictions:

| Message | Classification | Why |
|---|---|---|
| Abandoned cart recovery | Marketing | The store chose to send it; the customer did not request it, and the purpose is to sell |
| Browse abandonment | Marketing | Triggered by behaviour the visitor did not submit |
| Review request | Marketing | Solicits an action for the store's benefit after the transaction has completed |
| Replenishment reminder | Marketing | A predicted need, not a transaction in progress |
| Back-in-stock alert | Usually transactional-adjacent | If the customer explicitly requested this alert for this product, it is the fulfilment of their request — keep the request record |
| Win-back | Marketing | Unambiguously promotional |
| Loyalty points expiring | Marketing, usually | Promotional intent, even though the balance is factual |
| Order confirmation with a cross-sell block | Hybrid — see below | |

Consequence: a review request needs marketing consent and an unsubscribe link, and must respect
marketing suppression. Building it on the transactional path because "it's part of the order" is the
common mistake, and it is the one that produces complaints from people who never opted in.

## Hybrid messages

An order confirmation with a "you might also like" block is the classic case. Rules that keep it
safe:

- The transactional content must be the **primary purpose** — top of the message, majority of the
  content, what the subject line describes
- The promotional block sits below the transactional content, clearly secondary
- The subject line describes the transaction, never the promotion
- If the promotional content grows past incidental, the whole message is reclassified as marketing
  and needs consent and an unsubscribe

When in doubt, split the message. Two messages that are each clearly one type are easier to defend
and easier to measure than one that is arguably both.

## Legal distinctions in brief

**CAN-SPAM** turns on "primary purpose". A message whose primary purpose is transactional is exempt
from most requirements, but the header and sender information must still be accurate.

**GDPR** cares about lawful basis. Transactional mail is generally contract performance; marketing
generally requires consent. Consent for one does not extend to the other.

**CASL** exempts some transactional messages from the consent requirement but still requires sender
identification.

Detail in [Compliance](./compliance.md) and [SMS Compliance](./sms-compliance.md).

## Sending infrastructure

Separate subdomains, always:

```
t.example.com   transactional — receipts, resets, order and shipping updates
m.example.com   marketing     — campaigns, flows, promotions
```

Each gets its own SPF, DKIM and DMARC. The reason is blast radius: promotional mail attracts
complaints, complaints damage domain reputation, and a password reset that lands in spam is a
support incident and a security problem. Keeping them separate means the marketing calendar cannot
break authentication-critical mail.

The same logic applies to SMS numbers — see [SMS Deliverability](./sms-deliverability.md).

## Suppression behaves differently

| | Transactional | Marketing |
|---|---|---|
| Unsubscribe | Not offered | Required |
| Marketing suppression applies | No | Yes |
| Hard bounce suppression applies | Yes | Yes |
| Complaint suppression applies | Yes — investigate, it means the message was unwanted | Yes |
| Global opt-out applies | No | Yes |

Keeping two suppression scopes — "do not market to" and "do not send anything to" — is what lets an
unsubscribed customer still receive the receipt for the order they just placed.

## Related

- [Transactional Emails](./transactional-emails.md) — building them
- [Transactional Email Catalog](./transactional-email-catalog.md) — which ones this store needs
- [Marketing Emails](./marketing-emails.md) — building those
- [Compliance](./compliance.md) — the requirements each type carries
