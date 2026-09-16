# MCP Integration

## The boundary

**TargetBay Reviews MCP = what the agent can do. TargetBay Reviews Skills = how the agent should
accomplish a proof objective.**

This package contains no MCP implementation, no API client, no endpoint definitions and no tool schemas.
It declares *capabilities* it needs, and the agent host supplies them through whatever the TargetBay
Reviews MCP exposes.

## Why capabilities instead of tool names

```
Skill
  ↓ declares
Required capability          reviews.product_coverage
  ↓ mapped by this document (TODO)
Reviews MCP tool/resource    <not yet mapped>
```

Three reasons for the indirection:

1. **The skills and the MCP version independently.** A tool rename should not require editing every skill.
2. **Skills describe intent, not plumbing.** "I need product coverage" is a durable statement; "I need
   `get_product_review_summary`" is a coupling.
3. **This package has not inspected the TargetBay Reviews MCP surface.** Inventing tool names would
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
| `reviews.syndication` | write | capability itself unverified |
| `reviews.order_intelligence` | read | may belong to the commerce platform |

Mapping a capability means: naming the MCP tools or resources that satisfy it, recording the shape of what
they return, and confirming the access level matches. Until that is done, no skill in this package can
execute — they can only plan.

## Two capabilities that may not live here

`reviews.order_intelligence` and `reviews.messaging` are the two most likely to be satisfied by a system
other than TargetBay Reviews.

Request timing depends on fulfilment, which the commerce platform owns
([../rules/request-rules.md#R1](../rules/request-rules.md)). Request delivery may be owned by TargetBay Email & SMS
rather than by Reviews. Both are declared here because the skills genuinely need them; where they turn out
to be supplied elsewhere, this document records which system answers, and the skills are unchanged.

A store running both TargetBay Email & SMS and Reviews must not end up with two systems independently deciding to
contact the same customer. Whichever system sends, request frequency is reconciled in one place, and this
document must record where.

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
([../rules/safety-rules.md#S14](../rules/safety-rules.md)).

## What the MCP must never delegate to skills

Deterministic enforcement stays on the platform: consent, suppression, request frequency caps,
verified-buyer determination and moderation policy enforcement. Skills plan within these; they do not
approximate or bypass them ([../rules/global-rules.md#G10](../rules/global-rules.md)).

## TODOs before connecting to the real Reviews MCP

- [ ] Inspect the TargetBay Reviews MCP tool and resource surface
- [ ] Map every capability in [../capabilities.yaml](../capabilities.yaml) to real tools; replace `TODO`
- [x] **Confirm whether review requests are dispatched by Reviews or by TargetBay Email & SMS, and where
      request frequency is reconciled between them.** Answered in
      [contact-ownership-rules.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-onboarding/rules/contact-ownership-rules.md) — X2 gives Reviews the post-purchase and delivery moment, so
      the first ask is Reviews'; X6 reconciles its frequency against the one cross-product contact
      budget rather than against a Reviews-only cap. Which system physically dispatches is still an MCP
      question; who owns the moment is not.
- [ ] Confirm whether fulfilment and delivery timing is reachable, and from which system
- [ ] Confirm whether syndication exists at all, and to which destinations
- [ ] Establish how verified-buyer state is determined and exposed
- [ ] Define how the MCP signals "capability unavailable" so skills can degrade rather than fabricate,
      and how it distinguishes an empty result from an unavailable one — "this product has no reviews"
      and "the review read failed" must not arrive looking identical
- [ ] Record whether merchant replies are published immediately or queued for moderation, since the risk
      classification in [../rules/safety-rules.md#S1](../rules/safety-rules.md) depends on the answer
