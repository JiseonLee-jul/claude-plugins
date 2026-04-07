---
allowed-tools: Bash(python:*), Bash(test:*), Read, Write, Glob, Grep
argument-hint:
description: Compile new raw sources into wiki (incremental, max 10 files per run)
---

## Context

- KB root: !`cat ~/.claude/knowledge-base/config 2>/dev/null || echo "NOT_CONFIGURED"`
- KB structure: !`KB=$(cat ~/.claude/knowledge-base/config 2>/dev/null); test -d "$KB/wiki" && echo "OK" || echo "MISSING"`

## Your task

Incrementally compile new/modified raw sources into the wiki.

**IMPORTANT preconditions:**

- If KB root shows "NOT_CONFIGURED", stop and tell the user:
  > Knowledge base is not configured. Run `/knowledge-base:setup` first.
- If KB structure shows "MISSING", stop and tell the user:
  > Knowledge base directory structure is missing. Run `/knowledge-base:setup` to initialize.

### Step 1: Check compile status

```bash
echo '{"kb_root": "<KB_ROOT>"}' | python "${CLAUDE_PLUGIN_ROOT}/scripts/kb_compile_status.py"
```

If `total_pending` is 0, report "Wiki is up to date. No new files to compile." and stop.

### Step 2: Process each file in `batch` (max 10)

For each file in the `batch` array:

1. **Read the raw source file.** The LLM can read .md, .txt, .html, images (PNG, JPG), and PDFs natively.

2. **Generate summary** → Write to `<KB_ROOT>/wiki/summaries/<stem>.md`:
   ```markdown
   ---
   source: raw/<filename>
   compiled: <YYYY-MM-DD>
   topics: [topic1, topic2, ...]
   ---
   
   # Summary: <Title>
   
   <Comprehensive 3-5 paragraph summary>
   
   ## Key Points
   - Point 1
   - Point 2
   
   ## Related Concepts
   - [concept-name](../concepts/concept-name.md)
   ```

3. **Extract and write concepts** → For each key concept:
   - Filename: lowercase-hyphenated (e.g., `neural-networks.md`)
   - If concept file exists: Read existing content, **merge** new information (rewrite the document with combined knowledge from all sources — do NOT append)
   - If new concept: Create `<KB_ROOT>/wiki/concepts/<concept>.md`:
   ```markdown
   # <Concept Name>
   
   <Clear definition and explanation>
   
   ## Key Points
   - ...
   
   ## Sources
   - [source-name](../summaries/source-name.md)
   
   ## Related Concepts
   - [other-concept](other-concept.md)
   ```

4. **Discover connections** → For related concept pairs:
   - Filename: alphabetical order, `<a>--<b>.md` (e.g., `attention--transformers.md`)
   - Check if connection file already exists before creating
   - Write to `<KB_ROOT>/wiki/connections/<a>--<b>.md`:
   ```markdown
   # <Concept A> ↔ <Concept B>
   
   <Description of the relationship>
   
   ## From <Concept A> perspective
   - How A relates to B
   
   ## From <Concept B> perspective
   - How B relates to A
   
   ## Sources
   - [source](../summaries/source.md)
   ```

### Step 3: Rebuild index.md

Scan all wiki directories and write `<KB_ROOT>/wiki/index.md` from scratch:

```markdown
# Knowledge Base Index

*Last updated: <YYYY-MM-DD>*
*Sources: N | Concepts: N | Connections: N*

## Sources
- [source-name](summaries/source-name.md) — brief one-line description

## Concepts
- [concept-name](concepts/concept-name.md) — brief one-line description

## Connections
- [concept-a ↔ concept-b](connections/concept-a--concept-b.md)

## Recent Additions
- <date>: Compiled <source-name>
```

**Size guard:** If index.md exceeds 500 lines, add a warning at the top:
> **Warning:** Index is getting large (N lines). Consider organizing sub-indices for better performance.

### Step 4: Update compile state

Read `<KB_ROOT>/.kb_state.json`, add/update the hash for each successfully compiled file from the batch, write back.

**Important:** Only update the hash for files that were **successfully** compiled (summary + concepts written).

### Step 5: Verify integrity

```bash
echo '{"kb_root": "<KB_ROOT>"}' | python "${CLAUDE_PLUGIN_ROOT}/scripts/kb_verify_integrity.py"
```

Report any issues.

### Step 6: Report

- Files compiled: N of M pending
- Summaries created/updated: list
- Concepts created/updated: list
- Connections created: list
- Integrity: pass/fail
- If `remaining > 0`: "**N files remaining.** Run `/knowledge-base:compile` again to process the next batch."

All wiki directories (`summaries/`, `concepts/`, `connections/`) are guaranteed to exist because `/knowledge-base:setup` created them. Do NOT create directories from this command — if any are missing, that indicates a broken setup and should be reported as an error.
