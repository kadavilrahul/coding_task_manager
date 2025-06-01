"""
Function documentation extractor for automatic API documentation generation.
"""

import ast
import re
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

from ..utils.file_utils import FileUtils


class ParameterType(Enum):
    """Parameter types."""
    POSITIONAL = "positional"
    KEYWORD = "keyword"
    VAR_POSITIONAL = "var_positional"  # *args
    VAR_KEYWORD = "var_keyword"  # **kwargs


@dataclass
class Parameter:
    """Function parameter information."""
    name: str
    type_hint: Optional[str]
    default_value: Optional[str]
    parameter_type: ParameterType
    description: Optional[str] = None


@dataclass
class FunctionSignature:
    """Complete function signature information."""
    name: str
    parameters: List[Parameter]
    return_type: Optional[str]
    is_async: bool
    is_generator: bool
    decorators: List[str]


@dataclass
class FunctionDocumentation:
    """Complete function documentation."""
    signature: FunctionSignature
    docstring: Optional[str]
    description: Optional[str]
    parameters_doc: Dict[str, str]
    returns_doc: Optional[str]
    raises_doc: List[str]
    examples: List[str]
    notes: List[str]
    line_start: int
    line_end: int
    source_code: str
    complexity: int
    calls_made: List[str]
    called_by: List[str]


class FunctionExtractor:
    """Extract and document functions from Python code."""
    
    def __init__(self):
        """Initialize the function extractor."""
        self.extracted_functions = {}
        self.call_graph = {}
    
    def extract_from_file(self, file_path: Path) -> Dict[str, FunctionDocumentation]:
        """Extract all functions from a Python file."""
        if not FileUtils.file_exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        content = FileUtils.read_file(file_path)
        
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            raise SyntaxError(f"Syntax error in {file_path}: {e}")
        
        lines = content.split('\n')
        functions = {}
        
        # Extract all function definitions
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_doc = self._extract_function_documentation(node, lines, tree)
                functions[func_doc.signature.name] = func_doc
        
        # Build call graph
        self._build_call_graph(functions)
        
        self.extracted_functions[str(file_path)] = functions
        return functions
    
    def extract_from_directory(self, directory_path: Path, 
                             recursive: bool = True) -> Dict[str, Dict[str, FunctionDocumentation]]:
        """Extract functions from all Python files in a directory."""
        if not FileUtils.directory_exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        pattern = "**/*.py" if recursive else "*.py"
        python_files = FileUtils.list_files(directory_path, pattern, recursive)
        
        all_functions = {}
        
        for file_path in python_files:
            try:
                functions = self.extract_from_file(file_path)
                all_functions[str(file_path)] = functions
            except (SyntaxError, FileNotFoundError) as e:
                print(f"Warning: Could not process {file_path}: {e}")
                continue
        
        return all_functions
    
    def _extract_function_documentation(self, node: ast.FunctionDef, 
                                      lines: List[str], tree: ast.AST) -> FunctionDocumentation:
        """Extract complete documentation for a function."""
        # Extract signature
        signature = self._extract_signature(node)
        
        # Extract docstring and parse it
        docstring = ast.get_docstring(node)
        parsed_docstring = self._parse_docstring(docstring) if docstring else {}
        
        # Extract source code
        start_line = node.lineno - 1
        end_line = (node.end_lineno or node.lineno) - 1
        source_code = '\n'.join(lines[start_line:end_line + 1])
        
        # Calculate complexity
        complexity = self._calculate_function_complexity(node)
        
        # Extract function calls
        calls_made = self._extract_function_calls(node)
        
        return FunctionDocumentation(
            signature=signature,
            docstring=docstring,
            description=parsed_docstring.get('description'),
            parameters_doc=parsed_docstring.get('parameters', {}),
            returns_doc=parsed_docstring.get('returns'),
            raises_doc=parsed_docstring.get('raises', []),
            examples=parsed_docstring.get('examples', []),
            notes=parsed_docstring.get('notes', []),
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            source_code=source_code,
            complexity=complexity,
            calls_made=calls_made,
            called_by=[]  # Will be populated by call graph analysis
        )
    
    def _extract_signature(self, node: ast.FunctionDef) -> FunctionSignature:
        """Extract function signature information."""
        parameters = []
        
        # Regular arguments
        for arg in node.args.args:
            param = Parameter(
                name=arg.arg,
                type_hint=self._get_type_annotation(arg.annotation),
                default_value=None,
                parameter_type=ParameterType.POSITIONAL
            )
            parameters.append(param)
        
        # Default values for regular arguments
        defaults = node.args.defaults
        if defaults:
            # Defaults apply to the last len(defaults) parameters
            start_idx = len(parameters) - len(defaults)
            for i, default in enumerate(defaults):
                if start_idx + i < len(parameters):
                    parameters[start_idx + i].default_value = self._get_default_value(default)
                    parameters[start_idx + i].parameter_type = ParameterType.KEYWORD
        
        # *args parameter
        if node.args.vararg:
            param = Parameter(
                name=node.args.vararg.arg,
                type_hint=self._get_type_annotation(node.args.vararg.annotation),
                default_value=None,
                parameter_type=ParameterType.VAR_POSITIONAL
            )
            parameters.append(param)
        
        # Keyword-only arguments
        for arg in node.args.kwonlyargs:
            param = Parameter(
                name=arg.arg,
                type_hint=self._get_type_annotation(arg.annotation),
                default_value=None,
                parameter_type=ParameterType.KEYWORD
            )
            parameters.append(param)
        
        # Default values for keyword-only arguments
        kw_defaults = node.args.kw_defaults
        if kw_defaults:
            kw_start = len(node.args.args) + (1 if node.args.vararg else 0)
            for i, default in enumerate(kw_defaults):
                if default is not None and kw_start + i < len(parameters):
                    parameters[kw_start + i].default_value = self._get_default_value(default)
        
        # **kwargs parameter
        if node.args.kwarg:
            param = Parameter(
                name=node.args.kwarg.arg,
                type_hint=self._get_type_annotation(node.args.kwarg.annotation),
                default_value=None,
                parameter_type=ParameterType.VAR_KEYWORD
            )
            parameters.append(param)
        
        # Return type
        return_type = self._get_type_annotation(node.returns)
        
        # Check if async
        is_async = isinstance(node, ast.AsyncFunctionDef)
        
        # Check if generator
        is_generator = self._is_generator(node)
        
        # Extract decorators
        decorators = []
        for decorator in node.decorator_list:
            decorators.append(self._get_decorator_name(decorator))
        
        return FunctionSignature(
            name=node.name,
            parameters=parameters,
            return_type=return_type,
            is_async=is_async,
            is_generator=is_generator,
            decorators=decorators
        )
    
    def _parse_docstring(self, docstring: str) -> Dict[str, Any]:
        """Parse docstring to extract structured information."""
        if not docstring:
            return {}
        
        parsed = {
            'description': '',
            'parameters': {},
            'returns': None,
            'raises': [],
            'examples': [],
            'notes': []
        }
        
        lines = docstring.strip().split('\n')
        current_section = 'description'
        current_content = []
        
        for line in lines:
            line = line.strip()
            
            # Check for section headers
            if line.lower().startswith(('args:', 'arguments:', 'parameters:', 'param:')):
                if current_content and current_section == 'description':
                    parsed['description'] = '\n'.join(current_content).strip()
                current_section = 'parameters'
                current_content = []
                continue
            elif line.lower().startswith(('returns:', 'return:')):
                self._save_current_section(parsed, current_section, current_content)
                current_section = 'returns'
                current_content = []
                continue
            elif line.lower().startswith(('raises:', 'raise:', 'except:', 'exceptions:')):
                self._save_current_section(parsed, current_section, current_content)
                current_section = 'raises'
                current_content = []
                continue
            elif line.lower().startswith(('examples:', 'example:')):
                self._save_current_section(parsed, current_section, current_content)
                current_section = 'examples'
                current_content = []
                continue
            elif line.lower().startswith(('notes:', 'note:')):
                self._save_current_section(parsed, current_section, current_content)
                current_section = 'notes'
                current_content = []
                continue
            
            # Parse parameter lines
            if current_section == 'parameters':
                param_match = re.match(r'^\s*(\w+)\s*(?:\(([^)]+)\))?\s*:\s*(.+)$', line)
                if param_match:
                    param_name, param_type, param_desc = param_match.groups()
                    parsed['parameters'][param_name] = {
                        'type': param_type,
                        'description': param_desc
                    }
                    continue
            
            # Add line to current content
            if line:
                current_content.append(line)
        
        # Save the last section
        self._save_current_section(parsed, current_section, current_content)
        
        return parsed
    
    def _save_current_section(self, parsed: Dict[str, Any], section: str, content: List[str]):
        """Save current section content to parsed docstring."""
        if not content:
            return
        
        content_str = '\n'.join(content).strip()
        
        if section == 'description':
            parsed['description'] = content_str
        elif section == 'returns':
            parsed['returns'] = content_str
        elif section == 'raises':
            parsed['raises'].extend([line.strip() for line in content if line.strip()])
        elif section == 'examples':
            parsed['examples'].extend([line.strip() for line in content if line.strip()])
        elif section == 'notes':
            parsed['notes'].extend([line.strip() for line in content if line.strip()])
    
    def _get_type_annotation(self, annotation: Optional[ast.AST]) -> Optional[str]:
        """Extract type annotation as string."""
        if annotation is None:
            return None
        
        if hasattr(ast, 'unparse'):
            return ast.unparse(annotation)
        else:
            # Fallback for older Python versions
            if isinstance(annotation, ast.Name):
                return annotation.id
            elif isinstance(annotation, ast.Constant):
                return str(annotation.value)
            else:
                return str(annotation)
    
    def _get_default_value(self, default: ast.AST) -> str:
        """Extract default value as string."""
        if hasattr(ast, 'unparse'):
            return ast.unparse(default)
        else:
            # Fallback for older Python versions
            if isinstance(default, ast.Constant):
                if isinstance(default.value, str):
                    return f"'{default.value}'"
                return str(default.value)
            elif isinstance(default, ast.Name):
                return default.id
            else:
                return str(default)
    
    def _is_generator(self, node: ast.FunctionDef) -> bool:
        """Check if function is a generator."""
        for child in ast.walk(node):
            if isinstance(child, (ast.Yield, ast.YieldFrom)):
                return True
        return False
    
    def _get_decorator_name(self, decorator: ast.AST) -> str:
        """Extract decorator name."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{decorator.value.id}.{decorator.attr}"
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id
            elif isinstance(decorator.func, ast.Attribute):
                return f"{decorator.func.value.id}.{decorator.func.attr}"
        
        return str(decorator)
    
    def _calculate_function_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity for a function."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.With, ast.AsyncWith)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _extract_function_calls(self, node: ast.FunctionDef) -> List[str]:
        """Extract function calls made within a function."""
        calls = []
        
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    calls.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    calls.append(child.func.attr)
        
        return list(set(calls))  # Remove duplicates
    
    def _build_call_graph(self, functions: Dict[str, FunctionDocumentation]):
        """Build call graph showing which functions call which."""
        # Update called_by information
        for func_name, func_doc in functions.items():
            for called_func in func_doc.calls_made:
                if called_func in functions:
                    functions[called_func].called_by.append(func_name)
    
    def generate_api_documentation(self, functions: Dict[str, FunctionDocumentation], 
                                 format_type: str = 'markdown') -> str:
        """Generate API documentation for extracted functions."""
        if format_type.lower() == 'markdown':
            return self._generate_markdown_docs(functions)
        elif format_type.lower() == 'rst':
            return self._generate_rst_docs(functions)
        elif format_type.lower() == 'json':
            return self._generate_json_docs(functions)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _generate_markdown_docs(self, functions: Dict[str, FunctionDocumentation]) -> str:
        """Generate Markdown documentation."""
        docs = ["# API Documentation\n"]
        
        for func_name, func_doc in sorted(functions.items()):
            docs.append(f"## {func_name}\n")
            
            # Function signature
            signature = self._format_signature_markdown(func_doc.signature)
            docs.append(f"```python\n{signature}\n```\n")
            
            # Description
            if func_doc.description:
                docs.append(f"{func_doc.description}\n")
            
            # Parameters
            if func_doc.parameters_doc:
                docs.append("### Parameters\n")
                for param_name, param_info in func_doc.parameters_doc.items():
                    if isinstance(param_info, dict):
                        param_type = param_info.get('type', '')
                        param_desc = param_info.get('description', '')
                        docs.append(f"- **{param_name}** ({param_type}): {param_desc}")
                    else:
                        docs.append(f"- **{param_name}**: {param_info}")
                docs.append("")
            
            # Returns
            if func_doc.returns_doc:
                docs.append(f"### Returns\n{func_doc.returns_doc}\n")
            
            # Examples
            if func_doc.examples:
                docs.append("### Examples\n")
                for example in func_doc.examples:
                    docs.append(f"```python\n{example}\n```\n")
            
            # Complexity
            docs.append(f"**Complexity:** {func_doc.complexity}\n")
            
            docs.append("---\n")
        
        return '\n'.join(docs)
    
    def _generate_rst_docs(self, functions: Dict[str, FunctionDocumentation]) -> str:
        """Generate reStructuredText documentation."""
        docs = ["API Documentation", "=================", ""]
        
        for func_name, func_doc in sorted(functions.items()):
            docs.append(func_name)
            docs.append("-" * len(func_name))
            docs.append("")
            
            # Function signature
            signature = self._format_signature_rst(func_doc.signature)
            docs.append(f".. code-block:: python\n\n   {signature}\n")
            
            # Description
            if func_doc.description:
                docs.append(func_doc.description)
                docs.append("")
            
            # Parameters
            if func_doc.parameters_doc:
                docs.append(":Parameters:")
                for param_name, param_info in func_doc.parameters_doc.items():
                    if isinstance(param_info, dict):
                        param_type = param_info.get('type', '')
                        param_desc = param_info.get('description', '')
                        docs.append(f"   **{param_name}** (*{param_type}*) -- {param_desc}")
                    else:
                        docs.append(f"   **{param_name}** -- {param_info}")
                docs.append("")
            
            # Returns
            if func_doc.returns_doc:
                docs.append(f":Returns: {func_doc.returns_doc}")
                docs.append("")
        
        return '\n'.join(docs)
    
    def _generate_json_docs(self, functions: Dict[str, FunctionDocumentation]) -> str:
        """Generate JSON documentation."""
        import json
        
        docs = {}
        for func_name, func_doc in functions.items():
            docs[func_name] = {
                'signature': asdict(func_doc.signature),
                'description': func_doc.description,
                'parameters': func_doc.parameters_doc,
                'returns': func_doc.returns_doc,
                'examples': func_doc.examples,
                'complexity': func_doc.complexity,
                'line_start': func_doc.line_start,
                'line_end': func_doc.line_end
            }
        
        return json.dumps(docs, indent=2)
    
    def _format_signature_markdown(self, signature: FunctionSignature) -> str:
        """Format function signature for Markdown."""
        params = []
        for param in signature.parameters:
            param_str = param.name
            if param.type_hint:
                param_str += f": {param.type_hint}"
            if param.default_value:
                param_str += f" = {param.default_value}"
            params.append(param_str)
        
        async_prefix = "async " if signature.is_async else ""
        return_suffix = f" -> {signature.return_type}" if signature.return_type else ""
        
        return f"{async_prefix}def {signature.name}({', '.join(params)}){return_suffix}:"
    
    def _format_signature_rst(self, signature: FunctionSignature) -> str:
        """Format function signature for reStructuredText."""
        return self._format_signature_markdown(signature)  # Same format for now
    
    def get_function_statistics(self, functions: Dict[str, FunctionDocumentation]) -> Dict[str, Any]:
        """Get statistics about extracted functions."""
        if not functions:
            return {}
        
        complexities = [func.complexity for func in functions.values()]
        documented_count = sum(1 for func in functions.values() if func.description)
        
        return {
            'total_functions': len(functions),
            'documented_functions': documented_count,
            'documentation_coverage': round(documented_count / len(functions) * 100, 2),
            'average_complexity': round(sum(complexities) / len(complexities), 2),
            'max_complexity': max(complexities),
            'min_complexity': min(complexities),
            'async_functions': sum(1 for func in functions.values() if func.signature.is_async),
            'generator_functions': sum(1 for func in functions.values() if func.signature.is_generator),
            'decorated_functions': sum(1 for func in functions.values() if func.signature.decorators)
        }