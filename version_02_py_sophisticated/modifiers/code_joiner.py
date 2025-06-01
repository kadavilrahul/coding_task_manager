"""
Intelligent code merging and joining utilities.
"""

import re
import ast
from typing import Dict, Any, List, Optional, Tuple, Set
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from ..utils.file_utils import FileUtils


class MergeStrategy(Enum):
    """Code merging strategies."""
    APPEND = "append"
    PREPEND = "prepend"
    REPLACE = "replace"
    MERGE_FUNCTIONS = "merge_functions"
    MERGE_CLASSES = "merge_classes"
    MERGE_IMPORTS = "merge_imports"
    SMART_MERGE = "smart_merge"


class ConflictResolution(Enum):
    """Conflict resolution strategies."""
    KEEP_ORIGINAL = "keep_original"
    KEEP_NEW = "keep_new"
    MERGE_BOTH = "merge_both"
    ASK_USER = "ask_user"
    AUTO_RESOLVE = "auto_resolve"


@dataclass
class MergeConflict:
    """Represents a merge conflict."""
    type: str
    original_content: str
    new_content: str
    line_number: int
    description: str
    suggested_resolution: ConflictResolution


@dataclass
class MergeResult:
    """Result of a merge operation."""
    success: bool
    merged_content: str
    conflicts: List[MergeConflict]
    changes_made: List[str]
    warnings: List[str]


class CodeJoiner:
    """Intelligent code merging and joining utilities."""
    
    def __init__(self):
        """Initialize the code joiner."""
        self.conflict_resolution = ConflictResolution.AUTO_RESOLVE
        self.preserve_formatting = True
        self.merge_comments = True
        
        # Patterns for different code elements
        self.patterns = {
            'function': r'^\s*def\s+(\w+)\s*\(',
            'class': r'^\s*class\s+(\w+)\s*[\(:]',
            'import': r'^\s*(?:from\s+[\w.]+\s+)?import\s+',
            'assignment': r'^\s*(\w+)\s*=',
            'decorator': r'^\s*@\w+',
            'comment': r'^\s*#',
            'docstring': r'^\s*["\']{{3}}'
        }
    
    def merge_files(self, original_file: Path, new_file: Path, 
                   strategy: MergeStrategy = MergeStrategy.SMART_MERGE) -> MergeResult:
        """Merge two Python files intelligently."""
        if not FileUtils.file_exists(original_file):
            return MergeResult(
                success=False,
                merged_content="",
                conflicts=[],
                changes_made=[],
                warnings=[f"Original file not found: {original_file}"]
            )
        
        if not FileUtils.file_exists(new_file):
            return MergeResult(
                success=False,
                merged_content="",
                conflicts=[],
                changes_made=[],
                warnings=[f"New file not found: {new_file}"]
            )
        
        original_content = FileUtils.read_file(original_file)
        new_content = FileUtils.read_file(new_file)
        
        return self.merge_content(original_content, new_content, strategy)
    
    def merge_content(self, original_content: str, new_content: str,
                     strategy: MergeStrategy = MergeStrategy.SMART_MERGE) -> MergeResult:
        """Merge two code contents using the specified strategy."""
        if strategy == MergeStrategy.APPEND:
            return self._append_merge(original_content, new_content)
        elif strategy == MergeStrategy.PREPEND:
            return self._prepend_merge(original_content, new_content)
        elif strategy == MergeStrategy.REPLACE:
            return self._replace_merge(original_content, new_content)
        elif strategy == MergeStrategy.MERGE_FUNCTIONS:
            return self._merge_functions(original_content, new_content)
        elif strategy == MergeStrategy.MERGE_CLASSES:
            return self._merge_classes(original_content, new_content)
        elif strategy == MergeStrategy.MERGE_IMPORTS:
            return self._merge_imports(original_content, new_content)
        elif strategy == MergeStrategy.SMART_MERGE:
            return self._smart_merge(original_content, new_content)
        else:
            return MergeResult(
                success=False,
                merged_content=original_content,
                conflicts=[],
                changes_made=[],
                warnings=[f"Unknown merge strategy: {strategy}"]
            )
    
    def _append_merge(self, original: str, new: str) -> MergeResult:
        """Simple append merge."""
        merged = original
        if not original.endswith('\n'):
            merged += '\n'
        merged += '\n' + new
        
        return MergeResult(
            success=True,
            merged_content=merged,
            conflicts=[],
            changes_made=["Appended new content to original"],
            warnings=[]
        )
    
    def _prepend_merge(self, original: str, new: str) -> MergeResult:
        """Simple prepend merge."""
        merged = new
        if not new.endswith('\n'):
            merged += '\n'
        merged += '\n' + original
        
        return MergeResult(
            success=True,
            merged_content=merged,
            conflicts=[],
            changes_made=["Prepended new content to original"],
            warnings=[]
        )
    
    def _replace_merge(self, original: str, new: str) -> MergeResult:
        """Replace original with new content."""
        return MergeResult(
            success=True,
            merged_content=new,
            conflicts=[],
            changes_made=["Replaced original content with new content"],
            warnings=[]
        )
    
    def _smart_merge(self, original: str, new: str) -> MergeResult:
        """Intelligent merge based on code structure."""
        try:
            # Parse both contents
            original_tree = ast.parse(original)
            new_tree = ast.parse(new)
        except SyntaxError as e:
            return MergeResult(
                success=False,
                merged_content=original,
                conflicts=[],
                changes_made=[],
                warnings=[f"Syntax error during parsing: {e}"]
            )
        
        # Extract elements from both files
        original_elements = self._extract_code_elements(original)
        new_elements = self._extract_code_elements(new)
        
        # Merge elements intelligently
        merged_elements = self._merge_elements(original_elements, new_elements)
        
        # Reconstruct the merged content
        merged_content = self._reconstruct_content(merged_elements)
        
        return MergeResult(
            success=True,
            merged_content=merged_content,
            conflicts=merged_elements.get('conflicts', []),
            changes_made=merged_elements.get('changes', []),
            warnings=merged_elements.get('warnings', [])
        )
    
    def _merge_functions(self, original: str, new: str) -> MergeResult:
        """Merge functions from both files."""
        original_functions = self._extract_functions(original)
        new_functions = self._extract_functions(new)
        
        conflicts = []
        changes = []
        merged_functions = original_functions.copy()
        
        for func_name, func_content in new_functions.items():
            if func_name in original_functions:
                # Function exists in both - potential conflict
                if original_functions[func_name] != func_content:
                    conflict = MergeConflict(
                        type="function_conflict",
                        original_content=original_functions[func_name],
                        new_content=func_content,
                        line_number=self._find_function_line(original, func_name),
                        description=f"Function '{func_name}' exists in both files with different implementations",
                        suggested_resolution=ConflictResolution.KEEP_NEW
                    )
                    conflicts.append(conflict)
                    
                    if self.conflict_resolution == ConflictResolution.KEEP_NEW:
                        merged_functions[func_name] = func_content
                        changes.append(f"Updated function '{func_name}'")
                    elif self.conflict_resolution == ConflictResolution.KEEP_ORIGINAL:
                        changes.append(f"Kept original function '{func_name}'")
            else:
                # New function
                merged_functions[func_name] = func_content
                changes.append(f"Added new function '{func_name}'")
        
        # Reconstruct content with merged functions
        merged_content = self._reconstruct_with_functions(original, merged_functions)
        
        return MergeResult(
            success=True,
            merged_content=merged_content,
            conflicts=conflicts,
            changes_made=changes,
            warnings=[]
        )
    
    def _merge_classes(self, original: str, new: str) -> MergeResult:
        """Merge classes from both files."""
        original_classes = self._extract_classes(original)
        new_classes = self._extract_classes(new)
        
        conflicts = []
        changes = []
        merged_classes = original_classes.copy()
        
        for class_name, class_content in new_classes.items():
            if class_name in original_classes:
                # Class exists in both - merge methods
                merged_class, class_conflicts, class_changes = self._merge_class_methods(
                    original_classes[class_name], class_content, class_name
                )
                merged_classes[class_name] = merged_class
                conflicts.extend(class_conflicts)
                changes.extend(class_changes)
            else:
                # New class
                merged_classes[class_name] = class_content
                changes.append(f"Added new class '{class_name}'")
        
        # Reconstruct content with merged classes
        merged_content = self._reconstruct_with_classes(original, merged_classes)
        
        return MergeResult(
            success=True,
            merged_content=merged_content,
            conflicts=conflicts,
            changes_made=changes,
            warnings=[]
        )
    
    def _merge_imports(self, original: str, new: str) -> MergeResult:
        """Merge import statements from both files."""
        original_imports = self._extract_imports(original)
        new_imports = self._extract_imports(new)
        
        # Combine imports, removing duplicates
        all_imports = set(original_imports + new_imports)
        sorted_imports = sorted(all_imports)
        
        # Group imports
        stdlib_imports = []
        third_party_imports = []
        local_imports = []
        
        for imp in sorted_imports:
            if self._is_stdlib_import(imp):
                stdlib_imports.append(imp)
            elif self._is_local_import(imp):
                local_imports.append(imp)
            else:
                third_party_imports.append(imp)
        
        # Reconstruct import section
        import_lines = []
        if stdlib_imports:
            import_lines.extend(stdlib_imports)
            import_lines.append("")
        if third_party_imports:
            import_lines.extend(third_party_imports)
            import_lines.append("")
        if local_imports:
            import_lines.extend(local_imports)
            import_lines.append("")
        
        # Replace import section in original content
        merged_content = self._replace_import_section(original, import_lines)
        
        changes = []
        new_import_count = len(all_imports) - len(original_imports)
        if new_import_count > 0:
            changes.append(f"Added {new_import_count} new imports")
        
        return MergeResult(
            success=True,
            merged_content=merged_content,
            conflicts=[],
            changes_made=changes,
            warnings=[]
        )
    
    def _extract_code_elements(self, content: str) -> Dict[str, Any]:
        """Extract different code elements from content."""
        lines = content.split('\n')
        elements = {
            'imports': [],
            'functions': {},
            'classes': {},
            'variables': {},
            'comments': [],
            'other': []
        }
        
        current_element = None
        current_content = []
        
        for i, line in enumerate(lines):
            line_type = self._identify_line_type(line)
            
            if line_type == 'import':
                elements['imports'].append(line)
            elif line_type == 'function':
                if current_element:
                    self._save_current_element(elements, current_element, current_content)
                current_element = ('function', self._extract_function_name(line))
                current_content = [line]
            elif line_type == 'class':
                if current_element:
                    self._save_current_element(elements, current_element, current_content)
                current_element = ('class', self._extract_class_name(line))
                current_content = [line]
            elif line_type == 'assignment':
                var_name = self._extract_variable_name(line)
                elements['variables'][var_name] = line
            elif line_type == 'comment':
                elements['comments'].append(line)
            else:
                if current_element:
                    current_content.append(line)
                else:
                    elements['other'].append(line)
        
        # Save the last element
        if current_element:
            self._save_current_element(elements, current_element, current_content)
        
        return elements
    
    def _merge_elements(self, original_elements: Dict[str, Any], 
                       new_elements: Dict[str, Any]) -> Dict[str, Any]:
        """Merge code elements intelligently."""
        merged = {
            'imports': [],
            'functions': {},
            'classes': {},
            'variables': {},
            'comments': [],
            'other': [],
            'conflicts': [],
            'changes': [],
            'warnings': []
        }
        
        # Merge imports
        all_imports = set(original_elements['imports'] + new_elements['imports'])
        merged['imports'] = sorted(all_imports)
        if len(merged['imports']) > len(original_elements['imports']):
            merged['changes'].append(f"Added {len(merged['imports']) - len(original_elements['imports'])} new imports")
        
        # Merge functions
        merged['functions'] = original_elements['functions'].copy()
        for func_name, func_content in new_elements['functions'].items():
            if func_name in merged['functions']:
                if merged['functions'][func_name] != func_content:
                    # Conflict detected
                    conflict = MergeConflict(
                        type="function",
                        original_content=merged['functions'][func_name],
                        new_content=func_content,
                        line_number=0,  # Would need to calculate
                        description=f"Function '{func_name}' differs between files",
                        suggested_resolution=ConflictResolution.KEEP_NEW
                    )
                    merged['conflicts'].append(conflict)
                    
                    if self.conflict_resolution == ConflictResolution.KEEP_NEW:
                        merged['functions'][func_name] = func_content
                        merged['changes'].append(f"Updated function '{func_name}'")
            else:
                merged['functions'][func_name] = func_content
                merged['changes'].append(f"Added function '{func_name}'")
        
        # Merge classes (similar to functions)
        merged['classes'] = original_elements['classes'].copy()
        for class_name, class_content in new_elements['classes'].items():
            if class_name in merged['classes']:
                if merged['classes'][class_name] != class_content:
                    conflict = MergeConflict(
                        type="class",
                        original_content=merged['classes'][class_name],
                        new_content=class_content,
                        line_number=0,
                        description=f"Class '{class_name}' differs between files",
                        suggested_resolution=ConflictResolution.KEEP_NEW
                    )
                    merged['conflicts'].append(conflict)
                    
                    if self.conflict_resolution == ConflictResolution.KEEP_NEW:
                        merged['classes'][class_name] = class_content
                        merged['changes'].append(f"Updated class '{class_name}'")
            else:
                merged['classes'][class_name] = class_content
                merged['changes'].append(f"Added class '{class_name}'")
        
        # Merge variables
        merged['variables'] = original_elements['variables'].copy()
        for var_name, var_content in new_elements['variables'].items():
            if var_name in merged['variables']:
                if merged['variables'][var_name] != var_content:
                    merged['variables'][var_name] = var_content
                    merged['changes'].append(f"Updated variable '{var_name}'")
            else:
                merged['variables'][var_name] = var_content
                merged['changes'].append(f"Added variable '{var_name}'")
        
        # Merge comments and other content
        merged['comments'] = original_elements['comments'] + new_elements['comments']
        merged['other'] = original_elements['other'] + new_elements['other']
        
        return merged
    
    def _reconstruct_content(self, elements: Dict[str, Any]) -> str:
        """Reconstruct content from merged elements."""
        lines = []
        
        # Add imports
        if elements['imports']:
            lines.extend(elements['imports'])
            lines.append("")
        
        # Add variables
        if elements['variables']:
            for var_content in elements['variables'].values():
                lines.append(var_content)
            lines.append("")
        
        # Add functions
        if elements['functions']:
            for func_content in elements['functions'].values():
                if isinstance(func_content, list):
                    lines.extend(func_content)
                else:
                    lines.append(func_content)
                lines.append("")
        
        # Add classes
        if elements['classes']:
            for class_content in elements['classes'].values():
                if isinstance(class_content, list):
                    lines.extend(class_content)
                else:
                    lines.append(class_content)
                lines.append("")
        
        # Add other content
        if elements['other']:
            lines.extend(elements['other'])
        
        return '\n'.join(lines)
    
    def _identify_line_type(self, line: str) -> str:
        """Identify the type of a code line."""
        stripped = line.strip()
        
        if not stripped:
            return 'empty'
        
        for pattern_name, pattern in self.patterns.items():
            if re.match(pattern, line):
                return pattern_name
        
        return 'other'
    
    def _extract_function_name(self, line: str) -> str:
        """Extract function name from a function definition line."""
        match = re.match(r'^\s*def\s+(\w+)', line)
        return match.group(1) if match else 'unknown'
    
    def _extract_class_name(self, line: str) -> str:
        """Extract class name from a class definition line."""
        match = re.match(r'^\s*class\s+(\w+)', line)
        return match.group(1) if match else 'unknown'
    
    def _extract_variable_name(self, line: str) -> str:
        """Extract variable name from an assignment line."""
        match = re.match(r'^\s*(\w+)\s*=', line)
        return match.group(1) if match else 'unknown'
    
    def _save_current_element(self, elements: Dict[str, Any], 
                            current_element: Tuple[str, str], 
                            current_content: List[str]):
        """Save the current element to the elements dictionary."""
        element_type, element_name = current_element
        
        if element_type == 'function':
            elements['functions'][element_name] = current_content
        elif element_type == 'class':
            elements['classes'][element_name] = current_content
    
    def _extract_functions(self, content: str) -> Dict[str, str]:
        """Extract all functions from content."""
        functions = {}
        lines = content.split('\n')
        current_function = None
        current_content = []
        
        for line in lines:
            if re.match(r'^\s*def\s+\w+', line):
                if current_function:
                    functions[current_function] = '\n'.join(current_content)
                current_function = self._extract_function_name(line)
                current_content = [line]
            elif current_function:
                if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                    # End of function
                    functions[current_function] = '\n'.join(current_content)
                    current_function = None
                    current_content = []
                else:
                    current_content.append(line)
        
        if current_function:
            functions[current_function] = '\n'.join(current_content)
        
        return functions
    
    def _extract_classes(self, content: str) -> Dict[str, str]:
        """Extract all classes from content."""
        classes = {}
        lines = content.split('\n')
        current_class = None
        current_content = []
        
        for line in lines:
            if re.match(r'^\s*class\s+\w+', line):
                if current_class:
                    classes[current_class] = '\n'.join(current_content)
                current_class = self._extract_class_name(line)
                current_content = [line]
            elif current_class:
                if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                    # End of class
                    classes[current_class] = '\n'.join(current_content)
                    current_class = None
                    current_content = []
                else:
                    current_content.append(line)
        
        if current_class:
            classes[current_class] = '\n'.join(current_content)
        
        return classes
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract all import statements from content."""
        imports = []
        lines = content.split('\n')
        
        for line in lines:
            stripped = line.strip()
            if (stripped.startswith('import ') or 
                stripped.startswith('from ') and ' import ' in stripped):
                imports.append(line)
        
        return imports
    
    def _find_function_line(self, content: str, function_name: str) -> int:
        """Find the line number where a function is defined."""
        lines = content.split('\n')
        pattern = rf'^\s*def\s+{re.escape(function_name)}\s*\('
        
        for i, line in enumerate(lines):
            if re.match(pattern, line):
                return i + 1
        
        return 0
    
    def _merge_class_methods(self, original_class: str, new_class: str, 
                           class_name: str) -> Tuple[str, List[MergeConflict], List[str]]:
        """Merge methods within a class."""
        # This is a simplified implementation
        # In practice, you'd want to parse the class structure more carefully
        
        conflicts = []
        changes = []
        
        # For now, just use the new class if different
        if original_class != new_class:
            changes.append(f"Updated class '{class_name}'")
            return new_class, conflicts, changes
        
        return original_class, conflicts, changes
    
    def _reconstruct_with_functions(self, original: str, functions: Dict[str, str]) -> str:
        """Reconstruct content with merged functions."""
        # This is a simplified implementation
        # In practice, you'd want to preserve the original structure better
        
        lines = original.split('\n')
        result_lines = []
        skip_until_next_def = False
        
        for line in lines:
            if re.match(r'^\s*def\s+\w+', line):
                func_name = self._extract_function_name(line)
                if func_name in functions:
                    result_lines.append(functions[func_name])
                    skip_until_next_def = True
                else:
                    result_lines.append(line)
                    skip_until_next_def = False
            elif skip_until_next_def:
                if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                    skip_until_next_def = False
                    result_lines.append(line)
            else:
                result_lines.append(line)
        
        return '\n'.join(result_lines)
    
    def _reconstruct_with_classes(self, original: str, classes: Dict[str, str]) -> str:
        """Reconstruct content with merged classes."""
        # Similar to _reconstruct_with_functions but for classes
        lines = original.split('\n')
        result_lines = []
        skip_until_next_class = False
        
        for line in lines:
            if re.match(r'^\s*class\s+\w+', line):
                class_name = self._extract_class_name(line)
                if class_name in classes:
                    result_lines.append(classes[class_name])
                    skip_until_next_class = True
                else:
                    result_lines.append(line)
                    skip_until_next_class = False
            elif skip_until_next_class:
                if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                    skip_until_next_class = False
                    result_lines.append(line)
            else:
                result_lines.append(line)
        
        return '\n'.join(result_lines)
    
    def _is_stdlib_import(self, import_line: str) -> bool:
        """Check if an import is from the standard library."""
        stdlib_modules = {
            'os', 'sys', 'json', 'datetime', 'pathlib', 'typing', 're', 'collections',
            'itertools', 'functools', 'operator', 'math', 'random', 'string', 'time'
        }
        
        # Extract module name from import line
        if import_line.strip().startswith('import '):
            module = import_line.strip()[7:].split()[0].split('.')[0]
        elif import_line.strip().startswith('from '):
            module = import_line.strip().split()[1].split('.')[0]
        else:
            return False
        
        return module in stdlib_modules
    
    def _is_local_import(self, import_line: str) -> bool:
        """Check if an import is a local/relative import."""
        return import_line.strip().startswith('from .') or import_line.strip().startswith('from ..')
    
    def _replace_import_section(self, content: str, new_imports: List[str]) -> str:
        """Replace the import section of the content."""
        lines = content.split('\n')
        result_lines = []
        in_import_section = True
        import_section_added = False
        
        for line in lines:
            stripped = line.strip()
            
            if in_import_section:
                if (stripped.startswith('import ') or 
                    stripped.startswith('from ') or
                    not stripped or
                    stripped.startswith('#')):
                    # Skip original imports
                    if not import_section_added and stripped and not stripped.startswith('#'):
                        result_lines.extend(new_imports)
                        import_section_added = True
                    continue
                else:
                    # End of import section
                    in_import_section = False
                    if not import_section_added:
                        result_lines.extend(new_imports)
                        import_section_added = True
                    result_lines.append(line)
            else:
                result_lines.append(line)
        
        return '\n'.join(result_lines)