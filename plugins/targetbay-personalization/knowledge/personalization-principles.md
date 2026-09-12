# Personalization Principles

Durable reasoning about why onsite personalization does and does not work. Skills cite this for *why*; the
decisions live in skills, and the constraints in [../rules/](../rules/README.md).

## Most traffic is anonymous, and that is the design problem

A store's identified visitors are a minority, and usually its best customers — which means an experience
designed for them is designed for the people who needed the least help. The interesting question is what an
anonymous visitor sees, and the answer has to come from session behaviour rather than history
([../rules/targeting-rules.md#T2](../rules/targeting-rules.md)).

## Session intent beats historical profile more often than expected

What someone is doing right now — the query that brought them, the category they are moving through, what
is in the cart — predicts the next few minutes better than a sparse behavioural history. It also requires
far less of the visitor, which matters once consent is a precondition rather than an assumption.

## Personalization mostly redistributes attention

A recommendation carousel does not create demand; it changes which product absorbs it. That is frequently
worth doing — moving demand toward higher-margin, in-stock or better-converting products is real value —
but it is not the same as incremental revenue, and the two are reported as if they were interchangeable
more often than not ([../rules/measurement-rules.md#M3](../rules/measurement-rules.md)).

## The failure modes are more visible than the successes

A good recommendation is barely noticed. A bad one — the product already in the cart, the item bought last
week, the out-of-stock hero — is noticed immediately and costs credibility across the whole experience.
This asymmetry is why exclusions are designed first
([../rules/surface-rules.md#U4](../rules/surface-rules.md)) and why the empty state is part of the design
([#U6](../rules/surface-rules.md)).

## Attention is the budget, not screen space

Every element added to a page is taken from what the page was already doing. Pages accumulate widgets
because each was added against an empty-space argument rather than an attention-cost argument, and the
result converts worse than the simpler page it replaced
([../rules/global-rules.md#G7](../rules/global-rules.md)).

## Search is the highest-intent surface and the least attended to

A visitor who types a query has stated exactly what they want. Zero-result and low-conversion queries are
therefore the clearest, cheapest signal a store has about what its catalogue, synonyms or merchandising is
missing — and they are usually unread.

## Novelty inflates the first reading

A new element attracts attention because it is new. Effects measured in the first period overstate the
durable effect, which is why the horizon matters and why a favourable early result is not a result
([../rules/measurement-rules.md#M8](../rules/measurement-rules.md)).

## Complexity moves the failure into the model

A rules-based experience fails visibly and is fixable. A model-driven one fails quietly and is not, and
the store cannot explain to a customer why they were shown what they were shown. Where a simpler mechanism
produces a comparable result, the simpler one is also the one that can be debugged at the point it
misbehaves ([../rules/global-rules.md#G9](../rules/global-rules.md)).
