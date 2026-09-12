# Frequency Rules

Cadence, fatigue and collision. Cited as `frequency-rules.md#F1`.

Frequency is the one dimension where every skill's locally correct decision adds up to a globally wrong
outcome. Each campaign looks justified; the recipient receives nine messages in a week and unsubscribes.

---

### F1. The platform's caps are the floor, not the target.
`email_sms.suppression_and_consent` defines what is permitted. Permitted is not the same as advisable.
Plan below the cap, not up to it.

### F2. Count total contact, not per-skill contact.
Before adding a send, count everything the same contact will receive in that window from campaigns *and*
automations. A skill that only counts its own messages will always conclude there is room.

### F3. Automations and campaigns share the same budget.
A contact in a three-message post-purchase journey has already been contacted three times. A campaign on
top of that is a fourth.

### F4. Declare the cadence assumption.
Every plan states the contact frequency it assumes for each audience. An undeclared assumption cannot be
reviewed or corrected.

### F5. Frequency tolerance varies by segment.
Recently active buyers tolerate more contact than dormant contacts. Scale cadence to engagement, and
reduce it — do not increase it — for contacts who have stopped responding.

### F6. Escalating contact to a non-responder is the wrong direction.
Repeated messaging to someone who has ignored the last several is how a deliverability problem starts.
Reduce frequency, change channel, or stop.

### F7. SMS has a much lower ceiling than email.
Treat SMS as a scarce, interruptive channel. Its cadence budget is separate and smaller, and it carries a
per-message cost.

### F8. Resolve collisions explicitly.
When two planned sends hit the same contact within the same short window, decide which one yields, and
say so. See [audience-rules.md#A8](audience-rules.md).

### F9. Quiet hours and local time are part of the plan.
Sends are planned in the recipient's local time, and SMS respects quiet hours as configured on the
platform.

### F10. Peak periods raise frequency but not indefinitely.
Higher cadence during a major sale period is legitimate. It still needs an upper bound, and it still
needs to return to baseline afterwards.

### F11. Unsubscribe and complaint rates are frequency signals.
Rising opt-outs at steady content quality is a cadence problem. Treat it as one before rewriting copy.

### F12. Fatigue has a recovery period.
After an intense period, plan a reduced-contact window for the same audience rather than moving straight
to the next push.
