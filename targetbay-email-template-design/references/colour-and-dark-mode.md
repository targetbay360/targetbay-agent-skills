# Colour and Dark Mode

A palette for email is not the brand palette. It is a small set of *pairs* — a foreground and the
background it sits on — chosen so that every pair is legible, and so that a second set exists for
dark mode.

Clients do one of three things with dark mode: leave the message alone, swap colours by rule, or
force a full inversion. The design consequence is below; the client-by-client detail, alt text and
the contrast targets are in
[Accessibility](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/accessibility.md).

## Define roles, not colours

Assign every colour a job. A template built from named roles can be recoloured for a campaign, a
season or a sub-brand by swapping values; one built from hex codes scattered across blocks cannot.

| Role | Job | Pairs with |
|---|---|---|
| `canvas` | The area outside the message body | — |
| `surface` | A band or card background | `on-surface`, `muted` |
| `on-surface` | Body text | `surface` |
| `muted` | Secondary text — captions, timestamps, legal | `surface` |
| `border` | Dividers, card edges, table rules | `surface` |
| `primary` | The call to action, and nothing else | `on-primary` |
| `on-primary` | The label sitting on the primary colour | `primary` |
| `accent` | Badges, sale flags, highlights | its own text colour |
| `success` / `warning` / `error` | Transactional status | their own text colours |

The discipline that makes this work: **a foreground role is never chosen without naming the
background it sits on.** "Grey text" is not a decision. "`muted` on `surface`, checked at WCAG's
4.5:1" is. The targets themselves are in
[Accessibility](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/accessibility.md);
this document is the derivation that meets them.

## Reserve the action colour

Use one colour for the primary action, and use it nowhere else. When the brand colour is also the
heading colour, the link colour, the badge colour and the divider colour, the button stops being
findable — it is simply more of the same colour, in a rectangle.

If the brand has one colour and it must appear throughout, give the action a distinct treatment
instead: the brand colour as a solid fill for the button, and a restrained tint or a neutral for
everything else.

## Mapping a brand palette to email

Brand palettes are usually chosen for signage, packaging and large web hero areas, where a colour is
seen in quantity. Email uses colour in small text and small controls, where the same value often
fails.

Three adjustments, in order:

1. **Derive a text-safe variant of the brand colour.** A mid-tone brand colour used as body text or as
   a link on white rarely reaches 4.5:1. Darken it until it does, and keep that variant as the email
   text token. The logo keeps the original; text does not have to.
2. **Derive a surface tint.** The brand colour at full strength as a band background leaves nothing
   legible on it. A very light tint of it gives a branded band that still takes ordinary body text.
3. **Check the button pair specifically** — the label against the button fill, not the button
   against the page, per Accessibility. A brand yellow with white text is the failure this catches.

Where a brand guideline and a contrast target conflict, the contrast target wins and the guideline
gains a documented email exception.

## Avoid the absolute ends

Pure `#000000` on pure `#FFFFFF` is harsher than it needs to be, and black text is also what
disappears when a client repaints an implicit white background and leaves the text alone. Use a
near-black around 10–15% lightness for text and an off-white for surfaces. Both look better and both
fail less badly.

Every band declares its own background explicitly, and its text colour is declared with it.
This is a layout requirement as much as a colour one — see [Layout](./layout.md) — but it is the
palette that has to supply a defined pair for every band, including the ones that look white.

## Designing the dark variant

Build a second set of values for the same roles. Do not invert.

- **Darken surfaces to a dark neutral, not to black.** A very dark grey shows elevation and keeps
  borders visible; pure black flattens everything
- **Lighten and desaturate the foreground.** Full-strength white text on a dark surface is glare;
  an off-white at high but not maximum lightness reads better over a paragraph
- **Desaturate and lighten the brand colour** rather than reusing the light-mode value. A saturated
  mid-tone that looked right on white is usually too dim on a dark surface, and a saturated bright one
  vibrates against it
- **Re-check every pair.** Contrast in the dark set is a separate calculation; a pair that passes in
  light mode tells you nothing about its dark counterpart
- **Give the logo a variant or a plate.** Dark ink on transparency vanishes on a dark surface

Some clients honour a declared dark palette, some apply their own rules, and some force an inversion
regardless. The design consequence is that **the light palette also has to be legible after an
inversion it did not ask for** — which is what explicit background/foreground pairs on every band
buy. The client-by-client behaviour is in
[Accessibility](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/accessibility.md).

## Colour never carries meaning alone

A red price and a black price differ only for people who see the difference. A sale item needs the
word, a status needs its label, a required field needs more than a coloured border. This matters more
in transactional email than in campaigns, because a status colour without a status word is a support
ticket.

## Effects that do not survive

| Effect | What happens | Design instead |
|---|---|---|
| Semi-transparent colour over an image | Alpha support is inconsistent; the overlay may not appear | A solid band, or an image pre-composited with its overlay |
| Gradient backgrounds behind text | May render as a single flat colour, or not at all | Choose a solid that the text passes against, gradient as decoration |
| Coloured drop shadows for separation | Frequently dropped, leaving two adjacent blocks with no boundary | A `border` rule or a background change between bands |

## Related

- [CTA and Imagery](./cta-and-imagery.md) — where the reserved action colour gets used
- [Layout](./layout.md) — explicit backgrounds per band
