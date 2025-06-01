"""
Validation system for code changes to ensure quality and correctness.
"""

import ast
import re
import subprocess
import tempfile
from typing import Dict, Any, List, Optional, Tuple, Set
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from ..utils.file_utils import FileUtils


class ValidationLevel(Enum):
    """Validation strictness levels."""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    PEDANTIC = "pedantic"


class IssueType(Enum):
    """Types of validation issues."""
    SYNTAX_ERROR = "syntax_error"
    IMPORT_ERROR = "import_error"
    STYLE_VIOLATION = "style_violation"
    LOGIC_ERROR = "logic_error"
    SECURITY_ISSUE = "security_issue"
    PERFORMANCE_ISSUE = "performance_issue"
    COMPATIBILITY_ISSUE = "compatibility_issue"


class IssueSeverity(Enum):
    """Severity levels for validation issues."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    SUGGESTION = "suggestion"


@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    type: IssueType
    severity: IssueSeverity
    message: str
    line_number: int
    column: Optional[int]
    file_path: Optional[str]
    suggestion: Optional[str] = None
    rule_id: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of code validation."""
    is_valid: bool
    issues: List[ValidationIssue]
    score: float  # Quality score 0-100
    summary: Dict[str, int]
    suggestions: List[str]


class ChangeValidator:
    """Comprehensive code change validation system."""
    
    def __init__(self, validation_level: ValidationLevel = ValidationLevel.STANDARD):
        """Initialize the change validator."""
        self.validation_level = validation_level
        self.max_line_length = 88  # PEP 8 recommendation
        self.max_complexity = 10
        self.enable_security_checks = True
        self.enable_performance_checks = True
        
        # Security patterns to check for
        self.security_patterns = {
            'eval_usage': r'\beval\s*\(',
            'exec_usage': r'\bexec\s*\(',
            'shell_injection': r'subprocess\.(call|run|Popen).*shell\s*=\s*True',
            'sql_injection': r'["\'].*%s.*["\']',
            'hardcoded_password': r'password\s*=\s*["\'][^"\']+["\']',
            'hardcoded_secret': r'(secret|token|key)\s*=\s*["\'][^"\']+["\']'
        }
        
        # Performance anti-patterns
        self.performance_patterns = {
            'string_concatenation_loop': r'for\s+.*:\s*.*\+=.*["\']',
            'inefficient_membership': r'\bin\s+\[.*\]',
            'global_in_loop': r'for\s+.*:\s*.*global\s+',
            'repeated_computation': r'for\s+.*:\s*.*len\('
        }
    
    def validate_code(self, code: str, file_path: Optional[Path] = None) -> ValidationResult:
        """Validate code comprehensively."""
        issues = []
        
        # Basic syntax validation
        syntax_issues = self._validate_syntax(code, file_path)
        issues.extend(syntax_issues)
        
        # If syntax is invalid, return early
        if any(issue.severity == IssueSeverity.ERROR for issue in syntax_issues):
            return ValidationResult(
                is_valid=False,
                issues=issues,
                score=0.0,
                summary=self._create_summary(issues),
                suggestions=[]
            )
        
        # Style validation
        if self.validation_level in [ValidationLevel.STANDARD, ValidationLevel.STRICT, ValidationLevel.PEDANTIC]:
            style_issues = self._validate_style(code, file_path)
            issues.extend(style_issues)
        
        # Import validation
        import_issues = self._validate_imports(code, file_path)
        issues.extend(import_issues)
        
        # Logic validation
        if self.validation_level in [ValidationLevel.STRICT, ValidationLevel.PEDANTIC]:
            logic_issues = self._validate_logic(code, file_path)
            issues.extend(logic_issues)
        
        # Security validation
        if self.enable_security_checks:
            security_issues = self._validate_security(code, file_path)
            issues.extend(security_issues)
        
        # Performance validation
        if self.enable_performance_checks and self.validation_level == ValidationLevel.PEDANTIC:
            performance_issues = self._validate_performance(code, file_path)
            issues.extend(performance_issues)
        
        # Calculate quality score
        score = self._calculate_quality_score(code, issues)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(issues)
        
        # Determine if code is valid
        is_valid = not any(issue.severity == IssueSeverity.ERROR for issue in issues)
        
        return ValidationResult(
            is_valid=is_valid,
            issues=issues,
            score=score,
            summary=self._create_summary(issues),
            suggestions=suggestions
        )
    
    def validate_change(self, original_code: str, modified_code: str, 
                       file_path: Optional[Path] = None) -> ValidationResult:
        """Validate a code change by comparing original and modified versions."""
        # Validate the modified code
        result = self.validate_code(modified_code, file_path)
        
        # Additional change-specific validations
        change_issues = self._validate_change_specific(original_code, modified_code, file_path)
        result.issues.extend(change_issues)
        
        # Recalculate score and validity
        result.score = self._calculate_quality_score(modified_code, result.issues)
        result.is_valid = not any(issue.severity == IssueSeverity.ERROR for issue in result.issues)
        result.summary = self._create_summary(result.issues)
        
        return result
    
    def _validate_syntax(self, code: str, file_path: Optional[Path]) -> List[ValidationIssue]:
        """Validate Python syntax."""
        issues = []
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append(ValidationIssue(
                type=IssueType.SYNTAX_ERROR,
                severity=IssueSeverity.ERROR,
                message=f"Syntax error: {e.msg}",
                line_number=e.lineno or 0,
                column=e.offset,
                file_path=str(file_path) if file_path else None,
                rule_id="E001"
            ))
        except Exception as e:
            issues.append(ValidationIssue(
                type=IssueType.SYNTAX_ERROR,
                severity=IssueSeverity.ERROR,
                message=f"Parse error: {str(e)}",
                line_number=0,
                column=None,
                file_path=str(file_path) if file_path else None,
                rule_id="E002"
            ))
        
        return issues
    
    def _validate_style(self, code: str, file_path: Optional[Path]) -> List[ValidationIssue]:
        """Validate code style (PEP 8 compliance)."""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Line length check
            if len(line) > self.max_line_length:
                issues.append(ValidationIssue(
                    type=IssueType.STYLE_VIOLATION,
                    severity=IssueSeverity.WARNING,
                    message=f"Line too long ({len(line)} > {self.max_line_length} characters)",
                    line_number=i,
                    column=self.max_line_length,
                    file_path=str(file_path) if file_path else None,
                    suggestion=f"Break line into multiple lines",
                    rule_id="W001"
                ))
            
            # Trailing whitespace
            if line.endswith(' ') or line.endswith('\t'):
                issues.append(ValidationIssue(
                    type=IssueType.STYLE_VIOLATION,
                    severity=IssueSeverity.INFO,
                    message="Trailing whitespace",
                    line_number=i,
                    column=len(line.rstrip()),
                    file_path=str(file_path) if file_path else None,
                    suggestion="Remove trailing whitespace",
                    rule_id="W002"
                ))
            
            # Mixed tabs and spaces
            if '\t' in line and '    ' in line:
                issues.append(ValidationIssue(
                    type=IssueType.STYLE_VIOLATION,
                    severity=IssueSeverity.WARNING,
                    message="Mixed tabs and spaces",
                    line_number=i,
                    column=0,
                    file_path=str(file_path) if file_path else None,
                    suggestion="Use consistent indentation (prefer spaces)",
                    rule_id="W003"
                ))
            
            # Multiple statements on one line
            if ';' in line and not line.strip().startswith('#'):
                issues.append(ValidationIssue(
                    type=IssueType.STYLE_VIOLATION,
                    severity=IssueSeverity.WARNING,
                    message="Multiple statements on one line",
                    line_number=i,
                    column=line.find(';'),
                    file_path=str(file_path) if file_path else None,
                    suggestion="Put each statement on a separate line",
                    rule_id="W004"
                ))
        
        # Check for missing docstrings
        try:
            tree = ast.parse(code)
            issues.extend(self._check_docstrings(tree, file_path))
        except:
            pass  # Already handled in syntax validation
        
        return issues
    
    def _validate_imports(self, code: str, file_path: Optional[Path]) -> List[ValidationIssue]:
        """Validate import statements."""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            # Check for unused imports (simplified)
            imported_names = set()
            used_names = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_names.add(alias.asname or alias.name)
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        if alias.name != '*':
                            imported_names.add(alias.asname or alias.name)
                elif isinstance(node, ast.Name):
                    used_names.add(node.id)
            
            # Find potentially unused imports
            unused_imports = imported_names - used_names
            for unused in unused_imports:
                issues.append(ValidationIssue(
                    type=IssueType.IMPORT_ERROR,
                    severity=IssueSeverity.INFO,
                    message=f"Potentially unused import: {unused}",
                    line_number=0,  # Would need more complex analysis to get line number
                    column=None,
                    file_path=str(file_path) if file_path else None,
                    suggestion=f"Remove unused import '{unused}' if not needed",
                    rule_id="I001"
                ))
            
        except:
            pass  # Already handled in syntax validation
        
        return issues
    
    def _validate_logic(self, code: str, file_path: Optional[Path]) -> List[ValidationIssue]:
        """Validate code logic and detect potential issues."""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            # Check for unreachable code
            issues.extend(self._check_unreachable_code(tree, file_path))
            
            # Check for complexity
            issues.extend(self._check_complexity(tree, file_path))
            
            # Check for potential bugs
            issues.extend(self._check_potential_bugs(tree, file_path))
            
        except:
            pass  # Already handled in syntax validation
        
        return issues
    
    def _validate_security(self, code: str, file_path: Optional[Path]) -> List[ValidationIssue]:
        """Validate code for security issues."""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern_name, pattern in self.security_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    severity = IssueSeverity.ERROR if pattern_name in ['eval_usage', 'exec_usage'] else IssueSeverity.WARNING
                    
                    issues.append(ValidationIssue(
                        type=IssueType.SECURITY_ISSUE,
                        severity=severity,
                        message=f"Security issue: {pattern_name.replace('_', ' ')}",
                        line_number=i,
                        column=0,
                        file_path=str(file_path) if file_path else None,
                        suggestion=self._get_security_suggestion(pattern_name),
                        rule_id=f"S{hash(pattern_name) % 1000:03d}"
                    ))
        
        return issues
    
    def _validate_performance(self, code: str, file_path: Optional[Path]) -> List[ValidationIssue]:
        """Validate code for performance issues."""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern_name, pattern in self.performance_patterns.items():
                if re.search(pattern, line):
                    issues.append(ValidationIssue(
                        type=IssueType.PERFORMANCE_ISSUE,
                        severity=IssueSeverity.SUGGESTION,
                        message=f"Performance issue: {pattern_name.replace('_', ' ')}",
                        line_number=i,
                        column=0,
                        file_path=str(file_path) if file_path else None,
                        suggestion=self._get_performance_suggestion(pattern_name),
                        rule_id=f"P{hash(pattern_name) % 1000:03d}"
                    ))
        
        return issues
    
    def _validate_change_specific(self, original: str, modified: str, 
                                file_path: Optional[Path]) -> List[ValidationIssue]:
        """Validate change-specific issues."""
        issues = []
        
        # Check if change introduces breaking changes
        try:
            original_tree = ast.parse(original)
            modified_tree = ast.parse(modified)
            
            # Check for removed public functions/classes
            original_public = self._extract_public_names(original_tree)
            modified_public = self._extract_public_names(modified_tree)
            
            removed_public = original_public - modified_public
            for name in removed_public:
                issues.append(ValidationIssue(
                    type=IssueType.COMPATIBILITY_ISSUE,
                    severity=IssueSeverity.WARNING,
                    message=f"Removed public API: {name}",
                    line_number=0,
                    column=None,
                    file_path=str(file_path) if file_path else None,
                    suggestion=f"Consider deprecating '{name}' instead of removing it",
                    rule_id="C001"
                ))
            
        except:
            pass  # Syntax errors already handled
        
        return issues
    
    def _check_docstrings(self, tree: ast.AST, file_path: Optional[Path]) -> List[ValidationIssue]:
        """Check for missing docstrings."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    node_type = "function" if isinstance(node, ast.FunctionDef) else "class"
                    
                    # Skip private functions/classes in basic validation
                    if self.validation_level == ValidationLevel.BASIC and node.name.startswith('_'):
                        continue
                    
                    issues.append(ValidationIssue(
                        type=IssueType.STYLE_VIOLATION,
                        severity=IssueSeverity.INFO,
                        message=f"Missing docstring for {node_type} '{node.name}'",
                        line_number=node.lineno,
                        column=node.col_offset,
                        file_path=str(file_path) if file_path else None,
                        suggestion=f"Add docstring to {node_type} '{node.name}'",
                        rule_id="D001"
                    ))
        
        return issues
    
    def _check_unreachable_code(self, tree: ast.AST, file_path: Optional[Path]) -> List[ValidationIssue]:
        """Check for unreachable code."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Simple check for code after return statements
                for i, stmt in enumerate(node.body):
                    if isinstance(stmt, ast.Return):
                        if i < len(node.body) - 1:
                            next_stmt = node.body[i + 1]
                            issues.append(ValidationIssue(
                                type=IssueType.LOGIC_ERROR,
                                severity=IssueSeverity.WARNING,
                                message="Unreachable code after return statement",
                                line_number=next_stmt.lineno,
                                column=next_stmt.col_offset,
                                file_path=str(file_path) if file_path else None,
                                suggestion="Remove unreachable code or restructure logic",
                                rule_id="L001"
                            ))
        
        return issues
    
    def _check_complexity(self, tree: ast.AST, file_path: Optional[Path]) -> List[ValidationIssue]:
        """Check cyclomatic complexity."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity = self._calculate_complexity(node)
                if complexity > self.max_complexity:
                    issues.append(ValidationIssue(
                        type=IssueType.LOGIC_ERROR,
                        severity=IssueSeverity.WARNING,
                        message=f"High complexity: {complexity} (max: {self.max_complexity})",
                        line_number=node.lineno,
                        column=node.col_offset,
                        file_path=str(file_path) if file_path else None,
                        suggestion=f"Consider breaking down function '{node.name}' into smaller functions",
                        rule_id="L002"
                    ))
        
        return issues
    
    def _check_potential_bugs(self, tree: ast.AST, file_path: Optional[Path]) -> List[ValidationIssue]:
        """Check for potential bugs."""
        issues = []
        
        for node in ast.walk(tree):
            # Check for mutable default arguments
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for arg in node.args.defaults:
                    if isinstance(arg, (ast.List, ast.Dict, ast.Set)):
                        issues.append(ValidationIssue(
                            type=IssueType.LOGIC_ERROR,
                            severity=IssueSeverity.WARNING,
                            message="Mutable default argument",
                            line_number=node.lineno,
                            column=node.col_offset,
                            file_path=str(file_path) if file_path else None,
                            suggestion="Use None as default and create mutable object inside function",
                            rule_id="L003"
                        ))
        
        return issues
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _extract_public_names(self, tree: ast.AST) -> Set[str]:
        """Extract public function and class names."""
        names = set()
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not node.name.startswith('_'):
                    names.add(node.name)
        
        return names
    
    def _calculate_quality_score(self, code: str, issues: List[ValidationIssue]) -> float:
        """Calculate a quality score based on issues found."""
        if not code.strip():
            return 0.0
        
        # Base score
        score = 100.0
        
        # Deduct points based on issue severity
        for issue in issues:
            if issue.severity == IssueSeverity.ERROR:
                score -= 20
            elif issue.severity == IssueSeverity.WARNING:
                score -= 10
            elif issue.severity == IssueSeverity.INFO:
                score -= 5
            elif issue.severity == IssueSeverity.SUGGESTION:
                score -= 2
        
        # Ensure score doesn't go below 0
        return max(0.0, score)
    
    def _create_summary(self, issues: List[ValidationIssue]) -> Dict[str, int]:
        """Create a summary of issues by type and severity."""
        summary = {
            'total': len(issues),
            'errors': 0,
            'warnings': 0,
            'info': 0,
            'suggestions': 0
        }
        
        for issue in issues:
            if issue.severity == IssueSeverity.ERROR:
                summary['errors'] += 1
            elif issue.severity == IssueSeverity.WARNING:
                summary['warnings'] += 1
            elif issue.severity == IssueSeverity.INFO:
                summary['info'] += 1
            elif issue.severity == IssueSeverity.SUGGESTION:
                summary['suggestions'] += 1
        
        return summary
    
    def _generate_suggestions(self, issues: List[ValidationIssue]) -> List[str]:
        """Generate general improvement suggestions."""
        suggestions = []
        
        # Extract unique suggestions from issues
        issue_suggestions = {issue.suggestion for issue in issues if issue.suggestion}
        suggestions.extend(issue_suggestions)
        
        # Add general suggestions based on issue patterns
        error_count = sum(1 for issue in issues if issue.severity == IssueSeverity.ERROR)
        warning_count = sum(1 for issue in issues if issue.severity == IssueSeverity.WARNING)
        
        if error_count > 0:
            suggestions.append("Fix syntax errors before proceeding")
        
        if warning_count > 5:
            suggestions.append("Consider addressing warnings to improve code quality")
        
        # Security suggestions
        security_issues = [issue for issue in issues if issue.type == IssueType.SECURITY_ISSUE]
        if security_issues:
            suggestions.append("Review and address security issues immediately")
        
        return list(set(suggestions))  # Remove duplicates
    
    def _get_security_suggestion(self, pattern_name: str) -> str:
        """Get security-specific suggestions."""
        suggestions = {
            'eval_usage': "Avoid using eval(). Consider ast.literal_eval() for safe evaluation",
            'exec_usage': "Avoid using exec(). Consider alternative approaches",
            'shell_injection': "Avoid shell=True. Use list arguments instead",
            'sql_injection': "Use parameterized queries to prevent SQL injection",
            'hardcoded_password': "Store passwords securely, not in source code",
            'hardcoded_secret': "Store secrets in environment variables or secure vaults"
        }
        return suggestions.get(pattern_name, "Review for security implications")
    
    def _get_performance_suggestion(self, pattern_name: str) -> str:
        """Get performance-specific suggestions."""
        suggestions = {
            'string_concatenation_loop': "Use ''.join() for string concatenation in loops",
            'inefficient_membership': "Use sets for membership testing instead of lists",
            'global_in_loop': "Avoid global variable access in tight loops",
            'repeated_computation': "Cache repeated computations outside loops"
        }
        return suggestions.get(pattern_name, "Consider optimizing for better performance")
    
    def run_external_linter(self, code: str, linter: str = 'flake8') -> List[ValidationIssue]:
        """Run external linter and parse results."""
        issues = []
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            if linter == 'flake8':
                result = subprocess.run(
                    ['flake8', '--format=%(path)s:%(row)d:%(col)d: %(code)s %(text)s', temp_file],
                    capture_output=True,
                    text=True
                )
                
                for line in result.stdout.split('\n'):
                    if line.strip():
                        parts = line.split(':', 3)
                        if len(parts) >= 4:
                            line_num = int(parts[1])
                            col_num = int(parts[2])
                            message = parts[3].strip()
                            
                            issues.append(ValidationIssue(
                                type=IssueType.STYLE_VIOLATION,
                                severity=IssueSeverity.WARNING,
                                message=message,
                                line_number=line_num,
                                column=col_num,
                                file_path=None,
                                rule_id=message.split()[0] if message else None
                            ))
            
            # Clean up temp file
            Path(temp_file).unlink()
            
        except (subprocess.SubprocessError, FileNotFoundError):
            # Linter not available or failed
            pass
        
        return issues