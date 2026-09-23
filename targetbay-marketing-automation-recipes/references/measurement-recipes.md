# Measurement Recipes

Getting results out of the platform and in front of the people who decide what to do next. These
three are the cheapest recipes in the skill to run and the easiest to skip, which is why most stores
test inconsistently and report by hand.

All recipes below inherit [Guardrails](./guardrails.md), select a pre-built campaign rather than
creating one, and quote the source workflow's intervals rather than recommending them. See
[How to Read a Recipe](./how-to-read-a-recipe.md).

---

### Automated A/B cycle

**Problem** — "We mean to test things and then don't, because splitting the audience and chasing the
numbers afterwards is a job nobody has time for."

**Trigger** — schedule. The source workflow ran weekly.

**Preconditions** — **two pre-built campaign variants that differ in exactly one thing.** An audience
large enough that a difference could be detected at all — this is a precondition, not a detail, and
most stores fail it for most tests. Agreement on the decision rule before the test runs.

**Steps**
1. Read the test audience — `email_sms.segmentation`, or `email_sms.customer_intelligence` filtered.
2. **Check the audience can resolve the difference you are looking for.** If it cannot, stop here and
   report that: running the test anyway produces a number that means nothing and a decision made on
   noise.
3. Split randomly. Random, not by any attribute that correlates with the outcome.
4. Send variant A to one half and variant B to the other — `email_sms.messaging_email` twice.
5. Wait. The source workflow waited twenty-four hours — long enough that late openers are not
   systematically excluded.
6. Read both results — `email_sms.campaign_analytics`.
7. Apply the decision rule agreed at step 0. **"No detectable difference" is a result**, and the
   correct action is to keep the simpler variant.
8. Log the test, the variants, the numbers and the decision.
9. Report to the team.


**Guardrails** — one variable per test. Two changes at once produce a winner and no knowledge of why.
Do not stop early because a variant looks ahead — early leads reverse routinely, and a rule that
allows stopping on a glance is not a rule. Both variants spend from the same frequency budget: an
automated weekly test is an automated weekly send.

**What to measure** — outcome: the metric the test was designed around, chosen before the send. Guard:
unsubscribe and complaint rate per variant — a subject line that wins on opens and loses on
complaints has not won.

**Failure modes** — the audience is too small and the cycle produces a confident winner every week
from noise; step 2 is the only defence. Reports are not final at step 6 and the decision is made on
partial data. The split is not actually random.

**Not verified** — whether report data is complete at the point of reading, and whether the platform
offers native split-testing that would make this recipe unnecessary. Test design — what to test, how
long, what rule — belongs to
[ab-testing](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/ab-testing/SKILL.md).

---

### Periodic KPI summary

**Problem** — "Someone spends half a day each month assembling the same report by hand."

**Trigger** — schedule. The source workflow ran on the first of the month.

**Preconditions** — agreement on which metrics matter, reached before the recipe is built. A
recipient list that wants it.

**Steps**
1. Read the campaigns in the period — `email_sms.campaign_management`.
2. Read each campaign's results — `email_sms.campaign_analytics`.
3. Aggregate. State the denominator for every rate; a rate without its base is unreadable.
4. **Compare against the previous period, and against the same period last year** where seasonality
   matters. A number alone says nothing.
5. Render the report.
6. Send — `email_sms.messaging_email` to an internal list.
7. Store the period's figures for the next run's comparison.


**Guardrails** — report what the data supports and label what is missing rather than omitting it
silently — a metric that quietly disappears in a bad month is worse than an absent one. Do not
present a partial period as complete. This recipe reports; it does not recommend.

**What to measure** — outcome: whether the report changed a decision. Guard: whether anyone opens it.

**Failure modes** — a campaign sent late in the period has incomplete results and drags the averages
down every month. Paging stops early and the summary silently covers part of the period.

**Not verified** — whether report fields are consistent across campaign types, and whether revenue
attribution is present. Interpreting *why* the numbers moved belongs to
[revenue-analysis](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/revenue-analysis/SKILL.md).

---

### Campaign event capture

**Problem** — "Our email results live in one place and everything else about the business lives
somewhere else, so nobody can join them up."

**Trigger** — platform event for live capture, or a schedule for periodic export.

**Preconditions** — a destination that can accept the volume. A key that joins a campaign result to
whatever the destination holds — usually contact email or an internal id.

**Steps**
1. Receive the event, or read the campaigns for the period — `email_sms.campaign_management`.
2. Read results — `email_sms.campaign_analytics`.
3. Transform to the destination's shape. Keep the platform's own identifiers; they are how a
   discrepancy gets traced later.
4. Write to the destination, **keyed so that a re-run overwrites rather than appends**.
5. Record the watermark so the next run knows where it stopped.


**Guardrails** — idempotent writes. An append-only export that re-runs will double-count, and the
double-count will be discovered in a board report. Do not export more personal data than the
destination needs; an analytics sheet rarely needs full contact records.

**What to measure** — outcome: whether a question got answered that could not be answered before.
Guard: freshness — an export that silently stops is worse than no export, because people keep
trusting it.

**Failure modes** — the destination rate-limits and rows are dropped without error. Results change
after export as late events arrive, so the warehouse and the platform disagree; re-export a trailing
window rather than only new rows.

**Not verified** — whether report figures are final at any defined point, which decides how far back
the trailing window has to go.
