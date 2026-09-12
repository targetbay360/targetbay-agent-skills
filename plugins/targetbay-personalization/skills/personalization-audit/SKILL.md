---
name: personalization-audit
description: Use for an open-ended assessment of a store's whole onsite experience — when someone asks what is wrong with our site, where to start with personalization, what to fix first, or wants a review without naming a specific problem. Scans surfaces, recommendations, offers, search and measurement together and ranks what is most worth fixing.
license: MIT
metadata:
  targetbay.display_name: Personalization Audit
  targetbay.version: "1.0.0"
  targetbay.category: planning
  targetbay.requires: onsite.store_profile, onsite.consent_and_tracking, onsite.recommendation_placement, onsite.recommendation_analytics, onsite.offers, onsite.offer_analytics, onsite.search, onsite.experimentation, onsite.experience_analytics, onsite.visitor_intelligence
  targetbay.composes: surface-inventory, recommendation-strategy, offer-targeting, onsite-search, experience-experimentation
  targetbay.risk_level: recommendation
  targetbay.execution_mode: recommend_only
  targetbay.status: foundation
---

# Personalization Audit

## Purpose

Look at the whole onsite experience — surfaces, recommendations, offers, search, measurement and consent —
and say what is most worth fixing first.

The five other skills each answer one question well. This skill exists for the case where nobody knows
which question to ask, and its job is to find out rather than to default to adding personalization.

## When to Use

- Open-ended: "what's wrong with our site", "where do we start"
- Taking over a personalization setup somebody else built
- Periodic health check
- An onsite investment is being considered and its priority is unclear
- Several problems are suspected and their relative size is unknown

## When Not to Use

- The problem is already identified. Go straight to the owning skill:
  [surface-inventory](../surface-inventory/SKILL.md),
  [recommendation-strategy](../recommendation-strategy/SKILL.md),
  [offer-targeting](../offer-targeting/SKILL.md),
  [onsite-search](../onsite-search/SKILL.md) or
  [experience-experimentation](../experience-experimentation/SKILL.md).
- Something needs building or publishing. This skill recommends; it never executes.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Consent and tracking state | Bounds what any recommendation could be | Blocked |
| Surface inventory | What exists and what it is doing | Blocked |
| Per-element performance | Which elements earn their attention | Partial |
| Search query health | Search is usually the least examined surface | Partial |
| Funnel performance | Where visitors actually drop | Partial |
| Experiment history and discipline | Whether past decisions were proved or asserted | Partial |
| Traffic composition | Whether personalised paths reach anyone | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `onsite.consent_and_tracking` | The precondition dimension |
| `onsite.store_profile` | Traffic volume, catalogue size, vertical |
| `onsite.recommendation_placement` / `onsite.recommendation_analytics` | Recommendation dimension |
| `onsite.offers` / `onsite.offer_analytics` | Offer and interruption dimension |
| `onsite.search` | Discovery dimension |
| `onsite.experimentation` | Measurement discipline dimension |
| `onsite.experience_analytics` | Funnel dimension and baselines |
| `onsite.visitor_intelligence` | Traffic composition and session signal availability |

## Inputs

| Input | Required | Notes |
|---|---|---|
| `scope` | no | Limits the audit to a template set or funnel stage |
| `period` | no | Window for performance comparison |
| `objective` | no | Biases ranking toward conversion, AOV or risk reduction |
| `constraints` | no | Effort ceiling, surfaces out of bounds |

## Decision Process

```
1. Read consent first                          ← it bounds every recommendation below
2. Assess each dimension independently         ← surfaces, recommendations, offers, search, measurement
3. Locate the funnel's largest drop
4. Find the binding constraint                 ← which dimension caps the value of fixing the others
5. Size each gap in outcome terms
6. Rank by value against effort
7. Route each finding to its owning skill
8. State what is healthy and needs nothing
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md), and every domain rule file through
the skills this one composes.

- Read consent first (G5, [#S2](../../rules/safety-rules.md)). A ranked plan built on profiling that is not
  permitted here has to be rewritten from the top.
- Find the binding constraint before ranking. Adding recommendations to a site whose largest funnel drop is
  at delivery cost moves nothing.
- Do not default to "add personalization." Removing an element that costs attention and earns nothing is
  frequently the highest-value finding, and it is the one least often proposed
  ([../../rules/global-rules.md#G7](../../rules/global-rules.md)).
- Assess measurement discipline as its own dimension. A store that has never proved an onsite change does
  not know which of its current elements help, and that is a finding about every other dimension
  ([../../rules/measurement-rules.md#M1](../../rules/measurement-rules.md)).
- Report the anonymous share of traffic, and treat an identified-only experience as a finding (G12).
- Report healthy dimensions explicitly. An audit that lists only problems cannot be checked for
  completeness, and creates pressure to change what is working.
- Route every finding to the skill that owns it rather than restating that skill's reasoning here (G14).
- Rank by value against effort, and state the evidence for both (G2). Where value cannot be sized, say so
  and rank on reasoning with lower confidence (G15).
- Never recommend an action this skill would execute. `recommend_only` is the ceiling; the owning skills
  carry the approval requirements.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read consent and every dimension's current state | `read_only` |
| ANALYZE | Assess each dimension; locate the funnel drop; find the binding constraint | `analysis` |
| PLAN | Size and rank the findings | `recommendation` |
| PREVIEW | Present the ranked findings with their evidence and owning skills | `recommendation` |
| VALIDATE | Run the checks below | — |
| MEASURE | Re-audit after the top findings have been acted on | `read_only` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: consent state and what it permits, a
per-dimension assessment with its evidence, the binding constraint named explicitly, and a ranked list of
findings.

Each finding states what is wrong, the evidence, the estimated value of fixing it, the effort, the owning
skill, and its dependencies on other findings. Recommendations conform to
[../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json).

Plus: the dimensions assessed as healthy, the anonymous traffic share, and anything that could not be
assessed.

## Validation

- [ ] Consent read first and its implications stated (G5, S2)
- [ ] Every dimension assessed or explicitly reported as unassessable (G15)
- [ ] Binding constraint named, with the reasoning for why it binds
- [ ] Removal considered alongside addition (G7)
- [ ] Measurement discipline assessed as its own dimension (M1)
- [ ] Anonymous traffic share reported (G12)
- [ ] Each finding routed to exactly one owning skill
- [ ] Healthy dimensions reported, not omitted
- [ ] Ranking states value and effort evidence, or declares the confidence is low (G2)
- [ ] No action executed or proposed for execution from this skill

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend and rank | `recommendation` | None |

This skill executes nothing. Every recommendation it makes is carried out by a composed skill under that
skill's own approval requirements.

## Examples

**"Have a look at our site and tell us what to do about personalization."**
Finds eleven onsite elements, of which four earn nothing measurable and two cannibalise each other. The
binding constraint is measurement: nothing has ever been tested, so the store does not know which of its
existing elements help, and adding more would compound the problem. Ranks removal of the four
non-performing elements first, establishing measurement discipline second, and new placements last —
explicitly against the expectation that an audit produces things to add. Reports search as healthy.

**"Our conversion is bad — can personalization fix it?"**
The funnel shows the largest drop is at the delivery-cost step, which no recommendation or offer targeting
addresses. Names that as the binding constraint and states plainly that it sits outside this product.
Ranks the onsite findings below it, and notes that most site traffic has not granted tracking consent, so
any personalised path would reach a minority regardless.

## Failure Handling

| Situation | Response |
|---|---|
| `onsite.consent_and_tracking` unavailable | **Blocked.** Every recommendation depends on what is permissible (S2, G5) |
| Surface inventory unavailable | **Blocked.** Composed skill blocked; there is nothing to audit |
| One or more dimensions unreadable | **Partial.** Audit the rest, name the unassessed dimensions explicitly, and lower the ranking confidence |
| Funnel data unavailable | **Partial.** The binding constraint may sit outside what was measured; say so |
| No experiment history | Report it as the measurement-discipline finding, not as an absence of data |
| Every dimension healthy | Report that, with the evidence. "Nothing is worth changing" is a valid audit result |
| Findings cannot be sized in outcome terms | Rank on reasoning, mark confidence low, and state what data would make sizing possible (G15) |
| The binding constraint sits outside this product | Say so plainly and rank the onsite findings below it |

Degraded outcomes set `status` and populate `unmet_requirements`.
