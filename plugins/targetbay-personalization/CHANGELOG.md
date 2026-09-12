# Changelog

All notable changes to TargetBay Personalization Skills are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this package adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-12

First release. Six skills, a capability registry, and the rules and knowledge they cite.

This is a `0.x` line because no TargetBay Personalization MCP surface has been inspected yet. Every
capability in [capabilities.yaml](capabilities.yaml) maps to `TODO`, which means the skills can plan but
cannot execute. Skill reasoning is expected to be stable; capability identifiers may still change as the
real MCP is mapped.

### Added

- **Six skills.** `surface-inventory` (analysis), `recommendation-strategy` (plan), `offer-targeting`
  (plan), `onsite-search` (recommendation), `experience-experimentation` (plan) and
  `personalization-audit` (recommendation). `surface-inventory` sits at the bottom of the composition
  graph; the change-making skills hand off to `experience-experimentation` when a change should be proved
  rather than asserted.
- **Capability registry** with twelve `onsite.*` capabilities across read and write access.
  `onsite.consent_and_tracking` is treated differently from the rest: it is a precondition, and its
  absence blocks rather than degrades.
- **Rules.** `safety-rules.md` (S1–S15), `global-rules.md` (G1–G16), and domain rules for targeting,
  surfaces and measurement. Four safety rules are absolute: consent as a precondition, no targeting on
  sensitive attributes or their proxies, no price variation by visitor, and no experience a visitor cannot
  escape.
- **Knowledge.** Personalization principles and visitor behaviour, cited by skills for *why* — including
  that most traffic is anonymous, which is the design problem rather than an edge case.
- **Three commands.** `/targetbay-personalization:audit-experience`,
  `/targetbay-personalization:surface-map` and `/targetbay-personalization:search-gaps`.
- **Contracts.** Skill, skill-result and recommendation JSON Schemas, validated by the repository's shared
  `tests/validate.py`.

### Known gaps

- No MCP tool mappings. See [docs/mcp-integration.md](docs/mcp-integration.md), which records four
  questions the mapping has to settle — whether consent is per visitor or per region, what the platform
  enforces versus what it expects the caller to honour, whether experiments support a declared stopping
  condition, and whether cannibalisation is observable. The last one decides whether any skill here can
  claim incrementality rather than attribution.
- No vertical playbooks. They will be added when there is real per-vertical evidence to put in them rather
  than invented defaults.
