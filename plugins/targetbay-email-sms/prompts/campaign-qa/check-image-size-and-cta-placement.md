---
title: Check Logo, Hero and CTA on Mobile
summary: Whether my logo, hero image and main call to action hold up on phones and with images off.
skill: email-render-qa
---
Using TargetBay Email & SMS (`email-render-qa` skill), check how [EMAIL NAME] holds up on a phone before it sends.

Focus on:
- logo and hero image: sized for narrow screens, sharp, not too heavy to load
- main call to action: visible on the first screen, a real button rather than text inside an image
- images off: do the message and CTA still make sense
- dark mode: does the logo vanish or the hero clash

Weight each defect by the share of my opens from phones and each mail client, from my data.

Return a must-fix list and a may-ship list, each with the fix.

Analysis only: change nothing.
