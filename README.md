# Coding Task Manager

A comprehensive collection of task management tools designed to streamline software development workflows through intelligent automation, code analysis, and documentation generation. This repository contains multiple implementations ranging from simple Python scripts to sophisticated AI-powered systems.

## 🚀 Overview

The Coding Task Manager provides developers with powerful tools to:
- **Automate task creation** from Product Requirements Documents (PRDs)
- **Analyze code complexity** and dependencies
- **Generate comprehensive documentation** automatically
- **Manage development workflows** efficiently
- **Integrate AI assistance** for code analysis and modification

## 📁 Repository Structure

This repository contains five different versions, each designed for different use cases and complexity levels:

### 🐍 Python Implementations

#### **Version 1: Simple Python Tools** (`version_01_py_simple/`)
- **Best for**: Quick task management and PRD parsing
- **Features**: Basic task CRUD operations, PRD parsing, complexity analysis
- **Dependencies**: Python 3.x (no external libraries)
- **Use case**: Small projects, learning, rapid prototyping

#### **Version 2: Sophisticated AI System** (`version_02_py_sophisticated/`)
- **Best for**: Enterprise-level development workflows
- **Features**: AI agents, AST analysis, automated code generation, comprehensive testing
- **Dependencies**: Python 3.8+, OpenAI/Anthropic APIs, FastAPI, extensive ML stack
- **Use case**: Large projects, team collaboration, production environments

### 🔧 Shell Script Implementations

#### **Version 3: Comprehensive Shell Scripts** (`version_03_shellscript/`)
- **Best for**: Unix/Linux environments, CI/CD integration
- **Features**: Multi-language support, secure API handling, advanced file operations
- **Dependencies**: Bash, jq, curl, tree
- **Use case**: DevOps workflows, automated builds, cross-platform compatibility

#### **Version 4: Simple Shell Script** (`version_04_shellscript_simple/`)
- **Best for**: Quick project analysis
- **Features**: Basic project information extraction
- **Dependencies**: Bash
- **Use case**: Rapid project assessment, minimal setup requirements

### 📋 Specialized Tools

#### **Version 5: PRD Generator** (`version_05_prd_generator/`)
- **Best for**: Documentation-focused workflows
- **Features**: AI-powered PRD generation, project analysis
- **Dependencies**: Python 3.x, AI APIs
- **Use case**: Product management, requirement documentation

## 🎯 Quick Start Guide

### Choose Your Version

1. **For beginners or simple projects**: Start with `version_01_py_simple/`
2. **For enterprise or complex projects**: Use `version_02_py_sophisticated/`
3. **For shell/DevOps workflows**: Try `version_03_shellscript/`
4. **For quick analysis**: Use `version_04_shellscript_simple/`
5. **For documentation focus**: Use `version_05_prd_generator/`

### Basic Usage Example (Version 1)

```bash
https://github.com/kadavilrahul/coding_task_manager.git
```

```bash
# Navigate to the simple Python version
cd version_01_py_simple/

# Parse a PRD file to generate tasks
python3 prd_parser.py sample_prd.txt

# Manage tasks
python3 task_manager.py list
python3 task_manager.py add --task_name "Implement user login"

# Analyze task complexity
python3 complexity_analyzer.py "Implement user login"
```

### Advanced Usage Example (Version 2)

```bash
# Navigate to the sophisticated version
cd version_02_py_sophisticated/

# Install dependencies
pip install -r requirements.txt

# Run interactive mode
python main.py --interactive

# Generate PRD
python main.py generate-prd "My Project" --description "Project description"

# Analyze code
python main.py analyze path/to/file.py --output analysis.json
```

### Shell Script Example (Version 3)

```bash
# Navigate to shell script version
cd version_03_shellscript/

# Analyze project
./project_info.sh

# Generate PRD using AI
./generate_prd.sh --project "My Project" --description "Description"

# Extract functions from code
./extract_functions.sh --file src/main.py --language python
```

## 🛠 Installation

### Prerequisites

**For Python versions:**
- Python 3.7+ (Version 1)
- Python 3.8+ (Version 2)
- pip package manager

**For Shell script versions:**
- Bash shell
- Standard Unix tools (jq, curl, tree for Version 3)

**For AI features:**
- Gemini API key
- Internet connection

### Quick Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kadavilrahul/coding_task_manager.git
   cd coding_task_manager
   ```

2. **Choose and navigate to your preferred version:**
   ```bash
   cd version_01_py_simple/  # or your chosen version
   ```

3. **Follow the specific installation instructions** in each version's README.md

## 📚 Documentation

Each version contains its own detailed documentation:

- `version_01_py_simple/README.md` - Simple Python tools guide
- `version_02_py_sophisticated/README.md` - Comprehensive AI system documentation
- `version_03_shellscript/README.md` - Shell script tools guide
- `version_04_shellscript_simple/README.md` - Simple shell script usage
- `version_05_prd_generator/README.md` - PRD generator documentation

## 🔧 Configuration

### Environment Variables

For AI-powered features, set up your API keys:

```bash
# For OpenAI (GPT models)
export OPENAI_API_KEY="your-openai-api-key"

# For Anthropic (Claude models)
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# For Google (Gemini models)
export GEMINI_API_KEY="your-gemini-api-key"
```

### Project Configuration

Most versions support configuration files for customizing behavior:
- `.task-config.json` - Project-specific settings
- `.ai-context.json` - AI context and preferences
- `config.json` - Application configuration

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Guidelines

- Follow the existing code style in each version
- Add tests for new features
- Update documentation as needed
- Ensure backward compatibility when possible

## 📄 License

This project is licensed under the MIT License - see the individual LICENSE files in each version directory for details.

## 🆘 Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/kadavilrahul/coding_task_manager/issues)
- **Documentation**: Check the README.md in each version directory
- **Examples**: See the sample files included in each version

## 🔄 Version Comparison

| Feature | V1 Simple | V2 Sophisticated | V3 Shell | V4 Simple Shell | V5 PRD Gen |
|---------|-----------|------------------|----------|-----------------|------------|
| Task Management | ✅ Basic | ✅ Advanced | ❌ | ❌ | ❌ |
| PRD Parsing | ✅ | ✅ | ✅ | ❌ | ✅ |
| AI Integration | ❌ | ✅ Full | ✅ API | ❌ | ✅ Limited |
| Code Analysis | ✅ Basic | ✅ AST-based | ✅ Multi-lang | ✅ Basic | ✅ Basic |
| Dependencies | None | Heavy | Light | None | Light |
| Complexity | Low | High | Medium | Very Low | Low |
| Best For | Learning | Production | DevOps | Quick Analysis | Documentation |

## 🚀 Roadmap

- [ ] Web-based interface for task management
- [ ] Integration with popular IDEs (VS Code, IntelliJ)
- [ ] Support for more programming languages
- [ ] Enhanced AI model integration
- [ ] Real-time collaboration features
- [ ] Mobile application
- [ ] Docker containerization
- [ ] Kubernetes deployment templates

---

**Made with ❤️ for developers who want to focus on coding, not task management.**
