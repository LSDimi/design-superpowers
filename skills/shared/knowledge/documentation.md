# Documentation (L2)

> Loaded by /ds-manage Documentation Generator sub-agent. Covers uSpec templates, property table format, demo area structure, coverage checklist, and anti-patterns.

## uSpec Templates

uSpec is the DS documentation format. Each template covers one aspect of a component's specification. Use only the templates that apply — not every component needs all seven.

### API Spec Template
Documents the component's programmatic interface.
```markdown
## API Spec

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `variant` | `"primary" \| "secondary" \| "ghost"` | `"primary"` | No | Visual variant of the button |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` | No | Height and padding scale |
| `disabled` | `boolean` | `false` | No | Prevents interaction; applies disabled styling |
| `onClick` | `() => void` | — | No | Callback fired on click or Enter/Space key |
```

### Anatomy Template
Labels every visible part of the component with a name used consistently across all documentation.
```markdown
## Anatomy

1. **Container** — outer bounding box; applies padding and border radius
2. **Leading icon** (optional) — 16px icon to the left of the label
3. **Label** — required text; uses `text-sm` token
4. **Trailing icon** (optional) — 16px icon to the right of the label (used for dropdowns, external links)
5. **Spinner** (conditional) — replaces label during loading state
```

### Component Properties Template
Table format for Figma component properties (mirrors Prostar plugin output).
```markdown
## Component Properties

| Property | Values | Default | Description |
|----------|--------|---------|-------------|
| Variant | Primary, Secondary, Ghost, Danger | Primary | — |
| Size | SM, MD, LG | MD | — |
| State | Default, Hover, Pressed, Disabled, Loading | Default | — |
| Leading icon | Boolean | False | Shows leading icon slot |
| Trailing icon | Boolean | False | Shows trailing icon slot |
```

### Color Annotation Template
Documents all color tokens used within the component across states.
```markdown
## Color Tokens

| Element | State | Token | Value (light) | Value (dark) |
|---------|-------|-------|--------------|--------------|
| Background | Default | `color.bg.brand.default` | `brand-60` | `brand-40` |
| Background | Hover | `color.bg.brand.hover` | `brand-70` | `brand-30` |
| Label | Default | `color.text.on-brand` | `neutral-0` | `neutral-0` |
| Border | Focus | `color.border.focus` | `brand-50` | `brand-50` |
```

### Structure Template
Documents layout and spacing within the component.
```markdown
## Structure

| Element | Token | Value |
|---------|-------|-------|
| Horizontal padding | `space-3` | 12px (4px base) |
| Vertical padding (MD) | `space-2` | 8px |
| Gap (icon to label) | `space-1` | 4px |
| Border radius | `radius-md` | 6px |
| Min height (MD) | — | 36px |
```

### Screen Reader Template
Documents the accessible experience for assistive technology.
```markdown
## Screen Reader Behavior

- **Role:** `button`
- **Name:** Computed from label text; if icon-only, requires `aria-label`
- **State announcements:** `aria-disabled="true"` when disabled; `aria-busy="true"` when loading
- **Loading state:** Announce "Loading" via `aria-live="polite"` on status region; suppress button label during load
- **Keyboard:** `Enter` and `Space` activate; no trapping behavior
```

### Motion Template
Documents animation behavior within the component.
```markdown
## Motion

| Trigger | Property | Duration | Easing |
|---------|----------|----------|--------|
| Hover enter | `background-color` | `duration-micro` (100ms) | `ease-out` |
| Hover exit | `background-color` | `duration-micro` (100ms) | `ease-in` |
| Press | `transform: scale(0.97)` | `duration-micro` (100ms) | `ease-in-out` |
| Loading enter | `opacity` on spinner | `duration-small` (200ms) | `ease-out` |
```

## Property Table Format

When writing property tables outside a formal uSpec context, use this compact format:

| Name | Type | Default | Description | Example |
|------|------|---------|-------------|---------|
| `variant` | string enum | `"primary"` | Visual treatment of the component | `variant="ghost"` |
| `size` | string enum | `"md"` | Affects height, padding, and font size | `size="lg"` |
| `disabled` | boolean | `false` | Disables interaction and applies muted style | `disabled={true}` |

Rules:
- Type should be specific: `boolean`, `string`, `number`, string enum (`"a" | "b" | "c"`), or `ReactNode`.
- Default must be listed; use `—` for required props with no default.
- Description: one sentence, no "This prop...". Just the effect.
- Example: show the prop in use.

## Demo Area Structure

Every component in the DS should have a demo area in Figma with these sections in order:

1. **Overview** — one-line description + primary use case
2. **Usage** — canonical example of the component in context (not isolated)
3. **Variants** — all supported variants side-by-side with labels
4. **States** — Default, Hover, Focus, Pressed, Disabled, Loading, Error (as applicable)
5. **Accessibility** — keyboard behavior note, screen reader annotation
6. **Do / Don't** — 2–4 paired examples showing correct vs. incorrect usage

Keep demo areas in the Figma "Demo Area" file (see `skills/shared/tone-ds-context.md` for file key).

## Coverage Checklist

Before marking a component as documented:

- [ ] API Spec table complete (all props, types, defaults)
- [ ] Anatomy labels match the Figma component layer names
- [ ] All states shown in demo area (minimum: default, disabled, focus)
- [ ] All color tokens documented in Color Annotation template
- [ ] Structure tokens documented (padding, gap, radius, min-height)
- [ ] Screen reader behavior documented
- [ ] Motion documented (or explicitly noted as "no animation")
- [ ] Do / Don't examples present (minimum 2 pairs)
- [ ] "When to use / when not to use" guidance written
- [ ] Related components referenced ("see also: IconButton, Link")

## Anti-Patterns

| Anti-pattern | Problem | Fix |
|-------------|---------|-----|
| **Undocumented props** — component has 8 props but docs show 4 | Consumers guess behavior; bugs follow | Export full prop type and diff against docs table |
| **Missing "when to use"** — shows variants but no guidance | Consumers pick arbitrarily; inconsistent UI | Write 2–3 sentences: correct context, incorrect context |
| **Examples without context** — isolated component on white background | Hard to understand real usage | Show the component inside a realistic layout (form, card, navigation) |
| **Out-of-date docs** — docs written at v1, component is at v3 | Misinforms consumers; erodes trust | Docs update is part of the component PR — never separate |
| **Copy-pasting API from code without editing** — raw TypeScript types | Unreadable for design consumers | Translate types to plain language in the Description column |
