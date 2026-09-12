# Versioning

Two independent version lines: the package, and each skill.

## Package version

[../VERSION](../VERSION) holds the package version. Semantic versioning.

| Change | Bump |
|---|---|
| A structural change that breaks consumers: the skill contract changes, required sections change, a schema gains a required field, a capability id is renamed or removed, a skill is removed or renamed | **MAJOR** |
| A new skill, rule, knowledge document or playbook; a new optional schema field; a new capability; a materially expanded skill | **MINOR** |
| Clarifications, corrections, link fixes, wording, validation improvements that do not change the contract | **PATCH** |

Consumers of this package are agent hosts and the humans reviewing its output. A change that makes an
agent behave differently in a way a reviewer would not expect is at least MINOR, even when no file's shape
changed.

## Skill versions

Each skill carries its own `metadata.targetbay.version` in frontmatter, independent of the package. This lets one skill
evolve without forcing a package redesign.

Address a specific skill version as:

```
automation-architect@1.0.0
holiday-drip-campaign@1.0.0
monthly-marketing-planner@1.0.0
```

| Change to a skill | Bump |
|---|---|
| Its decisions change materially; sections are removed; `targetbay.requires` gains a capability; `targetbay.risk_level` or `targetbay.execution_mode` changes | **MAJOR** |
| New decision rules, new examples, expanded workflow, a new `targetbay.composes` entry, additional failure handling | **MINOR** |
| Wording, links, formatting, clarification that changes no decision | **PATCH** |

A skill's MAJOR bump is at least a MINOR bump for the package.

Moving a key between the frontmatter's top level and `metadata` is **not** a skill change: it alters where
the metadata sits, not a decision the skill makes. The 2.0.0 specification migration therefore bumped the
package MAJOR and left every skill version untouched.

## `targetbay.status`

| Status | Meaning |
|---|---|
| `foundation` | The contract is established and the reasoning is real, but the workflow has not been hardened against a live TargetBay Email & SMS MCP |
| `stable` | Production-ready: exercised against real capabilities, with its execution paths verified |
| `deprecated` | Superseded. `targetbay.deprecated_by` names the replacement |

Every skill in 1.0.0 is `foundation`. Promotion to `stable` requires the capability mappings in
[mcp-integration.md](mcp-integration.md) to be complete for that skill, plus verification of its execution
paths — not merely more prose.

## Deprecation

1. Set `status: deprecated` and `deprecated_by: <replacement>`
2. Keep the file for at least one MINOR release so existing references resolve
3. Note it in [../CHANGELOG.md](../CHANGELOG.md) with the migration path
4. Remove it in the next MAJOR release

Never silently delete a skill. Something references it.

## Capability registry

[../capabilities.yaml](../capabilities.yaml) carries its own `version`. Adding a capability is MINOR for
the package; renaming or removing one is MAJOR, because every skill's `targetbay.requires` list
depends on it.

Filling in an `mcp_tools` mapping is MINOR — it changes what the package can do without changing any
contract.

## Schemas

Schema changes follow the package version:

- Adding an optional property → MINOR
- Adding a required property, removing a property, narrowing an enum → MAJOR
- Description and title edits → PATCH

Schema `$id` URLs stay stable across versions.

## Rules

Rules are numbered and **never renumbered**. Skills cite them by number. A retired rule is marked retired
in place; its number is not reused.

Adding a binding rule is MINOR. A rule that invalidates existing skill behaviour is MAJOR.

## Evaluations and versions

[tests/evals/expectations.lock](https://github.com/targetbay360/targetbay-agent-skills/blob/main/tests/evals/README.md) ties each golden prompt's expectations to
the version of the skill it targets. Changing what a case expects without moving that skill's version
fails the run.

This makes intent explicit. Editing an expectation because the skill genuinely changed is a version
bump. Editing it because the case was failing is the thing the lock exists to prevent.

A change to a skill's `description` is at least **MINOR**: the description is the trigger surface an
agent host matches on, so widening or narrowing it changes which prompts reach the skill, even when no
decision inside the skill changed.

## Changelog

Every release is recorded in [../CHANGELOG.md](../CHANGELOG.md) in Keep a Changelog format. Skill-level
changes are listed with their skill version so a reader can tell which skills moved.

## Releasing

This plugin lives in a marketplace repository alongside other TargetBay products, and releases
independently of them. A release is a tag of the form `targetbay-email-sms@<version>`, where the version
matches [../VERSION](../VERSION).

Four places carry the version and validation asserts all four agree: `VERSION`, `package.json`,
`.claude-plugin/plugin.json`, and this plugin's entry in the repository's
`.claude-plugin/marketplace.json`. Bump them together.

Repository-level changes — the marketplace manifest, shared tooling, the plugin boundary — are recorded
in the repository's own changelog rather than this one.
