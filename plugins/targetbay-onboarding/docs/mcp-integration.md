# MCP Integration

## The boundary

**TargetBay MCP = what the agent can do. TargetBay Onboarding Skills = how the agent should onboard a
store.**

This package contains no MCP implementation, no API client, no endpoint definitions and no tool schemas.
It declares *capabilities* it needs, and the agent host supplies them through whatever the TargetBay MCP
exposes.

## What makes this plugin different from the other three

The three product plugins each declare the capabilities of one product. This one declares two things
neither of those can: four orchestration capabilities that no single product owns — a derived view of the
whole store, the answers the platform cannot observe, a cross-product apply path, and activation — and
eleven onsite capabilities that belong to no product because onsite capture is not one.

It deliberately does **not** re-declare the forty-three product capabilities; a skill here that needs
product data reads it through [../capabilities.yaml](../capabilities.yaml)'s
`onboarding.store_context`, which is where the derived view of all three products arrives.

## Capability registry

The registry is [../capabilities.yaml](../capabilities.yaml) — the single source of truth. Every skill's
`requires:` entries are validated against it.

| Capability | Access | MCP tools | Status |
|---|---|---|---|
| `onboarding.store_context` | read | — | **TODO** |
| `onboarding.intake` | write | — | **TODO** |
| `onboarding.provisioning` | write | — | **TODO — capability itself unverified** |
| `onboarding.activation` | send | — | **TODO** |
| `onboarding.consent_and_tracking` | read | — | **TODO — blocks every onsite skill** |
| `onboarding.visitor_intelligence` | read | — | **TODO** |
| `onboarding.product_intelligence` | read | — | **TODO** |
| `onboarding.audience_definition` | write | — | **TODO** |
| `onboarding.recommendation_placement` | write | — | **TODO** |
| `onboarding.recommendation_analytics` | read | — | **TODO** |
| `onboarding.offers` | write | — | **TODO** |
| `onboarding.offer_analytics` | read | — | **TODO** |
| `onboarding.onsite_search` | write | — | **TODO** |
| `onboarding.experimentation` | write | — | **TODO** |
| `onboarding.experience_analytics` | read | — | **TODO** |

Mapping a capability means naming the MCP tools or resources that satisfy it, recording the shape of what
they return, and confirming the access level matches. Until that is done, no skill in this package can
execute — they can only plan.

## The Store Context Pack

`onboarding.store_context` is the one capability this plugin cannot do without, and it is not a raw read.
It returns a derived document: identity, detected vertical, catalogue shape, customer shape, brand
profile, existing coverage across all three products, and a per-capability readiness matrix. Its shape is
[../schemas/context-pack.schema.json](../schemas/context-pack.schema.json).

**Derivation belongs on the platform side, for two reasons.** Computing a lapse point means reading a
full inter-purchase-interval distribution, and pulling that through an agent's context to produce one
percentile is waste. More importantly, a skill that never sees the raw distribution cannot invent a
threshold from it — which turns [../rules/global-rules.md#G3](../rules/global-rules.md) from author
discipline into something structural.

Where the platform exposes only raw reads, the affected values come back `absent` with the observation
that would make them derivable. They are never estimated from whatever sample happened to be readable.

## The one capability that is not like the others

`onboarding.consent_and_tracking` is a precondition rather than an input
([../rules/safety-rules.md#S15](../rules/safety-rules.md),
[../rules/global-rules.md#G19](../rules/global-rules.md)). Without it, no skill here may plan anything
that identifies or profiles a visitor — not at lowered confidence, not with a caveat. They degrade to
non-personalised defaults, which for several skills means blocking outright.

This is deliberately stricter than the treatment of other missing capabilities, because the consequence of
guessing is not a bad recommendation but processing somebody's behaviour without a basis for it.

## Signalling capability unavailable

Every plugin in this marketplace records the same open question: how does the MCP say "I cannot do that"
so a skill degrades rather than fabricates? Onboarding needs two answers, because planning and execution
need different things.

**A manifest, for planning.** One read returning, per capability and per store, a status of `available`,
`unavailable` (the product has it; this store does not), `unverified` (the platform's own support is
unconfirmed) or `absent` (the platform does not have it). A skill reads this once at the start of a run
and populates `unmet_requirements` from it, which is what
[../schemas/skill-result.schema.json](../schemas/skill-result.schema.json) already expects and what
[../rules/safety-rules.md#S12](../rules/safety-rules.md) forbids faking.

**A result envelope, for execution.** Every tool returns a status alongside its data and does not throw
for an unavailable capability. An exception is indistinguishable from a transport failure and invites a
retry loop; a structured fact is something a skill can record.

**The rule underneath both: never return an empty success.** An empty payload with a success status is
the exact shape that causes fabrication, because "this store has no lapsed customers" and "the
lapsed-customer read is unavailable" arrive looking identical. They are different findings and must be
distinguishable.

## Provisioning: two separate operations

Creating and activating must be different calls.

A single call with an "activate" flag makes [../rules/safety-rules.md#S2](../rules/safety-rules.md) a
request written in markdown. Two calls make it something the host's own permission system can enforce —
allow creation, prompt on activation. Onboarding is the workflow where that distinction earns its keep,
because it is the one moment when a dozen irreversible actions are queued up behind a single plan.

Two further requirements follow from onboarding being re-run after partial failure more often than any
other workflow:

- **Stable resource references.** Re-applying a plan updates in place rather than duplicating.
- **A dry run that returns a per-resource diff** — create, update, no change or conflict — plus the blast
  radius: audience size per resource, and the maximum messages one customer could receive per week across
  all three products once the set is live ([../rules/contact-ownership-rules.md#X7](../rules/contact-ownership-rules.md)).

## Authentication

Authentication is the host's concern, not this package's. Skills never handle credentials. See
[SECURITY.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/SECURITY.md).

Onboarding adds one requirement the product plugins do not have: **the surface must be store-scoped from
the start.** Every call carries the store it acts on, and the host resolves the caller's authority over
that store. This costs nothing while an internal team is running the skills, and it is not retrofittable
once store owners run them themselves.

## What the MCP must never delegate to skills

Deterministic enforcement stays on the platform: consent, suppression, legal opt-out, sending limits and
hard frequency caps. Skills plan within these; they do not approximate or bypass them
([../rules/global-rules.md#G10](../rules/global-rules.md)).

The cross-product contact budget is the case that needs stating explicitly. This plugin's
[../rules/contact-ownership-rules.md](../rules/contact-ownership-rules.md) decides *who owns which
moment*; it cannot enforce a cap. If the platform cannot supply a unified frequency and consent view
across all three products, the budget in a blueprint is a plan rather than an enforcement, and the
blueprint must say so on its face (X9).

## TODOs before connecting to the real TargetBay MCP

- [ ] Inspect the TargetBay MCP tool and resource surface across all three products
- [ ] Map the fifteen capabilities in [../capabilities.yaml](../capabilities.yaml) to real tools; replace `TODO`
- [ ] Confirm whether a write surface exists for segments, journeys, templates, review triggers, loyalty
      configuration and onsite placements — `onboarding.provisioning` is unverified until it does
- [ ] Confirm that creation and activation are, or can be, separate operations
- [ ] Decide where the Store Context Pack is derived, and which of its values the platform can compute
- [ ] Decide where intake answers are stored so they outlive a session and are readable by every product
- [ ] Confirm whether a unified cross-product frequency and consent view exists
- [ ] Enumerate the OAuth scopes each capability requires
- [ ] Establish whether consent state is per visitor or per region, and what it gates — the two produce
      materially different onsite designs
- [ ] Confirm whether onsite frequency caps are per visitor across surfaces, or per campaign; a cap an
      agent is expected to honour by convention is not a cap
      ([../rules/targeting-rules.md#T8](../rules/targeting-rules.md))
- [ ] Confirm whether experiments support a declared stopping condition, and whether anything
      auto-promotes a winner on an interim result
      ([../rules/measurement-rules.md#M4](../rules/measurement-rules.md))
- [ ] Establish whether cannibalisation is observable, since incrementality claims depend on it
      ([../rules/surface-rules.md#U5](../rules/surface-rules.md))
- [ ] Confirm how a placement behaves when its strategy returns too few results, so the empty state can be
      designed rather than discovered
- [ ] Define how the MCP signals "capability unavailable", and how it distinguishes an empty result from
      an unavailable one
