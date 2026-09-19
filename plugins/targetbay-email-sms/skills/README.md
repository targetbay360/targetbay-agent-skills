# Skills

A skill teaches an agent how to accomplish a marketing objective. It owns the reasoning — which customers,
which instrument, how many, in what order, and when to stop — while the TargetBay Email & SMS MCP owns the
capabilities that carry it out. See [../docs/architecture.md](../docs/architecture.md).

38 skills, grouped by what they decide.

## Revenue

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [AOV Growth](aov-growth/SKILL.md) | `aov-growth` | `recommendation` | 2.0.0 | `upsell`, `cross-sell`, `audience-discovery` |
| [Cross-sell](cross-sell/SKILL.md) | `cross-sell` | `recommendation` | 2.0.0 | `audience-discovery` |
| [Offer Strategy](offer-strategy/SKILL.md) | `offer-strategy` | `recommendation` | 1.0.0 | `audience-discovery` |
| [Opportunity Discovery](opportunity-discovery/SKILL.md) | `opportunity-discovery` | `recommendation` | 2.1.0 | `revenue-analysis`, `automation-strategy`, `campaign-optimization`, `deliverability-qa` |
| [Product Recommendation Strategy](product-recommendation-strategy/SKILL.md) | `product-recommendation-strategy` | `recommendation` | 1.0.0 | — |
| [Revenue Analysis](revenue-analysis/SKILL.md) | `revenue-analysis` | `analysis` | 2.0.0 | — |
| [Revenue Growth](revenue-growth/SKILL.md) | `revenue-growth` | `recommendation` | 2.0.0 | `audience-discovery`, `automation-strategy`, `campaign-optimization`, `revenue-analysis`, `aov-growth` |
| [Stock and Price Alerts](stock-and-price-alerts/SKILL.md) | `stock-and-price-alerts` | `recommendation` | 1.0.0 | `audience-discovery`, `automation-architect` |
| [Upsell](upsell/SKILL.md) | `upsell` | `recommendation` | 2.0.0 | `audience-discovery` |

## Retention and lifecycle

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Customer Lifecycle](customer-lifecycle/SKILL.md) | `customer-lifecycle` | `recommendation` | 2.0.0 | `customer-retention`, `customer-winback`, `automation-strategy`, `audience-discovery` |
| [Product Replenishment](product-replenishment/SKILL.md) | `product-replenishment` | `recommendation` | 2.0.0 | `automation-architect`, `audience-discovery` |
| [Customer Retention](customer-retention/SKILL.md) | `customer-retention` | `recommendation` | 2.0.0 | `audience-discovery`, `automation-architect`, `product-replenishment` |
| [Customer Win-back](customer-winback/SKILL.md) | `customer-winback` | `recommendation` | 2.2.0 | `audience-discovery`, `list-hygiene`, `offer-strategy` |

## Automation

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Automation Architect](automation-architect/SKILL.md) | `automation-architect` | `plan` | 2.1.0 | `audience-discovery`, `product-recommendation-strategy`, `offer-strategy` |
| [Automation Orchestration](automation-orchestration/SKILL.md) | `automation-orchestration` | `plan` | 1.0.0 | `automation-architect` |
| [Automation Recipe Selector](automation-recipe-selector/SKILL.md) | `automation-recipe-selector` | `plan` | 1.0.0 | `automation-strategy`, `audience-discovery` |
| [Automation Strategy](automation-strategy/SKILL.md) | `automation-strategy` | `plan` | 2.0.0 | `automation-architect`, `audience-discovery` |

## Planning

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Campaign Conflict Resolver](campaign-conflict-resolver/SKILL.md) | `campaign-conflict-resolver` | `plan` | 1.0.0 | `audience-discovery` |
| [Marketing Calendar](marketing-calendar/SKILL.md) | `marketing-calendar` | `plan` | 2.0.1 | `monthly-marketing-planner`, `holiday-marketing`, `product-launch` |
| [Monthly Marketing Planner](monthly-marketing-planner/SKILL.md) | `monthly-marketing-planner` | `plan` | 2.0.0 | `audience-discovery`, `campaign-optimization`, `holiday-marketing`, `product-launch`, `revenue-growth` |
| [Store Onboarding](store-onboarding/SKILL.md) | `store-onboarding` | `plan` | 3.0.0 | `automation-strategy`, `audience-discovery`, `monthly-marketing-planner` |

## Seasonal and launch

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Product Launch](product-launch/SKILL.md) | `product-launch` | `plan` | 2.0.1 | `audience-discovery`, `cross-sell` |
| [Holiday Drip Campaign](holiday-drip-campaign/SKILL.md) | `holiday-drip-campaign` | `plan` | 2.0.0 | `audience-discovery` |
| [Holiday Marketing](holiday-marketing/SKILL.md) | `holiday-marketing` | `plan` | 2.0.0 | `audience-discovery`, `holiday-drip-campaign` |

## Optimisation, content and audience

| Skill | Name | Risk | Version | Composes |
|---|---|---|---|---|
| [Audience Discovery](audience-discovery/SKILL.md) | `audience-discovery` | `recommendation` | 2.1.0 | — |
| [Consent and Contact Policy](consent-verification/SKILL.md) | `consent-verification` | `recommendation` | 1.1.0 | — |
| [List Hygiene](list-hygiene/SKILL.md) | `list-hygiene` | `recommendation` | 1.1.0 | `audience-discovery` |
| [AI Content Governance](ai-content-governance/SKILL.md) | `ai-content-governance` | `plan` | 1.0.0 | `content-optimization` |
| [Content Optimization](content-optimization/SKILL.md) | `content-optimization` | `recommendation` | 2.1.0 | `ab-testing`, `dynamic-content-personalizer` |
| [Dynamic Content Personalizer](dynamic-content-personalizer/SKILL.md) | `dynamic-content-personalizer` | `recommendation` | 1.0.0 | `product-recommendation-strategy`, `audience-discovery` |
| [Email Render QA](email-render-qa/SKILL.md) | `email-render-qa` | `recommendation` | 1.0.0 | — |
| [A/B Testing](ab-testing/SKILL.md) | `ab-testing` | `recommendation` | 2.1.0 | `audience-discovery` |
| [Automation Optimization](automation-optimization/SKILL.md) | `automation-optimization` | `recommendation` | 2.0.0 | `ab-testing` |
| [Campaign Optimization](campaign-optimization/SKILL.md) | `campaign-optimization` | `recommendation` | 2.2.0 | `audience-discovery`, `ab-testing`, `content-optimization`, `deliverability-qa`, `offer-strategy` |
| [Channel Optimization](channel-optimization/SKILL.md) | `channel-optimization` | `recommendation` | 2.1.0 | `audience-discovery` |
| [Deliverability QA](deliverability-qa/SKILL.md) | `deliverability-qa` | `recommendation` | 1.0.0 | `list-hygiene` |
| [Email Quality Auditor](email-quality-auditor/SKILL.md) | `email-quality-auditor` | `recommendation` | 1.0.0 | `deliverability-qa`, `email-render-qa`, `dynamic-content-personalizer`, `audience-discovery` |
| [Send-Time Optimization](send-time-optimization/SKILL.md) | `send-time-optimization` | `recommendation` | 1.0.0 | `ab-testing` |

All 38 skills are at `targetbay.status: foundation` — the contract is established and the reasoning is real, but the
workflows have not yet been hardened against a live TargetBay Email & SMS MCP. See
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
                                   ├── content-optimization ─┬── ab-testing
                                   │                         └── dynamic-content-personalizer
                                   ├── deliverability-qa ── list-hygiene
                                   └── offer-strategy

email-quality-auditor ─┬── deliverability-qa ── list-hygiene
                       ├── email-render-qa (composes nothing)
                       ├── dynamic-content-personalizer ── product-recommendation-strategy
                       └── audience-discovery

store-onboarding ── automation-strategy · monthly-marketing-planner
customer-lifecycle ── customer-retention ── product-replenishment ── automation-architect
customer-winback ── audience-discovery · list-hygiene · offer-strategy
opportunity-discovery ── revenue-analysis · automation-strategy · campaign-optimization · deliverability-qa

automation-architect ── audience-discovery · product-recommendation-strategy · offer-strategy
automation-recipe-selector ── automation-strategy · audience-discovery
automation-orchestration ── automation-architect
stock-and-price-alerts ── audience-discovery · automation-architect
campaign-conflict-resolver ── audience-discovery
send-time-optimization ── ab-testing
ai-content-governance ── content-optimization
list-hygiene ── audience-discovery
consent-verification (composes nothing — a policy decision with no delegation)

                         …and nearly everything ends at audience-discovery
```

`audience-discovery` is the most-composed skill in the package: every targeting question routes through
it, so targeting logic exists in exactly one place. `revenue-analysis` plays the same role for
decomposition, `ab-testing` for test design, and `product-recommendation-strategy` — deliberately
built as a leaf that composes nothing — for which items a message features.

`email-quality-auditor` is the only skill positioned above the others as a gate rather than beside
them as a peer. It owns the verdict and none of the reasoning: every dimension it sweeps belongs to
the skill it composes. See [../docs/email-quality-architecture.md](../docs/email-quality-architecture.md).

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
| "Set up back-in-stock alerts" | [stock-and-price-alerts](stock-and-price-alerts/SKILL.md) |
| "What automations do we need?" | [automation-strategy](automation-strategy/SKILL.md) |
| "Design this journey" | [automation-architect](automation-architect/SKILL.md) |
| "This journey underperforms" | [automation-optimization](automation-optimization/SKILL.md) |
| "Where should this step run?" | [automation-orchestration](automation-orchestration/SKILL.md) |
| "Which recipe should we set up first?" | [automation-recipe-selector](automation-recipe-selector/SKILL.md) |
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
| "When is the best time to send?" | [send-time-optimization](send-time-optimization/SKILL.md) |
| "Can it write our newsletter?" | [ai-content-governance](ai-content-governance/SKILL.md) |
| "Our bounce rate is climbing" | [list-hygiene](list-hygiene/SKILL.md) |
| "Should we use double opt-in?" | [consent-verification](consent-verification/SKILL.md) |
| "Who should we target?" | [audience-discovery](audience-discovery/SKILL.md) |
| "Can we safely send this?" | [email-quality-auditor](email-quality-auditor/SKILL.md) |
| "Are we authenticated? Is our reputation slipping?" | [deliverability-qa](deliverability-qa/SKILL.md) |
| "Will this break in dark mode or with images off?" | [email-render-qa](email-render-qa/SKILL.md) |
| "How should we personalize this?" | [dynamic-content-personalizer](dynamic-content-personalizer/SKILL.md) |
| "What offer should we use?" | [offer-strategy](offer-strategy/SKILL.md) |
| "Which products should we recommend?" | [product-recommendation-strategy](product-recommendation-strategy/SKILL.md) |
| "These sends overlap — what gives?" | [campaign-conflict-resolver](campaign-conflict-resolver/SKILL.md) |
| "How often is too often?" | [consent-verification](consent-verification/SKILL.md) |

## The contract

Every `SKILL.md` conforms to the [Agent Skills specification](https://agentskills.io/specification) —
`name`, `description` and `license` at the top level, everything else under `metadata` as `targetbay.*`
strings — and is additionally validated against
[../schemas/skill.schema.json](../schemas/skill.schema.json), which is stricter, plus these thirteen
sections, in order:

`Purpose` · `When to Use` · `When Not to Use` · `Required Context` · `Required MCP Capabilities` ·
`Decision Process` · `Decision Rules` · `Workflow` · `Expected Output` · `Validation` ·
`Approval Requirements` · `Examples` · `Failure Handling`

To add a skill, follow [../docs/skill-authoring.md](../docs/skill-authoring.md), give it a golden
prompt in [tests/evals/](https://github.com/targetbay360/targetbay-agent-skills/blob/main/tests/evals/README.md), and run both checkers.

## Coverage

Every objective area named in the product brief now has a skill. Adding more is a matter of a new
directory and a `SKILL.md` — no structural change, though the platform's event stream and event
tracking were added to [../capabilities.yaml](../capabilities.yaml) to support the orchestration and
alerting skills.

The decisions live here; the runnable patterns that carry them live in
[TargetBay Marketing Automation Recipes](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-marketing-automation-recipes/SKILL.md),
a standalone reference skill outside this plugin. `automation-recipe-selector` is the skill that
decides which of those a given store should adopt, and in what order.

Email quality and deliverability reasoning lives here; the operational detail it rests on — DNS record
syntax, provider requirements, accessibility rules, dark-mode behaviour — lives in the standalone
[best practices](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/SKILL.md)
and [template design](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-template-design/SKILL.md)
reference skills, which the skills here cite rather than restate.

Deliberately **not** covered by this package: acquisition channels outside email and SMS, paid media,
creative production, pricing strategy, seed-list inbox placement measurement (no capability exists —
see [../../../docs/mcp-capability-gap-analysis.md](../../../docs/mcp-capability-gap-analysis.md)), and
anything the TargetBay Email & SMS platform enforces deterministically (consent, suppression, sending
limits). See [../docs/architecture.md](../docs/architecture.md).
