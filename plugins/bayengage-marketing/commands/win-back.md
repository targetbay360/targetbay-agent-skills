---
description: Decide which lapsed customers are worth recovering, and where to stop
---

Use the `customer-winback` skill.

Derive the lapse definition from this store's own purchase intervals, not a fixed number of days.
Segment the lapsed base by prior value *and* current reachability, and route the unreachable tail to a
suppression recommendation rather than to more sending — state its size and prior value so the
trade-off is visible.

Bound the attempt count and state the stop condition before proposing the first send.

Sending any attempt needs explicit per-attempt approval; suppressing contacts is destructive and needs
explicit approval after the loss is reported (`rules/safety-rules.md`).
