# TargetBay Agent Skills

**Marketing judgement for AI agents that already have your store data.**

Your TargetBay MCP server tells an agent what it *can* do. These skills decide what it *should* do —
which customers to target, what to send, how often, and where to stop and ask you first.

[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![agent skills](https://img.shields.io/badge/Agent%20Skills-conformant-7c3aed)](https://agentskills.io/specification)
[![validate](https://github.com/targetbay360/targetbay-agent-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/targetbay360/targetbay-agent-skills/actions/workflows/validate.yml)

---

## What you get

- **Ranked recommendations with the evidence attached** — not a list of ideas, an order of work and
  what each one rests on
- **A refusal when the data is not there** — the skill names the gap instead of filling it with a
  plausible number
- **A stop before anything reaches a real person** — the blast radius is shown, then the question is
  asked

## Requirements

| You need | Why |
|---|---|
| A **TargetBay account** with the product enabled | The skills reason about *your* store — its orders, its catalogue, its sending history. Nothing here ships sample data |
| That product's **MCP server** connected to your agent host | It supplies the capabilities each skill declares. Contact [support@targetbay.com](mailto:support@targetbay.com) for access |
| An **agent host that loads Agent Skills** | Claude Code, Cursor, Codex, Gemini CLI, GitHub Copilot, Kimi CLI, and the other clients listed at [agentskills.io](https://agentskills.io/specification) |

> **Mapping status.** Every capability in all four plugins is `mcp_tools: TODO` today — 18 in
> email-sms, 15 in onboarding, 14 each in loyalty and reviews. Until an MCP is connected, a skill
> answers **`blocked`** and names the capability it is missing. It plans; it does not execute.
> Each plugin tracks its own status in `docs/mcp-integration.md`
> ([email-sms](plugins/targetbay-email-sms/docs/mcp-integration.md) ·
> [onboarding](plugins/targetbay-onboarding/docs/mcp-integration.md) ·
> [loyalty](plugins/targetbay-loyalty/docs/mcp-integration.md) ·
> [reviews](plugins/targetbay-reviews/docs/mcp-integration.md)).

Skills never handle credentials. Authenticating to a TargetBay product is the agent host's and the
product MCP's responsibility — see [SECURITY.md](SECURITY.md).

## Install

Add the marketplace once, then install the products you actually use.

```
/plugin marketplace add targetbay360/targetbay-agent-skills
```

```
/plugin install targetbay-email-sms@targetbay
/plugin install targetbay-reviews@targetbay
/plugin install targetbay-loyalty@targetbay
/plugin install targetbay-onboarding@targetbay
```

Each plugin also publishes to npm for hosts without a plugin system —
`npx @targetbay/reviews-skills --global`, and so on. See the plugin's own README.

## Your first five minutes

Ask in plain language. No syntax, no skill names:

> *"Win back our lapsed customers."*
> *"Which products need reviews?"*
> *"Can we double our points earn rate?"*
> *"Our widget recommends things people just bought."*
> *"We just signed up — set up everything across email, reviews, loyalty and onsite."*

A `blocked` answer naming a missing capability means the skills loaded and the MCP is not connected
yet. That is the quickest way to confirm the install worked.

## The four plugins

| Plugin | Decides | Skills | Version |
|---|---|---|---|
| [**targetbay-email-sms**](plugins/targetbay-email-sms/README.md) | How a store plans, targets, sequences and optimises email and SMS marketing | 38 | `4.2.1` |
| [**targetbay-onboarding**](plugins/targetbay-onboarding/README.md) | What a new store actually is, what to ask it, what to set up first across all three products, and which surfaces to personalise before any of them | 10 | `0.3.0` |
| [**targetbay-loyalty**](plugins/targetbay-loyalty/README.md) | Whether to run a programme, what a point is worth, where tier thresholds go, which members are leaving | 6 | `0.2.0` |
| [**targetbay-reviews**](plugins/targetbay-reviews/README.md) | When to ask for a review, which products lack proof, how to answer a falling rating, where proof belongs | 5 | `0.2.0` |

Every capability across the four is still unmapped. Each plugin records its own mapping status in its
`docs/mcp-integration.md`.

---

## How it works

Each TargetBay product exposes its platform capabilities through an MCP server. That tells an agent
*what it can do*. It does not tell the agent which customers to target, when a review request should
arrive, whether the value distribution supports three tiers, or whether this store's traffic can
resolve the test somebody wants to run.

```
TargetBay MCP    =  what the agent CAN do
TargetBay Skills =  how the agent SHOULD accomplish an objective
```

```
┌──────────────────────────────────────────────┐
│ AI Agent host                                │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ TargetBay Agent Skills                       │  ← this repository
│   skills · rules · knowledge · playbooks     │     HOW to decide
└──────────────────┬───────────────────────────┘
                   ▼  declares required capabilities
┌──────────────────────────────────────────────┐
│ Product MCP servers                          │  ← separate repositories
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ TargetBay platform                           │
└──────────────────────────────────────────────┘
```

Skills declare abstract capability identifiers — `email_sms.customer_intelligence`,
`reviews.product_coverage`, `loyalty.points_ledger`, `onboarding.store_context`,
`onboarding.consent_and_tracking` — never tool names.

Three plugins cover one product each. `targetbay-onboarding` is the exception: it sequences all three
for a store that has just arrived, and it is where everything no single product owns gets settled —
who is allowed to contact a customer and how often, and the onsite capture that spends none of that
budget and therefore goes in first.

## What every plugin has in common

Different products, same contract:

- **Thirteen sections per skill**, in order — including `When Not to Use`, `Approval Requirements` and
  `Failure Handling`, because a skill that cannot say what it will not do is not finished
- **A composition graph with one skill at the bottom**, so "which products", "which members", "which
  surfaces" each has exactly one implementation and does not drift between skills
- **`blocked` and `partial` as first-class results.** A skill that cannot get the data it needs says so
  rather than filling the gap
- **Rules cited by number, never restated.** A constraint copied into every skill drifts once per copy
- **Nothing invented.** No tool names before the MCP is inspected, no thresholds asserted as universal, no
  benchmark presented as this store's data
- **`high_impact` always stops for a human**, with the blast radius shown before the question is asked

## What this is not

- **Not** MCP servers — no tools, no resources, no server code
- **Not** API clients — no endpoints, no request code
- **Not** campaign, review, points or recommendation engines
- **Not** collections of prompt files — each plugin is a versioned package with contracts, schemas and
  validation

No file in this repository makes a network call.

## Repository layout

```
.claude-plugin/marketplace.json   one entry per plugin
tests/                            shared validation and golden prompts
plugins/<name>/                   a product plugin — self-contained
  skills/  rules/  knowledge/  schemas/  docs/  commands/  scripts/
  playbooks/  examples/           targetbay-email-sms only
  .claude-plugin/plugin.json  capabilities.yaml  VERSION  CHANGELOG.md  package.json
targetbay-email-sms-best-practices/       standalone reference skills — see below
targetbay-email-template-design/
targetbay-marketing-automation-recipes/
```

Every plugin is self-contained because Claude Code ships only what lives under a plugin's `source`
directory. A skill links to its own plugin's rules by relative path; anything outside the plugin is
referenced by full URL. `tests/validate.py` sweeps the whole repository and fails on a relative link
that does not resolve, so the boundary is enforced rather than remembered.

Plugins version and release independently, tagged `<plugin>@<version>`.

## The reference skills

Three skills sit outside `plugins/` on purpose. The plugins decide *what a store should do* against
declared capabilities; these three carry the layer beneath that — the operational detail a plugin
deliberately excludes, which skills cite rather than restate.

| Skill | Covers |
|---|---|
| [**targetbay-email-sms-best-practices**](targetbay-email-sms-best-practices/README.md) | How the sending layer works: DNS authentication, A2P 10DLC, consent law, delivery events, suppression, accessibility |
| [**targetbay-email-template-design**](targetbay-email-template-design/README.md) | What an email should look like: layout, email-safe typography, colour and dark mode, CTAs, imagery, the review before a template ships |
| [**targetbay-marketing-automation-recipes**](targetbay-marketing-automation-recipes/README.md) | How an automation is wired: lifecycle journeys, personalisation, retention sweeps, list health, measurement, integration — each with trigger, preconditions, guardrails and what to measure |

All three hold the same two boundaries as the plugins: **no invented API** (code calls your own
wrapper; unconfirmed headers are flagged as unconfirmed) and **no borrowed numbers** (published
requirements are attributed; anything else is labelled illustrative). The design skill adds a third —
**no markup**, design decisions only. The recipes skill adds its own — the platform surface is
described once, in a single reference, and every recipe names operations rather than paths.

They do not follow the plugin contract and are not in the marketplace. Install one by copying its
directory into your agent host's skills path; they have no dependencies. They link to each other and
to the plugins by full GitHub URL, because a relative link between them resolves during validation
and is dead on install.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the per-plugin contract, how to add a product plugin, and
what validation checks. [SECURITY.md](SECURITY.md) covers credential handling and the agent-safety
posture.

```bash
python3 -m pip install -r tests/requirements.txt
python3 tests/validate.py
python3 tests/evals/run_evals.py
```

---

[CONTRIBUTING.md](CONTRIBUTING.md) · [SECURITY.md](SECURITY.md) ·
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) · [CHANGELOG.md](CHANGELOG.md)
