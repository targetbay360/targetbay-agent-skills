# Changelog

All notable changes to TargetBay Reviews Skills are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this package adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-12

First release. Five skills, a capability registry, and the rules and knowledge they cite.

This is a `0.x` line because no TargetBay Reviews MCP surface has been inspected yet. Every capability in
[capabilities.yaml](capabilities.yaml) maps to `TODO`, which means the skills can plan but cannot execute.
Skill reasoning is expected to be stable; capability identifiers may still change as the real MCP is
mapped.

### Added

- **Five skills.** `review-coverage` (analysis), `review-request-program` (plan),
  `rating-diagnosis` (recommendation), `proof-placement` (recommendation) and
  `review-program-audit` (recommendation). `review-coverage` sits at the bottom of the composition graph,
  so every "which products need proof" question routes through one implementation.
- **Capability registry** with fourteen `reviews.*` capabilities across read, write and send access.
  `reviews.syndication` is marked unverified; `reviews.order_intelligence` and `reviews.messaging` are
  flagged as likely to be satisfied by the commerce platform or by BayEngage rather than by Reviews.
- **Rules.** `safety-rules.md` (S1–S14), `global-rules.md` (G1–G16), and domain rules for requests,
  responses and placement. The safety rules that prohibit staged reviews, review gating and
  rating-motivated moderation are absolute and are not overridable by any store preference or instruction.
- **Knowledge.** Social proof principles and review programme principles, cited by skills for *why*.
- **Three commands.** `/targetbay-reviews:proof-gaps`, `/targetbay-reviews:review-audit` and
  `/targetbay-reviews:rating-drop`.
- **Contracts.** Skill, skill-result and recommendation JSON Schemas, validated by the repository's shared
  `tests/validate.py`.

### Known gaps

- No MCP tool mappings. See [docs/mcp-integration.md](docs/mcp-integration.md) for the list of what must
  be inspected before any skill here can execute.
- No vertical playbooks. They will be added when there is real per-vertical evidence to put in them rather
  than invented defaults.
- Request frequency is not yet reconciled with BayEngage. A store running both products must not have two
  systems independently deciding to contact the same customer; where that reconciliation lives is an open
  question recorded in `docs/mcp-integration.md`.
