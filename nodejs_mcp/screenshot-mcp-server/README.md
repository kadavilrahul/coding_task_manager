# Node.js MCP Screenshot Server

A Model Context Protocol (MCP) server for taking webpage screenshots using headless Chrome.

## Files

- `screenshot-mcp-server.js` - Main MCP server implementation
- `package.json` - Node.js project configuration
- `README.md` - This documentation

## Prerequisites

- Node.js (v14.0.0 or higher)
- Chromium browser (`chromium-browser` command available)
- Claude Code CLI installed

## Installation Steps

### 1. Check Prerequisites
```bash
# Check Node.js version
node --version

# Check if Chromium is available
which chromium-browser

# Check Claude Code
claude --version
```

### 2. Setup Files
```bash
# Create project directory
mkdir screenshot-mcp-server
cd screenshot-mcp-server

# Copy the files (screenshot-mcp-server.js and package.json)
# Make server executable
chmod +x screenshot-mcp-server.js
```

### 3. Add to Claude Code
```bash
# Add MCP server to Claude Code (use absolute path)
claude mcp add screenshot-server /path/to/screenshot-mcp-server.js

# Verify installation
claude mcp list
```

### 4. Test Connection
```bash
# Check MCP server status in Claude Code
# Should show as connected, not "connecting..." or "failed"
```

## Usage

Once connected to Claude Code, you can use the screenshot tool:

```
Take a screenshot of https://example.com
```

**Important**: When running as root, you may encounter this error:
```
Running as root without --no-sandbox is not supported
```

To fix this, add the `--no-sandbox` flag to the chromium command in `screenshot-mcp-server.js`:
```javascript
const command = `chromium-browser --headless --disable-gpu --disable-software-rasterizer --no-sandbox --screenshot="${outputPath}" --window-size=${width},${height} --virtual-time-budget=10000 "${url}"`;
```

### Available Parameters

- `url` (required) - The webpage URL to screenshot
- `width` (optional) - Viewport width in pixels (default: 1920)
- `height` (optional) - Viewport height in pixels (default: 1080)
- `output_path` (optional) - Custom save path (default: auto-generated)

### Example Usage

```
Take a screenshot of https://google.com with width 1280 and height 720
```

## Technical Details

### MCP Protocol Implementation

The server implements the MCP protocol with:
- JSON-RPC 2.0 format
- Proper `initialize` and `initialized` handlers
- Tool discovery via `tools/list`
- Tool execution via `tools/call`

### Screenshot Implementation

- Uses headless Chromium browser
- Configurable viewport size
- Auto-generates timestamped filenames
- Validates URLs and adds https:// if missing
- 30-second timeout for page loading

## Troubleshooting

### Connection Issues

1. **"connecting..." forever**
   - Check if Chromium is installed: `which chromium-browser`
   - Verify file permissions: `chmod +x screenshot-mcp-server.js`
   - Check logs: `claude --debug mcp list`

2. **"failed" status**
   - Review logs in `~/.cache/claude-cli-nodejs/*/mcp-logs-screenshot-server/`
   - Test manually: `echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}' | node screenshot-mcp-server.js`

3. **Screenshot failures**
   - Check Chromium installation
   - Verify URL accessibility
   - Check file permissions in output directory

### Common Fixes

```bash
# Install Chromium if missing
sudo apt-get install chromium-browser

# Fix permissions
chmod +x screenshot-mcp-server.js

# Remove and re-add server
claude mcp remove screenshot-server
claude mcp add screenshot-server /full/path/to/screenshot-mcp-server.js
```

## Development Notes

### Key Implementation Details

1. **JSON-RPC Compliance**: Must include `jsonrpc: "2.0"` in responses
2. **Notification Handling**: Don't respond to requests without `id`
3. **Initialize Sequence**: Must handle both `initialize` and `initialized` methods
4. **Error Handling**: Proper error codes and messages

### Successful Implementation Steps

1. Created basic MCP server structure
2. Added screenshot functionality using headless Chrome
3. Fixed JSON-RPC response format issues
4. Added proper initialization handlers
5. Implemented notification handling for MCP protocol compliance

## License

MIT License