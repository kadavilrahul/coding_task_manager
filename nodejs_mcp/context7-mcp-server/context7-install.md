# Context7 MCP Server Installation

## Successful Installation Commands

### Prerequisites Check
```bash
# Check Node.js version (requires >= v18.0.0)
node --version
# Output: v20.19.3 ✅
```

### Installation Steps

1. **Add Context7 to Claude Code**
```bash
# Add Context7 MCP server
claude mcp add context7 npx @upstash/context7-mcp
```

2. **Verify Installation**
```bash
# List all MCP servers
claude mcp list
```

### Troubleshooting Commands

If Context7 shows as "failed":

1. **Remove failing server**
```bash
claude mcp remove context7
```

2. **Re-add with correct command format**
```bash
claude mcp add context7 npx @upstash/context7-mcp
```

3. **Check debug logs**
```bash
claude --debug mcp list
```

4. **View specific error logs**
```bash
ls -la /root/.cache/claude-cli-nodejs/-root/mcp-logs-context7/
```

## Key Issues Fixed

1. **Command Format Error**: 
   - ❌ Wrong: `npx -y @upstash/context7-mcp` (causes spawn ENOENT error)
   - ✅ Correct: `npx @upstash/context7-mcp`

2. **Error Pattern**: `spawn npx -y @upstash/context7-mcp ENOENT`
   - **Solution**: Remove the `-y` flag from the command

## Final Working Configuration

```bash
# Current MCP servers
screenshot-server: /root/screenshot-mcp-server.js 
context7: npx @upstash/context7-mcp
```

## Usage

Once connected, use Context7 by adding "use context7" to your prompts in Claude Code:

```
use context7 - show me how to create a React component with hooks
```

Context7 will inject up-to-date documentation for the libraries you're working with.