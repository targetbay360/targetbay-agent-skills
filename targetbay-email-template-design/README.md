```
  ╔═══════════════════════════════════════════╗
  ║                                           ║
  ║   T A R G E T B A Y                       ║
  ║                                           ║
  ║   Email — Template Design                 ║
  ║                                           ║
  ╚═══════════════════════════════════════════╝
```

# TargetBay Email Template Design

An agent skill for designing ecommerce email templates. Covers layout and spacing, email-safe
typography, colour and dark mode, template anatomy, calls to action and imagery, and the review that
happens before a template ships.

Email is constrained design, and the constraint is the renderer rather than taste. Every rule here
exists because a specific rendering reality makes the alternative fail.

## What it is not

No markup. These are design decisions; the templating layer implements them.

It also does not cover *whether the message arrives* or *when to send it*. That is the companion
skill:
[Email & SMS Best Practices](https://github.com/targetbay360/targetbay-agent-skills/tree/main/targetbay-email-sms-best-practices)
— deliverability, compliance, lifecycle flows and accessibility. Where the two overlap, this skill
links rather than restates.

## Structure

```
SKILL.md                              routing hub and the design decision order
references/layout.md                  width, columns, spacing, bands, tap targets
references/typography.md              font stacks, scale, measure, weight
references/colour-and-dark-mode.md    semantic roles, contrast pairs, the dark variant
references/anatomy.md                 blocks, shapes by message type, module library
references/cta-and-imagery.md         one action, button design, images off
references/design-qa.md               the review before sign-off
```

## Quick start

Copy this directory into an agent host's skills path. It has no dependencies and is not published to
the marketplace.

## License

MIT
