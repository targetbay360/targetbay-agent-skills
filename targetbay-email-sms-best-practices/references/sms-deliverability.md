# SMS Deliverability

SMS has no spam folder. A message is either delivered or it is silently dropped by a carrier, and
you often find out only from a flat click count.

Unlike email, where compliance and delivery are separate problems, in US SMS they are the same
problem: carriers enforce the rules directly, so a non-compliant programme is an undelivered one.
Read [SMS Compliance](./sms-compliance.md) alongside this.

## A2P 10DLC Registration (United States)

Application-to-Person messaging over standard 10-digit numbers must be registered.

- You register a **brand** (your legal business identity, EIN, address) and then one or more
  **campaigns** (use case, sample messages, opt-in description) through your messaging provider,
  which files them with The Campaign Registry.
- Since **1 February 2025**, US carriers block 100% of unregistered A2P traffic on 10DLC. There is no
  soft filter and no warning period — unregistered messages simply do not arrive.
- Your registered sample messages and opt-in description have to match what you actually send. A
  campaign registered as "order notifications" that carries promotions is a campaign at risk of
  being revoked.
- Registration determines your throughput tier. A brand with a low trust score sends slowly, which
  matters when a flash sale needs to reach the list inside an hour.

**Practical consequence:** budget days-to-weeks for registration before the first planned send. This
is the single most common reason a store's SMS launch slips.

## Number types

| Type | Best for | Notes |
|---|---|---|
| 10DLC (long code) | Most ecommerce programmes | Requires brand + campaign registration; throughput tiered by trust score |
| Toll-free | Cross-border, higher throughput without short-code cost | Requires toll-free verification; unverified toll-free is also filtered |
| Short code | Very high volume, strongest deliverability | Slowest and most expensive to provision |

Do not mix marketing and transactional traffic on one number if you can avoid it — the same
separation logic as transactional and marketing email subdomains.

## What gets messages filtered

Carriers run their own content and behaviour filters on top of registration. Common triggers:

- **Public URL shorteners.** Shared shortener domains are heavily abused and are deprioritised or
  blocked outright. Use a branded short domain on your own hostname. It also raises click-through,
  because a recognisable domain is the only trust signal a text has.
- **No sender identification.** A message that does not say who it is from reads as fraud to both
  the filter and the recipient.
- **Shouting punctuation** — ALL CAPS, `!!!`, `$$$`, "FREE".
- **SHAFT content** — Sex, Hate, Alcohol, Firearms, Tobacco. Age-gated categories need explicit
  carrier approval, and some are prohibited regardless.
- **Volume spikes.** A number that has been sending hundreds a day and suddenly sends tens of
  thousands looks compromised.
- **Identical bodies at high volume.** Some personalisation variance helps; a hundred thousand
  byte-identical messages does not.
- **A rising opt-out rate.** Carriers watch this the way mailbox providers watch complaints.

## Encoding, segments and cost

This is a delivery and budget decision, not a style one.

| Encoding | Single message | Per part when concatenated |
|---|---|---|
| GSM-7 (standard Latin set) | 160 characters | 153 characters |
| UCS-2 (Unicode) | 70 characters | 67 characters |

**One non-GSM character converts the entire message to UCS-2.** That includes a single emoji, and it
includes the curly quotes and en-dashes that word processors insert automatically. A 150-character
message written in a document and pasted in can arrive as three billed segments instead of one,
because of one apostrophe nobody looked at.

Practical rules:
- Compose in a plain-text editor, or run the body through a segment calculator before scheduling.
- Keep the whole message — brand, offer, link, opt-out — inside one segment where you can.
- Emoji are not free. Use one deliberately or none.
- Longer messages are not just more expensive; each additional segment is another chance for partial
  delivery on a poor connection.

A workable shape for one segment: **brand + offer + call to action + branded link + opt-out cue**.

## MMS

MMS carries images, GIFs and much longer text, and typically costs two to three times an SMS
segment. It earns that when the image is the message — a product drop, a lookbook, a cart recovery
showing the actual item. It does not earn it as decoration on a text that would have worked alone.

Check your provider's size and format limits before designing; oversized media is transcoded or
dropped rather than delivered.

## Opt-outs are a deliverability signal

Carriers treat opt-out rate as a health metric. An opt-out is also effectively permanent — the
recipient has to actively text back to rejoin, and almost nobody does. Every unnecessary message
permanently shrinks the channel.

This is why SMS frequency budgets are small and tracked separately from email, and why the
highest-value use of SMS is the moment where timing genuinely matters rather than routine
promotional volume.

## Monitoring

Watch, per campaign and per number:

- Delivery rate, and the carrier error codes behind failures — a rising rate of one specific code is
  a filtering problem, not a list problem
- Opt-out rate, trended rather than per-send
- Click-through on the branded domain
- Throughput actually achieved versus your registered tier

A sudden delivery-rate drop on one carrier while others hold steady is filtering. A drop across all
carriers at once is usually registration or number status.

## Related

- [SMS Compliance](./sms-compliance.md) — consent, quiet hours, STOP/HELP; the rules the carriers enforce
- [Ecommerce Flows](./ecommerce-flows.md) — which moments justify the channel
- [List Management](./list-management.md) — per-channel consent and suppression
- [Deliverability](./deliverability.md) — the email equivalent
