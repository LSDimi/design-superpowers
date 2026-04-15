#!/usr/bin/env python3
"""Validate the design-superpowers Claude Code plugin.

Checks:
  1. .claude-plugin/plugin.json is valid JSON with required fields.
  2. Every skills/<name>/SKILL.md has valid YAML frontmatter with name + description.
  3. Every ${CLAUDE_PLUGIN_ROOT}/... path referenced in a SKILL.md or shared/*.md
     resolves to a real file on disk.
  4. No bare skills/shared/ references remain (must use ${CLAUDE_PLUGIN_ROOT}).

Exits 0 on success, 1 on any failure. Prints all errors before exiting.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"
SKILLS_DIR = ROOT / "skills"

REQUIRED_PLUGIN_FIELDS = {"name", "description", "version"}
REQUIRED_SKILL_FRONTMATTER = {"name", "description"}

# Files that reference paths in prose/diagrams, not runtime file loads.
DOC_ONLY_FILES = {"skills/README.md"}

PATH_REF_RE = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([A-Za-z0-9_./-]+)")
BARE_SHARED_RE = re.compile(r"(?<!\{CLAUDE_PLUGIN_ROOT\}/)skills/shared/")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def validate_plugin_json(errors: list[str]) -> None:
    if not PLUGIN_JSON.exists():
        errors.append(f"missing {PLUGIN_JSON.relative_to(ROOT)}")
        return
    try:
        data = json.loads(PLUGIN_JSON.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"{PLUGIN_JSON.relative_to(ROOT)}: invalid JSON ({exc})")
        return
    missing = REQUIRED_PLUGIN_FIELDS - set(data.keys())
    if missing:
        errors.append(
            f"{PLUGIN_JSON.relative_to(ROOT)}: missing fields {sorted(missing)}"
        )


def validate_skill_frontmatter(errors: list[str]) -> list[Path]:
    skill_files: list[Path] = []
    if not SKILLS_DIR.exists():
        errors.append(f"missing {SKILLS_DIR.relative_to(ROOT)}")
        return skill_files
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        skill_files.append(skill_md)
        fields = parse_frontmatter(skill_md.read_text())
        if not fields:
            errors.append(f"{skill_md.relative_to(ROOT)}: missing YAML frontmatter")
            continue
        missing = REQUIRED_SKILL_FRONTMATTER - set(fields.keys())
        if missing:
            errors.append(
                f"{skill_md.relative_to(ROOT)}: missing frontmatter fields {sorted(missing)}"
            )
    return skill_files


def iter_markdown_files() -> list[Path]:
    return [
        p
        for p in SKILLS_DIR.rglob("*.md")
        if str(p.relative_to(ROOT)) not in DOC_ONLY_FILES
    ]


def validate_path_references(errors: list[str]) -> None:
    for md in iter_markdown_files():
        rel = md.relative_to(ROOT)
        text = md.read_text()
        for match in PATH_REF_RE.finditer(text):
            ref = match.group(1).rstrip(".,;:)")
            target = ROOT / ref
            if not target.exists():
                errors.append(f"{rel}: broken path reference -> {ref}")
        for match in BARE_SHARED_RE.finditer(text):
            line_no = text[: match.start()].count("\n") + 1
            errors.append(
                f"{rel}:{line_no}: bare 'skills/shared/' reference "
                "(use ${CLAUDE_PLUGIN_ROOT}/skills/shared/ instead)"
            )


def main() -> int:
    errors: list[str] = []
    validate_plugin_json(errors)
    validate_skill_frontmatter(errors)
    validate_path_references(errors)

    if errors:
        print("Plugin validation failed:\n")
        for err in errors:
            print(f"  - {err}")
        print(f"\n{len(errors)} error(s)")
        return 1

    print("Plugin validation OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
