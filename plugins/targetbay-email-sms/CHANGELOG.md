# Changelog

All notable changes to TargetBay Email & SMS Marketing Skills are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this package adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). See [docs/versioning.md](docs/versioning.md)
for how package and per-skill versions relate.

## [4.2.2] - 2026-09-22

Packaging only. No skill, rule, capability or schema changed, and no skill version moved.

### Fixed

- **`scripts/install.sh` leaves an installed skill alone unless `--force`.** It copied the whole
  `skills/` directory over the top on every run, so a local edit to an installed skill was lost
  without warning. `scripts/install.mjs` has always skipped what is already present.
- **`scripts/install.sh` rewrites citations only in the skills it wrote.** It swept every `.md` file
  in the destination, so installing this plugin rewrote the `../../rules/...` citations of any other
  plugin installed beside it to point into this one.
- **`scripts/install.mjs` no longer pins citations to a tag that may not exist.** Installing from a
  clone, whose `VERSION` is ahead of the newest tag, rewrote every citation to a 404. A published
  package or release tarball still pins to its own tag; a checkout uses the branch.
- `scripts/install.sh` defaults to `./.claude/skills` rather than `~/.claude/skills`, matching
  `scripts/install.mjs`, and takes `--global` for the old destination.

## [4.2.1] - 2026-09-22

Documentation only. No skill, rule, capability or schema changed, and no skill version moved.

### Removed

- **The `Authentication` section of `docs/mcp-integration.md` is now the same text the other three
  plugins carry** — authentication is the host's concern, no canonical scope list has been inspected,
  and inventing one would be the error that inventing tool names would be.
- **A section of the same file describing observed integration patterns.** The two conclusions skills
  actually depend on survive elsewhere in it: SMS dispatch is unverified in the capability table, and
  campaign creation is unconfirmed in the TODO list.
- **Provenance framing in `capabilities.yaml` and two earlier entries in this file.** Two capability
  `notes` and two changelog paragraphs attributed evidence to a specific integration rather than to
  the platform surface. The evidence is unchanged; only the attribution is gone.
- **Links to the repository-level capability and skill gap analyses.** Those documents are no longer in
  the public repository; mapping status per plugin stays in this plugin's `docs/mcp-integration.md`,
  which is where a reader of this package can act on it.
- Three `Known gaps` entries no longer name a scope authority.

### Note

Earlier entries in this file still reference `docs/` paths that the repository no longer carries. They
are left as written — a changelog records what was true at the time, and rewriting it to hide a filename
would make it less useful, not more.

## [4.2.0] - 2026-09-19

The layer between a finished campaign and a real audience, and the intelligence beneath it. Seven
skills, nine extended, one new rule family and one new capability — flagged unverified, because the
alternative was inventing one.

**Nothing stood between a built campaign and a send.** Every dimension that can make a send wrong was
owned by a skill that optimised only its own: the audience was checked by one, the copy by another,
the offer by a third, and none of them counted what the recipient actually receives. `email-quality-auditor`
is the sweep that does. It returns PASS, WARN or BLOCK, and BLOCK is deliberately narrow — four stop
conditions, all of them things `safety-rules.md` already forbids. Everything else is a warning with
its cost stated, because a gate that blocks on preference is a gate people learn to route around.

**Deliverability was one bullet in `email-principles.md` and a row in a funnel table.** `list-hygiene`
owned bounces, complaints and who leaves the population, which is the reputation layer; nothing owned
the layer above it. A store whose authentication does not align was being told to rewrite its subject
lines. `deliverability-rules.md` (D1..D10) and `knowledge/deliverability-principles.md` set out the
three layers and the order they are diagnosed in, and `deliverability-qa` stops at the first one that
fails. D7 is the rule that will get argued with most: inbox placement is not observable from sending
data, and this package does not pretend otherwise.

**Two decisions were being made inside five skills each.** `cross-sell`, `upsell`,
`product-replenishment`, `stock-and-price-alerts` and `product-launch` each chose products; nothing
held the reasoning. `product-recommendation-strategy` is built as a leaf that composes nothing, the
same shape as `audience-discovery` and for the same reason. `offer-strategy` does the same for
incentives, and makes the null offer the default rather than the thing nobody considered.

**The contact ceiling every planning skill was planning below had never been set.** F1 to F12 bound
the corpus and each skill counted only its own messages, so the number itself existed nowhere.
`consent-verification` — now Consent and Contact Policy — derives it per segment from where this
store's unsubscribe rate turns against delivered volume, and `campaign-conflict-resolver` arbitrates
against it. No universal priority hierarchy is hard-coded: the reflex of pausing all automations
during a promotion trades a store's highest-earning messages for its lowest, and a fixed ranking is
what makes that look correct.

Nine skills proposed by the brief behind this release were **not** built, because an existing skill
or rule family already owned the decision — `send-time-optimization` exists under that name,
`channel-optimization` is channel orchestration, `opportunity-discovery` is the portfolio analyser,
`content-optimization` owns subject lines.

### Added

- **`email-quality-auditor` 1.0.0** — the pre-send gate. Resolves the audience and states the blast
  radius before any verdict, runs four stop conditions first, then sweeps frequency, collisions,
  personalisation, products, offer accuracy, rendering and programme condition. Owns the verdict and
  none of the reasoning: every dimension is delegated to the skill that owns it. Names every
  dimension it could not check rather than reporting it as passed.
- **`deliverability-qa` 1.0.0** — identity, then reputation, then content, stopping at the first
  failure. Composes `list-hygiene` for the population half of any remedy. Reports authentication
  fixes with an owner outside the platform, because the records live in the store's DNS. Where no
  placement signal exists it says placement is unknown and labels its proxies as proxies.
- **`email-render-qa` 1.0.0** — whether the built message is readable by the whole list: images off,
  narrow screen, dark mode, assistive technology, links, footer. Weights defects by this store's own
  client mix. A missing opt-out is a stop, not a defect.
- **`dynamic-content-personalizer` 1.0.0** — applies P1..P12 to a specific message. Drops an element
  whose fallback branch would serve most recipients, on the grounds that the fallback is then the
  message. Delegates item selection rather than choosing products itself.
- **`offer-strategy` 1.0.0** — tests the null offer first. Derives depth from this store's own
  response history rather than a round number, treats non-monetary instruments as first-class, and
  states the cost as displaced full-price sales where margin data does not exist. Never assumes it
  does.
- **`product-recommendation-strategy` 1.0.0** — the product counterpart to `audience-discovery`. An
  evidence ladder from transacted through co-purchase to catalogue-wide popularity, with the rung
  named per item and the bottom rung never presented as personalised.
- **`campaign-conflict-resolver` 1.0.0** — allow, delay, suppress for the overlap, or substitute
  channel. Priority derived from per-contact value or a stated store policy, recorded for reuse. A
  complete rather than incidental overlap is reported as a portfolio defect and handed to
  `automation-strategy` instead of being arbitrated every month.
- **`rules/deliverability-rules.md`** — D1..D10. Diagnostic order, reputation as a shared pool,
  trends over thresholds, and the limit on what sending data can show.
- **`knowledge/deliverability-principles.md`** — the three-layer model, what warm-up is actually
  doing, and why bounces and complaints say different things. Operational detail is linked to the
  standalone reference skills by absolute URL rather than duplicated.
- **`capabilities.yaml` 1.3.0** — `email_sms.sending_infrastructure`, flagged UNVERIFIED with what
  is assumed. No inbox-placement capability was added: seed-list data does not exist, and adding a
  capability to justify a skill is what this registry's own header forbids.

### Changed

- **`consent-verification` 1.1.0** — now Consent and Contact Policy. Adds the cadence half: delivered
  contact measured across campaigns and automations, the ceiling derived per segment from where this
  store's rates turn, a separate and smaller SMS ceiling, a bounded peak allowance with its recovery
  window, and a recorded class precedence. A separate frequency skill was considered and rejected —
  permission and cadence are one standing policy, and splitting them puts half of it out of reach of
  the skill that needs both.
- **`channel-optimization` 2.1.0** — per-segment assignment derived from consent coverage rather than
  a tier map, the offset between paired channel touches as an explicit decision, a content brief per
  channel, and "reach this segment on nothing" as a legitimate assignment. Collisions are handed on
  rather than resolved here.
- **`campaign-optimization` 2.2.0** — Learn becomes a step in the loop, with the result dated and
  what it did not settle recorded. The funnel table names an owning skill per stage, and reach
  failures split between `deliverability-qa` and `list-hygiene` rather than being one row.
- **`automation-architect` 2.1.0** — product and offer branching as explicit decision points,
  delegated to their owners. A journey that hard-codes a discount depth has embedded a decision it
  does not own, and it goes stale inside the journey. A mid-journey channel change is a branch and
  must clear R10.
- **`customer-winback` 2.2.0** — dormancy classes derived from this store's own intervals, engagement
  and purchase kept as separate axes, the sunset decision handed to `list-hygiene`, and recovery
  measured on the second purchase. A separate reactivation skill was rejected: it would have owned
  nothing this does not.
- **`ab-testing` 2.1.0** — holdout as a first-class design, because no variant comparison can say
  whether a send earns anything at all. A dimensions table naming the trap specific to each lever,
  and an explicit refusal to report a directional difference as a finding.
- **`content-optimization` 2.1.0** — subject and preheader worked as one unit, variants judged on a
  downstream metric with a guard metric, and message architecture where every block justifies its
  place. A separate subject-line skill was rejected; this one already owned the decision.
- **`list-hygiene` 1.1.0** — trend over level, split by receiving domain before any list-wide
  conclusion, and authentication questions routed up rather than answered with suppression. A
  separate inbox-placement monitor was rejected: without a placement capability it would have been a
  skill that cannot run.
- **`opportunity-discovery` 2.1.0** — deliverability separated from list health as its own lens with
  its own owner, a contention lens that counts campaigns and automations together, and a fixed
  routing map so no finding is left without a destination.
- **`marketing-calendar` 2.0.1** — description only. Seven new skills re-weight the per-plugin IDF,
  which pushed "plan our marketing for the year" out of the selection check's top three. The fix is
  the description, not the prompt.

### Tests

- Sixteen eval cases, taking `targetbay-email-sms` from 49 to 65 — seven coverage prompts and nine
  ecommerce scenarios spread across fashion, beauty, electronics, grocery, home and furniture and
  subscription stores. Lexical top-1 agreement moves from 52/67 to 67/83.

## [4.1.0] - 2026-09-19

Seven decisions this plugin did not own, and two capabilities the registry had already observed but
never recorded.

**The registry was behind its own integration note.** `docs/mcp-integration.md` has said since it was
written that the platform surface covers "event tracking, plus webhook events for
campaign, contact, list and order activity" — and `capabilities.yaml` listed neither. That is not a
new capability invented to justify a skill; it is the registry catching up with evidence already
recorded in this package. Both entries ship with `notes` naming what is still unconfirmed, because a
request/response tool surface and a push subscription are different shapes and the MCP may expose
only one.

**`customer-winback` pointed at nothing.** Its `When Not to Use` sent the reader to "a deliverability
and list hygiene exercise" and no such skill existed, so the most common follow-up question in the
corpus dead-ended. `list-hygiene` closes it.

**The same correction, applied to the API.** The campaign resource exposes read, list, send and
reports — there is no create operation. That is recorded in `docs/mcp-integration.md` so no skill
plans against an operation nobody has confirmed, and stated in full in the new recipe library, where
every affected pattern names the workaround.

### Added

- **`list-hygiene` 1.0.0** — who leaves the sending population and by which route, when a complaint
  rate means pausing rather than tuning, and what suppression costs in revenue alongside what it buys
  in deliverability. Decides the programme's response; the platform still classifies and enforces.
- **`consent-verification` 1.0.0** — whether a confirmation step is worth its cost in list growth, per
  channel and per capture point, and what happens to contacts whose permission cannot be evidenced.
  Its most important output is a refusal: an unevidenced list is not mailed, and a re-permission pass
  does not launder one. Nothing in `skills/`, `rules/`, `knowledge/` or `playbooks/` mentioned opt-in
  before this.
- **`ai-content-governance` 1.0.0** — where the human sign-off sits in a pipeline that writes
  customer-facing copy: which message classes may ship unreviewed, what the reviewer checks and in what
  order, and the rule that a failed generation sends nothing rather than falling back to the last good
  version.
- **`automation-orchestration` 1.0.0** — where each step of a journey runs, and what moving a send
  outside the platform costs. A topology where suppression, consent, frequency or quiet hours has no
  named enforcing layer is refused rather than flagged. Names no external product.
- **`stock-and-price-alerts` 1.0.0** — availability and price changes as per-contact alerts. Units
  available gate the audience before it is sized, the serving order is stated rather than defaulted,
  and repeated price-drop notices are bounded because they train discount-waiting. `product-launch`
  keeps the broad restock announcement.
- **`send-time-optimization` 1.0.0** — which granularity of send timing the store's data can support,
  and the refusal when none of them beats the current time at this volume. `campaign-rules.md#C6`
  stated the rule and no skill owned the decision.
- **`automation-recipe-selector` 1.0.0** — ranks a published, finite recipe library against one store
  by readiness rather than appeal, names the single prerequisite blocking each entry, and hands back to
  `automation-strategy` when nothing in the library fits.
- Two capabilities: `email_sms.event_stream` (read) and `email_sms.event_tracking` (write), both
  `mcp_tools: TODO` with `notes` recording the open questions. `capabilities.yaml` is at 1.2.0.
- **Three rules**, each promoted from prose that three or more skills were about to state
  independently. `content-rules.md#N13` — a generation step that fails sends nothing, with no fallback
  to a previously approved version. `safety-rules.md#S13` — an approval gate that expires into a send
  is not a gate, and a standing instruction is not per-send approval. `audience-rules.md#A13` — an
  audience is a snapshot, re-checked at send time; `G13` bound planning time only and now points at it.
  The skills and the recipe library cite these rather than restating them.
- `## Recipe Priority` in all five playbooks, appended after `Known Limits`, with the signal to check
  before believing each position. `automation-recipe-selector` takes it as a prior and reports which
  position came from the playbook and which from store data.
- Ten golden-prompt cases across the five existing suites, including two `selection: skip` refusal
  cases — an instruction to send generated copy unattended, and an instruction to mail a purchased
  list.

### Changed

- **`campaign-optimization` 2.1.0** — owns the re-send to non-openers. Three rules: it spends from the
  same frequency budget, it changes one variable, and a third attempt at the same non-responders is
  escalation in the wrong direction. A near-duplicate skill was considered and rejected;
  `frequency-rules.md#F6` already decided the hard case.
- **`customer-winback` 2.1.0** — the list-hygiene pointer now resolves.
- **`audience-discovery` 2.1.0** — a machine-proposed cluster is a hypothesis, not an audience. It
  passes A1, A2, A3 and G8 before it is materialised, and is checked for sensitive attributes
  reconstructed from proxies before, not after.
- **`product-launch` 2.0.1** — routes per-contact availability and price alerts to
  `stock-and-price-alerts`; the broad restock announcement stays.
- `docs/mcp-integration.md` records the two new capabilities' open questions, corrects the prior-art
  paragraph to state that campaign creation is unverified, and adds three TODOs.
- The five playbooks are at 1.1.0, each with `recipe priority` in `overrides`.
- `lexical top-1 agreement` moves from 44/59 to 52/67 as the corpus grows. One thin-margin warning
  remains, between `revenue-analysis` and `revenue-growth`, and is drift from the larger corpus rather
  than a new overlap.

## [4.0.0] - 2026-09-16

### Changed

- **The skill contract is thirteen sections, not fourteen.** `Inputs` is removed from every skill and
  from `tests/validate.py`. Two thirds of the corpus declared no required input at all, and the four
  names that dominated the table — `scope`, `objective`, `constraints`, `period` — restated
  `Required Context` without its reason column. Every skill is therefore a MAJOR bump.
- **`aov-growth` and `upsell` no longer claim the same lever.** Thresholds and merchandising belong to
  `aov-growth`, which ranks the levers; `upsell` keeps tier, size, bundle and subscription moves and
  defers threshold design. Both descriptions changed, so both are at least MINOR on that count alone.
- **Descriptions sharpened where the golden prompts showed overlap.** `customer-winback`,
  `automation-strategy` and `audience-discovery` — whose description previously ended by telling a host
  not to trigger it. The evals now run with no thin-margin warnings, and lexical top-1 agreement rises
  from 41/59 to 44/59.
- `automation-architect` cites `automation-rules.md#R2` rather than reproducing its list of variant
  axes, and cites R7 for node count.
- `docs/mcp-integration.md` no longer transcribes `capabilities.yaml`; it records the one capability
  that still carries an open question and points at the registry for everything else.
- The architecture diagram lives once, in `docs/architecture.md`, with the box borders the rename broke
  now realigned. The plugin README links to it.
- `docs/` and `examples/` are published to npm, so the README's links to them resolve in the tarball.

### Fixed

- **Installed skills no longer cite files that are not there.** `install.mjs` and `install.sh` flatten
  `skills/` into the destination, which left every `../../rules/`, `../../knowledge/` and
  `../../schemas/` citation resolving to nothing — 335 rule references alone. Both installers now
  rewrite those to the released URL for the installed version. Sibling-skill links still resolve and
  are untouched.
- `install.sh` installs slash commands alongside a `.claude` tree, matching `install.mjs`.
- `install.mjs` no longer throws when a plugin ships no `commands/` directory.
- `package.json` no longer declares a `validate` script whose paths resolve nowhere from the plugin
  directory.
- `skills/README.md` listed `store-onboarding` at 1.1.0 while the skill declared 2.0.0.
- The README claimed the plugin contains `tests/` and named eight validation groups; there are nine, and
  the runners live at the repository root. It now points at CONTRIBUTING rather than restating them.
- The "restated in fourteen skills" idiom, stale since the plugin reached 24, no longer depends on a
  count. `docs/versioning.md` no longer claims every skill is at 1.0.0, and `docs/examples.md` no longer
  says evaluations have yet to be added.

## [3.1.0] - 2026-09-12

`store-onboarding` is now scoped to email and SMS, and is findable by the word people actually use.

### Changed

- **`store-onboarding` narrowed to email and SMS, and bumped to `2.0.0`.** Cross-product onboarding —
  sequencing reviews, loyalty and onsite personalization alongside email and SMS against a single contact
  budget — now belongs to
  [`onboarding-blueprint`](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-onboarding/skills/onboarding-blueprint/SKILL.md)
  in the new `targetbay-onboarding` plugin, which this skill's `When Not to Use` links by full URL.

- **`store-onboarding` gained the word *onboarding*** in its `description` and `When to Use`. This reads
  cosmetic and is not. `store` and `new` are both in `tests/evals/run_evals.py`'s `STOPWORDS`, so the
  prompt *"Onboard this new store"* reduced to the single term `onboard` — which the skill carried
  nowhere. It ranked 23rd of 24 against its own subject while passing its suite, because the one golden
  prompt it had happened to use vocabulary it did carry. It now ranks 1st.

- **`email_sms.store_profile` now names the Store Context Pack**, and `capabilities.yaml` is bumped to
  `1.1.0`. No skill frontmatter changed: every skill already requiring `store_profile` gains the derived
  vertical, catalogue shape, customer shape, brand profile and readiness matrix through the capability it
  already declares.

- **Eval case `plan-003` reworded** to stay within email and SMS, with a `must_not` forbidding the skill
  from planning reviews, loyalty or onsite work.

## [3.0.0] - 2026-09-12

Renamed from BayEngage to TargetBay Email & SMS. The package was the last one in the marketplace still
carrying a product brand of its own; every identifier it exposes now matches the convention its three
sibling plugins already follow. No skill content changed — all 24 skills keep their names, versions,
reasoning and composition edges. Everything that changed is an identifier.

Entries below this one are left as they were written and still say BayEngage. They record what the names
were at the time; the mapping to the new ones is in this entry.

### Changed

- **Plugin renamed** from `bayengage-marketing` to `targetbay-email-sms`, and the directory moved to
  `plugins/targetbay-email-sms/`. Every `/bayengage-marketing:*` slash command is now
  `/targetbay-email-sms:*`, and installation is `/plugin install targetbay-email-sms@targetbay`. The six
  command names themselves are unchanged.
- **npm package renamed** to `@targetbay/email-sms-skills`, matching `@targetbay/reviews-skills` and its
  siblings. Nothing was ever published under `@targetbay/bayengage-marketing-skills`, so there is no
  deprecation to honour — this release is the first the scope has carried. The bin is now
  `targetbay-email-sms-skills` rather than `bayengage-skills`.
- **Capability namespace moved** from `bayengage.*` to `email_sms.*` — all 15 identifiers, and every
  `targetbay.requires` line that names them. The namespace is the bare product word, as
  `targetbay-reviews` uses `reviews.*`; the schema pattern `^[a-z][a-z0-9_]*\.[a-z0-9_]+$` admits no
  hyphen, so the plugin slug could not be used verbatim. Nothing was bound to a live tool surface at the
  time of the move — every `mcp_tools` value was, and remains, `TODO`.
- **Releases are tagged `targetbay-email-sms@<version>`.** The prefix must equal the plugin directory
  name, so tags cut under the old prefix no longer resolve. `scripts/install.sh` filters on the new one.
- **Schema `$id` URLs** moved to `https://targetbay.com/schemas/targetbay-email-sms/*.schema.json`.
  Anything holding an external `$ref` to the old URLs must be repointed.
- **The product is called TargetBay Email & SMS in prose**, throughout the skills, rules, knowledge, docs
  and examples.

### Unchanged

- All 24 skill names, versions, capability declarations and composition edges
- Marketplace name `targetbay`, so the install suffix is the same
- The six slash command names — only the namespace before the colon changed

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

Unchanged: no MCP tool mappings, `bayengage.messaging_sms` still unverified, no OAuth scope names. The
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

Unchanged from 1.0.0: no MCP tool mappings, `bayengage.messaging_sms` still unverified, no OAuth scope
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
- No OAuth scope names are recorded; no canonical list was found during inspection.
- Ten objective areas from the product brief are documented as a roadmap in
  [skills/README.md](skills/README.md) rather than shipped as placeholder skills. *(Resolved in 1.1.0.)*
- No LLM evaluation harness. The repository is structured to accept one under `tests/` without
  restructuring.

[1.2.0]: https://github.com/targetbay/targetbay-email-sms-marketing-skills/releases/tag/v1.2.0
[1.1.0]: https://github.com/targetbay/targetbay-email-sms-marketing-skills/releases/tag/v1.1.0
[1.0.0]: https://github.com/targetbay/targetbay-email-sms-marketing-skills/releases/tag/v1.0.0
