"""
Dependency mapper for analyzing code relationships and dependencies.
"""

import ast
import re
from typing import Dict, Any, List, Optional, Set, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import json

from ..utils.file_utils import FileUtils


class DependencyType(Enum):
    """Types of dependencies."""
    IMPORT = "import"
    FUNCTION_CALL = "function_call"
    CLASS_INHERITANCE = "class_inheritance"
    VARIABLE_REFERENCE = "variable_reference"
    MODULE_REFERENCE = "module_reference"


class DependencyScope(Enum):
    """Scope of dependencies."""
    INTERNAL = "internal"  # Within the same project
    EXTERNAL = "external"  # External libraries
    BUILTIN = "builtin"   # Python built-ins


@dataclass
class Dependency:
    """Represents a dependency relationship."""
    source: str
    target: str
    dependency_type: DependencyType
    scope: DependencyScope
    line_number: int
    context: Optional[str] = None


@dataclass
class ModuleInfo:
    """Information about a module."""
    path: Path
    name: str
    imports: List[str]
    exports: List[str]
    functions: List[str]
    classes: List[str]
    dependencies: List[Dependency]


class DependencyMapper:
    """Analyze and map code dependencies."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize the dependency mapper."""
        self.project_root = project_root or Path.cwd()
        self.modules = {}
        self.dependency_graph = {}
        self.builtin_modules = {
            'os', 'sys', 'json', 'datetime', 'pathlib', 'typing', 're', 'collections',
            'itertools', 'functools', 'operator', 'math', 'random', 'string', 'time',
            'urllib', 'http', 'email', 'html', 'xml', 'csv', 'sqlite3', 'logging',
            'unittest', 'argparse', 'configparser', 'io', 'tempfile', 'shutil',
            'glob', 'fnmatch', 'pickle', 'copy', 'pprint', 'textwrap', 'unicodedata',
            'codecs', 'base64', 'binascii', 'struct', 'array', 'weakref', 'gc',
            'inspect', 'dis', 'ast', 'keyword', 'token', 'tokenize', 'traceback'
        }
    
    def analyze_project(self, project_path: Optional[Path] = None) -> Dict[str, Any]:
        """Analyze dependencies for an entire project."""
        if project_path:
            self.project_root = project_path
        
        # Find all Python files
        python_files = FileUtils.list_files(self.project_root, "**/*.py", recursive=True)
        
        # Analyze each file
        for file_path in python_files:
            try:
                self.analyze_file(file_path)
            except Exception as e:
                print(f"Warning: Could not analyze {file_path}: {e}")
                continue
        
        # Build dependency graph
        self._build_dependency_graph()
        
        # Generate analysis report
        return self._generate_analysis_report()
    
    def analyze_file(self, file_path: Path) -> ModuleInfo:
        """Analyze dependencies for a single file."""
        if not FileUtils.file_exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        content = FileUtils.read_file(file_path)
        
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            raise SyntaxError(f"Syntax error in {file_path}: {e}")
        
        # Extract module information
        module_name = self._get_module_name(file_path)
        
        module_info = ModuleInfo(
            path=file_path,
            name=module_name,
            imports=self._extract_imports(tree),
            exports=self._extract_exports(tree),
            functions=self._extract_function_names(tree),
            classes=self._extract_class_names(tree),
            dependencies=self._extract_dependencies(tree, file_path)
        )
        
        self.modules[str(file_path)] = module_info
        return module_info
    
    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract all import statements."""
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
                    # Also add specific imports
                    for alias in node.names:
                        if alias.name != '*':
                            imports.append(f"{node.module}.{alias.name}")
        
        return list(set(imports))  # Remove duplicates
    
    def _extract_exports(self, tree: ast.AST) -> List[str]:
        """Extract exported names (functions, classes, variables)."""
        exports = []
        
        # Look for __all__ definition
        for node in ast.walk(tree):
            if (isinstance(node, ast.Assign) and 
                len(node.targets) == 1 and 
                isinstance(node.targets[0], ast.Name) and 
                node.targets[0].id == '__all__'):
                
                if isinstance(node.value, ast.List):
                    for elt in node.value.elts:
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                            exports.append(elt.value)
                return exports
        
        # If no __all__, extract top-level definitions
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                if not node.name.startswith('_'):  # Public functions
                    exports.append(node.name)
            elif isinstance(node, ast.ClassDef):
                if not node.name.startswith('_'):  # Public classes
                    exports.append(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and not target.id.startswith('_'):
                        exports.append(target.id)
        
        return exports
    
    def _extract_function_names(self, tree: ast.AST) -> List[str]:
        """Extract all function names."""
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(node.name)
        
        return functions
    
    def _extract_class_names(self, tree: ast.AST) -> List[str]:
        """Extract all class names."""
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
        
        return classes
    
    def _extract_dependencies(self, tree: ast.AST, file_path: Path) -> List[Dependency]:
        """Extract all dependencies from the AST."""
        dependencies = []
        source_module = self._get_module_name(file_path)
        
        # Import dependencies
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    scope = self._determine_scope(alias.name)
                    dependencies.append(Dependency(
                        source=source_module,
                        target=alias.name,
                        dependency_type=DependencyType.IMPORT,
                        scope=scope,
                        line_number=node.lineno,
                        context="import"
                    ))
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    scope = self._determine_scope(node.module)
                    dependencies.append(Dependency(
                        source=source_module,
                        target=node.module,
                        dependency_type=DependencyType.IMPORT,
                        scope=scope,
                        line_number=node.lineno,
                        context="from_import"
                    ))
            
            # Function call dependencies
            elif isinstance(node, ast.Call):
                target = self._get_call_target(node)
                if target:
                    scope = self._determine_scope(target)
                    dependencies.append(Dependency(
                        source=source_module,
                        target=target,
                        dependency_type=DependencyType.FUNCTION_CALL,
                        scope=scope,
                        line_number=node.lineno,
                        context="function_call"
                    ))
            
            # Class inheritance dependencies
            elif isinstance(node, ast.ClassDef):
                for base in node.bases:
                    target = self._get_name_from_node(base)
                    if target:
                        scope = self._determine_scope(target)
                        dependencies.append(Dependency(
                            source=source_module,
                            target=target,
                            dependency_type=DependencyType.CLASS_INHERITANCE,
                            scope=scope,
                            line_number=node.lineno,
                            context=f"class {node.name}"
                        ))
        
        return dependencies
    
    def _get_module_name(self, file_path: Path) -> str:
        """Get module name from file path."""
        try:
            relative_path = file_path.relative_to(self.project_root)
            module_parts = list(relative_path.parts[:-1])  # Exclude filename
            if relative_path.stem != '__init__':
                module_parts.append(relative_path.stem)
            return '.'.join(module_parts) if module_parts else relative_path.stem
        except ValueError:
            # File is outside project root
            return file_path.stem
    
    def _determine_scope(self, target: str) -> DependencyScope:
        """Determine if a dependency is internal, external, or builtin."""
        # Check if it's a builtin module
        root_module = target.split('.')[0]
        if root_module in self.builtin_modules:
            return DependencyScope.BUILTIN
        
        # Check if it's an internal module
        for module_path in self.modules.keys():
            module_info = self.modules[module_path]
            if target.startswith(module_info.name):
                return DependencyScope.INTERNAL
        
        # Check if it's a relative import or project module
        if target.startswith('.') or any(target.startswith(name) for name in self._get_project_modules()):
            return DependencyScope.INTERNAL
        
        return DependencyScope.EXTERNAL
    
    def _get_project_modules(self) -> List[str]:
        """Get list of project module names."""
        return [info.name for info in self.modules.values()]
    
    def _get_call_target(self, node: ast.Call) -> Optional[str]:
        """Extract the target of a function call."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None
    
    def _get_name_from_node(self, node: ast.AST) -> Optional[str]:
        """Extract name from an AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name_from_node(node.value)}.{node.attr}"
        return None
    
    def _build_dependency_graph(self):
        """Build a dependency graph from analyzed modules."""
        self.dependency_graph = {}
        
        for module_path, module_info in self.modules.items():
            module_name = module_info.name
            self.dependency_graph[module_name] = {
                'dependencies': [],
                'dependents': [],
                'internal_deps': [],
                'external_deps': [],
                'builtin_deps': []
            }
            
            for dep in module_info.dependencies:
                self.dependency_graph[module_name]['dependencies'].append(dep.target)
                
                if dep.scope == DependencyScope.INTERNAL:
                    self.dependency_graph[module_name]['internal_deps'].append(dep.target)
                elif dep.scope == DependencyScope.EXTERNAL:
                    self.dependency_graph[module_name]['external_deps'].append(dep.target)
                elif dep.scope == DependencyScope.BUILTIN:
                    self.dependency_graph[module_name]['builtin_deps'].append(dep.target)
        
        # Build reverse dependencies (dependents)
        for module_name, graph_info in self.dependency_graph.items():
            for dep in graph_info['dependencies']:
                if dep in self.dependency_graph:
                    self.dependency_graph[dep]['dependents'].append(module_name)
    
    def _generate_analysis_report(self) -> Dict[str, Any]:
        """Generate a comprehensive dependency analysis report."""
        total_modules = len(self.modules)
        
        if total_modules == 0:
            return {'error': 'No modules analyzed'}
        
        # Collect statistics
        all_dependencies = []
        for module_info in self.modules.values():
            all_dependencies.extend(module_info.dependencies)
        
        internal_deps = [d for d in all_dependencies if d.scope == DependencyScope.INTERNAL]
        external_deps = [d for d in all_dependencies if d.scope == DependencyScope.EXTERNAL]
        builtin_deps = [d for d in all_dependencies if d.scope == DependencyScope.BUILTIN]
        
        # Find circular dependencies
        circular_deps = self._find_circular_dependencies()
        
        # Find orphaned modules
        orphaned_modules = self._find_orphaned_modules()
        
        # Calculate coupling metrics
        coupling_metrics = self._calculate_coupling_metrics()
        
        # Get most used dependencies
        most_used = self._get_most_used_dependencies()
        
        return {
            'summary': {
                'total_modules': total_modules,
                'total_dependencies': len(all_dependencies),
                'internal_dependencies': len(internal_deps),
                'external_dependencies': len(external_deps),
                'builtin_dependencies': len(builtin_deps)
            },
            'modules': {name: {
                'path': str(info.path),
                'functions': len(info.functions),
                'classes': len(info.classes),
                'imports': len(info.imports),
                'exports': len(info.exports),
                'dependencies': len(info.dependencies)
            } for name, info in self.modules.items()},
            'dependency_graph': self.dependency_graph,
            'circular_dependencies': circular_deps,
            'orphaned_modules': orphaned_modules,
            'coupling_metrics': coupling_metrics,
            'most_used_dependencies': most_used,
            'external_libraries': list(set(d.target for d in external_deps)),
            'builtin_modules_used': list(set(d.target for d in builtin_deps))
        }
    
    def _find_circular_dependencies(self) -> List[List[str]]:
        """Find circular dependencies in the dependency graph."""
        circular_deps = []
        visited = set()
        rec_stack = set()
        
        def dfs(node, path):
            if node in rec_stack:
                # Found a cycle
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                circular_deps.append(cycle)
                return
            
            if node in visited or node not in self.dependency_graph:
                return
            
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for dep in self.dependency_graph[node]['internal_deps']:
                dfs(dep, path.copy())
            
            rec_stack.remove(node)
        
        for module in self.dependency_graph:
            if module not in visited:
                dfs(module, [])
        
        return circular_deps
    
    def _find_orphaned_modules(self) -> List[str]:
        """Find modules that are not imported by any other module."""
        orphaned = []
        
        for module_name in self.dependency_graph:
            if not self.dependency_graph[module_name]['dependents']:
                orphaned.append(module_name)
        
        return orphaned
    
    def _calculate_coupling_metrics(self) -> Dict[str, Any]:
        """Calculate coupling metrics for the project."""
        if not self.dependency_graph:
            return {}
        
        # Afferent coupling (Ca) - number of modules that depend on this module
        # Efferent coupling (Ce) - number of modules this module depends on
        
        coupling_data = {}
        total_ca = 0
        total_ce = 0
        
        for module_name, graph_info in self.dependency_graph.items():
            ca = len(graph_info['dependents'])  # Afferent coupling
            ce = len(graph_info['internal_deps'])  # Efferent coupling
            
            # Instability (I) = Ce / (Ca + Ce)
            instability = ce / (ca + ce) if (ca + ce) > 0 else 0
            
            coupling_data[module_name] = {
                'afferent_coupling': ca,
                'efferent_coupling': ce,
                'instability': round(instability, 3)
            }
            
            total_ca += ca
            total_ce += ce
        
        # Calculate average metrics
        num_modules = len(self.dependency_graph)
        avg_ca = total_ca / num_modules if num_modules > 0 else 0
        avg_ce = total_ce / num_modules if num_modules > 0 else 0
        avg_instability = sum(data['instability'] for data in coupling_data.values()) / num_modules if num_modules > 0 else 0
        
        return {
            'module_coupling': coupling_data,
            'averages': {
                'afferent_coupling': round(avg_ca, 2),
                'efferent_coupling': round(avg_ce, 2),
                'instability': round(avg_instability, 3)
            }
        }
    
    def _get_most_used_dependencies(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the most frequently used dependencies."""
        dependency_counts = {}
        
        for module_info in self.modules.values():
            for dep in module_info.dependencies:
                if dep.target not in dependency_counts:
                    dependency_counts[dep.target] = {
                        'count': 0,
                        'scope': dep.scope.value,
                        'type': dep.dependency_type.value
                    }
                dependency_counts[dep.target]['count'] += 1
        
        # Sort by count and return top N
        sorted_deps = sorted(dependency_counts.items(), key=lambda x: x[1]['count'], reverse=True)
        
        return [
            {
                'name': name,
                'count': info['count'],
                'scope': info['scope'],
                'type': info['type']
            }
            for name, info in sorted_deps[:limit]
        ]
    
    def generate_dependency_report(self, output_format: str = 'json') -> str:
        """Generate a dependency report in the specified format."""
        analysis = self._generate_analysis_report()
        
        if output_format.lower() == 'json':
            return json.dumps(analysis, indent=2, default=str)
        elif output_format.lower() == 'markdown':
            return self._generate_markdown_report(analysis)
        elif output_format.lower() == 'text':
            return self._generate_text_report(analysis)
        else:
            raise ValueError(f"Unsupported format: {output_format}")
    
    def _generate_markdown_report(self, analysis: Dict[str, Any]) -> str:
        """Generate a Markdown dependency report."""
        lines = ["# Dependency Analysis Report\n"]
        
        # Summary
        summary = analysis['summary']
        lines.extend([
            "## Summary\n",
            f"- **Total Modules:** {summary['total_modules']}",
            f"- **Total Dependencies:** {summary['total_dependencies']}",
            f"- **Internal Dependencies:** {summary['internal_dependencies']}",
            f"- **External Dependencies:** {summary['external_dependencies']}",
            f"- **Builtin Dependencies:** {summary['builtin_dependencies']}\n"
        ])
        
        # Circular dependencies
        if analysis['circular_dependencies']:
            lines.append("## Circular Dependencies\n")
            for i, cycle in enumerate(analysis['circular_dependencies'], 1):
                cycle_str = " → ".join(cycle)
                lines.append(f"{i}. {cycle_str}")
            lines.append("")
        
        # Most used dependencies
        lines.append("## Most Used Dependencies\n")
        for dep in analysis['most_used_dependencies']:
            lines.append(f"- **{dep['name']}** ({dep['scope']}) - used {dep['count']} times")
        lines.append("")
        
        # External libraries
        if analysis['external_libraries']:
            lines.append("## External Libraries\n")
            for lib in sorted(analysis['external_libraries']):
                lines.append(f"- {lib}")
            lines.append("")
        
        return '\n'.join(lines)
    
    def _generate_text_report(self, analysis: Dict[str, Any]) -> str:
        """Generate a plain text dependency report."""
        lines = ["DEPENDENCY ANALYSIS REPORT", "=" * 30, ""]
        
        # Summary
        summary = analysis['summary']
        lines.extend([
            "SUMMARY:",
            f"Total Modules: {summary['total_modules']}",
            f"Total Dependencies: {summary['total_dependencies']}",
            f"Internal Dependencies: {summary['internal_dependencies']}",
            f"External Dependencies: {summary['external_dependencies']}",
            f"Builtin Dependencies: {summary['builtin_dependencies']}",
            ""
        ])
        
        # Circular dependencies
        if analysis['circular_dependencies']:
            lines.extend(["CIRCULAR DEPENDENCIES:", "-" * 20])
            for i, cycle in enumerate(analysis['circular_dependencies'], 1):
                cycle_str = " -> ".join(cycle)
                lines.append(f"{i}. {cycle_str}")
            lines.append("")
        
        # Most used dependencies
        lines.extend(["MOST USED DEPENDENCIES:", "-" * 22])
        for dep in analysis['most_used_dependencies']:
            lines.append(f"{dep['name']} ({dep['scope']}) - {dep['count']} times")
        lines.append("")
        
        return '\n'.join(lines)
    
    def visualize_dependencies(self, output_file: Optional[Path] = None) -> str:
        """Generate a DOT file for dependency visualization."""
        if not self.dependency_graph:
            return ""
        
        dot_lines = [
            "digraph dependencies {",
            "    rankdir=LR;",
            "    node [shape=box];",
            ""
        ]
        
        # Add nodes
        for module_name in self.dependency_graph:
            safe_name = module_name.replace('.', '_').replace('-', '_')
            dot_lines.append(f'    {safe_name} [label="{module_name}"];')
        
        dot_lines.append("")
        
        # Add edges
        for module_name, graph_info in self.dependency_graph.items():
            safe_source = module_name.replace('.', '_').replace('-', '_')
            for dep in graph_info['internal_deps']:
                safe_target = dep.replace('.', '_').replace('-', '_')
                if dep in self.dependency_graph:
                    dot_lines.append(f'    {safe_source} -> {safe_target};')
        
        dot_lines.append("}")
        
        dot_content = '\n'.join(dot_lines)
        
        if output_file:
            FileUtils.write_file(output_file, dot_content)
        
        return dot_content