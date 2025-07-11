# Browser Tools MCP Setup

This folder contains all the files and steps needed to install and configure the Browser Tools MCP from claudelog.com.

## What is Browser Tools MCP?

Browser Tools MCP is a Model Context Protocol server that enables AI assistants to interact with web browsers for automation, monitoring, and testing tasks.

### Key Features
- Real-time browser monitoring
- Console log and network request tracking
- Lighthouse performance analysis
- WCAG accessibility testing
- Automated browser testing via Puppeteer
- Chrome extension with auto-paste functionality

## Prerequisites

- Node.js 14 or higher
- Chrome browser
- MCP-compatible IDE (Cursor recommended)

## Quick Installation

Run the automated install script:
```bash
./install_script.sh
```

## Manual Installation

### 1. Install Browser Tools MCP Package
You need to run two servers simultaneously:

**Terminal 1 - Start the MCP server:**
```bash
npx @agentdeskai/browser-tools-mcp@1.2.0
```

**Terminal 2 - Start the local server:**
```bash
npx @agentdeskai/browser-tools-server@1.2.0
```

### 2. Add to Claude MCP Configuration
```bash
claude mcp add browser-tools "npx @agentdeskai/browser-tools-mcp@1.2.0"
```

### 3. Configure Claude Desktop (Optional)
Copy the provided configuration:
```bash
mkdir -p ~/.config/claude-desktop
cp claude_desktop_config.json ~/.config/claude-desktop/claude_desktop_config.json
```

### 4. Verify Installation
```bash
claude mcp list
```

You should see `browser-tools` listed among your MCP servers.

## Files in This Directory

- `README.md` - This documentation file
- `installation_steps.md` - Detailed installation log and steps
- `install_script.sh` - Automated installation script
- `claude_desktop_config.json` - Claude Desktop MCP configuration

## Usage

Once installed, the Browser Tools MCP provides various browser automation capabilities through natural language interactions with Claude. The MCP server will automatically discover and connect to running Chrome instances.

## Troubleshooting

If you encounter issues:
1. Ensure Chrome browser is installed and running
2. Check that Node.js version is 14 or higher
3. Verify the MCP server is listed in `claude mcp list`
4. Check that no firewall is blocking the required ports (3025-3035)

## Source

Original installation guide: https://claudelog.com/addons/browser-tools-mcp/

## Troubleshooting

If the MCP server shows as "failed":
1. The Browser Tools MCP requires a Chrome extension to be installed and running
2. Without the extension, the server will fail to find a browser connection
3. See `troubleshooting.md` for detailed solutions

## Current Installation Status

- ✅ MCP server installed globally (v1.2.1)
- ✅ Added to Claude MCP configuration
- ⚠️ Limited functionality without Chrome extension
- ❌ Chrome extension requires manual installation

## Installation Date

Installed on: 2025-07-11
Updated: 2025-07-11 (Fixed configuration issues)