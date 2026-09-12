## What changed

<!-- One or two sentences. Which skills, rules, playbooks or docs does this touch? -->

## Why

<!-- The problem this solves. If it came from an issue, link it. -->

## Checklist

- [ ] `python3 tests/validate.py` passes
- [ ] `python3 tests/evals/run_evals.py` passes
- [ ] Skill frontmatter stays within the Agent Skills specification — anything
      package-specific lives under `metadata` as a `targetbay.*` string
- [ ] `VERSION`, `package.json` and `.claude-plugin/plugin.json` still agree, and
      `CHANGELOG.md` has an entry if this is user-visible
- [ ] If this touches `rules/safety-rules.md` or any approval gate, I have read the
      **Agent safety** section of [SECURITY.md](../SECURITY.md) — removing a gate,
      broadening an approval scope, or letting a skill proceed on unverified data is
      a security change and will be reviewed as one
