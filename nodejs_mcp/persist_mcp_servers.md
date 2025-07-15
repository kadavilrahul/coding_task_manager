# Persisting MCP Servers After Reboot

MCP servers don't persist across reboots by default. This guide shows how to automatically restore them.

## Method 1: Using .bashrc (Recommended)

Add these commands to your `.bashrc` file:

```bash
# Auto-configure MCP servers for Claude
claude mcp add screenshot npx @anthropic-ai/mcp-server-screenshot 2>/dev/null
claude mcp add context7 npx @anthropic-ai/mcp-server-context7 2>/dev/null
```

The `2>/dev/null` suppresses error messages if the servers are already configured.

## Method 2: Manual Restoration

If you need to manually restore your MCP servers, run:

```bash
claude mcp add screenshot npx @anthropic-ai/mcp-server-screenshot
claude mcp add context7 npx @anthropic-ai/mcp-server-context7
```

## Verification

Check that your MCP servers are configured:

```bash
claude mcp list
```

## Troubleshooting

- If servers don't appear after reboot, source your `.bashrc`: `source ~/.bashrc`
- If you get permission errors, ensure the MCP packages are installed globally
- Configuration is stored in `~/.config/claude-code/settings.json`