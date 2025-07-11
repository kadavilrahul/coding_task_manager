# Working MCP Servers for E-commerce & AI Agent Business

Production-ready Model Context Protocol servers specifically optimized for e-commerce businesses managing 120,000+ products and AI agent services in India.

## 🎯 Business Overview

Perfect for managing:
- **120,000+ products** across nilgiristores.in and silkroademart.com
- **Hetzner Ubuntu LAMP stacks** for high-performance e-commerce
- **WordPress/WooCommerce** development and maintenance
- **AI Agent services** for clients in Kerala, India
- **Competitor monitoring** and market research
- **Visual verification** of website changes
- **Development workflows** with current documentation

## 📦 Active MCP Servers

### 1. 📸 Screenshot Server
**Webpage screenshot capture**
- Take screenshots of your websites for monitoring
- Capture competitor site changes
- Visual documentation for clients
- Custom Node.js implementation

**Installation**: `/root/screenshot-mcp-server.js`
**Status**: ✅ Connected

### 2. 📚 Context7 Server
**Real-time documentation injection**
- Get current, version-specific documentation
- Eliminate outdated API examples
- Perfect for staying current with WordPress/WooCommerce
- Supports all major frameworks and libraries

**Installation**: `npx @upstash/context7-mcp`
**Status**: ✅ Connected

### 3. 🛠️ IDE Server (Built-in)
**Development environment integration**
- Get language diagnostics from VS Code
- Execute Python code in Jupyter kernel
- Code analysis and debugging support
- Integrated development tools

**Status**: ✅ Connected (Auto-configured)

## 🚀 Quick Installation

### Working Servers Only
```bash
# Add Context7 MCP Server
claude mcp add context7 "npx @upstash/context7-mcp"

# Add Screenshot MCP Server
claude mcp add screenshot-server "/root/screenshot-mcp-server.js"
```

### Verify Installation
```bash
claude mcp list
```

## 💼 Business Use Cases

### E-commerce Operations
- **Visual monitoring**: Screenshot your websites regularly
- **Competitor analysis**: Capture competitor site changes
- **Documentation**: Always current API references for development
- **Development**: Python/Jupyter support for data analysis

### WordPress/WooCommerce Development
- **Plugin development**: Current documentation and diagnostics
- **Site monitoring**: Visual verification of changes
- **Code analysis**: IDE-level diagnostics and debugging
- **API integration**: Up-to-date documentation for WooCommerce APIs

### AI Agent Services
- **Client documentation**: Screenshot client sites for reports
- **Development support**: Current library documentation
- **Code quality**: IDE diagnostics for clean code
- **Data analysis**: Jupyter kernel for business intelligence

## 📊 Productivity Benefits

### Time Savings
- **Automated screenshots**: Monitor multiple sites visually
- **Current documentation**: No more outdated examples
- **IDE integration**: Professional development environment
- **Quick diagnostics**: Immediate code feedback

### Quality Improvements
- **Visual verification**: See changes before deploying
- **Code analysis**: Catch issues early with IDE diagnostics
- **Current APIs**: Always up-to-date library information
- **Professional tools**: IDE-level development support

## 🔧 Technical Integration

### Your Infrastructure
- **Hetzner Cloud**: Screenshot your server dashboards
- **WordPress Sites**: Monitor visual changes
- **Development**: Python/Jupyter for analytics
- **Documentation**: Current API references

### Development Workflow
1. **Code with IDE Server**: Professional diagnostics and debugging
2. **Document with Context7**: Get current library documentation
3. **Verify with Screenshots**: Visual confirmation of changes
4. **Analyze with Python**: Use Jupyter for data insights

## 📈 Usage Examples

### Screenshot Operations
```
Take a screenshot of https://nilgiristores.in
Take a screenshot of competitor site https://example.com
Screenshot the admin dashboard
```

### Documentation Lookup
```
use context7 - show me WooCommerce REST API documentation
use context7 - get current WordPress plugin development guide
use context7 - find React hooks documentation
```

### Development Support
```
Get diagnostics for this Python file
Execute this Python code in Jupyter
Analyze this JavaScript code
```

## 🛡️ Security & Reliability

### Tested Servers
- **Screenshot Server**: Custom Node.js implementation, battle-tested
- **Context7**: Official Upstash server, actively maintained
- **IDE Server**: Built-in Claude Code functionality, stable

### Safe Operations
- **No system access**: Screenshot and documentation only
- **Read-only operations**: No file modifications
- **Secure execution**: Controlled Python/Jupyter environment

## 🌍 India-Specific Benefits

### E-commerce Focus
- **Monitor Indian marketplaces**: Screenshot Flipkart, Amazon India
- **Regional documentation**: Get India-specific payment APIs
- **Local development**: Python tools for INR calculations
- **Visual verification**: Monitor your Kerala-based business sites

### Business Intelligence
- **Data analysis**: Use Jupyter for sales analytics
- **Market research**: Screenshot competitor pricing
- **Documentation**: Current Indian payment gateway APIs
- **Development**: IDE support for multilingual sites

## 📚 Documentation

Active server documentation:
- `screenshot-mcp-server/README.md` - Screenshot capture
- `context7-mcp-server/README.md` - Documentation injection

## 🔍 Troubleshooting

### Common Issues
- **Screenshot timeouts**: Check network connectivity
- **Context7 limits**: Monitor API usage
- **IDE connectivity**: Restart Claude Code if needed

### Debug Commands
```bash
# Check server status
claude mcp list

# Enable debug mode
claude --debug

# Test screenshot server
node /root/screenshot-mcp-server.js --help
```

## 📞 Support & Resources

### Active Repositories
- **Screenshot Server**: Custom implementation
- **Context7**: https://github.com/upstash/context7
- **IDE Server**: Built-in Claude Code functionality

### Getting Help
- **GitHub Issues**: Report problems with specific servers
- **Documentation**: Server-specific guides
- **Community**: Claude Code community support

---

*Streamlined setup with 3 working MCP servers for your e-commerce business with 120,000+ products in Kerala, India.*