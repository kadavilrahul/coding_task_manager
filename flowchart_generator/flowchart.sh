#!/bin/bash

# Simple Flowchart Generator for any codebase
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Install tools if missing
install_tools() {
    if ! command -v dot >/dev/null || ! command -v plantuml >/dev/null || ! command -v graph-easy >/dev/null; then
        info "Installing diagram tools..."
        sudo apt update -qq && sudo apt install -y graphviz plantuml default-jre libgraph-easy-perl boxes
    fi
}

# Select directory
select_dir() {
    echo "1) Current directory ($(pwd))"
    echo "2) Enter path"
    read -p "Choice (1-2): " choice
    case $choice in
        1) DIR="." ;;
        2) read -p "Path: " DIR ;;
        *) error "Invalid choice" ;;
    esac
    [[ -d "$DIR" ]] || error "Directory not found: $DIR"
}

# Get project name
get_name() {
    if [[ -f "$DIR/package.json" ]]; then
        NAME=$(grep -o '"name"[[:space:]]*:[[:space:]]*"[^"]*"' "$DIR/package.json" | cut -d'"' -f4 2>/dev/null || echo "project")
    else
        NAME=$(basename "$(realpath "$DIR")")
    fi
    NAME=$(echo "$NAME" | sed 's/[^a-zA-Z0-9_-]/_/g')
}

# Find directories (skip hidden, build, deps)
find_dirs() {
    DIRS=($(find "$DIR" -maxdepth 1 -type d -not -path '*/.*' -not -name 'node_modules' -not -name 'build' -not -name 'dist' -not -name 'target' | xargs -n1 basename | grep -v "^$(basename "$DIR")$" | sort))
}

# Generate GraphViz with component relationships
gen_graphviz() {
    cat > "$DIR/flowchart_${NAME}.dot" << EOF
digraph ${NAME} {
    rankdir=TB;
    node [shape=box, style=filled];
    
    // Entry Points
    Install [label="Install Script\\n(curl)", fillcolor=lightgreen];
    CLI [label="CLI Entry\\n(index.ts)", fillcolor=lightgreen];
    
    // Core Components
    TUI [label="TUI Frontend\\n(Go/Bubble Tea)", fillcolor=lightyellow];
    Server [label="Server/API\\n(TypeScript)", fillcolor=lightyellow];
    App [label="Core App Logic", fillcolor=lightyellow];
    
    // AI Components
    Agent [label="AI Agent", fillcolor=lightpink];
    Provider [label="AI Providers", fillcolor=lightpink];
    Tools [label="Tools System", fillcolor=lightpink];
    
    // Integration
    IDE [label="IDE Integration", fillcolor=orange];
    LSP [label="Language Server", fillcolor=orange];
    MCP [label="MCP Servers", fillcolor=orange];
    
    // External
    SDK [label="SDK/API Client", fillcolor=wheat];
    VSCode [label="VS Code Extension", fillcolor=wheat];
    GitHub [label="GitHub Action", fillcolor=wheat];
    
    // Infrastructure
    Config [label="Configuration", fillcolor=lightcyan];
    Auth [label="Authentication", fillcolor=lightcyan];
    Session [label="Session Management", fillcolor=lightgray];
    Storage [label="Storage", fillcolor=lightgray];
    File [label="File Operations", fillcolor=lightgray];
    
    // Web
    Web [label="Web Interface", fillcolor=lavender];
    Share [label="Share Feature", fillcolor=lavender];
    
    // Connections
    Install -> CLI;
    CLI -> TUI;
    CLI -> Server;
    Server -> App;
    App -> Config;
    App -> Auth;
    App -> Session;
    Session -> Agent;
    Agent -> Provider;
    Agent -> Tools;
    Tools -> File;
    Tools -> IDE;
    IDE -> LSP;
    Session -> Storage;
    App -> MCP;
    Server -> SDK;
    VSCode -> SDK;
    GitHub -> SDK;
    App -> Share;
    Share -> Web;
}
EOF
    timeout 10 dot -Tpng "$DIR/flowchart_${NAME}.dot" -o "$DIR/flowchart_${NAME}_graphviz.png" 2>/dev/null
}

# Generate PlantUML with detailed architecture
gen_plantuml() {
    cat > "$DIR/flowchart_${NAME}.puml" << EOF
@startuml
title $NAME Architecture Diagram

skinparam component {
    BackgroundColor<<entry>> LightGreen
    BackgroundColor<<core>> LightYellow
    BackgroundColor<<ai>> LightPink
    BackgroundColor<<integration>> Orange
    BackgroundColor<<web>> Lavender
    BackgroundColor<<infra>> LightGray
}

package "Entry Points" {
    component [Install Script] as Install <<entry>>
    component [CLI Entry] as CLI <<entry>>
}

package "Core Components" {
    component [TUI Frontend] as TUI <<core>>
    component [Server/API] as Server <<core>>
    component [Core App Logic] as App <<core>>
}

package "AI & Intelligence" {
    component [AI Agent] as Agent <<ai>>
    component [AI Providers] as Provider <<ai>>
    component [Tools System] as Tools <<ai>>
}

package "Development Integration" {
    component [IDE Integration] as IDE <<integration>>
    component [Language Server] as LSP <<integration>>
    component [MCP Servers] as MCP <<integration>>
}

package "External Interfaces" {
    component [SDK/API Client] as SDK <<integration>>
    component [VS Code Extension] as VSCode <<integration>>
    component [GitHub Action] as GitHub <<integration>>
}

package "Infrastructure" {
    component [Configuration] as Config <<infra>>
    component [Authentication] as Auth <<infra>>
    component [Session Management] as Session <<infra>>
    component [Storage] as Storage <<infra>>
    component [File Operations] as File <<infra>>
}

package "Web Interface" {
    component [Web Interface] as Web <<web>>
    component [Share Feature] as Share <<web>>
}

' Relationships
Install --> CLI
CLI --> TUI
CLI --> Server
Server --> App
App --> Config
App --> Auth
App --> Session
Session --> Agent
Agent --> Provider
Agent --> Tools
Tools --> File
Tools --> IDE
IDE --> LSP
Session --> Storage
App --> MCP
Server --> SDK
VSCode --> SDK
GitHub --> SDK
App --> Share
Share --> Web

@enduml
EOF
    timeout 10 plantuml -tpng "$DIR/flowchart_${NAME}.puml" 2>/dev/null
}

# Generate ASCII flowchart
gen_ascii() {
    cat > "$DIR/flowchart_${NAME}.txt" << 'EOF'
[Install] -> [CLI] -> [TUI]
[CLI] -> [Server] -> [App]
[App] -> [Config]
[App] -> [Auth] 
[App] -> [Session]
[Session] -> [Agent] -> [Provider]
[Agent] -> [Tools] -> [IDE] -> [LSP]
[Tools] -> [File]
[Session] -> [Storage]
[App] -> [MCP]
[Server] -> [SDK]
[VSCode] -> [SDK]
[GitHub] -> [SDK] 
[App] -> [Share] -> [Web]
EOF
    
    # Generate ASCII diagram
    graph-easy --input="$DIR/flowchart_${NAME}.txt" --as=ascii > "$DIR/flowchart_${NAME}_ascii.txt" 2>/dev/null
    
    # Add title
    sed -i '1i\\n'"$NAME"' Architecture (ASCII)\n========================\n' "$DIR/flowchart_${NAME}_ascii.txt"
}

# Main
main() {
    info "Simple Flowchart Generator"
    
    # Parse args or interactive
    if [[ $# -eq 0 ]]; then
        select_dir
    else
        DIR="$1"
        [[ -d "$DIR" ]] || error "Directory not found: $DIR"
    fi
    
    install_tools
    get_name
    find_dirs
    
    info "Generating diagrams for: $NAME"
    gen_graphviz && success "GraphViz: $DIR/flowchart_${NAME}_graphviz.png"
    gen_plantuml && success "PlantUML: $DIR/flowchart_${NAME}.png"
    gen_ascii && success "ASCII: $DIR/flowchart_${NAME}_ascii.txt"
}

main "$@"