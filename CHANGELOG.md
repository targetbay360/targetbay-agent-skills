# Changelog

Repository-level changes: the marketplace, shared tooling and the plugin boundary. Each plugin keeps its
own changelog under `plugins/<name>/CHANGELOG.md`, and versions independently.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2026-09-22] Internal-only material out of a public repository

This repository is public. A credential and confidentiality review found no secrets and no customer
data anywhere in the tree or its history. It did find documentation that described platform internals
and unshipped intent rather than helping a contributor decide anything — which is the standard this
repository applies to its own content. It is removed.

### Removed

- **`docs/`** — the capability inventory, the two gap analyses and the skill-priorities file. The
  directory is gone. `validate.py` never required it, so nothing structural depended on it. Mapping
  status that a reader of a plugin needs stays in that plugin's `docs/mcp-integration.md`.
- **`targetbay-marketing-automation-recipes/references/roadmap.md`** — replaced by
  `references/not-shipped.md`. The catalogue of unbuilt ideas and the status legend are gone, along
  with the framing around them. The four refusals are kept in full: they are a decision on the record,
  and the reason a pattern is absent is exactly what stops it being asked for again.

### Changed

- `README.md` and `CLAUDE.md` no longer describe a `docs/` directory.
- `targetbay-marketing-automation-recipes/SKILL.md` routes to the refusals rather than to a roadmap.
- Three links in `plugins/targetbay-email-sms/` reached the old `docs/` by `../../../` relative path,
  which hard requirement 7 forbids and `validate.py` does not catch — it checks that a path resolves,
  not that it stays inside the plugin. Removing the targets closed the violation with them.
- `targetbay-marketing-automation-recipes` no longer attributes its platform reading to a specific
  integration, and drops a judgement about third-party tooling that no reader needed. The API surface
  it documents and the `source workflow` attribution on every timing value are unchanged — the latter
  is what keeps the skill inside hard requirement 3.

## [2026-09-19] A third standalone skill, and seven decisions the plugin did not own

A set of requested automation patterns had no route through the skills corpus: webhook-triggered
lifecycle journeys, scheduled churn and hygiene sweeps, a human approval gate before an AI-written
send. A store asking an agent "what should we automate?" got strategy and no
path to a running automation.

**The recipes could not go into the plugin.** Hard requirements 1 to 4 in `CONTRIBUTING.md` forbid
endpoints, tool schemas, request code and threshold numbers anywhere under `plugins/`, and a recipe
without its trigger and its operations is not a recipe. The two existing standalone skills at the
repository root are the documented precedent for concrete content — `README.md` already explains why
they invert the no-numbers rule — so `targetbay-marketing-automation-recipes` joins them.
Twenty-five recipes across seven reference files, each with its trigger, preconditions, operations,
guardrails, what to measure and what has not been verified, plus three supporting references: the
recipe format, the guardrails every recipe carries, and the roadmap. The decisions stay in the
plugin, capability-abstract, where an agent looks for them.

**The platform surface has no campaign-create operation.** Reading the integration showed the campaign
resource exposes read, list, send and reports only — while a large share of the published example
workflows call a create operation anyway, returning nothing rather than failing loudly. Every recipe
here is written against a pre-built campaign that it selects and sends, and the gap is disclosed in
the skill body, in the surface reference and on each affected recipe. No count is published: this
repository has already been bitten by a hard-coded one.

**Two capabilities were added, and four patterns were refused.** `email_sms.event_stream` and
`email_sms.event_tracking` were already described in `docs/mcp-integration.md` as observed platform
behaviour and had simply never reached `capabilities.yaml`. On the other side, the cold-outreach and
address-scraping workflows are not shipped — they mail people who never opted in, which collides with
`safety-rules.md#S7` and with the compliance reference this repository already carries, and sending
reputation on a shared platform is shared. Invoice parsing and attachment routing are out of scope.
All four refusals are recorded in `references/not-shipped.md` rather than silently omitted.

### Added

- `targetbay-marketing-automation-recipes/` — the third standalone reference skill. Not in the
  marketplace, no manifest, no version file; like its siblings it is installed by copying.
- Seven skills, two capabilities, three rules and a `Recipe Priority` section in all five playbooks.
  See [plugins/targetbay-email-sms/CHANGELOG.md](plugins/targetbay-email-sms/CHANGELOG.md) for the
  detail.

### Changed

- `targetbay-email-sms` is at 4.1.0. The other three plugins are untouched.
- Ten golden-prompt cases across five of the six `targetbay-email-sms` eval suites — two of them
  `selection: skip` refusal cases, pinning the cold-outreach and address-scraping patterns as
  refusals rather than gaps — and a regenerated `tests/evals/expectations.lock`.
- `README.md` documents the third standalone skill, in the repository layout and in the section
  explaining why a skill that breaks the plugin contract is the right shape for this content.
- The three standalone skills now each link to the other two. Previously nothing linked *to*
  `targetbay-marketing-automation-recipes`, so it was unreachable from its siblings — the README
  already claimed the three cross-linked, and now they do. Full GitHub URLs, because each skill
  installs by copying its own directory and a relative link between them is dead on install.

### Fixed

- `docs/mcp-capability-inventory.md` had not been updated when the two capabilities above landed:
  the `targetbay-email-sms` registry reads 17 rather than 15, the total 60 rather than 58, and the
  open questions nine rather than seven. The plugin's own `docs/mcp-integration.md` already said 17,
  so the two files were contradicting each other. The dated entries below keep their original
  counts — 58 was correct when it was written.

## [2026-09-16] The skill contract loses a section, and installed skills keep their citations

Two problems, both of which the repository's own rules already named.

**`Inputs` was scaffolding.** Thirty of forty-five skills declared no required input at all, and the
four names that dominated the table — `scope`, `objective`, `constraints`, `period` — restated
`Required Context` without its reason column. The contract is now **thirteen sections**, enforced in
`tests/validate.py`. Removing a required section is a MAJOR change for every plugin, so all four bump,
and every skill with them.

**A skill installed from npm cited files that were not there.** Both installers flatten `skills/` into
the destination, which left every `../../rules/`, `../../knowledge/` and `../../schemas/` citation
resolving to nothing — 335 rule references alone, in the layer the whole "cite, do not restate"
architecture depends on. `install.mjs` and `install.sh` now rewrite those to the released URL for the
installed version, which is what `CONTRIBUTING.md` already requires of a reference that leaves its own
directory. Sibling-skill links still resolve after flattening and are untouched.

### Changed

- `aov-growth` and `upsell` no longer both claim free-shipping and gift thresholds. Threshold design
  and merchandising belong to `aov-growth`; `upsell` keeps the upward moves and defers the rest.
- Skill descriptions sharpened where the golden prompts showed overlap. The evals run with no
  thin-margin warnings, and lexical top-1 agreement rises from 41/59 to 44/59.
- Each plugin's `docs/mcp-integration.md` stops transcribing its `capabilities.yaml` — the pattern
  `docs/mcp-capability-inventory.md` explicitly forbids — and records only the seven capabilities that
  still carry an open question.
- `CONTRIBUTING.md` no longer implies every plugin carries `docs/skill-authoring.md`; only
  `targetbay-email-sms` does, and the guides are written once there for all four.
- The drift argument no longer counts skills. It was written as "fourteen skills" when the plugin had
  fourteen and has since had twenty-four, and appeared elsewhere as six, five and seven.
- `docs/` and, where present, `examples/` are published to npm.

### Fixed

- `tests/evals/run_evals.py` and `tests/README.md` no longer restate the lexical-proxy rationale that
  `tests/evals/README.md` carries; `CONTRIBUTING.md` points at the eval docs rather than summarising
  their check groups at lower fidelity.
- The `2026-09-15` entry below sat between two `2026-09-12` entries in a reverse-chronological file,
  with no blank line before its heading.
- `targetbay-loyalty` and `targetbay-reviews` shipped a `skill.schema.json` citing `docs/architecture.md`,
  which only `targetbay-email-sms` carries.
- Marketplace and plugin descriptions named work no skill does — photo and video UGC harvesting, a
  reward catalogue, redemption health.
- The bug-report template offered a version placeholder matching no plugin.
- `PLUGIN_OPTIONAL_DIRS` in `tests/validate.py` was defined and never referenced.

## [2026-09-16] A standalone reference skill for template design

The plugins produce content direction and explicitly stop short of finished creative, and the sending
layer skill covers whether a message arrives and what it must contain. Neither covers what an email
should look like. Repository-wide there was no material on template width, email-safe typography,
palette construction, block order or designing for images off — the nearest was the accessibility
reference, which describes what breaks rather than how to build.

### Added

- **`targetbay-email-template-design/`**, a standalone agent skill outside `plugins/`: a routing hub
  plus six references covering layout and spacing, typography, colour and dark mode, template
  anatomy, calls to action and imagery, and design QA. Design guidance only — no HTML, no client
  conditionals, no CSS. Where the sending-layer skill already owns a rule, it cites rather than
  restates.

### Changed

- `targetbay-email-sms-best-practices/SKILL.md` gains a routing row and a `Start Here` entry pointing
  at the design skill. The two standalone skills cross-link by full GitHub URL, because each installs
  by copying its own directory and a relative link between them would be dead on install.
- `README.md` documents both standalone skills rather than one.

## [2026-09-15] Personalization stops being a separate product

`targetbay-personalization` was listed and installed as a product alongside Email & SMS, Reviews and
Loyalty. It is not a product. It is the step every product's onboarding starts with — the onsite capture
that spends no contact budget and that cannot be added retroactively — and listing it separately meant a
store could complete onboarding without it.

The plugin is removed. Its six skills, three rule files, two knowledge documents and twelve capabilities
now live in `targetbay-onboarding`, which goes to `0.2.0`. Details, including the rule-citation changes,
are in [plugins/targetbay-onboarding/CHANGELOG.md](plugins/targetbay-onboarding/CHANGELOG.md).

### Removed

- **`targetbay-personalization`**, from `.claude-plugin/marketplace.json`, the README install list and the
  issue templates. `npx @targetbay/personalization-skills` is no longer published.

### Changed

- **The marketplace is four plugins: three products and onboarding.** Every "all four products" in shared
  prose is now three, and `targetbay-onboarding` describes itself as carrying the onsite work rather than
  sequencing a fourth product that would do it.

- **`docs/mcp-capability-inventory.md` counts 58 capabilities across four plugins**, down from 59 across
  five: `onsite.store_profile` is retired into `onboarding.store_context`, which already carried the same
  values.

- **Golden prompts moved.** `tests/evals/golden-prompts/targetbay-personalization/` is now
  `onsite-coverage.yaml` and `onsite-safety.yaml` under `targetbay-onboarding/`, with their rule
  citations remapped to the merged numbering.

## [2026-09-15] A standalone reference skill for the sending layer

The plugins decide what a store should do. Nothing in the repository explained how the sending layer
underneath them works — SPF alignment, 10DLC registration, one-click unsubscribe headers, webhook
signature verification, suppression scope. That material is deliberately excluded from the plugin
contract by `rules/global-rules.md#G10`, which treats it as a platform responsibility, so it had
nowhere to live and was simply absent.

### Added

- **`targetbay-email-sms-best-practices/`**, a standalone agent skill outside `plugins/`: a routing
  hub plus fourteen references covering email and SMS deliverability, CAN-SPAM/GDPR/CASL and
  TCPA/state compliance, the transactional message catalog, ecommerce lifecycle flows, capture and
  consent, suppression and hygiene, idempotency and retry, delivery events, and accessibility.
  It does not follow the fourteen-section plugin contract and is not registered in
  `marketplace.json` — it is reference material for an engineer, not a decision skill for an agent.
- **Two boundaries stated in the skill itself.** Code examples call a wrapper the reader owns rather
  than an SDK method, because the TargetBay API and webhook signatures were not inspected; and every
  figure is either an attributed external requirement or labelled illustrative, which is the same
  rule the plugins follow.

### Changed

- **`README.md` documents the directory** in the repository layout and in a section explaining why a
  skill that breaks the plugin contract is the correct shape for this content.

## [2026-09-12] Onboarding becomes a plugin

A store's first week is where it decides whether TargetBay is worth keeping, and it was the part of the
marketplace with no home. Four product plugins each knew how to run their own product well; nothing knew
what to do first, or how to stop all four from talking to the same customer at once.

This entry records the repository-level changes. What the plugin contains, and why, is in
[plugins/targetbay-onboarding/CHANGELOG.md](plugins/targetbay-onboarding/CHANGELOG.md).

### Added

- **A fifth plugin, `targetbay-onboarding`**, at `0.1.0` — four skills, its own `onboarding.*` registry,
  and the cross-product rules the four product plugins cannot own. It is a separate plugin because
  `tests/validate.py` makes it one: a plugin's capability identifiers may not span namespaces, and
  `composes:` may only name skills in the same plugin, so a skill needing `email_sms.*`, `reviews.*`,
  `loyalty.*` and `onsite.*` at once has nowhere else to live.

- **`docs/mcp-capability-inventory.md`** — the Phase 0 worksheet. All 59 capabilities across the five
  plugins are still `TODO`; this names the three answers that decide how far the onboarding pipeline can
  go, and sends them into the registries rather than into a worksheet that drifts.

### Changed

- **Cross-product contact is reconciled.** The rules live in
  `plugins/targetbay-onboarding/rules/contact-ownership-rules.md`; each of the four product plugins now
  carries a pointer to them in its own `rules/README.md`, naming which moment that product owns and
  stating plainly that those rules do not install alongside it. The residual dependency is recorded
  honestly in X9: ownership is settled here, but *enforcement* needs a unified cross-product frequency
  and consent view from the MCP, and where that does not exist the budget is labelled provisional rather
  than claimed.

- **Every `<ns>.store_profile` description now names the Store Context Pack**, in all four product
  registries, which are bumped to `1.1.0`. One sentence, four times: it is what gives every skill that
  already requires `store_profile` a store-specific context with no frontmatter change anywhere.

- **`store-onboarding` narrowed to email and SMS**, and `targetbay-email-sms` bumped to `3.1.0`. The
  cross-product question now belongs to `onboarding-blueprint`. The skill also gained the word
  *onboarding* in its `description` — measured, not cosmetic: `store` and `new` are both in the eval
  harness's `STOPWORDS`, so *"Onboard this new store"* reduced to the single term `onboard`, which the
  skill carried nowhere. It ranked 23rd of 24 against its own subject. It now ranks 1st, pinned by a new
  golden prompt so the word cannot be removed again with the suite still green.

- **`tests/validate.py` now polices stale TODOs.** A wholly unmapped registry is the documented state of
  an un-inspected MCP and stays legal. A *partly* mapped one is different: once real tools start landing,
  every remaining `mcp_tools: TODO` must carry a `notes` saying why. "Not mapped yet" cannot quietly
  become "nobody looked".

- **The link sweep now resolves cross-plugin GitHub URLs.** A plugin may not link outside itself by
  relative path, so siblings are referenced by full URL to this repository — and those were the only
  links the sweep skipped. They now resolve to a path and are checked, which is what makes the
  contact-ownership pointers above enforceable rather than decorative.

### Known gaps

- **Nothing is mapped yet.** All 59 capabilities are `TODO`, and four are flagged unverified. See
  `docs/mcp-capability-inventory.md`.
- **The contact budget is not enforceable from this repository.** The rules decide ownership; enforcement
  needs the platform.
- **The shared layer is now duplicated five times**, not four — and the fifth copy made the *drift*
  worse, not just the line count: the same nine shared rules now carry five different anchor numbers, so
  a cross-plugin citation like `safety-rules.md#S12` means different things in different plugins.
  Extraction remains the next structural change, and was deliberately not coupled to this one.

## [2026-09-12] BayEngage renamed to TargetBay Email & SMS

The restructure below left one plugin naming itself differently from the other three. This entry closes
that gap: `bayengage-marketing` is now `targetbay-email-sms`, and all four plugins name themselves the
same way.

Entries below this one still say BayEngage. They record what the names were when they were written; this
entry is the mapping.

### Changed

- **`bayengage-marketing` renamed** to `targetbay-email-sms`, directory and all. `marketplace.json`, the
  plugin's `plugin.json` and the directory name must agree — `tests/validate.py` asserts it — so the
  three moved together, as did `tests/evals/golden-prompts/`, whose subdirectory `run_evals.py` derives
  from the plugin directory name. The plugin went to `3.0.0`; the rename breaks its install command, its
  npm name, its command namespace and its capability identifiers.
- **Capability namespaces are now uniform.** The plugin's registry moved from `bayengage.*` to
  `email_sms.*`, so every plugin's identifiers are prefixed with its bare product word — `reviews.*`,
  `loyalty.*`, `personalization.*`, `email_sms.*`. The two fixtures under `tests/fixtures/valid/` moved
  with it, since the `references` group resolves them against the plugin's own `capabilities.yaml`.
- **The eval stopword list lost `bayengage`** (`tests/evals/run_evals.py`). `email` and `sms` were
  deliberately not added in its place: the list strips brand noise from TF-IDF ranking, and those two
  words genuinely discriminate between this plugin's skills. The one golden prompt that named the product
  — `plan-003`, the known-fragile `store-onboarding` case — was reworded to say TargetBay rather than
  TargetBay Email & SMS, so the rename does not quietly reshape what that case measures.
- **Changelogs were not rewritten.** Dated entries in this file and in each plugin's changelog still say
  BayEngage, because they record what the names were at the time. The new names are recorded here and in
  `plugins/targetbay-email-sms/CHANGELOG.md`.

## [2026-09-12] Marketplace restructure

The repository became a marketplace of product plugins. It previously held exactly one package at its
root; it now holds four under `plugins/`, and can hold more without any of them interfering.

### Changed

- **Repository renamed** from `targetbay-email-sms-marketing-skills` to `targetbay-agent-skills`. GitHub
  redirects the old URL, so an existing `/plugin marketplace add` keeps resolving — re-adding the new
  source is still recommended.
- **`bayengage-marketing` moved** from the repository root to `plugins/bayengage-marketing/`, whole. Every
  skill's relative links are unchanged because the entire package moved together; no skill content was
  edited. Its npm package was renamed to `@targetbay/bayengage-marketing-skills`, and the old name is
  deprecated.
- **`tests/validate.py` now runs per plugin.** Structure, spec conformance, skill contracts, playbooks,
  references, duplication, schemas and versioning all iterate over `plugins/*`. Three checks stay
  repo-wide: the relative-link sweep, which is the safety net for moving content between directories; a
  new `marketplace` group asserting that every listed plugin exists, every existing plugin is listed, and
  sources, names and versions agree; and the repo-level structure checks.
- **Duplication is scoped per plugin**, since two products may legitimately both want a skill of the same
  name.
- **Releases are tagged `<plugin>@<version>`** rather than `v<version>`, so products ship independently.
- **`playbooks/`, `examples/` and `commands/` are optional** per plugin, validated only when present. A
  new plugin should not invent five vertical playbooks it has no evidence for — the same discipline the
  repository already applies to MCP tool names.
- **Capability-id patterns in the schemas are namespace-agnostic.** Membership is enforced by each
  plugin's `capabilities.yaml` and the validator's `references` group, which is stronger than a regex, and
  a new `structure` check asserts a plugin's capability ids do not straddle namespaces.

### Added

- **Three product plugins** at `0.1.0`: `targetbay-reviews`, `targetbay-loyalty` and
  `targetbay-personalization`. Seventeen skills, three capability registries, and the rules and knowledge
  they cite. No MCP surface has been inspected for any of them, so every capability maps to `TODO` and the
  skills plan rather than execute.
- **A repository-level README** as the product catalogue, and this changelog for structural changes.

### Known gaps

- **No shared layer yet.** `rules/global-rules.md`, `rules/safety-rules.md`, the JSON Schemas and parts of
  the knowledge layer are near-identical across plugins and are currently duplicated. Extracting them to a
  `shared/` directory with a sync step was deliberately deferred until a second plugin's files proved
  identical in practice rather than in expectation — which they now have, for the schemas at least. This
  is the next structural change.
- **Cross-product contact is unreconciled.** BayEngage, Reviews and Loyalty can each decide to contact the
  same customer. Each plugin's `docs/mcp-integration.md` records the question; none of them can answer it
  alone. *Answered by `targetbay-onboarding` — see the entry at the top of this file.*
