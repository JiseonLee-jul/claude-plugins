# commands/setup.md
---
description: Setup guide for git plugin
---

## GitHub MCP Setup

This plugin uses GitHub MCP server.

### Option 1: OAuth (Recommended)
1. Run `/mcp` command
2. Select "Authenticate" for GitHub
3. Login via browser

### Option 2: Personal Access Token
If OAuth doesn't work:
1. Create PAT at https://github.com/settings/tokens
2. Set environment variable:
```bash
   export GITHUB_PAT="ghp_your_token"
```
3. Restart Claude Code