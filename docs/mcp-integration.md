# MCP Integration

## The boundary

**BayEngage MCP = what the agent can do. BayEngage Skills = how the agent should accomplish a marketing
objective.**

This package contains no MCP implementation, no API client, no endpoint definitions and no tool schemas.
It declares *capabilities* it needs, and the agent host supplies them through whatever BayEngage MCP
exposes.

## Why capabilities instead of tool names

```
Skill
  ↓ declares
Required capability          bayengage.customer_intelligence
  ↓ mapped by this document (TODO)
BayEngage MCP tool/resource  <not yet mapped>
```

Three reasons for the indirection:

1. **The skills and the MCP version independently.** A tool rename should not require editing fourteen
   skills.
2. **Skills describe intent, not plumbing.** "I need customer intelligence" is a durable statement; "I need
   `get_customer_360`" is a coupling.
3. **This package has not inspected the BayEngage MCP surface.** Inventing tool names would produce
   confident, wrong documentation — the exact failure the package's own rules prohibit.

## Capability registry

The registry is [../capabilities.yaml](../capabilities.yaml) — the single source of truth. Every skill's
`requires:` entries are validated against it.

Each entry carries an `id`, a `description`, an `access` level (`read` / `write` / `send`), and
`mcp_tools`, which is **`TODO` for every capability in this release**.

## Mapping status

| Capability | Access | MCP tools | Status |
|---|---|---|---|
| `bayengage.store_profile` | read | — | **TODO** |
| `bayengage.customer_intelligence` | read | — | **TODO** |
| `bayengage.product_intelligence` | read | — | **TODO** |
| `bayengage.order_intelligence` | read | — | **TODO** |
| `bayengage.segmentation` | write | — | **TODO** |
| `bayengage.campaign_management` | write | — | **TODO** |
| `bayengage.campaign_analytics` | read | — | **TODO** |
| `bayengage.automation` | write | — | **TODO** |
| `bayengage.automation_analytics` | read | — | **TODO** |
| `bayengage.template_management` | write | — | **TODO** |
| `bayengage.messaging_email` | send | — | **TODO** |
| `bayengage.messaging_sms` | send | — | **TODO — capability itself unverified** |
| `bayengage.suppression_and_consent` | read | — | **TODO** |
| `bayengage.marketing_calendar` | read | — | **TODO** |
| `bayengage.experimentation` | write | — | **TODO** |

Mapping a capability means: naming the MCP tools or resources that satisfy it, recording the shape of what
they return, and confirming the access level matches. Until that is done, no skill in this package can
execute — they can only plan.

## Authentication

Authentication is the host's concern, not this package's.

No scope names appear in this package. No canonical BayEngage scope list was found during inspection, and
inventing one would be the same error as inventing tool names.

Skills never handle credentials. See [../SECURITY.md](../SECURITY.md).

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

## TODOs before connecting to the real BayEngage MCP

- [ ] Inspect the BayEngage MCP tool and resource surface
- [ ] Map every capability in [../capabilities.yaml](../capabilities.yaml) to real tools; replace `TODO`
- [ ] Confirm whether SMS dispatch exists, and its consent and quiet-hours semantics
- [ ] Enumerate the OAuth scopes each capability requires
- [ ] Decide which layer enforces suppression and frequency caps, and record the decision
- [ ] Define how the MCP signals "capability unavailable" so skills can degrade rather than fabricate
- [ ] Confirm the concrete automation node types the platform supports, against the abstract vocabulary in
      [../schemas/workflow.schema.json](../schemas/workflow.schema.json)
- [ ] Confirm whether `bayengage.marketing_calendar` is a real capability or must be assembled from
      campaign and automation reads
