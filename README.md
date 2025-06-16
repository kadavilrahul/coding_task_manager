# Coding Task Manager

A comprehensive suite of AI-powered development tools that provides structured workflows for software development, code analysis, and project management. This toolkit includes four specialized script collections for different aspects of development assistance.

## 🚀 Overview

The Coding Task Manager consists of four main components:

- **Scripts 01**: AI-powered PRD generation and development SOPs
- **Scripts 02**: Basic coding assistant with function extraction tools  
- **Scripts 03**: Advanced coding assistant with comprehensive analysis and reporting
- **Scripts 04**: File versioning system with real-time backup monitoring

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📁 Script Collections](#-script-collections)
  - [Scripts 01: AI-Powered Development Tools](#scripts-01-ai-powered-development-tools)
  - [Scripts 02: Basic Coding Assistant](#scripts-02-basic-coding-assistant)
  - [Scripts 03: Advanced Coding Assistant](#scripts-03-advanced-coding-assistant)
  - [Scripts 04: File Versioning System](#scripts-04-file-versioning-system)
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

2. **Choose your script collection**:
   ```bash
   # For AI-powered PRD generation
   cd scripts_01
   
   # For basic coding assistance
   cd scripts_02
   
   # For advanced analysis tools
   cd scripts_03
   
   # For file versioning and backup
   cd scripts_04
   ```

3. **Follow the specific setup instructions** for your chosen collection below.

## 📁 Script Collections

### Scripts 01: AI-Powered Development Tools

**Purpose**: AI-powered PRD generation, development SOPs, and MCP integration for enhanced coding workflows.

#### 🛠️ Tools Included
- `00_generate_prd.py` - Multi-model PRD generator (Gemini/Claude)
- `00_generate_code_using_sop.json` - Comprehensive development SOP
- `00_generate_run_script.json` - Run script generation prompts
- `00_generate_project_info.sh` - Project structure and analysis
- `00_generate_mcp.md` - MCP setup for GitHub Copilot/Cline

#### 📦 Installation
```bash
cd scripts_01
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

### Scripts 02: Basic Coding Assistant

**Purpose**: Essential coding assistance with function extraction and basic code analysis tools.

#### 🛠️ Tools Included
- `extract_functions.py` - Python AST-based function extraction
- `collect_functions.sh` - Multi-method function collection (grep/ctags/AST)
- `run_cloc.sh` - Automated CLOC installation and execution
- `sop.json` - Basic coding assistant guidelines

#### 📦 Installation
```bash
cd scripts_02
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

### Scripts 03: Advanced Coding Assistant

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
cd scripts_03
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

### Scripts 04: File Versioning System

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
cd scripts_04
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

## 💻 Installation

### Prerequisites
- **Python 3.8+** (for Scripts 01 & 02)
- **Bash shell** (Linux/macOS/WSL)
- **Git** (for repository operations)
- **inotify-tools** (for Scripts 04 - Linux only)

### Optional Dependencies
The tools gracefully handle missing dependencies:
- `cloc` - Code line counting
- `ripgrep` (rg) - Fast pattern searching
- `tree` - Directory visualization
- `shellcheck` - Shell script linting
- `jq` - JSON processing
- `ctags` - Code indexing
- `inotify-tools` - Real-time file monitoring (required for Scripts 04)

### API Keys (Scripts 01 only)
- **Gemini API Key**: Required for Google's Gemini models
- **Anthropic API Key**: Optional for Claude models

## 📚 Usage Examples

### Generate a Complete Project Analysis
```bash
# Using Scripts 01
cd scripts_01
bash 00_generate_project_info.sh
python 00_generate_prd.py

# Using Scripts 03 for detailed analysis
cd ../scripts_03
./coding_assistant_tools.sh report
```

### Code Quality Workflow
```bash
cd scripts_03

# Check shell scripts
./coding_assistant_tools.sh lint-sh

# Validate JSON files
./coding_assistant_tools.sh lint-json

# Search for TODOs and FIXMEs
./coding_assistant_tools.sh search "TODO|FIXME"
```

### Function Discovery Workflow
```bash
cd scripts_02

# Interactive method selection
bash collect_functions.sh

# Direct Python AST extraction
python extract_functions.py
```

## ⚙️ Configuration

### Environment Variables (Scripts 01)
```bash
# Required for AI features
GEMINI_API_KEY=your_key_here

# Optional for Claude support
ANTHROPIC_API_KEY=your_key_here
```

### Tool Preferences (Scripts 03)
The advanced tools automatically detect and prefer:
- `ripgrep` over `grep` for searching
- `tree` over `find` for directory listing
- Native tools when specialized ones aren't available

## 🔧 Troubleshooting

### Common Issues

#### Scripts 01
- **`ValueError: Missing GEMINI_API_KEY`**: Create `.env` file with valid API key
- **`ModuleNotFoundError`**: Activate virtual environment and run `pip install -r requirements.txt`
- **`google-genai` errors**: Ensure `pip install google-genai` completed successfully

#### Scripts 02 & 03
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
# Note: inotify-tools not available on macOS (Scripts 04 requires Linux)
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
- Follow the 150-line modularity constraint from Scripts 01 SOP
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
ls -la scripts_*/
```

## 🔗 Related Projects

- [GitHub Copilot](https://github.com/features/copilot) - AI pair programmer
- [Cline](https://github.com/clinebot/cline) - AI coding assistant
- [CLOC](https://github.com/AlDanial/cloc) - Count Lines of Code
- [RipGrep](https://github.com/BurntSushi/ripgrep) - Fast text search

## 🚦 Status

- ✅ Scripts 01: Stable - AI-powered PRD generation working
- ✅ Scripts 02: Stable - Basic coding assistance tools functional  
- ✅ Scripts 03: Stable - Advanced analysis tools with comprehensive reporting
- ✅ Scripts 04: Stable - File versioning system with real-time monitoring
- 🔄 Continuous improvements and feature additions

## 🙏 Acknowledgments

- Google Gemini API for AI-powered PRD generation
- Anthropic Claude for additional AI model support
- The open-source community for the excellent tools integrated into this project
- Contributors who help improve and maintain this toolkit

---

**Made with ❤️ for developers who want to enhance their coding workflow with AI assistance and comprehensive analysis tools.**
