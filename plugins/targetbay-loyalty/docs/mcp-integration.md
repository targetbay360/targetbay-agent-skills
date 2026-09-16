# MCP Integration

## The boundary

**TargetBay Loyalty MCP = what the agent can do. TargetBay Loyalty Skills = how the agent should
accomplish a loyalty objective.**

This package contains no MCP implementation, no API client, no endpoint definitions and no tool schemas.
It declares *capabilities* it needs, and the agent host supplies them through whatever the TargetBay
Loyalty MCP exposes.

## Why capabilities instead of tool names

```
Skill
  ↓ declares
Required capability          loyalty.points_ledger
  ↓ mapped by this document (TODO)
Loyalty MCP tool/resource    <not yet mapped>
```

Three reasons for the indirection:

1. **The skills and the MCP version independently.** A tool rename should not require editing every skill.
2. **Skills describe intent, not plumbing.** "I need the points ledger" is a durable statement; "I need
   `get_member_points_history`" is a coupling.
3. **This package has not inspected the TargetBay Loyalty MCP surface.** Inventing tool names would
   produce confident, wrong documentation — the exact failure the package's own rules prohibit
   ([../rules/global-rules.md#G3](../rules/global-rules.md)).

## Capability registry

The registry is [../capabilities.yaml](../capabilities.yaml) — the single source of truth. Every skill's
`targetbay.requires` entries are validated against it.

Each entry carries an `id`, a `description`, an `access` level (`read` / `write` / `send`), and
`mcp_tools`, which is **`TODO` for every capability in this release**.

## Mapping status

All 14 capabilities in [../capabilities.yaml](../capabilities.yaml) are `mcp_tools: TODO`.
Rather than transcribe the registry here — two lists that drift — this section records only what
still needs a decision. Read the registry for ids, descriptions, access levels and notes.

| Capability | Access | Open question |
|---|---|---|
| `loyalty.order_intelligence` | read | may belong to the commerce platform |
| `loyalty.messaging` | send | capability ownership unverified |

Mapping a capability means: naming the MCP tools or resources that satisfy it, recording the shape of what
they return, and confirming the access level matches. Until that is done, no skill in this package can
execute — they can only plan.

## The questions this mapping has to settle

**Who sends?** `loyalty.messaging` is declared here because the skills need programme communication —
tier changes, balance and expiry notices. It may well be owned by TargetBay Email & SMS rather than by Loyalty. A
store running both must not end up with two systems independently contacting the same member
([../rules/global-rules.md#G13](../rules/global-rules.md)). Where the reconciliation lives has to be
recorded here before any skill plans a send.

**Where does margin come from?** [../rules/economics-rules.md#E2](../rules/economics-rules.md) requires
margin posture before an earn rate can be set responsibly. If neither Loyalty nor the commerce platform
exposes it, the economics skills degrade to `partial` permanently, and that should be known rather than
discovered.

**How is liability exposed?** [../rules/safety-rules.md#S3](../rules/safety-rules.md) requires a liability
projection on every economics recommendation. Whether `loyalty.points_ledger` returns outstanding balance
with ageing, or only individual events, decides whether that projection is a read or a computation.

**What does a bulk adjustment look like?** [#S4](../rules/safety-rules.md) requires the affected count and
value before approval. If `loyalty.points_adjustment` has no dry-run or preview form, the skills cannot
satisfy that rule and must stop short of bulk adjustment entirely.

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

Deterministic enforcement stays on the platform: balance arithmetic, tier qualification, expiry
enforcement, redemption eligibility, consent and suppression. Skills plan within these; they do not
approximate or bypass them ([../rules/global-rules.md#G10](../rules/global-rules.md)).

## TODOs before connecting to the real Loyalty MCP

- [ ] Inspect the TargetBay Loyalty MCP tool and resource surface
- [ ] Map every capability in [../capabilities.yaml](../capabilities.yaml) to real tools; replace `TODO`
- [ ] Confirm whether outstanding liability and its ageing are directly readable
- [ ] Confirm whether `loyalty.points_adjustment` supports a preview or dry run; without one, bulk
      adjustment is out of scope for every skill here
- [x] **Confirm whether programme messaging is owned by Loyalty or by TargetBay Email & SMS, and where
      frequency is reconciled between them.** Answered in
      [contact-ownership-rules.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-onboarding/rules/contact-ownership-rules.md) — X2 gives Loyalty the programme-state moment, and X5
      dispatches those messages through Email & SMS until the capability manifest confirms
      `loyalty.messaging` for a store, so they are counted once against the one cross-product contact
      budget. Ownership of the moment is settled; the dispatch capability is still an MCP question.
- [ ] Confirm whether margin data is reachable, and from which system
- [ ] Confirm how tier qualification windows are configured and whether they are changeable in-flight
- [ ] Define how the MCP signals "capability unavailable" so skills can degrade rather than fabricate,
      and how it distinguishes an empty result from an unavailable one — "this member has no points"
      and "the ledger read failed" must not arrive looking identical
