---
name: surface-inventory
description: Use when the question is what onsite personalization currently exists and what it is doing — which surfaces carry placements, offers or search configuration, what each one is worth, where attention is being spent for nothing, and which surfaces host a decision but carry no help. This is the assessment skill every other personalization skill routes through.
license: MIT
metadata:
  targetbay.display_name: Surface Inventory
  targetbay.version: "1.0.0"
  targetbay.category: personalization
  targetbay.requires: onsite.store_profile, onsite.consent_and_tracking, onsite.recommendation_placement, onsite.recommendation_analytics, onsite.offers, onsite.offer_analytics, onsite.experience_analytics, onsite.search
  targetbay.risk_level: analysis
  targetbay.execution_mode: analyze_only
  targetbay.status: foundation
---

# Surface Inventory

## Purpose

Establish what is currently running on the store's surfaces, what each element is doing, and where
attention is being spent without return.

Every other skill in this plugin needs the same foundation: the map of surfaces, what occupies them, and
what consent permits. Deriving it once, here, stops five skills from proposing additions to pages that are
already crowded ([../../rules/global-rules.md#G6](../../rules/global-rules.md)).

## When to Use

- Taking over a personalization setup somebody else built
- Before adding any placement, offer or targeting scheme
- A page converts badly and its onsite elements are a candidate explanation
- Nobody can say what is currently personalised
- Auditing what consent actually permits here

## When Not to Use

- The question is which recommendation strategy belongs where. Use
  [recommendation-strategy](../recommendation-strategy/SKILL.md).
- The question is who should see which offer. Use
  [offer-targeting](../offer-targeting/SKILL.md).
- The question is about search queries specifically. Use
  [onsite-search](../onsite-search/SKILL.md).
- The whole setup needs ranking by what to fix first. Use
  [personalization-audit](../personalization-audit/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Consent and tracking state | Decides what is permissible before anything else | Blocked |
| Current placements and their configuration | The inventory itself | Blocked |
| Current offers, their targeting and frequency | The other half of the inventory | Blocked |
| Per-element performance | What each is worth | Partial; value unassessable |
| Page and funnel performance | The baseline each element sits inside | Partial |
| Search configuration | Search is a surface and is usually unexamined | Partial |
| Traffic composition, anonymous versus identified | What proportion any personalised path reaches | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `onsite.consent_and_tracking` | What may be collected or acted on, and for which traffic |
| `onsite.store_profile` | Catalogue size, traffic volume, vertical |
| `onsite.recommendation_placement` | Which placements exist, on which surfaces, with which strategy |
| `onsite.recommendation_analytics` | Per-placement impressions, clicks, attributed revenue |
| `onsite.offers` | Which offers run, with what targeting and frequency |
| `onsite.offer_analytics` | Per-offer engagement, dismissal and conversion |
| `onsite.experience_analytics` | Page and funnel baselines the elements sit inside |
| `onsite.search` | Search configuration as a surface in the inventory |

## Inputs

| Input | Required | Notes |
|---|---|---|
| `scope` | no | A template, surface set or funnel stage |
| `period` | no | Window for performance comparison |
| `objective` | no | Pre-change audit, cleanup, consent review |
| `constraints` | no | Surfaces excluded from analysis |

## Decision Process

```
1. Read consent state first                   ← it bounds everything after it
2. Enumerate every element on every surface
3. Name the decision each surface hosts
4. Attach performance to each element
5. Measure attention cost against outcome
6. Find surfaces hosting a decision with no help
7. Find elements earning nothing
8. Report the traffic split, anonymous versus identified
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/surface-rules.md](../../rules/surface-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

- Read consent before anything else (G5, [#S2](../../rules/safety-rules.md)). The inventory states what is
  currently permissible, not only what is currently configured — those can differ, and where they do it is
  the most important finding on the page.
- Name the decision every surface hosts (U1). A placement sitting in front of no decision is reported as
  decoration regardless of its engagement numbers.
- Evaluate elements on outcome, never on impressions (U7, G1). An element with high engagement and no
  conversion effect is a candidate for removal, not for expansion.
- Report the anonymous share of traffic explicitly (G12). An elaborate identified-visitor experience
  reaching a small minority is a finding.
- State attribution limits wherever attributed revenue is reported (G4). Revenue flowing through a
  placement is not revenue caused by it.
- Report empty surfaces — pages hosting a real decision with nothing helping — alongside crowded ones. Both
  are inventory findings.
- Report what is working. An inventory that lists only problems cannot be checked for completeness.
- Never propose changes here. This skill is `analyze_only`; the acting skills compose it.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read consent, placements, offers, search, performance | `read_only` |
| ANALYZE | Map surfaces to decisions, attach outcomes, find gaps and waste | `analysis` |
| PLAN | Rank findings by attention cost against outcome | `analysis` |
| PREVIEW | Present the inventory with its evidence and its confidence | `analysis` |
| VALIDATE | Run the checks below | — |
| MEASURE | Re-inventory after changes have run a full comparison window | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: consent state and what it permits, a
surface-by-surface inventory naming the decision each hosts and the elements on it, per-element outcome
performance with its attribution limits, surfaces hosting a decision with no help, elements earning
nothing, and the anonymous-versus-identified traffic split.

Plus: what is working, and anything that could not be assessed.

No recommendations to act are produced here — the acting skills compose this one.

## Validation

- [ ] Consent state read first, and what it permits stated (G5, S2)
- [ ] Every surface's hosted decision named, or the surface reported as decoration (U1)
- [ ] Every element assessed on outcome, not impressions (U7, G1)
- [ ] Attribution limits stated wherever attributed revenue appears (G4)
- [ ] Anonymous traffic share reported explicitly (G12)
- [ ] Surfaces with a decision and no help reported, not only crowded ones
- [ ] Working elements reported as working
- [ ] No change proposed from this skill
- [ ] Anything unassessable recorded in `unmet_requirements` (G15)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |

This skill changes nothing and therefore requires no approval. Every action it implies is owned by a
composing skill, which carries its own approval requirements.

## Examples

**"What personalization do we actually have running?"**
Finds eleven elements across four templates, of which three are on surfaces that host no decision and two
duplicate each other on the product page. Reports that the product page's strongest element by attributed
revenue also cannibalises the one below it, so the attribution is not incremental. Notes that the cart
page — which hosts the clearest completion decision in the funnel — carries nothing at all.

**"We turned on personalization in the EU and nothing seems to happen."**
Consent state shows most EU traffic has not granted tracking, so the identified-visitor paths those
elements depend on never resolve. Reports that the configured experience and the permissible experience
differ for the majority of that traffic, and that the anonymous path was never designed — which is the
finding, rather than anything about the elements themselves (G12, T2).

## Failure Handling

| Situation | Response |
|---|---|
| `onsite.consent_and_tracking` unavailable | **Blocked.** What is permissible cannot be established, and an inventory that assumes permission is not usable (S2, G5) |
| `onsite.recommendation_placement` or `onsite.offers` unavailable | **Blocked.** There is no inventory without the elements |
| Per-element analytics unavailable | **Partial.** Report the inventory and the decisions hosted; state that element value is unassessed |
| Page performance unavailable | **Partial.** Elements cannot be compared against a baseline; say so and lower confidence |
| Traffic composition unavailable | **Partial.** Report that the reach of identified-visitor paths is unknown (G12) |
| Attribution method not exposed | Report attributed revenue with its method marked unknown, and do not call any of it incremental (G4, U5) |
| Nothing is configured | Report that, with the surfaces that host decisions and carry nothing. An empty inventory is a valid and useful result |

Degraded outcomes set `status` and populate `unmet_requirements`.
