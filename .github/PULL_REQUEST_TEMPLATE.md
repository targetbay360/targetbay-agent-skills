## Plugin

<!-- Which plugin does this touch? bayengage-marketing / targetbay-reviews / targetbay-loyalty /
     targetbay-personalization / repository-level (tooling, marketplace, CI). -->

## What changed

<!-- One or two sentences. Which skills, rules, knowledge or docs does this touch? -->

## Why

<!-- The problem this solves. If it came from an issue, link it. -->

## Checklist

- [ ] `python3 tests/validate.py` passes
- [ ] `python3 tests/evals/run_evals.py` passes
- [ ] Skill frontmatter stays within the Agent Skills specification — anything
      package-specific lives under `metadata` as a `targetbay.*` string
- [ ] Nothing inside a plugin links outside its own directory by relative path —
      repository-level files are referenced by full URL, because a relative link to them
      is dead for anyone who installed the plugin
- [ ] The plugin's `VERSION`, `package.json`, `.claude-plugin/plugin.json` and its entry in
      `.claude-plugin/marketplace.json` still agree, and its `CHANGELOG.md` has an entry if
      this is user-visible
- [ ] Golden prompts added or updated under `tests/evals/golden-prompts/<plugin>/`, and
      `--update` run if an expectation changed on purpose
- [ ] If this touches a plugin's `rules/safety-rules.md` or any approval gate, I have read the
      **Agent safety** section of [SECURITY.md](../SECURITY.md) — removing a gate,
      broadening an approval scope, or letting a skill proceed on unverified data is
      a security change and will be reviewed as one
