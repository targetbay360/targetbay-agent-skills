# Tests

One script. No framework, no fixtures directory conventions to learn, no CI configuration.

```bash
python3 -m pip install -r requirements.txt   # pyyaml, jsonschema
python3 validate.py                          # or: python3 tests/validate.py from the repo root
```

Exits 0 when everything passes, 1 with a list of failures otherwise.

## Check groups

| Group | Asserts |
|---|---|
| `structure` | Required files and directories exist; every `skills/*/` has a `SKILL.md`; every capability entry is well-formed |
| `spec` | Every skill passes the [Agent Skills](https://agentskills.io/specification) reference validator — top-level frontmatter closed to the six specification fields, `name` lowercase-hyphenated and matching the directory, `description` within 1024 characters |
| `skill-validation` | Frontmatter parses and validates against [../schemas/skill.schema.json](../schemas/skill.schema.json); `name` matches the directory; all fourteen sections present, in order, non-empty |
| `playbooks` | Playbook frontmatter keys and semver; `name` matches the directory; all six sections present and in order |
| `references` | Every `targetbay.requires` resolves in [../capabilities.yaml](../capabilities.yaml); every `targetbay.composes` resolves to a real skill; the composition graph is acyclic; every relative markdown link in the repository resolves |
| `duplication` | Skill `name` and `targetbay.display_name` are globally unique |
| `schemas` | All four schemas compile as JSON Schema 2020-12; valid fixtures pass; invalid fixtures are rejected; the broken-skill fixture is rejected |
| `versioning` | `VERSION` is semver and appears in `CHANGELOG.md`; every skill version is semver; `capabilities.yaml` carries a semver |

The `spec` group needs `skills-ref`, which `tests/requirements.txt` installs. CI additionally runs the
`agentskills validate` CLI over every skill, so a drift between the in-process check and the published
tool surfaces rather than hiding.

## Fixtures

```
fixtures/valid/       must validate against the schema named by the filename
fixtures/invalid/     must FAIL validation — these prove the schemas have teeth
fixtures/broken-skill/SKILL.md   must be REJECTED by the same code path that validates real skills
```

`fixtures/` is excluded from the repository-wide link check, because its contents are deliberately wrong.

The invalid fixtures are the reason a green run means something. A schema that accepts everything passes
its valid fixtures too; only the rejection cases show it is doing work.

## Adding a fixture

Name the file after the schema it exercises — `recommendation.json`, `workflow.json`,
`skill-result.json` — and put it in `valid/` or `invalid/`. The runner picks it up with no registration.

To exercise a new schema, add the schema to `schemas/` and a fixture pair; the runner derives the mapping
from the filename.

## What this does not check

- Whether the marketing reasoning is correct. That needs a human who knows the domain.
- Whether a model actually fires the right skill for a prompt. [evals/](evals/README.md) gets closer,
  but only a real run against a real model answers it.
- Anything about the BayEngage MCP. No capability is mapped yet — see
  [../docs/mcp-integration.md](../docs/mcp-integration.md).

## Evaluations

[evals/](evals/README.md) is the second runner, and a separate concern:

```bash
python3 tests/evals/run_evals.py          # golden prompts: 38 cases, 6 suites
```

It checks that every skill can be reached by a prompt a user would actually type, that cases agree with
the skills' declared composition, that cited rules exist, and that expectations cannot change silently.
Its selection check is a lexical proxy with a documented ceiling, not a model — the model-dependent
half is emitted as prompt packs via `--emit` and scored against [evals/rubric.md](evals/rubric.md).

`validate.py` stays a structural check and knows nothing about evals. Run both.
