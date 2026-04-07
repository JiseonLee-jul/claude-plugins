---
allowed-tools: Bash(mkdir:*), Bash(test:*), Bash(ls:*), Read, Write, AskUserQuestion
argument-hint: [optional kb_root path]
description: Initialize the knowledge base (config + directory structure)
---

## Context

- Existing config: !`cat ~/.claude/knowledge-base/config 2>/dev/null || echo "NONE"`

## Your task

Initialize the knowledge base by creating the config file and the complete directory structure.

### Step 1: Determine the KB root path

- If `$ARGUMENTS` is non-empty: use it as `kb_root`
- If existing config shows a valid path: confirm with the user whether to reuse it or replace it (use `AskUserQuestion`)
- Otherwise: ask the user where to create the knowledge base (use `AskUserQuestion` with examples like `/home/user/kb`, `./my-kb`, or `~/Documents/kb`)

Expand `~` to the actual home directory before use. Normalize the path (remove trailing slash).

### Step 2: Create the Claude Code config directory

```bash
mkdir -p ~/.claude/knowledge-base
```

### Step 3: Write the config file

Write the resolved `kb_root` path (one line, no trailing newline) to `~/.claude/knowledge-base/config`.

### Step 4: Create the knowledge base directory structure

```bash
mkdir -p <KB_ROOT>/raw/images
mkdir -p <KB_ROOT>/wiki/summaries
mkdir -p <KB_ROOT>/wiki/concepts
mkdir -p <KB_ROOT>/wiki/connections
```

Replace `<KB_ROOT>` with the actual path.

### Step 5: Create an empty index.md

If `<KB_ROOT>/wiki/index.md` does not already exist, create it with a minimal stub:

```markdown
# Knowledge Base Index

*Empty knowledge base. Use `/knowledge-base:ingest <source>` to add content.*
```

### Step 6: Verify

Run `ls` on `<KB_ROOT>` to confirm the structure, then report:

```markdown
## Setup Complete

- **KB root:** <path>
- **Config:** ~/.claude/knowledge-base/config
- **Structure created:**
  - raw/ (with images/ subdirectory)
  - wiki/index.md (empty stub)
  - wiki/summaries/
  - wiki/concepts/
  - wiki/connections/

### Next steps
- Ingest a source: `/knowledge-base:ingest <URL or file path>`
- Ask the knowledge base: `/knowledge-base:ask <question>`
- Check integrity: `/knowledge-base:health-check`
```

### Edge cases

- If the KB root path points to an existing non-empty directory that is NOT already a knowledge base (no `wiki/` subdirectory): warn the user before creating files inside it, and ask for confirmation.
- If the KB root is already a knowledge base (has `wiki/index.md`): skip structure creation, just update the config file, and report "already initialized, config updated."
- Never delete existing files. Setup is additive only.
