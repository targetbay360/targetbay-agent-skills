# Tests

Two scripts. No framework, no fixture conventions to learn, no per-plugin CI configuration.

```bash
python3 -m pip install -r requirements.txt   # pyyaml, jsonschema, skills-ref
python3 validate.py                          # or: python3 tests/validate.py from the repo root
python3 evals/run_evals.py
```

Both exit 0 when everything passes, 1 with a list of failures otherwise.

## Per plugin, or once?

The repository is a marketplace of product plugins under `plugins/`. Most checks run **once per
plugin**, and failures are prefixed with the plugin name so they are locatable. Three things run
**once, repo-wide**:

- the relative-link sweep, which is the safety net for moving content between directories
- the `marketplace` group, which reconciles `.claude-plugin/marketplace.json` against what is on disk
- the repo-level `structure` checks for governance files and shared tooling

Each plugin carries its own schemas, rules and `capabilities.yaml`, because Claude Code ships only what
lives under a plugin's `source` directory. The shared fixtures below are the contract every plugin's
copy of a schema has to honour.

## `validate.py` check groups

| Group | Asserts |
|---|---|
| `structure` | Repo-level and per-plugin required files and directories exist; every `skills/*/` has a `SKILL.md`; every capability entry is well-formed; a plugin's capability ids share one namespace |
| `spec` | Every skill passes the [Agent Skills](https://agentskills.io/specification) reference validator — top-level frontmatter closed to the six specification fields, `name` lowercase-hyphenated and matching the directory, `description` within 1024 characters |
| `skill-validation` | Frontmatter parses and validates against the plugin's own `schemas/skill.schema.json`; `name` matches the directory; all thirteen sections present, in order, non-empty |
| `playbooks` | Where a plugin has playbooks: frontmatter keys and semver, `name` matches the directory, all six sections present and in order |
| `references` | Every `targetbay.requires` resolves in the plugin's own `capabilities.yaml`; every `targetbay.composes` resolves to a skill in the same plugin; the composition graph is acyclic; every relative markdown link in the repository resolves |
| `duplication` | Skill `name` and `targetbay.display_name` are unique **within a plugin** — two products may legitimately both want an `audience-discovery` |
| `schemas` | Every plugin's schemas compile as JSON Schema 2020-12; valid fixtures pass; invalid fixtures are rejected; the broken-skill fixture is rejected |
| `versioning` | Each plugin's `VERSION` is semver, appears in its `CHANGELOG.md`, and matches both its manifests; every skill version is semver; `capabilities.yaml` carries a semver |
| `marketplace` | Every listed plugin exists, every existing plugin is listed, and `source`, `name` and `version` agree across the marketplace manifest, `plugin.json` and `VERSION` |

The `spec` group needs `skills-ref`, which `requirements.txt` installs. CI additionally runs the
`agentskills validate` CLI over every skill in every plugin, so a drift between the in-process check and
the published tool surfaces rather than hiding.

`playbooks`, `examples` and `commands` are optional per plugin and validated only when present. A young
plugin should not invent five vertical playbooks it has no evidence for — the same "never invent"
discipline the repository applies to MCP tool names.

## Fixtures

```
fixtures/valid/       must validate against the schema named by the filename
fixtures/invalid/     must FAIL validation — these prove the schemas have teeth
fixtures/broken-skill/SKILL.md   must be REJECTED by the same code path that validates real skills
```

Fixtures are shared across plugins deliberately: they are the contract, and a plugin whose copy of a
schema diverges enough to disagree with them fails. A fixture naming a schema a plugin does not carry
is skipped for that plugin — not every product plans workflows.

`fixtures/` is excluded from the repository-wide link check, because its contents are deliberately wrong.

The invalid fixtures are the reason a green run means something. A schema that accepts everything passes
its valid fixtures too; only the rejection cases show it is doing work.

## Adding a fixture

Name the file after the schema it exercises — `recommendation.json`, `workflow.json`,
`skill-result.json` — and put it in `valid/` or `invalid/`. The runner picks it up with no registration,
for every plugin carrying that schema.

## What this does not check

- Whether the reasoning is correct. That needs a human who knows the domain.
- Whether a model actually fires the right skill for a prompt. [evals/](evals/README.md) gets closer,
  but only a real run against a real model answers it.
- Anything about the MCP servers. No capability is mapped in any plugin yet — see each plugin's
  `docs/mcp-integration.md`.

## Evaluations

[evals/](evals/README.md) is the second runner, and a separate concern:

```bash
python3 tests/evals/run_evals.py
```

Cases live in `evals/golden-prompts/<plugin>/*.yaml`. The runner checks that every skill can be reached
by a prompt a user would actually type, that cases agree with the skills' declared composition, that
cited rules exist in that plugin's `rules/`, and that expectations cannot change silently.

Its selection check is a lexical proxy with a documented ceiling, not a model. Why it is scored per
plugin, and where the proxy stops being informative, is set out once in
[evals/README.md](evals/README.md); the model-dependent half is emitted as prompt packs via `--emit` and
scored against [evals/rubric.md](evals/rubric.md).

`validate.py` stays a structural check and knows nothing about evals. Run both.
