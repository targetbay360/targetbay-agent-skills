# MCP Integration

## The boundary

**TargetBay Personalization MCP = what the agent can do. TargetBay Personalization Skills = how the agent
should accomplish an onsite objective.**

This package contains no MCP implementation, no API client, no endpoint definitions and no tool schemas.
It declares *capabilities* it needs, and the agent host supplies them through whatever the TargetBay
Personalization MCP exposes.

## Why capabilities instead of tool names

```
Skill
  ↓ declares
Required capability                  onsite.recommendation_placement
  ↓ mapped by this document (TODO)
Personalization MCP tool/resource    <not yet mapped>
```

Three reasons for the indirection:

1. **The skills and the MCP version independently.** A tool rename should not require editing every skill.
2. **Skills describe intent, not plumbing.** "I need placement configuration" is a durable statement;
   "I need `get_widget_config`" is a coupling.
3. **This package has not inspected the TargetBay Personalization MCP surface.** Inventing tool names
   would produce confident, wrong documentation — the exact failure the package's own rules prohibit
   ([../rules/global-rules.md#G3](../rules/global-rules.md)).

## Capability registry

The registry is [../capabilities.yaml](../capabilities.yaml) — the single source of truth. Every skill's
`targetbay.requires` entries are validated against it.

Each entry carries an `id`, a `description`, an `access` level (`read` / `write` / `send`), and
`mcp_tools`, which is **`TODO` for every capability in this release**.

## Mapping status

| Capability | Access | MCP tools | Status |
|---|---|---|---|
| `onsite.store_profile` | read | — | **TODO** |
| `onsite.visitor_intelligence` | read | — | **TODO** |
| `onsite.audience_definition` | write | — | **TODO** |
| `onsite.recommendation_placement` | write | — | **TODO** |
| `onsite.recommendation_analytics` | read | — | **TODO** |
| `onsite.offers` | write | — | **TODO** |
| `onsite.offer_analytics` | read | — | **TODO** |
| `onsite.search` | write | — | **TODO** |
| `onsite.product_intelligence` | read | — | **TODO** |
| `onsite.experimentation` | write | — | **TODO** |
| `onsite.experience_analytics` | read | — | **TODO** |
| `onsite.consent_and_tracking` | read | — | **TODO — blocks everything else** |

Mapping a capability means: naming the MCP tools or resources that satisfy it, recording the shape of what
they return, and confirming the access level matches. Until that is done, no skill in this package can
execute — they can only plan.

## The one capability that is not like the others

`onsite.consent_and_tracking` is a precondition rather than an input
([../rules/safety-rules.md#S2](../rules/safety-rules.md),
[../rules/global-rules.md#G5](../rules/global-rules.md)). Without it, no skill here may plan anything that
identifies or profiles a visitor — not at lowered confidence, not with a caveat. They degrade to
non-personalised defaults, which for several skills means blocking outright.

This is deliberately stricter than the treatment of other missing capabilities, because the consequence of
guessing is not a bad recommendation but processing somebody's behaviour without a basis for it.

## The questions this mapping has to settle

**Is consent state readable per visitor, or only per region?** The two produce materially different
designs. A per-region signal means the anonymous path becomes the default path in some markets; a
per-visitor signal means it is decided at request time.

**What does the platform enforce, and what does it expect the caller to enforce?** Frequency caps,
exclusions and consent gating must be enforced deterministically
([../rules/global-rules.md#G10](../rules/global-rules.md)). Where the platform does not enforce one, the
skills have to know, because a cap an agent is expected to honour by convention is not a cap
([../rules/targeting-rules.md#T8](../rules/targeting-rules.md)).

**Does `onsite.experimentation` expose a stopping condition?** [#S10](../rules/safety-rules.md) and
[../rules/measurement-rules.md#M4](../rules/measurement-rules.md) require a pre-declared stopping rule
that is honoured. If the platform auto-promotes a winner on an interim result, that behaviour has to be
recorded here and worked around, not discovered in production.

**How is cannibalisation observable?** [../rules/surface-rules.md#U5](../rules/surface-rules.md) requires
separating incremental from redirected revenue. Whether that is possible decides whether the measurement
skills can report incrementality at all, or only attribution.

## Authentication

Authentication is the host's concern, not this package's. No scope names appear in this package, because
no canonical scope list has been inspected, and inventing one would be the same error as inventing tool
names.

Skills never handle credentials. See
[SECURITY.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/SECURITY.md).

## How a skill uses a capability

1. Declares it in `targetbay.requires`
2. States, in `Required MCP Capabilities`, what it uses each one for
3. Handles its absence in `Failure Handling` — degrade to `partial`, or `blocked`
4. Records unavailable capabilities in `unmet_requirements` in the result

A skill never assumes a capability is present, and never simulates its result
([../rules/safety-rules.md#S15](../rules/safety-rules.md)).

## What the MCP must never delegate to skills

Deterministic enforcement stays on the platform: consent gating, frequency caps, inventory availability,
price, eligibility and regional restrictions. Skills plan within these; they do not approximate or bypass
them ([../rules/global-rules.md#G10](../rules/global-rules.md)).

## TODOs before connecting to the real Personalization MCP

- [ ] Inspect the TargetBay Personalization MCP tool and resource surface
- [ ] Map every capability in [../capabilities.yaml](../capabilities.yaml) to real tools; replace `TODO`
- [ ] Establish whether consent state is per visitor or per region, and what it gates
- [ ] Enumerate what the platform enforces deterministically versus what it expects the caller to honour
- [ ] Confirm whether frequency caps are per visitor across surfaces, or per campaign
- [ ] Confirm whether experiments support a declared stopping condition, and whether anything auto-promotes
- [ ] Establish whether cannibalisation is observable, since incrementality claims depend on it
- [ ] Confirm how a placement behaves when its strategy returns too few results, so the empty state can be
      designed rather than discovered
- [ ] Define how the MCP signals "capability unavailable" so skills can degrade rather than fabricate
