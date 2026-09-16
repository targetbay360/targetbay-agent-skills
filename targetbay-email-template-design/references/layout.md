# Email Layout

The grid every other decision sits on. Get width, column count and spacing settled before any
visual work, because changing them later re-breaks every block.

## Width

**600px is a convention, not a rule** — the whole tooling ecosystem assumes it, and the value of
following it is compatibility with everything else rather than the number itself.
[Marketing Emails](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/marketing-emails.md)
sets 600px as the maximum; treat that as the working ceiling.

- A narrower template is fine, and often better for a short transactional message, where a narrow
  column reads as deliberate rather than cramped
- Below the template width the design is fluid: the message occupies the full screen width minus its
  gutter
- Going wider needs a reason that survives being said out loud — a product grid that genuinely needs
  the room — and it needs checking in a desktop preview pane, which is where a wide template clips

## One column by default

A single column stacks predictably, reorders cheaply, and renders the same everywhere. Multi-column
layouts have to be built to collapse, and in the clients that ignore the collapse they render as a
row of squeezed columns instead.

Multi-column earns its place in two situations:

| Layout | Use for | Requirement |
|---|---|---|
| Two equal columns | A product pair, two categories, before/after | Must stack to full width on narrow screens |
| Image beside text | A single feature block on desktop | Must stack, with a decided order — see below |

Everything else — hero, headline, body, call to action, footer — is one column.

**Three or more columns across a 600px canvas gives each column under 200px.** A product image, its
name and a price in 180px is a thumbnail with a caption. Use two columns and more rows.

## Stacking order is source order

When columns collapse on a narrow screen, most clients stack them in the order they appear in the
markup, left to right. A design where the image sits right of the text on desktop will stack with the
text first on mobile unless the template is built to reverse it, and the clients that ignore the
reversal will show it the other way round.

Design so that the source order reads correctly in both arrangements. An alternating
image-left/image-right rhythm down a desktop page becomes an inconsistent mobile stack, which is
usually worse than the visual monotony it was avoiding.

## Spacing

Use one spacing scale everywhere, in multiples of 4 with 8 as the working step. Arbitrary values are
what makes two blocks by two designers refuse to sit together.

| Tier | Typical value | Used for |
|---|---|---|
| Tight | 4–8px | Inside a component — label to value, icon to text |
| Component | 12–16px | Between elements of one block — headline to body, body to button |
| Block | 24–32px | Between blocks inside a section |
| Section | 40–48px | Between major sections — hero to body, body to footer |

Three vertical tiers — component, block, section — are enough to express hierarchy; Tight is
intra-component and does not count against them. A design reaching for a fourth is carrying hierarchy
with spacing alone when type size or a divider should carry it.

**Denser is not shorter.** Reducing every gap to fit more in does not make a message quicker to read;
it removes the grouping that lets someone skip what they do not want. The scale above is a comfortable
default. A dense variant (8/12/16/24) suits a receipt or an order summary, where the reader is
scanning for one value; an airy variant (16/24/32/64) suits a single-offer campaign.

## Gutters

Never let text touch the edge of the message. A minimum 16px inner gutter on the left and right,
24px on wider layouts. This is more visible on a phone, where the message is already at the screen
edge, than in a desktop preview pane where the surrounding background hides the problem.

## Blocks are full-width bands

Build a template as a vertical stack of full-width bands, each with its own background colour and its
own inner padding. Because:

- Bands can be reordered, duplicated or dropped without touching anything else — the requirement for
  a reusable module set
- Every band's background is explicit, which is what stops dark mode producing a bright rectangle
  where an implicit white showed through
- A band that is unsupported in some client degrades to a plain full-width block rather than
  breaking the blocks around it

Avoid overlapping elements, negative offsets and elements that bleed outside their band. They depend
on positioning support that is inconsistent across clients, and the failure mode is an overlap the
recipient sees rather than a graceful fallback.

## What the first screen has to carry

Assume the first screen is all that is read. On a phone that is roughly the height of the header plus
one block. It needs to answer what this message is and what it wants, which usually means: brand
mark, the offer or the point stated in words, and the primary call to action.

A hero image tall enough to fill that screen on its own pushes the message below it. Design the hero
as a band with a decided maximum height rather than a proportion of the screen, and put words in the
message rather than only in the image — see
[CTA and Imagery](./cta-and-imagery.md).

## Tap targets

Anything tappable needs a 44×44px minimum touch area (WCAG 2.1 SC 2.5.5, and the same figure in
Apple's interface guidelines), with clear space around it so neighbouring targets are not mis-tapped.
The figure is also in
[Accessibility](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/accessibility.md).
Two consequences that designs routinely miss:

- A text link in a paragraph is not a tap target. Fine for a secondary link, not for the action the
  message exists to get
- Stacked footer links set at a small size with tight line height are a mis-tap generator. Give
  footer links either real vertical padding or a separator that makes each one its own row

## Layout choices that break in real clients

| Choice | What goes wrong | Design instead |
|---|---|---|
| Background image behind text | Dropped in Outlook desktop; the text lands on whatever is beneath | A solid background colour that works alone, image as enhancement |
| Fixed-height blocks | Text at a larger system size overflows or clips | Let blocks grow with their content |
| Full-bleed edge-to-edge text | Unreadable on a phone, touches the screen edge | Inner gutter, always |
| Rounded corners and shadows on structure | Inconsistent support; a square block appears in some clients | Use them decoratively where a square fallback is acceptable |
| Precise absolute alignment between bands | Padding is rendered slightly differently per client | Align to the spacing scale, not to pixel coincidences |

## Related

- [Typography](./typography.md) — type scale and measure, which set the comfortable column width
- [Colour and Dark Mode](./colour-and-dark-mode.md) — why every band needs an explicit background
