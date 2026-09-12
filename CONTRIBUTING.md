# Contributing

This package is Markdown, YAML frontmatter and JSON Schema. There is no build step and no runtime. The
only tooling is two validation scripts and a dependency-free installer.

## Setup

```bash
python3 -m pip install -r tests/requirements.txt   # pyyaml, jsonschema, skills-ref
python3 tests/validate.py                          # structure, spec and contracts
python3 tests/evals/run_evals.py                   # golden prompts
```

That is the whole toolchain. Please do not add dependencies, package managers or frameworks without a
reason that this cannot be done without them. `scripts/install.mjs` is deliberately zero-dependency
Node, and `package.json` exists to publish, not to build.

## Frontmatter

Skill frontmatter follows the [Agent Skills specification](https://agentskills.io/specification), whose
reference validator rejects any top-level field outside `name`, `description`, `license`,
`compatibility`, `metadata` and `allowed-tools`. Anything this package needs goes under `metadata` as a
`targetbay.*` **string** — lists comma-separated. The `spec` group in `tests/validate.py` enforces this,
so a PR adding a top-level key fails before review. See
[docs/skill-authoring.md](docs/skill-authoring.md).

## Where things go

| Adding | Goes in | Guide |
|---|---|---|
| A marketing objective an agent should accomplish | `skills/<name>/SKILL.md` | [docs/skill-authoring.md](docs/skill-authoring.md) |
| A constraint that binds every skill | `rules/` | [docs/rules.md](docs/rules.md) |
| Durable marketing theory | `knowledge/` | [knowledge/README.md](knowledge/README.md) |
| Vertical defaults | `playbooks/<vertical>/PLAYBOOK.md` | [playbooks/README.md](playbooks/README.md) |
| A new abstract capability | `capabilities.yaml` | [docs/mcp-integration.md](docs/mcp-integration.md) |
| A shortcut for a common request | `commands/<name>.md` | route to an existing skill; add no reasoning |
| A narrated trace | `examples/` | [docs/examples.md](docs/examples.md) |

If the same paragraph would appear in more than one skill, it belongs in `rules/` or `knowledge/`, and the
skills link to it.

## Hard requirements

These are not style preferences. A change that breaks one of them will not be accepted.

1. **No MCP implementation.** No API clients, endpoints, tool schemas or request code. This package
   declares capabilities; the BayEngage MCP provides them.
2. **No invented tool names.** Capability identifiers only, from `capabilities.yaml`. Concrete tool
   mappings stay `TODO` until the real MCP surface is inspected.
3. **No hard-coded business assumptions.** No fixed campaign counts, node counts, sequence lengths,
   holiday dates or threshold numbers. Derive from store data and state the derivation.
4. **No invented data.** No illustrative statistics presented as real, and no external benchmarks
   presented as this store's numbers. Documentation figures are labelled illustrative.
5. **No duplicated instructions.** Cite rules by number rather than paraphrasing them.
6. **No vendor-specific behaviour.** Nothing that depends on a particular agent host.
7. **Safety rules are not negotiable.** `high_impact` and `destructive` actions always stop for explicit
   human approval.

## Making a change

1. Read the relevant guide above
2. Make the change
3. Run `python3 tests/validate.py` **and** `python3 tests/evals/run_evals.py`
4. Add or update a golden prompt if the change affects what a skill answers —
   see [tests/evals/README.md](tests/evals/README.md)
5. Update `skills/README.md` if the skill set changed
6. Add a `CHANGELOG.md` entry, with skill versions where skills changed
7. Bump `VERSION` per [docs/versioning.md](docs/versioning.md)

## What validation checks

| Group | Asserts |
|---|---|
| `structure` | Required files and directories exist; every skill directory has a `SKILL.md` |
| `skill-validation` | Frontmatter parses and matches the schema; all fourteen sections present, in order, non-empty |
| `references` | Every capability and composed skill resolves; composition graph is acyclic; every relative link resolves |
| `duplication` | Skill names and display names are unique |
| `schemas` | All schemas compile; valid fixtures pass; invalid fixtures fail |
| `versioning` | `VERSION` is semver and appears in `CHANGELOG.md`; skill versions are semver |

And `run_evals.py` adds:

| Group | Asserts |
|---|---|
| `schema` / `skill-refs` / `rule-refs` | Eval cases are well-formed and reference real skills, composition and rules |
| `selection` | Every skill is lexically reachable from a prompt a user would type |
| `coverage` | No skill is without a golden prompt |
| `regression` | Expectations cannot change while the target skill's version stays put |

A green run means the package is structurally sound. It does not mean the marketing advice is good — that
still needs a human who knows the domain.

## Review expectations

A skill change is reviewed for whether it makes the agent decide *better*, not whether it adds more text.
Length is not thoroughness. Removing a section that added no decision is a good change.

The most common review outcomes:

- Restating a rule instead of citing it → cite it
- Adding a threshold number → derive it from store data instead
- Adding a skill that overlaps an existing one → extend the existing one
- Adding an example without the rejected alternative → add what was rejected and why
- A golden prompt that cannot find its skill → fix the **description**, not the prompt

## Reporting a problem

- Structural or validation problems: open an issue with the failing output
- Marketing reasoning you disagree with: open an issue stating the rule or decision and what evidence
  contradicts it
- Security concerns: see [SECURITY.md](SECURITY.md) — do not open a public issue
