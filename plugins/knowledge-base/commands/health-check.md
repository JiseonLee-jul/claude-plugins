---
allowed-tools: Bash(python:*), Read, Write, Glob, Grep
argument-hint:
description: Check knowledge base consistency, impute missing data, discover connections, auto-fix
---

## Your task

Run a comprehensive health check on the knowledge base and auto-fix all issues found.

### Step 0: Read configuration and verify structure

Use the **Read** tool to read `~/.claude/knowledge-base/config`.

- If Read fails (file not found): stop and tell the user:
  > Knowledge base is not configured. Run `/knowledge-base:setup` first.
- If Read succeeds: extract `kb_root` (file content trimmed). Then attempt to Read `<kb_root>/wiki/index.md` to verify the structure exists.
  - If that Read fails: stop and tell the user:
    > Knowledge base directory structure is missing. Run `/knowledge-base:setup` to initialize.
  - If both Reads succeed: proceed to Phase 1 with the resolved `kb_root`.

**Important:** Do NOT use `cat` or `test` shell commands for these checks. The Read tool handles paths outside the working directory via Claude Code's tool permission flow.

### Phase 1: Structural Integrity (Deterministic)

Run the verification script first:

```bash
echo '{"kb_root": "<KB_ROOT>"}' | python "${CLAUDE_PLUGIN_ROOT}/scripts/kb_verify_integrity.py"
```

This checks:
- Every compiled raw file has a corresponding summary
- Every concept in connections/ exists in concepts/
- index.md lists all summaries and concepts
- No broken internal links

### Phase 2: Content Consistency (LLM)

Read all wiki files and check for:

1. **Contradictions** — Information in one document that contradicts another
   - Read each concept file and cross-reference with its related summaries
   - Flag any factual inconsistencies

2. **Stale references** — Concepts that reference sources or connections that no longer exist
   - Scan for links pointing to non-existent files

3. **Factual consistency** — Summaries that don't accurately represent their source
   - For each summary, spot-check key claims against the raw source (if readable)

### Phase 3: Missing Data Imputation

Identify thin content and supplement it:

1. Scan all concept files for those with **less than 3 sentences** of actual content
2. For each thin concept:
   - Use your knowledge to add relevant information
   - **Mark all imputed content** with `[imputed]` at the end of each added paragraph
   - Example: "Neural networks are computational models inspired by biological neural networks. [imputed]"
3. Note: Web search-based imputation is planned for v2. For now, use LLM training knowledge only.

### Phase 4: Connection Discovery

Find missing connections between existing concepts:

1. Read all concept files
2. Identify pairs of concepts that are clearly related but have no connection file
3. For each discovered connection:
   - Create `<KB_ROOT>/wiki/connections/<a>--<b>.md` (alphabetical order)
   - Write bidirectional relationship description
   - Add backlinks to both concept files

### Phase 5: Auto-Fix

Fix all issues found in Phases 1-4:

1. **Missing summaries** — Regenerate from raw source (read raw file, create summary)
2. **Broken links** — Fix or remove broken references
3. **Orphaned files** — Add missing entries to index.md
4. **Thin concepts** — Already handled in Phase 3 (imputation)
5. **Missing connections** — Already handled in Phase 4 (discovery)
6. **Rebuild index.md** — Regenerate from scratch to ensure completeness

### Phase 6: Post-Fix Verification

Run integrity check again:

```bash
echo '{"kb_root": "<KB_ROOT>"}' | python "${CLAUDE_PLUGIN_ROOT}/scripts/kb_verify_integrity.py"
```

Confirm all structural issues are resolved.

### Phase 7: Report

Generate a clear report:

```markdown
## Health Check Report

**Date:** <YYYY-MM-DD>
**Status:** HEALTHY | ISSUES_REMAINING

### Statistics
- Sources: N | Concepts: N | Connections: N
- Index lines: N

### Structural Issues (Phase 1)
- Found: N | Fixed: N
- <list of issues and fixes>

### Content Issues (Phase 2)
- Contradictions found: N
- Stale references: N
- <details>

### Imputed Content (Phase 3)
- Thin concepts found: N
- Content added to: <list>

### New Connections (Phase 4)
- Discovered: N
- <list of new connections>

### Remaining Issues
- <any unfixed issues, or "None">
```
