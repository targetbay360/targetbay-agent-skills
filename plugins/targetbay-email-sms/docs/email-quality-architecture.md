# Email Quality Architecture

How the skills added in 4.2.0 fit together, and why the quality gate owns a verdict rather than the
reasoning behind it.

## The shape

```
                     email-quality-auditor
                     one verdict: PASS / WARN / BLOCK
                              │
        ┌─────────────────────┼─────────────────────┬─────────────────────┐
        │                     │                     │                     │
  deliverability-qa     email-render-qa   dynamic-content-        audience-discovery
  is the programme      is the message    personalizer            is this the right
  fit to send?          readable?         does each variable      audience, and how
        │                                 element resolve?        many people?
   list-hygiene                                 │
   who leaves the                     product-recommendation-strategy
   population?                        which items, on what evidence?
```

Each box below the top one is a complete skill that runs on its own. The auditor composes them; it
does not reimplement them. That is the whole design decision, and it is worth stating why.

## Why the gate owns no reasoning

A pre-send check has an obvious and wrong implementation: one skill that knows how to check
everything. It fails in two directions at once.

It **drifts**. The rendering check inside the auditor and the rendering skill beside it diverge within
two releases, and nobody notices because both look reasonable. This is the same failure that put rules
in `rules/` rather than inside each skill.

It **cannot be used alone**. A store that wants its sending programme diagnosed without a campaign in
hand, or one message's rendering checked without a full audit, has no entry point. Every dimension has
to be independently callable, which means it has to be an independent skill.

So the auditor owns exactly one thing: the verdict. It resolves the audience, runs the stop
conditions, delegates each dimension, classifies the findings, and derives a verdict from them. Where a
composed skill returns `blocked`, the auditor propagates that as an unchecked dimension with the
reason attached rather than substituting a judgement of its own.

## Why the verdict is not a score

The obvious alternative is a weighted score with a pass threshold. It was rejected.

A score lets a real defect be offset by unrelated strengths. A campaign with a broken opt-out and
excellent everything else scores well, and the number is what people look at. A verdict derived from
findings cannot do that: a stop condition is a stop regardless of what else is true.

The consequence is that **BLOCK is narrow**. Four conditions, all of them restatements of things
`rules/safety-rules.md` and `rules/content-rules.md` already forbid — a broken or bypassed opt-out,
suppression or consent the send would override, an audience whose consent cannot be evidenced, and a
claim the store cannot support. Everything else is WARN with its cost stated, and the store decides. A
gate that blocks on preference is a gate people learn to route around, and a routed-around gate
catches nothing.

## The three layers, and who owns which

The diagnostic order in
[../knowledge/deliverability-principles.md](../knowledge/deliverability-principles.md) maps onto
skills directly:

| Layer | Changes | Owner |
|---|---|---|
| Identity — does the sender verify and align? | The store, in its DNS | [deliverability-qa](../skills/deliverability-qa/SKILL.md) |
| Reputation — what have recipients done with this mail? | The programme, through audience and cadence | [deliverability-qa](../skills/deliverability-qa/SKILL.md), delegating the population half to [list-hygiene](../skills/list-hygiene/SKILL.md) |
| Content — the message itself | The campaign | [content-optimization](../skills/content-optimization/SKILL.md), with the built artefact checked by [email-render-qa](../skills/email-render-qa/SKILL.md) |

Diagnosing the wrong layer is the expensive failure this split exists to prevent, and
[../rules/deliverability-rules.md#D1](../rules/deliverability-rules.md) makes the order binding rather
than advisory.

## What the package cannot see

Inbox placement. Delivery means the receiving server accepted the message; opens and clicks come only
from people who found it. No capability in [../capabilities.yaml](../capabilities.yaml) returns
mailbox-side evidence, and none was invented to make a skill look complete.

So [../rules/deliverability-rules.md#D7](../rules/deliverability-rules.md) holds: placement is stated
as unknown, and what the skills reason from instead is engagement, bounce and complaint movement
**split by receiving domain**, labelled as proxies. A collapse at one provider while the others hold
steady is the closest thing sending data contains to a placement signal, and it is still an inference.

## The future integration point

If a placement feed becomes available — seed accounts, a provider postmaster feed, or a third-party
monitor such as InboxEagle — it enters here, and only here:

1. **A new capability** in [../capabilities.yaml](../capabilities.yaml), something like
   `email_sms.inbox_placement`, with `access: read` and a `notes` block naming what it actually
   measures. Seed-list placement and panel-based placement are different claims and should not share
   an identifier.
2. **`deliverability-qa` gains it in `requires`**, and its `Failure Handling` row for "no placement
   signal of any kind" changes from *expected* to *partial*. Its Decision Process gains a step between
   reputation and the remedy split.
3. **`list-hygiene` does not change.** Placement tells you there is a problem; it does not tell you
   which contacts leave the population, which is still a value-and-engagement decision.
4. **`email-quality-auditor` gains a dimension**, not a stop condition. Poor placement is a cost the
   store may knowingly accept; it is not in the same class as a broken opt-out.
5. **`deliverability-rules.md#D7` is rewritten rather than deleted.** The rule against *inferring*
   placement from sending data still holds for every store that does not have the feed.

No separate plugin is created for this. A placement monitor is a data source for skills that already
exist, not a product surface of its own — and a skill that cannot run without a capability nobody has
confirmed is a skill that should not ship. That is why `inbox-placement-monitor` was rejected rather
than written and left degraded.

## Related

- [architecture.md](architecture.md) — the package-wide layering, risk model and execution lifecycle
- [../knowledge/deliverability-principles.md](../knowledge/deliverability-principles.md) — the three-layer model in full
- [../rules/deliverability-rules.md](../rules/deliverability-rules.md) — D1..D10
