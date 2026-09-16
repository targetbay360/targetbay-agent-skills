# Skills

A skill teaches an agent how to accomplish a proof objective. It owns the reasoning — which products,
which ask, when, where the proof goes, and when to stop — while the TargetBay Reviews MCP owns the
capabilities that carry it out. See [../docs/mcp-integration.md](../docs/mcp-integration.md).

Five skills, covering collection, rating health, display and programme assessment.

## Proof

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Review Coverage](review-coverage/SKILL.md) | `review-coverage` | `analysis` | 2.0.0 | — |

## Collection

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Review Request Programme](review-request-program/SKILL.md) | `review-request-program` | `plan` | 2.0.0 | `review-coverage` |

## Rating health

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Rating Diagnosis](rating-diagnosis/SKILL.md) | `rating-diagnosis` | `recommendation` | 2.0.0 | `review-coverage` |

## Display and distribution

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Proof Placement](proof-placement/SKILL.md) | `proof-placement` | `recommendation` | 2.0.0 | `review-coverage` |

## Planning

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Review Programme Audit](review-program-audit/SKILL.md) | `review-program-audit` | `recommendation` | 2.0.0 | `review-coverage`, `review-request-program`, `rating-diagnosis`, `proof-placement` |

## Composition graph

```
review-program-audit
  ├─▶ review-request-program ─┐
  ├─▶ rating-diagnosis ───────┤
  ├─▶ proof-placement ────────┤
  └─▶ review-coverage ◀───────┘
```

`review-coverage` sits at the bottom. Every question of the form "which products need proof" routes
through one implementation, so the answer does not drift between skills
([../rules/global-rules.md#G5](../rules/global-rules.md)).

The graph is validated acyclic. Composition is conceptual — a composing skill defers a decision to
another skill's reasoning; it is not a function call, and this package defines no runtime.

## Choosing between them

| The question | The skill |
|---|---|
| Which products are short of proof? | `review-coverage` |
| How do we get more reviews? | `review-request-program` |
| Why did our rating drop, and what do we say? | `rating-diagnosis` |
| We have reviews — why isn't anything changing? | `proof-placement` |
| Where do we even start? | `review-program-audit` |

## Adding a skill

A new skill must decide something none of the existing five decides. If it would mostly restate one of
them with a different scope, extend that skill instead.

Follow the contract every skill here conforms to: the thirteen sections in order, `targetbay.*` metadata
under `metadata`, capabilities drawn from [../capabilities.yaml](../capabilities.yaml), rules cited by
number rather than restated, and a golden prompt in
[tests/evals/](https://github.com/targetbay360/targetbay-agent-skills/blob/main/tests/evals/README.md).
