# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A marketplace of Agent Skills packages for TargetBay products. **Content only** — Markdown, YAML
frontmatter and JSON Schema. No build step, no runtime, no network calls in any file. The only code is
`tests/*.py` and a zero-dependency `scripts/install.mjs` per plugin.

Skills teach an agent *how to decide*; the product MCP servers (separate repos) supply *what it can do*.
A skill therefore declares abstract capability ids (`email_sms.segmentation`), never tool names.

## Commands

```bash
python3 -m pip install -r tests/requirements.txt   # pyyaml, jsonschema, skills-ref
python3 tests/validate.py                          # structure/spec/contracts — all plugins
python3 tests/evals/run_evals.py                   # golden prompts — all plugins
npm run validate                                   # both of the above
```

There is no per-plugin or per-group filter; both runners sweep everything and exit 1 with a list of
failures. A `.venv/` is present — `.venv/bin/python`, and `.venv/bin/agentskills validate <skill-dir>`
for the reference CLI that CI also runs over every skill.

Eval-specific flags:

```bash
python3 tests/evals/run_evals.py --update   # rewrite expectations.lock after an INTENDED change
python3 tests/evals/run_evals.py --emit     # write model-dependent prompt packs to tests/evals/out/
```

Run **both** runners after any change. CI (`.github/workflows/validate.yml`) additionally re-checks
manifest parsing, version agreement and that each installer copies every skill.

## Layout and the self-containment rule

```
.claude-plugin/marketplace.json            one entry per plugin, source ./plugins/<name>
plugins/<name>/                            a product plugin — self-contained
  skills/<name>/SKILL.md  rules/  knowledge/  schemas/  commands/  docs/  scripts/
  playbooks/  examples/                    targetbay-email-sms only
  capabilities.yaml  VERSION  CHANGELOG.md  package.json  .claude-plugin/plugin.json
tests/                                     validate.py, evals/, fixtures/
docs/mcp-capability-inventory.md           the Phase 0 worksheet — every capability is still unmapped
targetbay-email-sms-best-practices/        standalone reference skills — NOT plugins,
targetbay-email-template-design/           not in the marketplace, do not follow the
targetbay-marketing-automation-recipes/    plugin contract, installed by copying the directory
```

Claude Code ships only what lives under a plugin's `source` directory, so **a plugin never reaches
outside itself by relative path**. Link within the plugin relatively; link anywhere else (another
plugin, a repo-root file, a standalone skill) by full `https://github.com/targetbay360/targetbay-agent-skills/...`
URL. `validate.py` sweeps every relative Markdown link in the repo (except `tests/fixtures/`) and fails
on one that does not resolve, so this is enforced, not remembered.

Four plugins: `targetbay-email-sms` (38 skills), `targetbay-onboarding` (10, cross-product sequencing +
onsite), `targetbay-loyalty` (6), `targetbay-reviews` (5).

## The skill contract

Frontmatter is exactly the six Agent Skills spec fields; everything TargetBay-specific is a *string*
under `metadata` as `targetbay.*` (lists are comma-space separated — the spec allows no other type).
Required: `display_name`, `version`, `category`, `requires`, `risk_level`, `execution_mode`, `status`;
optional `composes`, `deprecated_by`. Enums live in each plugin's `schemas/skill.schema.json`.
`name` must equal the directory name.

Thirteen `##` sections, present, non-empty and in this order:

`Purpose` · `When to Use` · `When Not to Use` · `Required Context` · `Required MCP Capabilities` ·
`Decision Process` · `Decision Rules` · `Workflow` · `Expected Output` · `Validation` ·
`Approval Requirements` · `Examples` · `Failure Handling`

`requires` must resolve in the same plugin's `capabilities.yaml`; `composes` must name skills in the
same plugin and keep the graph acyclic. One skill sits at the bottom of each composition chain
(e.g. `audience-discovery`) so "which customers" has exactly one implementation.

## Rules vs knowledge vs skills

- `rules/` — constraints binding every skill, numbered per file (`G1`, `S7`, `F6`, `C4`). Skills **cite
  by anchor** (`../../rules/frequency-rules.md`, plus the number in prose); they never restate a rule.
  Precedence: safety > global > domain > playbook overlay > store context. A playbook or store may
  tighten a rule, never loosen a safety rule.
- `knowledge/` — durable domain theory.
- `skills/` — one objective each. If a paragraph would appear in two skills, it belongs in `rules/` or
  `knowledge/`.
- `commands/` — thin shortcuts that route to a skill; reasoning stays in the skill.

Anything the platform enforces deterministically (consent, suppression, hard caps, legal opt-out) is the
platform's job — do not reimplement it here.

## Hard requirements (a change breaking one will not be accepted)

1. No MCP implementation — no endpoints, clients, tool schemas or request code.
2. No invented tool names. `mcp_tools: TODO` stays until the real MCP surface is inspected.
3. No hard-coded business assumptions — no fixed campaign/node/tier counts, holiday dates or threshold
   numbers. Derive from store data and state the derivation.
4. No invented data. External benchmarks are never presented as this store's numbers; illustrative
   figures are labelled illustrative.
5. Cite rules, do not paraphrase them.
6. No vendor-specific (agent-host) behaviour.
7. No cross-plugin relative links.
8. `high_impact` and `destructive` always stop for explicit human approval, with blast radius shown
   first. `blocked` and `partial` are first-class results — a skill missing data says so rather than
   filling the gap.

## Versioning and release

A plugin's version appears in **four** places that validation asserts agree: `VERSION`,
`package.json`, `.claude-plugin/plugin.json`, and its entry in `.claude-plugin/marketplace.json` — plus
an entry in the plugin's `CHANGELOG.md`. Skill versions (`metadata.targetbay.version`) are independent
semver.

Plugins release independently on a `<plugin>@<version>` git tag (e.g. `targetbay-email-sms@4.1.0`),
which validates the whole repo, then publishes to npm and GitHub Packages.

## Evals: the parts that bite

- `tests/evals/expectations.lock` hashes each case's expectations against the targeted skill's version.
  Changing what a case expects **without bumping that skill's version** fails. That is deliberate: run
  `--update` only after an intended behaviour change that carries a version bump.
- `coverage` requires every skill in every plugin to be the expected answer to at least one prompt, so a
  new skill needs a golden prompt under `tests/evals/golden-prompts/<plugin>/`.
- `skill-refs` fails when a case claims a `composes` edge the frontmatter no longer declares — the usual
  casualty of a composition refactor.
- `selection` is a lexical tf-idf proxy with a documented ceiling, scored per plugin. **When a case
  cannot find its skill, fix the skill's `description`, not the prompt** — that is what the check is for.
  Use `selection: skip` only when the case asserts behaviour rather than routing (see any plugin's
  `safety.yaml`).

## Change checklist

Run both validators · add/update a golden prompt if what a skill answers changed · update the plugin's
`skills/README.md` if its skill set changed · add a `CHANGELOG.md` entry · bump `VERSION` in all four
places.

Guides live in `plugins/targetbay-email-sms/docs/` (`skill-authoring.md`, `rules.md`, `architecture.md`,
`examples.md`, `versioning.md`) and apply to all four plugins; every plugin carries its own
`docs/mcp-integration.md` and `knowledge/README.md`.

Review standard: a change is judged on whether the agent decides *better*, not on added text. Removing a
section that carried no decision is a good change.
