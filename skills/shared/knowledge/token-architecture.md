# Token Architecture (L2)

> Loaded by /ds-make Token Architect, /map-design Token Extractor. See the `tone-example` branch for a fully populated enterprise-tier implementation example.

## 3-Tier Model

```
Primitive → Semantic → Component
```

| Tier | Purpose | Example | Mutability |
|------|---------|---------|------------|
| **Primitive** | Raw values; named by value | `color.blue.500 = #3B82F6` | Stable — rarely change |
| **Semantic** | Roles and intent; context-neutral | `color.action.primary = {color.blue.500}` | Change when brand/theme changes |
| **Component** | Specific usage in one component | `button.bg.primary = {color.action.primary}` | Change when component design changes |

**Rule:** Always reference the tier above, never skip. A component token references a semantic token, which references a primitive. Never reference a primitive directly in component code.

## Naming Convention

Pattern: `<category>.<property>.<role>.<state>.<scale>`

| Segment | Optional? | Examples |
|---------|-----------|---------|
| `category` | No | `color`, `space`, `size`, `radius`, `shadow`, `font`, `duration` |
| `property` | No | `bg`, `text`, `border`, `icon`, `outline` |
| `role` | No | `primary`, `secondary`, `danger`, `success`, `neutral` |
| `state` | Yes | `default`, `hover`, `active`, `disabled`, `focus` |
| `scale` | Yes | `sm`, `md`, `lg`; or `100`–`900` for primitives |

**Examples:**
- `color.bg.primary` → semantic, no state
- `color.bg.primary.hover` → semantic with state
- `color.blue.500` → primitive (value-named)
- `space.inset.md` → spacing primitive
- `button.bg.primary.hover` → component token

## Collection Structure

Organize tokens into collections by category:

| Collection | Contains |
|------------|---------|
| `color` | All primitive color scales + semantic color roles |
| `space` | Spacing scale (base 4px or 8px), inset/stack/inline variants |
| `size` | Width/height sizing scale, icon sizes |
| `typography` | Font families, sizes, weights, line heights, letter spacing |
| `radius` | Border radius scale (none, sm, md, lg, full) |
| `shadow` | Elevation levels (0–5) with shadow values |
| `duration` | Animation timing tokens (micro, small, medium, large) |
| `easing` | Named easing curves (ease-in, ease-out, spring) |

## Dark Mode Strategy

- **Primitive tokens are stable** — same raw values exist in both modes.
- **Semantic tokens swap** — `color.bg.surface` maps to `gray.50` in light and `gray.900` in dark.
- **Never** create separate "dark" primitive scales. Invert lightness within the same scale.
- **Implementation:** Use a `mode` collection in Figma (or CSS `prefers-color-scheme`) — swap the semantic token → value mappings, not the primitives.

## Extraction Heuristics

When looking at a design, identify what should become a token:

1. **Recurring values:** Same hex color used 3+ times → semantic token candidate
2. **Role-carrying values:** A color that always means "error" → semantic token, not primitive direct use
3. **Magic numbers:** A spacing value like `12px` not in the scale → extract to `space.inset.sm` or similar
4. **State pairs:** If you see `bg` change on hover → both states are tokens, not ad-hoc overrides
5. **Responsive values:** Size/spacing that changes at breakpoints → parameterize as scale tokens

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Primitive in component code | Bypasses semantic layer; breaks theme switching | Always go Primitive → Semantic → Component |
| Hardcoded hex in component | `background: #3B82F6` — no token | Extract to semantic token |
| Duplicate semantic roles | `action-blue` and `primary-blue` for same intent | Consolidate under one semantic name |
| Magic numbers | `padding: 13px` not in spacing scale | Round to nearest scale step |
| Over-granular component tokens | One token per component property | Only create component tokens where the semantic default is wrong for that component |
| Under-granular primitives | Jumping from `blue.100` to `blue.900` | 11-step scale: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950 |
