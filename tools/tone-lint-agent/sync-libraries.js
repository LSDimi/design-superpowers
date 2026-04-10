// sync-libraries.js — Run via use_figma on ONE Tone library file
// Returns all component keys and style keys from this file.
// Agent runs this on each library file, merges results, then stores via store-keys.js.

async function collectKeys() {
  const components = [];
  const styles = [];

  // Collect component keys from all pages
  for (const page of figma.root.children) {
    await page.loadAsync();
    const comps = page.findAll(n => n.type === "COMPONENT" || n.type === "COMPONENT_SET");
    for (const c of comps) {
      components.push({ key: c.key, name: c.name });
    }
  }

  // Collect style keys
  const textStyles = await figma.getLocalTextStylesAsync();
  const effectStyles = await figma.getLocalEffectStylesAsync();
  const gridStyles = await figma.getLocalGridStylesAsync();

  for (const s of textStyles) styles.push({ key: s.key, name: s.name, type: "text" });
  for (const s of effectStyles) styles.push({ key: s.key, name: s.name, type: "effect" });
  for (const s of gridStyles) styles.push({ key: s.key, name: s.name, type: "grid" });

  return { fileName: figma.root.name, components, styles };
}

const result = await collectKeys();
return JSON.stringify(result);
