---
name: opportunity-discovery
description: Use when nobody has named the problem — "what should we be working on?", "where should we focus?", "review our programme", or a sense that something is off with no specific symptom. Runs an open-ended scan across revenue, lifecycle leakage, automation coverage, campaign performance, list health and deliverability, channel mix, cadence, catalogue and content, then ranks whatever is most worth fixing or building next. Use revenue-growth when the objective is already framed as revenue.
license: MIT
metadata:
  targetbay.display_name: Opportunity Discovery
  targetbay.version: "1.1.0"
  targetbay.category: revenue
  targetbay.requires: bayengage.store_profile, bayengage.customer_intelligence, bayengage.order_intelligence, bayengage.product_intelligence, bayengage.segmentation, bayengage.campaign_analytics, bayengage.automation, bayengage.automation_analytics, bayengage.suppression_and_consent, bayengage.marketing_calendar
  targetbay.composes: revenue-analysis, automation-strategy, campaign-optimization
  targetbay.risk_level: recommendation
  targetbay.execution_mode: recommend_only
  targetbay.status: foundation
---

# Opportunity Discovery

## Purpose

Scan the whole programme and report what is most worth doing next, when nobody has said what to look at.

Every other skill in this package answers a framed question. This one exists for the unframed one, and its
discipline is breadth: it must look everywhere before ranking, or it will simply confirm whatever the
operator already suspected.

## When to Use

- "What should we be working on?"
- Periodic programme review
- Inheriting a store and needing to know where it stands
- A sense that something is wrong without a specific symptom
- Before planning a quarter, to check nothing obvious is being missed

## When Not to Use

- The objective is already framed as revenue. Use [revenue-growth](../revenue-growth/SKILL.md).
- A specific thing is known to be broken. Use the skill that owns it.
- A new store with no history. Use [store-onboarding](../store-onboarding/SKILL.md) — there is nothing to
  discover yet.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Revenue history and decomposition | The largest single lens | Blocked |
| Lifecycle distribution and transition rates | Where customers leak | Blocked |
| Automation portfolio and per-journey performance | Coverage gaps and decayed journeys | Blocked |
| Campaign performance history | Underperformers and patterns | Partial |
| List health: engagement, unsubscribes, complaints | Deliverability exposure | Partial; a real blind spot |
| Channel consent and mix | Unused reach, or overused channels | Partial |
| Calendar occupancy and cadence | Fatigue exposure and unused capacity | Partial |
| Catalogue and stock posture | Products with no marketing attached | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `bayengage.store_profile` | Scale and context for what "normal" looks like |
| `bayengage.customer_intelligence` | Lifecycle leaks, value concentration, engagement decay |
| `bayengage.order_intelligence` | Revenue decomposition, intervals, AOV |
| `bayengage.product_intelligence` | Unmarketed products, affinity left unused |
| `bayengage.segmentation` | Sizing every candidate opportunity |
| `bayengage.campaign_analytics` | Underperformance patterns |
| `bayengage.automation` / `bayengage.automation_analytics` | Coverage gaps, decayed journeys |
| `bayengage.suppression_and_consent` | List health, unused consented reach |
| `bayengage.marketing_calendar` | Fatigue and unused capacity |

## Inputs

| Input | Required | Notes |
|---|---|---|
| `period` | no | Observation window; defaults to several repeat intervals |
| `max_findings` | no | Caps what is returned; the full scan still runs |
| `exclude_lenses` | no | Areas already known and being worked on |
| `playbook` | no | Vertical overlay |

## Decision Process

```
Scan every lens before ranking any of them:

  revenue        ← which term is weakest; what changed
  lifecycle      ← which transition leaks most
  automation     ← uncovered transitions; decayed or duplicated journeys
  campaigns      ← persistent underperformance; manual sends simulating triggers
  list health    ← unengaged share, complaint trend, deliverability exposure
  channel        ← consented reach unused; a channel overused
  cadence        ← fatigue exposure, or unused capacity
  catalogue      ← products carrying revenue with no marketing attached
  content        ← systematic weaknesses across messages
        ↓
  size every finding
        ↓
  rank by expected value ÷ effort
        ↓
  assign an owning skill per finding
```

Ranking before scanning is the failure mode. The first plausible finding is rarely the largest.

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../knowledge/marketing-principles.md](../../knowledge/marketing-principles.md).

- Scan every lens, including the ones nobody asked about. Report which lenses could not be scanned.
- Size every finding before ranking it. An interesting finding affecting few customers is not a priority.
- Rank by expected value against effort, and state the criteria (G14).
- Prefer fixing a leak over adding volume. A leaking programme scaled up leaks faster.
- Deliverability and list-health findings outrank most revenue findings, because they suppress everything
  else the store sends.
- Report findings that have no action attached as observations, clearly separated from recommendations.
- Every finding names the skill that owns it. A finding with no owner is not actionable.
- Say what was scanned and found healthy. A report that only lists problems reads as a programme in
  crisis, and hides the fact that most of it works.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read across every capability | `read_only` |
| ANALYZE | Run each lens; size every finding | `analysis` |
| PLAN | Rank, assign owning skills, separate observations from recommendations | `recommendation` |
| PREVIEW | Present findings with evidence and coverage of the scan itself | `recommendation` |
| VALIDATE | Run the checks below | — |

This skill never mutates and never plans execution; `targetbay.execution_mode` is `recommend_only`. Each finding is
handed to its owning skill.

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the lenses scanned and the lenses
skipped with reasons; ranked findings conforming to
[../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json), each with size,
evidence, owning skill, effort and risk; observations without actions, separated; and what was checked and
found healthy.

## Validation

- [ ] Every lens either scanned or reported as unscannable
- [ ] Every finding sized (A1)
- [ ] Every finding carries evidence with period and sample size (G2)
- [ ] Ranking criteria stated (G14)
- [ ] List-health findings weighted above ordinary revenue findings
- [ ] Every finding names an owning skill
- [ ] Observations separated from recommendations
- [ ] Healthy areas reported, not only problems
- [ ] No finding invented to fill a lens (G3)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Report findings | `recommendation` | None |
| Act on any finding | varies | In the owning skill |

## Examples

**"What should we be working on?"**
Scans all nine lenses. Revenue looks stable, which is where a narrower skill would have stopped. List
health shows a large unengaged share and a rising complaint trend — suppressing inbox placement for
everything else the store sends. That ranks first, above a larger-looking but slower revenue opportunity
in automation coverage, because it caps the ceiling on every other finding. Reports campaigns, cadence and
catalogue as healthy.

**"Review our programme before we plan the quarter."**
Finds three items: a decayed automation with an expired offer inside it, a consented SMS audience that has
never been used, and a manual campaign sent monthly that should be a triggered journey. Ranks by effort
against value — the decayed automation is a small fix with immediate effect and goes first.

## Failure Handling

| Situation | Response |
|---|---|
| Several capabilities unavailable | **Partial.** Scan what is reachable and name every lens that could not run |
| New store with no history | Recommend [store-onboarding](../store-onboarding/SKILL.md) instead |
| No findings above the size threshold | Report that plainly. "The programme is sound" is a valid output |
| Everything looks like a finding | Size first; most will fall below the threshold |
| Findings conflict with each other | Report the conflict and rank the one that unblocks the other first |
| Operator disagrees with the ranking | Present the evidence and criteria; re-rank on stated constraints, not on preference |

Degraded outcomes set `status` and populate `unmet_requirements`.
