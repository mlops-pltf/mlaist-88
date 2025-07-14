# Module 1: Basic MCP Server - Starter Code

Welcome to Module 1! In this module, you'll build a basic MCP server that helps developers create better pull requests by analyzing code changes and suggesting appropriate templates.

## Your Task

Implement an MCP server with three tools:

1. **analyze_file_changes** - Retrieve git diff information and changed files
2. **get_pr_templates** - List available PR templates 
3. **suggest_template** - Allow Claude to suggest the most appropriate template

## Setup

### 1. Install uv

Follow the official installation instructions at: https://docs.astral.sh/uv/getting-started/installation/

### 2. Install dependencies

```bash
# Install all dependencies
uv sync

# Or install with dev dependencies for testing
uv sync --all-extras
```

### 3. Start implementing!

Open `server.py` and follow the TODO comments to implement each tool.

**Note**: The starter code includes stub implementations that return "Not implemented" errors. This allows you to:
- Run the server immediately
- Test your setup with Claude
- Replace each stub with your actual implementation
- See helpful hints about what each tool should do

## Design Philosophy

Instead of using rigid rules based on file extensions or patterns, your tools should provide Claude with raw git data and let Claude's intelligence determine:
- What type of change is being made
- Which template is most appropriate
- How to customize the template for the specific changes

## Testing Your Implementation

1. Run the unit tests:
   ```bash
   uv run pytest test_server.py -v
   ```

2. Configure the MCP server in Claude Code:
   ```bash
   # Add the MCP server
   claude mcp add pr-agent -- uv --directory /absolute/path/to/module1/starter run server.py
   
   # Verify it's configured
   claude mcp list
   ```

3. Make some changes in a git repository and ask Claude to analyze your changes and suggest a PR template

## Need Help?

- Check the solution in `../solution/` if you get stuck
- Remember: The goal is to give Claude the data it needs, not to implement complex logic yourself



# Module 2: GitHub Actions Integration

This module extends the PR Agent with GitHub Actions webhook integration and MCP Prompts for standardized CI/CD workflows.

## Features Added in Module 2

1. **GitHub Actions Tools**:
   - `get_recent_actions_events()` - View recent webhook events
   - `get_workflow_status()` - Check workflow statuses

2. **MCP Prompts for CI/CD**:
   - `analyze_ci_results` - Comprehensive CI/CD analysis
   - `create_deployment_summary` - Team-friendly deployment updates
   - `generate_pr_status_report` - Combined code and CI/CD report
   - `troubleshoot_workflow_failure` - Systematic debugging guide

3. **Webhook Server**:
   - Separate script that runs on port 8080
   - Receives GitHub Actions events
   - Stores events in `github_events.json` for the MCP server to read

## Installation

```bash
# From the solution directory
uv sync
```

## Setting Up Cloudflare Tunnel

To receive GitHub webhooks locally, you'll need to set up Cloudflare Tunnel (cloudflared):

### Step 1: Install cloudflared

**macOS:**
```bash
brew install cloudflared
```

**Windows:**
Download the Windows installer from:
https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.msi

**Linux:**
```bash
# For Debian/Ubuntu (amd64)
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb
sudo dpkg -i cloudflared.deb

# For other Linux distros, download the appropriate binary:
# https://github.com/cloudflare/cloudflared/releases/latest
```

### Step 2: Start the Tunnel

```bash
# This creates a public URL that forwards to your local webhook server
cloudflared tunnel --url http://localhost:8080
```

You'll see output like:
```
Your quick tunnel has been created! Visit it at:
https://random-name-here.trycloudflare.com
```

### Step 3: Configure GitHub Webhook

1. Go to your GitHub repository → Settings → Webhooks
2. Click "Add webhook"
3. Set **Payload URL** to: `https://your-tunnel-url.trycloudflare.com/webhook/github`
4. Set **Content type** to: `application/json`
5. Select events:
   - Workflow runs
   - Check runs
   - Or choose "Send me everything"
6. Click "Add webhook"

## Running the Server

### For Development

```bash
# Terminal 1: Start the webhook server
python webhook_server.py

# Terminal 2: Start Cloudflare Tunnel (if testing with real GitHub)
cloudflared tunnel --url http://localhost:8080

# Terminal 3: Start the MCP server
uv run server.py
```

### With Claude Code

1. Add to Claude Code settings:
```json
{
  "pr-agent-actions": {
    "command": "uv",
    "args": ["run", "server.py"],
    "cwd": "/path/to/github-actions-integration/solution"
  }
}
```

2. Restart Claude Code
3. In a separate terminal, start the webhook server: `python webhook_server.py`
4. (Optional) Start Cloudflare Tunnel if testing with real GitHub webhooks

## Testing Webhooks

### Manual Test
```bash
# Send a test webhook
curl -X POST http://localhost:8080/webhook/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: workflow_run" \
  -d '{
    "action": "completed",
    "workflow_run": {
      "id": 123456789,
      "name": "CI Tests",
      "head_branch": "main",
      "run_number": 42,
      "status": "completed",
      "conclusion": "success",
      "html_url": "https://github.com/user/repo/actions/runs/123456789",
      "updated_at": "2024-01-01T10:00:00Z"
    },
    "repository": {
      "full_name": "user/repo"
    },
    "sender": {
      "login": "test-user"
    }
  }'
```

### With Claude Code

After setting up webhooks and pushing a commit:

1. **Check recent events**: 
   - Ask: "What GitHub Actions events have we received?"
   - Claude will use `get_recent_actions_events()`

2. **Analyze CI status**:
   - Use the prompt: "Analyze CI Results"
   - Claude will check workflows and provide insights

3. **Create deployment summary**:
   - Use the prompt: "Create Deployment Summary"
   - Claude will format a team-friendly update

## Module Structure

- `server.py` - Main MCP server with Tools and Prompts
- `webhook_server.py` - Separate webhook server that stores events
- `github_events.json` - File where webhook events are stored (created automatically)
- `pyproject.toml` - Dependencies for both servers
- `README.md` - This file

## Next Steps

- Complete the exercises in the module
- Experiment with different prompt workflows
- Move on to Module 3 for Hugging Face Hub integration