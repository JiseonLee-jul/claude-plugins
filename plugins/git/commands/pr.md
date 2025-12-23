---
allowed-tools: Bash(git push:*), Bash(gh pr create:*), Bash(gh pr edit:*)
description: Create PR
---

## Context

- Current branch: !`git branch --show-current`
- Commits in this branch (not in main): !`git log origin/HEAD..HEAD --oneline`
- Changes summary: !`git diff origin/HEAD..HEAD --stat`
- Detailed changes: !`git diff origin/HEAD..HEAD`
- Existing PR: !`gh pr view`

## Your task

Based on the above commits in this branch, create a pull request following @pr-convention:

1. Push current branch to remote if needed
2. Check if PR already exists for this branch:
    - If exists: Update the PR using `gh pr edit` based on all commits
    - If not exists: Create a new PR using `gh pr create`
3. You have the capability to call multiple tools in a single response. You MUST do all of the above in a single message. Do not use any other tools or do anything else. Do not send any other text or messages besides these tool calls.
