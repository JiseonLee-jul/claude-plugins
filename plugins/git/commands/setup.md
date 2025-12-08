---
description: Setup guide for github MCP
---

## GitHub MCP Setup

This plugin uses GitHub MCP server.

### Step 1: Generate a GitHub Personal Access Token (PAT)
1. Go to [GitHub Token Settings](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:org`, `read:user`
4. Click "Generate token" and copy it

### Step 2: Add GitHub MCP Server
1. Run the following command in the Claude Code CLI
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer YOUR_GITHUB_PAT"
```

2. Restart Claude Code

3. Run claude mcp list to see if the GitHub server is configured