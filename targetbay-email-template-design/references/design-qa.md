# Design QA

The review before a template ships. Work the
[decision order](../SKILL.md#design-decision-order) top-down — a failure at level 1 leaves everything
below it untested, because the fix will move things.

## The four views that catch most problems

Cheap, and between them they cover the failure modes that reach recipients.

| View | Looking for |
|---|---|
| Narrow width, roughly 320–375px | Overflow, columns that did not stack, a stack in the wrong order, text touching the edge, a headline taking four lines |
| Images off | Whether the message still makes sense, whether the offer is still stated, whether blocks collapsed to nothing |
| Dark mode | Vanished logos, black text on a repainted background, bright white rectangles, a button label that lost its contrast |
| Fallback font | Reflowed headlines, blocks that overflow, a hierarchy that collapsed because the intermediate weight does not exist |

The fallback-font view is the one most often skipped, and the one affecting the largest share of
recipients — see [Typography](./typography.md).

## Design checklist

The shared rules — contrast, alt text, images off, dark mode, 16px body, tap targets — are the
authoring checklist in
[Accessibility](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/accessibility.md#authoring-checklist).
Run that one; do not keep a second copy here that drifts from it. These are the design decisions it
does not cover:

- [ ] Stacking order reads correctly both stacked and unstacked — [Layout](./layout.md)
- [ ] One spacing scale, three vertical tiers or fewer between elements
- [ ] No fixed-height blocks, overlapping elements or negative offsets
- [ ] Nothing important depends on a background image
- [ ] Hierarchy survives with only regular and bold available — [Typography](./typography.md)
- [ ] Two typefaces at most, each with a metric-compatible fallback
- [ ] Body left-aligned, nothing justified, measure within 45–75 characters
- [ ] Every foreground role has a named background and a dark counterpart —
      [Colour and Dark Mode](./colour-and-dark-mode.md)
- [ ] The action colour appears only on the action
- [ ] One primary call to action, reachable in the first screen, secondary actions subordinate —
      [CTA and Imagery](./cta-and-imagery.md)
- [ ] Button built from colour and text, label stating the outcome on one line
- [ ] Images exported at twice display width with declared dimensions; animation works as a still
- [ ] Preheader written deliberately; grid cells uniform — [Anatomy](./anatomy.md)
- [ ] Blocks come from the module library; anything new is a variant, not a fork

## Testing beyond preview

Rendering previews catch layout; they do not catch everything.

- **Send to real accounts.** Keep seed accounts on the major webmail providers, a desktop client and a
  phone, and open the message on each. A preview service renders a screenshot; a real account shows
  the message in its actual inbox, with the real preheader and the real dark mode treatment
- **Open it on a phone held at arm's length.** The first-screen and one-action checks are judged far
  faster this way than by reading a specification
- **Check the widest and narrowest content.** The longest product name, the longest locale, an order
  with one line and an order with twenty

Screen readers, zoom, keyboard and contrast tooling are in
[Accessibility](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/accessibility.md)
and belong in the same pass.
