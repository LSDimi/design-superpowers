---
name: design
description: Use when designing product features, flows, pages, or screens using an existing design system or design language. Activates for /design, "design a feature", "build a page", "select components", "compose a flow", "what component should I use", "layout this screen", "is there a pattern for", "we're missing a component".
---

# /design — Product Design with DS

Router for product design sub-agents. Composes interfaces from existing DS components and patterns. At L3 (Enterprise), delegates to `skills/ds-consumer/SKILL.md`.

## Maturity Detection

Follow `skills/shared/maturity-detection.md`. Run detection before routing.

- **L0 (Greenfield):** Block. A design language must exist before composing. Redirect: "Run /creative to establish a visual direction, then /map-design to generate DESIGN.md."
- **L1 (DESIGN.md exists):** Compose using DESIGN.md primitives (colors, type scale, spacing). No DS library to reference — work from documented values only.
- **L2 (DS exists):** Full DS-aware composition. Load `.ds-context.md` for library keys. Select from available components; flag gaps via Gap Detector.
- **L3 (Enterprise DS):** Delegate to `skills/ds-consumer/SKILL.md`. Sub-agents below are available for exploration and planning; final design execution goes through ds-consumer workflows.

Always announce the detected level before routing.

## Always Load

- `skills/shared/knowledge/core-principles.md` (L1 — always)
- `skills/shared/knowledge/component-patterns.md` (L2 — component selection)
- `skills/shared/knowledge/ux-heuristics.md` (L2 — evaluate compositions)

## Hard Rules (all maturity levels)

- **NEVER propose creating new components here.** If a gap exists, use Gap Detector → route to /ds-make.
- **NEVER apply overrides or detach components** at L2/L3. Flag violations as P1.
- **Prefer existing patterns** over ad-hoc compositions. Check Pattern Matcher before composing from scratch.
- **User is the approver** for gap requests — never submit without explicit sign-off.

## Sub-Agent Router

| Trigger | Sub-Agent |
|---------|-----------|
| "which component", "what should I use", "select", "best fit", "compare components" | Component Selector |
| "compose", "layout", "page", "flow", "screen", "build a", "structure this" | Layout Composer |
| "pattern", "is there a pattern", "template", "how do others do", "existing solution" | Pattern Matcher |
| "gap", "missing", "nothing fits", "no component for", "request new" | Gap Detector |

If the request spans multiple (e.g., "compose this page and flag any gaps"), run Pattern Matcher → Component Selector → Layout Composer → Gap Detector in sequence.

---

## Sub-Agent: Component Selector

**Load additionally:** None — `component-patterns.md` already covers component API, hierarchy, and variant strategies.

**Optional L3 query:** `Grep pattern="<component type>" path="skills/shared/data/design-principles.csv"` for principle backing on composition decisions.

**L3 delegation:** If maturity is L3, delegate to **ds-consumer Workflow 3 (Component Selection)**. Use this sub-agent for exploration at L0/L1/L2.

### Ask first

1. What UI need are you trying to address? (one sentence — describe the user action or content, not the component name)
2. What maturity level are we working at? (confirm from detection — L1 DESIGN.md, L2 DS library, L3 enterprise DS)
3. Any constraints — viewport, density, or accessibility requirements?

### Workflow

1. **Understand the need**: Parse the user's described action/content. Do not anchor on a component name yet — stay problem-first.
2. **Map to component hierarchy**: Using `component-patterns.md`, determine what level is needed: Primitive, Component, Pattern, or Template.
3. **At L1**: Identify relevant primitives from DESIGN.md (colors, type roles, spacing tokens) that can compose the need. Describe the composition without naming DS components.
4. **At L2/L3**: Search available components for best fit. Evaluate on: purpose match, variant coverage, state support, composition flexibility.
5. **Rank options**: If multiple components could work, present a ranked table with rationale. Recommend one primary fit.
6. **Check for override temptation**: If the best-fit component requires an override to work, that is a gap — route to Gap Detector instead of recommending the override.
7. **Output** the recommendation with key variant to use and configuration note.

### Output format

```
## Component Recommendation — <Need Description>

**Best fit:** <ComponentName> — <one-line rationale>
**Variant to use:** <variant name and key props>
**State coverage:** <which states are handled>

### Alternatives Considered
| Component | Fit | Why not primary |
|-----------|-----|----------------|
...

### Notes
<Any composition or configuration caveats>
```

If no fit exists: "No suitable component found. Routing to Gap Detector."

---

## Sub-Agent: Layout Composer

**Load additionally:** `skills/shared/knowledge/layout.md`

**Optional L3 query:** `Grep pattern="navigation\|page\|grid" path="skills/shared/data/usability-homepage.csv"` for layout usability anchors relevant to the page type.

**L3 delegation:** If maturity is L3, delegate to **ds-consumer Workflow 1 (Design a New Feature/Page)**. Use this sub-agent for layout planning at L0/L1/L2.

### Ask first

1. What is the page or flow? (name + primary user goal in one sentence)
2. What primary content type dominates — data-dense (tables, lists), form-heavy, content/reading, or dashboard?
3. Desktop-first or mobile-first? Any fixed viewport constraints?

### Workflow

1. **Inventory the DS** (L2/L3): Identify layout tokens available — grid columns, spacing scale, breakpoints — from `.ds-context.md` or DESIGN.md at L1. Do not invent values not present in the design language.
2. **Propose structure**: Select the primary composition pattern from `layout.md` (sidebar+main, card grid, list-detail, split-view, master-detail) based on content type. Justify the choice.
3. **Map components to zones**: For each layout zone (nav, header, content, sidebar, footer), identify which DS components (or DESIGN.md primitives at L1) populate it. Flag any zone where no component fits.
4. **Evaluate against ux-heuristics**: Apply `ux-heuristics.md` checks to the proposed structure:
   - Visibility of system status (does the layout surface state?)
   - Match between system and real world (mental model alignment)
   - Recognition over recall (is navigation predictable?)
   - Aesthetic and minimalist design (no surplus layout regions)
   Flag any heuristic violations as P1 or P2 findings.
5. **Refine**: Adjust based on heuristic findings. Offer 1–2 alternative structures if the primary has significant P1 issues.
6. **Check responsive behavior**: Define how the layout adapts at key breakpoints from the spacing/grid system.
7. Output the layout spec.

### Output format

```
## Layout Proposal — <Page/Flow Name>

**Pattern:** <Composition pattern name>
**Grid:** <columns, gutter, margin>
**Density:** <compact / default / comfortable>

### Zone Map
| Zone | Component(s) / Primitives | Notes |
|------|--------------------------|-------|
...

### Responsive Behavior
| Breakpoint | Layout change |
|------------|--------------|
...

### Heuristic Findings
| Heuristic | Finding | Severity | Adjustment |
|-----------|---------|----------|-----------|
...
```

Offer to pass to Gap Detector if any zone lacks a component fit.

---

## Sub-Agent: Pattern Matcher

**Load additionally:** None — `component-patterns.md` covers composition hierarchy including Patterns and Templates.

**Optional L3 query:** `Grep pattern="<flow type>" path="skills/shared/data/ecommerce-usability.csv"` or `usability-homepage.csv` for domain-specific pattern precedent.

**L3 delegation:** If maturity is L3, consult **ds-consumer Workflow 1 step "Inventory"** for DS patterns (from `{{figma.libraries[role=patterns]}}`) and squad patterns lookup via the configured Figma adapter.

### Ask first

1. What is the user trying to accomplish? (describe the task or flow, not the UI element)
2. Is this in the context of an existing product area, or a new surface?
3. At L2/L3: should we search the DS library for existing patterns, or are you already certain none exist?

### Workflow

1. **Abstract the need**: Strip the request to its interaction primitive — form submission, item selection, bulk action, data exploration, wizard progression, etc.
2. **Search for an exact pattern match**: At L2/L3, use Figma MCP (`use_figma`) to inspect Patterns and Squad Patterns files for this interaction type. At L1, scan DESIGN.md for documented composition guidance.
3. **Search for a partial match**: If no exact pattern exists, find the closest analog. Describe what matches and what diverges.
4. **Assess the gap**: Is the divergence handleable by variant selection (no gap), by composition (no gap), or does it require a new component (gap)?
5. **Recommend**: If a pattern exists → name it + provide usage guidance. If a near-match → describe adaptation using existing components. If no match → route to Gap Detector.
6. **Verify no anti-pattern**: Check that the recommended pattern doesn't trigger any hard rules (override required, detach required). If it does, treat as a gap.

### Output format

```
## Pattern Search — <Need Description>

**Result:** Exact match / Near match / No match

### Match Details
**Pattern name:** <name or "none">
**Source:** <DS Patterns / Squad Patterns / DESIGN.md / Not found>
**Fits because:** <rationale>
**Diverges at:** <what the pattern doesn't cover, if near match>

### Recommendation
<Use as-is / Adapt with these components / Route to Gap Detector>
```

---

## Sub-Agent: Gap Detector

**Load additionally:** `skills/shared/knowledge/governance.md`

**Optional L3 query:** Not applicable — gap requests follow governance process, not CSV lookups.

**L3 delegation:** If maturity is L3, delegate to **ds-consumer Workflow 4 (Component Gap Request)**. Use this sub-agent to draft and plan gap requests at L0/L1/L2.

### Ask first

1. What were you trying to accomplish? (the original design need)
2. What did you try? (which components or patterns were considered and why they didn't fit)
3. How urgent is this — blocking a release, or for a future sprint?

### Workflow

1. **Confirm exhaustive search**: Verify that Component Selector and Pattern Matcher were run first. If not, run them before declaring a gap. A gap is only confirmed when no existing component or pattern can address the need (even with valid composition).
2. **Document the gap precisely**: What is the need? What component or behavior is missing? Which product area and user flow does it affect?
3. **Check governance rules** from `governance.md`: Is this a new component request, or an update to an existing one? Separate requests are tracked differently.
4. **Draft the gap request** in structured format (see output below).
5. **Present to user for approval**: The designer reviews and approves before any submission. Never submit without sign-off.
6. **At L2**: Advise on submitting to the DS team via the contribution process from `governance.md`.
7. **At L3**: Route to ds-consumer Workflow 4. Output the approved request in ds-consumer's required format.
8. **Flag interim workaround** (if acceptable): Can the design proceed temporarily with a near-fit component? Only suggest this if it requires zero overrides and zero detaching.

### Output format

```
## Gap Request — <Need Description>

**Type:** New component / Update to existing component
**Affected area:** <product area or flow>
**Priority:** <Blocking / High / Medium>

### Need Description
<What the design requires — user action, content type, behavior>

### Alternatives Attempted
| Component/Pattern | Why it doesn't fit |
|-------------------|-------------------|
...

### Proposed Solution
<Brief description of what a new or updated component would look like>

### Interim Workaround
<Near-fit composition with zero overrides, OR "none — must block on DS delivery">

### Next Step
<Submit to DS team via governance process / Route to ds-consumer Workflow 4 at L3>
```

Remind user: "This request requires your explicit approval before submission."
