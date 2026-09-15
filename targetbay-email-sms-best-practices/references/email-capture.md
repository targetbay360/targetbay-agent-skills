# Email and SMS Capture

Where the list comes from. A capture form that collects bad addresses or weak consent creates a
deliverability problem you will pay for months later.

## Validation

### Client-side

Catches typos before submission. It is a courtesy, never a guarantee.

```html
<input
  type="email"
  name="email"
  autocomplete="email"
  inputmode="email"
  required
  placeholder="you@example.com"
>
```

- `type="email"` gives the correct mobile keyboard and a free format check
- Validate on blur, not on every keystroke — validating mid-typing shows an error for every address
  before it is finished
- Offer a correction for the common domain typos (`gmial.com`, `hotmial.com`, `yahoo.con`) rather
  than rejecting them
- Never block submission on client-side validation alone

### Server-side

Required. Client-side validation is trivially bypassed.

- Syntax check, then MX record check on the domain — a domain with no MX cannot receive mail
- Reject disposable-domain addresses for accounts that matter, and keep the blocklist updated
- Decide deliberately about role addresses (`info@`, `sales@`, `support@`) — they are legitimate for
  B2B and a complaint risk for consumer marketing
- Normalise before storing and before deduplicating: trim, lowercase the domain
- Rate-limit by IP and by address to stop list-bombing, where an attacker signs a victim's address up
  to hundreds of forms at once

A verification API adds a reachability check beyond syntax and MX. Worth it for paid acquisition,
where a bad address costs you twice.

## Double opt-in

Send a confirmation message; only subscribe on confirmation.

**Worth it when:** the sending domain is new, the list is for marketing, acquisition is paid, or you
need defensible consent under GDPR or CASL.

**Skip it when:** the address is already verified through a completed transaction, and the
subscription is a secondary checkbox on that transaction.

| | Single opt-in | Double opt-in |
|---|---|---|
| List size | Larger | Smaller |
| List quality | Mixed | High |
| Bot and typo addresses | Enter the list | Filtered out |
| Consent evidence | Form record only | Form record plus a confirmed action |
| Early deliverability | Riskier | Protected |

Process:

1. Form submitted → record as pending, not subscribed
2. Confirmation message sent immediately
3. Confirmation link clicked → subscribed, timestamp recorded
4. Unconfirmed after the expiry window → discard the pending record, do not mail it again

Set the link to expire in 24 to 48 hours. Allow another confirmation message after a cooldown of
around 60 seconds, capped per hour. Phrase the control as **"Send it again"**.

## Onsite capture for ecommerce

The popup is the main acquisition surface for most stores, and the main irritation surface.

**Timing.** Fire on intent, not on arrival. Scroll depth, time on a product page, second page view
or exit intent all beat an immediate interrupt. An instant popup interrupts the visitor before they
know whether they want anything.

**Frequency.** Once per visitor per period, remembered across sessions. A dismissed popup that
returns on the next page view is the reason people install blockers.

**Mobile.** A full-screen interstitial on mobile is both a bad experience and a search-ranking
liability. Use a bar or a bottom sheet, and make the close control an obvious, finger-sized target.

**The incentive is a promise.** If the popup says 10% off, the welcome message carries the code and
it arrives immediately. Nothing burns a new subscriber faster than having to chase a discount they
were just promised.

**Ask for one thing.** Email, or phone, not both in one step. If you want both, take the email, then
offer SMS on the thank-you step as a second, separately consented action.

Other surfaces worth having: an inline footer form, a checkout opt-in checkbox (unticked), a
back-in-stock request form, and a post-purchase thank-you page offer.

## Consent checkboxes

For marketing, under opt-in regimes:

```html
<label>
  <input type="checkbox" name="marketing_email" value="1">
  Email me news, offers and product updates. Unsubscribe any time.
</label>

<label>
  <input type="checkbox" name="marketing_sms" value="1">
  Text me offers and order updates. Up to 4 msgs/month.
  Msg &amp; data rates may apply. Reply STOP to unsubscribe.
</label>
```

Rules:

- Unticked by default, always
- Separate checkbox per channel — one box cannot grant both
- The label states what they will get and how often
- Not a condition of purchase, and not bundled into terms acceptance
- Store the exact label text shown, alongside the timestamp and source

## SMS opt-in specifically

**A phone number is not SMS consent.** A number captured for delivery notifications does not permit
marketing texts. This is the single most expensive mistake in the channel — see
[SMS Compliance](./sms-compliance.md) for the damages.

The disclosure has to be at the point of capture, visible before submission, and must carry: the
brand name, the message type, the frequency, "Msg & data rates may apply", "Reply STOP to
unsubscribe", a link to terms, and a statement that consent is not required to purchase.

Keep-out list:
- No pre-ticked SMS box
- No single box covering email and SMS together
- No SMS consent inherited from an email subscription, or from a past purchase

## Form design

- One field for a newsletter signup. Every additional field costs conversions.
- Label above the field, not a placeholder used as a label — the placeholder disappears on focus and
  takes the question with it
- Full-width fields on mobile, 44px minimum tap height
- Button text that says what happens: "Get 10% off", not "Submit"
- Show the consent text before the button, not after it

## Error handling

**Invalid address:** say what is wrong and keep what they typed. "That does not look like an email
address — check for a typo?" Never clear the field.

**Already subscribed:** confirm rather than error. "You are already on the list." Do not reveal
account existence on a form that could be used to enumerate customers.

**Rate limited:** "Too many attempts. Try again in a few minutes." No detail about the limit.

**Server failure:** say so, keep the input, and offer a retry. Silently dropping a signup is the
worst outcome.

## Related

- [SMS Compliance](./sms-compliance.md) — what the SMS disclosure must contain
- [Compliance](./compliance.md) — consent records and what to store
- [Marketing Emails](./marketing-emails.md) — what counts as explicit opt-in
- [Ecommerce Flows](./ecommerce-flows.md) — the welcome flow that has to honour the promise
