# Changelog

All notable changes to TargetBay Onboarding Skills are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this package adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-09-16

### Changed

- **The skill contract is thirteen sections, not fourteen.** `Inputs` is removed from every skill and
  from `tests/validate.py`; every skill is a MAJOR bump as a result.
- **`personalization-audit`, `surface-inventory`, `onsite-search` and `context-audit` split more
  cleanly.** `surface-inventory` owns what is running now; `personalization-audit` owns what to do about
  it; `onsite-search` owns failing queries. Two golden prompts previously separated by a 0% margin now
  resolve without a warning.
- `docs/mcp-integration.md` no longer transcribes `capabilities.yaml`; it records the two capabilities
  that still carry an open question and points at the registry for the rest.
- The README documents the five slash commands, which it previously did not mention.
- `docs/` is published to npm, so the README's links to it resolve in the tarball.

### Fixed

- **Installed skills no longer cite files that are not there.** Both installers rewrite the
  `../../rules/`, `../../knowledge/` and `../../schemas/` citations that flattening breaks into the
  released URL for the installed version.
- `install.sh` installs slash commands alongside a `.claude` tree, matching `install.mjs`.

## [0.2.0] - 2026-09-15

Onsite personalisation moves in. It was a fifth plugin, `targetbay-personalization`, sold and installed as
a product of its own. It is not one — it is the step every product's onboarding starts with, and keeping
it separate meant a store could onboard without it and a plugin could drift from the sequence it belongs
to.

Six skills, three rule files and two knowledge documents now live here. The `onsite.*` registry is gone;
its capabilities are `onboarding.*`.

### Added

- **Six onsite skills.** [`surface-inventory`](skills/surface-inventory/SKILL.md) (analysis) sits at the
  bottom of its own graph and carries the consent read;
  [`recommendation-strategy`](skills/recommendation-strategy/SKILL.md),
  [`offer-targeting`](skills/offer-targeting/SKILL.md) and
  [`onsite-search`](skills/onsite-search/SKILL.md) decide what a surface shows and to whom;
  [`experience-experimentation`](skills/experience-experimentation/SKILL.md) decides whether a change can
  be proved at this store's traffic; [`personalization-audit`](skills/personalization-audit/SKILL.md)
  ranks what is worth fixing when nobody has named the problem. Ten skills in two graphs, each with one
  skill at the bottom.

- **Three rule files** — [`targeting-rules.md`](rules/targeting-rules.md) (`T1`–`T8`),
  [`surface-rules.md`](rules/surface-rules.md) (`U1`–`U7`) and
  [`measurement-rules.md`](rules/measurement-rules.md) (`M1`–`M8`). Their numbering is unchanged, because
  `T`, `U` and `M` collided with nothing here.

- **Eleven onsite capabilities** in [`capabilities.yaml`](capabilities.yaml), fifteen in total.
  `onboarding.consent_and_tracking` is the one whose absence blocks rather than degrades.

- **Two knowledge documents** — [`personalization-principles.md`](knowledge/personalization-principles.md)
  and [`visitor-behaviour.md`](knowledge/visitor-behaviour.md).

- **Three commands** — `/audit-experience`, `/surface-map` and `/search-gaps`.

### Changed

- **`global-rules.md` gains `G17`–`G24`**, the eight rules the onsite work needs that onboarding did not
  already state: revenue per session over engagement, attribution as a claim, consent before value,
  attention as the scarce resource, no segment that changes nothing, the simplest change that works,
  anonymous and identified as different problems, and measurement declared before the change. The
  existing `G1`–`G16` keep their numbers. `G5` absorbed the old personalization `G6`, because "inspect
  what already exists" was the same rule twice.

- **`safety-rules.md` gains `S15`–`S21`** — consent as a precondition, no targeting on a sensitive
  attribute or its proxy, no price variation by visitor, no experience the visitor cannot escape,
  inspection before a destructive action, no test called early because it is winning, and stopping on
  ambiguity in an irreversible path. `S1`'s risk table now covers live-visitor changes. `S15` through
  `S18` are absolute.

- **`onsite.*` capability identifiers are now `onboarding.*`.** `onsite.store_profile` is retired into
  `onboarding.store_context`, which already carried the same identity and catalogue values;
  `onsite.search` is `onboarding.onsite_search`. A plugin's registry may not span namespaces, and after
  this release onsite is not a separate namespace because it is not a separate product.

- **`skill.schema.json` accepts four more categories** — `onsite`, `merchandising`, `discovery` and
  `experimentation`. The two skills previously categorised `personalization` are now `onsite`.

- **The blueprint sequences three products, not four.** `contact-ownership-rules.md#X2` no longer lists
  Personalization as the owner of the onsite moment; nothing owns it, which is why `X3` holds and why the
  onsite work still sequences first.

### Migration

`targetbay-personalization` is removed from the marketplace. Install `targetbay-onboarding` instead —
every skill, rule and capability it carried is here, under the names above. Rule citations changed:
`global-rules.md#G1` is now `#G17`, `#G4` is `#G18`, `#G5` is `#G19`, `#G6` is `#G5`, `#G7` is `#G20`,
`#G8` is `#G21`, `#G9` is `#G22`, `#G12` is `#G23`, `#G13` is `#G24`, `#G14` is `#G13`. For safety,
`#S2` is now `#S15`, `#S3` is `#S16`, `#S4` is `#S17`, `#S5` is `#S18`, `#S6` is `#S5`, `#S7` is `#S4`,
`#S8` is `#S9`, `#S9` is `#S19`, `#S10` is `#S20`, `#S11` is `#S3`, `#S12` is `#S21`, `#S13` is `#S10`,
`#S14` is `#S11`, `#S15` is `#S12`.

### Known gaps

- Every capability still maps to `TODO`. The skills plan; they do not execute.
- `onboarding.provisioning` remains unverified — no TargetBay write surface has been inspected.
- Whether consent state is readable per visitor or only per region is still open, and the two produce
  materially different onsite designs. See [docs/mcp-integration.md](docs/mcp-integration.md).

## [0.1.0] - 2026-09-12

First release. Four skills forming one pipeline, a capability registry, the rules and knowledge they
cite, and the schema for the derived store context they all read.

This is a `0.x` line because no TargetBay MCP surface has been inspected yet. Every capability in
[capabilities.yaml](capabilities.yaml) maps to `TODO`, which means the skills can plan but cannot
execute. Skill reasoning is expected to be stable; capability identifiers may still change as the real
MCP is mapped.

### Added

- **Four skills forming a pipeline**, not a catalogue. [`context-audit`](skills/context-audit/SKILL.md)
  (analysis) sits at the bottom of the graph and establishes what is known;
  [`onboarding-intake`](skills/onboarding-intake/SKILL.md) (mutation) asks only what the platform cannot
  observe; [`onboarding-blueprint`](skills/onboarding-blueprint/SKILL.md) (plan) sequences all four
  products across ninety days; [`onboarding-provisioning`](skills/onboarding-provisioning/SKILL.md)
  (high_impact) builds the approved plan as drafts and stops. The risk level climbs at each step so a
  reviewer can disagree with the facts before the plan is built on them, and with the plan before
  anything is created.

- **A cross-product plugin, because the validator requires one.** A plugin's capability identifiers may
  not span namespaces, and `composes:` may only name skills in the same plugin. An onboarding skill that
  needs `reviews.*`, `loyalty.*` and `onsite.*` alongside `email_sms.*` therefore cannot live in any
  product plugin. The `onboarding.*` namespace declares four orchestration capabilities rather than a
  fifth copy of the fifty-five product ones.

- **[`contact-ownership-rules.md`](rules/contact-ownership-rules.md), answering the marketplace's
  unreconciled-contact problem.** TargetBay Email & SMS, Reviews and Loyalty can each decide,
  independently and correctly, to contact the same customer. X1 puts the contact budget on the platform
  rather than in each product; X2 assigns each lifecycle moment exactly one owner; X3 records why onsite
  personalization is structurally exempt; X5 and X6 answer the open dispatch questions recorded in the
  Loyalty and Reviews integration docs; X7 makes a stated aggregate a condition of approval. X9 states
  the residual dependency: none of this is *enforceable* without a unified cross-product frequency and
  consent view from the MCP, and where that view does not exist the budget is labelled provisional rather
  than claimed as enforced.

- **[`sequencing-rules.md`](rules/sequencing-rules.md).** Capture before consumption, because a review
  trigger armed on day sixty cannot ask about a day-ten order. Reversible before irreversible.
  Preconditions stated as observations, never as dates.

- **[`context-pack.schema.json`](schemas/context-pack.schema.json).** The derived store context every
  skill reads. Its load-bearing type is `derivedValue`: a quantity plus its basis — derived, provisional,
  stated or absent — its sample size and its evidence. A `derived` value must carry an `n` and evidence;
  a `provisional` or `absent` value must name the observation that would replace it; an `absent` value's
  `value` must be null. This makes global rules G3 and G14 a schema constraint rather than author
  discipline, which matters most for the zero-history store where every instinct is to fill the gap.

- **Rule anchors chosen to survive.** `sequencing-rules.md` uses the `SQ` prefix rather than `Q`, because
  `onboarding-intake`'s twelve intake questions are already `Q1`-`Q12` and
  `context-pack.schema.json` encodes their answers as `intake:Q3` — one plugin cannot have two meanings
  for `Q1`. `global-rules.md` keeps the same tail numbering as the other four plugins (`G15` declare what
  you could not check, `G16` prefer reversible steps first) so an author moving between plugins is not
  surprised.

- **Two knowledge documents.**
  [`evidence-and-provenance.md`](knowledge/evidence-and-provenance.md) covers the four bases and what a
  store with no history can honestly be given;
  [`onboarding-sequence.md`](knowledge/onboarding-sequence.md) covers why ordering decides the outcome.

### Known gaps

- **No MCP mapping.** All four capabilities are `TODO`. The nine questions that mapping must settle are
  listed at the bottom of [docs/mcp-integration.md](docs/mcp-integration.md).
- **`onboarding.provisioning` is unverified.** No TargetBay write surface has been inspected. Until one
  is, `onboarding-provisioning` degrades to producing a build checklist rather than creating anything.
- **The contact budget is not enforceable from here.** The rules decide ownership; enforcement needs a
  unified frequency and consent view from the platform. See X9.
- **No vertical playbooks.** Onboarding reads the detected vertical from the store context and applies
  the Email & SMS playbooks. Whether the other three products need their own overlays is an open
  question, and inventing five of them without evidence would be the error this marketplace avoids
  elsewhere.
- **A fifth copy of the shared layer.** `global-rules.md`, `safety-rules.md` and three schemas are now
  duplicated five times across the marketplace. Extracting a shared layer is tracked at the repository
  root and is deliberately not coupled to this release.
