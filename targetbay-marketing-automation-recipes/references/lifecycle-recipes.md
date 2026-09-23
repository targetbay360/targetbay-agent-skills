# Lifecycle Recipes

Journeys triggered by something the customer did. They reach people in a live buying moment rather
than on the store's calendar, which is why they earn more per recipient and generate fewer
complaints than campaigns.

All recipes below inherit [Guardrails](./guardrails.md), select a pre-built campaign rather than
creating one, and quote the source workflow's intervals rather than recommending them. See
[How to Read a Recipe](./how-to-read-a-recipe.md).

Derive your own intervals from the store's own data —
[automation-rules.md#R13](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/rules/automation-rules.md).

The six flows here are also described as strategy, without the wiring, in
[Ecommerce Flows](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/ecommerce-flows.md) —
read that for what each flow is for and when it should exit.

---

### Source-aware welcome

**Problem** — "Everyone who signs up gets the same first email, whether they came from a popup, a
checkout box or Instagram."

**Trigger** — platform event, `contact.created`.

**Preconditions** — the capture form records where the signup came from, in a field that is actually
populated rather than defaulting to blank. A pre-built template per source. Consent recorded at
capture.

**Steps**
1. Receive and verify the event. Reject unsigned.
2. Filter: is this a real signup, or a contact created by an import or an order? An import that
   creates thousands of contacts will fire thousands of welcomes.
3. Read the contact to get the source field — `email_sms.customer_intelligence`.
4. Branch on source. Unknown or missing source takes the default branch; it does not stop the
   journey.
5. Select the campaign for that branch — `email_sms.campaign_management`.
6. Check suppression and consent, then send — `email_sms.messaging_email`.
7. Record the send against the contact — `email_sms.event_tracking`.


**Guardrails** — dedupe on contact id plus journey name, so a redelivered `contact.created` does not
welcome twice. Explicitly exclude contacts created by bulk import. If the signup promised an
incentive, the first message carries it and nothing precedes it.

**What to measure** — outcome: first-purchase rate within the window, by source. Guard: unsubscribe
rate in the first message, by source. A source whose welcome unsubscribes heavily is a capture
problem, not a copy problem.

**Failure modes** — a bulk import fires a welcome storm; the source filter at step 2 is the only
thing preventing it, so test it against an import before going live. A missing source field silently
routes everyone to default, which looks like success; alert when the default branch share rises.

**Not verified** — where the signup source is stored, and whether it is present on the event payload
or requires the extra read at step 3. The recipe assumes the read, which is safe either way.

---

### Onboarding drip

**Problem** — "New subscribers hear from us once and then nothing until the next campaign."

**Trigger** — platform event, `contact.created`.

**Preconditions** — three pre-built campaigns. A clear exit condition, agreed before building.

**Steps**
1. Receive and verify the event; apply the same import filter as the welcome recipe.
2. Wait. The source workflow used one day.
3. Check the exit condition and suppression. If the contact has purchased, exit — do not keep
   courting someone who already converted.
4. Send the first drip message — `email_sms.messaging_email`.
5. Wait. The source workflow used three more days.
6. Re-check exit and suppression. Send the second — `email_sms.messaging_email`.
7. Wait. The source workflow used four more days.
8. Re-check exit and suppression. Send the third — `email_sms.messaging_email`.
9. Record completion — `email_sms.event_tracking`.


**Guardrails** — **the exit condition is checked before every send, not only at entry** — the most
common lifecycle bug there is. Dedupe on contact id plus step number, so a restarted orchestrator
does not replay the sequence.

**What to measure** — outcome: conversion by step, which shows where the sequence stops earning.
Guard: cumulative unsubscribe across the three sends.

**Failure modes** — a long wait held in orchestrator memory is lost on restart; hold the schedule in
durable state. In-flight contacts when the journey is edited will experience a mix of old and new —
decide before editing whether they finish on the old version.

**Not verified** — whether the platform can hold multi-day waits natively. If it can, this belongs
inside the platform and not in an orchestrator at all; see
[Automation Orchestration](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/automation-orchestration/SKILL.md).

---

### Two-touch cart recovery

**Problem** — "People fill a cart and leave, and we never follow up."

**Trigger** — platform event, `order.created`, filtered to carts that did not complete.

**Preconditions** — the platform emits an event for an abandoned cart, or the store pushes one. A
restored-cart link that actually restores the cart. Two pre-built campaigns.

**Steps**
1. Receive and verify the event.
2. Filter to abandonment rather than completed purchase. Getting this filter wrong mails people who
   already bought, which is the single worst outcome in this document.
3. Wait. The source workflow used one hour.
4. Read the contact — `email_sms.customer_intelligence`. Check suppression, consent and the frequency budget.
5. Check the cart is still purchasable.
6. Send the first reminder — `email_sms.messaging_email`.
7. Wait. The source workflow used a further twenty-four hours.
8. Re-check: purchased? cart cleared? suppressed? If any, exit.
9. Send the second reminder — `email_sms.messaging_email`.
10. Record the recovery attempt — `email_sms.event_tracking`.


**Guardrails** — exit on purchase, checked at step 8 and not only at entry. Dedupe on cart identifier
plus step. One identified visitor only — never send to an inferred address. What the messages should
say, and why the first one does not carry a discount, is in
[Ecommerce Flows](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/ecommerce-flows.md).

**What to measure** — outcome: recovered revenue attributable to the two sends. Guard: complaint rate,
which rises fast when the abandonment filter is wrong.

**Failure modes** — the purchase lands between step 8's check and step 9's send, and the customer
gets a reminder for an order they placed; narrow the gap by checking as late as possible. Stock sells
out during the wait.

**Not verified** — whether cart abandonment is distinguishable from order creation on the event
payload alone, or needs a store-side signal. If the latter, this is a store-pushed trigger and needs
`email_sms.event_tracking` plus an orchestrator.

---

### Order confirmation

**Problem** — "Our order receipts come from the store platform and look nothing like our brand, and
we can't see how they perform."

**Trigger** — platform event, `order.created`, filtered to confirmed orders.

**Preconditions** — a confirmation campaign with order personalisation. Agreement on which system
owns the receipt — two systems both sending one is worse than either.

**Steps**
1. Receive and verify the event.
2. Filter to confirmed orders only.
3. Read the contact — `email_sms.customer_intelligence`.
4. Assemble the order detail for personalisation.
5. Send — `email_sms.messaging_email`.
6. Record — `email_sms.event_tracking`.


**Guardrails** — dedupe on order id; a redelivered event must not send a second receipt. **Consent
rules differ here**: a receipt is transactional, but a receipt carrying product recommendations or an
offer is legally marketing in most jurisdictions, and a contact who opted out of marketing must not
receive that version. Decide which one this is before building it.

**What to measure** — outcome: delivery rate, which should be near-total for a transactional message.
Guard: complaint rate, which should be near-zero — anything else means the message is reading as
marketing.

**Failure modes** — duplicate receipts from redelivered events, which customers notice and report.
Both the store platform and this recipe sending, producing two receipts per order.

**Not verified** — whether a transactional send bypasses marketing suppression on this platform, and
whether it should. Confirm before assuming either.

---

### Review request after delivery

**Problem** — "We ask for reviews a fixed number of days after the order, so people who are still
waiting for the parcel get asked."

**Trigger** — platform event, `order.updated`, filtered to a delivered state.

**Preconditions** — delivery status actually reaches the platform. Without it this recipe cannot be
built correctly, and gating on order date instead is the thing it exists to avoid.

**Steps**
1. Receive and verify the event.
2. Filter to the delivered transition specifically, not any update.
3. Wait. The source workflow used three days — long enough to have used the product, short enough to
   still remember buying it.
4. Read the contact — `email_sms.customer_intelligence`. Check suppression and the frequency budget.
5. Check no review already exists for this order.
6. Send — `email_sms.messaging_email`.
7. Record — `email_sms.event_tracking`.


**Guardrails** — dedupe on order id. Do not ask twice for the same order. Do not ask a customer whose
order had a return or a support ticket open — that request lands as tone-deaf and generates the
review you did not want.

**What to measure** — outcome: reviews submitted per request sent. Guard: unsubscribe rate, and the
share of reviews below the store's own average — a spike suggests the timing or the audience is
wrong.

**Failure modes** — `order.updated` fires on any change, so a loose filter asks for a review when the
billing address changes. Delivery status never arrives and the recipe silently never fires; alert on
zero sends rather than assuming quiet means healthy.

**Not verified** — whether delivery state is present on the `order.updated` payload. The review
programme decision — who to ask, how often, what to do about a bad rating — belongs to
[review-request-program](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-reviews/skills/review-request-program/SKILL.md).

---

### VIP threshold crossing

**Problem** — "Someone becomes one of our best customers and we don't notice for a month."

**Trigger** — platform event, `contact.updated`.

**Preconditions** — a VIP definition the store agrees with, expressed against fields that are
actually populated. A VIP campaign that offers something real — recognition without substance reads
worse than silence.

**Steps**
1. Receive and verify the event.
2. Evaluate the VIP definition against the updated contact.
3. **Compare against previous state.** Only a *crossing* fires the journey; a contact who was already
   VIP and changed their phone number must not be congratulated again.
4. Read the contact — `email_sms.customer_intelligence`.
5. Add to the VIP list — `email_sms.segmentation`.
6. Check suppression, then send — `email_sms.messaging_email`.
7. Record the crossing — `email_sms.event_tracking`.


**Guardrails** — **the crossing check at step 3 is the whole recipe.** Without it, every profile
update to an existing VIP re-sends the welcome. Dedupe on contact id plus tier. Decide in advance
what happens when someone falls back below the threshold; silently demoting is usually right,
messaging about it is usually not.

**What to measure** — outcome: repeat rate of contacts who crossed, against those who crossed before
the recipe existed. Guard: how many contacts cross more than once in a period, which is the crossing
check failing.

**Failure modes** — `contact.updated` fires on every field change, so an unfiltered version is a
high-volume trigger that sends constantly. Membership held only in an orchestrator's memory is lost
on restart; the list at step 5 is the durable record.

**Not verified** — whether the event payload carries the previous value, or whether step 3 needs the
list membership from step 5 as its own state. The recipe assumes the latter, which works either way.
