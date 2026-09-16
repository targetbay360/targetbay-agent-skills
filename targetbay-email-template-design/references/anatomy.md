# Template Anatomy

Which blocks a template needs, in what order, and how to keep a set of templates from drifting into
a set of unrelated designs.

What each message *says* and when it sends is in
[Marketing Emails](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/marketing-emails.md)
and [Ecommerce Flows](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/ecommerce-flows.md).
This is the shape it takes.

## The blocks

Each one has to earn its place. The default for a block nobody can justify is to remove it — every
block delays the call to action for someone.

Preheader, headline and body, primary call to action and footer are always present. The rest earn
their place:

| Block | Earns its place when | Cut it when |
|---|---|---|
| Header | The brand needs recognising before the content is read | It has grown into a navigation bar |
| Hero | One image or one statement carries the message | It is decoration pushing the message down |
| Product grid | The message is about specific products | It is filler, or a generic bestseller row unrelated to the reason for the message |
| Social proof | The reader is deciding whether to trust, not what to buy | It is a logo wall on a receipt |
| Secondary content | There is a genuine second action of lower value | It is competing with the primary action |

### Preheader

What to write is in
[Transactional Emails](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/transactional-emails.md#preheader).
The design consequence is that the preheader needs somewhere deliberate to live at the top of the
template — left without one it fills with whatever renders first, usually a "view in browser" link or
an image alt text.

### Header

A brand mark, at a size that is recognisable rather than dominant, and little else. A header carrying
a full category navigation is borrowing a pattern from the website where it makes sense — in an
email it takes the first screen, adds tap targets that compete with the call to action, and is a
block of links a filtering system has to evaluate.

Keep utility links — view in browser, account — visually quiet, or move them to the footer.

### Hero

Either one image, or one short statement, or both stacked. Not a collage.

The hero is where designs most often bury the point. Give it a maximum height that leaves room for the
headline and the call to action inside the first screen. If the hero is an image carrying the offer in
its pixels, the offer is also stated in text — see [CTA and Imagery](./cta-and-imagery.md).

### Body

One idea per block, with the most important first. Someone who stops reading after the first block
should still have the message. Supporting detail, terms and secondary reasons come after the primary
call to action, not before it.

### Product grid

Two columns, more rows. Each cell needs an image, a name and a price, and anything more crowds it at
the width the cell actually has after stacking. Keep cells uniform — a grid where one product has a
longer name and pushes its price out of line is the most visible sloppiness in ecommerce email.

The point of a grid is a choice, so keep it to a number someone would actually compare. Past that it
is a catalogue, and a catalogue is browsed on the site rather than in an inbox.

### Footer

Company name, physical address, unsubscribe and preference link are required — the legal detail is in
[Compliance](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/compliance.md).
Design consequences:

- The unsubscribe link is findable and readable at the body-text contrast target, not hidden in pale
  grey at the smallest size available. A recipient who cannot find it reports the message instead,
  and a complaint costs the sending reputation in a way an unsubscribe does not
- Footer links need tappable spacing, not a tight stack of small text
- Social icons are optional and often the least valuable tap in the message. If they stay, they are
  small and quiet

## Shapes by message type

Block order carries as much of the message as the copy does. These are starting shapes, not fixed
structures.

**Promotional campaign** — the block order is in
[Marketing Emails](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/marketing-emails.md#structure).
The design decision it leaves open: the call to action goes before the product grid, because the grid
is support, and repeats below it for anyone who scrolled.

**Cart recovery** — brief headline → the abandoned items, shown as products → primary call to action
→ reassurance (returns, delivery, support) → footer. The items are the message; a hero image above
them delays the one thing that will be recognised.

**Order confirmation** — the canonical order is in
[Transactional Emails](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/transactional-emails.md#content-structure),
and it opens with the brand mark because recognition is the anti-phishing control. Design
consequences: restrained and dense, as it is read for values rather than scanned; no dependence on
images, because the receipt is opened again months later; and marketing content, where it appears at
all, sits below everything transactional.

**Shipping notification** — status → tracking as the primary action → item summary → footer. The
tracking action is what the message exists for.

**Review request** — brief context and the product purchased → rating or review call to action →
footer. One product and one action. A request that shows four products and asks for four reviews gets
none.

**Win-back** — headline that acknowledges the gap → the offer or the reason to return → primary call
to action → a small product grid if it is relevant → footer. Short; a long message to a disengaged
recipient is a longer thing to ignore.

**Welcome** — brand statement → what to expect → primary call to action → any incentive → footer.

## Building a module library

Design the modules once, then assemble.

**Inventory.** A working set is roughly: header, hero, text block, image-and-text block, product grid
row, single-product block, call-to-action block, divider, testimonial or rating block, and footer.
Variants of those, not new blocks, cover most of what campaigns ask for.

**Interchangeability is a spacing decision.** Modules are reusable only if any two can sit adjacent
without adjustment. That means every module owns its own inner padding, shares the spacing scale in
[Layout](./layout.md), and never relies on the block above it for its spacing.

**Name by function, not appearance.** `hero-image-text`, not `blue-banner`. A module named for its
colour is a module that will not be reused after a rebrand.

**Variants, not forks.** A product grid with two columns and one with three are variants of one
module. A second grid built from scratch for one campaign is the beginning of a second template set.

**One template per message class, not per message.** Marketing and transactional usually justify
separate base templates — different density, different tone, different footers. A new base template is
warranted when the structure genuinely differs, not when the content does.

**The welcome message is the test.** It sets the design expectation for every message after it, so
if it cannot be assembled from standard blocks the library is not finished.

**Review the set periodically.** Modules nobody has used belong deleted; a variant assembled by hand
for a third time belongs in the library.

## Related

- [Layout](./layout.md) — the spacing scale and band structure modules are built on
- [CTA and Imagery](./cta-and-imagery.md) — the call-to-action block and the hero
