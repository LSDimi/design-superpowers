# Component Patterns (L2)

> Loaded by /ds-make Component Builder, /design Component Selector, /map-design Component Cataloger.

## Composition Hierarchy

```
Primitives (tokens, icons, raw HTML) →
  Components (Button, Input, Card) →
    Patterns (Form, Table, Navigation) →
      Templates (Page layouts, full flows)
```

Each level consumes the level below. Never skip levels — a Pattern should use Components, not raw Primitives directly.

## Component API Design

### Props vs Variants Decision Tree

- Use a **variant prop** (enum) when the choice changes visual appearance and is mutually exclusive: `variant="primary|secondary|ghost"`
- Use a **boolean prop** when the option is an independent toggle: `disabled`, `loading`, `fullWidth`
- Use **separate components** when behavior diverges significantly (not just appearance): `Button` vs `IconButton`
- **Rule:** If adding a variant requires more than 3 conditional branches in rendering logic, split into two components.

### Slot Patterns

Slots allow content injection without prop explosion:
- **Named slots:** `leadingIcon`, `trailingAction`, `label` — use for predictable injection points
- **Default slot:** For arbitrary children (card body, dialog content)
- **Anti-pattern:** Never use slots for items that should be a variant (e.g., don't use a slot to swap a button's color)

### Compound Components

Use compound components when sub-parts need to communicate state:
```
<Select>
  <Select.Trigger />
  <Select.Content>
    <Select.Item />
  </Select.Content>
</Select>
```
Share state via context. Expose a single controlled API at the root (`value`, `onChange`, `open`).

## Variant Strategies

| Strategy | Use when | Example |
|----------|----------|---------|
| Enum variant | Mutually exclusive appearances | `size="sm|md|lg"` |
| Boolean modifier | Independent feature toggle | `rounded`, `elevated` |
| Compound component | Sub-parts need shared state | `Tabs`, `Select`, `Accordion` |
| Separate component | Behavior diverges significantly | `Button` vs `LinkButton` |

**Max variants per component:** Keep to ≤3 variant dimensions. Beyond that, consider splitting or composing.

## Naming Conventions

- **Components:** PascalCase, noun-based — `DatePicker`, `ActionMenu`, `EmptyState`
- **Props:** camelCase — `isDisabled`, `onChange`, `maxLength`, `leadingIcon`
- **Event handlers:** Verb prefix — `onChange`, `onSelect`, `onDismiss`
- **Micro components (internal):** `_` prefix — `_DropdownItem`, `_InputAdornment`
- **Avoid:** Abbreviations (`Btn`), numbered variants (`Button2`), client names in component names

## State Patterns

Every interactive component must define all applicable states:

| State | Visual requirement | Notes |
|-------|--------------------|-------|
| Default | Resting appearance | The baseline |
| Hover | Subtle highlight | Desktop only; don't rely on it for mobile |
| Focus | Visible focus ring (3:1 contrast min) | Required for keyboard users |
| Pressed / Active | Depressed or inverted feel | Confirms interaction |
| Disabled | Reduced opacity or muted palette | Not interactive; still readable |
| Loading | Spinner or skeleton replacement | Maintain layout; avoid CLS |
| Error | Red/danger semantic color; error message | Never color-only signal |
| Empty | Placeholder content or empty state component | Never show blank |

## Responsiveness

- **Fluid by default:** Components stretch to fill their container unless a max-width is set.
- **Breakpoint strategy:** Define at the Pattern/Template level, not inside components — components should be layout-agnostic.
- **Touch targets:** Minimum 44×44px interactive area (WCAG 2.5.5).
- **Density modes:** Support `compact|default|comfortable` via a density token or context prop, not hardcoded padding.

## Composition Patterns

**Composition over configuration:** Prefer accepting children and slots over adding one-off props for every use case.

**Controlled vs Uncontrolled:**
- Default to uncontrolled (internal state) for simple cases
- Always allow controlled override via `value` + `onChange` pair
- Never mix controlled/uncontrolled — if `value` is passed, the component is fully controlled

**Anti-patterns:**
- God components with 30+ props — split them
- Coupling layout into a component (margins, widths baked in)
- Using `index` as key in lists of mutable items
- Exposing internal implementation detail props (`__internalVariant`)
