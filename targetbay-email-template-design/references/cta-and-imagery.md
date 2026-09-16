# Calls to Action and Imagery

The two design decisions that most directly change whether a message does anything.

## One primary action

A message has one thing it wants, and
[Marketing Emails](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/marketing-emails.md#structure)
already sets the rule: one primary call to action, because the choice itself is friction. What
follows is how that gets designed.

- **One primary call to action**, repeated at most once further down for anyone who scrolled. The
  repeat is the same label and the same destination — a second, different button is a second action
- **Secondary actions are visually subordinate**: a text link, or an outlined button against the
  primary's solid fill. If a secondary action needs the same weight as the primary, the message is
  carrying two purposes and should be two messages
- **Navigation rows are actions too.** A header with six category links is six competing actions
  above the one that matters

## Designing the button

| Property | Guidance |
|---|---|
| Size | At least 44px tall, with real horizontal padding |
| Width | Full-width on narrow screens, contained on desktop |
| Label | 16px or larger, regular or bold weight — smaller reads as a caption, not a control |
| Fill | The reserved `primary` colour, solid — see [Colour and Dark Mode](./colour-and-dark-mode.md) |
| Shape | One radius across every template; a different radius per campaign reads as a different brand |
| Clear space | At least 16px above and below, more after a dense block |

Contrast is checked on the label against the fill, not the button against the page — the common
failure is a light label on a mid-tone brand fill. The target is in
[Accessibility](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/accessibility.md).

**Build the button from a background colour and text, not from an image.** An image button disappears
with images off, cannot be resized, and takes the message with it when it is the only action.

Where a client does not render a styled background, the fallback is a plain, obviously clickable
text link — not an invisible one.

### Labels

The label says what happens, in the recipient's terms. "Shop the sale", "Track your order", "Leave a
review". "Click here" and "Submit" describe the mechanism rather than the outcome, and both are
unusable out of context for anyone reading with a screen reader — the discernible-link-text rule in
[Accessibility](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/accessibility.md).

Keep labels to a few words. A label that wraps to two lines inside the button was written for a
desktop mockup.

### Placement

The primary call to action is inside the first screen wherever the message is short enough to allow
it, which on a phone means roughly: header, one block, button. A message that needs supporting
content before the action can reasonably be asked for still repeats the button above the fold when
the action is the point, and places the explanation below.

Never place the only call to action below the footer boundary, and never rely on a sticky element —
nothing sticks in email.

## Imagery

### Design for images off

Images may be blocked, slow, or simply not loaded before the message is judged.
[Accessibility](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/accessibility.md)
gives the test: remove every image and read the message. Alt text is the remedy when a single image
has lost its meaning — but **when the message as a whole stops making sense, the design is what needs
changing, and no alt text fixes it.**

What that rules out:

- **The single-image email.** One exported design as the whole message is blank when blocked,
  unreadable by a screen reader, untranslatable, and a filtering risk
- **The offer stated only in the hero image.** "30% off" rendered in pixels is 30% off that some of
  the list never sees. State it in text as well
- **Image-based buttons and image-based headlines.** Both belong as text

Alt text is the fallback, not the fix. It is covered in
[Accessibility](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/accessibility.md);
the design consequence is that a block should be laid out so that its alt text lands in a sensible
place and the block does not collapse to nothing when the image is gone.

### Practical image rules

- **Export at twice the display width** so the image is sharp on high-density screens, then keep the
  displayed dimensions fixed
- **Keep file sizes small.** Total message weight affects both load time on a phone and the point at
  which some clients truncate a long message. Compress before adding, not after complaints
- **Declare display dimensions** so the layout does not jump or collapse while images load, or when
  they are blocked
- **Do not put text inside images** — see [Typography](./typography.md)
- **Give transparent logos a background plate** or a light-ink variant, or they vanish on a dark
  surface
- **Crop for the narrow width.** A wide hero cropped to a 600px column, then shown at phone width,
  can lose the subject entirely. Check the crop at the narrowest width, not the widest
- **Uniform aspect ratios in a grid.** Mixed ratios in adjacent cells are the most visible
  inconsistency in a product row

### Animation

An animated GIF is not supported everywhere; some clients show only the first frame. So the **first
frame has to work as a still image**, which means it carries the message and the offer rather than
being the empty state before the reveal. Keep animation short, avoid flashing, and treat it as
decoration — never as the only place information appears.

## Related

- [Anatomy](./anatomy.md) — where the call-to-action block and hero sit in the order
- [Colour and Dark Mode](./colour-and-dark-mode.md) — the reserved action colour and its label pairing
