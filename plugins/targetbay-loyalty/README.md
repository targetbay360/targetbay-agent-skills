# TargetBay Loyalty Skills

A vendor-neutral AI Agent Skills package that teaches agents **how to design, price and run a loyalty and
referral programme** using TargetBay Loyalty.

[![version](https://img.shields.io/badge/version-0.2.0-blue)](VERSION)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![agent skills](https://img.shields.io/badge/Agent%20Skills-conformant-7c3aed)](https://agentskills.io/specification)

---

## Install

<table>
<tr><th>Claude Code</th><td>

```
/plugin marketplace add targetbay360/targetbay-agent-skills
/plugin install targetbay-loyalty@targetbay
```

</td></tr>
<tr><th>npm</th><td>

```bash
npx @targetbay/loyalty-skills --global
```

`--global` writes to `~/.claude/skills`. Omit it for `./.claude/skills`, or pass `--dest <dir>` for any
other host.

</td></tr>
</table>

### Try it

```
/targetbay-loyalty:program-health
/targetbay-loyalty:points-review
/targetbay-loyalty:quiet-members
```

Or just ask: *"Is our loyalty programme working?"* · *"Can we double our earn rate?"* ·
*"Our liability has doubled — should we expire points?"*

With no TargetBay Loyalty MCP connected, a skill will report itself **`blocked`** and name the capability
it is missing. That is the correct answer, and it is the quickest confirmation that the skills loaded.

---

## What this is

TargetBay Loyalty exposes its platform capabilities through an MCP server. That tells an agent *what it
can do*. It does not tell the agent whether this store should run a programme at all, what a point ought to
be worth, how many tiers the value distribution actually supports, or which quiet members are worth
contacting.

This package is that second half.

```
Loyalty MCP    =  what the agent CAN do
Loyalty Skills =  how the agent SHOULD accomplish a loyalty objective
```

## What this is not

- **Not** the TargetBay Loyalty MCP — no tools, no resources, no server
- **Not** the TargetBay Loyalty API — no clients, endpoints or request code
- **Not** a points engine, tier engine or redemption engine
- **Not** a collection of prompt files — it is a versioned package with contracts, schemas and validation

No file in this package makes a network call.

## Skills

| Skill | Decides | Risk |
|---|---|---|
| [Programme Diagnosis](skills/program-diagnosis/SKILL.md) | What the programme is actually doing | `analysis` |
| [Programme Design](skills/program-design/SKILL.md) | Whether to run one, and what shape | `plan` |
| [Points Economics](skills/points-economics/SKILL.md) | What a point is worth, and whether it is affordable | `recommendation` |
| [Tier Structure](skills/tier-structure/SKILL.md) | Whether tiers are warranted, and where the thresholds go | `plan` |
| [Referral Programme](skills/referral-program/SKILL.md) | What a referred customer is worth, and what to pay | `plan` |
| [Member Recovery](skills/member-recovery/SKILL.md) | Which quiet members are worth an intervention | `recommendation` |

Full graph and selection guidance: [skills/README.md](skills/README.md).

## Two things this package insists on

**The selection problem is named, every time.** Members outspend non-members in essentially every store,
and most of that gap existed before anybody enrolled — high-value customers join programmes. Any claim of
programme effect states how selection was accounted for, or states that it was not and lowers its
confidence ([rules/global-rules.md#G5](rules/global-rules.md)). This is the most common way a loyalty
programme is reported as working when it is not.

**Points are debt.** Every earn-rate, reward-price or expiry recommendation carries its effect on
outstanding liability, computed rather than asserted
([rules/safety-rules.md#S3](rules/safety-rules.md)). Nothing that reduces what members already earned —
devaluation, upward repricing, expiry — is folded into a larger proposal; it is stated as its own finding,
with the affected count and value, and approved separately.

## Architecture

```
┌──────────────────────────────────────────────┐
│ AI Agent host                                │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ TargetBay Loyalty Skills                     │  ← this package
│   skills · rules · knowledge                 │     HOW to decide
└──────────────────┬───────────────────────────┘
                   ▼  declares required capabilities
┌──────────────────────────────────────────────┐
│ TargetBay Loyalty MCP                        │  ← separate repository
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ TargetBay Loyalty platform                   │
└──────────────────────────────────────────────┘
```

Skills declare abstract capability identifiers — `loyalty.points_ledger`, not a tool name. The registry is
[capabilities.yaml](capabilities.yaml) and the mapping to real MCP tools is **TODO** for every entry in
this release. See [docs/mcp-integration.md](docs/mcp-integration.md), which also records the four questions
that mapping has to settle before any skill here can execute.

## Status

`0.2.0`. Skill reasoning is expected to be stable; capability identifiers may change as the real MCP
surface is mapped. See [CHANGELOG.md](CHANGELOG.md) for known gaps.

---

[CONTRIBUTING.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/CONTRIBUTING.md) ·
[SECURITY.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/SECURITY.md) ·
[CHANGELOG.md](CHANGELOG.md)
