# Deliverability Principles

Why a message reaches the inbox, and which of the reasons a marketing programme can actually change.
[email-principles.md](email-principles.md) establishes that deliverability sits above everything
else; this document is the mechanism underneath that claim.

## Three layers, in diagnostic order

Deliverability failures come from three places, and they are not interchangeable. Diagnosing the
wrong layer is the most common and most expensive mistake in the discipline, because each layer's
remedy does nothing for the others.

| Layer | What it is | Who changes it | How fast it responds |
|---|---|---|---|
| **Identity** | Whether the receiving provider can verify the sender is who it claims to be, and that the verified identity matches the visible one | The store, in its own DNS | Immediately, once propagated |
| **Reputation** | What recipients have done with this sender's mail over recent history, accumulated per sending domain and per IP | The programme, through who it mails and how often | Weeks |
| **Content** | The message itself — wording, links, images, structure | The campaign | Per send |

The order matters. Content is the layer everyone reaches for first and the one that explains the
least. A sender whose identity does not verify is filtered regardless of what the message says, and
a sender with poor reputation is filtered regardless of how well the message is written.

## Identity is binary; treat it as a gate

Verification either aligns or it does not. There is no partial credit and no gradual improvement, so
it is a precondition rather than a lever — something to confirm before planning volume, not
something to optimise. Because the records live in the store's DNS rather than in the sending
platform, fixing them is a recommendation with a named owner outside the marketing programme.

Large mailbox providers have progressively made this mandatory rather than advisory, particularly
for senders above a meaningful daily volume. The consequence for planning is that a store crossing
into that volume band has an infrastructure dependency before it has a campaign.

The record syntax, the alignment rules and the provider requirements are operational detail rather
than theory. They are maintained in the standalone reference skill:
[targetbay-email-sms-best-practices](https://github.com/targetbay360/targetbay-agent-skills/tree/main/targetbay-email-sms-best-practices)
(`references/deliverability.md`, `references/sending-reliability.md`).

## Reputation is behavioural, and it is the only layer marketing owns

Providers infer wanted mail from what recipients do: opening, replying, moving out of spam, and —
far more heavily — complaining, ignoring, or deleting unread. The programme moves this by changing
who receives mail and how often, which is why a reputation problem is an audience and cadence
problem wearing a technical costume.

Three consequences that shape decisions elsewhere in this package:

- **Mailing unengaged contacts is not free.** The cost is paid by the contacts who do engage, whose
  mail is placed worse as a result. This is why suppression usually raises total revenue rather than
  lowering it.
- **Reputation is per sending domain.** Separating transactional from promotional sending onto
  different subdomains means a promotional misstep does not take order confirmations down with it.
  It also means each domain must earn its reputation independently.
- **Reputation decays towards neutral during silence and falls fast during a bad run.** It is
  asymmetric: months to build, days to lose. A single large send to a stale population can undo a
  quarter of careful sending.

## What warm-up is actually doing

Ramping volume on a new domain or IP is not a formality. A receiving provider has no history for an
unknown sender, so it judges on the only thing available: whether the first cohorts of recipients
behave like people who wanted the mail. Warm-up exists to make sure the earliest and most heavily
weighted evidence comes from the most engaged part of the list.

That reframes it as a constraint on planning rather than a configuration step. During a ramp the
audience is chosen by engagement rather than by campaign objective, and the ceiling on volume is a
dependency every plan in that window inherits. The same logic applies after a long dormant period,
which a provider reads much like a new sender.

## Placement is not observable from sending data

This is the limit that most often gets ignored. Delivery means the receiving server accepted the
message; it says nothing about which folder it landed in. Opens and clicks come only from recipients
who found the mail, so they under-report a spam-foldered send rather than revealing it.

True placement requires evidence from inside receiving mailboxes — seed accounts or a provider feed.
Without one, the honest position is that placement is unknown, and the available proxies are
movements in engagement, bounce and complaint rates **segmented by receiving domain**. A sharp
engagement drop at one provider while others hold steady is the closest thing to a placement signal
that sending data contains, and it is still an inference.

## Bounces and complaints say different things

Both are reputation inputs and they are routinely conflated.

- A **permanent failure** is an address problem: the mailbox does not exist. Concentrated permanent
  failures point at acquisition — a form without validation, a purchased or inherited list, a typo
  path — and fixing the source matters more than suppressing the results, because the results
  regenerate.
- A **temporary failure** is a condition at the receiving end that may clear. Treating a single one
  as permanent discards deliverable customers; treating a repeated one as temporary keeps mailing a
  dead address. Where the boundary sits is derived from the store's own pattern.
- A **complaint** is the most expensive signal available, because it is an explicit statement that
  the recipient did not want this. Its levers are cadence and relevance, never wording.

## Rendering and accessibility are deliverability-adjacent, not deliverability

A message that arrives but cannot be read fails for the same commercial reason, and the two are
often diagnosed together, but the mechanisms are unrelated: an unreadable message is a design
failure, not a reputation one. Images-off rendering, dark mode, contrast and alternative text are
covered by
[targetbay-email-template-design](https://github.com/targetbay360/targetbay-agent-skills/tree/main/targetbay-email-template-design)
(`references/design-qa.md`, `references/colour-and-dark-mode.md`) and the accessibility rules in
[targetbay-email-sms-best-practices](https://github.com/targetbay360/targetbay-agent-skills/tree/main/targetbay-email-sms-best-practices)
(`references/accessibility.md`). Keep the diagnoses separate even when the remedies ship together.

## What the platform owns

Classification of bounces, complaint feedback processing, suppression enforcement and legal opt-out
handling are platform responsibilities, not agent ones — see
[../rules/global-rules.md#G10](../rules/global-rules.md). The decisions that remain are which
population is mailed, at what cadence, from which domain, and whether sending should continue at
all. Those are the ones these skills make.
