#!/usr/bin/env python3
"""Validate the TargetBay Agent Skills marketplace.

Run from anywhere:  python3 tests/validate.py
Exits 0 when every check passes, 1 otherwise.

The repository is a marketplace of product plugins under `plugins/`. Every plugin is
self-contained — Claude Code ships only what lives under a plugin's `source` directory,
so a skill linking `../../rules/safety-rules.md` must find that file inside its own
plugin, not at the repository root. Most checks therefore run once per plugin; the
handful that are genuinely repo-wide (the relative-link sweep, the marketplace manifest)
run once at the root.

Check groups: structure, spec, skill-validation, playbooks, references, duplication,
schemas, versioning, marketplace.

`spec` runs the Agent Skills reference validator (https://agentskills.io/specification)
over every skill. `skill-validation` then applies this package's own, stricter contract
on top of it.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
    from skills_ref.validator import validate as spec_validate
except ImportError as exc:  # pragma: no cover - environment problem, not a package problem
    sys.exit(f"missing dependency: {exc}\ninstall with: python3 -m pip install -r tests/requirements.txt")

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
FIXTURES = ROOT / "tests" / "fixtures"

REQUIRED_SECTIONS = [
    "Purpose",
    "When to Use",
    "When Not to Use",
    "Required Context",
    "Required MCP Capabilities",
    "Inputs",
    "Decision Process",
    "Decision Rules",
    "Workflow",
    "Expected Output",
    "Validation",
    "Approval Requirements",
    "Examples",
    "Failure Handling",
]

PLAYBOOK_SECTIONS = [
    "Vertical Signals",
    "Default Adjustments",
    "Additional Rules",
    "Lifecycle Notes",
    "Channel Notes",
    "Known Limits",
]

PLAYBOOK_KEYS = {"name", "display_name", "version", "applies_to", "overrides"}

# Repo-level: governance, CI and the marketplace manifest. Product content lives in plugins.
REPO_REQUIRED_FILES = [
    "README.md",
    "package.json",
    "CHANGELOG.md",
    ".claude-plugin/marketplace.json",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "tests/requirements.txt",
]

REPO_REQUIRED_DIRS = ["plugins", "tests", ".github"]

# Per plugin: what a plugin must carry to be installable and self-contained.
PLUGIN_REQUIRED_FILES = [
    "README.md",
    "CHANGELOG.md",
    "VERSION",
    "LICENSE",
    "package.json",
    ".claude-plugin/plugin.json",
    "capabilities.yaml",
    "scripts/install.mjs",
    "scripts/install.sh",
    "skills/README.md",
    "rules/README.md",
    "rules/global-rules.md",
    "rules/safety-rules.md",
    "knowledge/README.md",
    "schemas/skill.schema.json",
    "schemas/skill-result.schema.json",
    "schemas/recommendation.schema.json",
    "docs/mcp-integration.md",
]

PLUGIN_REQUIRED_DIRS = ["skills", "rules", "knowledge", "schemas", "docs"]

# Validated when present, not required. A young plugin should not invent five vertical
# playbooks it has no evidence for — the same "never invent" discipline the package
# applies to MCP tool names.
PLUGIN_OPTIONAL_DIRS = ["playbooks", "examples", "commands"]

SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$")
HEADING = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
EXTERNAL = re.compile(r"^(https?:|mailto:|#)")
# A full URL back into this repository — a plugin's only legal way to reference a sibling.
SELF_BLOB = re.compile(
    r"^https://github\.com/targetbay360/targetbay-agent-skills/blob/[^/]+/([^#?]+)")

failures: list[str] = []
group_counts: dict[str, int] = {}


def check(group: str, ok: bool, message: str) -> bool:
    group_counts[group] = group_counts.get(group, 0) + 1
    if not ok:
        failures.append(f"{group}: {message}")
    return ok


def split_frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    """Return (frontmatter, body, error)."""
    if not text.startswith("---\n"):
        return None, text, "file does not start with YAML frontmatter"
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text, "frontmatter is not terminated"
    raw, body = text[4:end], text[end + 5 :]
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return None, body, f"frontmatter is not valid YAML: {exc}"
    if not isinstance(data, dict):
        return None, body, "frontmatter is not a mapping"
    return data, body, None


def meta(fm: dict, key: str) -> str:
    """Read a package-specific value. The Agent Skills spec allows no custom top-level
    frontmatter keys, so everything this package adds lives under `metadata.targetbay.*`
    as a string."""
    return (fm.get("metadata") or {}).get(f"targetbay.{key}", "")


def meta_list(fm: dict, key: str) -> list[str]:
    """Read a comma-separated metadata value as a list."""
    return [v.strip() for v in meta(fm, key).split(",") if v.strip()]


def section_errors(body: str, required: list[str]) -> list[str]:
    found = [m.group(1) for m in HEADING.finditer(body)]
    errs = []
    if found[: len(required)] != required:
        missing = [s for s in required if s not in found]
        if missing:
            errs.append(f"missing sections: {', '.join(missing)}")
        else:
            errs.append(f"sections out of order; got {found[: len(required)]}")
        return errs
    spans = [m.start() for m in HEADING.finditer(body)] + [len(body)]
    for i, name in enumerate(required):
        content = body[spans[i] : spans[i + 1]]
        content = content.split("\n", 1)[1] if "\n" in content else ""
        if not content.strip():
            errs.append(f"section '{name}' is empty")
    return errs


# ---------------------------------------------------------------------------- load

check("structure", PLUGINS.is_dir(), "missing directory: plugins/")
plugin_dirs = sorted(p for p in PLUGINS.iterdir() if p.is_dir()) if PLUGINS.is_dir() else []
check("structure", bool(plugin_dirs), "plugins/ contains no plugins")


class Plugin:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.name = path.name
        self.capabilities: set[str] = set()
        self.cap_doc: dict = {}
        self.skills: dict[str, dict] = {}
        self.skill_errors: dict[str, list[str]] = {}
        self.playbooks: list[Path] = []

        cap_path = path / "capabilities.yaml"
        if cap_path.is_file():
            self.cap_doc = yaml.safe_load(cap_path.read_text()) or {}
            for entry in self.cap_doc.get("capabilities", []):
                self.capabilities.add(entry["id"])

        for skill_file in sorted(path.glob("skills/*/SKILL.md")):
            fm, body, err = split_frontmatter(skill_file.read_text())
            key = skill_file.parent.name
            self.skill_errors[key] = [err] if err else []
            if fm is not None:
                self.skills[key] = {"fm": fm, "body": body, "path": skill_file}

        self.playbooks = sorted(path.glob("playbooks/*/PLAYBOOK.md"))


plugins = [Plugin(p) for p in plugin_dirs]


# ------------------------------------------------------------------------ structure

print("\nstructure")
for rel in REPO_REQUIRED_DIRS:
    check("structure", (ROOT / rel).is_dir(), f"missing directory: {rel}/")
for rel in REPO_REQUIRED_FILES:
    check("structure", (ROOT / rel).is_file(), f"missing file: {rel}")

for pl in plugins:
    for rel in PLUGIN_REQUIRED_DIRS:
        check("structure", (pl.path / rel).is_dir(), f"{pl.name}: missing directory: {rel}/")
    for rel in PLUGIN_REQUIRED_FILES:
        check("structure", (pl.path / rel).is_file(), f"{pl.name}: missing file: {rel}")
    if (pl.path / "skills").is_dir():
        for d in sorted(p for p in (pl.path / "skills").iterdir() if p.is_dir()):
            check("structure", (d / "SKILL.md").is_file(),
                  f"{pl.name}: skills/{d.name}/ has no SKILL.md")
    check("structure", bool(pl.skills), f"{pl.name}: no skills found")
    check("structure", bool(pl.capabilities), f"{pl.name}: capabilities.yaml declares no capabilities")

    # An unmapped registry is the documented state of an un-inspected MCP. A PARTLY mapped
    # one is different: once real tools start landing, every remaining TODO has to say why
    # it is still a TODO, so "not mapped yet" cannot quietly become "nobody looked".
    entries = pl.cap_doc.get("capabilities", [])
    partly_mapped = any(e.get("mcp_tools") != "TODO" for e in entries)

    for entry in entries:
        cid = entry.get("id", "<unnamed>")
        check("structure", "description" in entry and "access" in entry and "mcp_tools" in entry,
              f"{pl.name}: capability {cid} is missing description/access/mcp_tools")
        check("structure", entry.get("access") in {"read", "write", "send"},
              f"{pl.name}: capability {cid} has invalid access: {entry.get('access')}")
        if entry.get("mcp_tools") != "TODO":
            check("structure", bool(entry.get("mcp_tools")),
                  f"{pl.name}: capability {cid} has an empty mcp_tools mapping")
        elif partly_mapped:
            check("structure", bool(str(entry.get("notes", "")).strip()),
                  f"{pl.name}: capability {cid} is still TODO in a partly mapped registry "
                  f"and carries no notes explaining why")

    # one registry, one namespace: a plugin's capabilities must not straddle products
    prefixes = {cid.split(".", 1)[0] for cid in pl.capabilities}
    check("structure", len(prefixes) <= 1,
          f"{pl.name}: capability ids span several namespaces: {', '.join(sorted(prefixes))}")


# ----------------------------------------------------------------------------- spec

print("spec")
for pl in plugins:
    if not (pl.path / "skills").is_dir():
        continue
    for d in sorted(p for p in (pl.path / "skills").iterdir() if p.is_dir()):
        errs = spec_validate(d)
        check("spec", not errs, f"{pl.name}/{d.name}: " + "; ".join(errs))


# ------------------------------------------------------------------ skill-validation

print("skill-validation")


def skill_validator_for(pl: Plugin) -> Draft202012Validator | None:
    schema_file = pl.path / "schemas" / "skill.schema.json"
    if not schema_file.is_file():
        return None
    return Draft202012Validator(json.loads(schema_file.read_text()))


def validate_skill(validator: Draft202012Validator, fm: dict, body: str,
                   expect_dirname: str | None) -> list[str]:
    errs = [f"{e.json_path}: {e.message}" for e in validator.iter_errors(fm)]
    if expect_dirname and fm.get("name") != expect_dirname:
        errs.append(f"name '{fm.get('name')}' does not match directory '{expect_dirname}'")
    errs += section_errors(body, REQUIRED_SECTIONS)
    return errs


for pl in plugins:
    validator = skill_validator_for(pl)
    if not check("skill-validation", validator is not None,
                 f"{pl.name}: no schemas/skill.schema.json to validate against"):
        continue
    for name, s in pl.skills.items():
        errs = pl.skill_errors.get(name, []) + validate_skill(validator, s["fm"], s["body"], name)
        check("skill-validation", not errs, f"{pl.name}/{name}: " + "; ".join(errs))
    for name, errs in pl.skill_errors.items():
        if errs and name not in pl.skills:
            check("skill-validation", False, f"{pl.name}/{name}: " + "; ".join(errs))


# -------------------------------------------------------------------------- playbooks

print("playbooks")
for pl in plugins:
    if (pl.path / "playbooks").is_dir():
        check("playbooks", bool(pl.playbooks), f"{pl.name}: playbooks/ exists but holds no PLAYBOOK.md")
    for pb in pl.playbooks:
        fm, body, err = split_frontmatter(pb.read_text())
        rel = pb.relative_to(ROOT)
        if err:
            check("playbooks", False, f"{rel}: {err}")
            continue
        errs = []
        missing = PLAYBOOK_KEYS - set(fm)
        if missing:
            errs.append(f"missing frontmatter keys: {', '.join(sorted(missing))}")
        if fm.get("name") != pb.parent.name:
            errs.append(f"name '{fm.get('name')}' does not match directory '{pb.parent.name}'")
        if not SEMVER.match(str(fm.get("version", ""))):
            errs.append(f"version '{fm.get('version')}' is not semver")
        errs += section_errors(body, PLAYBOOK_SECTIONS)
        check("playbooks", not errs, f"{rel}: " + "; ".join(errs))


# ------------------------------------------------------------------------ references

print("references")
for pl in plugins:
    for name, s in pl.skills.items():
        for cap in meta_list(s["fm"], "requires"):
            check("references", cap in pl.capabilities,
                  f"{pl.name}/{name} requires unknown capability '{cap}'")
        for dep in meta_list(s["fm"], "composes"):
            check("references", dep in pl.skills,
                  f"{pl.name}/{name} composes unknown skill '{dep}'")
            check("references", dep != name, f"{pl.name}/{name} composes itself")

    # composition graph must be acyclic, per plugin
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {n: WHITE for n in pl.skills}
    cycles: list[str] = []

    def visit(node: str, stack: list[str], pl: Plugin = pl, colour: dict = colour,
              cycles: list = cycles) -> None:
        colour[node] = GREY
        for nxt in meta_list(pl.skills[node]["fm"], "composes"):
            if nxt not in pl.skills:
                continue
            if colour[nxt] == GREY:
                cycles.append(" -> ".join(stack + [node, nxt]))
            elif colour[nxt] == WHITE:
                visit(nxt, stack + [node])
        colour[node] = BLACK

    for n in pl.skills:
        if colour[n] == WHITE:
            visit(n, [])
    check("references", not cycles, f"{pl.name}: composition cycle: " + "; ".join(cycles))

# every relative markdown link resolves, repo-wide. This is the safety net for moving
# content between directories (fixtures excluded: they are deliberately broken).
#
# A plugin may not link outside itself by relative path — Claude Code ships only what is
# under the plugin's `source` — so cross-plugin references are written as full GitHub URLs
# to this same repository. Those resolve to a path here, so they are checked too: a file
# renamed in one plugin should not silently break a sibling's link to it.
for md in sorted(ROOT.rglob("*.md")):
    if FIXTURES in md.parents or "node_modules" in md.parts:
        continue
    for target in MD_LINK.findall(FENCE.sub("", md.read_text())):
        self_ref = SELF_BLOB.match(target)
        if self_ref:
            path = (ROOT / self_ref.group(1)).resolve()
            check("references", path.exists(),
                  f"{md.relative_to(ROOT)} links to missing repository path '{self_ref.group(1)}'")
            continue
        if EXTERNAL.match(target):
            continue
        path = (md.parent / target.split("#", 1)[0]).resolve()
        check("references", path.exists(),
              f"{md.relative_to(ROOT)} links to missing path '{target}'")


# ----------------------------------------------------------------------- duplication

print("duplication")
# Scoped per plugin: two products may legitimately both want an `audience-discovery`.
for pl in plugins:
    for field in ("name", "display_name"):
        seen: dict[str, str] = {}
        for key, s in pl.skills.items():
            value = s["fm"].get("name") if field == "name" else meta(s["fm"], "display_name")
            check("duplication", value not in seen,
                  f"{pl.name}: duplicate {field} '{value}' in {key} and {seen.get(value)}")
            seen[value] = key


# --------------------------------------------------------------------------- schemas

print("schemas")
for pl in plugins:
    validators: dict[str, Draft202012Validator] = {}
    for schema_file in sorted((pl.path / "schemas").glob("*.json")):
        stem = schema_file.stem.replace(".schema", "")
        try:
            schema = json.loads(schema_file.read_text())
            Draft202012Validator.check_schema(schema)
            validators[stem] = Draft202012Validator(schema)
            check("schemas", True, "")
        except Exception as exc:
            check("schemas", False, f"{pl.name}: {schema_file.name} does not compile: {exc}")

    # The shared fixtures are the contract every plugin's copy of a schema must honour.
    for fixture in sorted((FIXTURES / "valid").glob("*.json")):
        v = validators.get(fixture.stem)
        if v is None:
            continue  # plugin does not carry this schema; not every product plans workflows
        errs = [f"{e.json_path}: {e.message}"
                for e in v.iter_errors(json.loads(fixture.read_text()))]
        check("schemas", not errs, f"{pl.name}: valid fixture {fixture.name} failed: " + "; ".join(errs))

    for fixture in sorted((FIXTURES / "invalid").glob("*.json")):
        v = validators.get(fixture.stem)
        if v is None:
            continue
        errs = list(v.iter_errors(json.loads(fixture.read_text())))
        check("schemas", bool(errs),
              f"{pl.name}: invalid fixture {fixture.name} was accepted but must be rejected")

    # the validator must reject a deliberately broken skill
    broken = FIXTURES / "broken-skill" / "SKILL.md"
    skill_v = validators.get("skill")
    if check("schemas", broken.is_file(), "missing fixture tests/fixtures/broken-skill/SKILL.md") \
            and skill_v is not None:
        fm, body, err = split_frontmatter(broken.read_text())
        errs = [err] if err else validate_skill(skill_v, fm, body, "broken-skill")
        check("schemas", bool(errs),
              f"{pl.name}: broken-skill fixture was accepted; skill validation is not catching errors")


# ------------------------------------------------------------------------ versioning

print("versioning")
for pl in plugins:
    version_file = pl.path / "VERSION"
    if not version_file.is_file():
        continue
    version = version_file.read_text().strip()
    check("versioning", bool(SEMVER.match(version)), f"{pl.name}: VERSION '{version}' is not semver")
    changelog = pl.path / "CHANGELOG.md"
    if changelog.is_file():
        check("versioning", version in changelog.read_text(),
              f"{pl.name}: CHANGELOG.md does not mention version {version}")
    for manifest in ("package.json", ".claude-plugin/plugin.json"):
        mf = pl.path / manifest
        if not mf.is_file():
            continue
        declared = json.loads(mf.read_text()).get("version")
        check("versioning", declared == version,
              f"{pl.name}: {manifest} is {declared}, VERSION is {version}")
    for name, s in pl.skills.items():
        v = meta(s["fm"], "version")
        check("versioning", bool(SEMVER.match(v)), f"{pl.name}/{name} version '{v}' is not semver")
    cap_version = str(pl.cap_doc.get("version", ""))
    check("versioning", bool(SEMVER.match(cap_version)),
          f"{pl.name}: capabilities.yaml version '{cap_version}' is not semver")


# ----------------------------------------------------------------------- marketplace

print("marketplace")
manifest_path = ROOT / ".claude-plugin" / "marketplace.json"
if check("marketplace", manifest_path.is_file(), "missing .claude-plugin/marketplace.json"):
    manifest = json.loads(manifest_path.read_text())
    entries = {e["name"]: e for e in manifest.get("plugins", [])}
    listed = set(entries)
    present = {pl.name for pl in plugins}

    for missing in sorted(listed - present):
        check("marketplace", False, f"marketplace lists '{missing}' but plugins/{missing}/ does not exist")
    for unlisted in sorted(present - listed):
        check("marketplace", False, f"plugins/{unlisted}/ exists but the marketplace does not list it")

    for pl in plugins:
        entry = entries.get(pl.name)
        if entry is None:
            continue
        check("marketplace", entry.get("source") == f"./plugins/{pl.name}",
              f"{pl.name}: marketplace source is '{entry.get('source')}', "
              f"expected './plugins/{pl.name}'")
        version_file = pl.path / "VERSION"
        if version_file.is_file():
            check("marketplace", entry.get("version") == version_file.read_text().strip(),
                  f"{pl.name}: marketplace version is {entry.get('version')}, "
                  f"VERSION is {version_file.read_text().strip()}")
        plugin_json = pl.path / ".claude-plugin" / "plugin.json"
        if plugin_json.is_file():
            declared = json.loads(plugin_json.read_text()).get("name")
            check("marketplace", declared == pl.name,
                  f"{pl.name}: plugin.json name is '{declared}', expected '{pl.name}'")


# ---------------------------------------------------------------------------- report

total = sum(group_counts.values())
print()
if failures:
    print(f"FAILED — {len(failures)} of {total} checks\n")
    for f in failures:
        print(f"  ✗ {f}")
    print()
    sys.exit(1)

print(f"PASSED — {total} checks across {len(group_counts)} groups")
for pl in plugins:
    print(f"  {pl.name}: {len(pl.skills)} skills, {len(pl.capabilities)} capabilities, "
          f"{len(pl.playbooks)} playbooks")
sys.exit(0)
