# AI-Assisted Recipes

Patterns where a model drafts something. The generation is the easy part and the least important
part; the approval gate is what decides whether these are safe to run.

**Read the approval gate first.** Every recipe below depends on it, and a generation pipeline without
one will eventually send a customer a claim about a product that is not true.

All recipes below inherit [Guardrails](./guardrails.md), select a pre-built campaign rather than
creating one, and quote the source workflow's intervals rather than recommending them. See
[How to Read a Recipe](./how-to-read-a-recipe.md).

The missing campaign-create operation constrains this group more than any other: the
"generate content, create a campaign, send it" shape cannot run at all.

Which message classes may ship unreviewed is a policy decision, not a wiring one. See
[ai-content-governance](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/ai-content-governance/SKILL.md).

---

### The approval gate with a correction pass

**Problem** — "We want a model to draft our sends, but we are not letting it mail customers
unsupervised."

**Trigger** — any recipe that generates customer-facing content.

**Preconditions** — a named reviewer and a channel they actually watch. A definition of what the
reviewer is checking, in order. A rejection path that does something useful.

**Steps**
1. Generate the draft.
2. Present it to the reviewer **whole** — the subject, the body, every claim, every price, the
   audience it will go to and its size. A gate that shows a summary is not a gate.
3. Block. This is a blocking step with an explicit approve or reject, not a notification that expires
   into approval.
4. On approve: proceed to the send path, which still runs its own suppression, consent and frequency
   checks. Approval of content is not approval to bypass the guardrails.
5. **On reject: capture the reason and run a correction pass**, then return to step 2. The reviewer's
   objection is the most valuable input the pipeline gets; discarding it makes the next draft no
   better.
6. Bound the correction attempts. After the bound, escalate to a person writing it — not another
   attempt.
7. Log the draft, the decision, the reason and who decided.

**Guardrails** — a failed generation sends nothing
([content-rules.md#N13](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/rules/content-rules.md)),
and no timeout auto-approves
([safety-rules.md#S13](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/rules/safety-rules.md)).
**What the reviewer checks, and in what order, is set per store by
[ai-content-governance](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/ai-content-governance/SKILL.md)** —
this recipe carries the gate, not the checklist.

**What to measure** — outcome: approval rate on first pass, which tells you whether the generation is
good enough to be worth the reviewer's time. Guard: **time spent reviewing**. A gate that costs more
than writing the message has removed the reason for the recipe.

**Failure modes** — the reviewer is unavailable and sends stall; decide in advance whether stalling
or a named deputy is right, and never auto-approve. Approval fatigue turns the gate into a rubber
stamp — a rising approval rate with a falling review time is the signal.

**Not verified** — nothing platform-side; this is an orchestrator pattern.

---

### Newsletter assembly from sources

**Problem** — "A curated newsletter is a good idea that dies after three issues because assembling it
is manual."

**Trigger** — schedule. Source workflows ran daily, weekly and on fixed slots.

**Preconditions** — sources worth curating. A newsletter campaign in the interface whose
personalisation can carry the assembled content. **The approval gate above.**

**Steps**
1. On the ingest schedule, collect from the sources and store them with their dates.
2. On the send schedule, select the period's items. **Attribute every item to its source and link
   out.** A newsletter that reproduces other people's work without attribution is a legal problem as
   well as a discourteous one.
3. Generate only the connective material — the intro, the section framing. The items themselves are
   quoted and linked, not rewritten.
4. **Approval gate.**
5. Read the recipients — `contact: list`, or `list: get`.
6. Check suppression and the frequency budget. Send — `campaign: send`.
7. Record — `event: track`.


**Guardrails** — generate the framing, not the facts. The narrower the generated surface, the less
there is to get wrong. An empty period sends nothing rather than padding. Content about the store's
own products carries a price or a claim and needs the strictest review.

**What to measure** — outcome: click-through to sources, which is what a curated newsletter is for.
Guard: unsubscribe rate per issue, which rises quickly when the curation slips.

**Failure modes** — a source stops publishing and the issue is thin; check volume before assembling.
Duplicate items across issues because the watermark is not stored.

**Not verified** — whether campaign personalisation can carry a full assembled body, which is the
constraint the missing campaign-create operation imposes. If it cannot, the newsletter must be built
in the interface per issue and this recipe reduces to assembling a draft for a human to paste.

---

### Machine-proposed segments

**Problem** — "Our segments are the three someone defined two years ago."

**Trigger** — schedule. The source workflow ran daily, which is far more often than segment
definitions should change.

**Preconditions** — **a human review step before any proposed cluster becomes a list.** Contact data
rich enough to cluster meaningfully.

**Steps**
1. Read the contact base — `contact: list`, paged.
2. Prepare the attributes the clustering may use. **Exclude sensitive attributes, and attributes that
   proxy for them** — this exclusion belongs at step 2, before the model sees the data, not as a
   filter on the output.
3. Propose clusters.
4. **Stop for review.** A proposed cluster is a hypothesis, not a segment: it needs a name a person
   understands, a reason to be treated differently from its neighbours, and a size worth acting on.
   Review also checks it has not reconstructed a sensitive attribute from proxies.
5. On approval, create the list — `list: create`.
6. Add members — `list: addContact`.
7. Record — `event: track`.


**Guardrails** — **clusters do not become lists without review**, and the tests a proposal must pass
to become an audience are owned by
[audience-discovery](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/audience-discovery/SKILL.md).
Sensitive attributes and their proxies are excluded before clustering, not filtered after. Do not
re-cluster daily: definitions that move constantly cannot be reported against, and a slower cadence
loses nothing.

**What to measure** — outcome: performance of campaigns to an approved cluster against the existing
segmentation. Guard: how many proposals are rejected at review — a high rate means the clustering is
not earning its cost.

**Failure modes** — daily re-clustering produces a different segmentation each morning and no
comparable reporting. Lists accumulate from every run; delete or reuse rather than creating new ones.
Note that the platform has **no segment resource** — every segment here is a list, and lists are
cheap to create and easy to leave lying around.

**Not verified** — whether membership can be replaced in bulk on an existing list, which decides
whether refreshes are cheap or require rebuilding.

---

### Generated campaign, end to end

**Problem** — "We want the whole weekly send produced automatically."

**Trigger** — schedule. The source workflow ran weekly.

**This recipe carries the strongest caveat in the skill.** It is included because it is what people
ask for, and because the constraints on it are worth stating plainly rather than leaving someone to
discover them.

**Preconditions** — everything the other three need, plus a tolerance for the gap below.

**Steps**
1. Read the audience — `contact: list` or `list: get`.
2. Profile the audience, so the draft is written against who is actually on the list today.
3. Generate the draft.
4. **Approval gate**, at full strictness. This send carries products, prices and offers.
5. On approval, select the campaign the approved content was built into — `campaign: get`.
6. Check suppression and the frequency budget. Send — `campaign: send`.
7. Record — `event: track`.


**Guardrails** — the approval gate is not optional here and cannot be reduced to a notification. The
generated copy may not assert a price, a stock position or a product claim that was not supplied to
it as data. There is no fallback send.

**What to measure** — outcome: performance against the store's own previous sends. Guard: first-pass
approval rate and review time together — if the reviewer rewrites most drafts, the recipe costs more
than writing the email.

**Failure modes** — the audience profile is stale and the copy addresses a list that no longer
exists. Approval fatigue.

**Not verified** — **the important one.** The obvious shape for this pattern creates a campaign
programmatically, and the platform surface has no campaign-create operation, so it cannot run as
written. Step 5 selects a campaign built in the interface instead — which means the "fully
automated" version does not exist against this surface, and the human is in the loop by construction
whether or not you wanted them there. Given step 4, that is not a loss.
