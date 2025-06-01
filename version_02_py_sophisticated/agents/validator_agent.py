"""
Validator Agent for code validation, testing, and quality assurance.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from pathlib import Path
import json
import re
import subprocess
from datetime import datetime
from enum import Enum

from ..utils.file_utils import FileUtils
from ..utils.ai_utils import AIUtils


class ValidationLevel(Enum):
    """Validation levels."""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    COMPREHENSIVE = "comprehensive"


class ValidationCategory(Enum):
    """Categories of validation."""
    SYNTAX = "syntax"
    STYLE = "style"
    LOGIC = "logic"
    PERFORMANCE = "performance"
    SECURITY = "security"
    DOCUMENTATION = "documentation"
    TESTING = "testing"


class IssueSeverity(Enum):
    """Issue severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidatorAgent:
    """Agent specialized in validating code quality and correctness."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the validator agent."""
        self.config = config
        self.validation_rules = self._load_validation_rules()
        self.language_validators = self._setup_language_validators()
        self.validation_history = []
    
    def _load_validation_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load validation rules for different languages and categories."""
        return {
            'python': {
                'syntax': {
                    'check_indentation': True,
                    'check_syntax_errors': True,
                    'check_imports': True
                },
                'style': {
                    'max_line_length': 88,  # Black formatter default
                    'check_naming_conventions': True,
                    'check_docstrings': True,
                    'check_type_hints': True
                },
                'logic': {
                    'check_unused_variables': True,
                    'check_undefined_variables': True,
                    'check_unreachable_code': True
                },
                'security': {
                    'check_sql_injection': True,
                    'check_hardcoded_secrets': True,
                    'check_unsafe_functions': True
                }
            },
            'javascript': {
                'syntax': {
                    'check_syntax_errors': True,
                    'check_semicolons': True,
                    'check_brackets': True
                },
                'style': {
                    'max_line_length': 100,
                    'check_naming_conventions': True,
                    'check_indentation': True
                },
                'logic': {
                    'check_unused_variables': True,
                    'check_undefined_variables': True,
                    'check_console_logs': True
                },
                'security': {
                    'check_eval_usage': True,
                    'check_xss_vulnerabilities': True,
                    'check_hardcoded_secrets': True
                }
            },
            'typescript': {
                'syntax': {
                    'check_syntax_errors': True,
                    'check_type_errors': True,
                    'check_imports': True
                },
                'style': {
                    'max_line_length': 100,
                    'check_naming_conventions': True,
                    'check_type_annotations': True
                },
                'logic': {
                    'check_unused_variables': True,
                    'check_type_safety': True,
                    'check_null_checks': True
                }
            }
        }
    
    def _setup_language_validators(self) -> Dict[str, Dict[str, Any]]:
        """Setup language-specific validators."""
        return {
            'python': {
                'syntax_checker': self._validate_python_syntax,
                'style_checker': self._validate_python_style,
                'logic_checker': self._validate_python_logic,
                'security_checker': self._validate_python_security
            },
            'javascript': {
                'syntax_checker': self._validate_js_syntax,
                'style_checker': self._validate_js_style,
                'logic_checker': self._validate_js_logic,
                'security_checker': self._validate_js_security
            },
            'typescript': {
                'syntax_checker': self._validate_ts_syntax,
                'style_checker': self._validate_ts_style,
                'logic_checker': self._validate_ts_logic,
                'security_checker': self._validate_js_security  # Reuse JS security checks
            }
        }
    
    def validate_file(self, file_path: Path, validation_level: ValidationLevel = ValidationLevel.STANDARD) -> Dict[str, Any]:
        """Validate a single file."""
        result = {
            'file_path': str(file_path),
            'timestamp': datetime.now().isoformat(),
            'validation_level': validation_level.value,
            'language': 'unknown',
            'overall_score': 0,
            'issues': [],
            'metrics': {},
            'suggestions': [],
            'passed': False
        }
        
        try:
            if not FileUtils.file_exists(file_path):
                result['issues'].append({
                    'category': ValidationCategory.SYNTAX.value,
                    'severity': IssueSeverity.ERROR.value,
                    'message': f"File {file_path} does not exist",
                    'line_number': None
                })
                return result
            
            # Detect language
            language = self._detect_language(file_path)
            result['language'] = language
            
            if language not in self.language_validators:
                result['issues'].append({
                    'category': ValidationCategory.SYNTAX.value,
                    'severity': IssueSeverity.WARNING.value,
                    'message': f"No validator available for language: {language}",
                    'line_number': None
                })
                return result
            
            # Read file content
            content = FileUtils.read_file(file_path)
            
            # Run validation checks based on level
            validators = self.language_validators[language]
            
            # Always run syntax validation
            syntax_issues = validators['syntax_checker'](content, file_path)
            result['issues'].extend(syntax_issues)
            
            # Run additional validations based on level
            if validation_level in [ValidationLevel.STANDARD, ValidationLevel.STRICT, ValidationLevel.COMPREHENSIVE]:
                style_issues = validators['style_checker'](content, file_path)
                result['issues'].extend(style_issues)
                
                logic_issues = validators['logic_checker'](content, file_path)
                result['issues'].extend(logic_issues)
            
            if validation_level in [ValidationLevel.STRICT, ValidationLevel.COMPREHENSIVE]:
                security_issues = validators['security_checker'](content, file_path)
                result['issues'].extend(security_issues)
            
            if validation_level == ValidationLevel.COMPREHENSIVE:
                # Additional comprehensive checks
                doc_issues = self._validate_documentation(content, language)
                result['issues'].extend(doc_issues)
                
                performance_issues = self._validate_performance(content, language)
                result['issues'].extend(performance_issues)
            
            # Calculate metrics
            result['metrics'] = self._calculate_metrics(content, result['issues'])
            
            # Calculate overall score
            result['overall_score'] = self._calculate_score(result['issues'], result['metrics'])
            
            # Generate suggestions
            result['suggestions'] = self._generate_suggestions(result['issues'], language)
            
            # Determine if validation passed
            critical_errors = [issue for issue in result['issues'] 
                             if issue['severity'] == IssueSeverity.CRITICAL.value]
            errors = [issue for issue in result['issues'] 
                     if issue['severity'] == IssueSeverity.ERROR.value]
            
            result['passed'] = len(critical_errors) == 0 and len(errors) == 0
            
            # Record validation
            self.validation_history.append(result.copy())
            
            return result
        
        except Exception as e:
            result['issues'].append({
                'category': ValidationCategory.SYNTAX.value,
                'severity': IssueSeverity.CRITICAL.value,
                'message': f"Validation failed: {e}",
                'line_number': None
            })
            return result
    
    def validate_project(self, project_path: Path, validation_level: ValidationLevel = ValidationLevel.STANDARD) -> Dict[str, Any]:
        """Validate an entire project."""
        result = {
            'project_path': str(project_path),
            'timestamp': datetime.now().isoformat(),
            'validation_level': validation_level.value,
            'file_results': {},
            'overall_score': 0,
            'total_issues': 0,
            'issue_summary': {},
            'suggestions': [],
            'passed': False
        }
        
        try:
            # Find all code files
            code_files = self._find_code_files(project_path)
            
            if not code_files:
                result['suggestions'].append("No code files found in project")
                return result
            
            # Validate each file
            all_issues = []
            total_score = 0
            
            for file_path in code_files:
                file_result = self.validate_file(file_path, validation_level)
                result['file_results'][str(file_path)] = file_result
                
                all_issues.extend(file_result['issues'])
                total_score += file_result['overall_score']
            
            # Calculate project-wide metrics
            result['total_issues'] = len(all_issues)
            result['overall_score'] = total_score / len(code_files) if code_files else 0
            
            # Summarize issues by category and severity
            result['issue_summary'] = self._summarize_issues(all_issues)
            
            # Generate project-level suggestions
            result['suggestions'] = self._generate_project_suggestions(result)
            
            # Determine if project validation passed
            critical_count = result['issue_summary'].get('severity', {}).get('critical', 0)
            error_count = result['issue_summary'].get('severity', {}).get('error', 0)
            
            result['passed'] = critical_count == 0 and error_count == 0
            
            return result
        
        except Exception as e:
            result['suggestions'].append(f"Project validation failed: {e}")
            return result
    
    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension."""
        extension = file_path.suffix.lower()
        
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.jsx': 'javascript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php'
        }
        
        return extension_map.get(extension, 'unknown')
    
    def _find_code_files(self, project_path: Path) -> List[Path]:
        """Find all code files in a project."""
        code_extensions = {'.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.cpp', '.c', '.cs', '.go', '.rs', '.rb', '.php'}
        
        code_files = []
        for file_path in project_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in code_extensions:
                # Skip common directories to ignore
                skip_dirs = {'node_modules', '__pycache__', '.git', 'venv', 'env', 'build', 'dist'}
                if not any(part in skip_dirs for part in file_path.parts):
                    code_files.append(file_path)
        
        return code_files
    
    def _validate_python_syntax(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Validate Python syntax."""
        issues = []
        
        try:
            # Try to compile the Python code
            compile(content, str(file_path), 'exec')
        except SyntaxError as e:
            issues.append({
                'category': ValidationCategory.SYNTAX.value,
                'severity': IssueSeverity.ERROR.value,
                'message': f"Syntax error: {e.msg}",
                'line_number': e.lineno,
                'column': e.offset
            })
        except Exception as e:
            issues.append({
                'category': ValidationCategory.SYNTAX.value,
                'severity': IssueSeverity.ERROR.value,
                'message': f"Compilation error: {e}",
                'line_number': None
            })
        
        # Check for import issues
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for relative imports without proper package structure
            if stripped.startswith('from .') and not self._is_package_file(file_path):
                issues.append({
                    'category': ValidationCategory.SYNTAX.value,
                    'severity': IssueSeverity.WARNING.value,
                    'message': "Relative import in non-package file",
                    'line_number': i
                })
        
        return issues
    
    def _validate_python_style(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Validate Python style."""
        issues = []
        lines = content.split('\n')
        
        rules = self.validation_rules['python']['style']
        
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > rules['max_line_length']:
                issues.append({
                    'category': ValidationCategory.STYLE.value,
                    'severity': IssueSeverity.WARNING.value,
                    'message': f"Line too long ({len(line)} > {rules['max_line_length']})",
                    'line_number': i
                })
            
            # Check for tabs
            if '\t' in line:
                issues.append({
                    'category': ValidationCategory.STYLE.value,
                    'severity': IssueSeverity.WARNING.value,
                    'message': "Use spaces instead of tabs",
                    'line_number': i
                })
            
            # Check trailing whitespace
            if line.endswith(' ') or line.endswith('\t'):
                issues.append({
                    'category': ValidationCategory.STYLE.value,
                    'severity': IssueSeverity.INFO.value,
                    'message': "Trailing whitespace",
                    'line_number': i
                })
        
        # Check naming conventions
        if rules['check_naming_conventions']:
            issues.extend(self._check_python_naming(content))
        
        return issues
    
    def _validate_python_logic(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Validate Python logic."""
        issues = []
        lines = content.split('\n')
        
        # Check for unused imports
        import_lines = []
        code_content = ""
        
        for line in lines:
            if line.strip().startswith(('import ', 'from ')):
                import_lines.append(line.strip())
            else:
                code_content += line + '\n'
        
        for import_line in import_lines:
            # Extract imported names
            if import_line.startswith('import '):
                module_name = import_line.replace('import ', '').split(' as ')[0].strip()
                if module_name not in code_content:
                    issues.append({
                        'category': ValidationCategory.LOGIC.value,
                        'severity': IssueSeverity.WARNING.value,
                        'message': f"Unused import: {module_name}",
                        'line_number': self._find_line_number(content, import_line)
                    })
        
        # Check for undefined variables (simplified)
        defined_vars = set()
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Track variable definitions
            if '=' in stripped and not stripped.startswith('#'):
                var_name = stripped.split('=')[0].strip()
                if var_name.isidentifier():
                    defined_vars.add(var_name)
        
        return issues
    
    def _validate_python_security(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Validate Python security."""
        issues = []
        lines = content.split('\n')
        
        # Check for dangerous functions
        dangerous_functions = ['eval', 'exec', 'compile', '__import__']
        
        for i, line in enumerate(lines, 1):
            for func in dangerous_functions:
                if func + '(' in line:
                    issues.append({
                        'category': ValidationCategory.SECURITY.value,
                        'severity': IssueSeverity.WARNING.value,
                        'message': f"Potentially dangerous function: {func}",
                        'line_number': i
                    })
        
        # Check for hardcoded secrets
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']'
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern in secret_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        'category': ValidationCategory.SECURITY.value,
                        'severity': IssueSeverity.ERROR.value,
                        'message': "Potential hardcoded secret",
                        'line_number': i
                    })
        
        return issues
    
    def _validate_js_syntax(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Validate JavaScript syntax."""
        issues = []
        lines = content.split('\n')
        
        # Basic syntax checks
        brace_count = 0
        paren_count = 0
        bracket_count = 0
        
        for i, line in enumerate(lines, 1):
            # Count braces, parentheses, and brackets
            brace_count += line.count('{') - line.count('}')
            paren_count += line.count('(') - line.count(')')
            bracket_count += line.count('[') - line.count(']')
        
        # Check for unmatched braces/parentheses
        if brace_count != 0:
            issues.append({
                'category': ValidationCategory.SYNTAX.value,
                'severity': IssueSeverity.ERROR.value,
                'message': "Unmatched braces",
                'line_number': None
            })
        
        if paren_count != 0:
            issues.append({
                'category': ValidationCategory.SYNTAX.value,
                'severity': IssueSeverity.ERROR.value,
                'message': "Unmatched parentheses",
                'line_number': None
            })
        
        if bracket_count != 0:
            issues.append({
                'category': ValidationCategory.SYNTAX.value,
                'severity': IssueSeverity.ERROR.value,
                'message': "Unmatched brackets",
                'line_number': None
            })
        
        return issues
    
    def _validate_js_style(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Validate JavaScript style."""
        issues = []
        lines = content.split('\n')
        
        rules = self.validation_rules['javascript']['style']
        
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > rules['max_line_length']:
                issues.append({
                    'category': ValidationCategory.STYLE.value,
                    'severity': IssueSeverity.WARNING.value,
                    'message': f"Line too long ({len(line)} > {rules['max_line_length']})",
                    'line_number': i
                })
            
            # Check for console.log in production code
            if 'console.log' in line and not line.strip().startswith('//'):
                issues.append({
                    'category': ValidationCategory.STYLE.value,
                    'severity': IssueSeverity.INFO.value,
                    'message': "console.log statement found",
                    'line_number': i
                })
        
        return issues
    
    def _validate_js_logic(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Validate JavaScript logic."""
        issues = []
        lines = content.split('\n')
        
        # Check for == vs === usage
        for i, line in enumerate(lines, 1):
            if ' == ' in line and ' === ' not in line:
                issues.append({
                    'category': ValidationCategory.LOGIC.value,
                    'severity': IssueSeverity.WARNING.value,
                    'message': "Use === instead of == for comparison",
                    'line_number': i
                })
        
        return issues
    
    def _validate_js_security(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Validate JavaScript security."""
        issues = []
        lines = content.split('\n')
        
        # Check for eval usage
        for i, line in enumerate(lines, 1):
            if 'eval(' in line:
                issues.append({
                    'category': ValidationCategory.SECURITY.value,
                    'severity': IssueSeverity.ERROR.value,
                    'message': "eval() is dangerous and should be avoided",
                    'line_number': i
                })
        
        return issues
    
    def _validate_ts_syntax(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Validate TypeScript syntax."""
        # Start with JavaScript validation
        issues = self._validate_js_syntax(content, file_path)
        
        # Add TypeScript-specific checks
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for any type usage
            if ': any' in line:
                issues.append({
                    'category': ValidationCategory.SYNTAX.value,
                    'severity': IssueSeverity.WARNING.value,
                    'message': "Avoid using 'any' type, use specific types instead",
                    'line_number': i
                })
        
        return issues
    
    def _validate_ts_style(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Validate TypeScript style."""
        # Start with JavaScript style validation
        issues = self._validate_js_style(content, file_path)
        
        # Add TypeScript-specific style checks
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for missing type annotations on function parameters
            if 'function ' in line and '(' in line and ')' in line:
                params_section = line[line.find('('):line.find(')') + 1]
                if ':' not in params_section and params_section != '()':
                    issues.append({
                        'category': ValidationCategory.STYLE.value,
                        'severity': IssueSeverity.INFO.value,
                        'message': "Consider adding type annotations to function parameters",
                        'line_number': i
                    })
        
        return issues
    
    def _validate_ts_logic(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Validate TypeScript logic."""
        # Start with JavaScript logic validation
        issues = self._validate_js_logic(content, file_path)
        
        # Add TypeScript-specific logic checks
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for non-null assertion operator usage
            if '!' in line and not line.strip().startswith('//'):
                # Simple check for non-null assertion
                if re.search(r'\w+!\.', line):
                    issues.append({
                        'category': ValidationCategory.LOGIC.value,
                        'severity': IssueSeverity.WARNING.value,
                        'message': "Non-null assertion operator (!) should be used carefully",
                        'line_number': i
                    })
        
        return issues
    
    def _validate_documentation(self, content: str, language: str) -> List[Dict[str, Any]]:
        """Validate documentation."""
        issues = []
        lines = content.split('\n')
        
        if language == 'python':
            # Check for missing docstrings
            in_class = False
            in_function = False
            
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                
                if stripped.startswith('class '):
                    in_class = True
                    # Check if next non-empty line is a docstring
                    next_line_idx = i
                    while next_line_idx < len(lines) and not lines[next_line_idx].strip():
                        next_line_idx += 1
                    
                    if next_line_idx < len(lines):
                        next_line = lines[next_line_idx].strip()
                        if not (next_line.startswith('"""') or next_line.startswith("'''")):
                            issues.append({
                                'category': ValidationCategory.DOCUMENTATION.value,
                                'severity': IssueSeverity.WARNING.value,
                                'message': "Class missing docstring",
                                'line_number': i
                            })
                
                elif stripped.startswith('def '):
                    in_function = True
                    # Check if next non-empty line is a docstring
                    next_line_idx = i
                    while next_line_idx < len(lines) and not lines[next_line_idx].strip():
                        next_line_idx += 1
                    
                    if next_line_idx < len(lines):
                        next_line = lines[next_line_idx].strip()
                        if not (next_line.startswith('"""') or next_line.startswith("'''")):
                            issues.append({
                                'category': ValidationCategory.DOCUMENTATION.value,
                                'severity': IssueSeverity.INFO.value,
                                'message': "Function missing docstring",
                                'line_number': i
                            })
        
        return issues
    
    def _validate_performance(self, content: str, language: str) -> List[Dict[str, Any]]:
        """Validate performance-related issues."""
        issues = []
        lines = content.split('\n')
        
        if language == 'python':
            for i, line in enumerate(lines, 1):
                # Check for inefficient string concatenation
                if '+=' in line and 'str' in line.lower():
                    issues.append({
                        'category': ValidationCategory.PERFORMANCE.value,
                        'severity': IssueSeverity.INFO.value,
                        'message': "Consider using join() for string concatenation in loops",
                        'line_number': i
                    })
        
        elif language in ['javascript', 'typescript']:
            for i, line in enumerate(lines, 1):
                # Check for inefficient DOM queries
                if 'document.getElementById' in line and 'for' in line:
                    issues.append({
                        'category': ValidationCategory.PERFORMANCE.value,
                        'severity': IssueSeverity.INFO.value,
                        'message': "Cache DOM queries outside loops",
                        'line_number': i
                    })
        
        return issues
    
    def _check_python_naming(self, content: str) -> List[Dict[str, Any]]:
        """Check Python naming conventions."""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check class names (should be PascalCase)
            if stripped.startswith('class '):
                class_name = stripped.split('(')[0].replace('class ', '').strip(':')
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', class_name):
                    issues.append({
                        'category': ValidationCategory.STYLE.value,
                        'severity': IssueSeverity.WARNING.value,
                        'message': f"Class name '{class_name}' should be PascalCase",
                        'line_number': i
                    })
            
            # Check function names (should be snake_case)
            elif stripped.startswith('def '):
                func_name = stripped.split('(')[0].replace('def ', '')
                if not re.match(r'^[a-z_][a-z0-9_]*$', func_name):
                    issues.append({
                        'category': ValidationCategory.STYLE.value,
                        'severity': IssueSeverity.WARNING.value,
                        'message': f"Function name '{func_name}' should be snake_case",
                        'line_number': i
                    })
        
        return issues
    
    def _is_package_file(self, file_path: Path) -> bool:
        """Check if file is part of a Python package."""
        return (file_path.parent / '__init__.py').exists()
    
    def _find_line_number(self, content: str, text: str) -> int:
        """Find line number where text appears."""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if text in line:
                return i
        return 1
    
    def _calculate_metrics(self, content: str, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate code metrics."""
        lines = content.split('\n')
        
        metrics = {
            'total_lines': len(lines),
            'code_lines': len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
            'comment_lines': len([line for line in lines if line.strip().startswith('#')]),
            'blank_lines': len([line for line in lines if not line.strip()]),
            'issue_count': len(issues),
            'issue_density': 0
        }
        
        if metrics['code_lines'] > 0:
            metrics['issue_density'] = metrics['issue_count'] / metrics['code_lines']
        
        return metrics
    
    def _calculate_score(self, issues: List[Dict[str, Any]], metrics: Dict[str, Any]) -> float:
        """Calculate overall quality score (0-100)."""
        base_score = 100
        
        # Deduct points for issues
        for issue in issues:
            severity = issue['severity']
            if severity == IssueSeverity.CRITICAL.value:
                base_score -= 20
            elif severity == IssueSeverity.ERROR.value:
                base_score -= 10
            elif severity == IssueSeverity.WARNING.value:
                base_score -= 5
            elif severity == IssueSeverity.INFO.value:
                base_score -= 1
        
        # Bonus for good metrics
        if metrics.get('issue_density', 1) < 0.1:  # Less than 0.1 issues per line of code
            base_score += 5
        
        return max(0, min(100, base_score))
    
    def _generate_suggestions(self, issues: List[Dict[str, Any]], language: str) -> List[str]:
        """Generate suggestions based on issues found."""
        suggestions = []
        
        # Count issues by category
        category_counts = {}
        severity_counts = {}
        
        for issue in issues:
            category = issue['category']
            severity = issue['severity']
            
            category_counts[category] = category_counts.get(category, 0) + 1
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Generate category-specific suggestions
        if category_counts.get(ValidationCategory.STYLE.value, 0) > 5:
            if language == 'python':
                suggestions.append("Consider using a code formatter like Black or autopep8")
            elif language in ['javascript', 'typescript']:
                suggestions.append("Consider using a code formatter like Prettier")
        
        if category_counts.get(ValidationCategory.SECURITY.value, 0) > 0:
            suggestions.append("Review security issues carefully and consider using security linting tools")
        
        if category_counts.get(ValidationCategory.DOCUMENTATION.value, 0) > 3:
            suggestions.append("Add documentation to improve code maintainability")
        
        # Generate severity-specific suggestions
        if severity_counts.get(IssueSeverity.CRITICAL.value, 0) > 0:
            suggestions.append("Address critical issues immediately before proceeding")
        
        if severity_counts.get(IssueSeverity.ERROR.value, 0) > 0:
            suggestions.append("Fix all errors to ensure code functionality")
        
        return suggestions
    
    def _summarize_issues(self, issues: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
        """Summarize issues by category and severity."""
        summary = {
            'category': {},
            'severity': {}
        }
        
        for issue in issues:
            category = issue['category']
            severity = issue['severity']
            
            summary['category'][category] = summary['category'].get(category, 0) + 1
            summary['severity'][severity] = summary['severity'].get(severity, 0) + 1
        
        return summary
    
    def _generate_project_suggestions(self, project_result: Dict[str, Any]) -> List[str]:
        """Generate project-level suggestions."""
        suggestions = []
        
        issue_summary = project_result['issue_summary']
        overall_score = project_result['overall_score']
        
        if overall_score < 50:
            suggestions.append("Project quality is below acceptable standards. Consider major refactoring.")
        elif overall_score < 70:
            suggestions.append("Project quality needs improvement. Focus on addressing errors and warnings.")
        elif overall_score < 85:
            suggestions.append("Good project quality. Address remaining issues for excellence.")
        else:
            suggestions.append("Excellent project quality. Keep up the good work!")
        
        # File-specific suggestions
        file_count = len(project_result['file_results'])
        failed_files = sum(1 for result in project_result['file_results'].values() if not result['passed'])
        
        if failed_files > 0:
            suggestions.append(f"{failed_files} out of {file_count} files have validation issues")
        
        return suggestions
    
    def generate_validation_report(self, validation_result: Dict[str, Any]) -> str:
        """Generate a human-readable validation report."""
        if 'file_results' in validation_result:
            # Project validation report
            return self._generate_project_report(validation_result)
        else:
            # Single file validation report
            return self._generate_file_report(validation_result)
    
    def _generate_file_report(self, result: Dict[str, Any]) -> str:
        """Generate a report for single file validation."""
        report_parts = [
            f"Validation Report: {result['file_path']}",
            f"Language: {result['language']}",
            f"Overall Score: {result['overall_score']:.1f}/100",
            f"Status: {'PASSED' if result['passed'] else 'FAILED'}",
            ""
        ]
        
        # Metrics
        metrics = result['metrics']
        report_parts.extend([
            "Metrics:",
            f"  Total Lines: {metrics.get('total_lines', 0)}",
            f"  Code Lines: {metrics.get('code_lines', 0)}",
            f"  Comment Lines: {metrics.get('comment_lines', 0)}",
            f"  Issues Found: {metrics.get('issue_count', 0)}",
            ""
        ])
        
        # Issues by severity
        issues = result['issues']
        if issues:
            severity_counts = {}
            for issue in issues:
                severity = issue['severity']
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            report_parts.append("Issues by Severity:")
            for severity, count in severity_counts.items():
                report_parts.append(f"  {severity.title()}: {count}")
            report_parts.append("")
            
            # Detailed issues
            report_parts.append("Detailed Issues:")
            for issue in issues[:10]:  # Show first 10 issues
                line_info = f" (line {issue['line_number']})" if issue['line_number'] else ""
                report_parts.append(f"  [{issue['severity'].upper()}] {issue['message']}{line_info}")
            
            if len(issues) > 10:
                report_parts.append(f"  ... and {len(issues) - 10} more issues")
            report_parts.append("")
        
        # Suggestions
        suggestions = result['suggestions']
        if suggestions:
            report_parts.append("Suggestions:")
            for suggestion in suggestions:
                report_parts.append(f"  - {suggestion}")
        
        return '\n'.join(report_parts)
    
    def _generate_project_report(self, result: Dict[str, Any]) -> str:
        """Generate a report for project validation."""
        report_parts = [
            f"Project Validation Report: {result['project_path']}",
            f"Overall Score: {result['overall_score']:.1f}/100",
            f"Status: {'PASSED' if result['passed'] else 'FAILED'}",
            f"Total Issues: {result['total_issues']}",
            ""
        ]
        
        # Issue summary
        issue_summary = result['issue_summary']
        if issue_summary.get('severity'):
            report_parts.append("Issues by Severity:")
            for severity, count in issue_summary['severity'].items():
                report_parts.append(f"  {severity.title()}: {count}")
            report_parts.append("")
        
        if issue_summary.get('category'):
            report_parts.append("Issues by Category:")
            for category, count in issue_summary['category'].items():
                report_parts.append(f"  {category.title()}: {count}")
            report_parts.append("")
        
        # File summary
        file_results = result['file_results']
        passed_files = sum(1 for r in file_results.values() if r['passed'])
        total_files = len(file_results)
        
        report_parts.extend([
            f"File Summary: {passed_files}/{total_files} files passed validation",
            ""
        ])
        
        # Top issues files
        failed_files = [(path, r) for path, r in file_results.items() if not r['passed']]
        if failed_files:
            report_parts.append("Files with Issues:")
            for path, file_result in failed_files[:5]:  # Show top 5
                issue_count = len(file_result['issues'])
                score = file_result['overall_score']
                report_parts.append(f"  {path}: {issue_count} issues (score: {score:.1f})")
            
            if len(failed_files) > 5:
                report_parts.append(f"  ... and {len(failed_files) - 5} more files")
            report_parts.append("")
        
        # Suggestions
        suggestions = result['suggestions']
        if suggestions:
            report_parts.append("Suggestions:")
            for suggestion in suggestions:
                report_parts.append(f"  - {suggestion}")
        
        return '\n'.join(report_parts)
    
    def get_validation_history(self, file_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Get validation history, optionally filtered by file."""
        if file_path:
            return [validation for validation in self.validation_history 
                   if validation.get('file_path') == str(file_path)]
        return self.validation_history.copy()