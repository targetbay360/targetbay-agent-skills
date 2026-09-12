# Playbooks

A playbook is a vertical overlay. It adjusts what a skill defaults to, without changing what the skill
does.

```
Core skill  +  Playbook  +  Store context  +  BayEngage MCP  =  the actual recommendation
   ↑              ↑              ↑                 ↑
 how to      vertical      this store's       real data
 decide      defaults       specifics        and actions
```

Skills stay vertical-agnostic. Everything a fashion store needs that a B2B supplier does not belongs
here, not in a conditional inside a skill.

## What a playbook may and may not do

| May | May not |
|---|---|
| Adjust default thresholds and windows | Change a skill's decision process |
| Reprioritise which levers are tried first | Override a rule in [../rules/](../rules/README.md) |
| Add vertical-specific rules | Loosen anything in [../rules/safety-rules.md](../rules/safety-rules.md) |
| Note which lifecycle stages matter most here | Introduce new capability requirements |
| Note channel conventions for the vertical | Assert store-specific facts as universal |
| Flag what is usually true and worth checking | Replace evidence with vertical assumption |

A playbook is a **prior**, not a fact. Every adjustment it suggests is checked against the store's own
data before it is used. Where the store's data disagrees with the playbook, the data wins — this is
[../rules/global-rules.md#G3](../rules/global-rules.md) applied to the overlay itself.

## Precedence

```
safety-rules  >  global-rules  >  domain rules  >  PLAYBOOK  >  store context
```

A playbook may tighten a rule. It may never loosen one. See [../docs/rules.md](../docs/rules.md).

## The contract

Every `playbooks/<vertical>/PLAYBOOK.md` has this frontmatter:

```yaml
---
name: ecommerce
display_name: General E-commerce
version: 1.0.0
applies_to: Direct-to-consumer online retail with a repeat-purchase catalogue.
overrides:
  - default thresholds
  - lever priority
---
```

And these six sections, in order:

`Vertical Signals` · `Default Adjustments` · `Additional Rules` · `Lifecycle Notes` · `Channel Notes` ·
`Known Limits`

`Known Limits` is required, and it is not a formality: it is where a playbook states the store types it
gets wrong. A playbook without stated limits will be applied where it does not belong.

## Shipped playbooks

| Playbook | Applies to |
|---|---|
| [ecommerce](ecommerce/PLAYBOOK.md) | General direct-to-consumer online retail — the baseline overlay |
| [retail](retail/PLAYBOOK.md) | Multi-channel retail with physical locations |
| [fashion](fashion/PLAYBOOK.md) | Apparel, footwear and accessories |
| [beauty](beauty/PLAYBOOK.md) | Cosmetics, skincare and personal care |
| [b2b](b2b/PLAYBOOK.md) | Business-to-business and wholesale |

`ecommerce` is the general case. The others assume it and state their differences from it.

## Using a playbook

A skill receives the playbook as an optional `playbook` input. When one is supplied, the skill applies its
adjustments as starting points and says in its output which adjustments came from the playbook, so a
reviewer can tell a vertical default from a data-driven conclusion.

When no playbook is supplied, skills use their own defaults and derive everything else from store data.
Skills must work correctly with no playbook at all.

## Adding one

Copy the frontmatter and the six section headings, fill them with adjustments you can justify, be
specific about `Known Limits`, and run `python3 tests/validate.py`.

Keep playbooks short. A playbook that restates general marketing advice is noise; a playbook that names
the three things this vertical does differently is useful.
