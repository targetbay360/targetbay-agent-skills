# Skills

A skill teaches an agent how to accomplish a marketing objective. It owns the reasoning — which
customers, which instrument, how many, in what order, and when to stop — while the BayEngage MCP owns the
capabilities that carry it out. See [../docs/architecture.md](../docs/architecture.md).

24 skills, grouped by what they decide.

## Revenue

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Revenue Growth](revenue-growth/SKILL.md) | `revenue-growth` | `recommendation` | 1.1.0 | `audience-discovery`, `automation-strategy`, `campaign-optimization`, `revenue-analysis`, `aov-growth` |
| [Revenue Analysis](revenue-analysis/SKILL.md) | `revenue-analysis` | `analysis` | 1.0.0 | — |
| [Opportunity Discovery](opportunity-discovery/SKILL.md) | `opportunity-discovery` | `recommendation` | 1.1.0 | `revenue-analysis`, `automation-strategy`, `campaign-optimization` |
| [AOV Growth](aov-growth/SKILL.md) | `aov-growth` | `recommendation` | 1.0.0 | `upsell`, `cross-sell`, `audience-discovery` |
| [Cross-sell](cross-sell/SKILL.md) | `cross-sell` | `recommendation` | 1.0.0 | `audience-discovery` |
| [Upsell](upsell/SKILL.md) | `upsell` | `recommendation` | 1.0.0 | `audience-discovery` |

## Retention and lifecycle

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Customer Lifecycle](customer-lifecycle/SKILL.md) | `customer-lifecycle` | `recommendation` | 1.0.0 | `customer-retention`, `customer-winback`, `automation-strategy`, `audience-discovery` |
| [Customer Retention](customer-retention/SKILL.md) | `customer-retention` | `recommendation` | 1.1.0 | `audience-discovery`, `automation-architect`, `product-replenishment` |
| [Customer Win-back](customer-winback/SKILL.md) | `customer-winback` | `recommendation` | 1.0.0 | `audience-discovery` |
| [Product Replenishment](product-replenishment/SKILL.md) | `product-replenishment` | `recommendation` | 1.0.0 | `automation-architect`, `audience-discovery` |

## Automation

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Automation Strategy](automation-strategy/SKILL.md) | `automation-strategy` | `plan` | 1.0.0 | `automation-architect`, `audience-discovery` |
| [Automation Architect](automation-architect/SKILL.md) | `automation-architect` | `plan` | 1.1.0 | `audience-discovery` |
| [Automation Optimization](automation-optimization/SKILL.md) | `automation-optimization` | `recommendation` | 1.2.0 | `ab-testing` |

## Planning

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Marketing Calendar](marketing-calendar/SKILL.md) | `marketing-calendar` | `plan` | 1.0.0 | `monthly-marketing-planner`, `holiday-marketing`, `product-launch` |
| [Monthly Marketing Planner](monthly-marketing-planner/SKILL.md) | `monthly-marketing-planner` | `plan` | 1.0.0 | `audience-discovery`, `campaign-optimization`, `holiday-marketing`, `product-launch`, `revenue-growth` |
| [Store Onboarding](store-onboarding/SKILL.md) | `store-onboarding` | `plan` | 1.1.0 | `automation-strategy`, `audience-discovery`, `monthly-marketing-planner` |

## Seasonal and launch

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Holiday Marketing](holiday-marketing/SKILL.md) | `holiday-marketing` | `plan` | 1.0.0 | `audience-discovery`, `holiday-drip-campaign` |
| [Holiday Drip Campaign](holiday-drip-campaign/SKILL.md) | `holiday-drip-campaign` | `plan` | 1.0.0 | `audience-discovery` |
| [Product Launch](product-launch/SKILL.md) | `product-launch` | `plan` | 1.0.0 | `audience-discovery`, `cross-sell` |

## Optimisation, content and audience

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Campaign Optimization](campaign-optimization/SKILL.md) | `campaign-optimization` | `recommendation` | 1.2.0 | `audience-discovery`, `ab-testing`, `content-optimization` |
| [Content Optimization](content-optimization/SKILL.md) | `content-optimization` | `recommendation` | 1.0.0 | `ab-testing` |
| [Channel Optimization](channel-optimization/SKILL.md) | `channel-optimization` | `recommendation` | 1.0.0 | `audience-discovery` |
| [A/B Testing](ab-testing/SKILL.md) | `ab-testing` | `recommendation` | 1.0.0 | `audience-discovery` |
| [Audience Discovery](audience-discovery/SKILL.md) | `audience-discovery` | `recommendation` | 1.1.0 | — |

All 24 skills are at `targetbay.status: foundation` — the contract is established and the reasoning is real, but the
workflows have not yet been hardened against a live BayEngage MCP. See
[../docs/versioning.md](../docs/versioning.md).

## Composition

Skills delegate rather than duplicate. `metadata.targetbay.composes` in the frontmatter declares the
delegation, and the graph is validated to stay acyclic on every run.

```
marketing-calendar
  └── monthly-marketing-planner
        ├── revenue-growth ─┬── revenue-analysis
        │                   ├── aov-growth ── upsell / cross-sell
        │                   └── automation-strategy ── automation-architect
        ├── holiday-marketing ── holiday-drip-campaign
        ├── product-launch ── cross-sell
        └── campaign-optimization ─┬── ab-testing
                                   └── content-optimization ── ab-testing

store-onboarding ── automation-strategy · monthly-marketing-planner
customer-lifecycle ── customer-retention ── product-replenishment ── automation-architect
opportunity-discovery ── revenue-analysis · automation-strategy · campaign-optimization

                         …and nearly everything ends at audience-discovery
```

`audience-discovery` is the most-composed skill in the package: every targeting question routes through
it, so targeting logic exists in exactly one place. `revenue-analysis` plays the same role for
decomposition, and `ab-testing` for test design.

## Which skill for which question

| The question | Skill |
|---|---|
| "What should we be working on?" | [opportunity-discovery](opportunity-discovery/SKILL.md) |
| "Increase revenue" | [revenue-growth](revenue-growth/SKILL.md) |
| "Why did revenue drop?" | [revenue-analysis](revenue-analysis/SKILL.md) |
| "Raise average order value" | [aov-growth](aov-growth/SKILL.md) |
| "Sell more categories per customer" | [cross-sell](cross-sell/SKILL.md) |
| "Move customers to the premium tier" | [upsell](upsell/SKILL.md) |
| "Map our customer lifecycle" | [customer-lifecycle](customer-lifecycle/SKILL.md) |
| "Our repeat rate is dropping" | [customer-retention](customer-retention/SKILL.md) |
| "Win back lapsed customers" | [customer-winback](customer-winback/SKILL.md) |
| "Set up reorder reminders" | [product-replenishment](product-replenishment/SKILL.md) |
| "What automations do we need?" | [automation-strategy](automation-strategy/SKILL.md) |
| "Design this journey" | [automation-architect](automation-architect/SKILL.md) |
| "This journey underperforms" | [automation-optimization](automation-optimization/SKILL.md) |
| "Plan the year" | [marketing-calendar](marketing-calendar/SKILL.md) |
| "Plan next month" | [monthly-marketing-planner](monthly-marketing-planner/SKILL.md) |
| "We're new — what do we set up?" | [store-onboarding](store-onboarding/SKILL.md) |
| "Should we do this holiday?" | [holiday-marketing](holiday-marketing/SKILL.md) |
| "Prepare a <holiday> campaign" | [holiday-drip-campaign](holiday-drip-campaign/SKILL.md) |
| "We're launching a product" | [product-launch](product-launch/SKILL.md) |
| "This campaign underperformed" | [campaign-optimization](campaign-optimization/SKILL.md) |
| "This copy isn't working" | [content-optimization](content-optimization/SKILL.md) |
| "What should we send on SMS?" | [channel-optimization](channel-optimization/SKILL.md) |
| "Design a test" | [ab-testing](ab-testing/SKILL.md) |
| "Who should we target?" | [audience-discovery](audience-discovery/SKILL.md) |

## The contract

Every `SKILL.md` conforms to the [Agent Skills specification](https://agentskills.io/specification) —
`name`, `description` and `license` at the top level, everything else under `metadata` as `targetbay.*`
strings — and is additionally validated against
[../schemas/skill.schema.json](../schemas/skill.schema.json), which is stricter, plus these fourteen
sections, in order:

`Purpose` · `When to Use` · `When Not to Use` · `Required Context` · `Required MCP Capabilities` ·
`Inputs` · `Decision Process` · `Decision Rules` · `Workflow` · `Expected Output` · `Validation` ·
`Approval Requirements` · `Examples` · `Failure Handling`

To add a skill, follow [../docs/skill-authoring.md](../docs/skill-authoring.md), give it a golden
prompt in [tests/evals/](https://github.com/targetbay360/targetbay-agent-skills/blob/main/tests/evals/README.md), and run both checkers.

## Coverage

Every objective area named in the product brief now has a skill. Adding more is a matter of a new
directory and a `SKILL.md` — no structural change, and no new capability is required by anything currently
on the horizon.

Deliberately **not** covered by this package: acquisition channels outside email and SMS, paid media,
creative production, pricing strategy, and anything the BayEngage platform enforces deterministically
(consent, suppression, sending limits). See [../docs/architecture.md](../docs/architecture.md).
