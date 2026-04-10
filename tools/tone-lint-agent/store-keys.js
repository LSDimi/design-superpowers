// store-keys.js — Run via use_figma on ANY file (e.g. the target product file)
// Stores the merged library key map in clientStorage.
// Agent replaces __KEY_MAP_JSON__ with the merged map before running.

const keyMap = __KEY_MAP_JSON__;
await figma.clientStorage.setAsync("tc_library_keys", JSON.stringify(keyMap));
return "Library key map stored: " + Object.keys(keyMap.componentKeys).length + " components, " + Object.keys(keyMap.styleKeys).length + " styles";
