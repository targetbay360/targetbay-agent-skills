# Trace: "Prepare a Diwali campaign."

> Illustrative. Figures are placeholders standing in for capability output, not real store data. The
> package ships no holiday calendar — dates and relevance come from store context and store data.

## Prompt

```
Prepare a Diwali campaign.
```

## Skill selection

[holiday-marketing](../skills/holiday-marketing/SKILL.md) first — relevance and posture must be decided
before a sequence is designed. It composes
[holiday-drip-campaign](../skills/holiday-drip-campaign/SKILL.md) once participation is confirmed, which
in turn composes [audience-discovery](../skills/audience-discovery/SKILL.md).

Going straight to the sequence would design an arc for a holiday that may not warrant one.

## Stage 1 — holiday-marketing

### DISCOVER

`email_sms.order_intelligence` for prior-period revenue around the date; `email_sms.product_intelligence`
for catalogue fit; `email_sms.customer_intelligence` for audience locale;
`email_sms.marketing_calendar` for surrounding commitments; `email_sms.campaign_analytics` for last
year's results.

### Decisions

**Relevance confirmed from data, not from the date existing.** *(illustrative)* Prior-period revenue shows
a consistent lift across a roughly three-week interest window, concentrated in the final days. Two
catalogue categories are genuinely relevant. A substantial share of the audience is in markets that
observe the holiday.

Had any of those failed, the correct output would have been **do not participate**, with the reasoning
recorded — see [holiday-marketing](../skills/holiday-marketing/SKILL.md).

**Posture decided here, before the sequence.** Moderate discount depth reserved for the promotion phase;
early phases lead on relevance and product discovery (C4). Deciding this first is what stops the sequence
escalating by default.

## Stage 2 — holiday-drip-campaign

### ANALYZE

*(illustrative)*

- Interest window: ~3 weeks; revenue concentrated in the final 4–5 days
- Delivery cut-off is a real, known date — so urgency has something true to say (N3)
- List has cadence headroom in the build-up, less in the final week where automations are already active
- Stock is deep in one relevant category, thin in the other
- The VIP audience is too small to justify a separate arc

### Deriving the stage count

| Factor | Effect on the count |
|---|---|
| Three-week window | ↑ |
| Revenue concentrated near the deadline | ↑ density at the end, not overall length |
| Two relevant categories, one thin on stock | ↓ — less genuinely different content |
| Cadence headroom in build-up, limited at the end | ↔ |
| Prior-year evidence available | ↑ confidence, not length |
| No exclusivity mechanic, small VIP audience | ↓ |

**Result: five stages.** Stated with the derivation, not as a template
([holiday-drip-campaign](../skills/holiday-drip-campaign/SKILL.md)).

### The arc

| Stage | Timing | Channel | Purpose |
|---|---|---|---|
| `awareness` | Start of window | Email | Occasion relevance; what the store has for it |
| `product discovery` | Mid-window | Email | The two relevant categories, affinity-personalised |
| `promotion` | Sale opens | Email | The offer, at the decided depth |
| `urgency` | 2 days before delivery cut-off | SMS | One real deadline, one link |
| `post-event` | After the period | Email | Retention handover for first-time buyers |

**Rejected stages, recorded:** `teaser` (nothing to tease that discovery does not cover), `early access`
(no exclusivity mechanic, VIP audience below usable size), `last chance` (would duplicate `urgency`
against a single cut-off date).

### Decisions

**Purchasers exit at `promotion`.** Someone who buys on day one must not receive last-chance urgency on
day six. This is the sequence's most visible failure mode and is designed out rather than caught later.

**SMS carries only `urgency`.** It is the one stage where immediacy is the entire value, and the cost
clears the bar ([knowledge/sms-principles.md](../knowledge/sms-principles.md), R14). Consent is checked
per contact; contacts without SMS consent receive an email equivalent.

**Post-event is not optional.** The period produces a cohort of first-time buyers, and the handover into
retention is where their value is won or lost
([knowledge/customer-lifecycle.md](../knowledge/customer-lifecycle.md)).

**Recovery window after the period.** Reduced contact for the same audience before the next push (F12).

## Output

A [workflow](../schemas/workflow.schema.json) of type `drip` with five stages, each carrying audience,
size, exclusions, channel, offer, content direction and expected outcome — plus the stage-count
derivation, the rejected stages, the cadence summary, the recovery window, and dependencies on stock and
the delivery cut-off.

## Approval

Drafts are `mutation`. **Each stage's send is `high_impact` and approved individually** (S2, S9), with the
SMS stage stating recipient count and cost. Staged approval is preferred: approve the first two, measure,
then decide the rest.

## What the skill refused to do

- Produce a fixed-length sequence regardless of the store's situation
- Include `teaser` and `early access` for symmetry when neither had anything to say
- Invent a delivery cut-off date — the urgency stage exists only because a real one is known (N3)
- Promise availability on the thin-stock category (P9)
- Duplicate the `urgency` message on both channels at once
