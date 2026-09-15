# TargetBay Onboarding Skills

A vendor-neutral AI Agent Skills package that teaches agents **how to onboard a store onto TargetBay** —
what this store actually is, what to set up first across all three products, and in what order. Onsite
capture is part of that: the placements, offers, search and tracking a store starts with live here rather
than in a product plugin, because no product owns them.

[![version](https://img.shields.io/badge/version-0.2.0-blue)](VERSION)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![agent skills](https://img.shields.io/badge/Agent%20Skills-conformant-7c3aed)](https://agentskills.io/specification)

---

## Install

<table>
<tr><th>Claude Code</th><td>

```
/plugin marketplace add targetbay360/targetbay-agent-skills
/plugin install targetbay-onboarding@targetbay
```

</td></tr>
<tr><th>npm</th><td>

```bash
npx @targetbay/onboarding-skills --global
```

`--global` writes to `~/.claude/skills`. Omit it for `./.claude/skills`, or pass `--dest <dir>` for any
other host.

</td></tr>
</table>

## The problem this package exists for

Onboarding is where a store decides whether TargetBay is worth keeping, and it is the easiest place to
give every store the same thing. The operator has never seen this store before, the store has no history
to argue with, and the fastest path is the checklist that worked last time.

The defence is not a longer checklist. It is knowing precisely which facts about *this* store are
measured, which are borrowed from its vertical, and which do not exist at all — and then sequencing three
products so they do not compete for the same customer's attention.

```
TargetBay MCP               =  what the agent CAN do
TargetBay Onboarding Skills =  how the agent SHOULD onboard a store
```

## What this is not

- **Not** the TargetBay MCP — no tools, no resources, no server
- **Not** the TargetBay API — no clients, endpoints or request code
- **Not** a replacement for the three product plugins — it sequences them, it does not duplicate them
- **Not** a collection of prompt files — it is a versioned package with contracts, schemas and validation

No file in this package makes a network call.

## Skills

**The pipeline.**

| Skill | Decides | Risk |
|---|---|---|
| [Store Context Audit](skills/context-audit/SKILL.md) | What is actually known about this store | `analysis` |
| [Onboarding Intake](skills/onboarding-intake/SKILL.md) | What only the store owner can answer | `mutation` |
| [Cross-Product Onboarding Blueprint](skills/onboarding-blueprint/SKILL.md) | What to set up first, across all three products | `plan` |
| [Onboarding Provisioning](skills/onboarding-provisioning/SKILL.md) | Building the approved plan, without activating it | `high_impact` |

**The onsite work the pipeline starts with.** It spends no contact budget
([rules/contact-ownership-rules.md#X3](rules/contact-ownership-rules.md)) and what it captures cannot be
captured retroactively, so it runs while the messaging programmes are still being decided.

| Skill | Decides | Risk |
|---|---|---|
| [Surface Inventory](skills/surface-inventory/SKILL.md) | What runs on the store's surfaces, and what consent permits | `analysis` |
| [Recommendation Strategy](skills/recommendation-strategy/SKILL.md) | What to recommend, where, and what it is worth | `plan` |
| [Offer Targeting](skills/offer-targeting/SKILL.md) | Who sees an onsite offer, when, and whether it should exist | `plan` |
| [Onsite Search](skills/onsite-search/SKILL.md) | What failing queries mean for vocabulary and catalogue | `recommendation` |
| [Experience Experimentation](skills/experience-experimentation/SKILL.md) | Whether a change can be proved at this store's traffic | `plan` |
| [Personalization Audit](skills/personalization-audit/SKILL.md) | Which onsite problem is worth fixing first | `recommendation` |

Full graph and selection guidance: [skills/README.md](skills/README.md).

## Four things this package insists on

**Every value carries where it came from.** A quantity is derived from this store's data, provisional from
a vertical default, stated by the store owner, or absent — and which one it is travels with it. A
provisional value that does not name the observation that would replace it is a disclaimer, not a plan
([rules/global-rules.md#G14](rules/global-rules.md)). The store owner cannot tell a measured threshold
from a borrowed one, which is exactly why the package says so.

**One customer has one attention budget.** Email & SMS, Reviews and Loyalty can each decide, correctly and
independently, to contact the same person on the same day. No single product can see the problem.
Onboarding is the only moment when all three programmes are designed at once, so it is where ownership of
each lifecycle moment is assigned and the aggregate is stated as a number
([rules/contact-ownership-rules.md](rules/contact-ownership-rules.md)).

**Creating is never activating.** Provisioning creates drafts. Activation is a separate gate, approved
one resource at a time with its recipient count stated
([rules/safety-rules.md#S2](rules/safety-rules.md)). "Approve the whole launch" is not available, even
when asked for.

**Consent decides the onsite work before value does.** Nothing that identifies, profiles or tracks a
visitor is planned before consent state is confirmed, and where it is absent the plan degrades to
non-personalised defaults rather than proceeding at lowered confidence
([rules/safety-rules.md#S15](rules/safety-rules.md)).

## The zero-history store

A store nine days old returns `absent` for nearly every derived value, and that is the most common
onboarding shape rather than an edge case. What it can still be given honestly: correct sequencing,
catalogue-shape decisions that need no order history, stated constraints, playbook defaults that are
labelled as such, and a review point expressed in orders rather than dates. What it cannot be given is a
personalised threshold — and every skill here is built to say so rather than produce one. See
[knowledge/evidence-and-provenance.md](knowledge/evidence-and-provenance.md).

## Architecture

```
┌──────────────────────────────────────────────┐
│ AI Agent host                                │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ TargetBay Onboarding Skills                  │  ← this package
│   skills · rules · knowledge                 │     HOW to onboard
└──────────────────┬───────────────────────────┘
                   ▼  declares required capabilities
┌──────────────────────────────────────────────┐
│ TargetBay MCP                                │  ← separate repository
│   all three products, one surface             │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ TargetBay platform                           │
└──────────────────────────────────────────────┘
```

Skills declare abstract capability identifiers — `onboarding.store_context`, not a tool name. The registry
is [capabilities.yaml](capabilities.yaml), fifteen entries covering the orchestration capabilities no
product owns and the onsite reads and writes the first step depends on. The mapping to real MCP tools is
**TODO** for every entry in this release. See [docs/mcp-integration.md](docs/mcp-integration.md), which
also records the fourteen questions that mapping has to settle before any skill here can execute.

## Status

`0.2.0`. Skill reasoning is expected to be stable; capability identifiers may change as the real MCP
surface is mapped. `onboarding.provisioning` is unverified — no TargetBay write surface has been
inspected. See [CHANGELOG.md](CHANGELOG.md) for known gaps.

---

[CONTRIBUTING.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/CONTRIBUTING.md) ·
[SECURITY.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/SECURITY.md) ·
[CHANGELOG.md](CHANGELOG.md)
