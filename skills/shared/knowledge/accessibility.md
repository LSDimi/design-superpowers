# Accessibility (L2)

> Loaded by /design-review A11y Auditor. Reference standard: WCAG 2.1 Level AA.

## WCAG 2.1 AA Checklist (by POUR)

### Perceivable

| Criterion | ID | Requirement | Common failure |
|-----------|-----|-------------|----------------|
| Text alternatives | 1.1.1 | All non-text content has a text alternative | Decorative images lack `alt=""`, icons lack accessible label |
| Captions | 1.2.2 | Pre-recorded video has captions | Video without captions |
| Audio description | 1.2.5 | Pre-recorded video has audio description | Visual-only information in video |
| Adaptable | 1.3.1 | Info and relationships conveyed through presentation can also be programmatically determined | Layout tables, missing heading hierarchy, no form labels |
| Sensory characteristics | 1.3.3 | Instructions don't rely solely on sensory characteristics (shape, color, size, position) | "Click the red button" |
| Orientation | 1.3.4 | Content doesn't restrict orientation | Forced landscape or portrait |
| Input purpose | 1.3.5 | Input fields identify their purpose for autocomplete | Missing `autocomplete` attributes |
| Use of color | 1.4.1 | Color is not the only means of conveying info | Red-only error indicator |
| Audio control | 1.4.2 | Audio that plays auto has a stop/pause mechanism | Autoplaying video with sound |
| Text contrast | 1.4.3 | Text contrast ≥ 4.5:1 (normal), 3:1 (large text ≥18pt/14pt bold) | Low contrast placeholder text |
| Non-text contrast | 1.4.11 | UI components and focus indicators ≥ 3:1 against adjacent colors | Low contrast button border |
| Resize text | 1.4.4 | Text can be resized to 200% without loss of content | Fixed-pixel containers that clip text |
| Reflow | 1.4.10 | Content reflows at 320px width without horizontal scroll | Broken layout at small widths |
| Text spacing | 1.4.12 | Content works with increased letter/word/line spacing | Text overflow when spacing adjusted |

### Operable

| Criterion | ID | Requirement | Common failure |
|-----------|-----|-------------|----------------|
| Keyboard accessible | 2.1.1 | All functionality available via keyboard | Mouse-only custom dropdowns |
| No keyboard trap | 2.1.2 | Keyboard focus can always be moved away | Modal without focus trap exit |
| Skip links | 2.4.1 | Mechanism to skip repeated navigation | No skip-to-main-content link |
| Page titled | 2.4.2 | Pages have descriptive titles | Generic `<title>App</title>` |
| Focus order | 2.4.3 | Focus order preserves meaning and operability | DOM order doesn't match visual order |
| Link purpose | 2.4.4 | Link purpose is determinable from link text or context | "Click here" or "Read more" links |
| Visible focus | 2.4.7 | Keyboard focus indicator is visible | `outline: none` with no replacement |
| Focus appearance | 2.4.11 | Focus indicator area ≥ perimeter of component (WCAG 2.2) | 1px outline only |
| Pointer gestures | 2.5.1 | Multipoint gestures have single-pointer alternatives | Pinch-only zoom |
| Touch target size | 2.5.5 | Touch targets ≥ 44×44px | 24px icon buttons without padding |
| Timing adjustable | 2.2.1 | Users can extend or disable time limits | Session timeout with no warning |
| Pause motion | 2.2.2 | Moving or auto-updating content can be paused | Autoplaying carousel |

### Understandable

| Criterion | ID | Requirement | Common failure |
|-----------|-----|-------------|----------------|
| Language of page | 3.1.1 | Default language of page is programmatically set | Missing `lang` attribute on `<html>` |
| On focus | 3.2.1 | Focus alone doesn't trigger context change | Select dropdown submits on focus |
| On input | 3.2.2 | Changing a setting doesn't auto-submit form | Auto-submit on radio change |
| Error identification | 3.3.1 | Input errors identified and described in text | "Invalid" with no explanation |
| Labels or instructions | 3.3.2 | Labels or instructions provided for user input | Unlabeled form fields |
| Error suggestion | 3.3.3 | Error messages suggest correction when known | "Error" only; no fix guidance |
| Error prevention | 3.3.4 | Submissions are reversible, checked, or confirmed | Permanent deletion with no undo |

### Robust

| Criterion | ID | Requirement | Common failure |
|-----------|-----|-------------|----------------|
| Parsing | 4.1.1 | Valid HTML — no duplicate IDs, properly nested | Duplicate form element IDs |
| Name, role, value | 4.1.2 | UI components have accessible name, role, state | Custom components without ARIA |
| Status messages | 4.1.3 | Status messages programmatically determined | Toast notifications without live region |

## Contrast Ratios Quick Reference

| Context | Minimum ratio | Enhanced (AAA) |
|---------|--------------|----------------|
| Body text (< 18pt normal / < 14pt bold) | **4.5:1** | 7:1 |
| Large text (≥ 18pt or ≥ 14pt bold) | **3:1** | 4.5:1 |
| UI components (borders, icons, controls) | **3:1** | — |
| Focus indicators | **3:1** against adjacent color | — |

**Tools:** Figma plugins — A11y Annotation Kit, Stark, Color Contrast Checker. CLI — `axe-core`, `pa11y`.

## Keyboard Patterns

- **Focus order:** Matches reading order (top-left → right → down). Never use `tabindex > 0`.
- **Focus trap (modals/dialogs):** Trap focus within the open dialog. Release on close. `Escape` always closes.
- **Skip links:** Provide "Skip to main content" as first focusable element. Can be visually hidden until focused.
- **Roving tabindex:** For composite widgets (tabs, toolbars, radio groups) — one `tabindex="0"` in group, rest are `-1`. Arrow keys navigate within.

## ARIA Patterns

**Use semantic HTML first; ARIA is a fallback.**

| Need | Prefer | ARIA fallback |
|------|--------|---------------|
| Navigation | `<nav>` | `role="navigation"` |
| Main content | `<main>` | `role="main"` |
| Button | `<button>` | `role="button"` + keyboard handler |
| Status update | — | `role="status"` or `aria-live="polite"` |
| Alert (urgent) | — | `role="alert"` or `aria-live="assertive"` |
| Label | `<label for>` | `aria-label` or `aria-labelledby` |
| Description | — | `aria-describedby` |
| Hidden (decorative) | — | `aria-hidden="true"` |
| Required | `required` | `aria-required="true"` |
| Invalid | — | `aria-invalid="true"` + `aria-describedby` pointing to error |
| Expanded | — | `aria-expanded="true|false"` |

**Live regions:** Use `aria-live="polite"` for non-urgent updates (search results loaded). Use `aria-live="assertive"` only for critical errors. Never use assertive for routine status.

## Screen Reader Patterns

- Semantic HTML headings (`h1`–`h6`) form the document outline — verify heading hierarchy.
- Form inputs always have associated `<label>` (not just placeholder text).
- Icon-only buttons need `aria-label`: `<button aria-label="Close dialog">`.
- Data tables need `<caption>` and `scope` attributes on `<th>`.
- Dynamic content injected into DOM must be in or announce to a live region.

## Motion Accessibility

- **`prefers-reduced-motion`:** Wrap all non-essential animations. Provide instant alternatives.
- **No content flashing** above 3 times per second (seizure trigger — WCAG 2.3.1).
- **No infinite animations** without user control.
- **Parallax and vestibular triggers:** Reduce or remove scrolling animations behind `prefers-reduced-motion`.

## Evaluation Output Format

| # | WCAG Criterion | Location | Issue | Severity | Fix |
|---|---------------|----------|-------|----------|-----|
| 1 | 1.4.3 Contrast | Search input placeholder | Placeholder text is `gray.300` on white — ratio 2.1:1 | P0 | Use `gray.500` minimum (4.5:1 achieved) |
| 2 | 4.1.2 Name, role | Icon-only delete button | No accessible name; screen reader announces "button" only | P0 | Add `aria-label="Delete campaign"` |
| 3 | 2.4.7 Visible Focus | Primary nav links | `outline: none` with no replacement focus style | P1 | Add 2px offset focus ring at 3:1 contrast |

## L3 Lookup

When you need a deeper reference during evaluation, query these CSVs with Grep:

- `skills/shared/data/psychological-principles.csv` — cognitive + perceptual principles
- `skills/shared/data/ecommerce-usability.csv` — forms, checkout, search patterns
- `skills/shared/data/usability-homepage.csv` — homepage, nav, filtering patterns
- `skills/shared/data/design-principles.csv` — classic design frameworks

**Query pattern:** `Grep pattern="<keyword>" path="skills/shared/data/<file>.csv"`
**Use sparingly:** Query only when a specific finding needs backing, not speculatively.
