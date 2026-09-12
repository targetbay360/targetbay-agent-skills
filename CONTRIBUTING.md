# Contributing

This repository is a marketplace of TargetBay product plugins. Every plugin is Markdown, YAML frontmatter
and JSON Schema. There is no build step and no runtime. The only tooling is two validation scripts and a
dependency-free installer per plugin.

## Setup

```bash
python3 -m pip install -r tests/requirements.txt   # pyyaml, jsonschema, skills-ref
python3 tests/validate.py                          # structure, spec and contracts, every plugin
python3 tests/evals/run_evals.py                   # golden prompts, every plugin
```

That is the whole toolchain. Please do not add dependencies, package managers or frameworks without a
reason that this cannot be done without them. Each `plugins/<plugin>/scripts/install.mjs` is deliberately
zero-dependency Node, and the plugin `package.json` files exist to publish, not to build.

## Repository layout

```
.claude-plugin/marketplace.json   one entry per plugin, source ./plugins/<name>
tests/                            shared validation and golden prompts
plugins/<name>/                   a product plugin — self-contained
```

A plugin is **self-contained** because Claude Code ships only what lives under its `source` directory. A
skill inside `plugins/bayengage-marketing/skills/` may link to `../../rules/safety-rules.md` because that
file lives inside the same plugin. It may **not** link to a repository-root file such as `SECURITY.md` by
relative path — that link is dead for anyone who installed the plugin. Use the full GitHub URL instead.

`tests/validate.py` sweeps every Markdown file in the repository and fails on a relative link that does
not resolve, so this is caught rather than argued about.

## Where things go

Paths below are relative to the plugin you are working in, `plugins/<plugin>/`.

| Adding | Goes in | Guide |
|---|---|---|
| An objective an agent should accomplish | `skills/<name>/SKILL.md` | `docs/skill-authoring.md` |
| A constraint that binds every skill | `rules/` | `docs/rules.md` |
| Durable domain theory | `knowledge/` | `knowledge/README.md` |
| Vertical defaults | `playbooks/<vertical>/PLAYBOOK.md` | `playbooks/README.md` |
| A new abstract capability | `capabilities.yaml` | `docs/mcp-integration.md` |
| A shortcut for a common request | `commands/<name>.md` | route to an existing skill; add no reasoning |
| A narrated trace | `examples/` | `docs/examples.md` |

If the same paragraph would appear in more than one skill, it belongs in `rules/` or `knowledge/`, and the
skills link to it.

## Adding a product plugin

1. Copy an existing plugin directory as the skeleton and strip its product content
2. Write `capabilities.yaml` **first** — abstract capability ids, one namespace, `mcp_tools: TODO` until
   the real MCP surface has been inspected
3. Write `docs/mcp-integration.md` recording what is mapped and what is not
4. Write skills against those capabilities, each handling their absence
5. Add `.claude-plugin/plugin.json`, `package.json`, `VERSION`, `CHANGELOG.md`, `LICENSE`, `README.md`
6. Add the plugin to `.claude-plugin/marketplace.json` with `source: "./plugins/<name>"` and a version
   matching its `VERSION`
7. Add golden prompts under `tests/evals/golden-prompts/<plugin>/`

`playbooks/`, `examples/` and `commands/` are optional and validated only when present. A young plugin
should not invent five vertical playbooks it has no evidence for.

## Hard requirements

These are not style preferences. A change that breaks one of them will not be accepted.

1. **No MCP implementation.** No API clients, endpoints, tool schemas or request code. A plugin declares
   capabilities; the product's MCP provides them.
2. **No invented tool names.** Capability identifiers only, from the plugin's `capabilities.yaml`. Concrete
   tool mappings stay `TODO` until the real MCP surface is inspected.
3. **No hard-coded business assumptions.** No fixed campaign counts, node counts, sequence lengths, tier
   counts, holiday dates or threshold numbers. Derive from store data and state the derivation.
4. **No invented data.** No illustrative statistics presented as real, and no external benchmarks presented
   as this store's numbers. Documentation figures are labelled illustrative.
5. **No duplicated instructions.** Cite rules by number rather than paraphrasing them.
6. **No vendor-specific behaviour.** Nothing that depends on a particular agent host.
7. **No cross-plugin relative links.** A plugin never reaches outside its own directory by relative path.
8. **Safety rules are not negotiable.** `high_impact` and `destructive` actions always stop for explicit
   human approval.

## Making a change

1. Read the relevant guide above
2. Make the change
3. Run `python3 tests/validate.py` **and** `python3 tests/evals/run_evals.py`
4. Add or update a golden prompt if the change affects what a skill answers —
   see [tests/evals/README.md](tests/evals/README.md)
5. Update the plugin's `skills/README.md` if its skill set changed
6. Add an entry to the plugin's `CHANGELOG.md`, with skill versions where skills changed
7. Bump the plugin's `VERSION`, and the matching version in `.claude-plugin/marketplace.json`,
   `package.json` and `.claude-plugin/plugin.json` — validation asserts all four agree

## What validation checks

| Group | Asserts |
|---|---|
| `structure` | Repo and per-plugin required files and directories exist; every skill directory has a `SKILL.md`; a plugin's capability ids share one namespace |
| `spec` | Every skill passes the Agent Skills reference validator |
| `skill-validation` | Frontmatter parses and matches the plugin's schema; all fourteen sections present, in order, non-empty |
| `playbooks` | Playbook frontmatter and sections, where playbooks exist |
| `references` | Every capability and composed skill resolves within its own plugin; composition graph is acyclic; every relative link in the repository resolves |
| `duplication` | Skill names and display names are unique within a plugin |
| `schemas` | All schemas compile; valid fixtures pass; invalid fixtures fail; the broken-skill fixture is rejected |
| `versioning` | Each plugin's `VERSION` is semver, appears in its `CHANGELOG.md`, and matches both manifests; skill versions are semver |
| `marketplace` | Every listed plugin exists, every existing plugin is listed, and sources, names and versions agree |

And `run_evals.py` adds:

| Group | Asserts |
|---|---|
| `schema` / `skill-refs` / `rule-refs` | Eval cases are well-formed and reference real skills, composition and rules |
| `selection` | Every skill is lexically reachable from a prompt a user would type |
| `coverage` | No skill is without a golden prompt |
| `regression` | Expectations cannot change while the target skill's version stays put |

A green run means the repository is structurally sound. It does not mean the advice is good — that still
needs a human who knows the domain.

## Review expectations

A skill change is reviewed for whether it makes the agent decide *better*, not whether it adds more text.
Length is not thoroughness. Removing a section that added no decision is a good change.

The most common review outcomes:

- Restating a rule instead of citing it → cite it
- Adding a threshold number → derive it from store data instead
- Adding a skill that overlaps an existing one → extend the existing one
- Adding an example without the rejected alternative → add what was rejected and why
- A golden prompt that cannot find its skill → fix the **description**, not the prompt
- A skill in one plugin reaching into another plugin's rules → duplicate the constraint or raise it in
  review; do not link across the boundary

## Reporting a problem

- Structural or validation problems: open an issue with the failing output, naming the plugin
- Reasoning you disagree with: open an issue stating the rule or decision and what evidence contradicts it
- Security concerns: see [SECURITY.md](SECURITY.md) — do not open a public issue
