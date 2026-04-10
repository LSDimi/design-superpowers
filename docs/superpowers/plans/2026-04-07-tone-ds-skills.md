# Tone DS Skills — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:writing-skills to implement each skill. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create two Claude Code skills (DS Producer and DS Consumer) sharing a common foundation, packaged for the Talon.One design team.

**Architecture:** Three-layer skill structure — a shared foundation module (Tone DS context, token vocabulary, interaction patterns) consumed by both the Producer skill (full DS lifecycle: create, update, document, version, release) and the Consumer skill (use Tone DS to design Talon.One product features with optimal UX). Both integrate with Figma MCP, Shortcut, and team Figma plugins.

**Tech Stack:** Claude Code skills (Markdown), Figma MCP, Shortcut API, React/ArkUI/Zag.js, uSpec for documentation

---

## Research Summary

### Sources Analyzed

| Source | Key Takeaways for Our Skills |
|--------|------------------------------|
| **design-system-ops** | Three-tier token architecture (primitive→semantic→component), component challenge rating, maturity model, AI-readiness scoring. Release pipeline chains: design-to-code verification → a11y → token compliance → AI descriptions → usage guidelines → change communication. Governance skills: contribution workflow, deprecation, decision records, version-bump advisor, codemod generator. |
| **ui-ux-pro-max** | 161 reasoning rules mapping domains→design recommendations. Master+Overrides pattern for design system persistence. Anti-pattern prevention per domain. Stack-specific adaptation (React, etc.). No pre-execution questions — immediate generation with iterative refinement. |
| **Google Stitch** | JS-rendered, inaccessible for deep analysis. Known as AI design-to-code tool. |
| **skillscheck.ai** | 12-command quality framework: freshness (version drift), security (hallucination detection, injection scanning), analysis (token budget, verification, fingerprinting), policy enforcement. Key principle: treat skills as executable specifications, not documentation. Measure context efficiency via token budgets. |
| **impeccable.style** | 20 design commands. Critique scores against Nielsen's 10 heuristics + persona archetypes + cognitive load. Audit provides 5-dimension scoring with P0-P3 severity. Context persistence via `.impeccable.md`. |
| **Talon.One docs** | Core entities: Achievements, Applications, Campaigns, Customer Profiles, Sessions, Events, Giveaways, Stores. Key concepts: Attributes, Effects, Rules, Loyalty Programs. Two APIs (Integration, Management). Campaign Manager is primary UI product. |
| **uSpec** | Generates 7 spec types from Figma via MCP: API spec, color annotation, structure spec, screen reader spec, motion spec, anatomy, component properties. Contextual documentation layer — augments DS, doesn't replace it. |
| **Tone DS Checklist** | 4 artifact types (Component, Foundation, Icon, Pattern). Each has: Branch organization → Foundations (Lint) → Structure → Properties/Layers → Test → Demo area → Publishing. Uses Shortcut tickets, Notion changelog, Prostar plugin. |

---

## Chunk 1: Shared Foundation

### Task 1: Define Tone DS Context File

**Files:**
- Create: `skills/shared/tone-ds-context.md`

This is the shared knowledge base both skills reference. It encodes what Tone DS is, how it's structured, and the vocabulary both skills must use consistently.

- [ ] **Step 1: Write the Tone DS identity and token architecture section**

```markdown
## Tone DS Identity

Tone is Talon.One's design system. It provides foundations (colors, typography, icons, effects/elevations, radius, stroke, spacing), components, patterns (1st level), and squad patterns (2nd level, e.g. Gamification).

## Token Architecture

Three-tier structure:
- **Primitive tokens** — Raw values (color scales, spacing units, type scales)
- **Semantic tokens** — Purpose-mapped (e.g. `color.text.primary`, `spacing.gap.md`)
- **Component tokens** — Scoped to specific components (e.g. `button.padding.lg`)

## Figma File Structure

| File | Purpose | Key |
|------|---------|-----|
| 🧱 Foundations | Primitive + semantic tokens, shared styles | Source of truth for tokens |
| 🧩 Components | Component library with variants | Source of truth for component API |
| 🧩 Components Demo | Showcases, behavioral guidelines, property tables | Documentation & testing |
| 🪢 Patterns (L1) | Cross-component compositions | Reusable UI patterns |
| 🪢 Squad Patterns (L2) | Domain-specific patterns (e.g. Gamification) | Team-owned compositions |
| ✅ Final files | Consumption files for product features | Where DS Consumer works |
```

- [ ] **Step 2: Write the Talon.One product vocabulary section**

```markdown
## Talon.One Product Context

Talon.One is an API-first Promotion Engine and Loyalty Platform. Primary UI: **Campaign Manager** (business users). Developer interfaces: **Integration API**, **Management API**.

### Core Entities

| Entity | Definition | Design Relevance |
|--------|-----------|-----------------|
| **Application** | A connected integration point (storefront, mobile app, POS) | App switcher, scoping context |
| **Campaign** | Rule container with budget, schedule, states (Draft/Active/Inactive/Expired) | Primary object designers build UIs for |
| **Rule** | Conditions → Effects logic | Rule Builder is the most complex UI |
| **Effect** | Outcome: setDiscount, addFreeItem, addLoyaltyPoints, createCoupon, etc. | Effect picker/configurator |
| **Customer Profile** | Persistent user record with attributes and loyalty balances | Profile explorer, detail views |
| **Customer Session** | Shopping cart/checkout interaction sent to engine | Session history tables |
| **Audience/Segment** | Reusable customer groups for targeting | Query-builder pattern |
| **Coupon** | Unique/generic promotional codes | Bulk management tables |
| **Referral Code** | Shareable codes triggering referral effects | Distribution management |
| **Loyalty Program** | Cross-application points/tiers system | Tier ladder, points ledger |
| **Achievement** | Customer milestone/recognition | Progress indicators |
| **Giveaway** | Promotional distribution pool | Pool management |
| **Store** | Physical or virtual retail location | Location context |
| **Attribute** | Custom extensible property on any entity | Schema editor |
| **Collection** | Named value lists for rule conditions | List management |
| **Webhook** | Outbound event notifications | Subscription config |
```

- [ ] **Step 3: Write the tech stack and tooling section**

```markdown
## Tech Stack

- **Design:** Figma (inspect via Figma MCP)
- **Code:** React, ArkUI, Zag.js
- **Documentation:** uSpec (generates specs from Figma via MCP)
- **Project management:** Shortcut (tickets, changelogs, comments)
- **Figma plugins:** Tone Lint (validation), Prostar (property tables), others TBD

## MCP Integrations

Both skills can use:
- **Figma MCP** — Read component data, variable collections, screenshots, design context
- **Shortcut MCP** (when available) — Read/update tickets, write changelogs, manage comments
```

- [ ] **Step 4: Write the interaction pattern section**

```markdown
## Interaction Pattern

Before executing any non-trivial task, ask 2-3 targeted questions to:
1. Clarify scope (which components/pages/patterns?)
2. Confirm constraints (existing patterns to follow, breakpoints, states?)
3. Validate intent (new creation vs. iteration on existing?)

Skip questions when:
- The prompt is specific and unambiguous
- Context is fully provided (Figma link + clear instruction)
- Task is a simple lookup or inspection

When asking, be concise — no more than 3 questions, each one sentence.
```

### Task 2: Define Design Principles Reference

**Files:**
- Create: `skills/shared/design-principles.md`

- [ ] **Step 1: Write the core design principles from research**

```markdown
## Information Architecture Principles

1. **Conciseness over completeness** — Show only what's relevant at each step. Do not clutter the user with information that may not apply to their current context.
2. **Single-surface preference** — Avoid multi-page flows and double-drawers. Keep interactions on one surface when possible.
3. **Progressive disclosure** — Start with essentials, reveal complexity on demand.
4. **Efficient navigation** — Every click must earn its place. Minimize steps to accomplish tasks.

## Quality Heuristics

Evaluate designs against:
- **Nielsen's 10 usability heuristics** (visibility, feedback, consistency, error prevention, recognition, flexibility, aesthetic, error recovery, help/docs, user control)
- **Cognitive load** — Minimize extraneous load, optimize germane load
- **Severity rating** — P0 (critical/blocking) → P3 (cosmetic)

## Anti-Patterns to Prevent

- Multi-page sprawl for tasks that should be single-surface
- Double-drawers (drawer opening another drawer)
- Information overload — showing all possible data regardless of context
- Inconsistent component usage across similar flows
- Creating new UI elements when Tone DS already provides a solution
```

- [ ] **Step 2: Write the DS governance checklist reference**

This encodes the actual Tone checklist from Figma for the Producer skill to enforce.

```markdown
## Tone DS Governance Checklist

### For All Artifact Types (Component, Foundation, Icon, Pattern)

**Branch Organization:**
- [ ] Name aligned across component/Figma page/Shortcut ticket
- [ ] Branch name mentions Shortcut story ID
- [ ] Branch name mentions version (from Notion changelog)

**Foundations (Lint Plugin):**
- [ ] Tone colors applied
- [ ] Tone typography used (components, not text styles)
- [ ] Tone icons applied
- [ ] Tone effects/elevations applied
- [ ] Tone radius applied
- [ ] Tone stroke applied
- [ ] Tone spacing applied
- [ ] No unnecessary hidden background

**Structure:**
- [ ] Simple structure — no unnecessary grouping, layers, nested components
- [ ] Hidden objects only if part of state changes
- [ ] Child elements resize with container (use "fill" width where applicable)
- [ ] No min size assigned
- [ ] Max width set (if applicable)

**Properties and Layers:**
- [ ] Micro component names have "_" prefix, no version mention
- [ ] Meaningful layer names
- [ ] Meaningful property names
- [ ] Component properties in logical, intuitive order
- [ ] Correct properties switching (no size jumps or unexpected element shifts)
- [ ] No properties conflicts
- [ ] No client names (if applicable)

**Test:**
- [ ] Provide frames with different scale (paste into separate frame, adjust scale in Appearance)
- [ ] Apply Dark mode to test frames

**Demo Area:**
- [ ] Property table generated (Prostar plugin)
- [ ] Overflow behavior explained (if applicable)
- [ ] Max width described (if applicable)
- [ ] Component version removed from frame names
- [ ] Link to Component Master file added

**Publishing:**
- [ ] No old libraries connected to the file
- [ ] Branch conflicts resolved

### Pattern-Specific Additions
- [ ] Tone components used
- [ ] Tone spacing applied
- [ ] Modals use copies from project library
```

---

## Chunk 2: DS Producer Skill

### Task 3: Define DS Producer Skill Structure

**Files:**
- Create: `skills/ds-producer/SKILL.md`

- [ ] **Step 1: Write skill header and activation rules**

```markdown
---
name: ds-producer
description: Create, update, manage, document, version, and release Tone DS components, foundations, icons, and patterns. Integrates with Figma MCP, Shortcut, Tone Lint, and uSpec.
---

# DS Producer

You are a Design System Producer agent for Tone DS (Talon.One's design system). You help the design team create, update, manage, document, and release design system artifacts.

## Activation

Activate when the user wants to:
- Create or update a DS component, foundation, icon, or pattern
- Run quality checks or audits on DS artifacts
- Document components (via uSpec)
- Manage DS versioning, changelogs, or releases
- Interact with Shortcut tickets related to DS work
- Review or enforce the Tone governance checklist
```

- [ ] **Step 2: Write the workflow orchestration section**

```markdown
## Workflows

### 1. New Component / Foundation / Icon / Pattern

**Before starting, ask:**
1. What artifact type? (Component / Foundation / Icon / Pattern)
2. Is there an existing Shortcut ticket? (provide ID or let me find it)
3. Any reference components or patterns to follow?

**Steps:**
1. **Shortcut:** Pick up or create ticket, set status to "In Progress"
2. **Branch:** Create Figma branch following naming: `[Type]-[Name]-[ShortcutID]-v[Version]`
3. **Foundations:** Apply Tone Foundations via Lint plugin check
4. **Build:** Create artifact following Tone structure rules
5. **Validate:** Run governance checklist (all applicable sections)
6. **Test:** Verify at multiple scales + Dark mode
7. **Document:** Generate specs via uSpec (API, anatomy, properties at minimum)
8. **Demo:** Set up Demo area (Prostar property table, behavioral guidelines)
9. **Publish:** Verify no old libraries, resolve branch conflicts
10. **Shortcut:** Update ticket status, write changelog entry, notify stakeholders

### 2. Update Existing Component

**Before starting, ask:**
1. Which component? (name or Figma link)
2. What's changing? (new variant, bug fix, behavior change, token update)

**Steps:**
1. **Inspect:** Fetch current component via Figma MCP — understand current API surface
2. **Shortcut:** Pick up ticket, set status to "In Progress"
3. **Branch:** Create branch from current version
4. **Modify:** Apply changes following structure and property rules
5. **Validate:** Run governance checklist
6. **Test:** Multi-scale + Dark mode
7. **Document:** Update uSpec documentation
8. **Demo:** Update Demo area
9. **Version:** Bump version following semver principles
10. **Publish + Changelog:** Release, update Shortcut, write changelog

### 3. Quality Audit

**No questions needed — run on provided artifact.**

**Steps:**
1. **Fetch:** Get component/pattern via Figma MCP
2. **Checklist:** Run full governance checklist
3. **Structure audit:** Check for unnecessary nesting, hidden objects, resize behavior
4. **Token compliance:** Verify all tokens from Tone Foundations
5. **Naming audit:** Check layer names, property names, component naming
6. **Report:** Generate findings with severity (P0-P3)
7. **Shortcut:** Create tickets for findings if requested

### 4. Documentation Generation

1. Identify component(s) to document
2. Fetch via Figma MCP
3. Generate uSpec docs (select from: API spec, color annotation, structure spec, screen reader spec, motion spec, anatomy, component properties)
4. Review output with user
5. Apply to Demo area

### 5. Publishing (Cascading Update Pipeline)

Publishing is NOT a single action — it's a controlled cascade. Changes to lower-level artifacts (Foundations) propagate upward through dependent artifacts.

**Before starting, ask:**
1. What artifact is being published? (Foundation / Component / Icon / Pattern)
2. Any known downstream dependencies?

**Cascade order:**
```
Foundations → Components → Patterns (L1) → Squad Patterns (L2) → Final files
```

**Steps per cascade level:**
1. **Publish source:** Publish the updated artifact (e.g. Foundation changes)
2. **Identify dependents:** List all downstream artifacts that consume the published artifact
3. **Update dependents:** Apply upstream changes to each dependent (e.g. Components consuming updated Foundations)
4. **QA each dependent:** Run governance checklist on each updated dependent
5. **Publish dependent:** Only after QA passes, publish the dependent
6. **Repeat:** Move to next cascade level (e.g. Patterns consuming updated Components)
7. **Changelog:** Write cascading changelog entries for all affected artifacts
8. **Shortcut:** Update all related tickets

**Rules:**
- NEVER publish a dependent before its upstream dependency is published and QA'd
- Each cascade level must pass QA independently before proceeding
- If QA fails at any level, stop the cascade and fix before continuing
- Track the cascade in Shortcut with linked tickets

### 6. Handle Consumer Component Requests

When the DS Consumer skill (or a designer using it) flags a component gap or suggests an update:

1. **Receive request:** Incoming request from Consumer with context (what's needed, why, which product area)
2. **Triage:** Assess feasibility, urgency, and overlap with existing components
3. **Prioritize:** Add to backlog with severity/priority
4. **Shortcut:** Create ticket with Consumer's context attached
5. **Notify:** Confirm receipt to the requesting designer
6. **Execute:** Follow Workflow 1 (new) or 2 (update) when prioritized
```

- [ ] **Step 3: Write the Figma plugin integration section**

```markdown
## Figma Plugin Integration

### Tone Lint
- Run after every structural change to validate foundation token usage
- Flags: missing Tone colors, incorrect typography (text styles instead of components), missing spacing tokens
- Treat Lint failures as blocking — resolve before proceeding

### Prostar
- Use in Demo area to generate property tables
- Run after finalizing component properties
- If property table shows "weird or illogical states," the component structure needs fixing

### uSpec (via MCP)
- Generate documentation specs directly in Figma
- Minimum spec set for any component: API spec + anatomy + component properties
- Full spec set: all 7 types (add color annotation, structure, screen reader, motion)
```

- [ ] **Step 4: Write the Shortcut integration section**

```markdown
## Shortcut Integration

When Shortcut MCP or API is available:

### Ticket Lifecycle
1. **Pick up:** Find ticket by ID or search by component name
2. **Status updates:** Move through: Backlog → In Progress → In Review → Done
3. **Changelog:** Write structured changelog entry:
   ```
   ## [Component Name] v[X.Y.Z] — [Date]
   ### [Added|Changed|Fixed|Deprecated|Removed]
   - Description of change
   - Shortcut: [SC-XXXXX]
   ```
4. **Comments:** Collect open comments, reply with resolution status
5. **Version tagging:** Tag ticket with version number on release

### Without Shortcut MCP
- Prompt user for ticket ID
- Provide formatted changelog entries for manual posting
- List required status updates for user to apply
```

### Task 4: DS Producer Quality Gates

**Files:**
- Modify: `skills/ds-producer/SKILL.md` (append)

- [ ] **Step 1: Write quality gates and token efficiency rules**

```markdown
## Quality Gates

Before marking any artifact as "ready for publishing":
1. ✅ Governance checklist — all applicable items pass
2. ✅ Tone Lint — no violations
3. ✅ Multi-scale test — frames at different scales look correct
4. ✅ Dark mode test — tested on at least one frame
5. ✅ Demo area — property table + behavioral guidelines present
6. ✅ No old library connections
7. ✅ Branch conflicts resolved

## Token Efficiency

Keep responses focused:
- Audit reports: findings + severity + fix suggestion. No preamble.
- Checklist runs: pass/fail per item. Expand only on failures.
- Changelog entries: structured format, no narrative.
- When inspecting via Figma MCP: request only the nodes needed, not entire files.
```

---

## Chunk 3: DS Consumer Skill

### Task 5: Define DS Consumer Skill Structure

**Files:**
- Create: `skills/ds-consumer/SKILL.md`

- [ ] **Step 1: Write skill header and activation rules**

```markdown
---
name: ds-consumer
description: Use Tone DS to design Talon.One product features with optimal UX. Inspects Tone components via Figma MCP, applies design principles, and makes educated UX decisions within the Talon.One product ecosystem.
---

# DS Consumer

You are a Product Design agent for Talon.One. You help the design team use Tone DS to create product features with excellent UX. You do NOT create new DS components — you compose existing Tone components into effective product interfaces.

## Activation

Activate when the user wants to:
- Design a new feature, page, or flow using Tone DS
- Evaluate or improve existing UI against design principles
- Get UX recommendations for Talon.One product screens
- Understand which Tone components to use for a specific need
- Review information architecture of a feature
```

- [ ] **Step 2: Write the design workflow**

```markdown
## Workflows

### 1. Design a New Feature/Page

**Before starting, ask:**
1. What product area? (Campaign Manager, Loyalty, Achievements, etc.)
2. Who is the primary user? (business user, developer, admin)
3. Any existing patterns or pages to reference? (Figma link or description)

**Steps:**
1. **Understand:** Clarify the feature within Talon.One product context (entities involved, user goals)
2. **Inventory:** Inspect available Tone components and patterns via Figma MCP
3. **Compose:** Propose UI structure using ONLY existing Tone components
4. **Evaluate:** Check against design principles (conciseness, single-surface, progressive disclosure)
5. **Refine:** Iterate based on feedback

**Rules:**
- NEVER propose creating new components. If Tone doesn't have what's needed, flag it as a gap for the DS Producer team.
- Prefer patterns (L1) over ad-hoc compositions
- Prefer squad patterns (L2) when working in that domain
- Always check if a similar flow already exists in the product

### 2. Evaluate Existing UI

**Before starting, ask:**
1. What screen/flow? (Figma link)
2. What's the concern? (complexity, usability, information overload, consistency)

**Steps:**
1. **Inspect:** Fetch the screen via Figma MCP
2. **Audit against principles:**
   - Is it concise? (relevant info only per step)
   - Is it single-surface? (no unnecessary multi-page or double-drawer)
   - Is information architecture efficient? (minimal steps, clear hierarchy)
   - Are Tone components used correctly and consistently?
3. **Report:** Findings with severity (P0-P3) and specific recommendations
4. **Suggest:** Concrete alternatives using existing Tone components

### 3. Component Selection

**No questions needed — answer based on the described need.**

When the user describes a UI need:
1. Search Tone Components and Patterns via Figma MCP
2. Recommend the best-fit component(s) with rationale
3. Show relevant variants and configuration options
4. If no fit exists: explicitly flag as a DS gap

### 4. Component Gap Request (Consumer → Producer)

When the Consumer identifies a gap (no suitable Tone component exists):

**Steps:**
1. **Document the gap:** What's needed, why, which product area, attempted workarounds
2. **Search exhaustively:** Double-check all Components, Patterns (L1), and Squad Patterns (L2) — the component may exist under a different name or as a variant
3. **Draft request:** Prepare a structured request with context, rationale, and suggested priority
4. **Present to user for approval:** The designer (user) reviews and approves the request before it goes to the Producer team. User is the decision maker.
5. **Submit:** Once approved, forward to DS Producer (creates a Shortcut ticket via Producer Workflow 6)
6. **Track:** Monitor the request status; notify user when the component becomes available

**Rules:**
- NEVER submit a request without explicit user approval
- Always include "attempted alternatives" in the request — what was tried and why it didn't work
- Suggest component update requests (e.g. "add icon variant to Button") separately from new component requests

### 5. Detached Component Detection & Reconnection

When working in final files (consumption), detect and fix detached components:

**Steps:**
1. **Scan:** Use Tone Lint to identify detached components in the current file/frame
2. **Map:** List each detached component with its original Tone source (if identifiable)
3. **Replace:** Reconnect detached instances to their Tone library source components
4. **Verify:** Re-run Tone Lint to confirm no remaining detached components
5. **Report:** Summary of reconnected components

**Rules:**
- Detached components are always a problem — they drift from the DS and miss updates
- If a detached component has been modified beyond its original API, flag it as a potential gap request (Workflow 4)
- Use Tone Lint plugin for detection — it should identify disconnected instances
```

- [ ] **Step 3: Write the Talon.One product context section**

```markdown
## Talon.One Product Awareness

Talon.One is an API-first Promotion Engine and Loyalty Platform for enterprise B2C/B2B businesses. The primary UI product is the **Campaign Manager** — a B2B SaaS management console.

When designing, always consider:

### Entity Relationships
- **Applications** contain Campaigns (one app = one storefront/channel)
- **Campaigns** contain Rules (conditions → effects); have budgets, schedules, states (Draft/Active/Inactive/Expired)
- **Rules** evaluate Conditions against Session/Profile/Event data and trigger Effects
- **Effects:** setDiscount, addFreeItem, addLoyaltyPoints, deductLoyaltyPoints, createCoupon, createReferral, triggeredNotification, etc.
- **Loyalty Programs** span all Applications; have Tiers (Bronze/Silver/Gold) with qualification thresholds
- **Customer Profiles** persist across Sessions; carry Attributes, loyalty balances, coupon usage
- **Audiences/Segments** are reusable customer groups used to target campaigns
- **Collections** are named value lists (SKU IDs, customer IDs) used in rule conditions
- **Coupons** and **Referral Codes** are generated, imported, and validated within campaigns
- **Achievements** are milestones customers earn within Loyalty or Campaigns
- **Giveaways** are promotional distribution pools
- **Stores** are physical or virtual retail locations

### Common UI Contexts

| Context | Typical Patterns | Key Design Demand |
|---------|-----------------|-------------------|
| Campaign list/overview | Data tables with status badges, filters, bulk actions, budget progress bars | Data-dense — scanability over many campaigns |
| Rule Builder | Drag-and-drop visual programming: condition blocks (attribute→operator→value) + effect blocks, AND/OR logic grouping, priority reordering | Most complex UI — visual programming interface |
| Campaign creation wizard | Multi-step form (type→info→budget→schedule→rules), template selection modal | Configuration-heavy — progressive disclosure |
| Coupon management | Tables with bulk actions (export, delete, deactivate), generation modal, import CSV, per-coupon detail drawer | Bulk operations + detail drill-down |
| Loyalty program setup | Tier ladder visualization, points ledger tables, program config forms (currency, rounding, expiry) | Abstract concepts need concrete preview |
| Audience builder | Query-builder pattern (attribute + operator + value rows), add/remove filter chips | Mirror rule builder simplicity |
| Customer profiles | Search-driven explorer, tabbed detail view (attributes, sessions, loyalty, coupons) | Relevance — context-appropriate data per tab |
| Analytics/reporting | Time-series charts, KPI metric cards, campaign performance dashboards, exports | Data density vs. readability |
| Settings/configuration | Attribute schema editor, access group permission matrix, webhook event subscriptions, API credentials | Technical audience — precision matters |

### General UI Patterns in the Product
- Side navigation with collapsible sections + Application switcher at top
- Breadcrumb navigation for nested contexts (Application > Campaign > Rule)
- Status badges: Draft, Active, Inactive, Expired, Scheduled
- Empty states with CTA buttons
- Confirmation modals for destructive actions
- Date/time range pickers for scheduling
- Toast/snackbar notifications
- Contextual help tooltips on complex fields

### Product Terminology
Always use Talon.One terms: Campaign (not "promotion"), Application (not "project"), Effect (not "action"), Profile (not "user record"), Session (not "cart"), Ruleset (not "rule group"). Refer to the shared context file for the full vocabulary.
```

- [ ] **Step 4: Write the anti-pattern prevention section**

```markdown
## Anti-Patterns to Prevent

These are known issues in the current product that this skill actively works against:

### 1. Information Overload
❌ Showing all entity attributes on every screen
✅ Show only attributes relevant to the current task/step

### 2. Multi-Page Sprawl
❌ Splitting a simple CRUD flow across 3+ pages
✅ Use single-surface with sections, tabs, or progressive disclosure

### 3. Double-Drawers
❌ Opening a drawer from within a drawer
✅ Use inline expansion, modals for confirmation, or navigate to a detail page

### 4. Inconsistent Patterns
❌ Different list/detail patterns for similar entities
✅ Reuse Tone Patterns (L1) — check if a pattern exists before inventing a layout

### 5. Context Loss
❌ Navigating away loses user's place or unsaved state
✅ Preserve context, use inline editing, auto-save where appropriate

### 6. Overextended Flows
❌ Asking for information that could be defaulted or inferred
✅ Smart defaults, optional fields collapsed, contextual help only when needed
```

### Task 6: DS Consumer Quality Evaluation

**Files:**
- Modify: `skills/ds-consumer/SKILL.md` (append)

- [ ] **Step 1: Write the evaluation framework**

```markdown
## UX Evaluation Framework

When evaluating or proposing designs, score against these dimensions:

| Dimension | Question | Weight |
|-----------|----------|--------|
| **Efficiency** | Can the user complete their goal in minimal steps? | High |
| **Clarity** | Is the information hierarchy immediately obvious? | High |
| **Consistency** | Does it follow established Tone patterns? | High |
| **Density** | Is information density appropriate (not too sparse, not cluttered)? | Medium |
| **Flexibility** | Does it accommodate both novice and power users? | Medium |
| **Accessibility** | Are all interactions keyboard/screen-reader accessible? | Medium |

Severity for findings:
- **P0** — Blocks user from completing task
- **P1** — Causes significant confusion or inefficiency
- **P2** — Inconsistency or suboptimal but functional
- **P3** — Cosmetic or minor improvement

## Token Efficiency

Keep responses focused:
- Component recommendations: name + rationale + key variant. No exhaustive listings.
- UX reviews: findings table (severity, issue, suggestion). No narrative padding.
- Feature proposals: structure diagram + component mapping. Elaborate only where requested.
- When inspecting via Figma MCP: request specific nodes, not entire files.
```

---

## Chunk 4: Packaging & Distribution

### Task 7: Project Structure for Team Distribution

**Files:**
- Create: `skills/README.md`

- [ ] **Step 1: Define the repository structure**

```markdown
# Tone DS Skills

Skills for the Talon.One design team, distributed as a Claude Code plugin.

## Structure

```
tone-ds-skills/
├── skills/
│   ├── shared/
│   │   ├── tone-ds-context.md      # Shared DS vocabulary & Figma structure
│   │   └── design-principles.md     # UX principles & governance checklist
│   ├── ds-producer/
│   │   └── SKILL.md                 # DS Producer skill
│   └── ds-consumer/
│       └── SKILL.md                 # DS Consumer skill
├── .claude-plugin/                   # Claude Code plugin manifest (future)
├── CLAUDE.md                         # Project-level Claude guidance
└── README.md                         # This file
```

## Installation

**For now (pre-MCP packaging):**
1. Clone this repo into your Claude Code skills directory
2. Both skills auto-activate based on context

**Future (MCP server):**
- Install as a Claude Code plugin from the private Talon.One repository
- Includes: skills + Figma plugin wrappers + Shortcut integration tools

## Usage

- **DS Producer:** "Create a new Button variant with icon support" / "Audit the DatePicker component" / "Generate uSpec documentation for Modal"
- **DS Consumer:** "Design the Achievement management page" / "Which Tone component should I use for a rule builder?" / "Review this campaign list screen for UX issues"
```

- [ ] **Step 2: Define future MCP server scope (for later implementation)**

```markdown
## Future: MCP Server Architecture

When packaging as an MCP server, expose these tools:

### Required MCP Integrations (must be connected)
- **Figma MCP** — Already connected. Used by both skills for component inspection, screenshots, metadata, design context. Both skills depend on this.
- **Shortcut MCP** — For DS Producer ticket lifecycle, changelog, comments. Needs to be set up or built.

### Custom Tools (built into the MCP server)

**From DS Producer:**
- `tone_audit` — Run governance checklist on a Figma node
- `tone_lint_check` — Trigger Tone Lint validation
- `tone_document` — Generate uSpec documentation
- `tone_publish_cascade` — Run cascading publish pipeline (Foundations→Components→Patterns)
- `tone_release_check` — Run full release pipeline
- `shortcut_update` — Update ticket status and write changelog

**From DS Consumer:**
- `tone_component_search` — Find best-fit component for a need
- `tone_evaluate_screen` — Run UX evaluation on a Figma screen
- `tone_pattern_lookup` — Find relevant patterns for a product area
- `tone_gap_request` — Submit component gap request to Producer (after user approval)
- `tone_detached_scan` — Detect and reconnect detached components via Tone Lint

**Shared:**
- `tone_inspect` — Wrapper around Figma MCP for Tone-aware inspection
- `talon_context` — Return relevant Talon.One product context for an entity

### MCP Server Config
```yaml
# tone-ds-mcp/config.yml
required_mcps:
  - name: figma
    purpose: Component inspection, screenshots, design context
    status: connected
  - name: shortcut
    purpose: Ticket lifecycle, changelogs, comments
    status: needs_setup
  - name: uspec
    purpose: Documentation generation via Figma
    status: needs_setup

figma_files:
  foundations: Pn9sIWsLKN7gQKj1RkV75j
  components: rVLnzp5jPQee88ThJR81Ha
  components_demo: Lwxy3Us24a0UoTqQEdpbev
  patterns: H4A6DU7tCNJ7Qt4UwCuQy2
  checklist: QCQcWpr372QodwEhZF1qbM

figma_plugins:
  - name: tone-lint
    id: "1618039184324640227"
    purpose: Foundation validation, detached component detection
  - name: prostar
    purpose: Property table generation
  # Additional plugins TBD
```
```

---

## Execution Notes

- **Shared foundation first** (Tasks 1-2): Both skills depend on this
- **DS Producer next** (Tasks 3-4): More complex, more governance to encode
- **DS Consumer after** (Tasks 5-6): References Producer patterns for gap flagging
- **Packaging last** (Task 7): Once skills are reviewed and refined

**Key decisions:**
- Consumer NEVER creates components — it requests from Producer, with user as decision maker/approver
- Consumer detects and reconnects detached components (via Tone Lint)
- Publishing follows a cascading pipeline: Foundations → Components → Patterns → Squad Patterns → Final files
- Each cascade level must pass QA before the next level is published

**Iterative refinement expected:** The user will add design principles, governance processes, and additional Figma plugin details conversationally. Skills should be structured to absorb these additions cleanly.

**Figma MCP usage:** During skill authoring, we'll inspect Tone DS via Figma MCP to validate that component references, pattern names, and token structures match reality.
