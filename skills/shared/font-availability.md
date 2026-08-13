# Font Availability (shared helper)

> Used by /creative Typography Director (recommend from what exists), /map-design (verify DESIGN.md fonts), /design-review (flag missing fonts), and any sub-agent about to name a typeface in a deliverable. Answers two questions: **what fonts does this user actually have**, and **is a named font usable here**?

A font recommendation the user can't render is a broken deliverable. Every named typeface in output gets one of three availability marks:

| Mark | Meaning | Behavior |
|------|---------|----------|
| `[installed]` | Present on the user's machine | Safe for code and local design work |
| `[figma]` | Available in the user's Figma (Google Fonts or shared org fonts) but not installed locally | Safe for Figma work; flag for code handoff (needs webfont or install) |
| `[needs-install]` | Not found in either inventory | Still recommendable — but must ship with a source (Google Fonts / Fontshare / foundry) and license note, plus the closest available fallback |

## Probe 1 — Local fonts (cache-first)

1. If `.ds-context.md` has `fonts.inventory_path` and the file exists and `fonts.last_scan` is under 30 days old, use the cached inventory. Otherwise scan and refresh the cache.
2. Scan (macOS) — **recursively**, subfolders matter: `find /System/Library/Fonts /Library/Fonts ~/Library/Fonts -type f \( -name "*.ttf" -o -name "*.otf" -o -name "*.ttc" \) 2>/dev/null`. The classic Apple faces (Futura, Didot, Baskerville, Rockwell, Zapfino…) live in `/System/Library/Fonts/Supplemental/` — a non-recursive `ls` misses ~300 files and produces false "not installed" verdicts. Derive family names from filenames (strip extension and weight/style suffixes like `-Bold`, `Italic`, `_Light`; collapse hyphens/underscores to spaces).
   - Exact pass (only when a name is ambiguous): `system_profiler SPFontsDataType -json` yields true family names — slow (seconds), use to confirm a specific candidate, never for the full scan.
   - Linux: `fc-list : family | sort -u`. Windows: `Get-ChildItem C:\Windows\Fonts` + user fonts under `%LOCALAPPDATA%\Microsoft\Windows\Fonts`.
3. Write one family per line to the inventory file (`fonts.inventory_path`, default `fonts-inventory.txt` at project root — add it to `.gitignore`), and set `fonts.last_scan` (ISO date) in `.ds-context.md`. At L0/L1 (no `.ds-context.md`), keep the inventory in memory for the session and offer to save it.

## Probe 2 — Figma fonts (only when the deliverable is Figma work)

Route through the configured Figma adapter (`figma-adapter.md`). With PluginOS connected:

```
execute_figma: const fams = [...new Set((await figma.listAvailableFontsAsync()).map(f => f.fontName.family))];
return fams.slice(0, 200).join('|')   // then further calls with .slice(200, 400) etc. until exhausted
```

Chunk the return by index (fixed-size slices) joined as a flat string — the bridge's serializer truncates deep structures, and flat strings survive. Cache alongside the local inventory (`fonts.figma_inventory_path`, default `fonts-figma.txt`). If no bridge, skip this probe and say so — never guess Figma availability.

## Matching rule

Normalize both sides before comparison: lowercase, strip weight/style words (hairline/thin/extralight/ultralight/light/regular/medium/semibold/demibold/bold/extrabold/black/heavy/italic/oblique/condensed), collapse whitespace/hyphens, and **also compare with ALL spaces removed** — filenames are often CamelCase (`AmericanTypewriter.ttc` must match "American Typewriter"). `SF-Pro-Display-Semibold.otf` and "SF Pro Display" must match. Compare with **word-boundary token matching — never raw substring**: every token of the requested name must appear as a whole word in the candidate's tokens. "Inter" matches "Inter Display" (variant of the family) but not "SignPainter" (no word boundary); "SF Pro" matches "SF Pro Text". Prefer the exact-equality candidate when several match. On uncertain matches, verify with the exact pass rather than claiming availability.

## Classification Resolver

When a context row, style recipe, or archetype names a typography *class* ("old-style serif", "geometric sans", "condensed athletic"), resolve it deterministically:

1. Grep `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/typography-styles.csv` for the class. When you know the class name, anchor to the row start (`Grep pattern="^Humanist Sans" -i`) so sibling rows ("Geometric Sans", "Neo-Grotesque Sans") don't collide; use unanchored keyword grep only for discovery (rows carry synonyms and serves-hooks as keywords).
2. Walk the row's **ranked candidates in order**; the first candidate present in the user's inventory (local — or Figma inventory for Figma deliverables) is the working choice, marked `[installed]`/`[figma]`.
3. If a higher-ranked candidate is genuinely better for the brief but absent, recommend it `[needs-install]` (source + license from the row) **and** name the first-available candidate as the working substitute — the user gets both the ideal and the usable-today option.
4. If NO candidate is available (rare — every class carries a macOS-bundled fallback), fall back to the row's closest sibling class and say so.

The resolver makes class → font deterministic; taste still chooses *which class* serves the theme.

## Behavior contracts

- **Typography Director:** run Probe 1 (and Probe 2 for Figma deliverables) before recommending. Prefer strong `[installed]`/`[figma]` candidates when they serve the theme equally well; never let availability veto a clearly better typeface — recommend it as `[needs-install]` with source + license + fallback. Every font in the output spec carries its mark.
- **/map-design:** when generating or refreshing DESIGN.md, check every named font against the inventories; annotate missing ones inline (`Newsreader (not installed — source: Google Fonts)`) so the gap is recorded where the font is defined.
- **/design-review:** a DESIGN.md or spec font that is neither `[installed]` nor `[figma]` is a **P2 finding** ("design language names a font the environment cannot render") with the install source as the fix. Escalate to P1 if the missing font is the primary UI face of a shipping product.
- **Respect the scan budget:** probes run once per session at most (cache-first). Never re-scan per recommendation.

## .ds-context.md fields (see ds-context-schema.md)

```yaml
fonts:
  inventory_path: fonts-inventory.txt      # local families, one per line
  figma_inventory_path: fonts-figma.txt    # Figma-available families (optional)
  last_scan: 2026-07-13                    # refresh when > 30 days
```
