# Experimentation Principles

The purpose of a test is to produce a decision. A test that cannot change what anyone does afterwards is
measurement theatre.

## Test one variable at a time

Changing the subject line, the offer and the audience together produces a result nobody can attribute.
If several things must change at once, that is a new campaign, not an experiment.

## Start from a hypothesis

> *We believe [change] will improve [metric] for [audience] because [reason]. We will know by [measure].*

A test without a stated belief is data collection, and data collection without a question generates
findings that get interpreted after the fact to support whatever was already preferred.

## Test what is worth testing

Roughly by expected impact:

1. **Offer and incentive** — largest effect, directly affects margin
2. **Audience and targeting** — who receives it usually beats what it says
3. **Timing and cadence** — cheap to test, frequently significant
4. **Channel and sequencing** — email, SMS, or both, and in what order
5. **Content angle** — the argument the message makes
6. **Subject line** — worth testing, routinely over-weighted
7. **Creative details** — button colour and similar; almost never worth the measurement cost

Most testing effort concentrates on items 6 and 7, where the effects are smallest and the noise is
largest.

## Measure the outcome, not the proxy

If the hypothesis is about revenue, measure revenue. A subject-line test that wins on opens and loses on
revenue selected the wrong winner. Always check the downstream metric before declaring a result, and
always check the unsubscribe rate — a variant that wins on clicks while burning the list is a loss.

## Sample size and duration are decided in advance

Deciding when to stop *after* seeing the results is how noise becomes strategy. Before the test:

- What audience size does each variant get?
- How long does it run?
- What difference is large enough to act on?

Small audiences cannot resolve small differences. If the store's volume cannot produce a readable result,
do not run the test — make the decision on reasoning and say that is what you did.

## Most tests are inconclusive, and that is a result

"No detectable difference" is useful: it means stop spending attention here and test something with a
larger expected effect. Manufacturing a winner from noise is worse than admitting the test failed.

## One test at a time per audience

Overlapping tests on the same contacts contaminate each other's results.

## Record the outcome where the next decision will look

An experiment whose result is not written down will be re-run in six months. Results belong in the
evidence that future recommendations cite — see
[../schemas/recommendation.schema.json](../schemas/recommendation.schema.json).

## Winners decay

An audience habituates. A winning subject-line style stops winning once it becomes the norm. Periodic
re-testing of settled questions is legitimate; treating an old result as permanent is not.
