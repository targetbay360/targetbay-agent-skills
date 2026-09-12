# Skills

A skill teaches an agent how to accomplish an onsite objective. It owns the reasoning — which surface,
which strategy, who sees it, and whether it can be proved — while the TargetBay Personalization MCP owns
the capabilities that carry it out. See [../docs/mcp-integration.md](../docs/mcp-integration.md).

Six skills, covering inventory, recommendations, offers, discovery, measurement and assessment.

## Inventory

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Surface Inventory](surface-inventory/SKILL.md) | `surface-inventory` | `analysis` | 1.0.0 | — |

## Merchandising

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Recommendation Strategy](recommendation-strategy/SKILL.md) | `recommendation-strategy` | `plan` | 1.0.0 | `surface-inventory` |

## Offers

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Offer Targeting](offer-targeting/SKILL.md) | `offer-targeting` | `plan` | 1.0.0 | `surface-inventory` |

## Discovery

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Onsite Search](onsite-search/SKILL.md) | `onsite-search` | `recommendation` | 1.0.0 | `surface-inventory` |

## Measurement

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Experience Experimentation](experience-experimentation/SKILL.md) | `experience-experimentation` | `plan` | 1.0.0 | `surface-inventory` |

## Planning

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Personalization Audit](personalization-audit/SKILL.md) | `personalization-audit` | `recommendation` | 1.0.0 | `surface-inventory`, `recommendation-strategy`, `offer-targeting`, `onsite-search`, `experience-experimentation` |

## Composition graph

```
personalization-audit
  ├─▶ recommendation-strategy ────┐
  ├─▶ offer-targeting ────────────┤
  ├─▶ onsite-search ──────────────┤
  ├─▶ experience-experimentation ─┤
  └─▶ surface-inventory ◀─────────┘
```

`surface-inventory` sits at the bottom. Every question about what currently occupies a surface — and, more
importantly, what consent permits — routes through one implementation, so five skills do not propose
additions to pages that are already crowded.

`experience-experimentation` is where the other change-making skills hand off when a change should be
proved rather than asserted ([../rules/measurement-rules.md#M5](../rules/measurement-rules.md)).

The graph is validated acyclic. Composition is conceptual — a composing skill defers a decision to another
skill's reasoning; it is not a function call, and this package defines no runtime.

## Choosing between them

| The question | The skill |
|---|---|
| What personalization do we actually have running? | `surface-inventory` |
| What should we recommend, and where? | `recommendation-strategy` |
| Who should see this offer, and how often? | `offer-targeting` |
| Why does our search fail? | `onsite-search` |
| Can we prove this change works? | `experience-experimentation` |
| Where do we even start? | `personalization-audit` |

## Adding a skill

A new skill must decide something none of the existing six decides. If it would mostly restate one of them
with a different scope, extend that skill instead.

Follow the contract every skill here conforms to: the fourteen sections in order, `targetbay.*` metadata
under `metadata`, capabilities drawn from [../capabilities.yaml](../capabilities.yaml), rules cited by
number rather than restated, and a golden prompt in
[tests/evals/](https://github.com/targetbay360/targetbay-agent-skills/blob/main/tests/evals/README.md).
