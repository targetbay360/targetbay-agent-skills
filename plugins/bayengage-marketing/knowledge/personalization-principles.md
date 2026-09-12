# Personalisation Principles

Personalisation works because relevance works. It fails when it is decoration, and it fails badly when it
is wrong.

The binding constraints are in
[../rules/personalization-rules.md](../rules/personalization-rules.md). This document is the reasoning
behind them.

## A hierarchy of value

Not all personalisation is equal. Roughly, in descending order of impact:

1. **Sending the right thing** — the product, category or offer this person would plausibly want
2. **Sending at the right time** — their replenishment interval, their decision window, their engagement hour
3. **Sending for the right reason** — a message whose premise matches their actual state
4. **Showing the right details** — recommendations, past purchases, saved items
5. **Using their name**

Most personalisation effort goes into the last item and most of the value sits in the first three.

## Timing is personalisation

A generic reminder at the moment someone runs out beats a beautifully personalised message sent
arbitrarily. Timing is frequently the cheapest and largest available improvement, and it requires no
content work at all.

## The asymmetry of errors

Correct personalisation produces a modest lift. Incorrect personalisation produces an outsized negative
reaction — the recipient now knows the store is guessing. This asymmetry is the entire justification for
[../rules/personalization-rules.md#P1](../rules/personalization-rules.md): only verified data.

Broken personalisation is worse than none:

- A missing value rendered literally
- A recommendation for something just purchased
- A "we miss you" message to someone who ordered last week
- A reference to a product that is out of stock or discontinued

## Creepiness is a real constraint

There is a line between *useful* and *surveillant*, and it sits closer than the data permits.
Referencing a purchase is normal. Narrating browsing behaviour in detail is not. Inferring life events
from purchase patterns is not. The line is about what the recipient expects the store to know.

## Personalisation depth follows data depth

A store with thin behavioural data should send simpler, more honest messages — not fabricated
specificity. Degrading gracefully means fewer personalised elements, not invented ones.

## Segmentation or personalisation?

- Different **strategy** — different offer, channel, timing, objective → segment
- Same strategy, different **details** → personalise inside one send

Choosing segmentation where personalisation was needed produces segment sprawl. See
[segmentation-principles.md](segmentation-principles.md).

## Every personalised element needs an empty state

If a value can be missing, the message must read correctly without it. This is testable before send and
should be stated in the plan.
