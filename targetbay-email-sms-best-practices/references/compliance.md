# Email Compliance

Not legal advice. These are the requirements engineers and marketers have to build for; a lawyer
decides what applies to your business.

## Quick Reference

| Law | Region | Consent model | Exposure |
|---|---|---|---|
| CAN-SPAM | United States | Opt-out — you may mail until told to stop | Per-message civil penalties, adjusted annually for inflation |
| GDPR | European Union / EEA | Opt-in — consent required before the first message | Up to €20M or 4% of global annual turnover |
| CASL | Canada | Opt-in, with narrow implied-consent windows | Up to CAD $1M for individuals, CAD $10M for organisations |
| UK GDPR + PECR | United Kingdom | Opt-in, with a narrow "soft opt-in" for existing customers | Up to £17.5M or 4% of turnover |

Your obligations follow **where the recipient is**, not where the company is. A US store with
European customers is subject to GDPR for those contacts. Build to the strictest regime present in
your list and you are covered everywhere; build to CAN-SPAM only and you are exposed the moment one
EU address signs up.

## CAN-SPAM (United States)

Applies to commercial messages. Requirements:

- Accurate `From`, `Reply-To` and routing information — no disguised sender
- A subject line that does not misrepresent the content
- Identification as an advertisement, where the message is not obviously one
- A valid physical postal address in every message
- A clear, working opt-out mechanism
- Opt-outs honoured within 10 business days, and no fee or extra information required to use them
- Liability extends to a third party mailing on your behalf — outsourcing does not transfer it

## GDPR (European Union)

Consent must be freely given, specific, informed and unambiguous — an affirmative action.

- **No pre-ticked boxes**, and no consent bundled into terms acceptance
- Consent for marketing is separate from the transaction; a checkout cannot require it
- Record what was consented to, when, how, and the exact wording shown
- Withdrawal must be as easy as giving it
- Honour the data-subject rights: access, rectification, erasure, portability, objection
- Have a lawful basis. Transactional mail usually rests on contract performance; marketing usually
  rests on consent, and "legitimate interest" for ecommerce marketing is a position to take with
  legal advice, not a default

## CASL (Canada)

The strictest of the common regimes.

- Express consent, requested and recorded separately
- Implied consent exists but is time-limited — commonly two years from a purchase, six months from
  an enquiry — and it expires whether or not you noticed
- Every message identifies the sender, gives a mailing address and a working contact method
- Unsubscribe must work for at least 60 days after the message was sent
- Opt-outs honoured within 10 business days
- The burden of proving consent is on you, so an unevidenced consent is no consent

## Unsubscribe — what "working" means

Every marketing message needs:

1. A visible unsubscribe link, in the body, without hunting
2. One-click behaviour where possible — no login, no password, no "tell us why" gate
3. Processing within 10 business days at the outside; same-day in practice, because the gap is where
   complaints come from
4. No cost and no extra data collection

### The List-Unsubscribe headers

Gmail and Yahoo require one-click unsubscribe for bulk senders, and it takes **both** headers.
Publishing one without the other does not satisfy the requirement.

```
List-Unsubscribe: <https://example.com/unsubscribe?token=abc123>, <mailto:unsubscribe@example.com?subject=unsubscribe>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

The URL must accept a `POST` and act on it immediately, without a confirmation page. A one-click
endpoint that renders "are you sure?" is a broken one-click endpoint, and the provider treats it as
non-compliant.

Token design matters: the token identifies the subscription, so it must be unguessable, single-purpose
and not reveal the address. Providers may fetch these links pre-emptively, so a `GET` must never
unsubscribe anyone on its own.

## Preference centre vs unsubscribe

A preference centre is good practice — letting someone drop to monthly instead of leaving entirely
saves the contact. It is not a substitute for the exit.

- The one-click header must unsubscribe, not open the preference centre
- "Unsubscribe from all" has to be present on the preference page itself
- Per-channel: unsubscribing from email does not opt someone out of SMS, and the reverse is also
  true. Store consent per channel. See [List Management](./list-management.md).

## Consent records

For every contact, store enough to prove consent later:

| Field | Why |
|---|---|
| Channel | Email and SMS consent are separate grants |
| Timestamp | Proves order of events and CASL expiry windows |
| Source | Which form, popup, checkout or import |
| IP address / user agent | Corroborates a web opt-in |
| Exact wording shown | The claim is about what they agreed to, not what the form says today |
| Double opt-in confirmation | The strongest single piece of evidence |

Keep the record for as long as you mail the contact, plus your jurisdiction's limitation period.

## Data retention

Do not keep personal data indefinitely because it was cheap to store.

- Set a retention period per data class and enforce it with a scheduled job
- Suppression entries are the exception — they must outlive the contact record, or an erased
  unsubscribe becomes a re-subscribe on the next import
- Erasure requests remove the profile but retain the suppression token; store a hash rather than the
  plaintext address where you can

## Privacy policy

It has to say, in plain language: what you collect, why, the lawful basis, who it is shared with,
how long it is kept, what rights the person has and how to exercise them, and how to contact you.
Link it from every capture point, not only the footer.

## Related

- [SMS Compliance](./sms-compliance.md) — a separate and stricter regime
- [Email Capture](./email-capture.md) — collecting consent that holds up
- [List Management](./list-management.md) — suppression and per-channel consent
- [Email Types](./email-types.md) — which messages these rules apply to
