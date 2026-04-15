---
name: map-design
description: Use to extract design language from an existing artifact (screenshot, URL, Figma file, or codebase) and generate a DESIGN.md. Activates for /map-design, "extract tokens", "generate DESIGN.md", "crawl this design", "document design language", "what tokens does this use", "reverse-engineer this UI", "create a DESIGN.md from this".
---

# /map-design — Design Extraction

Router for design extraction sub-agents. Crawls existing designs — screenshots, Figma files, or running apps — and produces a structured `DESIGN.md` at the project root.

## Maturity Detection

Follow `${CLAUDE_PLUGIN_ROOT}/skills/shared/maturity-detection.md`. Run detection before routing.

- **L0 (Greenfield):** Primary use case. Extract from reference artifacts or screenshots to bootstrap a `DESIGN.md` from scratch. No constraints — extract freely.
- **L1 (DESIGN.md exists):** Enrich mode. Read the existing `DESIGN.md` first, then extract from the new artifact, and propose additions or corrections to each section.
- **L2 (DS exists):** Refresh mode. Extract a snapshot of the current DS state from the DS library (via Figma MCP) to update `DESIGN.md` to reflect the current truth.
- **L3 (Enterprise DS):** Limited. The enterprise DS already maintains a full design language; `/map-design` here is scoped to specific sections (e.g., regenerating the Agent Prompt Guide, or documenting a new squad library).

Always announce the detected level before routing.

## Always Load

- `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/core-principles.md` (L1 — always)
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/design-md-schema.md` (L2 — DESIGN.md structure and field guide)

## Execution Chain

When running the full extraction flow, sub-agents execute sequentially — each feeding its output to the next:

```
Visual Parser → Token Extractor → Component Cataloger → DESIGN.md Generator
```

Each step's output is passed as context to the following step. The chain terminates with a confirmed write to `DESIGN.md`.

Users may also invoke a single sub-agent directly:
- "Just extract the tokens from this screenshot" → Token Extractor only
- "List the components in this Figma file" → Component Cataloger only
- "Parse what's on this screen" → Visual Parser only

## Sub-Agent Router

| Trigger | Sub-Agent |
|---------|-----------|
| "parse", "what's in this", "identify", "what do I see", "read this design" | Visual Parser |
| "tokens", "colors", "typography", "spacing", "extract values", "what tokens" | Token Extractor |
| "components", "catalog", "inventory", "list patterns", "what components" | Component Cataloger |
| "generate DESIGN.md", "write design.md", "create design.md", "full extraction" | Full chain (Visual Parser → Token Extractor → Component Cataloger → DESIGN.md Generator) |

If the user provides an artifact and asks for a `DESIGN.md`, run the full chain automatically. Confirm the chain order before starting.

---

## Sub-Agent: Visual Parser

**Load additionally:** `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/visual-quality.md`

**Optional L3 query:** Not applicable at this stage — this is an observational pass.

### Ask first

1. What is the source artifact? (screenshot file path, Figma file URL, or live URL to screenshot)
2. Is this a single screen, a multi-screen flow, or a component library?
3. Any areas to exclude from parsing? (e.g., placeholder content, dev scaffolding)

### Workflow

1. **Obtain the artifact**:
   - Screenshot / image file: Use Read tool on the file path.
   - Figma file or node: Use `use_figma(fileKey)` to fetch the document tree. Request specific pages or frames, not the full file.
   - Live URL: Request a screenshot of the URL via available browser tool.
2. **Identify all visible elements**: Enumerate every distinct visual element on screen. Do not interpret purpose yet — observe first.
3. **Tag by category**:
   - **Content**: Text (headings, body, labels, captions), images, icons, data values
   - **Chrome**: Navigation bars, headers, footers, sidebars, toolbars, modals, drawers
   - **Action**: Buttons, links, form inputs, toggles, checkboxes, selects, sliders
   - **Feedback**: Status indicators, badges, alerts, tooltips, loading states, empty states
   - **Layout**: Grid containers, card wrappers, dividers, spacer regions
4. **Note visual hierarchy signals**: What appears most prominent (size, weight, color emphasis)? What is secondary? What is tertiary?
5. **Identify repeating patterns**: Note any element that appears 3+ times in the same structural form — these are component candidates.
6. **Flag ambiguities**: Elements that are unclear or partially visible — note them but do not interpret.
7. Output a tagged element inventory. This becomes the input for Token Extractor and Component Cataloger.

### Output format

```
## Visual Parse — <Artifact Name>

**Source type:** Screenshot / Figma file / Live URL
**Scope:** Single screen / Multi-screen flow / Component library

### Element Inventory

#### Content
- <element description> — location: <zone>
...

#### Chrome
- <element description> — location: <zone>
...

#### Action
- <element description> — location: <zone>
...

#### Feedback
- <element description> — location: <zone>
...

#### Layout
- <element description> — location: <zone>
...

### Visual Hierarchy
Primary: <most prominent element(s)>
Secondary: <supporting elements>
Tertiary: <background/structural elements>

### Repeating Patterns
- <pattern description> — appears <N> times — component candidate: Yes/Maybe/No

### Ambiguities
<list any unclear elements>
```

Pass this output to Token Extractor.

---

## Sub-Agent: Token Extractor

**Load additionally:**
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/token-architecture.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/color-theory.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/typography.md`

**Optional L3 query:** `Grep pattern="token\|variable\|naming" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/design-principles.csv"` for naming convention backing.

### Ask first

1. Should I extract all token categories (color, typography, spacing, radius, effects), or focus on specific ones?
2. For color extraction from images: should I quantize to a palette, or identify precise values from Figma?

### Workflow

1. **Receive Visual Parser output** (or re-read the artifact if running standalone).
2. **Color extraction**:
   - From Figma: Use `use_figma` to read fill and stroke values from nodes. Collect unique color values.
   - From image/screenshot: Quantize the image to identify dominant colors (10–20 representative samples). Group by apparent role (background, surface, text, accent, semantic).
   - Map observed colors to a **3-tier structure** from `token-architecture.md`: which are primitives (raw hues), which function as semantic tokens (purpose-bound), which appear scoped to a specific component.
   - Check for color scale completeness using `color-theory.md` — does an 11-step neutral exist? A brand scale? Semantic colors (success/warning/error/info)?
3. **Typography extraction**:
   - Identify all distinct font family + weight combinations in use.
   - Collect font size values. Sort ascending. Identify the scale pattern — is it modular (consistent ratio) or ad-hoc? Reference `typography.md` scale ratios (1.125, 1.2, 1.25, 1.333) for identification.
   - Note line heights and letter spacing per size if determinable.
   - Map to semantic roles: which size = body, which = heading-sm, heading-md, etc.?
4. **Spacing extraction**:
   - Measure padding, margin, and gap values from the artifact (from Figma: auto-layout gap/padding values; from image: visual estimation).
   - Identify the base unit (4px or 8px grid?) by looking for the smallest consistent gap.
   - Map to a t-shirt scale: `xs`, `sm`, `md`, `lg`, `xl`, `2xl`.
5. **Radius extraction**: Collect all border-radius values in use. Flag inconsistencies (too many distinct values signal no token system).
6. **Effects extraction**: Collect shadow values if visible (offset-x, offset-y, blur, spread, color).
7. **Propose 3-tier token structure**: Based on findings, draft a minimal token architecture:
   - Primitive tier: raw values
   - Semantic tier: purpose bindings
   - Component tier: scoped tokens (if identifiable)
8. Flag anti-patterns from `token-architecture.md`: direct primitive-to-component bindings, magic numbers with no pattern, more than one base unit competing.

### Output format

```
## Token Extraction — <Artifact Name>

### Color
**Base unit:** — (N/A for color)
**Primitive colors identified:**
| Value | Approximate role |
|-------|----------------|
...

**Proposed semantic bindings:**
| Semantic Token | Value | Dark mode counterpart |
|---------------|-------|----------------------|
...

### Typography
**Font families:** <list>
**Scale pattern:** Modular (ratio: ~X.XX) / Ad-hoc
| Size | px | rem | Apparent role |
|------|----|-----|--------------|
...
**Line heights detected:** <list>

### Spacing
**Base unit:** <4px / 8px / unknown>
| Token | Value (px) | Frequency |
|-------|-----------|-----------|
...

### Radius
| Value | Frequency | Apparent scope |
|-------|-----------|---------------|
...

### Effects / Shadows
| Value | Apparent purpose |
|-------|----------------|
...

### Anti-patterns detected
<list any token anti-patterns found>
```

Pass this output to Component Cataloger.

---

## Sub-Agent: Component Cataloger

**Load additionally:** `${CLAUDE_PLUGIN_ROOT}/skills/shared/knowledge/component-patterns.md`

**Optional L3 query:** `Grep pattern="<component keyword>" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/design-principles.csv"` for composition or hierarchy principle anchors.

### Ask first

1. Should I catalog all components, or focus on a specific category (e.g., form elements, navigation, data display)?
2. Should I infer variants, or only identify base patterns?

### Workflow

1. **Receive Visual Parser output** (or re-read the artifact if running standalone). Review the "Repeating Patterns" section for component candidates already flagged.
2. **Identify components**: For each distinct UI pattern that appears with its own visual identity, treat it as a component candidate.
3. **Apply hierarchy from `component-patterns.md`**:
   - **Primitive**: Atomic — button, input, badge, icon, avatar, divider
   - **Component**: Assembled — card, form group, dropdown, tooltip, modal header
   - **Pattern**: Multi-component compositions — search bar with filters, data table with pagination, form wizard
   - **Template**: Full page compositions — list+detail layout, dashboard, settings page
4. **Label each component**: Assign a descriptive name. Describe its purpose in one sentence.
5. **Detect variants**: Look for the same component in different states or configurations. List the variant dimensions observed (size, intent/color, layout, state).
6. **Detect hierarchy**: Does Component A contain Component B? Map containment relationships where clear.
7. **Assess completeness**: Are all expected states present for each component? (default, hover, focus, disabled, loading, error, empty — as applicable). Flag missing states.
8. **Flag ambiguous cases**: Components that are unclear, one-off, or may actually be overridden DS components — note these separately.

### Output format

```
## Component Catalog — <Artifact Name>

### Primitives
| Name | Purpose | Variants observed | States observed |
|------|---------|------------------|----------------|
...

### Components
| Name | Purpose | Contains | Variants observed | States observed |
|------|---------|----------|------------------|----------------|
...

### Patterns
| Name | Purpose | Components used | Notes |
|------|---------|----------------|-------|
...

### Templates
| Name | Purpose | Patterns/Components used |
|------|---------|------------------------|
...

### Missing States
| Component | Missing state | Priority |
|-----------|--------------|---------|
...

### Ambiguous / One-off Elements
<list elements that don't clearly fit a reusable component>
```

Pass this output to DESIGN.md Generator.

---

## Sub-Agent: DESIGN.md Generator

**Load additionally:** None — `design-md-schema.md` is already loaded via Always Load.

**Optional L3 query:** Not applicable — this step synthesizes prior outputs into structured prose.

### Ask first

No questions before generating. This sub-agent synthesizes the outputs of the prior three sub-agents. If running standalone, ask: "Please provide the Visual Parser, Token Extractor, and Component Cataloger outputs, or the artifact to extract from."

### Workflow

1. **Collect inputs**: Gather outputs from Visual Parser, Token Extractor, and Component Cataloger. If any are missing, note gaps in the corresponding DESIGN.md section rather than fabricating content.
2. **At L1 (enrich mode)**: Read the existing `DESIGN.md` first. For each section, determine: confirm existing content, update with new findings, or add net-new information. Do not remove content unless it is factually contradicted.
3. **Fill all 9 sections** per `design-md-schema.md`:
   - **Section 1 — Visual Theme**: Synthesize from Visual Parser's hierarchy notes and Token Extractor's color tone. Draft a mood statement (3 adjectives + noun). Note apparent reference influences.
   - **Section 2 — Color Palette**: Use Token Extractor's color output. Fill primitive scale, semantic bindings, and dark mode counterparts where identified.
   - **Section 3 — Typography**: Use Token Extractor's typography output. Font families, type scale table, role mapping.
   - **Section 4 — Components**: Use Component Cataloger's catalog. List each component with purpose and key variants.
   - **Section 5 — Layout**: Use Token Extractor's spacing output + Visual Parser's layout zone observations. Grid type, base unit, spacing scale, breakpoints if determinable.
   - **Section 6 — Depth**: Use Token Extractor's effects/shadows. Elevation levels if identifiable, layering rules (what appears on top of what).
   - **Section 7 — Do's and Don'ts**: Derive from anti-patterns flagged in Token Extractor and Component Cataloger. Aim for 5 Do's and 5 Don'ts specific to this design language.
   - **Section 8 — Responsive**: Note any breakpoint-specific behaviors observed. If none determinable from the artifact, note: "Responsive behavior not observed — define before handoff."
   - **Section 9 — Agent Prompt Guide**: Write 3–5 invariants that an AI agent should preserve when working with this design language. Examples: "Always use the 8px base unit", "Never use raw hex values — reference semantic tokens only", "Heading hierarchy: H1 > H2 only; never skip levels".
4. **Confirm before writing**: Present the complete DESIGN.md draft to the user. State: "Ready to write DESIGN.md to the project root. Confirm to proceed."
5. **Write only after confirmation**: Use Write tool to create or overwrite `DESIGN.md` at project root.
6. **Announce maturity change**: If this is L0 → writing first DESIGN.md, announce: "DESIGN.md created. Project maturity is now L1. /design and /ds-make can now use this as their source of truth."

### Output format

Present the full DESIGN.md draft in a code block for review before writing:

````
```markdown
# <Project Name> Design Language

## Visual Theme
<mood statement — 3 adjectives + noun>
<2–3 sentences on the feeling and reference influences>

## Color Palette
### Neutrals
| Token | Value | Role |
...

### Brand / Primary
...

### Semantic
| Role | Light | Dark |
...

## Typography
**Families:** <primary font> + <secondary/body font>
**Scale ratio:** ~X.XX (or "ad-hoc")

| Token | Size | rem | Role | Line Height |
...

## Components
| Component | Hierarchy | Purpose | Key Variants |
...

## Layout
**Grid:** <type, columns>
**Base unit:** <4px / 8px>
**Spacing scale:** xs=Xpx, sm=Xpx, md=Xpx, lg=Xpx, xl=Xpx

## Depth
| Level | Shadow value | Used for |
...

## Do's and Don'ts
### Do
- ...

### Don't
- ...

## Responsive
<Breakpoint strategy and key adaptations>

## Agent Prompt Guide
- <Invariant 1>
- <Invariant 2>
- ...
```
````

After user confirmation, write the file and confirm: "DESIGN.md written to project root."
