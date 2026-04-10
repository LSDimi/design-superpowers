# DESIGN.md Schema (L2)

> Loaded by /map-design DESIGN.md Generator. Defines the 9-section schema, a fill-in template, and a field guide. Based on awesome-design-md conventions.

## The 9 Sections

| # | Section | Purpose |
|---|---------|---------|
| 1 | **Visual Theme** | Mood statement, character adjectives, reference influences |
| 2 | **Color Palette** | Neutral + brand + semantic scales with values |
| 3 | **Typography** | Font families, type scale, role mapping |
| 4 | **Components** | Catalog of components with purpose and key variants |
| 5 | **Layout** | Grid, spacing system, breakpoints, density |
| 6 | **Depth** | Elevation, shadows, layering rules |
| 7 | **Do's and Don'ts** | 5–10 bullets each, specific to this project |
| 8 | **Responsive** | Breakpoint strategy, mobile/desktop adaptations |
| 9 | **Agent Prompt Guide** | How agents should use this file; invariants to preserve |

## Template

```markdown
# [Project Name] Design Language

> One-sentence description of the product and its primary users.

## 1. Visual Theme

**Theme statement:** [adjective], [adjective], [noun]

**Character:** [2–3 sentences describing the intended feeling and visual character]

**References:** [3–5 influences — brand names, design systems, art movements]

---

## 2. Color Palette

### Neutral Scale
| Token | Value | Usage |
|-------|-------|-------|
| `neutral-0` | #FAFAFA | Page background |
| `neutral-10` | #F0F0F0 | Subtle surface |
| `neutral-40` | #9E9E9E | Placeholder, disabled |
| `neutral-70` | #424242 | Secondary text |
| `neutral-90` | #1A1A1A | Primary text |

### Brand Scale
| Token | Value | Usage |
|-------|-------|-------|
| `brand-30` | #[hex] | Hover surface |
| `brand-50` | #[hex] | Primary CTA, key accent |
| `brand-70` | #[hex] | Text on light |

### Semantic Colors
| Role | Light token | Dark token |
|------|------------|-----------|
| Success | `success-50` | `success-40` |
| Warning | `warning-50` | `warning-40` |
| Error | `error-50` | `error-40` |
| Info | `info-50` | `info-40` |

---

## 3. Typography

**Font families:**
- Display / Headings: [Font name], [fallback stack]
- Body: [Font name], [fallback stack]
- Mono (if used): [Font name], [fallback stack]

**Type scale:**
| Token | Size | Weight | Line height | Usage |
|-------|------|--------|-------------|-------|
| `text-xs` | 11px | 400 | 1.4 | Captions, metadata |
| `text-sm` | 13px | 400 | 1.5 | Helper text, secondary |
| `text-base` | 16px | 400 | 1.6 | Body copy |
| `text-lg` | 20px | 500 | 1.4 | Card intro, emphasized body |
| `text-xl` | 25px | 600 | 1.3 | Section heading (h3) |
| `text-2xl` | 31px | 700 | 1.2 | Page heading (h2) |
| `text-3xl` | 39px | 700 | 1.1 | Display heading (h1) |

---

## 4. Components

| Component | Purpose | Key variants |
|-----------|---------|-------------|
| Button | Primary CTA and secondary actions | Primary, Secondary, Ghost, Danger |
| Input | Text entry | Default, Error, Disabled |
| Badge | Status indicator | Success, Warning, Error, Info, Neutral |
| [Add more as needed] | — | — |

---

## 5. Layout

**Grid:** [12-col / 8-col] grid, [24px] gutters, [48px] margins at 1280px+

**Spacing base unit:** [4px / 8px]

**Breakpoints:**
| Name | Min-width | Notes |
|------|-----------|-------|
| Mobile | 0 | Single column, stacked |
| Tablet | 768px | 2-col, sidebar optional |
| Desktop | 1024px | Full grid active |
| Wide | 1280px | Max content width: [1200px] |

**Density mode:** [Compact / Default / Comfortable]

---

## 6. Depth

**Elevation scale:**
| Token | Value | Usage |
|-------|-------|-------|
| `shadow-none` | none | Flat surfaces |
| `shadow-sm` | 0 1px 3px rgba(0,0,0,0.12) | Cards, inputs |
| `shadow-md` | 0 4px 12px rgba(0,0,0,0.15) | Dropdowns, popovers |
| `shadow-lg` | 0 8px 24px rgba(0,0,0,0.18) | Modals, dialogs |

**Layering order (z-index):**
- Base content: 0
- Sticky headers/sidebars: 100
- Dropdowns: 200
- Modals: 300
- Toasts/notifications: 400

---

## 7. Do's and Don'ts

### Do
- [Project-specific rule 1]
- [Project-specific rule 2]
- [Add 3–8 more]

### Don't
- [Project-specific anti-pattern 1]
- [Project-specific anti-pattern 2]
- [Add 3–8 more]

---

## 8. Responsive

**Strategy:** Mobile-first. [Describe how the primary UI pattern adapts — e.g., "sidebar collapses to bottom nav on mobile"]

**Key adaptations:**
| Element | Mobile | Desktop |
|---------|--------|---------|
| Navigation | Bottom bar | Left sidebar |
| Data tables | Horizontal scroll | Full width |
| Modals | Full-screen sheet | Centered dialog |

---

## 9. Agent Prompt Guide

**When generating UI for this project, agents must:**
- Always reference tokens from Sections 2–6; never use raw hex or pixel values
- Respect the Visual Theme statement in Section 1 — every decision should be defensible against it
- Prefer existing components from Section 4 before proposing new ones
- Apply the Do's and Don'ts from Section 7 as hard rules

**Invariants — never change these without updating this file:**
- [e.g., "Brand color is always brand-50 on white backgrounds"]
- [e.g., "All primary actions use the Button/Primary component"]

**Open questions / known gaps:**
- [e.g., "Dark mode not yet defined — default to light mode only"]
```

## Field Guide

**Section 1 — Visual Theme** anchors every design decision that follows. The theme statement (`<adjective>, <adjective>, <noun>`) must be specific enough to reject decisions — if everything fits, it's too vague. References should be real, named sources so any team member can look them up and verify alignment. Do not include more than 5 references; synthesis is the goal, not a mood board dump.

**Section 2 — Color Palette** should be machine-readable: tokens with values, not just adjectives. List only the steps that are actually used in the product — unused steps add noise. Include both light and dark values if the project supports dark mode. Semantic colors must cover all four roles (success, warning, error, info) at minimum.

**Section 3 — Typography** must name fonts with full fallback stacks so agents can generate CSS directly. The type scale table is the single source of truth — if a size isn't in this table, it should not appear in the product. Include line-height in the table; it is not optional.

**Section 4 — Components** is a catalog, not full documentation. One row per component is sufficient here. Full component documentation lives in the DS or uSpec files. Mark components as "planned" if they exist in design but not yet in code.

**Section 5 — Layout** must commit to a grid and spacing base unit. Vague entries like "flexible grid" are not actionable. Agents need a number. If the project uses container queries, note that here.

**Section 6 — Depth** documents the elevation scale and z-index order. These two things together eliminate entire classes of stacking context bugs. Do not leave either table empty.

**Section 7 — Do's and Don'ts** must be project-specific, not generic. "Use consistent spacing" is not a Do for this section — it belongs in the shared knowledge files. Write rules that only apply to this product's specific decisions, risks, or brand constraints.

**Section 8 — Responsive** must describe actual behavior, not intent. "Mobile-friendly" is not a strategy. Name the specific pattern change at each breakpoint for the 2–3 most critical UI structures (navigation, data display, forms).

**Section 9 — Agent Prompt Guide** is the contract between this file and every agent that reads it. Invariants are non-negotiable rules that agents must not override. Open questions flag gaps so agents don't silently fill them with assumptions — they ask instead.
