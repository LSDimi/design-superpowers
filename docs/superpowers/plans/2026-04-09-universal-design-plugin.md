# Universal Design Plugin Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a universal Claude Code design plugin with 6 commands (`/creative`, `/ds-make`, `/ds-manage`, `/design`, `/design-review`, `/map-design`), ~20 sub-agents, and a 4-layer knowledge system that adapts across 4 project maturity levels.

**Architecture:** Each command is a single SKILL.md acting as a router to inline sub-agent sections. Knowledge is split into 4 layers: L1 core principles (always loaded), L2 domain reference files (loaded per sub-agent), L3 CSV lookups (queried on demand), L4 project context (persisted DESIGN.md / .ds-context.md). Existing ds-producer and ds-consumer skills become L3 (Enterprise/Tone) specializations referenced by /ds-make and /design.

**Tech Stack:** Markdown (SKILL.md format), CSV data files, YAML frontmatter, Claude Skill tool, Figma MCP (`use_figma`), Read/Grep/Glob tools. No compiled code.

**Spec:** `docs/superpowers/specs/2026-04-09-universal-design-plugin-design.md`

**Constraints:**
- **Token-sensitive:** L1 must stay under 2K tokens. L2 files target 1-3K tokens each. L3 CSVs never pre-loaded.
- **DRY:** Cross-reference, never duplicate. All sub-agents reference shared/knowledge/*.md via relative paths.
- **YAGNI:** Do not author content for sub-agents beyond what the 4 curated source CSVs provide. No speculative frameworks.
- **Validation:** After each knowledge file, verify token count with `wc -w` (rough: words × 1.3 ≈ tokens).

---

## File Structure

### Created in this plan
```
skills/shared/knowledge/
├── core-principles.md              # L1 (~2K tokens, always loaded)
├── creative-direction.md           # L2
├── color-theory.md                 # L2
├── typography.md                   # L2
├── layout.md                       # L2
├── token-architecture.md           # L2
├── component-patterns.md           # L2
├── governance.md                   # L2 (extracts from existing design-principles.md)
├── ux-heuristics.md                # L2
├── accessibility.md                # L2
├── motion.md                       # L2
├── visual-quality.md               # L2
├── documentation.md                # L2
└── design-md-schema.md             # L2

skills/shared/data/                 # L3 (curated from src/data/)
├── psychological-principles.csv
├── usability-homepage.csv
├── ecommerce-usability.csv
└── design-principles.csv

skills/shared/
├── maturity-detection.md           # Shared helper: how to detect L0-L3

skills/creative/SKILL.md            # /creative router + 4 sub-agents
skills/ds-make/SKILL.md             # /ds-make router + 4 sub-agents (+ L3 delegation to ds-producer)
skills/ds-manage/SKILL.md           # /ds-manage router + 4 sub-agents
skills/design/SKILL.md              # /design router + 4 sub-agents (+ L3 delegation to ds-consumer)
skills/design-review/SKILL.md       # /design-review router + 5 sub-agents
skills/map-design/SKILL.md          # /map-design router + 4 sub-agents
```

### Modified in this plan
```
skills/shared/design-principles.md  # Slimmed; content moved to knowledge/governance.md
skills/shared/tone-ds-context.md    # Add .ds-context.md reference
skills/ds-producer/SKILL.md         # Add L3 delegation header (referenced by /ds-make)
skills/ds-consumer/SKILL.md         # Add L3 delegation header (referenced by /design)
```

### Untouched (existing)
```
src/data/*.csv                      # Raw source — preserved, not moved
tools/tone-lint-agent/*             # Existing agent scripts
```

---

## Conventions

- **Token budgets** listed per file. Verify with: `wc -w <file>` — multiply by 1.3 for rough token estimate.
- **SKILL.md frontmatter** always includes `name` and `description`. The description controls when Claude activates the skill, so it must be precise and trigger-worthy.
- **Sub-agent sections** are delimited with `## Sub-Agent: <Name>` headings inside each command SKILL.md.
- **Knowledge references** use relative paths: `skills/shared/knowledge/<file>.md`.
- **Every sub-agent section** must declare: (1) activation triggers, (2) required L1+L2 knowledge, (3) optional L3 queries, (4) workflow steps, (5) output format.
- **Commits:** One per chunk. Commit message format: `feat(skills): <chunk-summary>`.

---

## Chunk 1: Knowledge Layer Foundations (L1 + core L2 files)

Build the shared knowledge substrate first. Every downstream sub-agent depends on this.

### Task 1.1: Extract and curate L1 core principles

**Files:**
- Create: `skills/shared/knowledge/core-principles.md`
- Source: `src/data/Design Principles, Performance Attributes, and Strategy Tenets Reference Table - Table 1.csv`

- [ ] **Step 1: Read the source CSV**

Use Read tool on the 53-row design principles CSV. Identify columns: Principle, Main Characteristics, Do's, Don'ts, Other Characteristics, Severity.

- [ ] **Step 2: Filter to universal principles**

Keep only principles that apply regardless of domain (design system, product design, creative, review). Target ~50 rows. Drop: domain-specific SOLID programming principles, anything requiring software context. Keep: Dieter Rams (all 10), Universal Design (all 7), UX Strategy tenets, motion principles, accessibility universals.

- [ ] **Step 3: Write core-principles.md**

Structure:
```markdown
# Core Design Principles (L1 — Always Loaded)

> Compact reference loaded into every sub-agent. Total budget: ~2K tokens.

## How to use
When making any design decision, recall these principles. They are the floor, not the ceiling. Domain-specific knowledge (L2) extends these.

## Principles

### 1. <Principle Name>
**Do:** <one line>
**Don't:** <one line>
**Severity:** <Critical|High|Medium>

### 2. ...
```

Keep each entry to 3 lines maximum. No "Other Characteristics" column. No narrative padding.

- [ ] **Step 4: Verify token budget**

Run: `wc -w "skills/shared/knowledge/core-principles.md"`
Expected: ≤1500 words (≈2K tokens). If over budget, drop lowest-severity entries.

- [ ] **Step 5: Commit**

```bash
git add skills/shared/knowledge/core-principles.md
git commit -m "feat(skills): add L1 core principles knowledge file"
```

---

### Task 1.2: Create maturity detection helper

**Files:**
- Create: `skills/shared/maturity-detection.md`

- [ ] **Step 1: Write the maturity detection logic**

Content structure:
```markdown
# Maturity Level Detection

> Shared helper referenced by every command SKILL.md. Detects which of 4 project maturity levels applies.

## Levels

| Level | Name | Signals |
|-------|------|---------|
| L0 | Greenfield | No DESIGN.md, no .ds-context.md, no Figma library keys in repo |
| L1 | Design Language Defined | DESIGN.md exists, no DS library |
| L2 | Has Design System | .ds-context.md exists with Figma library keys |
| L3 | Enterprise DS | .ds-context.md names Tone OR matches known enterprise pattern |

## Detection Workflow

1. Check for `DESIGN.md` at project root (Glob: `DESIGN.md`)
2. Check for `.ds-context.md` at project root (Glob: `.ds-context.md`)
3. If .ds-context.md exists, Read it and look for `enterprise: true` or `name: Tone`
4. Return the highest matched level

## Behavior Adaptation

| Level | /creative | /ds-make | /design | /design-review |
|-------|-----------|----------|---------|----------------|
| L0 | Full freedom, generate DESIGN.md | Scaffold new DS from scratch | Block — need design language first | Heuristics only |
| L1 | Refine DESIGN.md | Scaffold DS from DESIGN.md | Compose from DESIGN.md tokens | Heuristics + DESIGN.md checks |
| L2 | Refine within DS constraints | Extend existing DS | Compose from DS components | Full DS compliance |
| L3 | Tone-aware | Delegate to ds-producer | Delegate to ds-consumer | Full Tone governance |

## Telling the user

Always announce the detected level at the start: "Detected maturity level: L2 (project has DS). Adapting behavior accordingly."
```

- [ ] **Step 2: Commit**

```bash
git add skills/shared/maturity-detection.md
git commit -m "feat(skills): add maturity level detection helper"
```

---

### Task 1.3: Author governance.md (extract from existing design-principles.md)

**Files:**
- Create: `skills/shared/knowledge/governance.md`
- Modify: `skills/shared/design-principles.md` (to slim down after extraction)

- [ ] **Step 1: Read existing design-principles.md**

Read the file at `skills/shared/design-principles.md`. Identify sections: IA principles, anti-patterns, governance model, contribution process, versioning, deprecation, consumption rules, publishing cascade, checklist.

- [ ] **Step 2: Write knowledge/governance.md**

Move these sections verbatim (they are already well-formed):
- Governance model (decision-making)
- Contribution process
- Versioning (semver rules)
- Deprecation workflow
- Consumption rules
- Publishing cascade
- Checklist

Header:
```markdown
# Design System Governance (L2)

> Loaded by /ds-make, /ds-manage, /design-review sub-agents. Covers contribution, versioning, deprecation, publishing cascade, and consumption rules.
```

Token budget: ~3K tokens (this is a dense reference; budget is generous).

- [ ] **Step 3: Slim down design-principles.md**

Leave only: IA principles and anti-patterns table (these are design heuristics, not governance). Add a header pointer: `> Governance content moved to knowledge/governance.md`. Keep the file for backward compatibility with existing ds-producer/ds-consumer references until Chunk 3 updates those.

- [ ] **Step 4: Verify no broken references**

Run: `Grep pattern="design-principles.md" path="skills/"`
Expected: ds-producer/SKILL.md and ds-consumer/SKILL.md still reference it. Leave as-is until Chunk 3.

- [ ] **Step 5: Commit**

```bash
git add skills/shared/knowledge/governance.md skills/shared/design-principles.md
git commit -m "feat(skills): extract governance into L2 knowledge file"
```

---

### Task 1.4: Author component-patterns.md

**Files:**
- Create: `skills/shared/knowledge/component-patterns.md`

- [ ] **Step 1: Write the file**

Content covers:
- **Component API design:** Props vs variants decision tree, slot patterns, compound components
- **Variant strategies:** Boolean props, enum props, when to split into separate components
- **Composition patterns:** Composition over configuration, slot injection, controlled/uncontrolled
- **Naming conventions:** Component names (PascalCase, noun-based), prop names (camelCase, action verbs for handlers)
- **Responsiveness:** Fluid vs. fixed, breakpoint strategy
- **State patterns:** Default, hover, focus, pressed, disabled, loading, error, empty
- **Composition hierarchy:** Primitives → Components → Patterns → Templates

Token budget: ~2K tokens. Header: `# Component Patterns (L2)` with load-directive comment.

- [ ] **Step 2: Commit**

```bash
git add skills/shared/knowledge/component-patterns.md
git commit -m "feat(skills): add component-patterns L2 knowledge"
```

---

### Task 1.5: Author token-architecture.md

**Files:**
- Create: `skills/shared/knowledge/token-architecture.md`

- [ ] **Step 1: Write the file**

Content covers:
- **3-tier model:** Primitive → Semantic → Component (with examples)
- **Naming convention:** `<category>.<property>.<role>.<state>.<size>` with real examples
- **Collection structure:** How to group tokens (color, spacing, typography, radius, effects)
- **Dark mode strategy:** Semantic tokens swap values, primitives stay stable
- **Anti-patterns:** Tying primitives to components, bypassing semantic layer, magic numbers
- **Extraction heuristics:** Given a design, how to identify what should be a token

Reference `skills/shared/tone-ds-context.md` as the canonical Tone example but keep content universal.

Token budget: ~2K tokens.

- [ ] **Step 2: Commit**

```bash
git add skills/shared/knowledge/token-architecture.md
git commit -m "feat(skills): add token-architecture L2 knowledge"
```

---

### Task 1.6: Author ux-heuristics.md

**Files:**
- Create: `skills/shared/knowledge/ux-heuristics.md`

- [ ] **Step 1: Write the file**

Content:
- **Nielsen's 10 heuristics** — each with one-line definition, one Do, one Don't, severity guidance
- **Cognitive load framework** — intrinsic, extraneous, germane load, how to measure
- **IA principles** — discoverability, findability, scanability, predictability
- **Severity rubric** — P0 (blocker), P1 (major), P2 (minor), P3 (cosmetic)
- **Evaluation output format** — finding table: (Heuristic, Location, Issue, Severity, Suggestion)

Token budget: ~2K tokens.

- [ ] **Step 2: Commit**

```bash
git add skills/shared/knowledge/ux-heuristics.md
git commit -m "feat(skills): add ux-heuristics L2 knowledge"
```

---

### Task 1.7: Author accessibility.md

**Files:**
- Create: `skills/shared/knowledge/accessibility.md`

- [ ] **Step 1: Write the file**

Content:
- **WCAG 2.1 AA checklist** — grouped by Perceivable, Operable, Understandable, Robust
- **Keyboard patterns** — focus order, focus traps, skip links, visible focus
- **ARIA patterns** — when to use, landmarks, live regions, labels vs descriptions
- **Contrast ratios** — 4.5:1 text, 3:1 UI, 7:1 enhanced; tools to verify
- **Screen reader patterns** — semantic HTML first, ARIA as fallback
- **Motion/animation a11y** — prefers-reduced-motion, no flashing
- **Output format** — finding table: (WCAG criterion, Location, Issue, Severity, Fix)

Token budget: ~2.5K tokens.

- [ ] **Step 2: Commit**

```bash
git add skills/shared/knowledge/accessibility.md
git commit -m "feat(skills): add accessibility L2 knowledge"
```

---

## Chunk 2: Knowledge Layer — Specialized Domains

Remaining L2 files for creative, visual, motion, and documentation domains.

### Task 2.1: Author creative-direction.md

**Files:**
- Create: `skills/shared/knowledge/creative-direction.md`

- [ ] **Step 1: Write the file**

Content:
- **Configurable dials** — creativity (safe→bold), density (airy→packed), variance (uniform→playful), motion (static→kinetic); how to interpret user settings
- **Moodboard method** — identify 5-7 reference sources, extract 3-5 traits each, synthesize into theme statement
- **Theme statement template** — `<adjective> + <adjective> + <noun>` (e.g., "precise, confident, utilitarian")
- **Translation to tokens** — how a theme becomes color palette, type scale, spacing rhythm
- **Anti-patterns** — mixing references without synthesis, skipping theme statement, overfitting to one reference

Token budget: ~1.5K tokens.

- [ ] **Step 2: Commit**

```bash
git add skills/shared/knowledge/creative-direction.md
git commit -m "feat(skills): add creative-direction L2 knowledge"
```

---

### Task 2.2: Author color-theory.md

**Files:**
- Create: `skills/shared/knowledge/color-theory.md`

- [ ] **Step 1: Write the file**

Content:
- **Palette structure** — neutral scale (11 steps), brand/primary scale, semantic colors (success/warning/error/info)
- **Scale generation** — OKLCH preferred, HSL fallback; lightness step rules
- **Contrast validation** — WCAG ratios, how to verify per pair
- **Dark mode** — invert lightness, preserve hue, adjust saturation
- **Color semantics** — cultural considerations, colorblind safety
- **Anti-patterns** — hue-only scales, arbitrary lightness jumps, missing semantic roles

Token budget: ~1.5K tokens.

- [ ] **Step 2: Commit**

```bash
git add skills/shared/knowledge/color-theory.md
git commit -m "feat(skills): add color-theory L2 knowledge"
```

---

### Task 2.3: Author typography.md

**Files:**
- Create: `skills/shared/knowledge/typography.md`

- [ ] **Step 1: Write the file**

Content:
- **Type scale generation** — modular scale ratios (1.125, 1.2, 1.25, 1.333), base size, role mapping
- **Font pairing** — serif + sans, variable fonts, fallback stacks
- **Readability** — line length (45-75ch), line height (1.4-1.6 body, 1.1-1.3 headings), letter spacing
- **Hierarchy** — size + weight + color, never size alone
- **Responsive type** — fluid type with clamp(), breakpoint-based
- **Anti-patterns** — too many sizes (>7), weights below 400 for UI, decorative fonts for body

Token budget: ~1.5K tokens.

- [ ] **Step 2: Commit**

```bash
git add skills/shared/knowledge/typography.md
git commit -m "feat(skills): add typography L2 knowledge"
```

---

### Task 2.4: Author layout.md

**Files:**
- Create: `skills/shared/knowledge/layout.md`

- [ ] **Step 1: Write the file**

Content:
- **Grid systems** — 12-col, 8-col, fluid, CSS grid vs flexbox
- **Spacing rhythm** — 4px or 8px base unit, t-shirt sizing, inset/stack/inline patterns
- **Responsive breakpoints** — mobile-first, container queries, fluid gaps
- **Density modes** — compact/default/comfortable, how to parameterize
- **Composition patterns** — sidebar+main, split-view, card grid, list-detail, master-detail
- **Anti-patterns** — inconsistent spacing, misaligned edges, competing grids

Token budget: ~1.5K tokens.

- [ ] **Step 2: Commit**

```bash
git add skills/shared/knowledge/layout.md
git commit -m "feat(skills): add layout L2 knowledge"
```

---

### Task 2.5: Author motion.md

**Files:**
- Create: `skills/shared/knowledge/motion.md`

- [ ] **Step 1: Write the file**

Content:
- **Motion purpose** — feedback, continuity, spatial orientation, delight (in priority order)
- **Timing standards** — micro (100ms), small (200ms), medium (300ms), large (500ms)
- **Easing** — ease-out for enter, ease-in for exit, ease-in-out for position, spring for natural
- **Physics** — mass, tension, friction; when to use spring vs. duration
- **Performance** — transform + opacity only, avoid layout thrash, 60fps budget
- **Accessibility** — prefers-reduced-motion, no infinite loops, no seizure triggers
- **Anti-patterns** — decorative-only motion, long durations, bounce on every interaction

Token budget: ~1.5K tokens.

- [ ] **Step 2: Commit**

```bash
git add skills/shared/knowledge/motion.md
git commit -m "feat(skills): add motion L2 knowledge"
```

---

### Task 2.6: Author visual-quality.md

**Files:**
- Create: `skills/shared/knowledge/visual-quality.md`

- [ ] **Step 1: Write the file**

Content:
- **Alignment rules** — edges, centers, baseline grid
- **Spacing consistency** — use tokens, not ad-hoc values; measure gaps
- **Visual rhythm** — repeated patterns, consistent component density
- **Balance** — symmetry, asymmetry, weight distribution
- **Hierarchy verification** — squint test, 3-second test, grayscale test
- **Anti-patterns** — fake alignment (off by 1px), inconsistent border radii, mixed icon stroke widths
- **Inspection checklist** — what to look for when reviewing a screen

Token budget: ~1.5K tokens.

- [ ] **Step 2: Commit**

```bash
git add skills/shared/knowledge/visual-quality.md
git commit -m "feat(skills): add visual-quality L2 knowledge"
```

---

### Task 2.7: Author documentation.md

**Files:**
- Create: `skills/shared/knowledge/documentation.md`

- [ ] **Step 1: Write the file**

Content:
- **uSpec templates** — API spec, anatomy, component properties, color annotation, structure, screen reader, motion
- **Property table format** — name, type, default, description, example
- **Demo area structure** — overview, usage, variants, states, accessibility, do/don't examples
- **Documentation coverage checklist** — what every component needs
- **Anti-patterns** — undocumented props, missing "when to use", examples without context

Token budget: ~1.5K tokens.

- [ ] **Step 2: Commit**

```bash
git add skills/shared/knowledge/documentation.md
git commit -m "feat(skills): add documentation L2 knowledge"
```

---

### Task 2.8: Author design-md-schema.md

**Files:**
- Create: `skills/shared/knowledge/design-md-schema.md`

- [ ] **Step 1: Write the file**

Content: The 9-section DESIGN.md schema, with a template and field guide.

Structure:
```markdown
# DESIGN.md Schema (L2)

> Loaded by DESIGN.md Generator sub-agent. Based on awesome-design-md conventions.

## The 9 Sections

1. **Visual Theme** — mood statement, adjectives, reference influences
2. **Color Palette** — neutral + brand + semantic scales, with hex values
3. **Typography** — font families, type scale, role mapping
4. **Components** — catalog of components with purpose and key variants
5. **Layout** — grid, spacing system, breakpoints, density
6. **Depth** — elevation, shadows, layering rules
7. **Do's and Don'ts** — 5-10 bullets each, specific to this project
8. **Responsive** — breakpoint strategy, mobile/desktop adaptations
9. **Agent Prompt Guide** — how agents should use this file, invariants to preserve

## Template

\`\`\`markdown
# <Project Name> Design Language

## Visual Theme
<mood statement — 3 adjectives + noun>

## Color Palette
<...>

...
\`\`\`

## Field guide
<one paragraph per section explaining what goes in it and what to avoid>
```

Token budget: ~1.5K tokens.

- [ ] **Step 2: Commit**

```bash
git add skills/shared/knowledge/design-md-schema.md
git commit -m "feat(skills): add design-md-schema L2 knowledge"
```

---

## Chunk 3: L3 CSV Data Curation

Curate the four source CSVs into lean lookup files that sub-agents query on demand.

### Task 3.1: Curate design-principles.csv

**Files:**
- Create: `skills/shared/data/design-principles.csv`
- Source: `src/data/Design Principles, Performance Attributes, and Strategy Tenets Reference Table - Table 1.csv`

- [ ] **Step 1: Read source**

Read the full 53-row source CSV.

- [ ] **Step 2: Drop rows used in L1**

Any row that already made it into `core-principles.md` (Task 1.1) can be dropped OR kept (L3 is a deeper reference). Keep all 53 — L3 is the fuller reference, L1 is the subset. No curation needed, just copy.

- [ ] **Step 3: Write to destination**

Copy the file to `skills/shared/data/design-principles.csv`. Normalize column names to `principle,characteristics,dos,donts,category,severity` (lowercase, no spaces) for easier grep.

- [ ] **Step 4: Commit**

```bash
git add skills/shared/data/design-principles.csv
git commit -m "feat(skills): add curated design-principles L3 data"
```

---

### Task 3.2: Curate psychological-principles.csv

**Files:**
- Create: `skills/shared/data/psychological-principles.csv`
- Source: `src/data/100 Psychological Principles for Design Agents - Table 1.csv`

- [ ] **Step 1: Read source and inspect**

100 rows. Columns: Principle, Main Characteristics, Do's, Don'ts, Other Characteristics, Severity.

- [ ] **Step 2: Normalize column headers**

Rename to: `principle,characteristics,dos,donts,category,severity`. The "Other Characteristics" column contains mixed category + platform info — extract just the category (e.g., "How People See", "How People Think") and drop the platform notes.

- [ ] **Step 3: Drop duplicates and weak entries**

Scan for rows that duplicate design-principles.csv content. Drop any row where `severity` is "Low" or missing. Target: ~80 curated rows.

- [ ] **Step 4: Write the normalized CSV**

- [ ] **Step 5: Commit**

```bash
git add skills/shared/data/psychological-principles.csv
git commit -m "feat(skills): add curated psychological-principles L3 data"
```

---

### Task 3.3: Curate usability-homepage.csv

**Files:**
- Create: `skills/shared/data/usability-homepage.csv`
- Source: `src/data/79 Usability Guidelines for E-commerce Homepage and Category Navigation - Table 1.csv`

- [ ] **Step 1: Read source**

79 rows covering homepage, navigation, categories, filtering.

- [ ] **Step 2: Normalize headers**

Same 6 columns as Task 3.2. Category column should contain: "Homepage", "Navigation", "Categories", "Filtering".

- [ ] **Step 3: Filter and write**

Keep rows with severity "Critical" or "High". Drop low-severity. Target: ~60 rows.

- [ ] **Step 4: Commit**

```bash
git add skills/shared/data/usability-homepage.csv
git commit -m "feat(skills): add curated usability-homepage L3 data"
```

---

### Task 3.4: Curate ecommerce-usability.csv

**Files:**
- Create: `skills/shared/data/ecommerce-usability.csv`
- Source: `src/data/93 Ecommerce Usability Guidelines for Design Agents - Table 1.csv`

- [ ] **Step 1: Read source**

93 rows. Overlaps with usability-homepage.csv and design-principles.csv.

- [ ] **Step 2: Dedupe against other two CSVs**

For each row, check if an equivalent principle exists in design-principles.csv or usability-homepage.csv. If yes, drop. If the row has unique value (e.g., ecommerce-specific: cart, checkout, PDP, search, forms, touch), keep.

- [ ] **Step 3: Normalize and write**

Same 6 columns. Category examples: "Forms", "Checkout", "Search", "Product Detail", "Cart", "Touch". Target: ~50 rows after dedup.

- [ ] **Step 4: Commit**

```bash
git add skills/shared/data/ecommerce-usability.csv
git commit -m "feat(skills): add curated ecommerce-usability L3 data"
```

---

### Task 3.5: Add L3 query guidance to knowledge files

**Files:**
- Modify: `skills/shared/knowledge/ux-heuristics.md`
- Modify: `skills/shared/knowledge/accessibility.md`
- Modify: `skills/shared/knowledge/visual-quality.md`
- Modify: `skills/shared/knowledge/creative-direction.md`

- [ ] **Step 1: Add L3 query section to each file**

Append to each relevant L2 file:

```markdown
## L3 Lookup

When you need a deeper reference during evaluation, query these CSVs with Grep:

- `skills/shared/data/psychological-principles.csv` — cognitive + perceptual principles
- `skills/shared/data/ecommerce-usability.csv` — forms, checkout, search patterns
- `skills/shared/data/usability-homepage.csv` — homepage, nav, filtering patterns
- `skills/shared/data/design-principles.csv` — classic design frameworks

**Query pattern:** `Grep pattern="<keyword>" path="skills/shared/data/<file>.csv"`
**Use sparingly:** Query only when a specific finding needs backing, not speculatively.
```

Add only to files where CSV lookup is relevant (the 4 listed above). Token cost: ~80 tokens per file.

- [ ] **Step 2: Commit**

```bash
git add skills/shared/knowledge/
git commit -m "feat(skills): add L3 query guidance to relevant L2 files"
```

---

## Chunk 4: Command Skills — /creative, /ds-make, /ds-manage

Build the first three command SKILL.md files with inline sub-agents.

### Task 4.1: Build /creative SKILL.md

**Files:**
- Create: `skills/creative/SKILL.md`

- [ ] **Step 1: Write frontmatter and router**

```markdown
---
name: creative
description: Use when exploring visual direction, generating moodboards, proposing color palettes, typography systems, or layout strategies for a new or refreshing design language. Activates for commands like /creative, "help me find a visual direction", "propose a palette", "what typography should we use".
---

# /creative — Creative Direction

Router for creative-direction sub-agents. Use when no design language exists yet (L0/L1) or when refreshing one (L2/L3).

## Maturity Detection

Follow `skills/shared/maturity-detection.md`. Behavior:
- **L0:** Full creative freedom. Output → DESIGN.md via /map-design after exploration.
- **L1:** Refine existing DESIGN.md. Load DESIGN.md as constraint.
- **L2:** Refine within DS. Respect existing tokens; propose additions only.
- **L3:** Delegate token proposals to /ds-make.

## Always Load

- `skills/shared/knowledge/core-principles.md` (L1)
- `skills/shared/knowledge/creative-direction.md` (L2)

## Sub-Agent Router

Read the user's request and route to one of:
| Trigger | Sub-agent |
|---------|-----------|
| "mood", "theme", "vibe", "direction", "references" | Moodboard Generator |
| "palette", "color", "swatch" | Palette Architect |
| "type", "font", "typography", "scale" | Typography Director |
| "layout", "grid", "spacing", "composition" | Layout Strategist |

Unclear → ask the user which aspect first, then route.
```

- [ ] **Step 2: Write Moodboard Generator sub-agent section**

```markdown
## Sub-Agent: Moodboard Generator

**Load additionally:** none (creative-direction.md already covers moodboard method)
**Optional L3:** `skills/shared/data/psychological-principles.csv` for emotional associations

### Ask first
1. What project or product is this for? (one sentence)
2. What adjectives describe the feeling you want? (2-4 words)
3. Any brands/products you admire as references? (optional)
4. Dials: creativity (safe/balanced/bold), density (airy/balanced/packed)?

### Workflow
1. Propose a **theme statement** — `<adjective> + <adjective> + <noun>`
2. Identify 5-7 reference touchpoints (existing design languages, art movements, industrial design)
3. Extract 3-5 traits per reference
4. Synthesize into 3 theme variants (safe, balanced, bold) respecting dials
5. Present as a table: Theme | Adjectives | Key traits | Best for
6. Ask user to pick or iterate

### Output format
Theme table + next-step options ("want to explore palette next?").
```

- [ ] **Step 3: Write Palette Architect sub-agent section**

Same structure. Load: `color-theory.md`. Workflow: ask for base hue or let theme drive it → generate 11-step neutral + 9-step brand + semantic colors → validate contrast → output as table with hex + OKLCH.

- [ ] **Step 4: Write Typography Director sub-agent section**

Load: `typography.md`. Workflow: ask for tone (editorial/product/technical) → propose font pair → generate type scale with modular ratio → map to roles → output as table.

- [ ] **Step 5: Write Layout Strategist sub-agent section**

Load: `layout.md`. Workflow: ask for density preference and primary UI pattern → propose grid + spacing system + breakpoints → output as spec block.

- [ ] **Step 6: Verify and commit**

Total file budget: ~4K tokens. Verify with `wc -w skills/creative/SKILL.md`.

```bash
git add skills/creative/SKILL.md
git commit -m "feat(skills): add /creative command with 4 sub-agents"
```

---

### Task 4.2: Build /ds-make SKILL.md

**Files:**
- Create: `skills/ds-make/SKILL.md`
- Modify: `skills/ds-producer/SKILL.md` (add L3 delegation header)

- [ ] **Step 1: Write /ds-make frontmatter and router**

```markdown
---
name: ds-make
description: Use when creating, updating, versioning, or deprecating design system tokens, components, or patterns. Activates for /ds-make, "new component", "add token", "bump version", "deprecate X".
---

# /ds-make — DS Creation & Lifecycle

Router for DS creation sub-agents. At L3 (Tone/Enterprise), delegates to `skills/ds-producer/SKILL.md` workflows.

## Maturity Detection

Follow `skills/shared/maturity-detection.md`. Behavior:
- **L0:** Scaffold a new DS from scratch. Requires DESIGN.md first (run /creative → /map-design).
- **L1:** Scaffold DS from existing DESIGN.md.
- **L2:** Extend existing DS. Use token architecture from .ds-context.md.
- **L3:** Delegate to ds-producer. Invoke its workflows (new component, update, deprecation, version).

## Always Load

- `skills/shared/knowledge/core-principles.md` (L1)
- `skills/shared/knowledge/governance.md` (L2)

## Sub-Agents

- Token Architect — load `token-architecture.md`
- Component Builder — load `component-patterns.md`
- Deprecation Planner — load `governance.md` (already loaded)
- Version Advisor — load `governance.md` (already loaded)

## Routing

| Trigger | Sub-agent |
|---------|-----------|
| "token", "variable", "color scale" | Token Architect |
| "component", "new <X>", "variant" | Component Builder |
| "deprecate", "remove", "sunset" | Deprecation Planner |
| "version", "bump", "semver", "breaking" | Version Advisor |
```

- [ ] **Step 2: Write all 4 sub-agent sections**

Each follows the Chunk 4.1 template: ask-first questions, workflow steps, output format. Reference the governance cascade from L2 where relevant. For L3, each sub-agent's workflow section includes: "If maturity is L3, delegate to ds-producer Workflow N instead."

- [ ] **Step 3: Add L3 delegation header to ds-producer/SKILL.md**

Prepend to the existing description field (don't replace):
```
description: ... Used by /ds-make at L3 maturity as the Enterprise (Tone DS) specialization.
```
And add a section near the top:
```markdown
## Relationship to /ds-make

This skill is the L3 (Enterprise/Tone) specialization invoked by `/ds-make` when `.ds-context.md` identifies Tone. At L0-L2, /ds-make uses its universal sub-agents directly.
```

- [ ] **Step 4: Commit**

```bash
git add skills/ds-make/SKILL.md skills/ds-producer/SKILL.md
git commit -m "feat(skills): add /ds-make command with L3 ds-producer delegation"
```

---

### Task 4.3: Build /ds-manage SKILL.md

**Files:**
- Create: `skills/ds-manage/SKILL.md`

- [ ] **Step 1: Write frontmatter and router**

```markdown
---
name: ds-manage
description: Use for DS operations — publishing cascades, adoption analytics, documentation generation, health/drift monitoring. Activates for /ds-manage, "publish", "adoption report", "generate docs", "check health".
---

# /ds-manage — DS Operations

Router for ongoing DS management. At L3, delegates Publisher and Health Monitor to ds-producer workflows.

## Maturity Detection
See `skills/shared/maturity-detection.md`. Manage commands assume L2+ (a DS must exist). At L0/L1, politely redirect to /ds-make.

## Always Load
- `skills/shared/knowledge/core-principles.md`
- `skills/shared/knowledge/governance.md`

## Sub-Agents

| Sub-agent | Extra load | Purpose |
|-----------|-----------|---------|
| Publisher | — | Execute publishing cascade with QA gates |
| Analytics Reporter | — | Adoption metrics, usage trends |
| Documentation Generator | `documentation.md` | uSpec, property tables, demo areas |
| Health Monitor | — | Library drift, detached components, token compliance |

## Routing Table
| Trigger | Sub-agent |
|---------|-----------|
| "publish", "release", "cascade" | Publisher |
| "adoption", "usage", "metrics", "report" | Analytics Reporter |
| "document", "uspec", "property table", "demo" | Documentation Generator |
| "health", "drift", "detached", "audit" | Health Monitor |

## Workflow Chains

Two common chains:
1. **Pre-release chain:** Health Monitor → Documentation Generator → Publisher
2. **Weekly ops chain:** Analytics Reporter → Health Monitor → (optional: Deprecation Planner from /ds-make)
```

- [ ] **Step 2: Write 4 sub-agent sections**

- **Publisher:** Ask first (artifact, downstream deps). Workflow = governance cascade from L2. At L3, reference Tone Lint via `use_figma` for audit reads.
- **Analytics Reporter:** Ask first (time window, which libraries). Workflow = run analytics CLI or read cached CSV output, summarize adoption %, flag regressions.
- **Documentation Generator:** Ask first (component, spec types). Workflow = fetch via Figma MCP, run uSpec templates from documentation.md, update demo area.
- **Health Monitor:** Ask first (scope: file, page, selection). Workflow = at L3, read Tone Lint sharedPluginData; at L2, run governance checklist manually. Output finding table with severity.

- [ ] **Step 3: Commit**

```bash
git add skills/ds-manage/SKILL.md
git commit -m "feat(skills): add /ds-manage command with 4 sub-agents"
```

---

## Chunk 5: Command Skills — /design, /design-review, /map-design

### Task 5.1: Build /design SKILL.md

**Files:**
- Create: `skills/design/SKILL.md`
- Modify: `skills/ds-consumer/SKILL.md` (add L3 delegation header)

- [ ] **Step 1: Write /design frontmatter and router**

```markdown
---
name: design
description: Use when designing product features, flows, pages, or screens using an existing design system or design language. Activates for /design, "design a feature", "build a page", "select components", "compose a flow".
---

# /design — Product Design with DS

Router for product design sub-agents. At L3 (Tone), delegates to `skills/ds-consumer/SKILL.md`.

## Maturity Detection
- **L0:** Block. Require DESIGN.md first (/creative → /map-design).
- **L1:** Compose using DESIGN.md primitives. No DS library to select from.
- **L2:** Full DS-aware composition.
- **L3:** Delegate to ds-consumer.

## Always Load
- `skills/shared/knowledge/core-principles.md`
- `skills/shared/knowledge/component-patterns.md`
- `skills/shared/knowledge/ux-heuristics.md`

## Hard Rules (all maturity levels)
- NEVER propose creating new components here. Use /ds-make for gaps.
- NEVER apply overrides or detach components (L2/L3).
- Prefer existing patterns over ad-hoc compositions.

## Sub-Agents

| Sub-agent | Extra load | Purpose |
|-----------|-----------|---------|
| Component Selector | — | Recommend best-fit component(s) |
| Layout Composer | `layout.md` | Page/flow composition |
| Pattern Matcher | — | Find existing patterns for a need |
| Gap Detector | `governance.md` | Identify missing DS coverage, draft requests |

## Routing
| Trigger | Sub-agent |
|---------|-----------|
| "which component", "select", "best fit" | Component Selector |
| "compose", "layout", "page", "flow" | Layout Composer |
| "pattern", "is there a pattern", "template" | Pattern Matcher |
| "gap", "missing", "request new" | Gap Detector |
```

- [ ] **Step 2: Write all 4 sub-agent sections**

Each with ask-first questions, workflow, output format. Layout Composer workflow includes: inventory DS → propose structure → evaluate against ux-heuristics.md → refine.

- [ ] **Step 3: Add L3 delegation header to ds-consumer/SKILL.md**

Similar to Task 4.2 Step 3. Add relationship section referencing /design.

- [ ] **Step 4: Commit**

```bash
git add skills/design/SKILL.md skills/ds-consumer/SKILL.md
git commit -m "feat(skills): add /design command with L3 ds-consumer delegation"
```

---

### Task 5.2: Build /design-review SKILL.md

**Files:**
- Create: `skills/design-review/SKILL.md`

- [ ] **Step 1: Write frontmatter and router**

```markdown
---
name: design-review
description: Use to evaluate existing designs against UX heuristics, accessibility, DS compliance, visual quality, or motion principles. Activates for /design-review, "review this design", "audit UI", "check accessibility", "is this compliant".
---

# /design-review — Design Validation

Router for design review sub-agents. Runs heuristic evaluation plus DS compliance checks where applicable.

## Maturity Detection
- **L0:** Heuristics only (UX Critic, A11y Auditor, Visual Quality Inspector, Motion Reviewer). No DS Compliance Checker.
- **L1:** Heuristics + DESIGN.md conformance checks.
- **L2:** All 5 sub-agents.
- **L3:** All 5 + Tone Lint integration via `use_figma` for DS Compliance Checker.

## Always Load
- `skills/shared/knowledge/core-principles.md`
- `skills/shared/knowledge/ux-heuristics.md`

## Multi-Sub-Agent Execution

Unlike other commands, /design-review often runs multiple sub-agents in parallel. Default chain:
1. Visual Quality Inspector (first — catches structural issues)
2. UX Critic (heuristic pass)
3. A11y Auditor (WCAG pass)
4. DS Compliance Checker (L2+ only)
5. Motion Reviewer (if motion is present)

Each produces a finding table. Aggregate into one final report grouped by severity (P0 → P3).

## Sub-Agents

| Sub-agent | Extra load | Purpose |
|-----------|-----------|---------|
| UX Critic | `ux-heuristics.md` (already loaded) | Heuristic + cognitive load review |
| A11y Auditor | `accessibility.md` | WCAG 2.1 AA audit |
| DS Compliance Checker | `governance.md` | Tokens, overrides, detached |
| Visual Quality Inspector | `visual-quality.md` | Alignment, rhythm, balance |
| Motion Reviewer | `motion.md` | Timing, purpose, a11y |

## Output Format

Final report:
```
## Design Review — <file/screen name>

### P0 (Blockers)
| # | Category | Location | Issue | Fix |

### P1 (Major)
...
```
```

- [ ] **Step 2: Write all 5 sub-agent sections**

- **UX Critic:** Ask first (screen, concern). Load ux-heuristics. Workflow: apply Nielsen's 10, measure cognitive load, optional L3 query to psychological-principles.csv for specific findings.
- **A11y Auditor:** Ask first (screen, target WCAG level). Load accessibility.md. Workflow: walk checklist, test keyboard, verify contrast, flag issues.
- **DS Compliance Checker:** Ask first (scope). Workflow: L2 manual checklist from governance; L3 read Tone Lint via `use_figma(fileKey, code: 'return figma.root.getSharedPluginData("tone_lint", "lint_results")')`.
- **Visual Quality Inspector:** Ask first (screen). Workflow: squint test, 3-second test, alignment audit, spacing audit.
- **Motion Reviewer:** Ask first (interaction, prototype link). Workflow: verify purpose → measure timing → check a11y.

- [ ] **Step 3: Commit**

```bash
git add skills/design-review/SKILL.md
git commit -m "feat(skills): add /design-review command with 5 sub-agents"
```

---

### Task 5.3: Build /map-design SKILL.md

**Files:**
- Create: `skills/map-design/SKILL.md`

- [ ] **Step 1: Write frontmatter and router**

```markdown
---
name: map-design
description: Use to extract design language from an existing artifact (screenshot, URL, Figma file, or codebase) and generate a DESIGN.md. Activates for /map-design, "extract tokens", "generate DESIGN.md", "crawl this design", "document this design language".
---

# /map-design — Design Extraction

Router for design extraction sub-agents. Crawls existing designs and produces a structured DESIGN.md.

## Maturity Detection
- **L0:** Primary use case — extract from references/screenshots to bootstrap DESIGN.md.
- **L1:** Enrich existing DESIGN.md.
- **L2:** Extract from DS to refresh DESIGN.md snapshot.
- **L3:** Not typical (Tone already has full DS); limited to specific sections.

## Always Load
- `skills/shared/knowledge/core-principles.md`
- `skills/shared/knowledge/design-md-schema.md`

## Execution Chain

/map-design runs sub-agents sequentially, each feeding the next:
1. Visual Parser — identify what's on screen
2. Token Extractor — pull colors, type, spacing
3. Component Cataloger — identify components and hierarchy
4. DESIGN.md Generator — synthesize into 9-section output

User can invoke single sub-agents directly ("just extract tokens from this").

## Sub-Agents

| Sub-agent | Extra load |
|-----------|-----------|
| Visual Parser | `visual-quality.md` |
| Token Extractor | `token-architecture.md`, `color-theory.md`, `typography.md` |
| Component Cataloger | `component-patterns.md` |
| DESIGN.md Generator | (design-md-schema.md already loaded) |

## Routing
| Trigger | Sub-agent |
|---------|-----------|
| "what's in this", "parse", "identify" | Visual Parser |
| "extract tokens", "colors", "typography", "spacing" | Token Extractor |
| "list components", "inventory", "catalog" | Component Cataloger |
| "generate DESIGN.md", "write design.md" | DESIGN.md Generator |
```

- [ ] **Step 2: Write 4 sub-agent sections**

- **Visual Parser:** Ask first (source: screenshot/URL/Figma). Workflow: read source via Read (for images) or `use_figma` (for Figma) → list identified elements → tag by category (content, chrome, action).
- **Token Extractor:** Ask first (scope). Workflow: sample colors (quantize if from image) → detect type scale → measure spacing → propose 3-tier token structure.
- **Component Cataloger:** Ask first. Workflow: identify repeated patterns → label as components → detect hierarchy → output component list with purpose + variants.
- **DESIGN.md Generator:** No questions. Workflow: take outputs of previous 3 sub-agents → fill 9-section template → write to project root DESIGN.md. Confirm before writing.

- [ ] **Step 3: Commit**

```bash
git add skills/map-design/SKILL.md
git commit -m "feat(skills): add /map-design command with 4 sub-agents"
```

---

## Chunk 6: Integration, Validation & README

### Task 6.1: Update tone-ds-context.md to reference .ds-context.md

**Files:**
- Modify: `skills/shared/tone-ds-context.md`

- [ ] **Step 1: Add header section**

Prepend after the existing title:
```markdown
## Project Context File

This file serves as the `.ds-context.md` equivalent for Tone DS. When /map-design or /ds-manage detect Tone specifically, they load this file for L3 context. Projects on other design systems should maintain their own `.ds-context.md` at the repo root with similar structure.
```

- [ ] **Step 2: Commit**

```bash
git add skills/shared/tone-ds-context.md
git commit -m "docs(skills): mark tone-ds-context as L3 Tone .ds-context equivalent"
```

---

### Task 6.2: Cross-reference validation

- [ ] **Step 1: Grep for all knowledge/ references**

```
Grep pattern="skills/shared/knowledge/" path="skills/" output_mode="content"
```

Expected: every command SKILL.md references at least `core-principles.md`. Each sub-agent references its declared L2 file.

- [ ] **Step 2: Grep for all data/ references**

```
Grep pattern="skills/shared/data/" path="skills/" output_mode="content"
```

Expected: ux-heuristics, accessibility, visual-quality, creative-direction files mention L3 query patterns.

- [ ] **Step 3: Verify no orphaned files**

```
Glob pattern="skills/shared/knowledge/*.md"
```

Every file should appear in at least one Grep result from Step 1. Orphaned files are dead weight — remove or integrate.

- [ ] **Step 4: Verify token budgets**

Run `wc -w` on each knowledge file. Check against budgets:
- core-principles.md: ≤1500 words
- Each L2 file: ≤2500 words (visual-quality, documentation, creative-direction: ≤1200)
- governance.md: ≤3500 words

If over budget, trim the largest-severity-Low entries.

- [ ] **Step 5: Commit (if any trims)**

```bash
git add -u
git commit -m "fix(skills): trim knowledge files to token budgets"
```

---

### Task 6.3: Update CLAUDE.md and create README

**Files:**
- Modify: `CLAUDE.md`
- Create: `skills/README.md`

- [ ] **Step 1: Update CLAUDE.md Project Overview section**

Replace the "Project Overview" section to describe the 6 commands and L3 specialization pattern. Reference the design spec at `docs/superpowers/specs/2026-04-09-universal-design-plugin-design.md`.

- [ ] **Step 2: Create skills/README.md**

Content: one-line description of each command, a routing matrix, and the knowledge architecture diagram. This is the team's entry point.

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md skills/README.md
git commit -m "docs(skills): update project overview for 6-command architecture"
```

---

### Task 6.4: End-to-end smoke test

- [ ] **Step 1: Manually simulate each command routing**

For each of the 6 commands, read the SKILL.md and mentally walk a sample user prompt through the router to a sub-agent. Verify:
- Routing table matches sub-agent sections present in the file
- All referenced knowledge files exist at claimed paths
- Ask-first questions are reasonable and not redundant

- [ ] **Step 2: Test L3 delegation path**

Open `skills/ds-make/SKILL.md` and verify the L3 delegation notes point to real workflow numbers in `skills/ds-producer/SKILL.md`. Same for /design → ds-consumer.

- [ ] **Step 3: Test a real query with L3 CSV**

Pick a review scenario: "user is auditing a checkout form for accessibility." Simulate: /design-review → A11y Auditor loads accessibility.md → optional L3 query `Grep pattern="form" path="skills/shared/data/ecommerce-usability.csv"`. Verify the grep returns real rows.

- [ ] **Step 4: Commit any fixes**

```bash
git add -u
git commit -m "fix(skills): smoke test corrections"
```

---

### Task 6.5: Final cleanup

- [ ] **Step 1: Remove legacy design-principles.md if fully absorbed**

Check: does anything still reference `skills/shared/design-principles.md`?
```
Grep pattern="shared/design-principles.md" path="skills/"
```

If only ds-producer and ds-consumer reference it, and their content has been absorbed into `knowledge/governance.md`, update those two files to reference the new location, then delete the legacy file.

- [ ] **Step 2: Final commit**

```bash
git add -u
git commit -m "refactor(skills): remove legacy design-principles.md after absorption"
```

---

## Out of Scope (Explicit Non-Goals)

The following are **not** part of this plan:
- Building the MCP server for Figma plugin integration (separate plan: `2026-04-08-plugin-integration.md`)
- Deploying Tone Lint to the team (pending deployment decision — see PROJECT_CONTEXT.md)
- Building a CLI to run skills outside Claude Code
- Writing content beyond what source CSVs provide (no speculative principles)
- Automated token counting tooling
- Skill testing harness (manual smoke test only)

## Success Criteria

1. All 6 command SKILL.md files exist and route correctly.
2. All ~20 sub-agents have workflow + output format sections.
3. L1 core-principles.md is ≤2K tokens.
4. All L2 knowledge files are within their budgets.
5. L3 CSVs are curated, deduped, and queryable via Grep.
6. Every knowledge file is referenced by at least one sub-agent.
7. L3 delegation from /ds-make and /design to existing ds-producer/ds-consumer works.
8. Smoke test walkthrough succeeds for all 6 commands.

## Execution Notes

- Each chunk is independently committable. Chunks 1→2 and 4→5 have no cross-dependencies and could be parallelized if using subagent-driven execution.
- Chunk 3 (CSV curation) can run in parallel with Chunks 1-2.
- Chunk 6 (integration) must run last.
- Review after each chunk before proceeding. If token budgets blow out, trim before adding more.
