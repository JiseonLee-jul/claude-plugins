---
allowed-tools: Bash(gh issue:*), Bash(git checkout:*), Bash(git branch:*)
argument-hint: <issue-number>
description: Create a branch linked to a GitHub issue
---

## Context

- Issue details: !`gh issue view $ARGUMENTS`
- Current branch: !`git branch --show-current`
- Remote: !`git remote -v`

## Your task

1. Fetch the issue information using the provided issue number
2. Create a branch name following @branch-name conventions
3. Create the branch using `gh issue develop $ARGUMENTS --name <branch-name>` to link it to the issue
   - If gh issue develop is not available, create branch manually and push with `-u`
   