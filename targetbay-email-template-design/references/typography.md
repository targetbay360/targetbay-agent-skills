# Email Typography

Type is where web design habits fail most often in email, because the font chosen in the mockup is
frequently not the font the recipient sees.

## Web fonts are an enhancement, never the design

Apple Mail and several mobile clients honour a downloaded web font. Gmail and Outlook on Windows
strip it and serve the fallback. Support shifts, so confirm it in a render test rather than trusting
a list — but design as though a large share of the list sees the fallback, because it does.

**Design in the fallback font first, then add the web font as an improvement.** A design signed off
in a mockup showing the brand typeface, where nobody has looked at the fallback, is a design that has
not been reviewed for most of its audience.

Choose the fallback for its *metrics*, not its personality. A narrow brand typeface with a wide
fallback reflows every headline — lines wrap that did not, a two-line headline becomes three, and the
block that was sized for it overflows. Match x-height and width before matching mood.

## Fonts that render without downloading

These are installed widely enough to be relied on. Group by the job, then pick one per role.

| Personality | Stack | Notes |
|---|---|---|
| Neutral sans | Arial, Helvetica, sans-serif | The default. Renders everywhere, says nothing |
| Wide, legible sans | Verdana, Geneva, sans-serif | Larger x-height; good for small text, wide at headline sizes |
| Compact sans | Tahoma, Segoe UI, sans-serif | Narrower than Arial; useful when a headline must fit |
| Humanist sans | Trebuchet MS, Lucida Grande, sans-serif | More character than Arial, still safe |
| Serif | Georgia, Times New Roman, serif | Georgia holds up at small sizes; Times does not |
| Monospace | Courier New, Consolas, monospace | Order numbers, codes, anything read character by character |

A system stack (the client's own interface font, with Arial or Helvetica behind it) is also a
reasonable default. It renders natively everywhere and reads as unremarkable, which for a receipt is
the right answer.

**Two typefaces is the ceiling.** One for headings, one for body, and often the same one for both at
different weights and sizes. A third is a thing to maintain, not a thing to gain.

## Sizes

A consistent scale, roughly: 12, 14, 16, 18, 24, 32. Assign roles, do not pick per block.

| Role | Size | Notes |
|---|---|---|
| Hero headline | 28–32px | On a phone this wraps to two or three lines. Write it to survive that |
| Section heading | 20–24px | |
| Sub-heading, product name | 18px | |
| Body | 16px | The floor for anything meant to be read in full |
| Supporting, captions, labels | 14px | |
| Legal, footer, address | 14px | [Transactional Emails](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/transactional-emails.md) sets 14px as the floor anywhere in a message |

Some mobile clients enlarge very small text automatically, which reflows the block it sits in. Setting
a sensible minimum avoids both the readability problem and the reflow.

Sizes do not scale down for mobile. 16px body on a phone is 16px body on a desktop; the column is what
changes. Headlines are the exception — a 32px hero headline often needs to come down to 24–28px on a
narrow screen so it does not take four lines.

## Line height, measure and alignment

- **Line height** 1.4–1.6 for body, 1.2–1.3 for headlines. Tight body line height is what makes a
  message read as heavy even when its length is fine
- **Measure** 45–75 characters per line. At 600px with 16px body this lands in range naturally, which
  is one of the quiet reasons the 600px convention works. Widening the column without increasing type
  size pushes it past comfortable
- **Left-align body text.** Centre only short blocks — a headline of a line or two, a call to action,
  a footer address. Centred paragraphs force the eye to hunt for each line start
- **Never justify.** Email clients do not hyphenate, so justified text opens rivers of white space,
  and it is worse in the narrow column after stacking

## Weight and emphasis

Build hierarchy from size and spacing first, weight second, colour last. Colour-only hierarchy fails
in dark mode and for anyone with low vision.

Most widely installed fonts ship only regular and bold — there is no 500 or 600 to fall back on. A
hierarchy designed around three weights collapses to two, and the middle level disappears. Design the
hierarchy so it still reads with regular and bold alone, then let a web font add the intermediate
weight where it is available.

- **Bold** for emphasis, sparingly. A paragraph with four bold phrases has no emphasis
- **Avoid italics for anything important** — they render poorly at small sizes in several clients
- **All caps only for short labels**, such as a badge or an eyebrow above a headline. In a sentence it
  slows reading, and some screen readers announce longer capitalised strings letter by letter
- **Avoid tight letter-spacing on body text.** It is a display effect; at 16px it costs legibility for
  no gain

## Numbers, prices and tables

Order summaries and price lists are read by column, not by line. Right-align numeric columns so digits
stack, and keep the font consistent down a column so the alignment holds. Where a font offers
proportional figures of varying width, a monospace stack for the numeric column is a reasonable trade
— an order total that shifts position between rows reads as sloppy on the one message where trust
matters most.

## Two things that look like type problems and are not

- **Text set as an image.** It cannot be resized, selected, translated or read by a screen reader, it
  disappears with images off, and it is a filtering risk. See
  [CTA and Imagery](./cta-and-imagery.md) and
  [Accessibility](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/accessibility.md)
- **Long words in other languages.** German compounds, long product SKUs and URLs overflow a narrow
  column that Latin-script English fitted. If the list is multilingual, review the narrow width with
  the longest locale, not the shortest

## Related

- [Layout](./layout.md) — the column width the measure depends on
- [Colour and Dark Mode](./colour-and-dark-mode.md) — text colour and contrast
