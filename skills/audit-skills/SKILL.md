---
name: audit-skills
description: Slash-only. Use only when the user explicitly invokes /audit-skills. Audits the skills of the personal plugin repo against the current Claude Code conventions and recent changes, then proposes and applies fixes after the user agrees. Never trigger from natural-language requests.
disable-model-invocation: true
argument-hint: "[repo path, default ~/code/skills]"
allowed-tools: Bash(python3 *), Bash(git *), Bash(claude --version), Read, Edit, Write, Glob, Grep, WebFetch, WebSearch, Agent, AskUserQuestion
---

# Audit Skills

Keeps the skills of the personal plugin repo up to date with the Claude Code docs.

`REPO` is `$ARGUMENTS`, or `~/code/skills`. Work only in `REPO`. Never edit the skills of a project repo.

## Steps

1. **Run the mechanical checks.**
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/audit-skills/scripts/check_skills.py REPO`
   Lines are `LEVEL<TAB>skill<TAB>message`. `INFO` lines list the front matter keys in use.
   Some warnings are false positives (a file that belongs to another skill, for example). Read the
   skill before you keep a finding.

2. **Read the current rules.** Do not rely on memory: the conventions change.
   - Read the live docs: `https://code.claude.com/docs/en/skills` and `https://code.claude.com/docs/en/plugins`
     (and the plugin marketplace page). Use the `claude-code-guide` agent, or `WebFetch`.
   - Read `REPO/.last-audit.json` if it exists (`date`, `claudeVersion`). Look at the Claude Code release
     notes or changelog since that date. Without the file, look at the last three months.
   - Get the installed version with `claude --version`.

3. **Compare the skills with the docs.** Look for:
   - front matter keys in use that are renamed, deprecated or unknown;
   - new keys or features worth adopting (name each one and say why);
   - description rules (length, wording, when to use);
   - body rules (size, `references/` split, script paths, `${CLAUDE_PLUGIN_ROOT}`);
   - plugin and marketplace file format (`plugin.json`, `marketplace.json`, `version`);
   - dependencies on files or skills that exist only in a project repo.
   Every finding that does not come from the script cites the doc page. If you cannot confirm it in the
   docs, label it "to verify". Do not invent a rule.

4. **Report in the chat, in French.** One table: severity, skill, finding, proposed fix. Group the
   findings from the script and the findings from the docs. End with the fixes you recommend.
   Write no report file.

5. **Ask which fixes to apply** (`AskUserQuestion`). Never delete a skill without an explicit yes.

6. **Apply the chosen fixes.**
   - Edit the skill files. Keep names in `kebab-case`, verb first, no `tnx-` prefix.
   - Keep the README glossary in sync: one line per skill, same groups.
   - Run the script again. No new `ERROR`.
   - Bump the patch number of `version` in `.claude-plugin/plugin.json`.
   - Write `REPO/.last-audit.json` with today's date and the `claude --version` value.

7. **Commit, do not push.** One commit per logical change, message in simple English. Tell the user to
   push and to run `/plugin marketplace update <marketplace-name>`.
