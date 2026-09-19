# Retention and Recovery Recipes

Scheduled sweeps that find customers drifting away and intervene before they are gone, plus the
win-back for the ones already lapsed.

All recipes below inherit [Guardrails](./guardrails.md), select a pre-built campaign rather than
creating one, and quote the source workflow's intervals rather than recommending them. See
[How to Read a Recipe](./how-to-read-a-recipe.md).

All three run on a schedule against the whole contact base, which makes the already-messaged guard
the most important thing in this file. A daily sweep without one mails the same at-risk customer
every day.

---

### Daily churn-risk sweep

**Problem** — "By the time we notice a good customer has stopped buying, they have already gone."

**Trigger** — schedule. The source workflow ran daily.

**Preconditions** — purchase history with enough depth to establish each customer's *own* rhythm. A
retention campaign that offers something other than a discount. Agreement on what "at risk" means for
this store, derived from its own repeat intervals rather than a round number of days.

**Steps**
1. Read the contact base — `contact: list`, paged.
2. Score each contact against **their own** purchase interval, not a store-wide one. A customer who
   buys quarterly is not at risk after five weeks; a customer who buys weekly is.
3. Filter to the at-risk set.
4. Apply the already-messaged guard: drop anyone this recipe touched inside the window.
5. Check suppression, consent and the frequency budget.
6. Send — `campaign: send`.
7. Record the intervention and its date — `event: track`.
8. Alert the team with the day's counts.


**Guardrails** — **the already-messaged guard is the recipe.** Without it a daily schedule mails the
same person daily until they unsubscribe. Score relative to each contact's own pattern; a global
threshold flags every infrequent buyer as churning. Cap the daily volume — a scoring change that
suddenly flags a third of the base should not be able to mail a third of the base.

**What to measure** — outcome: repeat rate of contacts who received the intervention against a
holdout of scored-at-risk contacts who did not. **Without the holdout this recipe cannot be
evaluated at all** — customers who were going to buy anyway will buy, and the recipe will take
credit. Guard: unsubscribe rate among the at-risk set, who are by definition disengaged and quick to
leave.

**Failure modes** — the scoring runs on stale order data and flags people who bought yesterday. A
volume spike after a scoring change; the daily cap is what makes that survivable. The write-back at
step 7 fails after the send, so tomorrow's guard does not see today's message.

**Not verified** — whether order history is reachable at the volume step 1 implies without
unacceptable paging cost. The strategy of who is worth retaining and what to offer belongs to
[customer-retention](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/customer-retention/SKILL.md).

---

### Dormant re-engagement sweep

**Problem** — "A big slice of our list never opens anything and we keep mailing them anyway."

**Trigger** — schedule. The source workflow ran weekly.

**Preconditions** — engagement history long enough to tell dormant from new. A re-engagement campaign
that asks a real question rather than shouting the same offer louder. **A decision, made before
building, about what happens to the people who do not respond** — if the answer is "keep mailing
them", this recipe makes deliverability worse rather than better.

**Steps**
1. Read the contact base — `contact: list`, paged.
2. Identify contacts with no engagement across a window derived from the store's own campaign
   cadence. A store that mails monthly needs a longer window than one that mails daily.
3. Exclude the recently acquired, who have not had a chance to engage.
4. Apply the already-messaged guard.
5. Check suppression and consent.
6. Send — `campaign: send`.
7. Record the attempt — `event: track`.
8. **Mark non-responders for the sunset path.** This is the step that makes the recipe worth running.


**Guardrails** — a bounded number of attempts, agreed up front. Continued sending to a
never-engaging cohort is the thing degrading inbox placement for everyone else on the list, so the
recipe must end in either re-engagement or suppression. Never escalate frequency to a non-responder.

**What to measure** — outcome: re-engagement rate, and how much of it survives the following month —
a single open under a re-engagement subject line is not recovery. Guard: complaint rate, which runs
high in this cohort because many of them forgot signing up.

**Failure modes** — the dormancy window is copied from another store and flags healthy infrequent
buyers. Non-responders are marked but nothing consumes the mark, so the list never actually improves.

**Not verified** — whether per-contact engagement recency is available directly or must be assembled
from campaign reports. Who to suppress and when belongs to
[list-hygiene](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/list-hygiene/SKILL.md);
whether a lapsed buyer is worth recovering at all belongs to
[customer-winback](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/customer-winback/SKILL.md).

---

### Win-back with an already-offered guard

**Problem** — "We have a list of customers who stopped buying and no systematic way of approaching
them — and when we do, some get asked twice."

**Trigger** — schedule. The source workflow ran daily.

**Preconditions** — a lapsed set that has been checked for whether it is worth recovering at all.
**A durable record of who has already received a win-back offer** — this recipe's source workflow
kept it in a spreadsheet, and the record is more important than the generation logic. A pre-approved
offer set with margin bounds.

**Steps**
1. Read the lapsed set — `contact: list`, paged, or from a maintained list.
2. Filter to the eligible: lapsed beyond the store's own repeat interval, **and not already offered**.
3. If nothing is eligible, log that and stop. A quiet day is a result, not a failure.
4. For each eligible contact, select an offer from the approved set within margin bounds.
5. Check suppression, consent and the frequency budget.
6. Send — `campaign: send`.
7. **Record the offer against the contact before moving on** — this is what step 2 reads tomorrow.
8. Log the run, including the contacts found ineligible and why.


**Guardrails** — **the already-offered filter and the write-back at step 7 are a pair; one without
the other is worse than neither.** If the write-back can fail after a successful send, record the
intent before sending so the failure mode is a missed offer rather than a repeated one. Bound the
discount depth: a win-back is where margin discipline erodes fastest, because the customer is already
lost and any revenue looks like a win.

**What to measure** — outcome: reactivation rate against a holdout of eligible contacts who were not
offered. Guard: margin on reactivated orders, and whether reactivated customers buy a second time —
a win-back that buys one discounted order and no loyalty has cost money.

**Failure modes** — the offer record and the send fall out of step, producing repeat offers to the
same person. The eligible set is empty every day because the filter is too tight, and nobody notices
because a quiet day looks like a healthy day; alert on a run of zero-eligible days.

**Not verified** — whether the offer record can live on the contact as a custom field or needs
external storage. If a model generates the offer rather than selecting from the set, the approval gate
in [AI-Assisted Recipes](./ai-assisted-recipes.md) applies.
