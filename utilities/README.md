# Utilities

## Overview
Core utility scripts that provide essential functionality for the coding task manager. These tools can be used independently or integrated with the script collections.

## Tools Included

### `github_repository_cloner.sh`
**Purpose**: Interactive GitHub repository cloning tool with advanced features

**Features**:
- GitHub API integration for repository discovery
- Personal access token support for private repositories
- Interactive repository selection with filtering
- Favorites and recent repositories management
- Configurable clone locations
- Repository information display

**Usage**:
```bash
bash github_repository_cloner.sh
```

### `project_analyzer.sh`
**Purpose**: Comprehensive project analysis and reporting tool

**Features**:
- Interactive directory selection and browsing
- Project structure visualization
- Security scanning for sensitive data
- Code statistics and metrics
- CLOC integration for line counting
- Function extraction from multiple languages
- Pattern searching with ripgrep/grep
- Git repository statistics
- Automated report generation

**Usage**:
```bash
# Interactive mode
bash project_analyzer.sh

# Direct command mode
bash project_analyzer.sh /path/to/project report
bash project_analyzer.sh . cloc
bash project_analyzer.sh . search TODO
```

### `codebase_comparator.sh`
**Purpose**: Interactive tool for comparing line counts across multiple codebases

**Features**:
- Multi-codebase analysis and comparison
- Interactive folder selection
- Automated reporting with timestamps
- Error handling for missing directories
- Results export to text file

**Usage**:
```bash
bash codebase_comparator.sh
# Follow prompts to enter codebase paths
# Type 'quit' or 'q' to finish and generate report
```

### `config.json`
**Purpose**: Configuration file for GitHub repository cloner

**Contains**:
- GitHub credentials (username, token)
- Default clone paths
- Favorites and recent repositories
- Filter preferences

## Installation
No special installation required. Ensure the following dependencies are available:
- `git` - For repository operations
- `curl` - For API calls
- `jq` - For JSON processing (optional, fallback parsing available)
- `fzf` - For enhanced selection (optional)
- `cloc` - For code line counting (optional)
- `ripgrep` - For fast pattern searching (optional)
- `tree` - For directory visualization (optional)

## Integration
These utilities are designed to work seamlessly with all script collections:
- **Scripts 01-04**: Core analysis and development tools
- **Scripts 05**: Flowchart generation workflows
- **Scripts 06**: Remote Linux operations

## Security Notes
- Never commit sensitive credentials to version control
- Use environment variables or secure configuration files
- Set appropriate file permissions for configuration files
- Review generated reports before sharing

## Configuration
Most utilities support configuration through:
- Environment variables
- Configuration files (like `config.json`)
- Interactive prompts
- Command-line arguments

## Output
All utilities generate output in the following locations:
- Reports: `./reports/` directory
- Logs: Individual tool log files
- Configurations: Local configuration files