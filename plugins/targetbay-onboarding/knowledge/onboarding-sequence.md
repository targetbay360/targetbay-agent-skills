# Onboarding Sequence

Why the order of onboarding work decides its outcome, independently of what gets built.

## Order is the decision

Given the same store and the same three products, two operators will usually agree on roughly what should
exist and disagree on what happens first. The disagreement matters more than the agreement, because all
three products compete for the same scarce resource and one kind of configuration loses value permanently
when it is delayed.

## Capture is not retroactive

Some configuration captures data. A review trigger records that an order was delivered and asks about it.
Onsite tracking records what a visitor looked at. Event instrumentation records what happened.

Configuration of this kind has an asymmetry nothing else in onboarding has: **delaying it destroys value
that cannot be recovered.** A review trigger armed on day sixty cannot ask about a day-ten order. The
order happened, the customer had an experience, and the moment to ask has passed. By contrast a win-back
campaign built on day sixty works exactly as well as one built on day one — better, in fact, because it
has more evidence behind it.

This is why capture-shaped work sequences early even when its payoff is later, and consumption-shaped
work sequences late even when its payoff feels more immediate.

## The contact budget is the scarce resource

All three products send messages. Each has its own sensible limits, and a customer receives the sum of
all three. Nothing inside any one product can see this, which is why it is settled at onboarding and
written down in [../rules/contact-ownership-rules.md](../rules/contact-ownership-rules.md).

The onsite work is the exception, and the exception is structural rather than lucky: it acts on a visitor
who is already on the site and already chose to be there. It spends none of the budget. That single
property is why it can proceed while everything else is still being argued about.

## Why evidence-hungry decisions go last

Some decisions are impossible to make well without history, and building them early does not make them
arrive sooner — it makes them arrive wrong:

- **Loyalty tier thresholds** need a value distribution and a repeat rate. On a store with three orders
  there is no distribution to break at, and a tier boundary picked anyway will sit in the wrong place for
  as long as the programme runs.
- **Replenishment intervals** need observed reorder behaviour per product. A category default fires at
  the wrong time for almost every product it covers.
- **Win-back timing** needs a lapse point, which needs enough second purchases to know what lapsed means
  for this store.

Sequencing these late is not deferral. It is the difference between a derived programme and an invented
one, and the review point is what turns the wait into a plan rather than a gap.

## What a good sequence looks like

Not a fixed list — the store's data decides — but the shape is usually:

1. **Capture and no-cost surfaces.** Onsite placements and search, tracking, review triggers armed.
   Nothing spends contact budget; nothing waits on evidence that does not exist.
2. **The lifecycle baseline.** Welcome, post-purchase, abandonment — the moments that exist for every
   store and need no threshold to be correct. Consent and deliverability posture gate this, not the
   calendar.
3. **The evidence-dependent layer.** Replenishment, win-back, second-purchase timing, loyalty structure —
   each gated on the observation that makes it derivable.

Each step carries the reason it sits where it does, so a later operator can reverse the decision on
evidence rather than on taste.

## Reading this alongside

- [../rules/sequencing-rules.md](../rules/sequencing-rules.md) — the enforceable form of this document
- [evidence-and-provenance.md](evidence-and-provenance.md) — what "gated on an observation" means in
  practice
