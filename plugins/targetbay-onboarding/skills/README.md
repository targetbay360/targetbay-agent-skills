# Skills

A skill teaches an agent how to accomplish an onboarding objective. It owns the reasoning — what this
store actually is, what to ask, what to build first, and when to stop — while the TargetBay MCP owns the
capabilities that carry it out. See [../docs/mcp-integration.md](../docs/mcp-integration.md).

Four skills, forming one pipeline rather than a catalogue.

## The pipeline

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Store Context Audit](context-audit/SKILL.md) | `context-audit` | `analysis` | 0.1.0 | — |
| [Onboarding Intake](onboarding-intake/SKILL.md) | `onboarding-intake` | `mutation` | 0.1.0 | `context-audit` |
| [Cross-Product Onboarding Blueprint](onboarding-blueprint/SKILL.md) | `onboarding-blueprint` | `plan` | 0.1.0 | `context-audit`, `onboarding-intake` |
| [Onboarding Provisioning](onboarding-provisioning/SKILL.md) | `onboarding-provisioning` | `high_impact` | 0.1.0 | `onboarding-blueprint` |

## Composition

```
onboarding-provisioning
        │
        ▼
onboarding-blueprint ──────┐
        │                  │
        ▼                  │
onboarding-intake          │
        │                  │
        ▼                  ▼
     context-audit ◀───────┘
```

`context-audit` sits at the bottom and composes nothing. Everything above it depends on the same
partition of what is derived, what is borrowed and what is absent, so that partition is computed once and
disagreed with once.

## Choosing between them

| The question | The skill |
|---|---|
| "What do we actually know about this store?" | `context-audit` |
| "What do we need to ask them?" | `onboarding-intake` |
| "What should we set up first, across all four products?" | `onboarding-blueprint` |
| "The plan is approved — build it" | `onboarding-provisioning` |
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
that product's plugin, not here. See
[CONTRIBUTING.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/CONTRIBUTING.md).
