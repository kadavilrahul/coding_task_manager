#!/bin/bash

# MCP Server Management Commands
# All successful commands for managing MCP servers

echo "=== MCP Server Management Commands ==="
echo

# Prerequisites check
echo "1. Check Prerequisites:"
echo "node --version          # Check Node.js version"
echo "claude --version        # Check Claude Code CLI"
echo

# Screenshot Server Commands
echo "2. Screenshot Server Commands:"
echo "claude mcp add screenshot-server /root/screenshot-mcp-server.js"
echo "claude mcp remove screenshot-server"
echo

# Context7 Server Commands  
echo "3. Context7 Server Commands:"
echo "claude mcp add context7 npx @upstash/context7-mcp"
echo "claude mcp remove context7"
echo

# General MCP Commands
echo "4. General MCP Commands:"
echo "claude mcp list                    # List all MCP servers"
echo "claude --debug mcp list           # List with debug info"
echo

# Troubleshooting Commands
echo "5. Troubleshooting Commands:"
echo "ls -la ~/.cache/claude-cli-nodejs/-root/mcp-logs-*/         # Check log directories"
echo "cat ~/.cache/claude-cli-nodejs/-root/mcp-logs-*/latest.txt # Read latest logs"
echo

# Example Usage
echo "6. Example Installation Script:"
echo "# Install both servers"
echo "claude mcp add screenshot-server /root/screenshot-mcp-server.js"
echo "claude mcp add context7 npx @upstash/context7-mcp"
echo "claude mcp list"
echo

echo "=== End of Commands ==="