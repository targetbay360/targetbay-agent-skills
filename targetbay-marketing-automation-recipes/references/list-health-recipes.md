# List Health Recipes

Keeping the sending population clean. Deliverability degrades silently — nothing alerts you that
inbox placement slipped — which is why these three run on a schedule or on an event rather than when
someone thinks to look.

All recipes below inherit [Guardrails](./guardrails.md), select a pre-built campaign rather than
creating one, and quote the source workflow's intervals rather than recommending them. See
[How to Read a Recipe](./how-to-read-a-recipe.md).

The decision about **who leaves the sending population and when** is not a wiring decision. See
[list-hygiene](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/list-hygiene/SKILL.md).

---

### Scheduled hygiene audit

**Problem** — "We have no idea what shape our list is in until something goes wrong."

**Trigger** — schedule. The source workflow ran weekly.

**Preconditions** — somewhere for the report to go that a person actually reads. A prior run to
compare against — a single snapshot tells you almost nothing; the trend is the signal.

**Steps**
1. Read the contact base — `email_sms.customer_intelligence`, paged.
2. Read recent campaign results — `email_sms.campaign_management`, then `email_sms.campaign_analytics` per campaign.
3. Compute the shape of the list: how it is growing, what share has never engaged, where bounces and
   complaints are concentrated, which acquisition sources produce which quality.
4. **Compare against the previous run.** Report movement, not levels.
5. Flag anything moving in the wrong direction against a threshold derived from this store's own
   variance — never a round number borrowed from elsewhere.
6. Send the report to the team — `email_sms.messaging_email` to an internal list, or a message to a team channel.
7. Store the run so the next one has something to compare against.


**Guardrails** — this recipe reports; it does not suppress. Automatic removal based on an aggregate
audit removes people who were merely quiet. Segment quality by acquisition source — one bad source
will otherwise look like a general decline and send you looking in the wrong place.

**What to measure** — outcome: whether a flagged problem was acted on before it became a
deliverability incident. Guard: how often the report is read; an unread report is a recipe that costs
and returns nothing.

**Failure modes** — the report is sent to an internal list that is itself suppressed, so nobody gets
it. Thresholds set from published benchmarks rather than the store's own history, producing constant
false alarms until people stop reading.

**Not verified** — whether engagement recency is available per contact or must be assembled from
campaign reports, which changes the cost of step 1 considerably at scale.

---

### Bounce and complaint response

**Problem** — "Bounces pile up and we find out when a mailbox provider starts blocking us."

**Trigger** — platform event, `campaign.bounced` and `campaign.unsubscribed`. A rate check on a
schedule as well, since a slow rise never produces a single alarming event.

**Preconditions** — the platform's own bounce classification. **This recipe never classifies a bounce
itself** — it reads the platform's verdict and decides the programme's response.

**Steps**
1. Receive and verify the event.
2. Read the platform's classification. A permanent failure and a temporary one get different
   responses; treating them alike either keeps mailing a dead address or discards a good one.
3. Read the contact — `email_sms.customer_intelligence`.
4. Permanent failure: update the contact's state — a contact write, which has no registered capability yet (see [Capabilities](./how-to-read-a-recipe.md#capabilities)) — and remove from active lists —
   `email_sms.segmentation`.
5. Repeated temporary failures for the same address: treat as permanent once the count derived from
   the store's own pattern is reached.
6. Record the outcome — `email_sms.event_tracking`.
7. Separately, on a schedule, compute the bounce and complaint rate and alert if it moves beyond the
   store's own recent variance.


**Guardrails** — **a single soft bounce is not a signal.** Acting on one removes people whose mailbox
was briefly full. Removal from a list is not suppression; make sure the contact cannot simply be
re-added by the next import. Rate alerting uses a threshold derived from this store's own variance,
not a published figure.

**What to measure** — outcome: bounce rate trend after the responder is live. Guard: how many
contacts were removed that later proved deliverable, which is the cost of an over-eager rule.

**Failure modes** — the classification is missing from the payload and everything is treated as
permanent, quietly shrinking the list. Removal succeeds but the contact is re-added by a nightly
sync, producing an endless loop of bounce, remove, re-add.

**Not verified** — whether bounce classification is present on the event payload or requires a
contact read, and whether removal from a list also suppresses. Confirm, because the difference
decides whether this recipe protects the list or merely tidies it.

---

### Double opt-in verification

**Problem** — "Anyone can type any address into our form, and some of them are typos and some are
other people's."

**Trigger** — inbound form submission.

**Preconditions** — somewhere to hold a pending verification with an expiry. A verification message
that is transactional in tone and content. **A decision that the list-growth cost is worth it** — this
recipe deliberately reduces signups. The code lifetime, the resend cooldown and the rest of the
capture mechanics are specified in
[Email Capture](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/email-capture.md); this recipe wires them to the platform.

**Steps**
1. Receive the submission. Validate the address shape before anything else.
2. Generate a single-use code with an expiry.
3. Store it against the submitted address, pending.
4. Send the verification message — `email_sms.messaging_email`.
5. Wait for the confirmation form.
6. Check the code: correct, unexpired, unused. Wrong code returns to the form with a bounded number
   of retries; expired means start again.
7. **Only on success**, create the contact — a contact write, which has no registered capability yet (see [Capabilities](./how-to-read-a-recipe.md#capabilities)) — and add to the list —
   `email_sms.segmentation`.
8. Record the verification, with its timestamp, as the consent evidence.
9. Expire and discard pending records that were never confirmed.


**Guardrails** — **nothing reaches the marketing list before step 7.** An unverified address that is
created "provisionally" and mailed anyway defeats the recipe entirely. Rate-limit by address and by
origin, or the verification sender becomes a way to mail arbitrary strangers. Bound the retries. The
verification message itself is transactional and must not carry marketing content.

**What to measure** — outcome: verification completion rate, and bounce and complaint rates for
verified contacts against the pre-verification baseline. Guard: **total verified signups**, not
completion rate — a change that lifts completion while halving submissions has lost you subscribers.

**Failure modes** — the verification lands in spam and completion collapses; it is the one message
that most needs to arrive, so check its placement separately. Pending records are never expired and
accumulate indefinitely. The code is guessable.

**Not verified** — whether the platform can hold a pending, unconfirmed contact state natively. If it
can, this recipe is mostly unnecessary. Whether the store *should* require this at all is a policy
decision — see
[consent-verification](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/consent-verification/SKILL.md).
