# Changelog

Repository-level changes: the marketplace, shared tooling and the plugin boundary. Each plugin keeps its
own changelog under `plugins/<name>/CHANGELOG.md`, and versions independently.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
  alone.
