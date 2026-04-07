---
allowed-tools: Bash(python:*), Bash(cp:*), Bash(test:*), Read, Write, Glob, WebFetch
argument-hint: <URL or local file/directory path>
description: Ingest a source into the knowledge base (URL or local file), then auto-compile
---

## Context

- KB root: !`cat ~/.claude/knowledge-base/config 2>/dev/null || echo "NOT_CONFIGURED"`
- KB structure: !`KB=$(cat ~/.claude/knowledge-base/config 2>/dev/null); test -d "$KB/wiki" && echo "OK" || echo "MISSING"`

## Your task

Ingest the source specified in $ARGUMENTS into the knowledge base, then auto-compile it.

**IMPORTANT preconditions:**

- If KB root shows "NOT_CONFIGURED", stop and tell the user:
  > Knowledge base is not configured. Run `/knowledge-base:setup` first.
- If KB structure shows "MISSING", stop and tell the user:
  > Knowledge base directory structure is missing. Run `/knowledge-base:setup` to initialize.

### Step 1: Determine source type

Check if `$ARGUMENTS` starts with `http://` or `https://`:
- **YES** → URL ingest (Step 2a)
- **NO** → Local file ingest (Step 2b)

### Step 2a: URL Ingest

1. Generate a `source_name` from the URL (domain + path slug, e.g., `example_com_article-title`)
2. **Fetch the page content using WebFetch:**
   - Use the WebFetch tool with the URL from `$ARGUMENTS`
   - WebFetch returns the page content as readable text/markdown
3. **Download images using the Python script:**
   ```bash
   echo '{"url": "$ARGUMENTS", "kb_root": "<KB_ROOT>", "source_name": "<SOURCE_NAME>"}' | python "${CLAUDE_PLUGIN_ROOT}/scripts/kb_ingest_url.py"
   ```
   - The script downloads images to `raw/images/<source_name>/` and returns the list of downloaded filenames
4. **Refine the WebFetch content into clean markdown:**
   - Clean up any remaining noise (navigation remnants, ads, footers)
   - Structure with proper headings, lists, links
   - If images were downloaded, add image references using local paths: `![alt](images/<source_name>/filename.png)`
   - Preserve all meaningful content — do not summarize at this stage
5. Write the refined markdown to `<KB_ROOT>/raw/<source_name>.md`

### Step 2b: Local File Ingest

1. Check if `$ARGUMENTS` is a file or directory
2. Copy to `<KB_ROOT>/raw/` (the directory already exists from setup):
   - File: `cp "$ARGUMENTS" <KB_ROOT>/raw/`
   - Directory: `cp -r "$ARGUMENTS"/* <KB_ROOT>/raw/`
3. Report what was copied

### Step 3: Auto-compile the ingested source

After ingest completes, run incremental compile for the new file(s):

1. Run compile status script:
   ```bash
   echo '{"kb_root": "<KB_ROOT>"}' | python "${CLAUDE_PLUGIN_ROOT}/scripts/kb_compile_status.py"
   ```
2. For each file in the `batch` array from the output:
   a. Read the raw source file
   b. **Generate summary** → Write to `<KB_ROOT>/wiki/summaries/<stem>.md`:
      - Include YAML-style metadata at top: source path, date compiled, key topics
      - Write a comprehensive summary (3-5 paragraphs)
      - Add a "Related Concepts" section with links to `../concepts/<name>.md`
   c. **Extract concepts** → For each key concept identified:
      - Use lowercase-hyphenated filenames (e.g., `machine-learning.md`)
      - If `<KB_ROOT>/wiki/concepts/<concept>.md` exists: Read it, merge new information (rewrite with combined knowledge, not append)
      - If new: Create `<KB_ROOT>/wiki/concepts/<concept>.md` with structured content (definition, key points, related concepts with backlinks)
   d. **Discover connections** → For pairs of related concepts:
      - Use alphabetical ordering: `<concept-a>--<concept-b>.md` (e.g., `embeddings--transformers.md`)
      - Write to `<KB_ROOT>/wiki/connections/<a>--<b>.md` with bidirectional description

3. **Rebuild index.md** — Read all wiki directories and write `<KB_ROOT>/wiki/index.md`:
   ```markdown
   # Knowledge Base Index
   
   *Last updated: <date>*
   *Sources: N | Concepts: N | Connections: N*
   
   ## Sources
   - [source_name](summaries/source_name.md) — brief description
   
   ## Concepts
   - [concept-name](concepts/concept-name.md) — brief description
   
   ## Connections
   - [concept-a ↔ concept-b](connections/concept-a--concept-b.md)
   
   ## Recent Additions
   - <date>: Added <source_name>
   ```

4. **Update compile state** — Read existing `.kb_state.json`, add the hash for each compiled file, write back.

5. **Verify integrity:**
   ```bash
   echo '{"kb_root": "<KB_ROOT>"}' | python "${CLAUDE_PLUGIN_ROOT}/scripts/kb_verify_integrity.py"
   ```
   Report any issues found.

### Step 4: Report

Summarize what was done:
- Source ingested: name, type (URL/local), size
- Wiki updates: summaries created, concepts created/updated, connections discovered
- Integrity check: pass/fail
- Any errors or warnings

All wiki directories (`summaries/`, `concepts/`, `connections/`) are guaranteed to exist because `/knowledge-base:setup` created them. Do NOT create directories from this command — if any are missing, that indicates a broken setup and should be reported as an error.
