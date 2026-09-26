---
title: Clear My SMS Messages Before Sending
summary: A PASS, WARN or BLOCK verdict on an SMS campaign or automation covering consent, opt-out and timing.
skill: email-quality-auditor
---
Using TargetBay Email & SMS (`email-quality-auditor` skill), audit the SMS in [CAMPAIGN OR AUTOMATION NAME] before it sends or goes live.

Check:
- every recipient has SMS consent and isn't suppressed
- opt-out instructions and store identification are present
- the send lands outside quiet hours in each recipient's local time
- how many messages the same people received recently
- links, personalisation fallbacks, offer terms and product availability
- collisions with other sends in the window

Return the verdict, the resolved audience size, each finding with cost and fix, and checks you couldn't run.

If data is missing, say so and ask; don't estimate. Change nothing and send nothing until I approve; show who and how many it affects first.
