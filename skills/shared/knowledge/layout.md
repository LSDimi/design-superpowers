# Layout (L2)

> Loaded by /creative Layout Strategist, /design Layout Composer. Covers grids, spacing rhythm, breakpoints, density modes, and composition patterns.

## Grid Systems

**12-column grid** — most flexible for product UI. Column width is fluid; gutters and margins are fixed.

| Context | Columns | Gutter | Margin |
|---------|---------|--------|--------|
| Desktop (≥1280px) | 12 | 24px | 48px |
| Tablet (768–1279px) | 8 | 16px | 24px |
| Mobile (<768px) | 4 | 16px | 16px |

**8-column grid** — simpler, good for dashboards and data-heavy interfaces where 12 columns create too many narrow cells.

**Fluid grid** — no fixed columns; sections defined as fractions (`fr`) of available space. Use for full-width layouts, marketing pages, and responsive containers.

**CSS Grid vs. Flexbox — decision rule:**

| Use CSS Grid when | Use Flexbox when |
|-------------------|-----------------|
| Two-dimensional layout (rows AND columns) | One-dimensional (row OR column) |
| Layout-first (items fit the grid) | Content-first (grid fits the content) |
| Page-level structure, card grids | Navigation bars, button groups, form rows |

Never nest CSS Grid inside CSS Grid more than 2 levels deep without clear reason — complexity compounds quickly.

## Spacing Rhythm

**Base unit:** 4px or 8px. Choose one per project. 4px gives more granularity (good for compact UIs); 8px forces larger, more deliberate spacing (good for airy, editorial interfaces).

**T-shirt sizing — map to tokens, never raw values:**

| Token | 4px base | 8px base | Usage |
|-------|----------|----------|-------|
| `space-1` | 4px | 8px | Inline gap between icon + label |
| `space-2` | 8px | 16px | Padding inside small components |
| `space-3` | 12px | 24px | Padding inside standard components |
| `space-4` | 16px | 32px | Section padding, card gap |
| `space-5` | 24px | 40px | Major section separation |
| `space-6` | 32px | 48px | Page-level padding, large gaps |
| `space-8` | 48px | 64px | Hero whitespace, display sections |

**Spacing pattern vocabulary:**

- **Inset** — padding inside a container (`padding: space-3` on all sides; `inset-squish` for asymmetric top/bottom vs left/right)
- **Stack** — vertical space between elements in a column (`margin-bottom` or `gap` in flex column)
- **Inline** — horizontal space between elements in a row (`margin-right` or `gap` in flex row)

Always use `gap` on flex/grid containers rather than margin on children — it avoids double-margin issues and is easier to override.

## Responsive Breakpoints

**Mobile-first approach:** write base styles for mobile, add `min-width` media queries for larger viewports.

| Breakpoint | Name | Min-width | Typical use |
|------------|------|-----------|-------------|
| Default | Mobile | — | Stack everything, single column |
| `sm` | Mobile large | 480px | Adjust typography, 2-col card grid |
| `md` | Tablet | 768px | Sidebar appears, nav expands |
| `lg` | Desktop | 1024px | 12-col grid activates |
| `xl` | Wide desktop | 1280px | Max content width applied |
| `2xl` | Ultra-wide | 1536px | Margins grow; content stays contained |

**Container queries** — prefer over media queries for component-level layout. A card should reflow based on its container width, not the viewport. Use `@container` for components that appear in varying layout contexts (sidebar, full-width, modal).

## Density Modes

Three modes adapt the same layout to different user needs. Toggle via a token set or CSS class at the root.

| Mode | Space multiplier | Target user |
|------|-----------------|-------------|
| **Compact** | 0.75× base spacing | Power users, data operators, small screens |
| **Default** | 1× base spacing | Most users, standard desktop |
| **Comfortable** | 1.25× base spacing | Accessibility needs, touch interfaces |

Implementation: define spacing tokens as CSS custom properties; density mode changes the root multiplier. Components use relative tokens — they automatically adapt without code changes.

## Composition Patterns

Common full-page layout patterns. Each has a preferred CSS approach.

| Pattern | Description | CSS approach |
|---------|-------------|-------------|
| **Sidebar + main** | Fixed-width sidebar, fluid main content | Grid: `grid-template-columns: 240px 1fr` |
| **Split view** | Two equal (or ratio) panels, both scrollable | Grid: `grid-template-columns: 1fr 1fr` with `overflow: auto` on each |
| **Card grid** | Equal-width cards that reflow | Grid: `repeat(auto-fill, minmax(280px, 1fr))` |
| **List-detail** | Narrow list + wide detail (master-detail) | Grid: `grid-template-columns: 320px 1fr`; detail replaces on mobile |
| **Master-detail (stacked)** | Mobile: list → push to detail. Desktop: side-by-side | CSS Grid + conditional `display: none` on mobile |
| **Full-bleed hero** | Content spans full viewport width | `margin: 0 calc(-1 * var(--page-margin))` or grid escape |

**Pattern selection heuristic:** Start with the user's primary task. If it's navigating a list to take action on one item → List-detail. If it's comparing two states → Split view. If it's browsing a collection → Card grid.

## Anti-Patterns

| Anti-pattern | Problem | Fix |
|-------------|---------|-----|
| **Mixed base units** — some components use 4px, others 8px | Spacing inconsistency; nothing aligns | Audit and pick one base unit; re-token all components |
| **Absolute pixel spacing in components** — `margin: 13px` | Can't scale with density modes; breaks on zoom | Replace with spacing tokens |
| **Competing grids** — two overlapping column grids | Elements misalign visually | One grid per layout level; nest only with clear containment |
| **Breakpoint-first component design** — components designed only at 1440px | Breaks at real device widths | Design components at 375px and 1024px minimum |
| **Using both margin and gap** — margin on children AND gap on container | Double spacing; brittle | Choose one: `gap` on container is preferred |
