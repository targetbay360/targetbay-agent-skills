#!/usr/bin/env python3
"""Validate the TargetBay Email & SMS Marketing Skills package.

Run from anywhere:  python3 tests/validate.py
Exits 0 when every check passes, 1 otherwise.

Check groups: structure, spec, skill-validation, playbooks, references, duplication,
schemas, versioning.

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

REQUIRED_FILES = [
    "README.md",
    "package.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "scripts/install.mjs",
    "scripts/install.sh",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "VERSION",
    "capabilities.yaml",
    "skills/README.md",
    "rules/README.md",
    "knowledge/README.md",
    "playbooks/README.md",
    "schemas/skill.schema.json",
    "schemas/skill-result.schema.json",
    "schemas/recommendation.schema.json",
    "schemas/workflow.schema.json",
    "docs/architecture.md",
    "docs/skill-authoring.md",
    "docs/mcp-integration.md",
    "docs/rules.md",
    "docs/versioning.md",
    "docs/examples.md",
    "tests/requirements.txt",
]

REQUIRED_DIRS = ["skills", "rules", "knowledge", "playbooks", "schemas", "docs", "examples", "tests"]

SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$")
HEADING = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
EXTERNAL = re.compile(r"^(https?:|mailto:|#)")

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


# --------------------------------------------------------------------------- load

capabilities: set[str] = set()
cap_path = ROOT / "capabilities.yaml"
if cap_path.exists():
    cap_doc = yaml.safe_load(cap_path.read_text())
    for entry in (cap_doc or {}).get("capabilities", []):
        capabilities.add(entry["id"])

skills: dict[str, dict] = {}
skill_errors: dict[str, list[str]] = {}
for skill_file in sorted(ROOT.glob("skills/*/SKILL.md")):
    fm, body, err = split_frontmatter(skill_file.read_text())
    key = skill_file.parent.name
    skill_errors[key] = [err] if err else []
    if fm is not None:
        skills[key] = {"fm": fm, "body": body, "path": skill_file}


# ----------------------------------------------------------------------- structure

print("\nstructure")
for rel in REQUIRED_DIRS:
    check("structure", (ROOT / rel).is_dir(), f"missing directory: {rel}/")
for rel in REQUIRED_FILES:
    check("structure", (ROOT / rel).is_file(), f"missing file: {rel}")
for d in sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir()):
    check("structure", (d / "SKILL.md").is_file(), f"skills/{d.name}/ has no SKILL.md")
check("structure", bool(skills), "no skills found")
check("structure", bool(capabilities), "capabilities.yaml declares no capabilities")
for entry in (yaml.safe_load(cap_path.read_text()) or {}).get("capabilities", []):
    cid = entry.get("id", "<unnamed>")
    check("structure", "description" in entry and "access" in entry and "mcp_tools" in entry,
          f"capability {cid} is missing description/access/mcp_tools")
    check("structure", entry.get("access") in {"read", "write", "send"},
          f"capability {cid} has invalid access: {entry.get('access')}")


# ----------------------------------------------------------------------------- spec

print("spec")
for d in sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir()):
    errs = spec_validate(d)
    check("spec", not errs, f"{d.name}: " + "; ".join(errs))


# ---------------------------------------------------------------- skill-validation

print("skill-validation")
skill_schema = json.loads((ROOT / "schemas" / "skill.schema.json").read_text())
skill_validator = Draft202012Validator(skill_schema)


def validate_skill(name: str, fm: dict, body: str, expect_dirname: str | None) -> list[str]:
    errs = [f"{e.json_path}: {e.message}" for e in skill_validator.iter_errors(fm)]
    if expect_dirname and fm.get("name") != expect_dirname:
        errs.append(f"name '{fm.get('name')}' does not match directory '{expect_dirname}'")
    errs += section_errors(body, REQUIRED_SECTIONS)
    return errs


for name, s in skills.items():
    errs = skill_errors.get(name, []) + validate_skill(name, s["fm"], s["body"], name)
    check("skill-validation", not errs, f"{name}: " + "; ".join(errs))
for name, errs in skill_errors.items():
    if errs and name not in skills:
        check("skill-validation", False, f"{name}: " + "; ".join(errs))


# ------------------------------------------------------------------------ playbooks

print("playbooks")
playbooks = sorted(ROOT.glob("playbooks/*/PLAYBOOK.md"))
check("playbooks", bool(playbooks), "no playbooks found")
for pb in playbooks:
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


# ----------------------------------------------------------------------- references

print("references")
for name, s in skills.items():
    for cap in meta_list(s["fm"], "requires"):
        check("references", cap in capabilities,
              f"{name} requires unknown capability '{cap}'")
    for dep in meta_list(s["fm"], "composes"):
        check("references", dep in skills, f"{name} composes unknown skill '{dep}'")
        check("references", dep != name, f"{name} composes itself")

# composition graph must be acyclic
WHITE, GREY, BLACK = 0, 1, 2
colour = {n: WHITE for n in skills}
cycles: list[str] = []


def visit(node: str, stack: list[str]) -> None:
    colour[node] = GREY
    for nxt in meta_list(skills[node]["fm"], "composes"):
        if nxt not in skills:
            continue
        if colour[nxt] == GREY:
            cycles.append(" -> ".join(stack + [node, nxt]))
        elif colour[nxt] == WHITE:
            visit(nxt, stack + [node])
    colour[node] = BLACK


for n in skills:
    if colour[n] == WHITE:
        visit(n, [])
check("references", not cycles, "composition cycle: " + "; ".join(cycles))

# every relative markdown link resolves (fixtures excluded: they are deliberately broken)
for md in sorted(ROOT.rglob("*.md")):
    if FIXTURES in md.parents:
        continue
    # fenced code blocks are samples, not references
    for target in MD_LINK.findall(FENCE.sub("", md.read_text())):
        if EXTERNAL.match(target):
            continue
        path = (md.parent / target.split("#", 1)[0]).resolve()
        check("references", path.exists(),
              f"{md.relative_to(ROOT)} links to missing path '{target}'")


# ---------------------------------------------------------------------- duplication

print("duplication")
for field in ("name", "display_name"):
    seen: dict[str, str] = {}
    for key, s in skills.items():
        value = s["fm"].get("name") if field == "name" else meta(s["fm"], "display_name")
        check("duplication", value not in seen,
              f"duplicate {field} '{value}' in {key} and {seen.get(value)}")
        seen[value] = key


# -------------------------------------------------------------------------- schemas

print("schemas")
validators: dict[str, Draft202012Validator] = {}
for schema_file in sorted((ROOT / "schemas").glob("*.json")):
    stem = schema_file.stem.replace(".schema", "")
    try:
        schema = json.loads(schema_file.read_text())
        Draft202012Validator.check_schema(schema)
        validators[stem] = Draft202012Validator(schema)
        check("schemas", True, "")
    except Exception as exc:
        check("schemas", False, f"{schema_file.name} does not compile: {exc}")

for fixture in sorted((FIXTURES / "valid").glob("*.json")):
    v = validators.get(fixture.stem)
    if not check("schemas", v is not None, f"no schema for fixture {fixture.name}"):
        continue
    errs = [f"{e.json_path}: {e.message}" for e in v.iter_errors(json.loads(fixture.read_text()))]
    check("schemas", not errs, f"valid fixture {fixture.name} failed: " + "; ".join(errs))

for fixture in sorted((FIXTURES / "invalid").glob("*.json")):
    v = validators.get(fixture.stem)
    if not check("schemas", v is not None, f"no schema for fixture {fixture.name}"):
        continue
    errs = list(v.iter_errors(json.loads(fixture.read_text())))
    check("schemas", bool(errs), f"invalid fixture {fixture.name} was accepted but must be rejected")

# the validator must reject a deliberately broken skill
broken = FIXTURES / "broken-skill" / "SKILL.md"
if check("schemas", broken.is_file(), "missing fixture tests/fixtures/broken-skill/SKILL.md"):
    fm, body, err = split_frontmatter(broken.read_text())
    errs = [err] if err else validate_skill("broken-skill", fm, body, "broken-skill")
    check("schemas", bool(errs),
          "broken-skill fixture was accepted; skill validation is not catching errors")


# ----------------------------------------------------------------------- versioning

print("versioning")
version = (ROOT / "VERSION").read_text().strip()
check("versioning", bool(SEMVER.match(version)), f"VERSION '{version}' is not semver")
check("versioning", version in (ROOT / "CHANGELOG.md").read_text(),
      f"CHANGELOG.md does not mention version {version}")
for name, s in skills.items():
    v = meta(s["fm"], "version")
    check("versioning", bool(SEMVER.match(v)), f"{name} version '{v}' is not semver")
cap_version = str((yaml.safe_load(cap_path.read_text()) or {}).get("version", ""))
check("versioning", bool(SEMVER.match(cap_version)),
      f"capabilities.yaml version '{cap_version}' is not semver")


# --------------------------------------------------------------------------- report

total = sum(group_counts.values())
print()
if failures:
    print(f"FAILED — {len(failures)} of {total} checks\n")
    for f in failures:
        print(f"  ✗ {f}")
    print()
    sys.exit(1)

print(f"PASSED — {total} checks across {len(group_counts)} groups")
print(f"  {len(skills)} skills, {len(capabilities)} capabilities, {len(playbooks)} playbooks")
sys.exit(0)
