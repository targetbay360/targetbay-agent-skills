# Evidence and Provenance

Why onboarding tracks where every number came from, and what it costs when it does not.

## The problem onboarding has that optimisation does not

Almost every other skill in the TargetBay marketplace derives its thresholds from history. A lapse point
comes from the store's own inter-purchase interval. A VIP boundary comes from where the value
distribution actually breaks. Those skills can afford to fail loudly when the data is missing, because a
store asking for optimisation has usually been running long enough to have some.

Onboarding has the opposite situation. The store is asking precisely because nothing has happened yet.
Refusing to answer is not an option — the store needs a programme on day one — and neither is inventing
the numbers. What is left is being exact about which is which.

## Four bases, and why the distinction is load-bearing

A quantity in the Store Context Pack is one of four things:

**Derived.** Computed from this store's own data, with a sample size and the observation behind it. This
is the only kind that can be trusted without qualification, and the only kind that may gate an
irreversible decision.

**Provisional.** A vertical-playbook default standing in for a measurement. Useful, and genuinely better
than nothing, but it is a statement about stores in general, not about this store. A provisional value is
only honest when it travels with the observation that would replace it.

**Stated.** The store told us. Margin posture, brand policy, capacity and channel restrictions are not
observable from data at all, and no amount of history will make them so. A stated value is not weaker
than a derived one — for these questions it is the only valid source — but confusing the two is how an
agent ends up "deriving" a margin ceiling from discount history that merely reflects what the store
happened to run.

**Absent.** Not derivable and not defaulted. The hardest of the four to leave alone, because an absent
value looks like a gap that wants filling. Filling it is the error.

## Why an empty result is not an answer

A read that returns nothing is ambiguous in a way that matters. "This store has no lapsed customers" and
"the lapsed-customer read is unavailable for this store" are different findings with opposite
implications, and they arrive looking identical unless the platform distinguishes them.

This is the single most common route to a fabricated onboarding plan: a read comes back empty, the empty
result is treated as a measurement, and a store with unreadable data gets a programme built on the
assumption that it has no customers. The pack's readiness matrix exists to make the distinction
explicit before any skill has to guess.

## The zero-history store

A store nine days old will return `absent` for nearly every derived value in the pack. This is the most
common onboarding shape, not an edge case, and being honest about it changes what onboarding is for.

What such a store can still be given, without inventing anything:

- **Sequencing.** The order of work is a structural decision, not a statistical one. It does not need
  history to be correct.
- **Catalogue-shape decisions.** Whether the catalogue supports replenishment at all is visible from the
  products, before a single order exists.
- **Stated constraints.** Intake answers are `stated` on day one and never get better with age.
- **Playbook defaults, labelled.** A vertical default is a reasonable starting point as long as nobody
  mistakes it for a measurement.
- **A review point.** The moment the provisional values become derivable, expressed as a count of orders
  or repeat purchases rather than a date.

What it cannot be given is a personalised threshold. Every skill in this plugin is built to say so
rather than to produce one.

## Reading this alongside

- [../rules/global-rules.md](../rules/global-rules.md) — G3 and G14 are the enforceable form of this
  document
- [../schemas/context-pack.schema.json](../schemas/context-pack.schema.json) — where the four bases are
  a schema constraint rather than a convention
