# Email Principles

Email is the high-context channel: cheap per send, tolerant of length, and entirely dependent on a
reputation that takes months to build and days to lose.

## The deliverability constraint sits above everything

A perfectly targeted campaign that lands in spam produces nothing. Reputation is earned through
consistent recipient behaviour — engagement, low complaints, low bounces — and it is shared across every
send the store makes.

Practical consequences for planning:

- **Sending to unengaged contacts costs more than it earns.** It suppresses inbox placement for the
  contacts who *do* engage.
- **List hygiene is a revenue activity.** Suppressing the dead portion of a list usually raises total
  revenue, because the surviving sends land.
- **Volume spikes are a risk.** A store that sends to 10% of its list weekly and then blasts 100% has
  changed its pattern, and the pattern is part of what is being judged.
- **Complaints are the most expensive metric.** They are a direct signal that the recipient did not want
  this. Cadence and relevance are the levers.

Bounce handling, complaint feedback loops and suppression enforcement are platform
responsibilities — see [../rules/global-rules.md#G10](../rules/global-rules.md). The mechanism
underneath all of this — why identity, reputation and content are three separate layers with three
separate remedies — is [deliverability-principles.md](deliverability-principles.md).

## What email is good at

- Context: several ideas, images, comparison, browsing
- Consideration-phase content — education, proof, collections
- Anything the recipient may want to return to later
- Low marginal cost, which makes broad sends economically viable

## What it is bad at

- Immediacy. Open rates accumulate over hours or days.
- Guaranteed attention. Inbox placement is not reading.
- Very short, urgent, single-action messages — SMS does those better.

## Structural fundamentals

- **From name** does more work than the subject line. Recognition decides the open.
- **Subject line and preheader are one unit.** The preheader is not filler.
- **First screen carries the message.** Assume nothing below it is read.
- **One primary call to action.** See [../rules/content-rules.md#N2](../rules/content-rules.md).
- **Must survive images off.** A message that is one large image is a message that fails for a
  meaningful share of recipients and for accessibility.
- **Mobile-first.** Most opens are on a phone; a desktop-designed email that reflows badly is a broken
  email.

## Engagement metrics, correctly ranked

1. Revenue and conversion — what the campaign was for
2. Unsubscribe and complaint rate — what it cost
3. Click rate — whether the content worked
4. Open rate — a weak, increasingly unreliable diagnostic, distorted by privacy-protection prefetching

Open rate is useful for *comparing* two subject lines in a controlled test. It is not useful as a success
criterion. See [../rules/global-rules.md#G1](../rules/global-rules.md).

## Cadence

Email tolerates more frequency than SMS, but the ceiling is set by engagement, not by permission. Rising
unsubscribes at stable content quality means the cadence is too high for that segment. See
[../rules/frequency-rules.md](../rules/frequency-rules.md).

## Email and SMS together

Email carries the context; SMS carries the urgency. Sequencing them deliberately — email for the
explanation, SMS for the deadline — outperforms sending the same content twice. See
[sms-principles.md](sms-principles.md).
