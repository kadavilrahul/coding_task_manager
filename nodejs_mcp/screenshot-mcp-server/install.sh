#!/bin/bash

echo "=== Node.js MCP Screenshot Server Installation ==="
echo

# Check prerequisites
echo "1. Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js v14.0.0 or higher"
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js found: $NODE_VERSION"

# Check Chromium
if ! command -v chromium-browser &> /dev/null; then
    echo "❌ Chromium not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y chromium-browser
    if ! command -v chromium-browser &> /dev/null; then
        echo "❌ Failed to install Chromium"
        exit 1
    fi
fi

echo "✅ Chromium browser found"

# Check Claude Code
if ! command -v claude &> /dev/null; then
    echo "❌ Claude Code CLI not found. Please install Claude Code first"
    exit 1
fi

CLAUDE_VERSION=$(claude --version)
echo "✅ Claude Code found: $CLAUDE_VERSION"

echo

# Setup files
echo "2. Setting up MCP server..."

# Make server executable
chmod +x screenshot-mcp-server.js
echo "✅ Made server executable"

# Get absolute path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
SERVER_PATH="$SCRIPT_DIR/screenshot-mcp-server.js"

echo "📁 Server path: $SERVER_PATH"

echo

# Add to Claude Code
echo "3. Adding MCP server to Claude Code configuration..."

# Path to Claude desktop config
CONFIG_DIR="$HOME/.config/claude-desktop"
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

# Create config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Create or update config file
if [ -f "$CONFIG_FILE" ]; then
    echo "✅ Updating existing Claude desktop config"
    # Backup existing config
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
else
    echo "✅ Creating new Claude desktop config"
    # Create basic config structure
    cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {}
}
EOF
fi

# Add screenshot-mcp-server to config
python3 -c "
import json
import sys

config_file = '$CONFIG_FILE'
server_path = '$SERVER_PATH'

try:
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    if 'mcpServers' not in config:
        config['mcpServers'] = {}
    
    config['mcpServers']['screenshot-mcp-server'] = {
        'command': 'node',
        'args': [server_path]
    }
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print('✅ MCP server added to configuration')
except Exception as e:
    print(f'❌ Failed to update config: {e}')
    sys.exit(1)
"

echo

# Verify installation
echo "4. Verifying installation..."

# Show config file contents
echo "Current Claude desktop config:"
cat "$CONFIG_FILE"

echo
echo "To verify MCP server is working:"
echo "1. Restart Claude Desktop application"
echo "2. Run: claude mcp list"

echo
echo "=== Installation Complete ==="
echo
echo "🎉 Screenshot MCP server is now ready!"
echo
echo "Usage:"
echo "1. Open Claude Code in interactive mode"
echo "2. Use the screenshot tool: 'Take a screenshot of https://example.com'"
echo
echo "If you see 'connecting...' status, wait a moment for the server to initialize."
echo "If you see 'failed' status, check the troubleshooting section in README.md"
echo