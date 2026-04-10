---
name: design-review
description: Use to evaluate existing designs against UX heuristics, accessibility standards, DS compliance, visual quality, or motion principles. Activates for /design-review, "review this design", "audit UI", "check accessibility", "is this compliant", "critique this screen", "WCAG check", "visual audit", "does this follow our DS".
---

# /design-review — Design Validation

Router for design review sub-agents. Runs heuristic evaluation, accessibility audit, DS compliance checks, visual quality inspection, and motion review. Aggregates findings into a single severity-grouped report.

## Maturity Detection

Follow `skills/shared/maturity-detection.md`. Run detection before routing.

- **L0 (Greenfield):** Run UX Critic, A11y Auditor, Visual Quality Inspector, and Motion Reviewer (if motion present). No DS Compliance Checker — no DS to check against.
- **L1 (DESIGN.md exists):** All L0 sub-agents plus DESIGN.md conformance checking within UX Critic and Visual Quality Inspector.
- **L2 (DS exists):** All 5 sub-agents active. DS Compliance Checker runs manual governance checklist from `governance.md`.
- **L3 (Tone/Enterprise):** All 5 sub-agents + DS Compliance Checker integrates Tone Lint via `use_figma` for automated compliance data.

Always announce the detected level before running.

## Always Load

- `skills/shared/knowledge/core-principles.md` (L1 — always)
- `skills/shared/knowledge/ux-heuristics.md` (L2 — evaluation framework and severity rubric)

## Multi-Sub-Agent Execution

Unlike other commands, `/design-review` typically runs multiple sub-agents in sequence on the same artifact. Default chain:

1. **Visual Quality Inspector** — structural and visual pass (run first to identify layout issues before heuristic analysis)
2. **UX Critic** — heuristic and cognitive load pass
3. **A11y Auditor** — WCAG 2.1 AA pass
4. **DS Compliance Checker** — token, override, detach pass (L2+ only)
5. **Motion Reviewer** — timing, purpose, a11y pass (run only if motion or animation is present)

Each sub-agent produces a finding table. After all sub-agents complete, aggregate all findings into one **Final Report** grouped by severity P0–P3.

If the user asks for a specific sub-agent only (e.g., "just check accessibility"), run that sub-agent alone and skip aggregation.

## Sub-Agent Router

| Trigger | Sub-Agent |
|---------|-----------|
| "visual", "alignment", "spacing", "layout quality", "polish" | Visual Quality Inspector |
| "heuristics", "usability", "cognitive load", "ux critique", "UX review" | UX Critic |
| "accessibility", "a11y", "WCAG", "contrast", "keyboard", "screen reader" | A11y Auditor |
| "compliant", "DS check", "tokens", "overrides", "detached", "Tone Lint" | DS Compliance Checker |
| "motion", "animation", "transition", "timing", "easing" | Motion Reviewer |
| "full review", "audit", "review everything", or no specific sub-agent | Run full default chain |

## Aggregated Output Format

After all sub-agents complete, produce:

```
## Design Review — <Screen/File Name>
**Maturity level:** <L0/L1/L2/L3>
**Sub-agents run:** <list>
**Total findings:** <count> (P0: X, P1: X, P2: X, P3: X)

---

### P0 — Blockers (must fix before release)
| # | Category | Sub-Agent | Location | Issue | Fix |
|---|----------|-----------|----------|-------|-----|
...

### P1 — Major (fix in this sprint)
| # | Category | Sub-Agent | Location | Issue | Fix |
...

### P2 — Minor (fix before handoff)
| # | Category | Sub-Agent | Location | Issue | Fix |
...

### P3 — Cosmetic (fix when possible)
| # | Category | Sub-Agent | Location | Issue | Fix |
...

---
### Summary
<2–3 sentences on the overall quality and priority theme>
```

---

## Sub-Agent: Visual Quality Inspector

**Load additionally:** `skills/shared/knowledge/visual-quality.md`

**Optional L3 query:** `Grep pattern="align\|spacing\|visual" path="skills/shared/data/design-principles.csv"` for principle backing on specific findings.

### Ask first

1. What is the artifact? (Figma link, screenshot path, or description)
2. Is this a final design or a work-in-progress? (calibrates severity expectations)

### Workflow

1. **Obtain the artifact**: If Figma link provided, fetch via `use_figma`. If screenshot, read via Read tool. If description only, note limited inspection capability.
2. **Run the squint test**: Blur your view of the layout mentally. Is the primary hierarchy immediately apparent? Are there competing focal points?
3. **Run the 3-second test**: After 3 seconds of viewing, can you identify: what this page is, what the primary action is, and where to start reading?
4. **Run the grayscale test**: Does the design work without color? Is hierarchy expressed through size, weight, and position — not color alone?
5. **Alignment audit** using `visual-quality.md` rules:
   - Check edge alignment (left edges, right edges consistent within zones)
   - Check center alignment (intentional vs. accidental)
   - Check baseline grid adherence
6. **Spacing audit**: Are gap values consistent with the spacing scale? Flag any ad-hoc values not from the token system.
7. **Visual rhythm**: Are repeated elements (cards, rows, list items) consistent in size and density?
8. **Balance**: Is visual weight distributed intentionally? Flag heavy-one-side compositions unless intentional.
9. **Anti-patterns check** from `visual-quality.md`: pseudo-alignment (off by 1–2px), inconsistent border radii, mixed icon stroke widths, orphan elements.
10. Assign severity to each finding using the P0–P3 rubric from `ux-heuristics.md`.

### Output format (per sub-agent, before aggregation)

```
## Visual Quality Findings — <Screen Name>

| # | Category | Location | Issue | Severity | Fix |
|---|----------|----------|-------|----------|-----|
...

**Overall visual quality:** Needs work / Acceptable / Strong
```

---

## Sub-Agent: UX Critic

**Load additionally:** None — `ux-heuristics.md` is already loaded.

**Optional L3 query:** `Grep pattern="<specific concern keyword>" path="skills/shared/data/psychological-principles.csv"` for cognitive or perceptual principle backing on specific findings.

### Ask first

1. What is the screen or flow? (Figma link or description)
2. What is the primary user goal on this screen?
3. Any specific concern — complexity, cognitive load, navigation confusion, hierarchy? (optional; if none, run the full heuristic pass)

### Workflow

1. **Obtain the artifact**: Fetch via Figma MCP or read from path.
2. **Apply Nielsen's 10 heuristics** from `ux-heuristics.md` — evaluate each heuristic against the design:
   - H1 Visibility of system status
   - H2 Match between system and real world
   - H3 User control and freedom
   - H4 Consistency and standards
   - H5 Error prevention
   - H6 Recognition over recall
   - H7 Flexibility and efficiency
   - H8 Aesthetic and minimalist design
   - H9 Help users recognize, diagnose, recover from errors
   - H10 Help and documentation
3. **Cognitive load assessment** using the framework in `ux-heuristics.md`:
   - Intrinsic load: Is the inherent complexity appropriate for the task?
   - Extraneous load: Is there unnecessary complexity in the layout or language?
   - Germane load: Does the design help the user build a correct mental model?
4. **IA check**: Discoverability (can the user find key actions?), findability (can the user re-find items?), scanability (is the hierarchy clear at a glance?), predictability (does the design behave as expected?).
5. **At L1**: Cross-check against DESIGN.md "Do's and Don'ts" section if it exists.
6. Assign severity per heuristic finding using the P0–P3 rubric. Use the finding table format from `ux-heuristics.md`.

### Output format

```
## UX Heuristic Findings — <Screen Name>

| # | Heuristic | Location | Issue | Severity | Suggestion |
|---|-----------|----------|-------|----------|-----------|
...

**Cognitive load assessment:** Low / Medium / High — <one sentence reason>
```

---

## Sub-Agent: A11y Auditor

**Load additionally:** `skills/shared/knowledge/accessibility.md`

**Optional L3 query:** `Grep pattern="form\|touch\|contrast" path="skills/shared/data/ecommerce-usability.csv"` for domain-specific accessibility anchors.

### Ask first

1. What is the screen or component to audit? (Figma link or description)
2. Target WCAG level — AA (standard) or AAA (enhanced)? Default: AA.
3. Any specific concern — contrast, keyboard navigation, screen reader, form labeling?

### Workflow

1. **Obtain the artifact**: Fetch via Figma MCP or read from path.
2. **Walk the WCAG 2.1 AA checklist** from `accessibility.md` grouped by principle:
   - **Perceivable**: Alt text for non-text content, captions, color not sole means of conveying info, contrast ratios (4.5:1 text, 3:1 UI, 7:1 enhanced for AAA).
   - **Operable**: Keyboard accessible (all actions reachable via keyboard), focus order logical, focus visible, no keyboard trap, skip links, touch target size (≥44×44px).
   - **Understandable**: Labels on inputs, error identification and suggestion, consistent navigation, readable language.
   - **Robust**: Semantic structure, ARIA landmarks correct, no ARIA misuse, states exposed.
3. **Contrast check**: For all text/background pairs visible in the artifact, verify ratios. Flag violations with the specific pair and measured ratio if determinable.
4. **Keyboard pattern check**: Identify interactive elements. Verify they follow expected keyboard patterns from `accessibility.md` (buttons, links, menus, dialogs, tabs).
5. **ARIA check**: Are landmark roles present? Are form elements labeled? Are live regions used where status changes occur?
6. **Motion a11y**: Does the design use animation? Flag if `prefers-reduced-motion` handling is not addressed. Flag any content that flashes (potential seizure risk).
7. Assign severity: contrast failures at normal text = P0; keyboard trap = P0; missing label = P1; missing skip link = P2; cosmetic focus ring styling = P3.

### Output format

```
## Accessibility Findings — <Screen Name>
**Target level:** WCAG 2.1 AA

| # | WCAG Criterion | Location | Issue | Severity | Fix |
|---|---------------|----------|-------|----------|-----|
...

**Contrast failures:** <count>
**Keyboard issues:** <count>
**Overall a11y status:** Failing / Needs work / Passing with minor issues / Passing
```

---

## Sub-Agent: DS Compliance Checker

**Load additionally:** `skills/shared/knowledge/governance.md`

**Optional L3 query:** Not applicable — compliance is checked against DS governance rules, not CSVs.

**L3 note:** At L3, this sub-agent reads Tone Lint results via `use_figma` before running the manual checklist.

### Ask first

1. What file, page, or selection should be checked? (Figma link or scope description)
2. At L2: do you have the `.ds-context.md` available for library reference?

### Workflow

**At L3 (Tone DS):**

1. Read Tone Lint results:
   ```
   use_figma(fileKey, code: 'return figma.root.getSharedPluginData("tone_lint", "lint_results")')
   ```
   Parse the returned JSON for: `unbound_variables`, `detached_components`, `override_violations`, `naming_issues`.
2. Supplement with the manual checklist below for any areas Tone Lint does not cover.

**At L2 (Generic DS) and L3 manual supplement:**

3. **Token compliance**: Are all fills, strokes, spacing, and radius values bound to DS tokens? Any hard-coded values (hex, px literals not from tokens) are violations.
4. **Override check**: Are any component instance properties overridden beyond what the DS API allows (copy/text permitted; structural overrides are P1)?
5. **Detached components**: Are any DS components detached (converted to frames/groups)? Detached components are always P1 — they miss future DS updates.
6. **Library version**: Is the DS library version current? Flag if a known update exists.
7. **Pattern conformance**: Does the design use Patterns (L1) and Squad Patterns (L2) where available, or is it composing ad-hoc when a pattern exists?
8. **Pre-handoff checklist** per `governance.md`: Tone Lint run, UX review done, all states designed, responsive breakpoints covered.
9. Assign severity: detached component = P1; unbound variable = P1; unauthorized override = P1; outdated library = P2; missing state = P2; pattern bypass = P2.

### Output format

```
## DS Compliance Findings — <Screen Name>
**DS:** <DS name and version>
**Lint source:** Tone Lint automated / Manual checklist

| # | Category | Component/Element | Issue | Severity | Fix |
|---|----------|------------------|-------|----------|-----|
...

**Compliance summary:** <count> unbound variables, <count> detached components, <count> override violations
**Pre-handoff gate:** Pass / Fail — <blocking items if fail>
```

---

## Sub-Agent: Motion Reviewer

**Load additionally:** `skills/shared/knowledge/motion.md`

**Optional L3 query:** Not applicable for motion review.

### Ask first

1. What interaction or transition are we reviewing? (describe or link prototype)
2. Is a Figma prototype available, or are we reviewing motion specs only?
3. Any specific concern — timing feels off, animation purpose unclear, accessibility?

### Workflow

1. **Obtain the motion artifact**: Access Figma prototype via `use_figma` if available, or parse motion specs from the design description.
2. **Verify motion purpose** — each animation should serve one of the priority order from `motion.md`: feedback > continuity > spatial orientation > delight. Flag any animation that serves only delight with no functional purpose (P3 if subtle, P2 if distracting).
3. **Measure timing** against standards from `motion.md`:
   - Micro-interactions (button feedback, toggle): 100ms
   - Small transitions (tooltip, dropdown): 200ms
   - Medium transitions (panel open, modal): 300ms
   - Large transitions (page, full-screen): 500ms
   Flag durations that exceed these by >50% as P2.
4. **Check easing** against `motion.md` guidelines:
   - Enter transitions: ease-out
   - Exit transitions: ease-in
   - Position changes: ease-in-out
   - Natural/physical: spring
   Flag mismatched easing as P2.
5. **Performance check**: Does the motion use only `transform` and `opacity`? Any animation that triggers layout or paint is P1.
6. **Accessibility check**:
   - Is `prefers-reduced-motion` respected? If not addressed at all: P1.
   - Any animation that loops infinitely without user control: P1.
   - Any content that flashes more than 3 times per second: P0 (seizure risk).
7. **Anti-patterns** from `motion.md`: bounce on every interaction, decorative-only long-duration motion, motion competing with focus flow.

### Output format

```
## Motion Review Findings — <Screen/Interaction Name>

| # | Animation | Purpose | Timing | Easing | Issue | Severity | Fix |
|---|-----------|---------|--------|--------|-------|----------|-----|
...

**Motion a11y:** prefers-reduced-motion addressed? Yes / No / Partially
**Overall motion quality:** Purposeful / Mixed / Decorative-heavy
```
