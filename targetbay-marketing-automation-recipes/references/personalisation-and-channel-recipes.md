# Personalisation and Channel Recipes

Varying what a person receives, and sequencing across email and SMS so the two reinforce rather than
collide.

All recipes below inherit [Guardrails](./guardrails.md), select a pre-built campaign rather than
creating one, and quote the source workflow's intervals rather than recommending them. See
[How to Read a Recipe](./how-to-read-a-recipe.md).

---

### Offer selection from a pre-approved set

**Problem** — "We run one blanket promo for everyone, so we discount people who would have paid full
price and under-offer the ones who needed more."

**Trigger** — platform event, `contact.updated`, filtered to contacts with purchase history. Or a
schedule, if the update event is too noisy.

**Preconditions** — **a pre-approved offer set with margin bounds already agreed.** This is the
precondition that makes the recipe safe, and without it the recipe should not be built. Purchase
history rich enough to distinguish one contact from another. A campaign per offer, or one campaign
whose personalisation carries the offer.

**Steps**
1. Receive the trigger; filter to contacts with enough history to be worth differentiating.
2. Read the contact and their order history — `email_sms.customer_intelligence`.
3. **Select** an offer from the approved set. Selection, never generation: the model or the rule
   picks from a fixed list and cannot invent a discount.
4. Check the offer against the margin bound for those products. Out of bounds means no offer, not a
   clamped one.
5. Check suppression, consent and the frequency budget.
6. Send the campaign for the selected offer — `email_sms.messaging_email`.
7. Record which offer went to whom — `email_sms.event_tracking`.


**Guardrails** — **selection from an approved set, never generation.** An unbounded per-person offer
is price discrimination, and it is also how a 90% discount reaches a customer at 3am with nobody
watching. Cap how often one contact receives an offer at all; repeated discounting trains people to
wait. Record the offer sent, so the next run can see it.

**What to measure** — outcome: incremental revenue against a holdout who got the standard offer.
Guard: margin per order, which is what an over-generous selector destroys first. Track both or the
recipe will look successful while losing money.

**Failure modes** — history-poor contacts all receive the same default offer, which is fine but must
be visible rather than presented as personalisation. The approved set goes stale and the recipe keeps
sending an expired code.

**Not verified** — whether order history is reachable through the contact read or needs a separate
source. The strategic question of which offer a segment deserves belongs to
[aov-growth](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/aov-growth/SKILL.md);
the governance of a model doing the selecting belongs to
[ai-content-governance](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/ai-content-governance/SKILL.md).

---

### Email then SMS escalation

**Problem** — "We send the same thing on both channels at the same time, so it costs twice as much
and annoys people."

**Trigger** — platform event, or any recipe that wants a second touch.

**Preconditions** — **separate SMS consent**, recorded per channel. A phone number on a record is not
permission to text it. A short SMS body that stands alone — the SMS is not a summary of the email.

**Steps**
1. Branch on whether the contact has a phone number **and** SMS consent. No consent, no branch — the
   email-only path is the complete recipe for them, not a degraded one.
2. Check suppression and consent for email. Send — `email_sms.messaging_email`.
3. Wait. The source workflow used five minutes.
4. Re-check: did they act on the email? If so, stop. The SMS exists to catch people who did not.
5. Check SMS consent again, and the recipient's local time against quiet hours.
6. Send the SMS — `email_sms.messaging_sms`.
7. Record the multi-channel touch — `email_sms.event_tracking`.


**Guardrails** — the two sends spend from **one** frequency budget, not two. Quiet hours are
evaluated in the recipient's local time and are a legal constraint on SMS in many jurisdictions, not
a courtesy. Five minutes is short enough that step 4 will usually find nothing; if the SMS is a
reminder rather than a nudge, the gap should be longer and derived from how fast this store's
customers actually open.

**What to measure** — outcome: action rate for the two-channel path against email-only, on comparable
contacts. Guard: SMS opt-out rate, which is the fastest-moving signal of over-contact in the set.

**Failure modes** — sending SMS on the presence of a phone number rather than on consent, which is a
compliance failure and not a bug. The email lands late and the SMS arrives first, making the SMS
incomprehensible.

**Not verified** — **whether the MCP exposes SMS dispatch at all.** `email_sms.messaging_sms` is
declared but unconfirmed. Confirm before building; if it is absent, this recipe degrades to
email-only rather than sending SMS by another route.

---

### Click-branched nurture

**Problem** — "Everyone in the nurture gets the same three emails whether they engaged with the first
one or ignored it."

**Trigger** — inbound form, or platform event `contact.created`.

**Preconditions** — click data reaching the recipe, either from `campaign.clicked` or a read of
campaign reports. Two follow-up paths with genuinely different content — branching to two near-identical
messages is complexity with no payoff.

**Steps**
1. Capture the contact — a contact write, which has no registered capability yet (see [Capabilities](./how-to-read-a-recipe.md#capabilities)).
2. Add to the nurture list — `email_sms.segmentation`.
3. Check suppression, then send the first message — `email_sms.messaging_email`.
4. Wait. The source workflow used twenty-four hours.
5. Determine engagement: a `campaign.clicked` event for this contact, or a report read.
6. **Branch.** Engaged takes the interested path. Not engaged takes a *different* message — not the
   same one again, and not a more insistent version of it.
7. Re-check suppression and the budget. Send — `email_sms.messaging_email`.
8. Record the branch taken — `email_sms.event_tracking`.


**Guardrails** — **escalating contact to someone who did not respond is the wrong direction.** The
non-engaged branch is a different approach or a stop, never a louder repeat. Absence of a click is
weak evidence — a click tracked through a redirect can be missed, and image-blocking hides opens
entirely — so treat the non-engaged branch as "no signal", not "not interested".

**What to measure** — outcome: conversion per branch. Guard: unsubscribe rate on the non-engaged
branch specifically, which is where over-contact shows up first.

**Failure modes** — click data arrives after step 5 evaluates, so everyone falls into the non-engaged
branch; check the timing against the store's real click distribution before setting the wait. A
redelivered click event re-branches a contact already past that point.

**Not verified** — whether `campaign.clicked` is reliable enough to branch on, and whether report
reads are timely enough to substitute. Test both against a real send before relying on either.
