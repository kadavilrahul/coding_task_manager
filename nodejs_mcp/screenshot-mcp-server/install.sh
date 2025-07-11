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
echo "3. Adding MCP server to Claude Code..."

# Remove existing server if present
claude mcp remove screenshot-server 2>/dev/null || true

# Add server
claude mcp add screenshot-server "$SERVER_PATH"

if [ $? -eq 0 ]; then
    echo "✅ MCP server added successfully"
else
    echo "❌ Failed to add MCP server"
    exit 1
fi

echo

# Verify installation
echo "4. Verifying installation..."

# List MCP servers
echo "Current MCP servers:"
claude mcp list

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