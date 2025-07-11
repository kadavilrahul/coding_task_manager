#!/bin/bash

echo "=== Installing All MCP Servers for E-commerce & AI Agent Business ==="
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

# Check uv for Serena
if ! command -v uv &> /dev/null; then
    echo "❌ uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source ~/.bashrc
fi

echo "✅ uv found: $(uv --version)"

# Check Git
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git"
    exit 1
fi

echo "✅ Git found: $(git --version)"

echo

# Add all MCP servers to Claude Code
echo "2. Adding MCP servers to Claude Code..."

# Remove existing servers (if any)
claude mcp remove git-mcp 2>/dev/null || true
claude mcp remove shell-mcp 2>/dev/null || true
claude mcp remove puppeteer-mcp 2>/dev/null || true
claude mcp remove context7 2>/dev/null || true
claude mcp remove screenshot-server 2>/dev/null || true


# Add Git MCP Server
echo "Adding Git MCP Server..."
claude mcp add git-mcp "npx @cyanheads/git-mcp-server"

# Add Shell MCP Server
echo "Adding Shell MCP Server..."
claude mcp add shell-mcp "npx @mkusaka/mcp-shell-server"

# Add Puppeteer MCP Server
echo "Adding Puppeteer MCP Server..."
claude mcp add puppeteer-mcp "npx @modelcontextprotocol/server-puppeteer"

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
fi

echo

# Verify installations
echo "4. Verifying installations..."
echo "Current MCP servers:"
claude mcp list

echo
echo "=== Installation Complete ==="
echo
echo "🎉 All MCP servers are now ready for your business!"
echo
echo "Installed MCP Servers:"
echo "1. 📝 Git MCP - Repository management and version control"
echo "2. 💻 Shell MCP - Server management and system operations"
echo "3. 🌐 Puppeteer MCP - Web scraping and browser automation"
echo "4. 📚 Context7 MCP - Real-time documentation injection"
echo "5. 📸 Screenshot MCP - Webpage screenshot capture"
echo
echo "Perfect for your e-commerce business with 120,000+ products!"
echo
echo "Usage Examples:"
echo "• 'Take a screenshot of https://nilgiristores.in'"
echo "• 'Scrape product data from competitor website'"
echo "• 'Check server status on Hetzner servers'"
echo "• 'Analyze WordPress code for optimization'"
echo "• 'use context7 - show me WooCommerce best practices'"
echo "• 'Commit changes to Git repository'"
echo
echo "For troubleshooting, check individual server documentation in:"
echo "$(dirname "${BASH_SOURCE[0]}")/*/README.md"
echo