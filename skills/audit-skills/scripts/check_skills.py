#!/usr/bin/env python3
"""Checks the skills of a plugin repo against the mechanical conventions.

Usage: check_skills.py <repo-path>
Prints one line per finding: LEVEL<TAB>skill<TAB>message. Exit code 0 always.
"""
import json
import re
import sys
from pathlib import Path

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_BODY_LINES = 500
RESERVED_WORDS = ("claude", "anthropic")


def parse_frontmatter(text):
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None, text
    fields, key = {}, None
    for line in match.group(1).splitlines():
        top_level = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if top_level:
            key = top_level.group(1)
            fields[key] = top_level.group(2).strip()
        elif key and line.strip():
            fields[key] = (fields[key] + " " + line.strip()).strip()
    for key, value in fields.items():
        fields[key] = re.sub(r"^[>|]-?\s*", "", value)
    return fields, text[match.end():]


def check_skill(skill_dir, report):
    name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        report("ERROR", name, "SKILL.md is missing")
        return
    fields, body = parse_frontmatter(skill_file.read_text())
    if fields is None:
        report("ERROR", name, "no front matter")
        return
    if fields.get("name") != name:
        report("ERROR", name, f"name '{fields.get('name')}' differs from the folder name")
    if not NAME_PATTERN.match(name) or len(name) > MAX_NAME_LENGTH:
        report("ERROR", name, "name must be kebab-case, 64 characters at most")
    if any(word in name for word in RESERVED_WORDS):
        report("ERROR", name, "name contains a reserved word")
    description = fields.get("description", "")
    if not description:
        report("ERROR", name, "description is empty")
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        report("WARN", name, f"description has {len(description)} characters (check the current limit in the docs)")
    if len(body.splitlines()) > MAX_BODY_LINES:
        report("WARN", name, f"body has more than {MAX_BODY_LINES} lines: move detail to references/")
    if "slash-only" in description.lower() and fields.get("disable-model-invocation") != "true":
        report("WARN", name, "description says slash-only but disable-model-invocation is not true")
    report("INFO", name, "front matter keys: " + ", ".join(fields))

    for path in skill_dir.rglob("*"):
        if not path.is_file() or path.suffix in (".json", ".html"):
            continue
        text = path.read_text(errors="ignore")
        relative = path.relative_to(skill_dir)
        for old_name in sorted(set(re.findall(r"tnx-[a-z]+(?:-[a-z]+)+", text))):
            report("WARN", name, f"{relative}: depends on project skill '{old_name}'")
        if re.search(r"\.claude/skills/", text):
            report("WARN", name, f"{relative}: path '.claude/skills/' exists only in the project; use ${{CLAUDE_PLUGIN_ROOT}}")
        if re.search(r"\.\./[a-z-]+/", text):
            report("WARN", name, f"{relative}: relative path to another skill folder")
    for reference in sorted(set(re.findall(r"`((?:references|scripts|templates|assets)/[^`\s]+)`", body))):
        if "<" not in reference and not (skill_dir / reference).exists():
            report("WARN", name, f"SKILL.md mentions missing file '{reference}'")


def check_plugin_files(repo, skill_names, report):
    plugin_file = repo / ".claude-plugin" / "plugin.json"
    marketplace_file = repo / ".claude-plugin" / "marketplace.json"
    plugin = {}
    for file in (plugin_file, marketplace_file):
        try:
            data = json.loads(file.read_text())
            if file == plugin_file:
                plugin = data
        except Exception as error:
            report("ERROR", file.name, f"cannot read: {error}")
    for field in ("name", "version", "description"):
        if plugin and field not in plugin:
            report("WARN", "plugin.json", f"field '{field}' is missing")
    readme = (repo / "README.md").read_text() if (repo / "README.md").exists() else ""
    for name in skill_names:
        if f"`{name}`" not in readme:
            report("WARN", "README.md", f"skill '{name}' is not in the glossary")
    for listed in re.findall(r"^\| `([a-z0-9-]+)` \|", readme, re.M):
        if listed not in skill_names:
            report("WARN", "README.md", f"glossary lists '{listed}' but the skill does not exist")


def main():
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").expanduser()
    findings = []

    def report(level, subject, message):
        findings.append((level, subject, message))

    skills_dir = repo / "skills"
    skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir()) if skills_dir.exists() else []
    for skill_dir in skill_dirs:
        check_skill(skill_dir, report)
    check_plugin_files(repo, [path.name for path in skill_dirs], report)
    for level, subject, message in findings:
        print(f"{level}\t{subject}\t{message}")
    print(f"SUMMARY\t{len(skill_dirs)} skills\t{sum(f[0] == 'ERROR' for f in findings)} errors, {sum(f[0] == 'WARN' for f in findings)} warnings")


main()
