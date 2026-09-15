# Transactional Email Best Practices

The message someone is waiting for. It has the highest engagement of anything you send and the
lowest tolerance for cleverness.

## Core principles

1. **Clarity over creativity.** The recipient wants one fact or one action. Give it to them above
   the fold.
2. **Action-oriented.** One primary action, stated once, as a button and as a plain URL.
3. **Time-sensitive.** These arrive in seconds, not minutes. A password reset that takes five
   minutes generates a support ticket and a second reset request.
4. **Unmistakably you.** Recognition is what stops an OTP mail being mistaken for phishing.

## Subject lines

State what happened or what to do. No curiosity gap, no emoji, no brand voice exercise.

| Good | Bad | Why |
|---|---|---|
| `Your Acme order #10482 is confirmed` | `Thanks for shopping with us!` | The order number is what they search for later |
| `Reset your Acme password` | `Action required` | "Action required" is what phishing says |
| `Your verification code is 483920` | `Welcome aboard 🎉` | The code in the subject means no need to open |
| `Order #10482 shipped — arriving Thursday` | `Good news inside` | Both facts, no open needed |

Putting the code or order number in the subject is a feature, not a leak of the payoff. The goal is
the recipient getting what they need, not an open.

## Preheader

The preheader is part of the subject line, not decoration. It is the second line of the inbox
preview and it is read.

- Continue the subject, do not repeat it
- Never leave it to default to "View this email in your browser" or the first alt text
- Put a hidden preheader block at the top of the body so clients pick the right text

```html
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">
  Arriving Thursday 14 March. Track it any time from your account.
</div>
```

## Content structure

Top to bottom:

1. **Logo or brand name** — recognition first
2. **The fact or the action** — one sentence
3. **The detail** — order contents, code, what changed
4. **The primary button** — one, with the plain URL beneath it
5. **What to do if this was not you** — for anything security-related
6. **Support contact**
7. **Footer** — company name, address, no unsubscribe link

Anything below the first screen should be detail, not the point.

## Mobile first

Most of these are read on a phone, often in a notification preview.

- Single column. A two-column receipt reflows badly and hides the total.
- Body text 16px minimum, and do not go below 14px anywhere.
- Buttons at least 44×44px with real padding, not a styled inline link.
- Assume images are blocked. A message that is one exported image is a message that fails for a
  meaningful share of recipients, fails for screen readers, and looks like spam to filters.
- Test in dark mode — see [Accessibility](./accessibility.md).

## Sender configuration

- **From name:** the brand, consistently. `Acme` beats `Acme Notifications` beats `noreply`.
- **From address:** a real mailbox on the transactional subdomain. `noreply@` trains people that
  replying is useless, and some of them reply anyway — route it to support instead of a void.
- **Reply-To:** somewhere a human reads.
- Keep the From name stable across every transactional message. Changing it per message type breaks
  the recognition that is doing the work.

## Codes and links

**Verification codes:**
- Long enough to resist guessing, short enough to retype — six digits is the common balance
- Displayed large, in a monospace face, with generous letter spacing
- Never split across lines, and not inside an image
- State the expiry in the message, in minutes
- Include the code in the subject line where the use case allows

**Action links:**
- A button, plus the full URL in plain text beneath it for clients that strip buttons
- Single use, short expiry, invalidated once used
- Same domain as the brand — a link to an unfamiliar tracking domain in a password reset reads as an
  attack, and some security tools will strip it
- Do not wrap security links in click tracking. Prefetching by security scanners will consume them
  before the human clicks.

That last point causes a specific, hard-to-debug bug: a corporate mail scanner follows every link in
the message, the single-use reset token is consumed, and the user sees "this link has expired" on
their first click. Exempt security links from tracking, and make consumption happen on the form
submit rather than on the page load.

## Letting the user ask again

Verification and reset messages need a way to request another one.

- Enforce a cooldown before a second request — around 60 seconds
- Cap attempts per hour per address
- Invalidate the previous code when a new one is issued, so two live codes never exist
- Say plainly what happened: "A new code is on its way. The previous one no longer works."

Phrase the control as **"Send again"** or **"Send a new code"**.

## Failure handling

The message that reports a failure needs more care than the one that reports success.

- Say what failed, in the recipient's terms: "We could not charge the card ending 4242."
- Say what happens next, with the date: "We will try again on 18 March."
- Say what they can do, with one link straight to the fix
- Do not make them log in to find out what went wrong

## Related

- [Transactional Email Catalog](./transactional-email-catalog.md) — which messages to build
- [Email Types](./email-types.md) — where the transactional boundary sits
- [Sending Reliability](./sending-reliability.md) — making sure it actually goes once
- [Accessibility](./accessibility.md) — structure, contrast, dark mode
