# Marketing Email Best Practices

Campaigns are the discretionary sends: you choose the audience, the content and the moment. That
freedom is why they carry most of the reputation risk.

## Core principles

1. **Consent first.** No consent, no send. Not "we bought a list that opted in somewhere".
2. **Earn the send.** If you cannot say what the recipient gets from this message, do not send it.
3. **Respect the preference.** Frequency, channel and topic choices are instructions, not hints.
4. **Campaigns are the reputation risk.** Automated flows go to people in a live buying moment and
   rarely generate complaints. Promotional campaigns go to everyone, including the person who has
   not opened anything in a year. Almost every complaint spike traces back to a campaign.

## Opt-in

### What counts as explicit

- An affirmative act — ticking an unticked box, submitting a form whose purpose is subscribing,
  texting a keyword
- Specific to marketing on that channel
- Not bundled with terms acceptance, not a condition of checkout
- Recorded with timestamp, source and the wording shown

### What does not count

- A pre-ticked box
- A purchase, on its own, under opt-in regimes
- A contest entry that did not mention marketing
- An address collected for support, shipping or an invoice
- A list bought, rented, scraped or inherited in an acquisition without checking the consent basis

### Double opt-in

Costs some signups and pays for itself in deliverability. It gives you a verified address, evidence
of consent, and a list that engages. Strongly worth it for a new sending domain, where early
engagement is what builds the reputation. See [Email Capture](./email-capture.md).

## Unsubscribe

- Visible link in the body of every marketing message
- `List-Unsubscribe` **and** `List-Unsubscribe-Post` headers — details in [Compliance](./compliance.md)
- Works without a login
- Processed immediately
- A preference centre is an option, never the only exit

A hard-to-find unsubscribe does not retain anyone. It converts an unsubscribe — which costs you one
contact — into a complaint, which costs you inbox placement for the whole list.

## Subject lines and preheader

- Say what is inside. Curiosity gaps work once and train people to distrust you.
- Front-load the specific words; mobile truncates hard.
- The preheader is the second line, not a dumping ground.
- Emoji: at most one, and only where it matches the brand. Two or more reads as promotional noise to
  both humans and filters.
- Never fake a reply (`Re:`) or an urgency you do not have. It is a CAN-SPAM problem as well as a
  trust problem.

## Structure

1. Recognisable brand mark
2. One message, stated in the first screen
3. Supporting content — products, proof, detail
4. One primary call to action, repeated at most once lower down
5. Secondary links, if any
6. Footer: company name, physical address, unsubscribe, preference centre

**One primary action.** A campaign with four equally weighted buttons converts worse than the same
campaign with one, because the choice itself is friction.

## Mobile first

Most opens are on a phone.

- Single column, 600px maximum, fluid below that
- 16px body text
- Tap targets 44×44px with space between them
- The call to action visible without scrolling
- Images with meaningful alt text — assume they are blocked
- Never a single exported image as the whole message

## Segmentation

Segmentation is what separates a campaign programme from a blast. The useful axes in ecommerce:

- Purchase recency and frequency
- Lifetime value and average order value
- Category or brand affinity
- Engagement recency — who has opened or clicked lately
- Acquisition source
- Location, where it changes the offer or the shipping promise

The most valuable segment is usually the negative one: **who should not receive this**. Excluding
people who just bought the product being promoted, and excluding the long-unengaged, improves both
revenue per send and deliverability.

Do not create a segment that changes nothing. If two segments receive the same message, they are one
segment.

## Personalisation that degrades safely

Every personalised field needs a fallback, and the fallback has to read naturally.

- `Hi {{first_name}}` with an empty field produces `Hi ,` — use a default of nothing and rewrite the
  line so it works without the name
- Only personalise on data you actually hold and trust. A wrong first name is worse than none.
- Behavioural personalisation ("you were looking at X") needs a light touch — see the browse
  abandonment note in [Ecommerce Flows](./ecommerce-flows.md)
- Test the empty case for every dynamic block, including product feeds that can return zero items

## Frequency and timing

- Cadence is bounded by engagement, not by permission. Rising unsubscribes at steady content quality
  means the cadence is too high **for that segment**.
- Set frequency caps across campaigns and flows together. A customer in three flows plus the weekly
  campaign is receiving more than anyone planned.
- Send-time claims in industry advice are not transferable. Test against your own list.
- Keep the pattern steady. Volume spikes are a deliverability signal — see
  [Deliverability](./deliverability.md).

## Required in every marketing message

- [ ] Accurate From name and address
- [ ] Subject line that matches the content
- [ ] Physical postal address
- [ ] Visible unsubscribe link
- [ ] `List-Unsubscribe` and `List-Unsubscribe-Post` headers
- [ ] Sent only to contacts with consent on this channel
- [ ] Checked against suppression before send
- [ ] Sent from the marketing subdomain

## Related

- [Ecommerce Flows](./ecommerce-flows.md) — the automated sends, which outperform campaigns
- [Email Capture](./email-capture.md) — where consent comes from
- [Compliance](./compliance.md) — the legal floor
- [List Management](./list-management.md) — who to stop sending to
