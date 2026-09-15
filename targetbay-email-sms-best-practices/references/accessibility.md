# Email Accessibility

Most ecommerce email fails basic accessibility checks. The fixes are small, they are in the template
rather than in every campaign, and several of them also improve deliverability — an image-only
message fails for screen readers, for people with images off, and for spam filters, all at once.

Severity labels below indicate how much the failure costs the recipient.

## Rules

### Set `lang` and `dir` (Serious)

Without a language, a screen reader announces the text using the listener's default voice and
pronunciation. English read with a Japanese phoneme set is unintelligible.

```html
<html lang="en" dir="ltr">
```

Set it on any element whose content is in a different language:

```html
<p lang="fr">Livraison gratuite</p>
```

For right-to-left languages set `dir="rtl"`, and set it on the direct children of `<body>` too —
some clients strip attributes from `<html>`.

### Mark layout tables as presentational (Serious)

Email layout still uses tables. A screen reader announces an unmarked table as a data table:
"table, 4 columns, 12 rows", then reads cell coordinates. For a layout grid that is pure noise.

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0">
```

Every layout table, including nested ones. A real data table — an order summary with item, quantity
and price — keeps its semantics and gains `<th scope="col">` headers.

### One `<h1>`, headings nested in order (Mild)

Screen reader users navigate by heading. A message with no headings is one undifferentiated block
they have to listen to linearly.

- One `<h1>`: the message's actual subject
- `<h2>` for sections, `<h3>` beneath those — never skip a level to get a smaller font
- Size comes from CSS, structure comes from the tag

### Every link needs discernible text (Serious)

A linked image with no alt text is announced as its URL, or as "link" with nothing else. A
bulletproof button built from a table needs the text inside the anchor, not beside it.

```html
<!-- Bad: nothing to announce -->
<a href="https://example.com/sale"><img src="sale.png"></a>

<!-- Good -->
<a href="https://example.com/sale"><img src="sale.png" alt="Shop the spring sale"></a>
```

### Link text must describe the destination (Moderate)

Screen reader users can pull up a list of every link in the message, out of context. A list of nine
entries all reading "click here" is useless.

| Bad | Good |
|---|---|
| Click here | Track your order |
| Read more | Read the full care guide |
| Learn more | See the size chart |
| https://example.com/orders/10482 | View order #10482 |

Never use a bare URL as link text — it is read character by character in some configurations.

### Meaningful alt text, and `alt=""` for decorative images (Critical)

```html
<!-- Product image: describe what it shows -->
<img src="boot.jpg" alt="Tan leather ankle boot, side view">

<!-- Logo: the brand name is the content -->
<img src="logo.png" alt="Acme">

<!-- Decorative divider: explicitly empty, so it is skipped -->
<img src="divider.png" alt="">
```

- Empty `alt=""` is not the same as a missing `alt`. Missing means the reader falls back to the
  filename; empty means "skip this".
- Do not start with "Image of" — the reader already says that.
- If the image contains text, the alt text carries that text.
- Style the alt text (colour, size, weight) so a blocked image still reads as part of the design
  rather than as broken system text.

### Include a `<title>` (Serious)

```html
<title>Your order #10482 has shipped</title>
```

Used by the browser view of the message and by some assistive technology as the document name.
Without it the tab and the announcement read as the URL.

### 4.5:1 contrast, then check dark mode (Serious)

- Body text: 4.5:1 minimum against its background
- Large text (18pt+, or 14pt bold): 3:1
- Buttons: the label against the button colour, not against the page
- Light grey on white — the default "secondary text" of most designs — usually fails

## Dark mode

Clients handle dark mode three different ways, and the differences break templates that look fine in
one of them.

| Client behaviour | What happens |
|---|---|
| No change | Your light design renders as designed |
| Colour swap by rule | Backgrounds and text colours are inverted, sometimes selectively |
| Full forced inversion | Everything flips, including things you set explicitly |

What breaks, and what to do:

- **Transparent-background PNG logos in dark ink become invisible.** Give the logo a light background
  plate, or supply a version with a visible outline.
- **Text set to `#000000` on an implicit white background** — the background inverts, the text does
  not, and it disappears. Always set both the text colour and its background explicitly, on the same
  element.
- **Hard-coded white boxes** become bright rectangles in an otherwise dark message.
- **Images of text** cannot adapt at all. Another reason not to ship a message as one image.
- Test in Apple Mail, Outlook and Gmail's mobile app in dark mode — they behave differently from
  each other.

Where it matters, use `@media (prefers-color-scheme: dark)` for the clients that honour it, and make
sure the non-honouring fallback is still legible.

## Priority order

If you fix these in one pass, this is the order by cost to the recipient:

1. Alt text on every image — a blocked or unseen product image with no alt is a blank message
2. `role="presentation"` on layout tables
3. `lang` on `<html>`
4. Discernible, descriptive link text
5. `<title>`
6. Contrast, checked in both modes
7. Heading structure

## Authoring checklist

- [ ] `lang` and `dir` on `<html>`
- [ ] `<title>` describing the message
- [ ] Every layout table `role="presentation"`
- [ ] One `<h1>`, headings in order
- [ ] Every image has `alt`, decorative ones `alt=""`
- [ ] Every link has discernible text that describes the destination
- [ ] Text and background colours both set explicitly
- [ ] 4.5:1 contrast on body text
- [ ] Readable with images blocked
- [ ] Readable in dark mode
- [ ] Single column, 16px body text, 44px tap targets

## Testing

- Turn images off and read the message. If it no longer makes sense, the alt text is wrong.
- Read it with a screen reader — VoiceOver on macOS and iOS, NVDA on Windows. Listening to one of
  your own campaigns is the fastest way to understand why these rules exist.
- Check contrast with any WCAG contrast tool before the design is signed off, not after.
- View at 200% zoom.
- Render in dark mode in at least three clients.

## Related

- [Transactional Emails](./transactional-emails.md) — structure and mobile-first layout
- [Marketing Emails](./marketing-emails.md) — the same rules apply to campaigns
- [Deliverability](./deliverability.md) — image-only messages are also a filtering risk
