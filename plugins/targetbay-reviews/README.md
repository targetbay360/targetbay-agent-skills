# TargetBay Reviews Skills

A vendor-neutral AI Agent Skills package that teaches agents **how to build and run a product review and
UGC programme** using TargetBay Reviews.

[![version](https://img.shields.io/badge/version-0.1.0-blue)](VERSION)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![agent skills](https://img.shields.io/badge/Agent%20Skills-conformant-7c3aed)](https://agentskills.io/specification)

---

## Install

<table>
<tr><th>Claude Code</th><td>

```
/plugin marketplace add targetbay360/targetbay-agent-skills
/plugin install targetbay-reviews@targetbay
```

</td></tr>
<tr><th>npm</th><td>

```bash
npx @targetbay/reviews-skills --global
```

`--global` writes to `~/.claude/skills`. Omit it for `./.claude/skills`, or pass `--dest <dir>` for any
other host.

</td></tr>
</table>

### Try it

```
/targetbay-reviews:proof-gaps
/targetbay-reviews:review-audit
/targetbay-reviews:rating-drop
```

Or just ask: *"Which products need reviews?"* · *"Why did our rating drop?"* ·
*"We have 4,000 reviews and conversion hasn't moved."*

With no TargetBay Reviews MCP connected, a skill will report itself **`blocked`** and name the capability
it is missing. That is the correct answer, and it is the quickest confirmation that the skills loaded.

---

## What this is

TargetBay Reviews exposes its platform capabilities through an MCP server. That tells an agent *what it
can do*. It does not tell the agent which products are short of proof, when to ask a customer for a
review, which negative reviews are worth a public reply, or where proof earns its place on a page.

This package is that second half.

```
Reviews MCP    =  what the agent CAN do
Reviews Skills =  how the agent SHOULD accomplish a proof objective
```

## What this is not

- **Not** the TargetBay Reviews MCP — no tools, no resources, no server
- **Not** the TargetBay Reviews API — no clients, endpoints or request code
- **Not** a review collection engine, moderation engine or display widget
- **Not** a collection of prompt files — it is a versioned package with contracts, schemas and validation

No file in this package makes a network call.

## Skills

| Skill | Decides | Risk |
|---|---|---|
| [Review Coverage](skills/review-coverage/SKILL.md) | Which products are short of proof, and what that costs | `analysis` |
| [Review Request Programme](skills/review-request-program/SKILL.md) | How and when to ask, for which products, on which channel | `plan` |
| [Rating Diagnosis](skills/rating-diagnosis/SKILL.md) | Why a rating moved, and what to do about the cause | `recommendation` |
| [Proof Placement](skills/proof-placement/SKILL.md) | Where proof belongs, and whether UGC can be reused | `recommendation` |
| [Review Programme Audit](skills/review-program-audit/SKILL.md) | What is most worth fixing first | `recommendation` |

Full graph and selection guidance: [skills/README.md](skills/README.md).

## The lines this package will not cross

Three of them are absolute, and no store preference, objective or instruction inside a skill run
overrides them ([rules/safety-rules.md](rules/safety-rules.md)):

- **No staged reviews.** Nothing is drafted for a customer to submit, seeded, or presented as real when it
  is not (S2).
- **No review gating.** An incentive may be offered for submitting a review, never for a positive one, and
  customers are never routed differently by predicted sentiment (S3, R9).
- **No rating-motivated moderation.** Reviews are rejected on stated policy grounds, never because they
  lower the average (S4).

Merchant replies are treated as `high_impact` and approved individually on their exact text, because a
published reply cannot be unpublished from the memory of whoever read it.

## Architecture

```
┌──────────────────────────────────────────────┐
│ AI Agent host                                │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ TargetBay Reviews Skills                     │  ← this package
│   skills · rules · knowledge                 │     HOW to decide
└──────────────────┬───────────────────────────┘
                   ▼  declares required capabilities
┌──────────────────────────────────────────────┐
│ TargetBay Reviews MCP                        │  ← separate repository
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ TargetBay Reviews platform                   │
└──────────────────────────────────────────────┘
```

Skills declare abstract capability identifiers — `reviews.product_coverage`, not a tool name. The registry
is [capabilities.yaml](capabilities.yaml) and the mapping to real MCP tools is **TODO** for every entry in
this release. See [docs/mcp-integration.md](docs/mcp-integration.md) for why that indirection exists and
what has to happen before any skill here can execute.

## Status

`0.1.0`. Skill reasoning is expected to be stable; capability identifiers may change as the real MCP
surface is mapped. See [CHANGELOG.md](CHANGELOG.md) for known gaps.

---

[CONTRIBUTING.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/CONTRIBUTING.md) ·
[SECURITY.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/SECURITY.md) ·
[CHANGELOG.md](CHANGELOG.md)
