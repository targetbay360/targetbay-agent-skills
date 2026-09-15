# SMS Compliance

Not legal advice. SMS is regulated more tightly than email, enforced privately through class actions,
and additionally policed by the carriers — so non-compliance costs money twice: in damages and in
undelivered messages.

## TCPA (United States)

The federal floor for text marketing.

- **Prior express written consent** is required before any marketing text. Written means a recorded
  affirmative act — a ticked box, a submitted form, a text-in keyword — not a phone number captured
  at checkout.
- Consent must be **specific to SMS marketing**. An email subscription is not SMS consent. A phone
  number given for delivery updates is not SMS marketing consent.
- It cannot be **bundled** — consent to texts cannot be a condition of purchase, and cannot be
  buried in terms acceptance.
- It cannot be **pre-ticked**.
- **Statutory damages are per message**: USD $500, rising to $1,500 where the violation is wilful.
  There is no cap, which is what makes this class-action territory. Recent settlements in this area
  have run into eight figures.

Transactional texts — order confirmation, shipping, delivery, an OTP — rest on a different footing
from marketing, but the safest build treats the consent record as the gate for all of them and
records the purpose.

## State laws layer on top

Roughly fifteen states now impose additional duties beyond the TCPA, and the list grows.

- **Florida (FTSA)** and **Texas (SB 140, effective 1 September 2025)** are the most cited; Texas
  provides statutory damages up to USD $5,000 per violating message.
- California, New York, Washington, Virginia and others add their own consent, timing or disclosure
  requirements.

**Build for the strictest state present in your list.** Segmenting compliance by recipient state is
possible but fragile — one mis-mapped area code is a violation, and area code is not a reliable
proxy for where someone lives.

## Quiet hours

Marketing texts are restricted to **8am–9pm in the recipient's local time**, with some states
narrowing the window further.

This makes time-zone-aware scheduling a compliance control, not a courtesy:

- Schedule against the recipient's zone, never the store's
- Derive the zone from a stored attribute, not from the area code
- Where the zone is unknown, use the most restrictive window that covers your market
- Hold queued messages that would land outside the window rather than sending them late — a delayed
  send is a marketing decision, a 2am send is a liability

Automated flows are where this breaks. A cart-abandonment text triggered at 11:40pm fires at 11:40pm
unless the flow explicitly defers it.

## Required keyword handling

| Keyword | Required behaviour |
|---|---|
| STOP, UNSUBSCRIBE, CANCEL, END, QUIT | Opt out immediately. Send exactly one confirmation, then nothing further on that programme |
| HELP, INFO | Reply with the programme name, what it sends, and a contact method |
| START, UNSTOP, YES | Re-subscribe, only after a prior opt-out from the same person |

Rules that follow from this:

- The opt-out confirmation is a confirmation. It is not a retention pitch, a discount offer or a
  "sorry to see you go" survey.
- Honour the opt-out across the programme, not just the campaign that triggered it.
- Match on the keyword regardless of case and surrounding whitespace, and handle the common
  variants — carriers expect the recipient to be able to type it naturally.
- Opt-outs propagate to the number, not to the contact record alone. If the same person exists twice
  in your data, both records stop.

## Disclosures at opt-in

The point of capture must state, visibly and before submission:

- Who is sending — the brand name
- What kind of messages, and roughly how many ("up to 4 msgs/month")
- **"Msg & data rates may apply"**
- How to opt out ("Reply STOP to unsubscribe")
- A link to terms and privacy policy
- That consent is not a condition of purchase

These are also what you file in your A2P 10DLC campaign registration, and the registration is
checked against what the form actually says. A mismatch can get the campaign rejected or revoked —
see [SMS Deliverability](./sms-deliverability.md).

## Content restrictions

**SHAFT** — Sex, Hate, Alcohol, Firearms, Tobacco — is restricted or prohibited by carrier policy
regardless of legality. Age-gated categories require explicit carrier approval and age verification
at opt-in. Cannabis and most CBD messaging is prohibited on US carriers even in states where the
product is legal.

## Every message needs

- Identifiable sender in the body — the recipient sees a number, not a From name
- A link only if it is on your own branded short domain
- Opt-out instructions, at minimum on the first message of a programme and periodically after
- Content matching the registered campaign use case

## Outside the United States

- **Canada (CASL)** covers SMS as well as email, with the same express-consent and 60-day
  unsubscribe rules.
- **EU/UK** treat a phone number as personal data — GDPR/PECR consent rules apply, and the UK's
  soft opt-in is narrow.
- **Australia (Spam Act)** requires consent, sender identification and a functional unsubscribe.

Cross-border SMS also crosses carrier regimes; sender-ID rules, registration and permitted content
vary by country and change often. Confirm per market before launching there.

## Related

- [SMS Deliverability](./sms-deliverability.md) — carriers enforce most of this in the delivery path
- [Email Capture](./email-capture.md) — building the opt-in that produces valid consent
- [List Management](./list-management.md) — per-channel consent and suppression
- [Compliance](./compliance.md) — the email-side regimes
