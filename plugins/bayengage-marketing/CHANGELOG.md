# Changelog

All notable changes to TargetBay Email & SMS Marketing Skills are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this package adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). See [docs/versioning.md](docs/versioning.md)
for how package and per-skill versions relate.

## [2.1.0] - 2026-09-12

Moved into the TargetBay Agent Skills marketplace. No skill content changed — all 24 skills, their
versions and their reasoning are byte-identical to 2.0.0. What changed is where the package lives and
what it is called.

### Changed

- **The repository is now a marketplace of product plugins.** This package moved from the repository root
  to `plugins/bayengage-marketing/`, alongside plugins for other TargetBay products. Every skill's
  relative links to `../../rules/`, `../../knowledge/`, `../../schemas/` and `../../capabilities.yaml`
  are unchanged, because the whole package moved together and remains self-contained.
- **Repository renamed** to `targetbay360/targetbay-agent-skills`. GitHub redirects the old URL, so an
  existing `/plugin marketplace add targetbay360/targetbay-email-sms-marketing-skills` keeps resolving,
  but re-adding the new source is recommended.
- **npm package renamed** to `@targetbay/bayengage-marketing-skills`. The old name,
  `@targetbay/targetbay-email-sms-marketing-skills`, is deprecated and points here.
- **Releases are tagged `bayengage-marketing@<version>`** rather than `v<version>`, so each product plugin
  releases independently. `scripts/install.sh` now resolves the latest release matching that prefix and
  extracts `plugins/bayengage-marketing/skills/` from the tarball.
- **Links from inside this plugin to repository-level files** (`SECURITY.md`, `CONTRIBUTING.md`,
  `tests/`) are now absolute GitHub URLs. A relative path to them would be dead for anyone who installed
  the plugin, since Claude Code ships only what lives under the plugin directory.

### Unchanged

- Plugin name `bayengage-marketing`, so every `/bayengage-marketing:*` command keeps working
- Marketplace name `targetbay`, so `/plugin install bayengage-marketing@targetbay` is unchanged
- All 24 skill names, versions, capabilities and composition edges

## [2.0.0] - 2026-09-12

Conforms to the [Agent Skills specification](https://agentskills.io/specification), and ships. The
package was content-complete but uninstallable: no git repository, no manifests, no release, and
frontmatter the spec's own reference validator rejects.

### Changed — BREAKING

- **Skill frontmatter now matches the Agent Skills specification exactly.** The reference validator
  (`skills_ref.validator.ALLOWED_FIELDS`) permits only `name`, `description`, `license`,
  `compatibility`, `metadata` and `allowed-tools` at the top level, so all 24 skills failed it. The
  eight package-specific keys — `display_name`, `version`, `category`, `requires`, `composes`,
  `risk_level`, `execution_mode`, `status` — moved under `metadata` as `targetbay.*` string values.
  Lists are comma-separated because `metadata` admits no other type.
- `schemas/skill.schema.json` rewritten around that shape: the top level is closed to the six spec
  fields, and the former patterns and enums now constrain the `metadata.targetbay.*` strings.
- Anything reading a skill's `requires` or `composes` must now read
  `metadata["targetbay.requires"]` and split on commas. `tests/validate.py` and
  `tests/evals/run_evals.py` do this through a shared `meta_list` helper.
- Folded (`>-`) descriptions flattened to single-line scalars. The spec parser is `strictyaml`, not
  PyYAML; single-line plain scalars remove any question about how it treats folded blocks.
- `VERSION` 1.2.0 → 2.0.0.

### Added

- **Claude Code plugin.** `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` make the
  repository a self-hosting one-plugin marketplace:
  `/plugin marketplace add targetbay360/targetbay-email-sms-marketing-skills`, then
  `/plugin install bayengage-marketing@targetbay`.
- **Six slash commands** in `commands/` — `/plan-month`, `/what-now`, `/win-back`, `/holiday`,
  `/diagnose`, `/audit-automations`. Thin routers to the skills that already own the reasoning, so a
  customer does not have to know 24 skill names. Each restates the plan-only constraint.
- **npm package** `@targetbay/targetbay-email-sms-marketing-skills`, with a zero-dependency installer
  (`scripts/install.mjs`) that copies skills into `./.claude/skills`, `~/.claude/skills` or any
  `--dest`. Mirrored to GitHub Packages, which needs a token even for public reads — npmjs is the
  documented path.
- **`scripts/install.sh`** — POSIX `curl | sh` install from the latest release tarball, for hosts with
  neither a plugin system nor npm.
- **CI.** `.github/workflows/validate.yml` runs both test suites, the `agentskills validate` CLI over
  every skill, manifest parsing, a VERSION-agreement check and a live installer run.
  `.github/workflows/release.yml` publishes on a `v*` tag and refuses a tag that disagrees with
  `VERSION`.
- **`spec` check group** in `tests/validate.py`, running the reference validator in process, so the
  specification is enforced locally and not only in CI. `skills-ref>=0.1.1` added to
  `tests/requirements.txt`.

### Unchanged

Every skill's reasoning, rules, knowledge, playbooks and per-skill `targetbay.version`. Only the
location of the metadata changed, not a single decision any skill makes.

`capabilities.yaml` still carries `mcp_tools: TODO` for all 15 capabilities. Skills plan; they cannot
execute. See [docs/mcp-integration.md](docs/mcp-integration.md).

## [1.2.0] - 2026-09-11

Adds the evaluation layer, and fixes the six skill descriptions it immediately exposed.

### Added

- `tests/evals/` — 38 golden prompts across 6 suites (revenue, lifecycle, automation, planning,
  optimization, safety), each declaring the expected skill, expected composition, rules that must be
  honoured, and behaviours that must not occur
- `tests/evals/run_evals.py` — deterministic runner covering schema, skill references, rule-anchor
  resolution, a lexical selection proxy, per-skill coverage and regression locking. No model, no
  network
- `tests/evals/expectations.lock` — ties each case's expectations to the target skill's version, so an
  expectation cannot be quietly edited until it passes
- `--emit` prompt packs — one self-contained file per case with the skill catalogue as a host would
  present it, the prompt, and the rubric, for scoring against a real model
- `tests/evals/rubric.md` — four-axis scoring (selection, composition, rules honoured, must-not), with
  must-not binary and safety cases scored on it alone

### Changed

Six descriptions lacked the vocabulary users actually type, which the selection check surfaced
immediately. `store-onboarding` ranked 23rd of 24 against *"we've just moved to BayEngage, what should
we set up?"*. Fixing the descriptions rather than the test raised lexical top-1 agreement from roughly
40% to 64%.

- `automation-architect@1.1.0` — now names welcome, post-purchase, abandoned cart, replenishment and
  win-back journeys, and the "should we split this flow?" question
- `automation-optimization@1.2.0` — now names the symptoms: not converting, revenue down, falling
  completion, decayed journey
- `campaign-optimization@1.2.0` — now names newsletters, blasts, declining engagement and rising
  unsubscribes
- `audience-discovery@1.1.0` — now names lists, segments and "should we segment this?"
- `store-onboarding@1.1.0` — now names getting started, newly signed up, just migrated, from scratch
- `opportunity-discovery@1.1.0` — now names "what should we be working on?" and "where should we focus?"

Documentation updated to run both checkers: `tests/README.md`, `CONTRIBUTING.md`,
`docs/skill-authoring.md`, `docs/versioning.md` (which now states that a description change is at least
MINOR, because the description is the trigger surface).

### Notes

The selection check is a lexical proxy with a stated ceiling, not a model. Semantic distinctions —
`upsell` versus `aov-growth` on *"raise our average order value"* — are not resolvable by any bag of
words, which is why the gate is a rank threshold and top-1 agreement is reported rather than enforced.
Safety cases set `selection: skip` because they assert refusal rather than routing.

### Known gaps

Unchanged: no MCP tool mappings, `bayengage.messaging_sms` still unverified, no Hydra scope names. The
model-dependent half of evaluation is emitted but not executed — running it requires a model this
package deliberately does not depend on.

## [1.1.0] - 2026-09-11

Completes objective coverage. Ten skills added, covering every area named in the product brief that 1.0.0
documented as a roadmap. Four existing skills gained composition edges to the new skills.

Still foundation-phase: no capability is mapped to a real BayEngage MCP tool, and no new capability was
needed — all ten new skills declare capabilities that already existed in `capabilities.yaml`.

### Added

- `revenue-analysis@1.0.0` — read-only revenue decomposition, attribution and period comparison, with
  alternative explanations tested before a cause is stated
- `opportunity-discovery@1.0.0` — open-ended nine-lens scan for the unframed "what should we be working
  on?"; weights list-health findings above ordinary revenue findings
- `aov-growth@1.0.0` — chooses between threshold, bundle, tier and attachment levers by decomposing AOV
  into items-per-order and item value
- `customer-lifecycle@1.0.0` — derives the store's own stage boundaries and maps transition leakage
- `product-replenishment@1.0.0` — derives reorder intervals per product *and* size, never store-wide
- `marketing-calendar@1.0.0` — multi-period horizon planning, capacity allocation and recovery windows
- `store-onboarding@1.0.0` — new-store baseline that labels every provisional value and sets a
  data-based review point instead of inventing defaults
- `channel-optimization@1.0.0` — email/SMS division of work, sequencing and cost-per-message discipline
- `content-optimization@1.0.0` — content direction once the funnel shows the message is the failure point
- `ab-testing@1.0.0` — test design with size, duration and threshold fixed before the run, and
  unresolvable tests reported as unresolvable

### Changed

- `revenue-growth@1.1.0` — now composes `revenue-analysis` for decomposition and `aov-growth` for the AOV
  term, rather than handling both inline
- `campaign-optimization@1.1.0` — now composes `ab-testing` for test design and `content-optimization`
  for content-level fixes
- `automation-optimization@1.1.0` — now composes `ab-testing`
- `customer-retention@1.1.0` — now composes `product-replenishment` for consumable reorder timing
- `skills/README.md` — regrouped by decision area; roadmap section replaced with a coverage statement

### Known gaps

Unchanged from 1.0.0: no MCP tool mappings, `bayengage.messaging_sms` still unverified, no Hydra scope
names, no LLM evaluation harness. *(Evaluation layer added in 1.2.0.)*

## [1.0.0] - 2026-09-11

Foundation release. Establishes the skill contract, the separation between skills, rules, knowledge and
playbooks, the execution and risk model, the machine-readable schemas, and validation.

All skills ship at `status: foundation`: the contracts are established and the reasoning is real, but the
workflows have not been hardened against a live BayEngage MCP. No capability is mapped to a real MCP tool
yet — see [docs/mcp-integration.md](docs/mcp-integration.md).

### Added

**Skills** — 14, all at `1.0.0`

- `revenue-growth@1.0.0` — opportunity identification against the revenue equation
- `customer-retention@1.0.0` — repeat purchase and churn prevention for active customers
- `customer-winback@1.0.0` — recovery of lapsed customers, including when to stop and suppress
- `automation-strategy@1.0.0` — automation portfolio audit and roadmap
- `automation-architect@1.0.0` — automation variant and topology design
- `automation-optimization@1.0.0` — per-node diagnosis and tuning of live journeys
- `monthly-marketing-planner@1.0.0` — derived marketing calendar for a period
- `holiday-marketing@1.0.0` — holiday relevance, participation decision and strategy
- `holiday-drip-campaign@1.0.0` — derived-length seasonal message sequences
- `campaign-optimization@1.0.0` — funnel diagnosis and hypothesis-led testing
- `audience-discovery@1.0.0` — ranked, sized, exclusion-aware targeting
- `cross-sell@1.0.0` — category expansion from observed co-purchase data
- `upsell@1.0.0` — order value growth from observed price-band behaviour
- `product-launch@1.0.0` — wave-sequenced launch planning

**Rules** — `global`, `safety`, `audience`, `campaign`, `automation`, `personalization`, `content`,
`frequency`, with numbered, citable rules and a defined precedence order.

**Knowledge** — marketing principles, customer lifecycle, segmentation, campaign, automation, email, SMS,
personalisation and experimentation principles.

**Playbooks** — `ecommerce` (baseline), `retail`, `fashion`, `beauty`, `b2b`, with a defined overlay
contract that may tighten but never loosen rules.

**Schemas** — `skill`, `recommendation`, `workflow`, `skill-result` (JSON Schema 2020-12).

**Capability registry** — `capabilities.yaml` with 15 abstract `bayengage.*` capabilities, every
`mcp_tools` mapping marked `TODO`.

**Documentation** — architecture, skill authoring, MCP integration, rules, versioning, examples.

**Examples** — five narrated traces covering revenue growth, monthly planning, holiday drip, automation
strategy and win-back.

**Validation** — `tests/validate.py` covering structure, skill metadata, section integrity, capability and
skill references, composition acyclicity, name uniqueness, schema compilation, fixture validation and
repository-wide link resolution.

### Known gaps

- No capability is mapped to a real BayEngage MCP tool. Skills can plan; they cannot execute.
- `bayengage.messaging_sms` is declared but unverified — no inspected BayEngage implementation exposes SMS
  dispatch. Skills degrade to email-only when it is absent.
- No Hydra OAuth scope names are recorded; no canonical list was found during inspection.
- Ten objective areas from the product brief are documented as a roadmap in
  [skills/README.md](skills/README.md) rather than shipped as placeholder skills. *(Resolved in 1.1.0.)*
- No LLM evaluation harness. The repository is structured to accept one under `tests/` without
  restructuring.

[1.2.0]: https://github.com/targetbay/targetbay-email-sms-marketing-skills/releases/tag/v1.2.0
[1.1.0]: https://github.com/targetbay/targetbay-email-sms-marketing-skills/releases/tag/v1.1.0
[1.0.0]: https://github.com/targetbay/targetbay-email-sms-marketing-skills/releases/tag/v1.0.0
