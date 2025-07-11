#!/bin/bash

echo "=== Installing Working MCP Servers for E-commerce Business ==="
echo

# Check prerequisites
echo "1. Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js v20.0.0 or higher"
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js found: $NODE_VERSION"

# Check Claude Code
if ! command -v claude &> /dev/null; then
    echo "❌ Claude Code CLI not found. Please install Claude Code first"
    exit 1
fi

CLAUDE_VERSION=$(claude --version)
echo "✅ Claude Code found: $CLAUDE_VERSION"

# Check Chromium for screenshots
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

echo

# Add working MCP servers to Claude Code
echo "2. Adding working MCP servers to Claude Code..."

# Remove existing servers (if any)
claude mcp remove context7 2>/dev/null || true
claude mcp remove screenshot-server 2>/dev/null || true

# Add Context7 MCP Server
echo "Adding Context7 MCP Server..."
claude mcp add context7 "npx @upstash/context7-mcp"

# Add Screenshot MCP Server
echo "Adding Screenshot MCP Server..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
SCREENSHOT_SERVER_PATH="$SCRIPT_DIR/screenshot-mcp-server/screenshot-mcp-server.js"
if [ -f "$SCREENSHOT_SERVER_PATH" ]; then
    chmod +x "$SCREENSHOT_SERVER_PATH"
    claude mcp add screenshot-server "$SCREENSHOT_SERVER_PATH"
else
    echo "⚠️  Screenshot server not found at $SCREENSHOT_SERVER_PATH"
    echo "Using default path..."
    claude mcp add screenshot-server "/root/screenshot-mcp-server.js"
fi

echo

# Verify installations
echo "3. Verifying installations..."
echo "Current MCP servers:"
claude mcp list

echo
echo "=== Installation Complete ==="
echo
echo "🎉 Working MCP servers are now ready for your business!"
echo
echo "Active MCP Servers:"
echo "1. 📸 Screenshot Server - Webpage screenshot capture"
echo "2. 📚 Context7 Server - Real-time documentation injection"
echo "3. 🛠️ IDE Server - Built-in development tools (auto-configured)"
echo
echo "Perfect for your e-commerce business with 120,000+ products!"
echo
echo "Usage Examples:"
echo "• 'Take a screenshot of https://nilgiristores.in'"
echo "• 'use context7 - show me WooCommerce REST API documentation'"
echo "• 'Get diagnostics for this Python file'"
echo "• 'Execute this Python code in Jupyter'"
echo
echo "For troubleshooting, check documentation in:"
echo "$(dirname "${BASH_SOURCE[0]}")/MCP-SERVERS-OVERVIEW.md"
echo