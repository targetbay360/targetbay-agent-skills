# TargetBay Personalization Skills

A vendor-neutral AI Agent Skills package that teaches agents **how to plan, target and measure onsite
personalization** using TargetBay Personalization.

[![version](https://img.shields.io/badge/version-0.1.0-blue)](VERSION)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![agent skills](https://img.shields.io/badge/Agent%20Skills-conformant-7c3aed)](https://agentskills.io/specification)

---

## Install

<table>
<tr><th>Claude Code</th><td>

```
/plugin marketplace add targetbay360/targetbay-agent-skills
/plugin install targetbay-personalization@targetbay
```

</td></tr>
<tr><th>npm</th><td>

```bash
npx @targetbay/personalization-skills --global
```

`--global` writes to `~/.claude/skills`. Omit it for `./.claude/skills`, or pass `--dest <dir>` for any
other host.

</td></tr>
</table>

### Try it

```
/targetbay-personalization:audit-experience
/targetbay-personalization:surface-map
/targetbay-personalization:search-gaps
```

Or just ask: *"What personalization do we actually have running?"* ·
*"Our widget recommends things people just bought."* · *"The variant is up 18% after three days — ship it?"*

With no TargetBay Personalization MCP connected, a skill will report itself **`blocked`** and name the
capability it is missing. That is the correct answer, and it is the quickest confirmation that the skills
loaded.

---

## What this is

TargetBay Personalization exposes its platform capabilities through an MCP server. That tells an agent
*what it can do*. It does not tell the agent which surface hosts which decision, what an anonymous visitor
should see, whether an offer is discounting demand that was already converting, or whether this store's
traffic can resolve the test somebody wants to run.

This package is that second half.

```
Personalization MCP    =  what the agent CAN do
Personalization Skills =  how the agent SHOULD accomplish an onsite objective
```

## What this is not

- **Not** the TargetBay Personalization MCP — no tools, no resources, no server
- **Not** the TargetBay Personalization API — no clients, endpoints or request code
- **Not** a recommendation engine, offer engine or search engine
- **Not** a collection of prompt files — it is a versioned package with contracts, schemas and validation

No file in this package makes a network call.

## Skills

| Skill | Decides | Risk |
|---|---|---|
| [Surface Inventory](skills/surface-inventory/SKILL.md) | What is running, and what consent permits | `analysis` |
| [Recommendation Strategy](skills/recommendation-strategy/SKILL.md) | What to recommend, where, and to whom | `plan` |
| [Offer Targeting](skills/offer-targeting/SKILL.md) | Who sees an offer, when, and whether it should exist | `plan` |
| [Onsite Search](skills/onsite-search/SKILL.md) | What failing queries mean and how to fix them | `recommendation` |
| [Experience Experimentation](skills/experience-experimentation/SKILL.md) | Whether a change can be proved here, and how | `plan` |
| [Personalization Audit](skills/personalization-audit/SKILL.md) | What is most worth fixing first | `recommendation` |

Full graph and selection guidance: [skills/README.md](skills/README.md).

## The lines this package will not cross

Four of them are absolute, and no store preference, objective or instruction inside a skill run overrides
them ([rules/safety-rules.md](rules/safety-rules.md)):

- **Consent is a precondition, not a setting.** Nothing that identifies or profiles a visitor is planned
  without confirming consent state. Its absence blocks rather than degrades (S2).
- **No targeting on sensitive attributes, or their proxies.** Health, pregnancy, sexuality, religion,
  ethnicity, immigration status, financial distress and political affiliation — including when inferred
  from browsing rather than collected. A rejected proposal names the proxy it used (S3).
- **No price variation by visitor.** Varying which products and offers a visitor sees is merchandising.
  Varying the price of the same product is not, under any framing (S4).
- **No experience the visitor cannot escape.** Dismissals that work, frequency caps that hold, and no
  pattern making declining harder than accepting (S5).

And one discipline that is not a safety rule but catches more errors than any of them: **a test is never
stopped because it is winning** (S10). A test stopped for any other reason is reported as inconclusive,
never as a result.

## Architecture

```
┌──────────────────────────────────────────────┐
│ AI Agent host                                │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ TargetBay Personalization Skills             │  ← this package
│   skills · rules · knowledge                 │     HOW to decide
└──────────────────┬───────────────────────────┘
                   ▼  declares required capabilities
┌──────────────────────────────────────────────┐
│ TargetBay Personalization MCP                │  ← separate repository
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ TargetBay Personalization platform           │
└──────────────────────────────────────────────┘
```

Skills declare abstract capability identifiers — `onsite.recommendation_placement`, not a tool name. The
registry is [capabilities.yaml](capabilities.yaml) and the mapping to real MCP tools is **TODO** for every
entry in this release. See [docs/mcp-integration.md](docs/mcp-integration.md), which also records the four
questions that mapping has to settle before any skill here can execute.

## Status

`0.1.0`. Skill reasoning is expected to be stable; capability identifiers may change as the real MCP
surface is mapped. See [CHANGELOG.md](CHANGELOG.md) for known gaps.

---

[CONTRIBUTING.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/CONTRIBUTING.md) ·
[SECURITY.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/SECURITY.md) ·
[CHANGELOG.md](CHANGELOG.md)
