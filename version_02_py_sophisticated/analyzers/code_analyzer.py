"""
AST-based code analyzer for deep code understanding.
"""

import ast
import re
from typing import Dict, Any, List, Optional, Set, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from ..utils.file_utils import FileUtils


class ComplexityLevel(Enum):
    """Code complexity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class FunctionInfo:
    """Information about a function."""
    name: str
    line_start: int
    line_end: int
    args: List[str]
    returns: Optional[str]
    docstring: Optional[str]
    complexity: int
    calls: List[str]
    decorators: List[str]
    is_async: bool = False
    is_method: bool = False
    is_static: bool = False
    is_class_method: bool = False


@dataclass
class ClassInfo:
    """Information about a class."""
    name: str
    line_start: int
    line_end: int
    bases: List[str]
    methods: List[FunctionInfo]
    attributes: List[str]
    docstring: Optional[str]
    decorators: List[str]
    is_abstract: bool = False


@dataclass
class ImportInfo:
    """Information about imports."""
    module: str
    names: List[str]
    alias: Optional[str]
    line_number: int
    is_from_import: bool = False


class CodeAnalyzer:
    """AST-based code analyzer for Python files."""
    
    def __init__(self):
        """Initialize the code analyzer."""
        self.builtin_functions = {
            'print', 'len', 'range', 'str', 'int', 'float', 'bool', 'list', 'dict',
            'set', 'tuple', 'type', 'isinstance', 'hasattr', 'getattr', 'setattr',
            'open', 'input', 'sum', 'max', 'min', 'abs', 'round', 'sorted', 'reversed',
            'enumerate', 'zip', 'map', 'filter', 'any', 'all'
        }
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a Python file and extract detailed information."""
        if not FileUtils.file_exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        content = FileUtils.read_file(file_path)
        
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            return {
                'error': f"Syntax error in {file_path}: {e}",
                'valid': False
            }
        
        analysis = {
            'file_path': str(file_path),
            'valid': True,
            'imports': self._extract_imports(tree),
            'functions': self._extract_functions(tree, content),
            'classes': self._extract_classes(tree, content),
            'global_variables': self._extract_global_variables(tree),
            'constants': self._extract_constants(tree),
            'complexity_metrics': self._calculate_complexity_metrics(tree),
            'code_quality': self._assess_code_quality(tree, content),
            'dependencies': self._extract_dependencies(tree),
            'docstring_coverage': self._calculate_docstring_coverage(tree),
            'line_count': len(content.split('\n')),
            'code_lines': self._count_code_lines(content),
            'comment_lines': self._count_comment_lines(content),
            'blank_lines': self._count_blank_lines(content)
        }
        
        return analysis
    
    def _extract_imports(self, tree: ast.AST) -> List[ImportInfo]:
        """Extract import information from AST."""
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(ImportInfo(
                        module=alias.name,
                        names=[alias.name],
                        alias=alias.asname,
                        line_number=node.lineno,
                        is_from_import=False
                    ))
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                names = [alias.name for alias in node.names]
                imports.append(ImportInfo(
                    module=module,
                    names=names,
                    alias=None,
                    line_number=node.lineno,
                    is_from_import=True
                ))
        
        return imports
    
    def _extract_functions(self, tree: ast.AST, content: str) -> List[FunctionInfo]:
        """Extract function information from AST."""
        functions = []
        lines = content.split('\n')
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                # Get function arguments
                args = []
                if node.args.args:
                    args.extend([arg.arg for arg in node.args.args])
                if node.args.vararg:
                    args.append(f"*{node.args.vararg.arg}")
                if node.args.kwarg:
                    args.append(f"**{node.args.kwarg.arg}")
                
                # Get return type annotation
                returns = None
                if node.returns:
                    returns = ast.unparse(node.returns) if hasattr(ast, 'unparse') else str(node.returns)
                
                # Get docstring
                docstring = ast.get_docstring(node)
                
                # Calculate complexity
                complexity = self._calculate_function_complexity(node)
                
                # Get function calls
                calls = self._extract_function_calls(node)
                
                # Get decorators
                decorators = []
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Name):
                        decorators.append(decorator.id)
                    elif isinstance(decorator, ast.Attribute):
                        decorators.append(f"{decorator.value.id}.{decorator.attr}")
                
                # Determine function type
                is_async = isinstance(node, ast.AsyncFunctionDef)
                is_method = self._is_method(node, tree)
                is_static = 'staticmethod' in decorators
                is_class_method = 'classmethod' in decorators
                
                functions.append(FunctionInfo(
                    name=node.name,
                    line_start=node.lineno,
                    line_end=node.end_lineno or node.lineno,
                    args=args,
                    returns=returns,
                    docstring=docstring,
                    complexity=complexity,
                    calls=calls,
                    decorators=decorators,
                    is_async=is_async,
                    is_method=is_method,
                    is_static=is_static,
                    is_class_method=is_class_method
                ))
        
        return functions
    
    def _extract_classes(self, tree: ast.AST, content: str) -> List[ClassInfo]:
        """Extract class information from AST."""
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Get base classes
                bases = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        bases.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        bases.append(f"{base.value.id}.{base.attr}")
                
                # Get methods
                methods = []
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        # Extract method info (similar to function extraction)
                        method_info = self._extract_method_info(item)
                        methods.append(method_info)
                
                # Get class attributes
                attributes = self._extract_class_attributes(node)
                
                # Get docstring
                docstring = ast.get_docstring(node)
                
                # Get decorators
                decorators = []
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Name):
                        decorators.append(decorator.id)
                
                # Check if abstract
                is_abstract = any('abc' in base.lower() or 'abstract' in base.lower() for base in bases)
                
                classes.append(ClassInfo(
                    name=node.name,
                    line_start=node.lineno,
                    line_end=node.end_lineno or node.lineno,
                    bases=bases,
                    methods=methods,
                    attributes=attributes,
                    docstring=docstring,
                    decorators=decorators,
                    is_abstract=is_abstract
                ))
        
        return classes
    
    def _extract_global_variables(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract global variable assignments."""
        variables = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                var_name = node.targets[0].id
                var_type = self._infer_type(node.value)
                
                variables.append({
                    'name': var_name,
                    'type': var_type,
                    'line_number': node.lineno,
                    'is_constant': var_name.isupper()
                })
        
        return variables
    
    def _extract_constants(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract constants (uppercase variables)."""
        constants = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                var_name = node.targets[0].id
                if var_name.isupper():
                    var_type = self._infer_type(node.value)
                    constants.append({
                        'name': var_name,
                        'type': var_type,
                        'line_number': node.lineno
                    })
        
        return constants
    
    def _calculate_complexity_metrics(self, tree: ast.AST) -> Dict[str, Any]:
        """Calculate various complexity metrics."""
        metrics = {
            'cyclomatic_complexity': self._calculate_cyclomatic_complexity(tree),
            'cognitive_complexity': self._calculate_cognitive_complexity(tree),
            'nesting_depth': self._calculate_max_nesting_depth(tree),
            'function_count': len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
            'class_count': len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]),
            'complexity_level': None
        }
        
        # Determine overall complexity level
        cc = metrics['cyclomatic_complexity']
        if cc <= 10:
            metrics['complexity_level'] = ComplexityLevel.LOW.value
        elif cc <= 20:
            metrics['complexity_level'] = ComplexityLevel.MEDIUM.value
        elif cc <= 50:
            metrics['complexity_level'] = ComplexityLevel.HIGH.value
        else:
            metrics['complexity_level'] = ComplexityLevel.VERY_HIGH.value
        
        return metrics
    
    def _assess_code_quality(self, tree: ast.AST, content: str) -> Dict[str, Any]:
        """Assess code quality metrics."""
        quality = {
            'has_docstrings': self._has_docstrings(tree),
            'follows_naming_conventions': self._follows_naming_conventions(tree),
            'has_type_hints': self._has_type_hints(tree),
            'line_length_issues': self._check_line_lengths(content),
            'duplicate_code': self._detect_duplicate_code(content),
            'code_smells': self._detect_code_smells(tree),
            'maintainability_index': self._calculate_maintainability_index(tree, content)
        }
        
        return quality
    
    def _extract_dependencies(self, tree: ast.AST) -> Dict[str, List[str]]:
        """Extract code dependencies."""
        dependencies = {
            'internal_calls': [],
            'external_calls': [],
            'imported_modules': []
        }
        
        # Get imported modules
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    dependencies['imported_modules'].append(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                dependencies['imported_modules'].append(node.module)
        
        # Get function calls
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    if func_name in self.builtin_functions:
                        dependencies['external_calls'].append(func_name)
                    else:
                        dependencies['internal_calls'].append(func_name)
                elif isinstance(node.func, ast.Attribute):
                    attr_name = node.func.attr
                    dependencies['external_calls'].append(attr_name)
        
        return dependencies
    
    def _calculate_docstring_coverage(self, tree: ast.AST) -> Dict[str, Any]:
        """Calculate docstring coverage."""
        total_functions = 0
        documented_functions = 0
        total_classes = 0
        documented_classes = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                total_functions += 1
                if ast.get_docstring(node):
                    documented_functions += 1
            elif isinstance(node, ast.ClassDef):
                total_classes += 1
                if ast.get_docstring(node):
                    documented_classes += 1
        
        function_coverage = (documented_functions / total_functions * 100) if total_functions > 0 else 100
        class_coverage = (documented_classes / total_classes * 100) if total_classes > 0 else 100
        
        return {
            'function_coverage': round(function_coverage, 2),
            'class_coverage': round(class_coverage, 2),
            'overall_coverage': round((function_coverage + class_coverage) / 2, 2),
            'documented_functions': documented_functions,
            'total_functions': total_functions,
            'documented_classes': documented_classes,
            'total_classes': total_classes
        }
    
    def _count_code_lines(self, content: str) -> int:
        """Count lines of code (excluding comments and blank lines)."""
        lines = content.split('\n')
        code_lines = 0
        
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                code_lines += 1
        
        return code_lines
    
    def _count_comment_lines(self, content: str) -> int:
        """Count comment lines."""
        lines = content.split('\n')
        comment_lines = 0
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#'):
                comment_lines += 1
        
        return comment_lines
    
    def _count_blank_lines(self, content: str) -> int:
        """Count blank lines."""
        lines = content.split('\n')
        return sum(1 for line in lines if not line.strip())
    
    def _calculate_function_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity for a function."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.With, ast.AsyncWith):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _extract_function_calls(self, node: ast.FunctionDef) -> List[str]:
        """Extract function calls within a function."""
        calls = []
        
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    calls.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    calls.append(child.func.attr)
        
        return list(set(calls))  # Remove duplicates
    
    def _is_method(self, node: ast.FunctionDef, tree: ast.AST) -> bool:
        """Check if a function is a method (inside a class)."""
        for parent in ast.walk(tree):
            if isinstance(parent, ast.ClassDef):
                if node in parent.body:
                    return True
        return False
    
    def _extract_method_info(self, node: ast.FunctionDef) -> FunctionInfo:
        """Extract method information."""
        # Similar to function extraction but for methods
        args = [arg.arg for arg in node.args.args]
        returns = ast.unparse(node.returns) if node.returns and hasattr(ast, 'unparse') else None
        docstring = ast.get_docstring(node)
        complexity = self._calculate_function_complexity(node)
        calls = self._extract_function_calls(node)
        decorators = [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list]
        
        return FunctionInfo(
            name=node.name,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            args=args,
            returns=returns,
            docstring=docstring,
            complexity=complexity,
            calls=calls,
            decorators=decorators,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            is_method=True,
            is_static='staticmethod' in decorators,
            is_class_method='classmethod' in decorators
        )
    
    def _extract_class_attributes(self, node: ast.ClassDef) -> List[str]:
        """Extract class attributes."""
        attributes = []
        
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attributes.append(target.id)
        
        return attributes
    
    def _infer_type(self, node: ast.AST) -> str:
        """Infer the type of a value node."""
        if isinstance(node, ast.Constant):
            return type(node.value).__name__
        elif isinstance(node, ast.List):
            return 'list'
        elif isinstance(node, ast.Dict):
            return 'dict'
        elif isinstance(node, ast.Set):
            return 'set'
        elif isinstance(node, ast.Tuple):
            return 'tuple'
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                return node.func.id
        return 'unknown'
    
    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity for the entire file."""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.With, ast.AsyncWith):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _calculate_cognitive_complexity(self, tree: ast.AST) -> int:
        """Calculate cognitive complexity."""
        # Simplified cognitive complexity calculation
        complexity = 0
        nesting_level = 0
        
        def visit_node(node, level):
            nonlocal complexity
            
            if isinstance(node, (ast.If, ast.While, ast.For)):
                complexity += 1 + level
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1 + level
            
            # Increase nesting for certain constructs
            if isinstance(node, (ast.If, ast.While, ast.For, ast.With, ast.ExceptHandler)):
                level += 1
            
            for child in ast.iter_child_nodes(node):
                visit_node(child, level)
        
        visit_node(tree, 0)
        return complexity
    
    def _calculate_max_nesting_depth(self, tree: ast.AST) -> int:
        """Calculate maximum nesting depth."""
        max_depth = 0
        
        def visit_node(node, depth):
            nonlocal max_depth
            max_depth = max(max_depth, depth)
            
            if isinstance(node, (ast.If, ast.While, ast.For, ast.With, ast.FunctionDef, ast.ClassDef)):
                depth += 1
            
            for child in ast.iter_child_nodes(node):
                visit_node(child, depth)
        
        visit_node(tree, 0)
        return max_depth
    
    def _has_docstrings(self, tree: ast.AST) -> bool:
        """Check if the module has docstrings."""
        return ast.get_docstring(tree) is not None
    
    def _follows_naming_conventions(self, tree: ast.AST) -> Dict[str, bool]:
        """Check if code follows Python naming conventions."""
        conventions = {
            'functions_snake_case': True,
            'classes_pascal_case': True,
            'constants_upper_case': True,
            'variables_snake_case': True
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    conventions['functions_snake_case'] = False
            elif isinstance(node, ast.ClassDef):
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    conventions['classes_pascal_case'] = False
        
        return conventions
    
    def _has_type_hints(self, tree: ast.AST) -> Dict[str, Any]:
        """Check for type hints usage."""
        total_functions = 0
        typed_functions = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                total_functions += 1
                if node.returns or any(arg.annotation for arg in node.args.args):
                    typed_functions += 1
        
        coverage = (typed_functions / total_functions * 100) if total_functions > 0 else 0
        
        return {
            'has_type_hints': typed_functions > 0,
            'coverage_percentage': round(coverage, 2),
            'typed_functions': typed_functions,
            'total_functions': total_functions
        }
    
    def _check_line_lengths(self, content: str) -> List[Dict[str, Any]]:
        """Check for long lines."""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            if len(line) > 100:  # PEP 8 recommends 79, but being lenient
                issues.append({
                    'line_number': i,
                    'length': len(line),
                    'content': line[:50] + '...' if len(line) > 50 else line
                })
        
        return issues
    
    def _detect_duplicate_code(self, content: str) -> List[Dict[str, Any]]:
        """Detect potential duplicate code blocks."""
        # Simplified duplicate detection
        lines = content.split('\n')
        duplicates = []
        
        # Look for identical lines (excluding blank lines and comments)
        line_counts = {}
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and len(stripped) > 10:
                if stripped in line_counts:
                    line_counts[stripped].append(i)
                else:
                    line_counts[stripped] = [i]
        
        for line, occurrences in line_counts.items():
            if len(occurrences) > 1:
                duplicates.append({
                    'content': line[:50] + '...' if len(line) > 50 else line,
                    'occurrences': occurrences,
                    'count': len(occurrences)
                })
        
        return duplicates
    
    def _detect_code_smells(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Detect common code smells."""
        smells = []
        
        for node in ast.walk(tree):
            # Long parameter lists
            if isinstance(node, ast.FunctionDef) and len(node.args.args) > 5:
                smells.append({
                    'type': 'long_parameter_list',
                    'function': node.name,
                    'parameter_count': len(node.args.args),
                    'line_number': node.lineno
                })
            
            # Large classes (many methods)
            if isinstance(node, ast.ClassDef):
                method_count = sum(1 for item in node.body if isinstance(item, ast.FunctionDef))
                if method_count > 20:
                    smells.append({
                        'type': 'large_class',
                        'class': node.name,
                        'method_count': method_count,
                        'line_number': node.lineno
                    })
        
        return smells
    
    def _calculate_maintainability_index(self, tree: ast.AST, content: str) -> float:
        """Calculate maintainability index (simplified)."""
        # Simplified MI calculation
        lines_of_code = self._count_code_lines(content)
        cyclomatic_complexity = self._calculate_cyclomatic_complexity(tree)
        
        if lines_of_code == 0:
            return 100.0
        
        # Simplified formula
        mi = max(0, (171 - 5.2 * (cyclomatic_complexity / lines_of_code) * 100 - 0.23 * cyclomatic_complexity - 16.2 * (lines_of_code / 1000)) * 100 / 171)
        
        return round(mi, 2)