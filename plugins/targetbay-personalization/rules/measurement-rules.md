# Measurement Rules

Constraints on how an onsite change is evaluated. Cited as `measurement-rules.md#M4`.

---

### M1. Declare the metric, the comparison and the horizon before the change.
A success criterion chosen after the results are in is not a criterion
([global-rules.md#G13](global-rules.md)). State all three as part of the proposal.

### M2. The current experience is the baseline and it is presumed adequate.
The burden of evidence sits with the change. A variant that does not beat the default is a variant that
does not ship, not a variant that needs a better audience.

### M3. Separate incremental revenue from redirected revenue.
Attribution to a placement counts purchases that flowed through it, not purchases it caused. State the
attribution method and its limits, and check cannibalisation before calling anything incremental
([global-rules.md#G4](global-rules.md), [surface-rules.md#U5](surface-rules.md)).

### M4. Declare the stopping condition, and honour it.
A test runs to its pre-declared sample or duration. Stopping early on a favourable interim result is
prohibited ([safety-rules.md#S10](safety-rules.md)); stopping early for a different reason is reported as
inconclusive, never as a result.

### M5. Do not run a test the traffic cannot resolve.
Compute whether this store's volume can detect an effect worth acting on within a plausible horizon. Where
it cannot, say so and propose a decision made on reasoning instead — an underpowered test is worse than no
test, because it produces a number people believe.

### M6. One change per test.
A variant that alters placement, strategy and creative at once yields a result nobody can act on. Where
several changes must ship together, say that the test measures the bundle and cannot attribute within it.

### M7. Measure the losers too.
Report what the change cost as well as what it gained — the surface it displaced, the segment that
converted worse, the traffic that saw nothing. A result reported only where it was favourable is not a
result.

### M8. Novelty decays.
A new onsite element attracts attention because it is new. Where the horizon permits, check whether the
effect persists past the first period before treating it as durable.
