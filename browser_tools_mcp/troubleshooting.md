# Browser Tools MCP Troubleshooting

## Issue: MCP Server Status Shows "Failed"

### Problem Description
The Browser Tools MCP server shows as "failed" in Claude's MCP status interface. The server expects to connect to a Chrome browser extension and server running on ports 3025-3035, but no such server is found.

### Root Cause
The Browser Tools MCP is designed to work with a Chrome browser extension that needs to be separately installed and running. Without this extension, the MCP server cannot function properly.

### Error Output
```
Starting server discovery process
Will try hosts: 127.0.0.1, 127.0.0.1, localhost
Will try ports: 3025, 3026, 3027, 3028, 3029, 3030, 3031, 3032, 3033, 3034, 3035
...
No server found during discovery
Initial server discovery failed. Will try again when tools are used.
```

## Solutions Attempted

### 1. Updated to Latest Version
```bash
# Remove old version
claude mcp remove browser-tools

# Install latest version globally
npm install -g @agentdeskai/browser-tools-mcp@1.2.1

# Add with global command
claude mcp add browser-tools "browser-tools-mcp"
```

### 2. Package Information
- Package: `@agentdeskai/browser-tools-mcp@1.2.1`
- Dependencies: @modelcontextprotocol/sdk, express, cors, ws, etc.
- Binary: `browser-tools-mcp`

## Required Setup for Full Functionality

### Chrome Extension Required
1. Download Chrome extension from GitHub repository
2. Load unpacked extension in Chrome (Developer mode)
3. Extension creates local server on ports 3025-3035
4. MCP server connects to this local server

### Alternative: Use Without Extension
The MCP server will start but functionality will be limited without the browser extension. It may still provide some basic browser automation capabilities through Puppeteer.

## Current Status
- ✅ MCP server installed globally
- ✅ Added to Claude MCP configuration
- ⚠️ Limited functionality without Chrome extension
- ❌ Chrome extension not installed (requires manual setup)

## Recommendations
1. For full functionality, install the Chrome extension
2. For basic testing, the current setup may work with limited features
3. Consider alternative browser automation MCPs if extension setup is not feasible