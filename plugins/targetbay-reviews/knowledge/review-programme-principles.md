# Review Programme Principles

How a review programme behaves over time, and what that implies for planning.

## A programme is a rate, not a campaign

Reviews arrive as a function of orders, request coverage and submission rate. That makes the programme a
throughput problem: a store can only collect proof as fast as it sells, asks, and converts the ask. Every
proposal to "get more reviews" resolves into moving one of those three, and it is worth naming which.

## The catalogue is always outrunning the programme

New products arrive with zero proof and inherit none. A store that added products faster than it collected
reviews will show a healthy average and a growing hole underneath it. This is why coverage is measured
per product ([../rules/global-rules.md#G5](../rules/global-rules.md)) and why a coverage gap tends to
reappear rather than being solved once.

## Submission rate is mostly timing and friction

The two levers that move submission are when the ask arrives relative to possession, and how much work the
submission takes. Both are measurable through `reviews.request_analytics`. Message wording matters less
than either, which is the opposite of where most effort goes.

## Requests fatigue faster than marketing email

A review request is a favour asked of the customer with no benefit to them. The tolerance is therefore
lower than for promotional contact, and it is consumed per order rather than per period — which is why one
order gets one ask ([../rules/request-rules.md#R3](../rules/request-rules.md)).

## Ratings move slowly and fall faster than they rise

An average over a large base is hard to shift with new volume, but a run of low ratings on recent orders
signals a live problem that volume will not fix. The asymmetry means a falling rating is treated as a
diagnosis task and a low rating as an arithmetic one
([../rules/response-rules.md#P8](../rules/response-rules.md)).

## Moderation is a policy, not a judgement call

A queue worked case by case drifts, and drift in moderation is what turns a legitimate policy into the
appearance of censorship. The useful artefact is a written policy applied consistently, with the queue as
its output — not a set of individual decisions made under pressure about the rating.

## The programme has an end state worth naming

A mature programme is one where new products acquire proof automatically, coverage does not degrade as the
catalogue grows, ratings are monitored rather than managed, and replies are exceptional rather than
routine. Planning toward that state produces different choices from planning toward a review count.
