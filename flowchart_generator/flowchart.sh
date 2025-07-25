#!/bin/bash

# Codebase Flowchart Generator
# Automatically analyzes any codebase and generates flowcharts using GraphViz and PlantUML

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
CODEBASE_PATH="."
OUTPUT_DIR="./flowcharts"
PROJECT_NAME=""
VERBOSE=false

# Print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Usage function
usage() {
    cat << EOF
Usage: $0 [OPTIONS] [CODEBASE_PATH]

Generate flowchart diagrams for any codebase using GraphViz and PlantUML.

OPTIONS:
    -h, --help          Show this help message
    -o, --output DIR    Output directory for generated diagrams (default: ./flowcharts)
    -n, --name NAME     Project name (default: auto-detected from directory)
    -v, --verbose       Enable verbose output
    --install-only      Only install dependencies, don't generate diagrams

EXAMPLES:
    $0                          # Analyze current directory
    $0 /path/to/project         # Analyze specific project
    $0 -o /tmp/diagrams .       # Custom output directory
    $0 -n MyProject -v .        # Custom name with verbose output

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                usage
                exit 0
                ;;
            -o|--output)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            -n|--name)
                PROJECT_NAME="$2"
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            --install-only)
                INSTALL_ONLY=true
                shift
                ;;
            -*)
                print_error "Unknown option: $1"
                usage
                exit 1
                ;;
            *)
                CODEBASE_PATH="$1"
                shift
                ;;
        esac
    done
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install required tools
install_dependencies() {
    print_info "Installing diagram generation tools..."
    
    # Detect package manager
    if command_exists apt-get; then
        print_info "Using apt package manager"
        sudo apt-get update -qq
        sudo apt-get install -y graphviz plantuml default-jre
    elif command_exists yum; then
        print_info "Using yum package manager"
        sudo yum install -y graphviz plantuml java
    elif command_exists dnf; then
        print_info "Using dnf package manager"
        sudo dnf install -y graphviz plantuml java
    elif command_exists pacman; then
        print_info "Using pacman package manager"
        sudo pacman -S --noconfirm graphviz plantuml jre-openjdk
    elif command_exists brew; then
        print_info "Using Homebrew package manager"
        brew install graphviz plantuml
    else
        print_error "No supported package manager found!"
        print_error "Please install graphviz and plantuml manually."
        exit 1
    fi
    
    # Verify installations
    if command_exists dot && command_exists plantuml; then
        print_success "All dependencies installed successfully!"
    else
        print_error "Failed to install some dependencies"
        exit 1
    fi
}

# Auto-detect project name
detect_project_name() {
    if [[ -z "$PROJECT_NAME" ]]; then
        if [[ -f "$CODEBASE_PATH/package.json" ]]; then
            PROJECT_NAME=$(grep -o '"name"[[:space:]]*:[[:space:]]*"[^"]*"' "$CODEBASE_PATH/package.json" | cut -d'"' -f4 2>/dev/null || echo "")
        fi
        
        if [[ -z "$PROJECT_NAME" ]] && [[ -f "$CODEBASE_PATH/Cargo.toml" ]]; then
            PROJECT_NAME=$(grep -o 'name[[:space:]]*=[[:space:]]*"[^"]*"' "$CODEBASE_PATH/Cargo.toml" | cut -d'"' -f2 2>/dev/null || echo "")
        fi
        
        if [[ -z "$PROJECT_NAME" ]] && [[ -f "$CODEBASE_PATH/pyproject.toml" ]]; then
            PROJECT_NAME=$(grep -o 'name[[:space:]]*=[[:space:]]*"[^"]*"' "$CODEBASE_PATH/pyproject.toml" | cut -d'"' -f2 2>/dev/null || echo "")
        fi
        
        if [[ -z "$PROJECT_NAME" ]]; then
            PROJECT_NAME=$(basename "$(realpath "$CODEBASE_PATH")")
        fi
    fi
    
    # Sanitize project name
    PROJECT_NAME=$(echo "$PROJECT_NAME" | sed 's/[^a-zA-Z0-9_-]/_/g')
    
    [[ $VERBOSE == true ]] && print_info "Project name: $PROJECT_NAME"
}

# Analyze codebase structure
analyze_codebase() {
    print_info "Analyzing codebase structure..."
    
    # Find main directories
    MAIN_DIRS=()
    while IFS= read -r -d '' dir; do
        dirname=$(basename "$dir")
        # Skip hidden, build, and dependency directories
        if [[ ! "$dirname" =~ ^(\.|build|dist|target|node_modules|vendor|__pycache__|\.git)$ ]]; then
            MAIN_DIRS+=("$dirname")
        fi
    done < <(find "$CODEBASE_PATH" -maxdepth 1 -type d -print0 2>/dev/null)
    
    # Detect project type and key files
    PROJECT_TYPE="unknown"
    MAIN_FILES=()
    CONFIG_FILES=()
    
    # Check for different project types
    if [[ -f "$CODEBASE_PATH/package.json" ]]; then
        PROJECT_TYPE="nodejs"
        [[ -f "$CODEBASE_PATH/src/index.js" ]] && MAIN_FILES+=("src/index.js")
        [[ -f "$CODEBASE_PATH/src/index.ts" ]] && MAIN_FILES+=("src/index.ts")
        [[ -f "$CODEBASE_PATH/src/app.js" ]] && MAIN_FILES+=("src/app.js")
        [[ -f "$CODEBASE_PATH/src/app.ts" ]] && MAIN_FILES+=("src/app.ts")
        CONFIG_FILES+=("package.json")
        [[ -f "$CODEBASE_PATH/tsconfig.json" ]] && CONFIG_FILES+=("tsconfig.json")
    fi
    
    if [[ -f "$CODEBASE_PATH/Cargo.toml" ]]; then
        PROJECT_TYPE="rust"
        [[ -f "$CODEBASE_PATH/src/main.rs" ]] && MAIN_FILES+=("src/main.rs")
        [[ -f "$CODEBASE_PATH/src/lib.rs" ]] && MAIN_FILES+=("src/lib.rs")
        CONFIG_FILES+=("Cargo.toml")
    fi
    
    if [[ -f "$CODEBASE_PATH/setup.py" ]] || [[ -f "$CODEBASE_PATH/pyproject.toml" ]]; then
        PROJECT_TYPE="python"
        [[ -f "$CODEBASE_PATH/__main__.py" ]] && MAIN_FILES+=("__main__.py")
        [[ -f "$CODEBASE_PATH/main.py" ]] && MAIN_FILES+=("main.py")
        [[ -f "$CODEBASE_PATH/app.py" ]] && MAIN_FILES+=("app.py")
        [[ -f "$CODEBASE_PATH/setup.py" ]] && CONFIG_FILES+=("setup.py")
        [[ -f "$CODEBASE_PATH/pyproject.toml" ]] && CONFIG_FILES+=("pyproject.toml")
    fi
    
    if [[ -f "$CODEBASE_PATH/go.mod" ]]; then
        PROJECT_TYPE="go"
        [[ -f "$CODEBASE_PATH/main.go" ]] && MAIN_FILES+=("main.go")
        CONFIG_FILES+=("go.mod")
    fi
    
    [[ $VERBOSE == true ]] && print_info "Project type: $PROJECT_TYPE"
    [[ $VERBOSE == true ]] && print_info "Main directories: ${MAIN_DIRS[*]}"
    [[ $VERBOSE == true ]] && print_info "Main files: ${MAIN_FILES[*]}"
}

# Generate GraphViz diagram
generate_graphviz() {
    print_info "Generating GraphViz diagram..."
    
    local output_file="$OUTPUT_DIR/${PROJECT_NAME}_graphviz"
    
    cat > "${output_file}.dot" << EOF
digraph ${PROJECT_NAME}Flow {
    rankdir=TB;
    node [shape=box, style=filled, fillcolor=lightblue];
    
    // Entry Points
    Entry [label="Entry Point\\n${MAIN_FILES[0]:-"main"}", fillcolor=lightgreen];
    
EOF

    # Add main directories as nodes
    local color_index=0
    local colors=("lightyellow" "lightcyan" "lightpink" "orange" "lightgray" "wheat" "lavender")
    
    for dir in "${MAIN_DIRS[@]}"; do
        local color=${colors[$((color_index % ${#colors[@]}))]}
        cat >> "${output_file}.dot" << EOF
    ${dir} [label="${dir}/", fillcolor=${color}];
EOF
        ((color_index++))
    done
    
    # Add configuration files
    for config in "${CONFIG_FILES[@]}"; do
        cat >> "${output_file}.dot" << EOF
    Config_$(basename "$config" | sed 's/[^a-zA-Z0-9]/_/g') [label="$config", fillcolor=lightsteelblue];
EOF
    done
    
    cat >> "${output_file}.dot" << EOF

    // Connections based on project structure
    Entry -> src;
EOF

    # Add connections based on common patterns
    for dir in "${MAIN_DIRS[@]}"; do
        case "$dir" in
            "src"|"lib")
                cat >> "${output_file}.dot" << EOF
    Entry -> ${dir};
EOF
                ;;
            "config"|"configs")
                cat >> "${output_file}.dot" << EOF
    ${dir} -> Entry;
EOF
                ;;
            "test"|"tests"|"spec")
                cat >> "${output_file}.dot" << EOF
    src -> ${dir};
EOF
                ;;
            "docs"|"doc")
                cat >> "${output_file}.dot" << EOF
    src -> ${dir};
EOF
                ;;
        esac
    done
    
    cat >> "${output_file}.dot" << EOF
}
EOF

    # Generate PNG
    dot -Tpng "${output_file}.dot" -o "${output_file}.png"
    
    if [[ -f "${output_file}.png" ]]; then
        print_success "GraphViz diagram generated: ${output_file}.png"
    else
        print_error "Failed to generate GraphViz diagram"
    fi
}

# Generate PlantUML diagram
generate_plantuml() {
    print_info "Generating PlantUML diagram..."
    
    local output_file="$OUTPUT_DIR/${PROJECT_NAME}_plantuml"
    
    cat > "${output_file}.puml" << EOF
@startuml
title $PROJECT_NAME Architecture Diagram

skinparam packageStyle rectangle
skinparam component {
    BackgroundColor<<entry>> LightBlue
    BackgroundColor<<core>> LightYellow
    BackgroundColor<<config>> LightGray
    BackgroundColor<<test>> Orange
    BackgroundColor<<doc>> Pink
}

EOF

    # Add entry point
    if [[ ${#MAIN_FILES[@]} -gt 0 ]]; then
        cat >> "${output_file}.puml" << EOF
component [${MAIN_FILES[0]}] as Entry <<entry>>

EOF
    fi

    # Add packages for main directories
    for dir in "${MAIN_DIRS[@]}"; do
        local stereotype="core"
        case "$dir" in
            "test"|"tests"|"spec") stereotype="test" ;;
            "docs"|"doc"|"documentation") stereotype="doc" ;;
            "config"|"configs"|"configuration") stereotype="config" ;;
        esac
        
        cat >> "${output_file}.puml" << EOF
package "$dir" {
    component [${dir} modules] as ${dir} <<${stereotype}>>
}

EOF
    done
    
    # Add configuration files
    if [[ ${#CONFIG_FILES[@]} -gt 0 ]]; then
        cat >> "${output_file}.puml" << EOF
package "Configuration" {
EOF
        for config in "${CONFIG_FILES[@]}"; do
            local safe_name=$(basename "$config" | sed 's/[^a-zA-Z0-9]/_/g')
            cat >> "${output_file}.puml" << EOF
    component [$config] as Config_${safe_name} <<config>>
EOF
        done
        cat >> "${output_file}.puml" << EOF
}

EOF
    fi
    
    # Add relationships
    cat >> "${output_file}.puml" << EOF
' Relationships
EOF
    
    # Connect entry to main directories
    for dir in "${MAIN_DIRS[@]}"; do
        case "$dir" in
            "src"|"lib"|"source")
                cat >> "${output_file}.puml" << EOF
Entry --> ${dir}
EOF
                ;;
        esac
    done
    
    # Connect directories based on common patterns
    for dir in "${MAIN_DIRS[@]}"; do
        case "$dir" in
            "test"|"tests"|"spec")
                cat >> "${output_file}.puml" << EOF
src --> ${dir}
EOF
                ;;
            "docs"|"doc")
                cat >> "${output_file}.puml" << EOF
src --> ${dir}
EOF
                ;;
        esac
    done
    
    cat >> "${output_file}.puml" << EOF

@enduml
EOF

    # Generate PNG
    plantuml -tpng "${output_file}.puml"
    
    if [[ -f "${output_file}.png" ]]; then
        print_success "PlantUML diagram generated: ${output_file}.png"
    else
        print_error "Failed to generate PlantUML diagram"
    fi
}

# Generate summary report
generate_summary() {
    local summary_file="$OUTPUT_DIR/${PROJECT_NAME}_analysis.md"
    
    cat > "$summary_file" << EOF
# $PROJECT_NAME - Codebase Analysis Report

**Generated on:** $(date)
**Project Type:** $PROJECT_TYPE
**Analysis Path:** $(realpath "$CODEBASE_PATH")

## Project Structure

### Main Directories
$(printf '- %s/\n' "${MAIN_DIRS[@]}")

### Entry Points
$(printf '- %s\n' "${MAIN_FILES[@]}")

### Configuration Files
$(printf '- %s\n' "${CONFIG_FILES[@]}")

## Generated Diagrams

1. **GraphViz Flowchart:** \`${PROJECT_NAME}_graphviz.png\`
2. **PlantUML Architecture:** \`${PROJECT_NAME}_plantuml.png\`

## Files Generated

- \`${PROJECT_NAME}_graphviz.dot\` - GraphViz source
- \`${PROJECT_NAME}_graphviz.png\` - GraphViz diagram
- \`${PROJECT_NAME}_plantuml.puml\` - PlantUML source  
- \`${PROJECT_NAME}_plantuml.png\` - PlantUML diagram
- \`${PROJECT_NAME}_analysis.md\` - This analysis report

EOF

    print_success "Analysis report generated: $summary_file"
}

# Main function
main() {
    print_info "Codebase Flowchart Generator"
    print_info "============================"
    
    # Parse arguments
    parse_args "$@"
    
    # Validate codebase path
    if [[ ! -d "$CODEBASE_PATH" ]]; then
        print_error "Codebase path does not exist: $CODEBASE_PATH"
        exit 1
    fi
    
    # Create output directory
    mkdir -p "$OUTPUT_DIR"
    
    # Check and install dependencies
    if ! command_exists dot || ! command_exists plantuml; then
        print_warning "Required tools not found. Installing dependencies..."
        install_dependencies
    else
        print_success "All required tools are already installed"
    fi
    
    # Exit if install-only mode
    if [[ "${INSTALL_ONLY:-false}" == true ]]; then
        print_success "Dependencies installed successfully!"
        exit 0
    fi
    
    # Analyze codebase
    detect_project_name
    analyze_codebase
    
    # Generate diagrams
    generate_graphviz
    generate_plantuml
    
    # Generate summary
    generate_summary
    
    print_success "All flowcharts generated successfully in: $OUTPUT_DIR"
    print_info "View the generated diagrams:"
    print_info "  - GraphViz: $OUTPUT_DIR/${PROJECT_NAME}_graphviz.png"
    print_info "  - PlantUML: $OUTPUT_DIR/${PROJECT_NAME}_plantuml.png"
    print_info "  - Report: $OUTPUT_DIR/${PROJECT_NAME}_analysis.md"
}

# Run main function
main "$@"