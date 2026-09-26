---
title: Check Every Link Before Sending
summary: Broken, mistargeted or untracked links in one campaign, with a send verdict.
skill: email-quality-auditor
---
Using TargetBay Email & SMS (`email-quality-auditor` skill), check every link in my campaign [CAMPAIGN NAME] before it goes out.

For each link give: visible text, destination, whether it resolves, whether its UTM tracking parameters are present and consistent, and whether a linked product is in stock at the price shown.

Also check the opt-out link and any personalised link's empty-data fallback.

Return:
- verdict: PASS, WARN or BLOCK
- each finding with its cost and fix
- links you couldn't verify, named individually

If data is missing, say so and ask; don't estimate. Change nothing and send nothing until I approve; show who and how many it affects first.
