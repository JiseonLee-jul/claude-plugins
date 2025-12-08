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

If OAuth doesn't work, use a Personal Access Token.

#### Step 1: Create PAT
1. Go to https://github.com/settings/tokens
2. Generate a new token with required permissions
3. Copy the token (starts with `ghp_`)

#### Step 2: Set Environment Variable

**macOS / Linux (bash)**
```bash
# Temporary (current session only)
export GITHUB_PAT="ghp_your_token"

# Permanent
echo 'export GITHUB_PAT="ghp_your_token"' >> ~/.bashrc
source ~/.bashrc
```

**macOS / Linux (zsh)**
```bash
# Temporary (current session only)
export GITHUB_PAT="ghp_your_token"

# Permanent
echo 'export GITHUB_PAT="ghp_your_token"' >> ~/.zshrc
source ~/.zshrc
```

**Windows (PowerShell)**
```powershell
# Temporary (current session only)
$env:GITHUB_PAT = "ghp_your_token"

# Permanent (User level)
[System.Environment]::SetEnvironmentVariable("GITHUB_PAT", "ghp_your_token", "User")
```

**Windows (CMD)**
```cmd
# Temporary (current session only)
set GITHUB_PAT=ghp_your_token

# Permanent (requires Admin)
setx GITHUB_PAT "ghp_your_token"
```

#### Step 3: Restart Claude Code

Close and reopen Claude Code for changes to take effect.

#### Step 4: Verify

Check if the environment variable is set:

**macOS / Linux**
```bash
echo $GITHUB_PAT
```

**Windows (PowerShell)**
```powershell
echo $env:GITHUB_PAT
```

**Windows (CMD)**
```cmd
echo %GITHUB_PAT%
```