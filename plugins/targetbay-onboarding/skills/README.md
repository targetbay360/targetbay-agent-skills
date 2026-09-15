# Skills

A skill teaches an agent how to accomplish an onboarding objective. It owns the reasoning — what this
store actually is, what to ask, what to build first, and when to stop — while the TargetBay MCP owns the
capabilities that carry it out. See [../docs/mcp-integration.md](../docs/mcp-integration.md).

Ten skills in two groups: a four-step pipeline, and the onsite work that pipeline starts with.

## The pipeline

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Store Context Audit](context-audit/SKILL.md) | `context-audit` | `analysis` | 0.1.0 | — |
| [Onboarding Intake](onboarding-intake/SKILL.md) | `onboarding-intake` | `mutation` | 0.1.0 | `context-audit` |
| [Cross-Product Onboarding Blueprint](onboarding-blueprint/SKILL.md) | `onboarding-blueprint` | `plan` | 0.2.0 | `context-audit`, `onboarding-intake` |
| [Onboarding Provisioning](onboarding-provisioning/SKILL.md) | `onboarding-provisioning` | `high_impact` | 0.1.0 | `onboarding-blueprint` |

## The onsite work

Onsite capture and personalisation is not a product. It is where onboarding starts, because it spends no
contact budget ([../rules/contact-ownership-rules.md#X3](../rules/contact-ownership-rules.md)) and
because what it captures cannot be captured retroactively
([../rules/sequencing-rules.md#SQ1](../rules/sequencing-rules.md)).

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Surface Inventory](surface-inventory/SKILL.md) | `surface-inventory` | `analysis` | 1.1.0 | — |
| [Recommendation Strategy](recommendation-strategy/SKILL.md) | `recommendation-strategy` | `plan` | 1.1.0 | `surface-inventory` |
| [Offer Targeting](offer-targeting/SKILL.md) | `offer-targeting` | `plan` | 1.1.0 | `surface-inventory` |
| [Onsite Search](onsite-search/SKILL.md) | `onsite-search` | `recommendation` | 1.1.0 | `surface-inventory` |
| [Experience Experimentation](experience-experimentation/SKILL.md) | `experience-experimentation` | `plan` | 1.1.0 | `surface-inventory` |
| [Personalization Audit](personalization-audit/SKILL.md) | `personalization-audit` | `recommendation` | 1.1.0 | `surface-inventory`, `recommendation-strategy`, `offer-targeting`, `onsite-search`, `experience-experimentation` |

## Composition

```
onboarding-provisioning          personalization-audit
        │                          ├─▶ recommendation-strategy ────┐
        ▼                          ├─▶ offer-targeting ────────────┤
onboarding-blueprint ──────┐       ├─▶ onsite-search ──────────────┤
        │                  │       ├─▶ experience-experimentation ─┤
        ▼                  │       └─▶ surface-inventory ◀─────────┘
onboarding-intake          │
        │                  │
        ▼                  ▼
     context-audit ◀───────┘
```

Two graphs, one per group, each with a single skill at the bottom.

`context-audit` composes nothing. Everything above it depends on the same partition of what is derived,
what is borrowed and what is absent, so that partition is computed once and disagreed with once.

`surface-inventory` plays the same role onsite. Every question about what currently occupies a surface —
and, more importantly, what consent permits — routes through one implementation, so five skills do not
propose additions to pages that are already crowded.

`experience-experimentation` is where the other onsite skills hand off when a change should be proved
rather than asserted ([../rules/measurement-rules.md#M5](../rules/measurement-rules.md)).

Both graphs are validated acyclic. Composition is conceptual — a composing skill defers a decision to
another skill's reasoning; it is not a function call, and this package defines no runtime.

## Choosing between them

| The question | The skill |
|---|---|
| "What do we actually know about this store?" | `context-audit` |
| "What do we need to ask them?" | `onboarding-intake` |
| "What should we set up first, across all three products?" | `onboarding-blueprint` |
| "The plan is approved — build it" | `onboarding-provisioning` |
| "What is actually running on our site right now?" | `surface-inventory` |
| "What should we recommend, and where?" | `recommendation-strategy` |
| "Who should see this offer, and how often?" | `offer-targeting` |
| "Why does our search fail?" | `onsite-search` |
| "Can we prove this change works?" | `experience-experimentation` |
| "Where do we even start onsite?" | `personalization-audit` |
| "What should we set up first in email and SMS only?" | [store-onboarding](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/store-onboarding/SKILL.md), in the Email & SMS plugin |

## Why the risk levels climb

The pipeline runs from `analysis` to `high_impact` in four steps, and each step is separately approvable.
That is deliberate: onboarding is the workflow where a single approval would otherwise be asked to cover
reading a store, interviewing its owner, planning a quarter of work, and activating a dozen things that
reach real people. Splitting it means a reviewer can disagree with the facts before the plan is built on
them, and with the plan before anything is created.

## Adding a skill

An onboarding skill must answer a question a store owner would actually ask on their first week, and must
not overlap an existing skill's trigger. If it decides what a single product should do, it belongs in
that product's plugin, not here — onsite work is the exception, because no product owns it. See
[CONTRIBUTING.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/CONTRIBUTING.md).
