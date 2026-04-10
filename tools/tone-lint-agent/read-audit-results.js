// read-audit-results.js — ~50 tokens to read
// Run via use_figma on the file that was audited
return figma.root.getSharedPluginData("tone_lint", "audit_results") || '{"error": "No audit results found. Run Tone Lint Auditor first."}';
