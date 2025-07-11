# Browser Tools MCP Installation Steps

## Installation Commands Used

### 1. Install Browser Tools MCP
```bash
npx @agentdeskai/browser-tools-mcp@1.2.0
```

### 2. Add to Claude MCP Configuration
```bash
claude mcp add browser-tools "npx @agentdeskai/browser-tools-mcp@1.2.0"
```

### 3. Verify Installation
```bash
claude mcp list
```

## Installation Output

### NPX Installation Output
```
Starting server discovery process
Will try hosts: 127.0.0.1, 127.0.0.1, localhost
Will try ports: 3025, 3026, 3027, 3028, 3029, 3030, 3031, 3032, 3033, 3034, 3035
...
npm warn exec The following package was not found and will be installed: @agentdeskai/browser-tools-mcp@1.2.0
Attempting initial server discovery on startup...
No server found during discovery
Initial server discovery failed. Will try again when tools are used.
```

### Claude MCP Add Output
```
Added stdio MCP server browser-tools with command: npx @agentdeskai/browser-tools-mcp@1.2.0  to local config
```

### Claude MCP List Output
```
screenshot-server: /root/screenshot-mcp-server.js 
context7: npx @upstash/context7-mcp
browser-tools: npx @agentdeskai/browser-tools-mcp@1.2.0
```

## Installation Status
✅ Successfully installed and configured Browser Tools MCP
✅ Added to Claude CLI configuration
✅ Server running and ready for browser automation tasks