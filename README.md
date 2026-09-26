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

### Claude Code

Add the marketplace once, then install the products you use.

```
/plugin marketplace add targetbay360/targetbay-agent-skills
```

```
/plugin install targetbay-email-sms@targetbay
/plugin install targetbay-onboarding@targetbay
/plugin install targetbay-loyalty@targetbay
/plugin install targetbay-reviews@targetbay
```

This is the fullest install. It is the only one that also brings the slash commands, and the only one
where each plugin's `rules/` and `knowledge/` land next to its skills, so a skill's rule citations
resolve on disk.

### Cursor · Codex · Gemini CLI · Copilot · Kimi · anything else

Any host that reads the [Agent Skills](https://agentskills.io/specification) format loads these
unmodified. Two routes, both working today.

**GitHub CLI** — one command, knows where your host looks. Needs `gh` 2.90 or later.

```bash
gh skill install targetbay360/targetbay-agent-skills --all --pin main   --agent kimi-cli --scope user
```

Swap `--agent` for yours: `claude-code`, `github-copilot`, `cursor`, `codex`, `gemini-cli`,
`kimi-cli`, `cline`, `continue`, `goose`, `opencode`, `roo`, `warp`, `universal`, and around forty
more — `gh skill install --help` lists them. `--scope project` installs into the current
repository instead of your home directory, and `--dir <dir>` overrides both. Drop `--all` to pick
skills one at a time, and keep `--pin main` — without it `gh` resolves the newest release tag, which
today is behind the current skills.

**Clone and copy** — Node 18 or later, no dependencies, works for a host `gh` has never heard of.

```bash
git clone https://github.com/targetbay360/targetbay-agent-skills.git
node targetbay-agent-skills/plugins/targetbay-email-sms/scripts/install.mjs --dest ~/.kimi/skills
```

Flags: `--global` (writes to `~/.claude/skills`), `--dest <dir>`, `--force`, `--help`. Prefer this
route when rule citations matter — it rewrites each skill's relative links to GitHub URLs on the way
out, which `gh skill install` does not.

#### Where your host looks

| Host | Skills directory |
|---|---|
| Claude Code | `~/.claude/skills` |
| Cursor | `~/.cursor/skills` · `~/.agents/skills` |
| Codex | `~/.agents/skills` |
| Gemini CLI | `~/.gemini/skills` |
| GitHub Copilot | `.github/skills` (project scope) |
| Kimi CLI | `~/.kimi/skills` · `~/.claude/skills` · `~/.config/agents/skills` · `~/.agents/skills` |
| Cline · Amp · OpenCode · Warp · Antigravity | `~/.agents/skills` |

`~/.agents/skills` is shared by most of them, so one install there can serve several hosts at once.

#### Kimi CLI

Kimi reads any of the four paths above, plus the project-level `.kimi/`, `.claude/`, `.codex/` and
`.agents/skills`. For a directory it does not scan, add it to `extra_skill_dirs` in your Kimi config:

```toml
extra_skill_dirs = ["~/targetbay-agent-skills/plugins/targetbay-email-sms/skills"]
```

or pass `--skills-dir` at launch. Kimi surfaces each skill as a slash command, so
`/skill:audience-discovery` loads one directly instead of waiting for the model to reach for it.

### The reference skills

The three skills at the repository root are not in the marketplace. Copy the directory you want into
your host's skills path — they have no dependencies.

<details>
<summary>npm and curl</summary>

Each plugin has an npm package name reserved (`@targetbay/email-sms-skills`,
`@targetbay/reviews-skills`, `@targetbay/loyalty-skills`, `@targetbay/onboarding-skills`) and a
`scripts/install.sh` that pulls the latest tagged release. Neither is ready to recommend yet: nothing
is published to npm, and only `targetbay-email-sms` has a release, which is behind the current
skills. Use the two routes above until that changes.

</details>

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
| [**targetbay-email-sms**](plugins/targetbay-email-sms/README.md) | How a store plans, targets, sequences and optimises email and SMS marketing | 38 | `4.2.2` |
| [**targetbay-onboarding**](plugins/targetbay-onboarding/README.md) | What a new store actually is, what to ask it, what to set up first across all three products, and which surfaces to personalise before any of them | 10 | `0.3.1` |
| [**targetbay-loyalty**](plugins/targetbay-loyalty/README.md) | Whether to run a programme, what a point is worth, where tier thresholds go, which members are leaving | 6 | `0.2.1` |
| [**targetbay-reviews**](plugins/targetbay-reviews/README.md) | When to ask for a review, which products lack proof, how to answer a falling rating, where proof belongs | 5 | `0.2.1` |

Every capability across the four is still unmapped. Each plugin records its own mapping status in its
`docs/mcp-integration.md`.

## What to ask, and where it goes

You never name a skill. You describe the outcome, and the host picks. This is the short version of the
routing each plugin documents in its own `skills/README.md`.

| What you ask | What decides it |
|---|---|
| *"What should we be working on?"* | [`opportunity-discovery`](plugins/targetbay-email-sms/skills/opportunity-discovery/SKILL.md) |
| *"Win back our lapsed customers."* | [`customer-winback`](plugins/targetbay-email-sms/skills/customer-winback/SKILL.md) |
| *"Who should we target for this?"* · *"Which list?"* | [`audience-discovery`](plugins/targetbay-email-sms/skills/audience-discovery/SKILL.md) |
| *"Plan next month's marketing."* | [`monthly-marketing-planner`](plugins/targetbay-email-sms/skills/monthly-marketing-planner/SKILL.md) |
| *"Is Diwali worth doing for us?"* | [`holiday-marketing`](plugins/targetbay-email-sms/skills/holiday-marketing/SKILL.md) |
| *"We've just moved to TargetBay — what should we set up?"* | [`store-onboarding`](plugins/targetbay-email-sms/skills/store-onboarding/SKILL.md) |
| *"We just signed up — set up everything across all four."* | [`onboarding-blueprint`](plugins/targetbay-onboarding/skills/onboarding-blueprint/SKILL.md) |
| *"Our widget recommends things people just bought."* | [`personalization-audit`](plugins/targetbay-onboarding/skills/personalization-audit/SKILL.md) |
| *"Which products need reviews?"* | [`review-coverage`](plugins/targetbay-reviews/skills/review-coverage/SKILL.md) |
| *"Why did our rating fall?"* | [`rating-diagnosis`](plugins/targetbay-reviews/skills/rating-diagnosis/SKILL.md) |
| *"Can we double our points earn rate?"* | [`points-economics`](plugins/targetbay-loyalty/skills/points-economics/SKILL.md) |
| *"Which members are drifting away?"* | [`member-recovery`](plugins/targetbay-loyalty/skills/member-recovery/SKILL.md) |

## Prompt library

Copy-paste prompts for merchants who want a result without learning the skill names. Each prompt routes
to one skill, derives its thresholds from store data, and stops for approval before anything changes.

| Product | Library | Prompts |
|---|---|---|
| TargetBay Email & SMS | [`targetbay-email-sms/prompts/`](plugins/targetbay-email-sms/prompts/README.md) | 81 |
| TargetBay Reviews | [`targetbay-reviews/prompts/`](plugins/targetbay-reviews/prompts/README.md) | 16 |
| TargetBay Rewards | [`targetbay-loyalty/prompts/`](plugins/targetbay-loyalty/prompts/README.md) | 15 |

## Worked examples

Five traces follow one prompt all the way through — which skill was selected and which was passed
over, what it read, what it decided and why, what needs approval, and what it refused to do. They are
illustrative: the figures stand in for capability output, not real store data.

| Ask | Trace |
|---|---|
| *"Win back our lapsed customers."* | [`customer-winback.md`](plugins/targetbay-email-sms/examples/customer-winback.md) |
| *"Increase revenue this month."* | [`increase-revenue.md`](plugins/targetbay-email-sms/examples/increase-revenue.md) |
| *"Plan next month's marketing."* | [`plan-next-month.md`](plugins/targetbay-email-sms/examples/plan-next-month.md) |
| *"Improve our post-purchase marketing."* | [`automation-strategy.md`](plugins/targetbay-email-sms/examples/automation-strategy.md) |
| *"Prepare a Diwali campaign."* | [`holiday-drip.md`](plugins/targetbay-email-sms/examples/holiday-drip.md) |

Only `targetbay-email-sms` has traces so far. The other three plugins do not, and inventing them would
break the rule the traces themselves are written to demonstrate.

### One of them, in short

**You ask:** *"Win back our lapsed customers."*

`customer-winback` runs, composing `audience-discovery`. It passes over `customer-retention` — these
customers have already lapsed — but raises it as a follow-on, because most of this cohort would never
have reached win-back had anyone intervened when their purchase interval first lengthened.

It derives "lapsed" from the store's own repeat interval per category, so a customer is late relative
to *their own* pattern rather than a store-wide number. The lapsed base splits three ways:

| Group | Prior value | Still engaging | Verdict |
|---|---|---|---|
| A | High | Opens, no purchases | Three attempts — relevance first, incentive last |
| B | Moderate | Minimal | One attempt, stop condition set before the first send |
| C | Low | None, for a long period | **Suppress** |

Then it stops. Creating the campaigns is a `mutation` and needs a preview. Each send is `high_impact`
and needs approval on its own, with the recipient count. Suppressing Group C is `destructive` and needs
approval after the count and the prior value being written off are reported.

**And it refuses six things** — mailing the whole lapsed base because it is technically reachable;
opening with the deepest discount; leaving the attempt count open-ended; re-adding suppressed contacts;
presenting suppression as a loss-free cleanup; and claiming a recovery rate it cannot evidence.

That last list is the point. [Full trace](plugins/targetbay-email-sms/examples/customer-winback.md) ·
[how traces are written](plugins/targetbay-email-sms/docs/examples.md)

## Getting good answers out of these skills

**Ask for the outcome, not the mechanism.** "Win back our lapsed customers" routes better than "build
a three-email flow", because the first leaves the skill free to tell you the flow is not the problem.
When you cannot name the problem at all, that is what
[`opportunity-discovery`](plugins/targetbay-email-sms/skills/opportunity-discovery/SKILL.md) is for.

**Diagnose before you build.** Each product has an entry point that only looks:
`/targetbay-email-sms:what-now`, `/targetbay-onboarding:store-context`,
`/targetbay-reviews:review-audit`, `/targetbay-loyalty:program-health`. Skills are classified across
seven risk levels from `read_only` to `destructive` (safety rule S1); starting at the bottom costs one
extra question and saves a plan built on the wrong premise.

**Answer the questions it asks you.** An onboarding intake exists because some things cannot be
derived — and the answers are stored back onto the store record, so every later skill reads them as
constraints instead of asking again.

**Treat `blocked` and `partial` as answers.** A skill that names the capability it is missing has told
you something true about your setup (global rule G15). A skill that returns a confident number it could
not source would be the failure.

**Read the refusals.** [`docs/examples.md`](plugins/targetbay-email-sms/docs/examples.md) calls "what
the skill refused to do" the most informative part of a trace, and it is right. A skill declining to
target on "high income" because the attribute is inferred rather than verified (audience rule A9) is
working exactly as designed.

**Approve the action, not the objective.** "Send the campaign" is not an approval request; "send to
41,206 contacts" is — blast radius first, then the question (safety rules S2 and S4). Approval is
scoped and expires (S3), and is never batched across irreversible steps (S9). An agent that asks you
to approve a whole quarter in one go is not following this package.

**Tighten rules for your store; never loosen the safety ones.** Precedence runs safety → global →
domain → playbook → store context. A [playbook](plugins/targetbay-email-sms/playbooks/README.md) or a
store preference may make any rule stricter. Neither can make a safety rule looser.

**Install the reference skills when an answer needs the operational layer.** The plugins decide what a
store should do and cite the detail rather than restating it — DNS authentication, A2P 10DLC, dark-mode
rendering, the wiring of a specific journey. That detail lives in the three reference skills above.

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
  prompts/                        copy-paste prompts, one skill each
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

All three hold the same two boundaries as the plugins: **no invented API** (the platform is
reached only through the TargetBay MCP; code calls your own wrapper) and **no borrowed numbers** (published
requirements are attributed; anything else is labelled illustrative). The design skill adds a third —
**no markup**, design decisions only. The recipes skill adds its own — every recipe names MCP
capabilities from the plugin registry, never API paths.

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
