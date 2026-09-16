# Changelog

All notable changes to TargetBay Loyalty Skills are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this package adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-09-16

### Changed

- **The skill contract is thirteen sections, not fourteen.** `Inputs` is removed from every skill and
  from `tests/validate.py`; every skill is a MAJOR bump as a result.
- `docs/mcp-integration.md` no longer transcribes `capabilities.yaml`; it records the two capabilities
  that still carry an open question and points at the registry for the rest.
- `rules/README.md` no longer states the drift argument in terms of a skill count that will go stale.
- `docs/` is published to npm, so the README's links to it resolve in the tarball.
- Tautological lines beneath the `Approval Requirements` table are gone; the routing they carried stays.

### Fixed

- **Installed skills no longer cite files that are not there.** Both installers rewrite the
  `../../rules/`, `../../knowledge/` and `../../schemas/` citations that flattening breaks into the
  released URL for the installed version.
- `install.sh` installs slash commands alongside a `.claude` tree, matching `install.mjs`.
- `schemas/skill.schema.json` cited `docs/architecture.md`, which only the email-sms plugin carries; it
  now cites `rules/safety-rules.md#S1`.
- The marketplace and plugin descriptions named a reward catalogue and redemption health as covered
  work; no skill here decides either. They now name tier thresholds and referral economics, which do
  have skills.

## [0.1.0] - 2026-09-12

First release. Six skills, a capability registry, and the rules and knowledge they cite.

This is a `0.x` line because no TargetBay Loyalty MCP surface has been inspected yet. Every capability in
[capabilities.yaml](capabilities.yaml) maps to `TODO`, which means the skills can plan but cannot execute.
Skill reasoning is expected to be stable; capability identifiers may still change as the real MCP is
mapped.

### Added

- **Six skills.** `program-diagnosis` (analysis), `program-design` (plan), `points-economics`
  (recommendation), `tier-structure` (plan), `referral-program` (plan) and `member-recovery`
  (recommendation). `program-diagnosis` sits at the bottom of the composition graph; `points-economics` is
  the second-level shared dependency, so tier benefits and referral incentives are costed through one
  implementation rather than estimated separately.
- **Capability registry** with fourteen `loyalty.*` capabilities across read, write and send access.
  `loyalty.messaging` is flagged as possibly owned by BayEngage rather than by Loyalty;
  `loyalty.order_intelligence` may be satisfied by the commerce platform.
- **Rules.** `safety-rules.md` (S1–S15), `global-rules.md` (G1–G16), and domain rules for economics, tiers
  and referral. The rules that prohibit retroactively reducing earned value, changing economics without a
  liability projection, and bulk adjustment without a stated count are absolute.
- **Knowledge.** Loyalty principles and member lifecycle, cited by skills for *why* — including the
  selection problem, which is the single most common reason loyalty programmes are reported as working
  when they are not.
- **Three commands.** `/targetbay-loyalty:program-health`, `/targetbay-loyalty:points-review` and
  `/targetbay-loyalty:quiet-members`.
- **Contracts.** Skill, skill-result and recommendation JSON Schemas, validated by the repository's shared
  `tests/validate.py`.

### Known gaps

- No MCP tool mappings. See [docs/mcp-integration.md](docs/mcp-integration.md), which records four
  questions the mapping has to settle — who sends, where margin comes from, how liability is exposed, and
  whether bulk adjustment supports a preview. Without a preview form,
  [safety-rules.md#S4](rules/safety-rules.md) cannot be satisfied and bulk adjustment stays out of scope.
- No vertical playbooks. They will be added when there is real per-vertical evidence to put in them rather
  than invented defaults.
- Programme messaging is not yet reconciled with BayEngage. A store running both products must not have
  two systems independently deciding to contact the same member.
