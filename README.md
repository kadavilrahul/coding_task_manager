# Coding Task Manager

A comprehensive suite of AI-powered development tools that provides structured workflows for software development, code analysis, and project management. This toolkit includes six specialized script collections for different aspects of development assistance.

## 🚀 Overview

The Coding Task Manager consists of seven main components:

- **AI-Powered Development**: AI-powered PRD generation and development SOPs
- **Basic Coding Assistant**: Basic coding assistant with function extraction tools  
- **Advanced Coding Assistant**: Advanced coding assistant with comprehensive analysis and reporting
- **File Versioning System**: File versioning system with real-time backup monitoring
- **Flowchart Generator**: Streamlined flowchart generation in HTML and PNG formats
- **Remote Linux Tools**: Automated remote Linux server login and command execution
- **Docker MCP**: Model Context Protocol server setup with Docker for browser automation

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🛠️ Root Utility Scripts](#root-utility-scripts)
- [📁 Script Collections](#-script-collections)
  - [AI-Powered Development Tools](#ai-powered-development-tools)
  - [Basic Coding Assistant](#basic-coding-assistant)
  - [Advanced Coding Assistant](#advanced-coding-assistant)
  - [File Versioning System](#file-versioning-system)
  - [Flowchart Generator](#flowchart-generator)
  - [Remote Linux Tools](#remote-linux-tools)
  - [Docker MCP](#docker-mcp)
- [🛠️ Utilities](#-utilities)
- [💻 Installation](#-installation)
- [📚 Usage Examples](#-usage-examples)
- [⚙️ Configuration](#️-configuration)
- [🔧 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [📊 Project Statistics](#-project-statistics)
- [🔗 Related Projects](#-related-projects)
- [🚦 Status](#-status)

## ✨ Features

### 🤖 AI-Powered Development
- **PRD Generation**: Create detailed Product Requirements Documents using Gemini/Claude AI
- **Standard Operating Procedures**: JSON-based SOPs for AI-assisted development
- **MCP Integration**: Model Context Protocol setup for GitHub Copilot and Cline
- **Code Generation Guidelines**: Structured prompts for consistent code quality

### 📊 Code Analysis & Metrics
- **Line Counting**: Comprehensive code metrics with CLOC integration
- **Function Extraction**: Multiple methods (grep, ctags, AST) for function discovery
- **Pattern Search**: Fast text search with RipGrep/grep fallback
- **Quality Linting**: ShellCheck, JSON validation, and code quality checks

### 🔍 Project Intelligence
- **Structure Analysis**: Automated project structure generation
- **Sensitive Data Scanning**: Security-focused content analysis
- **Git Statistics**: Repository metrics and contributor analysis
- **Comprehensive Reporting**: Markdown reports with timestamped outputs

### 🔄 File Management & Backup
- **Real-time Monitoring**: Automatic file change detection with inotify
- **Timestamped Backups**: Automatic backup creation on file modifications
- **Smart Filtering**: Configurable ignore patterns for selective monitoring
- **Background Operation**: Non-intrusive process management with PID tracking

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kadavilrahul/coding_task_manager.git
   ```
   ```bash
   cd coding_task_manager
   ```

2. **Root utility**:

   A unified script that combines functionality from all script collections into a single executable.

   ```bash
   bash run.sh
   ```
   Interactive tool for counting and comparing total lines of code across multiple codebases.

   ```bash
   bash compare.sh
   ```

3. **Choose your script collection**:
   ```bash
   # For AI-powered PRD generation
   cd ai_powered_development
   
   # For basic coding assistance
   cd basic_coding_assistant
   
   # For advanced analysis tools
   cd advanced_coding_assistant
   
   # For file versioning and backup
   cd file_versioning_system
   
   # For flowchart generation
   cd flowchart_generator
   
   # For remote Linux operations
   cd remote_linux_tools
   ```

4. **Follow the specific setup instructions** for your chosen collection below.

## Root Utility Scripts

The repository includes two utility scripts in the root directory for quick access:

### [`run.sh`](run.sh) - Comprehensive Shell Script Runner
A unified script that combines functionality from all script collections into a single executable.

**Features:**
- **Project Analysis**: Generate comprehensive project information and structure
- **Code Metrics**: CLOC integration for detailed line counting
- **Function Discovery**: Multiple methods (grep, ctags, AST) for function extraction
- **File Monitoring**: Real-time file versioning and backup capabilities
- **Quality Tools**: Linting, validation, and code quality checks
- **Interactive & CLI Modes**: Flexible usage options

**Usage:**
```bash
# Run interactively
./run.sh

# Or use specific functions directly
./run.sh generate_project_info
./run.sh install_and_run_cloc
./run.sh collect_functions_interactive
```

### [`compare.sh`](compare.sh) - Codebase Line Counter & Comparator
Interactive tool for counting and comparing total lines of code across multiple codebases.

**Features:**
- **Multi-Codebase Analysis**: Compare line counts across different projects
- **Interactive Interface**: User-friendly prompts for folder selection
- **Automated Reporting**: Results saved to `codebase_line_counts.txt`
- **Error Handling**: Validates paths and handles missing directories

**Usage:**
```bash
./compare.sh
# Follow prompts to enter codebase paths
# Type 'quit' or 'q' to finish and generate report
```

---

## 📁 Script Collections

### AI-Powered Development Tools

**Purpose**: AI-powered PRD generation, development SOPs, and MCP integration for enhanced coding workflows.

#### 🛠️ Tools Included
- `00_generate_prd.py` - Multi-model PRD generator (Gemini/Claude)
- `00_generate_code_using_sop.json` - Comprehensive development SOP
- `00_generate_run_script.json` - Run script generation prompts
- `00_generate_project_info.sh` - Project structure and analysis
- `00_generate_mcp.md` - MCP setup for GitHub Copilot/Cline

#### 📦 Installation
```bash
cd ai_powered_development
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

#### ⚙️ Configuration
Create a `.env` file:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_claude_api_key_here  # Optional
```

#### 🚀 Usage
```bash
# Generate project information
bash 00_generate_project_info.sh

# Generate PRD with AI
python 00_generate_prd.py

# Follow MCP setup instructions
cat 00_generate_mcp.md
```

---

### Basic Coding Assistant

**Purpose**: Essential coding assistance with function extraction and basic code analysis tools.

#### 🛠️ Tools Included
- `extract_functions.py` - Python AST-based function extraction
- `collect_functions.sh` - Multi-method function collection (grep/ctags/AST)
- `run_cloc.sh` - Automated CLOC installation and execution
- `sop.json` - Basic coding assistant guidelines

#### 📦 Installation
```bash
cd basic_coding_assistant
# Optional: Create virtual environment for Python scripts
python3 -m venv venv
source venv/bin/activate
```

#### 🚀 Usage
```bash
# Extract functions using different methods
bash collect_functions.sh

# Run code analysis
bash run_cloc.sh

# Extract Python functions specifically
python extract_functions.py
```

---

### Advanced Coding Assistant

**Purpose**: Professional-grade coding assistance with comprehensive analysis, reporting, and quality tools.

#### 🛠️ Tools Included
- `coding_assistant_tools.sh` - Multi-functional analysis toolkit
- `sop.json` - Advanced coding assistant guidelines

#### 📦 Features
- **Code Metrics**: CLOC integration for detailed statistics
- **Pattern Search**: RipGrep/grep with fallback support
- **Quality Checks**: ShellCheck, JSON validation
- **Git Analysis**: Repository statistics and history
- **Report Generation**: Timestamped Markdown reports
- **Interactive & CLI Modes**: Flexible usage options

#### 🚀 Usage

**Interactive Mode**:
```bash
cd advanced_coding_assistant
./coding_assistant_tools.sh
```

**Command Line Mode**:
```bash
# Count lines of code
./coding_assistant_tools.sh cloc

# Search for patterns
./coding_assistant_tools.sh search "TODO"

# Generate comprehensive report
./coding_assistant_tools.sh report

# Lint shell scripts
./coding_assistant_tools.sh lint-sh
```

---

### File Versioning System

**Purpose**: Lightweight file versioning system with real-time monitoring and automatic backup creation using Linux inotify.

#### 🛠️ Tools Included
- `file_versioning.sh` - Main monitoring script with inotify integration
- `check_versioning.sh` - Status checker and process management
- `setup_file_versioning.sh` - Automated setup and configuration

#### 📦 Features
- **Real-time Monitoring**: Uses Linux inotify for instant file change detection
- **Automatic Backups**: Creates timestamped backups on file modifications
- **Smart Filtering**: `.versioningignore` file for excluding unwanted files
- **Process Management**: PID tracking for easy start/stop operations
- **Background Operation**: Non-intrusive monitoring with log output
- **AI-Editor Friendly**: Perfect for use with AI-based code editors

#### 📋 Prerequisites
```bash
# Ubuntu/Debian
sudo apt-get install inotify-tools

# CentOS/RHEL
sudo yum install inotify-tools
```

#### 🚀 Usage

**Quick Setup**:
```bash
cd file_versioning_system
# Copy scripts to your target directory
cp {setup_file_versioning.sh,file_versioning.sh,check_versioning.sh} /path/to/your/project/
cd /path/to/your/project/

# Run setup and start monitoring
bash setup_file_versioning.sh
nohup bash file_versioning.sh > file_versioning.log 2>&1 &
```

**Management Commands**:
```bash
# Check status
bash check_versioning.sh

# Stop monitoring
pkill -f file_versioning.sh
```

#### 📁 File Organization
- `backups/` - Timestamped backup files (auto-created)
- `.versioningignore` - Ignore patterns configuration
- `.file_versioning.pid` - Process ID for management
- `file_versioning.log` - Monitoring activity log

---

### Flowchart Generator

**Purpose**: Streamlined flowchart generation in HTML and PNG formats for AI workflows and documentation.

#### 🛠️ Tools Included
- `setup_flowchart.sh` - Automated setup and dependency installation
- `generate.sh` - Flowchart generation script

#### 📦 Features
- Command line based flowchart generation environment
- Automated dependency management and setup
- HTML and PNG output formats
- Easy-to-use command line interface
- Automatic environment configuration

#### 🚀 Usage

**First time setup**:
```bash
cd flowchart_generator
bash setup_flowchart.sh
```

**Subsequent runs**:
```bash
bash generate.sh
```

#### 🔧 System Requirements
- Linux system with GUI (GUI needed to view files)
- Tested on Ubuntu 24.04 LTS

---

### Remote Linux Tools

**Purpose**: Automated remote Linux server login and command execution for distributed development workflows.

#### 🛠️ Tools Included
- `main.sh` - Main automation script for remote command execution
- `test_login_manually.sh` - Interactive login testing script
- `test_run_commands_with_manual_login.sh` - Combined login and command execution test

#### 📦 Features
- **Secure SSH Authentication**: Multiple authentication methods supported
- **Automated Command Execution**: Execute commands on remote servers automatically
- **Configurable Settings**: Easy-to-configure remote server parameters
- **Error Handling**: Robust error handling and validation
- **Interactive Testing**: Manual testing capabilities for debugging
- **Batch Operations**: Support for running multiple commands

#### 🚀 Usage

**Configuration**:
```bash
cd remote_linux_tools
# Edit main.sh to configure:
DEFAULT_USER="your_username"
DEFAULT_PORT="22"
DEFAULT_IP="remote_server_ip"
DEFAULT_PASS="your_password"  # Use SSH keys instead
```

**Automated Execution**:
```bash
bash main.sh
```

**Interactive Testing**:
```bash
bash test_login_manually.sh
bash test_run_commands_with_manual_login.sh
```

---

### Docker MCP

**Purpose**: Model Context Protocol server setup with Docker for browser automation and AI-powered web interactions.

#### 🛠️ Tools Included
- `Dockerfile` - Custom MCP Puppeteer server image
- `docker-compose.yml` - Docker Compose configuration for service management
- `setup.sh` - Automated setup and deployment script
- `configs/claude-config.json` - Claude Desktop integration configuration
- `configs/mcp-puppeteer-server.json` - Basic MCP server configuration

#### 📦 Features
- **Browser Automation**: Puppeteer-based web automation through MCP protocol
- **Docker Integration**: Containerized deployment with official and custom images
- **Claude Desktop Support**: Ready-to-use configurations for AI integration
- **Screenshot Capture**: Automated screenshot functionality with volume mounting
- **Headless Operation**: Chromium-based headless browser automation
- **Security Features**: Digitally signed images with Software Bill of Materials (SBOM)

#### 📋 Prerequisites
```bash
# Docker and Docker Compose
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (optional)
sudo usermod -aG docker $USER
```

#### 🚀 Usage

**Quick Start**:
```bash
cd docker_mcp
# Make setup script executable
chmod +x scripts/setup.sh
# Run automated setup
./scripts/setup.sh
```

**Manual Setup**:
```bash
# Pull official image
docker pull mcp/puppeteer:latest

# Create screenshots directory
mkdir -p screenshots

# Run with Docker Compose
docker-compose up -d

# Or run directly
docker run -i --rm --init -e DOCKER_CONTAINER=true mcp/puppeteer
```

#### ⚙️ Configuration

**Claude Desktop Integration**:
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", "--init",
        "-e", "DOCKER_CONTAINER=true",
        "mcp/puppeteer"
      ]
    }
  }
}
```

**Available MCP Tools**:
- `navigate_to_url` - Navigate to specific URLs
- `screenshot` - Capture webpage screenshots
- `click_element` - Interact with webpage elements
- `execute_javascript` - Run custom JavaScript
- `fill_form` - Fill out web forms
- `wait_for_element` - Wait for elements to appear

#### 🔧 Management Commands
```bash
# Check running containers
docker ps | grep puppeteer

# View logs
docker logs mcp-puppeteer-server

# Stop services
docker-compose down

# Update images
docker pull mcp/puppeteer:latest
docker-compose restart
```

---

## 🛠️ Utilities

The `utilities/` directory contains core tools that support all script collections:

### Tools Included
- **`github_repository_cloner.sh`** - Interactive GitHub repository cloning with API integration
- **`project_analyzer.sh`** - Comprehensive project analysis and reporting
- **`codebase_comparator.sh`** - Multi-codebase line count comparison
- **`config.json`** - Configuration file for GitHub operations

### Usage
```bash
cd utilities
bash github_repository_cloner.sh    # Clone GitHub repositories
bash project_analyzer.sh            # Analyze projects
bash codebase_comparator.sh         # Compare codebases
```

---

## 💻 Installation

### Prerequisites
- **Python 3.8+** (for AI-Powered Development & Basic Coding Assistant)
- **Bash shell** (Linux/macOS/WSL)
- **Git** (for repository operations)
- **inotify-tools** (for File Versioning System - Linux only)

### Optional Dependencies
The tools gracefully handle missing dependencies:
- `cloc` - Code line counting
- `ripgrep` (rg) - Fast pattern searching
- `tree` - Directory visualization
- `shellcheck` - Shell script linting
- `jq` - JSON processing
- `ctags` - Code indexing
- `inotify-tools` - Real-time file monitoring (required for Scripts 04)

### API Keys (AI-Powered Development only)
- **Gemini API Key**: Required for Google's Gemini models
- **Anthropic API Key**: Optional for Claude models

## 📚 Usage Examples

### Generate a Complete Project Analysis
```bash
# Using AI-Powered Development
cd ai_powered_development
bash 00_generate_project_info.sh
python 00_generate_prd.py

# Using Advanced Coding Assistant for detailed analysis
cd ../advanced_coding_assistant
./coding_assistant_tools.sh report
```

### Code Quality Workflow
```bash
cd advanced_coding_assistant

# Check shell scripts
./coding_assistant_tools.sh lint-sh

# Validate JSON files
./coding_assistant_tools.sh lint-json

# Search for TODOs and FIXMEs
./coding_assistant_tools.sh search "TODO|FIXME"
```

### Function Discovery Workflow
```bash
cd basic_coding_assistant

# Interactive method selection
bash collect_functions.sh

# Direct Python AST extraction
python extract_functions.py
```

## ⚙️ Configuration

### Environment Variables (AI-Powered Development)
```bash
# Required for AI features
GEMINI_API_KEY=your_key_here

# Optional for Claude support
ANTHROPIC_API_KEY=your_key_here
```

### Tool Preferences (Advanced Coding Assistant)
The advanced tools automatically detect and prefer:
- `ripgrep` over `grep` for searching
- `tree` over `find` for directory listing
- Native tools when specialized ones aren't available

## 🔧 Troubleshooting

### Common Issues

#### AI-Powered Development
- **`ValueError: Missing GEMINI_API_KEY`**: Create `.env` file with valid API key
- **`ModuleNotFoundError`**: Activate virtual environment and run `pip install -r requirements.txt`
- **`google-genai` errors**: Ensure `pip install google-genai` completed successfully

#### Basic & Advanced Coding Assistant
- **Permission denied**: Make scripts executable with `chmod +x *.sh`
- **Command not found**: Install missing dependencies or use fallback options
- **No functions found**: Ensure you're in a directory with code files

### Tool Installation

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install cloc ripgrep tree shellcheck jq exuberant-ctags inotify-tools
```

#### macOS (with Homebrew)
```bash
brew install cloc ripgrep tree shellcheck jq ctags
# Note: inotify-tools not available on macOS (File Versioning System requires Linux)
```

#### Windows (WSL recommended)
Use WSL with Ubuntu and follow the Ubuntu installation steps.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow the 150-line modularity constraint from AI-Powered Development SOP
- Add comprehensive error handling
- Include usage examples in documentation
- Test on multiple platforms when possible

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📊 Project Statistics

```bash
# Get project overview
find . -name "*.py" -o -name "*.sh" -o -name "*.json" -o -name "*.md" | wc -l
# Expected: ~15+ files across all script collections

# Check script collections
ls -la */
```

## 🔗 Related Projects

- [GitHub Copilot](https://github.com/features/copilot) - AI pair programmer
- [Cline](https://github.com/clinebot/cline) - AI coding assistant
- [CLOC](https://github.com/AlDanial/cloc) - Count Lines of Code
- [RipGrep](https://github.com/BurntSushi/ripgrep) - Fast text search

## 🚦 Status

- ✅ **AI-Powered Development**: Stable - AI-powered PRD generation working
- ✅ **Basic Coding Assistant**: Stable - Basic coding assistance tools functional  
- ✅ **Advanced Coding Assistant**: Stable - Advanced analysis tools with comprehensive reporting
- ✅ **File Versioning System**: Stable - File versioning system with real-time monitoring
- ✅ **Flowchart Generator**: Stable - Flowchart generation in HTML and PNG formats
- ✅ **Remote Linux Tools**: Stable - Remote SSH automation and command execution
- ✅ **Docker MCP**: Stable - Model Context Protocol server with Docker for browser automation
- ✅ **Utilities**: Stable - Core utility tools for project management
- 🔄 Continuous improvements and feature additions

## 🙏 Acknowledgments

- Google Gemini API for AI-powered PRD generation
- Anthropic Claude for additional AI model support
- The open-source community for the excellent tools integrated into this project
- Contributors who help improve and maintain this toolkit

---

**Made with ❤️ for developers who want to enhance their coding workflow with AI assistance and comprehensive analysis tools.**
