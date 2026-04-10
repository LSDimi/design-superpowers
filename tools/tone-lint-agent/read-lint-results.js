// read-lint-results.js — ~50 tokens to read
// Run via use_figma on the file that was linted
return figma.root.getSharedPluginData("tone_lint", "lint_results") || '{"error": "No lint results found. Run Tone Lint plugin first."}';
