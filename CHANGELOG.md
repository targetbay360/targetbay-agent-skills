# Changelog

Repository-level changes: the marketplace, shared tooling and the plugin boundary. Each plugin keeps its
own changelog under `plugins/<name>/CHANGELOG.md`, and versions independently.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
