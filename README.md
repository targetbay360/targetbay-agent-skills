# TargetBay Agent Skills

A marketplace of vendor-neutral AI Agent Skills packages — one per TargetBay product, plus one that
onboards a store across all of them and carries the onsite work that goes in first. Each teaches agents
**how to accomplish an objective** — the reasoning the MCP server does not carry.

[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![agent skills](https://img.shields.io/badge/Agent%20Skills-conformant-7c3aed)](https://agentskills.io/specification)
[![validate](https://github.com/targetbay360/targetbay-agent-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/targetbay360/targetbay-agent-skills/actions/workflows/validate.yml)

---

## Install

Add the marketplace once, then install the products you actually use.

```
/plugin marketplace add targetbay360/targetbay-agent-skills
```

| Plugin | Decides | Skills | Version | MCP |
|---|---|---|---|---|
| [**targetbay-email-sms**](plugins/targetbay-email-sms/README.md) | How a store plans, targets, sequences and optimises email and SMS marketing | 31 | `4.1.0` | mapping TODO |
| [**targetbay-reviews**](plugins/targetbay-reviews/README.md) | When to ask for a review, which products lack proof, how to answer a falling rating, where proof belongs | 5 | `0.2.0` | mapping TODO |
| [**targetbay-loyalty**](plugins/targetbay-loyalty/README.md) | Whether to run a programme, what a point is worth, where tier thresholds go, which members are leaving | 6 | `0.2.0` | mapping TODO |
| [**targetbay-onboarding**](plugins/targetbay-onboarding/README.md) | What a new store actually is, what to ask it, what to set up first across all three products, and which surfaces to personalise before any of them | 10 | `0.3.0` | mapping TODO |

```
/plugin install targetbay-email-sms@targetbay
/plugin install targetbay-reviews@targetbay
/plugin install targetbay-loyalty@targetbay
/plugin install targetbay-onboarding@targetbay
```

Each plugin also publishes to npm for hosts without a plugin system —
`npx @targetbay/reviews-skills --global`, and so on. See the plugin's own README.

### Try it

Ask in plain language: *"Win back our lapsed customers."* · *"Which products need reviews?"* ·
*"Can we double our points earn rate?"* · *"Our widget recommends things people just bought."* ·
*"We just signed up — set up everything across email, reviews, loyalty and onsite."*

With no MCP connected, a skill reports itself **`blocked`** and names the capability it is missing. That is
the correct answer, and the quickest confirmation that the skills loaded.

Every capability across the four plugins is still unmapped. The worksheet that closes that gap is
[docs/mcp-capability-inventory.md](docs/mcp-capability-inventory.md) — one row per capability, filled in
against the real MCP surface, plus the three answers that decide how far the onboarding pipeline can go.

---

## What these are

Each TargetBay product exposes its platform capabilities through an MCP server. That tells an agent *what
it can do*. It does not tell the agent which customers to target, when a review request should arrive,
whether the value distribution supports three tiers, or whether this store's traffic can resolve the test
somebody wants to run.

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
`onboarding.consent_and_tracking` — never tool names. Each plugin carries its own `capabilities.yaml` and its
own `docs/mcp-integration.md` recording what is mapped and what is not.

Three plugins cover one product each. `targetbay-onboarding` is the exception: it sequences all three for
a store that has just arrived, and it is where everything no single product owns gets settled — who is
allowed to contact a customer and how often, and the onsite capture that spends none of that budget and
therefore goes in first.

## What these are not

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
  skills/  rules/  knowledge/  schemas/  docs/  commands/
  capabilities.yaml  VERSION  CHANGELOG.md  package.json
targetbay-email-sms-best-practices/       a standalone reference skill — see below
targetbay-email-template-design/          a standalone reference skill — see below
targetbay-marketing-automation-recipes/   a standalone reference skill — see below
```

Every plugin is self-contained because Claude Code ships only what lives under a plugin's `source`
directory. A skill links to its own plugin's rules by relative path; anything outside the plugin is
referenced by full URL. `tests/validate.py` sweeps the whole repository and fails on a relative link that
does not resolve, so the boundary is enforced rather than remembered.

Plugins version and release independently, tagged `<plugin>@<version>`.

## The standalone reference skills

`targetbay-email-sms-best-practices/` sits outside `plugins/` deliberately. It is a routing hub plus
fourteen reference documents covering the layer beneath the plugins: DNS authentication, A2P 10DLC
registration, consent law, delivery events, suppression and accessibility.

It does not follow the plugin contract, and should not be made to. The plugins decide *what a store
should do* against declared MCP capabilities — no request code, no asserted thresholds, and
deliverability and compliance explicitly treated as platform responsibilities
([`rules/global-rules.md#G10`](plugins/targetbay-email-sms/rules/global-rules.md)). This skill is
exactly that excluded material: it teaches an engineer how the sending layer works, so it carries
implementation patterns and cites published external requirements by name.

Two boundaries it holds:

- **No invented API.** Code examples call your own `sendEmail(...)` / `verifySignature(...)` wrapper.
  Webhook headers and event names are flagged as "confirm in TargetBay's documentation".
- **No borrowed numbers.** Published provider and regulatory requirements are attributed as such;
  anything else is labelled illustrative or described as a derivation from store data.

`targetbay-email-template-design/` sits alongside it and covers the other half of that excluded
material: what an email should look like. Layout and spacing, email-safe typography, colour and dark
mode, template anatomy, calls to action and imagery, and the review before a template ships. The
plugins produce content direction and stop short of finished creative
([`rules/content-rules.md`](plugins/targetbay-email-sms/rules/content-rules.md)); this is the design
layer that turns direction into a template. It holds the same two boundaries, and adds a third: **no
markup** — design decisions only, with the templating layer left to implement them.

`targetbay-marketing-automation-recipes/` is the third, and covers the wiring. Runnable recipes across lifecycle journeys, personalisation, retention sweeps, list health, measurement,
AI-assisted content and system integration — each with its trigger, preconditions, the platform
operations it calls, the guardrails it must carry and what to measure. It holds the same boundaries
with one addition of its own: **the platform surface is described once, in a single reference**, and
every recipe names operations rather than paths, so endpoint drift is a one-file fix. It also states
plainly where the surface has no operation for what a recipe wants, rather than assuming one exists
because a published example calls it.

It draws the same line the other two do. The plugins decide *which* automations a store should adopt
and in what order — [`automation-recipe-selector`](plugins/targetbay-email-sms/skills/automation-recipe-selector/SKILL.md)
ranks the library against one store's readiness — and this skill covers how each one is wired once
chosen. It ships no pattern that mails a contact who did not opt in, and records the refusals rather
than omitting them.

The three link to each other by full GitHub URL rather than relative path. Each installs by copying
its own directory, so a relative link between them resolves during validation and is dead on install —
the same reason a plugin never reaches outside its own directory.

Install any of them by copying the directory into an agent host's skills path; they have no
dependencies and are not published to the marketplace.

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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the per-plugin contract, how to add a product plugin, and what
validation checks. [SECURITY.md](SECURITY.md) covers credential handling and the agent-safety posture.

```bash
python3 -m pip install -r tests/requirements.txt
python3 tests/validate.py
python3 tests/evals/run_evals.py
```

---

[CONTRIBUTING.md](CONTRIBUTING.md) · [SECURITY.md](SECURITY.md) ·
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) · [CHANGELOG.md](CHANGELOG.md)
