# MCP Integration

## The boundary

**TargetBay Email & SMS MCP = what the agent can do. TargetBay Email & SMS Skills = how the agent should
accomplish a marketing objective.**

This package contains no MCP implementation, no API client, no endpoint definitions and no tool schemas.
It declares *capabilities* it needs, and the agent host supplies them through whatever TargetBay Email & SMS MCP
exposes.

## Why capabilities instead of tool names

```
Skill
  ↓ declares
Required capability          email_sms.customer_intelligence
  ↓ mapped by this document (TODO)
TargetBay Email & SMS MCP tool/resource  <not yet mapped>
```

Three reasons for the indirection:

1. **The skills and the MCP version independently.** A tool rename should not require editing fourteen
   skills.
2. **Skills describe intent, not plumbing.** "I need customer intelligence" is a durable statement; "I need
   `get_customer_360`" is a coupling.
3. **This package has not inspected the TargetBay Email & SMS MCP surface.** Inventing tool names would produce
   confident, wrong documentation — the exact failure the package's own rules prohibit.

## Capability registry

The registry is [../capabilities.yaml](../capabilities.yaml) — the single source of truth. Every skill's
`requires:` entries are validated against it.

Each entry carries an `id`, a `description`, an `access` level (`read` / `write` / `send`), and
`mcp_tools`, which is **`TODO` for every capability in this release**.

## Mapping status

All 18 capabilities in [../capabilities.yaml](../capabilities.yaml) are `mcp_tools: TODO`.
Rather than transcribe the registry here — two lists that drift — this section records only what
still needs a decision. Read the registry for ids, descriptions, access levels and notes.

| Capability | Access | Open question |
|---|---|---|
| `email_sms.messaging_sms` | send | capability itself unverified |
| `email_sms.sending_infrastructure` | read | whether authentication record state, alignment and warm-up posture are readable at all. Every sending platform holds this; whether the MCP exposes it has never been inspected |
| `email_sms.event_stream` | read | whether an MCP surface can expose a push subscription at all, or whether subscription is configured out of band |
| `email_sms.event_tracking` | write | whether event names are enumerated, and whether a recorded event can trigger a platform automation |

Mapping a capability means: naming the MCP tools or resources that satisfy it, recording the shape of what
they return, and confirming the access level matches. Until that is done, no skill in this package can
execute — they can only plan.

The capabilities added in 4.2.0, the one deliberately **not** added, and which unconfirmed shapes block
which skill are set out in
[the capability gap analysis](https://github.com/targetbay360/targetbay-agent-skills/blob/main/docs/mcp-capability-gap-analysis.md).
The headline: contact-level journey membership is the single missing shape that degrades three skills.

## Observed prior art — not authoritative

Two non-MCP TargetBay Email & SMS integrations exist in adjacent repositories and were inspected while
writing this package:

- An OpenAI Agents SDK toolkit exposing tools named in a `bayengage_<verb>_<noun>` style, covering
  contacts, campaigns, templates, drip sequences, A/B tests and newsletters. That prefix is quoted as
  observed — it is the adjacent repository's own naming, not this package's, and renaming it here would
  misreport what was inspected.
- An n8n community node with a resource/operation matrix covering contacts, lists, campaigns, templates
  and event tracking, plus webhook events for campaign, contact, list and order activity. Its campaign
  operations are read, list, send and reports — there is **no create operation**. Programmatic campaign
  creation is therefore unverified, and no skill may assume it. A large share of that repository's own
  published example workflows call a campaign-create operation the node does not implement; this was
  found by reading the node rather than by running them.

These are recorded here as **evidence of an existing naming convention**, not as the MCP surface. Neither
is an MCP server. No name from either has been copied into a skill, and none should be until the actual
TargetBay Email & SMS MCP has been inspected.

Notable coverage gap in both: **SMS appears nowhere**, which is why `email_sms.messaging_sms` is marked
unverified throughout this package.

## Authentication

Authentication is the host's concern, not this package's. The TargetBay Email & SMS MCP is described as using Hydra
OAuth; the adjacent integrations use a mix of client-credentials OAuth and header API keys.

No scope names appear in this package. No canonical TargetBay Email & SMS scope list was found during
inspection, and inventing one would be the same error as inventing tool names.

Skills never handle credentials. See [SECURITY.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/SECURITY.md).

## How a skill uses a capability

1. Declares it in `requires:`
2. States, in `Required MCP Capabilities`, what it uses each one for
3. Handles its absence in `Failure Handling` — degrade to `partial`, or `blocked`
4. Records unavailable capabilities in `unmet_requirements` in the result

A skill never assumes a capability is present, and never simulates its result
([../rules/safety-rules.md#S12](../rules/safety-rules.md)).

## What the MCP must never delegate to skills

Deterministic enforcement stays on the platform: consent, suppression, legal opt-out, sending limits and
hard frequency caps. Skills plan within these; they do not approximate or bypass them
([../rules/global-rules.md#G10](../rules/global-rules.md)).

## TODOs before connecting to the real TargetBay Email & SMS MCP

- [ ] Inspect the TargetBay Email & SMS MCP tool and resource surface
- [ ] Map every capability in [../capabilities.yaml](../capabilities.yaml) to real tools; replace `TODO`
- [ ] Confirm whether SMS dispatch exists, and its consent and quiet-hours semantics
- [ ] Enumerate the Hydra OAuth scopes each capability requires
- [ ] Decide which layer enforces suppression and frequency caps, and record the decision
- [ ] Define how the MCP signals "capability unavailable" so skills can degrade rather than fabricate,
      and how it distinguishes an empty result from an unavailable one — "this campaign has no results" and "the results read failed"
      must not arrive looking identical
- [ ] Confirm the concrete automation node types the platform supports, against the abstract vocabulary in
      [../schemas/workflow.schema.json](../schemas/workflow.schema.json)
- [ ] Confirm whether `email_sms.marketing_calendar` is a real capability or must be assembled from
      campaign and automation reads
- [ ] Confirm whether campaign creation exists in the MCP surface at all; the inspected node has none,
      and several skills would plan differently if a campaign can only be selected rather than created
- [ ] Confirm how subscription to `email_sms.event_stream` is configured — through the MCP, or out of band
- [ ] Confirm whether an event recorded through `email_sms.event_tracking` can trigger a platform
      automation. If it cannot, every store-pushed trigger needs an external orchestrator, which is the
      decision `automation-orchestration` owns
