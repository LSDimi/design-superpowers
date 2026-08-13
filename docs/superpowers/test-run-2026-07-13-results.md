# Test Run Results — Aesthetic Mechanics Cycle (2026-07-13)

> **Re-run addendum (2026-07-13, post-fix):** all three Partials re-run against the fixed knowledge and **flipped to Yes** with no regressions in spot-checked secondary behaviours — CTX1a now yields 3 variants differentiated on open grammars (layout/depth/imagery/density) under the context-locked serif; IMG1's brief core hand-counts at 53 words; the Palette Architect defines hover/active/focus/disabled derivations. **Final: 66 / 66 Yes.** Transcripts: `scratchpad/results/reruns-flipped.md`. Live re-run completed later the same day once the Bridge was launched inside ds testground: **SG1-live Partial** — a genuine live review found real drift with concrete fixes (6px vs 8px radius, off-grid 13/29/17/9px spacing, hex-re-entry near-miss #4f45e5 vs brand/500 #4f46e5), but the literal soft-shadow-on-neubrutalism scenario is not reproducible in this file (zero shadow effects anywhere — noted honestly, degraded-path pass stands as scenario coverage); **IMG3-live NOT-REPRODUCIBLE** (full 4-page node walk: zero image fills). To make both reproducible, the testground needs a shadow-bearing drifted sample and a photography screen. PluginOS failure log for the plugin project: `pluginos-failure-log-2026-07-13.md` (19 calls: 16 OK, 3 failures + 1 silent data truncation).

_Branch `feat/aesthetic-mechanics-and-data-audit` at commit `011ec84` (fixes from findings landed after as `5b2584e`). Scope per Dimi's directive: new tests + the affected slice of the 239; fundamentals untouched by this cycle (ds-make, ds-manage, map-design, ds-producer/consumer) were NOT re-run._

## Headline

| Suite | Yes | Partial | No | Blocked | Total |
|-------|-----|---------|----|---------| ------|
| New tests (plan sections A–E) | 28 | 2 | 0 | 0 | 30 |
| Affected-239 slice (/creative all levels + review-VQ) | 35 | 1 | 0 | 0 | 36 |
| **Total** | **63** | **3** | **0** | **0** | **66** |

All three Partials were concrete, single-criterion gaps — **fixed and committed the same day** (`5b2584e`, see below). Zero regressions from the data-layer restructure, the /creative expansion, or the brand/context work.

## Method

- Runner: one subagent per cell (affected slice, self-scored with evidence — same protocol as the baseline/v2 runs) and per new-test batch (transcripts only); **independent grader** for all new tests, hard-artifact criteria. Model: Sonnet throughout (runners + grader) — note when comparing absolute scores to earlier runs.
- Fixtures: fresh L0 (empty), L1 (Lumen DESIGN.md), L2 (Fathom DS + .ds-context), L3 (Meridian enterprise .ds-context), rebuilt in scratchpad.
- Figma: PluginOS bridge was live but connected to a different file than the ds testground for most of the run (and briefly fully disconnected). Every agent handled this per `figma-adapter.md` — documented mismatch, degraded path, no fabricated reads. IMG3 turned this into a genuine live review of the actually-connected photography-heavy screen: it found two real content bugs (placeholder "Badge" text on 3 cards; leftover "Superhost" copy from a repurposed template) and hand-computed a passing WCAG ratio.

## The differentiation test (the cycle's core question)

CTX1 (traditional Italian pasta brand) vs CTX2 (paintball team fan page), same command, same phrasing:

- **Pass on divergence:** opposite typography classes (transitional serif vs angular condensed sans), opposite palette temperatures, disjoint reference pools, each grounded in the correct `style-contexts.csv` row (Artisanal Heritage; Gaming/Fandom — which names paintball squads).
- **Grader's craft note:** "reads as a designer who understood both worlds, but executed one (CTX2) more rigorously" — CTX2's three variants each anchored to a distinct named recipe; CTX1's three variants leaned on one serif family at three intensities (→ the CTX1a Partial).

## Partials and same-day fixes (`5b2584e`)

| Finding | Test | Fix |
|---------|------|-----|
| False variety under narrow contexts — when the context row pins typography (heritage → serif), variants collapsed into one family | CTX1a | Range rule now says: differentiate on the grammars that remain open (layout, depth, imagery, density) when a context row narrows one |
| Image-brief promptable core ran 73–98 words vs the 30–60 spec (and the transcript miscounted itself) | IMG1b | Hard cap 60 words, "count them before delivering," metadata excluded from the count |
| Palette anchor never derived a disabled state | L0-creative-probe-07 | Palette Architect step 4 now requires hover/active/focus/disabled derivations (never opacity-only on text) |

These fixes are knowledge/skill edits; the three tests should flip on the next slice re-run.

## Notable strong behaviors (evidence in `scratchpad/results/`)

- **Graceful degradation held everywhere** it was provoked: wrong-file bridge (RS, IMG2, IMG3), disconnected bridge (SG1 → degraded-path review still caught the neubrutalism/soft-shadow depth-grammar violation with row citations), L0 refresh request (RS3 → handoff, not a block).
- **New usability rows fired non-speculatively** (DR2): inline-validation and consent rows matched a described signup form's flaws almost verbatim.
- **Brand Layer 1 discipline:** BA3 flagged the fintech blue as a presumed Core distinctive asset requiring business evidence before any change — exactly the Sharp/Romaniuk behavior the two-layer design intended.
- **L3 delegation intact:** RS4/creative-L3 cell routed token work through /ds-make → ds-producer, named cascade order, no ad-hoc restyling.

## Caveats & environment notes

- Grader flagged possible rubric visibility in one BA run (transcript self-labels a criterion) — behavior was genuinely present, but next harness should hide expected_behaviours from runners of new tests.
- Test-plan header said 28 tests; the tables enumerate 30 — all 30 graded.
- SG1's grading note and the plan's BLOCKED rule conflicted (fully-down bridge vs wrong-file bridge); resolved in favor of grading the degraded path since that behavior is specified by the suite. Rule out live-Figma variance: re-run IMG3/SG1 with the ds testground file open in Figma when convenient.
- `usability.csv` currently has no Low-severity rows (scale is used, tier just doesn't occur) — noted so future graders don't misread the vocabulary claim.
- Single-run LLM grading retains ±1-tier variance on soft criteria; hard-artifact criteria (word counts, field presence, family disjointness) behaved as intended.

## Recommendation

The cycle's changes are validated at the behavior level with zero regressions in the affected surface. Suggested next steps:
1. Merge the branch (11 commits) after your review — then fold the 30 new tests into the master xlsx as a fifth sheet or per-level additions.
2. Re-run the 3 flipped tests + IMG3/SG1 live-Figma variants after merge (small, cheap slice).
3. Next cycle candidates unchanged: ds-producer token-rename codemod, /ds-manage templates, RTL + perceived-perf lenses.
