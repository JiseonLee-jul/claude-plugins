---
allowed-tools: Bash(gh issue:*), Bash(git checkout:*), Bash(git branch:*)
argument-hint: <issue-number>
description: Create a branch linked to a GitHub issue
---


## Context

- Issue details: !`[ -n "$ARGUMENTS" ] && gh issue view $ARGUMENTS`
- Linked branches: !`[ -n "$ARGUMENTS" ] && gh issue develop --list $ARGUMENTS`
- Current branch: !`git branch --show-current`
- Remote: !`git remote -v`

## Your task

1. Fetch the issue information using the provided issue number
2. Create a branch name following @branch-name conventions
3. Create the branch to link it to the issue
   ```bash
   gh issue develop $ARGUMENTS --name <branch-name>
   ```
