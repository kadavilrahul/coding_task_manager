#!/bin/bash

# Browser Tools MCP Installation Script
# Run this script to install and configure Browser Tools MCP

echo "Installing Browser Tools MCP..."

# Install the MCP package globally
echo "Step 1: Installing Browser Tools MCP package globally..."
npm install -g @agentdeskai/browser-tools-mcp@1.2.1

# Add to Claude MCP configuration
echo "Step 2: Adding to Claude MCP configuration..."
claude mcp add browser-tools "browser-tools-mcp"

# Create Claude Desktop config directory if it doesn't exist
echo "Step 3: Setting up Claude Desktop configuration..."
mkdir -p ~/.config/claude-desktop

# Copy the configuration file
cp claude_desktop_config.json ~/.config/claude-desktop/claude_desktop_config.json

# Verify installation
echo "Step 4: Verifying installation..."
claude mcp list

echo "✅ Browser Tools MCP installation complete!"
echo ""
echo "Available MCP servers:"
claude mcp list