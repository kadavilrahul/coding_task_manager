# Context7 MCP Server

Context7 is an MCP server that provides real-time, version-specific documentation to AI coding assistants.

## What is Context7?

Context7 fetches current documentation directly from source libraries and injects it into your AI's context, eliminating outdated or hallucinated code examples.

## Features

- ✅ Real-time, version-specific documentation
- ✅ Direct injection into AI context
- ✅ Works with multiple AI coding tools
- ✅ Eliminates outdated API references
- ✅ No installation of additional packages needed

## Files in this folder

- `README.md` - This documentation
- `context7-install.md` - Complete installation guide with troubleshooting
- `mcp-commands.sh` - All successful MCP management commands

## Quick Installation

### Prerequisites
- Node.js >= v18.0.0
- Claude Code CLI installed

### Installation Command
```bash
claude mcp add context7 npx @upstash/context7-mcp
```

### Verification
```bash
claude mcp list
```

## Usage

Once installed, use Context7 by adding "use context7" to your prompts:

```
use context7 - show me how to create a React component with hooks
```

Context7 will automatically fetch and inject current React documentation.

## Troubleshooting

If Context7 shows as "failed":

1. Remove and re-add:
```bash
claude mcp remove context7
claude mcp add context7 npx @upstash/context7-mcp
```

2. Check logs:
```bash
claude --debug mcp list
```

See `context7-install.md` for detailed troubleshooting steps.

## Repository

https://github.com/upstash/context7