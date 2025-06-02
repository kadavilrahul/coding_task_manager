# Agno Code Tools - Simple Version

A simplified version of the code analysis tools combining shell scripts for project analysis with Python-based AI agents for PRD generation using the Agno framework.

## Features

### project_info.sh (Shell Script)
Gathers essential project information including:
- **Project Structure**: Directory tree (using `tree` command or `find` fallback)
- **Sensitive Information Scan**: Detects potential API keys, secrets, passwords, tokens
- **Lines of Code**: Counts lines for multiple programming languages
- **Summary Statistics**: Total files and lines count

### generate_prd.py (Python + Agno Framework)
AI-powered Product Requirements Document generator using multi-agent workflow:
- **Multi-Agent Architecture**: Three specialized agents working in sequence
  - **ProjectAnalyst-X**: Analyzes codebase and extracts product insights
  - **RequirementsEngineer-X**: Converts technical features into structured requirements
  - **PRDMaster-X**: Crafts comprehensive, professional PRDs
- **Intelligent Analysis**: Deep analysis of project structure and functionality
- **Structured Output**: Professional PRDs with all essential sections
- **Caching System**: Efficient caching for faster subsequent runs
- **Customizable**: Extensible agent framework for domain-specific needs

**Supported File Types:**
- Python (*.py)
- JavaScript (*.js)
- TypeScript (*.ts)
- Java (*.java)
- C (*.c)
- C++ (*.cpp)
- Shell (*.sh)
- Go (*.go)
- Ruby (*.rb)
- PHP (*.php)

## Quick Start

### Install pip and venv
```bash
apt install python3-pip python3.12-venv
```

pip install google-genai

### Manual Setup
1. **Install Python dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   # Edit the .env file with your Gemini API key
   # Replace 'your_gemini_api_key_here' with your actual API key
   nano .env
   ```

3. **Make shell scripts executable:**
   ```bash
   chmod +x *.sh
   ```

### Usage
1. **Analyze your project:**
   ```bash
   ./project_info.sh              # Analyze current directory
   ./project_info.sh /path/to/dir # Analyze specific directory
   ```

2. **Generate PRD:**
   ```bash
   python generate_prd.py                    # Generate from project_info.txt
   python generate_prd.py -i custom.txt     # Custom input file
   python generate_prd.py -o my_prd.md      # Custom output file
   python generate_prd.py --no-cache        # Disable caching
   python generate_prd.py --debug           # Enable debug mode
   ```

## Output Files

**project_info.sh generates:**
- `project_info.txt` - Combined report with all information
- `project_structure.txt` - Directory tree structure
- `sensitive_info.txt` - Sensitive information scan results
- `line_counts.txt` - Code line counts and statistics

**generate_prd.py generates:**
- `prd_output.md` - Professional Product Requirements Document (default)
- Custom output file (when using `-o` option)
- `tmp/agno_workflows.db` - SQLite database for caching (auto-created)

## Dependencies

**Shell Scripts (project_info.sh):**
- `bash` (standard on most systems)
- `find`, `grep`, `wc`, `sed` (standard Unix tools)
- `tree` (optional, for better directory visualization)

**Python PRD Generator:**
- Python 3.8+
- `agno` - Agent framework
- `pydantic` - Data validation
- `sqlalchemy` - Database ORM
- `rich` - Terminal formatting
- `google-generativeai` - Gemini API client
- `python-dotenv` - Environment variable management

**Configuration:**
- `.env` file with Gemini API key
- Uses `gemini-2.0-flash-exp` model by default

**API Requirements:**
- Google API key (for Gemini models)

## Key Improvements from v03

✅ **Multi-Agent Architecture**: Replaced single API call with sophisticated 3-agent workflow  
✅ **Enhanced Tree Structure**: Added proper tree generation with fallback  
✅ **Better Statistics**: Added summary counts and file statistics  
✅ **Agno Framework Integration**: Professional agent framework with caching and workflows  
✅ **Structured Analysis**: Deep project analysis with structured data models  
✅ **Professional PRDs**: Comprehensive, industry-standard PRD generation  
✅ **Intelligent Caching**: Efficient caching system for faster subsequent runs  
✅ **Extensible Architecture**: Easy to extend with additional agents and capabilities  

## Agno Agent Workflow

The PRD generator uses a sophisticated multi-agent workflow:

### 1. ProjectAnalyst-X Agent
- **Purpose**: Analyzes codebase and extracts product insights
- **Input**: Raw project information (file structure, code, etc.)
- **Output**: Structured `ProjectAnalysis` with:
  - Project name and type identification
  - Core functionality extraction
  - Technical stack analysis
  - User persona identification
  - Complexity assessment

### 2. RequirementsEngineer-X Agent
- **Purpose**: Converts technical implementation into business requirements
- **Input**: Structured project analysis
- **Output**: Structured `PRDRequirements` with:
  - Functional and non-functional requirements
  - User stories in standard format
  - Acceptance criteria
  - Technical constraints
  - Success metrics and KPIs

### 3. PRDMaster-X Agent
- **Purpose**: Crafts comprehensive, professional PRD documents
- **Input**: Project analysis + structured requirements
- **Output**: Complete PRD in markdown format with:
  - Executive summary
  - Technical specifications
  - Implementation plan
  - Risk assessment
  - Success metrics

### Workflow Benefits
- **Separation of Concerns**: Each agent specializes in one aspect
- **Structured Data Flow**: Pydantic models ensure data consistency
- **Caching**: Each stage is cached for efficiency
- **Extensibility**: Easy to add new agents or modify existing ones
- **Quality**: Multi-stage analysis produces higher quality output

## Security Features

- Excludes common directories (`.git`, `node_modules`, `__pycache__`)
- Scans for sensitive patterns in code
- Safe file handling with proper cleanup
- Secure API key handling without logging
- Structured data validation with Pydantic models