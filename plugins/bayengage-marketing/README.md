# TargetBay Email & SMS Marketing Skills

A vendor-neutral AI Agent Skills package that teaches agents **how to accomplish email and SMS marketing
outcomes** using BayEngage.

[![version](https://img.shields.io/badge/version-2.1.0-blue)](VERSION)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![agent skills](https://img.shields.io/badge/Agent%20Skills-conformant-7c3aed)](https://agentskills.io/specification)
[![validate](https://github.com/targetbay360/targetbay-agent-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/targetbay360/targetbay-agent-skills/actions/workflows/validate.yml)

---

## Install

<table>
<tr><th>Claude Code</th><td>

```
/plugin marketplace add targetbay360/targetbay-agent-skills
/plugin install bayengage-marketing@targetbay
```

Installs the 24 skills and six slash commands.

</td></tr>
<tr><th>npm</th><td>

```bash
npx @targetbay/bayengage-marketing-skills --global
```

`--global` writes to `~/.claude/skills`. Omit it for `./.claude/skills`, or pass
`--dest <dir>` for any other host (Cursor, Codex, your own agent).

</td></tr>
<tr><th>curl</th><td>

```bash
curl -fsSL https://raw.githubusercontent.com/targetbay360/targetbay-agent-skills/main/plugins/bayengage-marketing/scripts/install.sh | sh
```

No npm, no plugin system. Takes an optional destination argument.

</td></tr>
<tr><th>manual</th><td>

Download the `bayengage-marketing@<version>` tarball from
[Releases](https://github.com/targetbay360/targetbay-agent-skills/releases) and copy `skills/` into your
agent's skills directory. Releases are tagged per plugin, so pick the one whose tag starts with
`bayengage-marketing@`.

</td></tr>
</table>

The package is also mirrored to GitHub Packages. That registry requires a GitHub token even to read a
public package, so npmjs above is the path to use unless your organisation already standardises on it.

> This plugin lives in the [TargetBay Agent Skills](https://github.com/targetbay360/targetbay-agent-skills)
> marketplace alongside skills for Reviews, Loyalty and Personalization. Adding the marketplace once lets
> you install any of them; each versions and releases independently.
>
> Previously published as `@targetbay/targetbay-email-sms-marketing-skills` from a repository of the same
> name. Both still resolve — the GitHub URL redirects and the npm package is deprecated with a pointer
> here — but new installs should use the names above.

### Try it

```
/bayengage-marketing:plan-month next month
/bayengage-marketing:what-now
/bayengage-marketing:win-back
```

Or just ask: *"Win back our lapsed customers."* · *"Why did this campaign underperform?"* ·
*"Prepare a Diwali campaign."*

With no BayEngage MCP connected, a skill will report itself **`blocked`** and name the capability it is
missing. That is the correct answer, and it is the quickest confirmation that the skills loaded.

### Commands

| Command | Does |
|---|---|
| `/bayengage-marketing:plan-month` | A dated calendar for the period, campaign count derived not templated |
| `/bayengage-marketing:what-now` | Open-ended scan; ranks what is most worth fixing or building |
| `/bayengage-marketing:win-back` | Who among the lapsed is worth recovering, and where to stop |
| `/bayengage-marketing:holiday <name>` | Whether a holiday is worth doing here, then the sequence |
| `/bayengage-marketing:diagnose <campaign>` | Why a campaign underperformed, and a testable fix |
| `/bayengage-marketing:audit-automations` | Portfolio audit; gaps, splits, retirements, sequenced |

---

## What this is

BayEngage already exposes its platform capabilities through an MCP server. That tells an agent *what it
can do*. It does not tell the agent which customers to target, whether an objective needs one automation
or four, how many stages a holiday sequence should have, or when to stop and ask a human.

This package is that second half.

```
BayEngage MCP    =  what the agent CAN do
BayEngage Skills =  how the agent SHOULD accomplish a marketing objective
```

## What this is not

- **Not** BayEngage MCP — no tools, no resources, no server
- **Not** the BayEngage API — no clients, endpoints or request code
- **Not** a campaign engine, customer database or automation engine
- **Not** a collection of prompt files — it is a versioned package with contracts, schemas and validation

No file in this repository makes a network call.

## Architecture

```
┌──────────────────────────────────────────────┐
│ AI Agent host                                │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ TargetBay Email & SMS Marketing Skills       │  ← this package
│   skills · rules · knowledge · playbooks     │     HOW to decide
└──────────────────┬───────────────────────────┘
                   ▼  declares required capabilities
┌──────────────────────────────────────────────┐
│ BayEngage MCP                                │  ← separate repository
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ BayEngage platform                           │
└──────────────────────────────────────────────┘
```

Skills declare **abstract capabilities** — `bayengage.customer_intelligence`, not a tool name — so the two
repositories version independently. Full reasoning in [docs/architecture.md](docs/architecture.md).

## Example

```
User: "Plan next month's marketing."
```

```
monthly-marketing-planner
        │
        ├── reads store context via BayEngage MCP
        │     campaign analytics · customer intelligence
        │     product intelligence · automations · calendar
        │
        ├── establishes cadence capacity BEFORE selecting campaigns
        │
        ├── composes  audience-discovery      → who, ranked and sized
        │             holiday-marketing       → is the holiday in the window worth it?
        │             product-launch          → wave-sequenced launch
        │             campaign-optimization   → what worked last time
        │
        └── returns a dated calendar: date · campaign · objective · audience ·
            channel · product · offer · content direction · expected outcome ·
            dependencies · risk
                │
                └── each send stops for explicit human approval
```

The campaign count is **derived**, not templated. An empty week is a valid output. See
[examples/plan-next-month.md](examples/plan-next-month.md) for the full trace.

## The 24 skills

| | Skills |
|---|---|
| **Revenue** | [revenue-growth](skills/revenue-growth/SKILL.md) · [revenue-analysis](skills/revenue-analysis/SKILL.md) · [opportunity-discovery](skills/opportunity-discovery/SKILL.md) · [aov-growth](skills/aov-growth/SKILL.md) · [cross-sell](skills/cross-sell/SKILL.md) · [upsell](skills/upsell/SKILL.md) |
| **Retention & lifecycle** | [customer-lifecycle](skills/customer-lifecycle/SKILL.md) · [customer-retention](skills/customer-retention/SKILL.md) · [customer-winback](skills/customer-winback/SKILL.md) · [product-replenishment](skills/product-replenishment/SKILL.md) |
| **Automation** | [automation-strategy](skills/automation-strategy/SKILL.md) · [automation-architect](skills/automation-architect/SKILL.md) · [automation-optimization](skills/automation-optimization/SKILL.md) |
| **Planning** | [marketing-calendar](skills/marketing-calendar/SKILL.md) · [monthly-marketing-planner](skills/monthly-marketing-planner/SKILL.md) · [store-onboarding](skills/store-onboarding/SKILL.md) |
| **Seasonal & launch** | [holiday-marketing](skills/holiday-marketing/SKILL.md) · [holiday-drip-campaign](skills/holiday-drip-campaign/SKILL.md) · [product-launch](skills/product-launch/SKILL.md) |
| **Optimisation & content** | [campaign-optimization](skills/campaign-optimization/SKILL.md) · [content-optimization](skills/content-optimization/SKILL.md) · [channel-optimization](skills/channel-optimization/SKILL.md) · [ab-testing](skills/ab-testing/SKILL.md) |
| **Audience** | [audience-discovery](skills/audience-discovery/SKILL.md) |

Index, composition graph and the question-to-skill table: [skills/README.md](skills/README.md).

## Layout

```
skills/        24 skills, one SKILL.md each — objective → decisions → plan
rules/         8 numbered, citable rule sets that bind every skill
knowledge/     9 marketing principles documents, vendor-agnostic
playbooks/     5 vertical overlays that adjust defaults without editing skills
schemas/       4 JSON Schemas — skill, recommendation, workflow, skill-result
commands/      6 slash commands that route a plain request to the right skill
docs/          architecture, authoring, MCP integration, rules, versioning, examples
examples/      5 narrated traces of skills reasoning end to end
tests/         two runners — structural validation, and golden-prompt evaluations
scripts/       install.mjs (npm) and install.sh (curl) — no dependencies
capabilities.yaml   the abstract capability registry
.claude-plugin/     plugin and marketplace manifests
```

## What the skills refuse to do

The package is defined as much by its constraints as its content. Every skill:

- **Never assumes one objective means one automation**, or that an automation has a fixed node count
- **Never fixes a sequence length** — holiday drips, calendars and journeys all derive their size
- **Never invents customer, product or performance data** — a missing figure is reported, not filled in
- **Never optimises on open rate** — revenue, conversion, AOV and unsubscribe risk lead
- **Never targets an audience without confirming it exists and is large enough**
- **Never sends, activates or deletes anything without explicit human approval**
- **Never personalises on data BayEngage cannot verify for that contact**

`blocked` and `partial` are first-class results. See [rules/](rules/README.md).

## Status

**2.0.0 — foundation, published.** Contracts established, reasoning real, workflows not yet hardened
against a live BayEngage MCP. Every objective area named in the product brief now has a skill, and the
package now installs four ways.

**No capability is mapped to a real MCP tool yet.** Every entry in
[capabilities.yaml](capabilities.yaml) carries `mcp_tools: TODO`. Skills can plan; they cannot execute
until that mapping exists — deliberately, because inventing tool names would produce confident, wrong
documentation. See [docs/mcp-integration.md](docs/mcp-integration.md) for the mapping checklist.

`bayengage.messaging_sms` is declared but **unverified** — no inspected BayEngage implementation exposes
SMS dispatch. Skills degrade to email-only when it is absent.

## Validate

```bash
python3 -m pip install -r tests/requirements.txt
python3 tests/validate.py            # structure and contracts
python3 tests/evals/run_evals.py     # golden prompts
```

`validate.py` — eight groups: structure, **spec**, skill metadata, playbooks, references and link
resolution, duplication, schemas, versioning. The `spec` group runs the Agent Skills reference validator
over every skill, so conformance is a test rather than a claim. Invalid fixtures must be *rejected*, so a
green run means the checks are doing work.

`run_evals.py` — 38 golden prompts asserting which skill answers which question, what it composes, and
what it must never do. Its selection check is a lexical proxy with a documented ceiling, not a model;
the model-dependent half is emitted as prompt packs via `--emit`. It found six skill descriptions that
did not contain the words users actually type.

See [tests/README.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/tests/README.md) and [tests/evals/README.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/tests/evals/README.md).

## Using it

Every skill conforms to the [Agent Skills specification](https://agentskills.io/specification), so any
host implementing that format loads this package unmodified — Claude Code, Claude.ai, and the other
clients listed at [agentskills.io/clients](https://agentskills.io/clients).

The specification closes the top level of the frontmatter to `name`, `description`, `license`,
`compatibility`, `metadata` and `allowed-tools`, and its reference validator rejects anything else.
Everything this package adds therefore lives under `metadata`, namespaced `targetbay.`:

```yaml
---
name: customer-winback
description: Use when targeting customers who have already lapsed — dormant or churned contacts who …
license: MIT
metadata:
  targetbay.display_name: Customer Win-back
  targetbay.version: "1.0.0"
  targetbay.category: retention
  targetbay.requires: bayengage.customer_intelligence, bayengage.order_intelligence, …
  targetbay.composes: audience-discovery
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---
```

A host that reads none of that sees a well-formed skill with a `name` and a `description`, which is the
point. A host that reads it gets the capability contract, the composition graph and the risk class.

The agent also needs access to BayEngage MCP. Without it, skills will correctly report themselves as
`blocked` rather than guessing.

## Contributing

[CONTRIBUTING.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/CONTRIBUTING.md) · [docs/skill-authoring.md](docs/skill-authoring.md) ·
[SECURITY.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/SECURITY.md) · [CHANGELOG.md](CHANGELOG.md)

## License

MIT — see [LICENSE](LICENSE).
