---
allowed-tools: Read, Glob, Grep
argument-hint: <question about your knowledge base>
description: Ask a question answered from your compiled knowledge base
---

## Your task

Answer the question in $ARGUMENTS using ONLY the knowledge base wiki content.

### Step 0: Read configuration and verify structure

Use the **Read** tool to read `~/.claude/knowledge-base/config`.

- If Read fails (file not found): stop and tell the user:
  > Knowledge base is not configured. Run `/knowledge-base:setup` first.
- If Read succeeds: extract `kb_root` (file content trimmed). Then attempt to Read `<kb_root>/wiki/index.md` to verify the structure exists.
  - If that Read fails: stop and tell the user:
    > Knowledge base directory structure is missing. Run `/knowledge-base:setup` to initialize.
  - If both Reads succeed: proceed to Step 1 with the resolved `kb_root`. The index content from this Read can be reused in Step 1.

**Important:** Do NOT use `cat` or `test` shell commands for these checks. The Read tool handles paths outside the working directory via Claude Code's tool permission flow.

### Step 1: Read the index

Read `<KB_ROOT>/wiki/index.md` to understand the full knowledge structure.

**Size guard:** If the index exceeds 1000 lines, warn:
> **Note:** Index is very large. Answers may be incomplete. Consider running `/knowledge-base:health-check`.

If `index.md` does not exist or the wiki is empty, tell the user:
> Knowledge base is empty. Use `/knowledge-base:ingest <URL or file>` to add sources first.

### Step 2: Identify relevant documents

Based on the question ($ARGUMENTS), identify which documents are most relevant:
- Scan the index for concepts, summaries, and connections related to the question
- Prioritize concept files for definitional questions
- Prioritize summary files for source-specific questions
- Prioritize connection files for relationship questions

### Step 3: Read relevant documents

Read the identified relevant files from `wiki/concepts/`, `wiki/summaries/`, and `wiki/connections/`. Read only what is needed to answer the question — do NOT read the entire wiki.

### Step 4: Synthesize answer

Compose an answer that:
- Is **grounded in the wiki content** — do NOT use your training knowledge to fill gaps
- **Cites sources** with relative file paths, e.g.: *(Source: [concept-name](wiki/concepts/concept-name.md))*
- Acknowledges when information is incomplete or uncertain
- Is well-structured with headings if the answer is complex

### Step 5: Handle unanswerable questions

If the question cannot be answered from the wiki:
- State clearly: "This question cannot be answered from the current knowledge base."
- Suggest what to ingest: "Consider ingesting sources about <topic> using `/knowledge-base:ingest`."
- List the closest related content that IS in the wiki, if any.

### Response format

```markdown
## Answer

<Your grounded answer here>

### Sources
- [source-name](wiki/summaries/source-name.md)
- [concept-name](wiki/concepts/concept-name.md)
```
