# Skills

A skill teaches an agent how to accomplish a loyalty objective. It owns the reasoning — whether a
programme is warranted, what a point is worth, which members to intervene with, and when to stop — while
the TargetBay Loyalty MCP owns the capabilities that carry it out. See
[../docs/mcp-integration.md](../docs/mcp-integration.md).

Six skills, covering assessment, design, economics, structure, acquisition and recovery.

## Assessment

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Programme Diagnosis](program-diagnosis/SKILL.md) | `program-diagnosis` | `analysis` | 2.0.0 | — |

## Design

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Programme Design](program-design/SKILL.md) | `program-design` | `plan` | 2.0.0 | `program-diagnosis`, `points-economics`, `tier-structure`, `referral-program` |
| [Tier Structure](tier-structure/SKILL.md) | `tier-structure` | `plan` | 2.0.0 | `program-diagnosis`, `points-economics` |

## Economics

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Points Economics](points-economics/SKILL.md) | `points-economics` | `recommendation` | 2.0.0 | `program-diagnosis` |

## Acquisition

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Referral Programme](referral-program/SKILL.md) | `referral-program` | `plan` | 2.0.0 | `program-diagnosis`, `points-economics` |

## Retention

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Member Recovery](member-recovery/SKILL.md) | `member-recovery` | `recommendation` | 2.0.0 | `program-diagnosis` |

## Composition graph

```
program-design
  ├─▶ tier-structure ──────┐
  ├─▶ referral-program ────┤
  ├─▶ points-economics ◀───┘
  └─▶ program-diagnosis ◀──────── member-recovery
                        ◀──────── points-economics
```

`program-diagnosis` sits at the bottom. Every question about how the programme is currently behaving
routes through one implementation, so five skills do not invent five definitions of a healthy programme.

`points-economics` is the second-level shared dependency: tier benefits and referral incentives are both
costed through it rather than estimated separately
([../rules/economics-rules.md#E2](../rules/economics-rules.md)).

The graph is validated acyclic. Composition is conceptual — a composing skill defers a decision to another
skill's reasoning; it is not a function call, and this package defines no runtime.

## Choosing between them

| The question | The skill |
|---|---|
| Is our programme working? | `program-diagnosis` |
| Should we have a programme, and what shape? | `program-design` |
| What is a point worth, and can we afford it? | `points-economics` |
| Should we have tiers, and where? | `tier-structure` |
| What should we pay for a referral? | `referral-program` |
| Our members are going quiet | `member-recovery` |

## Adding a skill

A new skill must decide something none of the existing six decides. If it would mostly restate one of them
with a different scope, extend that skill instead.

Follow the contract every skill here conforms to: the thirteen sections in order, `targetbay.*` metadata
under `metadata`, capabilities drawn from [../capabilities.yaml](../capabilities.yaml), rules cited by
number rather than restated, and a golden prompt in
[tests/evals/](https://github.com/targetbay360/targetbay-agent-skills/blob/main/tests/evals/README.md).
