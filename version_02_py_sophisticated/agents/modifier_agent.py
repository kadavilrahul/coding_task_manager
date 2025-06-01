"""
Modifier Agent for code modification and implementation tasks.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from pathlib import Path
import json
import re
from datetime import datetime
from enum import Enum

from ..utils.file_utils import FileUtils
from ..utils.ai_utils import AIUtils


class ModificationType(Enum):
    """Types of code modifications."""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    REFACTOR = "refactor"
    FIX = "fix"
    OPTIMIZE = "optimize"
    DOCUMENT = "document"


class ModificationScope(Enum):
    """Scope of modifications."""
    FILE = "file"
    FUNCTION = "function"
    CLASS = "class"
    MODULE = "module"
    PROJECT = "project"


class ModifierAgent:
    """Agent specialized in modifying and implementing code changes."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the modifier agent."""
        self.config = config
        self.modification_history = []
        self.backup_enabled = config.get("backup_enabled", True)
        self.validation_enabled = config.get("validation_enabled", True)
        
        # Language-specific configurations
        self.language_configs = {
            'python': {
                'file_extension': '.py',
                'comment_style': '#',
                'indent_style': '    ',  # 4 spaces
                'line_ending': '\n'
            },
            'javascript': {
                'file_extension': '.js',
                'comment_style': '//',
                'indent_style': '  ',  # 2 spaces
                'line_ending': '\n'
            },
            'typescript': {
                'file_extension': '.ts',
                'comment_style': '//',
                'indent_style': '  ',  # 2 spaces
                'line_ending': '\n'
            },
            'java': {
                'file_extension': '.java',
                'comment_style': '//',
                'indent_style': '    ',  # 4 spaces
                'line_ending': '\n'
            },
            'cpp': {
                'file_extension': '.cpp',
                'comment_style': '//',
                'indent_style': '    ',  # 4 spaces
                'line_ending': '\n'
            }
        }
    
    def create_file(self, file_path: Path, content: str, language: str = 'python') -> Dict[str, Any]:
        """Create a new file with the specified content."""
        result = {
            'operation': ModificationType.CREATE.value,
            'file_path': str(file_path),
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'message': '',
            'changes': []
        }
        
        try:
            # Check if file already exists
            if FileUtils.file_exists(file_path):
                result['message'] = f"File {file_path} already exists"
                return result
            
            # Format content according to language conventions
            formatted_content = self._format_content(content, language)
            
            # Add file header if configured
            if self.config.get("add_file_headers", True):
                header = self._generate_file_header(file_path, language)
                formatted_content = header + formatted_content
            
            # Create the file
            FileUtils.write_file(file_path, formatted_content)
            
            # Record the modification
            modification = {
                'type': ModificationType.CREATE.value,
                'file_path': str(file_path),
                'timestamp': datetime.now().isoformat(),
                'content_length': len(formatted_content),
                'language': language
            }
            
            self.modification_history.append(modification)
            
            result['success'] = True
            result['message'] = f"Successfully created file {file_path}"
            result['changes'] = [modification]
            
            return result
        
        except Exception as e:
            result['message'] = f"Failed to create file {file_path}: {e}"
            return result
    
    def update_file(self, file_path: Path, modifications: List[Dict[str, Any]], 
                   language: Optional[str] = None) -> Dict[str, Any]:
        """Update an existing file with specified modifications."""
        result = {
            'operation': ModificationType.UPDATE.value,
            'file_path': str(file_path),
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'message': '',
            'changes': [],
            'backup_path': None
        }
        
        try:
            # Check if file exists
            if not FileUtils.file_exists(file_path):
                result['message'] = f"File {file_path} does not exist"
                return result
            
            # Create backup if enabled
            if self.backup_enabled:
                backup_path = FileUtils.backup_file(file_path)
                result['backup_path'] = str(backup_path)
            
            # Read current content
            current_content = FileUtils.read_file(file_path)
            
            # Detect language if not provided
            if language is None:
                language = self._detect_language(file_path)
            
            # Apply modifications
            modified_content = current_content
            applied_changes = []
            
            for modification in modifications:
                mod_result = self._apply_modification(modified_content, modification, language)
                if mod_result['success']:
                    modified_content = mod_result['content']
                    applied_changes.append(mod_result['change'])
                else:
                    # If any modification fails, restore from backup and return error
                    if self.backup_enabled and result['backup_path']:
                        FileUtils.copy_file(result['backup_path'], file_path)
                    result['message'] = f"Modification failed: {mod_result['message']}"
                    return result
            
            # Validate the modified content if enabled
            if self.validation_enabled:
                validation_result = self._validate_content(modified_content, language)
                if not validation_result['valid']:
                    if self.backup_enabled and result['backup_path']:
                        FileUtils.copy_file(result['backup_path'], file_path)
                    result['message'] = f"Validation failed: {', '.join(validation_result['issues'])}"
                    return result
            
            # Write the modified content
            FileUtils.write_file(file_path, modified_content)
            
            # Record the modifications
            for change in applied_changes:
                change['file_path'] = str(file_path)
                change['timestamp'] = datetime.now().isoformat()
                self.modification_history.append(change)
            
            result['success'] = True
            result['message'] = f"Successfully updated file {file_path}"
            result['changes'] = applied_changes
            
            return result
        
        except Exception as e:
            # Restore from backup if something went wrong
            if self.backup_enabled and result['backup_path']:
                try:
                    FileUtils.copy_file(result['backup_path'], file_path)
                except:
                    pass
            
            result['message'] = f"Failed to update file {file_path}: {e}"
            return result
    
    def _apply_modification(self, content: str, modification: Dict[str, Any], 
                          language: str) -> Dict[str, Any]:
        """Apply a single modification to content."""
        mod_type = modification.get('type', 'replace')
        
        if mod_type == 'replace':
            return self._apply_replace_modification(content, modification, language)
        elif mod_type == 'insert':
            return self._apply_insert_modification(content, modification, language)
        elif mod_type == 'delete':
            return self._apply_delete_modification(content, modification, language)
        elif mod_type == 'append':
            return self._apply_append_modification(content, modification, language)
        elif mod_type == 'prepend':
            return self._apply_prepend_modification(content, modification, language)
        else:
            return {
                'success': False,
                'message': f"Unknown modification type: {mod_type}",
                'content': content,
                'change': {}
            }
    
    def _apply_replace_modification(self, content: str, modification: Dict[str, Any], 
                                  language: str) -> Dict[str, Any]:
        """Apply a replace modification."""
        old_text = modification.get('old_text', '')
        new_text = modification.get('new_text', '')
        
        if not old_text:
            return {
                'success': False,
                'message': "Replace modification requires 'old_text'",
                'content': content,
                'change': {}
            }
        
        if old_text not in content:
            return {
                'success': False,
                'message': f"Text to replace not found: {old_text[:50]}...",
                'content': content,
                'change': {}
            }
        
        # Count occurrences
        occurrences = content.count(old_text)
        if occurrences > 1:
            # If multiple occurrences, be more specific
            return {
                'success': False,
                'message': f"Multiple occurrences found ({occurrences}). Please be more specific.",
                'content': content,
                'change': {}
            }
        
        # Format new text according to language conventions
        formatted_new_text = self._format_content(new_text, language)
        
        # Apply replacement
        new_content = content.replace(old_text, formatted_new_text)
        
        change = {
            'type': 'replace',
            'old_text': old_text,
            'new_text': formatted_new_text,
            'line_number': self._find_line_number(content, old_text)
        }
        
        return {
            'success': True,
            'message': "Replace modification applied successfully",
            'content': new_content,
            'change': change
        }
    
    def _apply_insert_modification(self, content: str, modification: Dict[str, Any], 
                                 language: str) -> Dict[str, Any]:
        """Apply an insert modification."""
        insert_text = modification.get('text', '')
        line_number = modification.get('line_number')
        after_text = modification.get('after_text')
        
        if not insert_text:
            return {
                'success': False,
                'message': "Insert modification requires 'text'",
                'content': content,
                'change': {}
            }
        
        lines = content.split('\n')
        
        # Format insert text
        formatted_text = self._format_content(insert_text, language)
        
        if line_number is not None:
            # Insert at specific line number
            if 0 <= line_number <= len(lines):
                lines.insert(line_number, formatted_text)
                new_content = '\n'.join(lines)
                
                change = {
                    'type': 'insert',
                    'text': formatted_text,
                    'line_number': line_number
                }
                
                return {
                    'success': True,
                    'message': f"Text inserted at line {line_number}",
                    'content': new_content,
                    'change': change
                }
            else:
                return {
                    'success': False,
                    'message': f"Invalid line number: {line_number}",
                    'content': content,
                    'change': {}
                }
        
        elif after_text:
            # Insert after specific text
            if after_text in content:
                new_content = content.replace(after_text, after_text + '\n' + formatted_text)
                
                change = {
                    'type': 'insert',
                    'text': formatted_text,
                    'after_text': after_text,
                    'line_number': self._find_line_number(content, after_text)
                }
                
                return {
                    'success': True,
                    'message': f"Text inserted after: {after_text[:30]}...",
                    'content': new_content,
                    'change': change
                }
            else:
                return {
                    'success': False,
                    'message': f"Reference text not found: {after_text[:50]}...",
                    'content': content,
                    'change': {}
                }
        
        else:
            return {
                'success': False,
                'message': "Insert modification requires 'line_number' or 'after_text'",
                'content': content,
                'change': {}
            }
    
    def _apply_delete_modification(self, content: str, modification: Dict[str, Any], 
                                 language: str) -> Dict[str, Any]:
        """Apply a delete modification."""
        delete_text = modification.get('text', '')
        line_number = modification.get('line_number')
        line_range = modification.get('line_range')
        
        if delete_text:
            # Delete specific text
            if delete_text not in content:
                return {
                    'success': False,
                    'message': f"Text to delete not found: {delete_text[:50]}...",
                    'content': content,
                    'change': {}
                }
            
            new_content = content.replace(delete_text, '')
            
            change = {
                'type': 'delete',
                'deleted_text': delete_text,
                'line_number': self._find_line_number(content, delete_text)
            }
            
            return {
                'success': True,
                'message': "Text deleted successfully",
                'content': new_content,
                'change': change
            }
        
        elif line_number is not None:
            # Delete specific line
            lines = content.split('\n')
            if 0 <= line_number < len(lines):
                deleted_line = lines.pop(line_number)
                new_content = '\n'.join(lines)
                
                change = {
                    'type': 'delete',
                    'deleted_text': deleted_line,
                    'line_number': line_number
                }
                
                return {
                    'success': True,
                    'message': f"Line {line_number} deleted successfully",
                    'content': new_content,
                    'change': change
                }
            else:
                return {
                    'success': False,
                    'message': f"Invalid line number: {line_number}",
                    'content': content,
                    'change': {}
                }
        
        elif line_range:
            # Delete range of lines
            start_line, end_line = line_range
            lines = content.split('\n')
            
            if 0 <= start_line < len(lines) and 0 <= end_line < len(lines) and start_line <= end_line:
                deleted_lines = lines[start_line:end_line + 1]
                del lines[start_line:end_line + 1]
                new_content = '\n'.join(lines)
                
                change = {
                    'type': 'delete',
                    'deleted_text': '\n'.join(deleted_lines),
                    'line_range': line_range
                }
                
                return {
                    'success': True,
                    'message': f"Lines {start_line}-{end_line} deleted successfully",
                    'content': new_content,
                    'change': change
                }
            else:
                return {
                    'success': False,
                    'message': f"Invalid line range: {line_range}",
                    'content': content,
                    'change': {}
                }
        
        else:
            return {
                'success': False,
                'message': "Delete modification requires 'text', 'line_number', or 'line_range'",
                'content': content,
                'change': {}
            }
    
    def _apply_append_modification(self, content: str, modification: Dict[str, Any], 
                                 language: str) -> Dict[str, Any]:
        """Apply an append modification."""
        append_text = modification.get('text', '')
        
        if not append_text:
            return {
                'success': False,
                'message': "Append modification requires 'text'",
                'content': content,
                'change': {}
            }
        
        # Format append text
        formatted_text = self._format_content(append_text, language)
        
        # Add newline if content doesn't end with one
        if content and not content.endswith('\n'):
            new_content = content + '\n' + formatted_text
        else:
            new_content = content + formatted_text
        
        change = {
            'type': 'append',
            'text': formatted_text,
            'line_number': len(content.split('\n'))
        }
        
        return {
            'success': True,
            'message': "Text appended successfully",
            'content': new_content,
            'change': change
        }
    
    def _apply_prepend_modification(self, content: str, modification: Dict[str, Any], 
                                  language: str) -> Dict[str, Any]:
        """Apply a prepend modification."""
        prepend_text = modification.get('text', '')
        
        if not prepend_text:
            return {
                'success': False,
                'message': "Prepend modification requires 'text'",
                'content': content,
                'change': {}
            }
        
        # Format prepend text
        formatted_text = self._format_content(prepend_text, language)
        
        # Add newline if formatted text doesn't end with one
        if not formatted_text.endswith('\n'):
            new_content = formatted_text + '\n' + content
        else:
            new_content = formatted_text + content
        
        change = {
            'type': 'prepend',
            'text': formatted_text,
            'line_number': 0
        }
        
        return {
            'success': True,
            'message': "Text prepended successfully",
            'content': new_content,
            'change': change
        }
    
    def _format_content(self, content: str, language: str) -> str:
        """Format content according to language conventions."""
        if language not in self.language_configs:
            return content
        
        config = self.language_configs[language]
        
        # Normalize line endings
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        # Apply indentation (basic formatting)
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Preserve existing indentation structure but normalize indent style
            stripped = line.lstrip()
            if stripped:
                # Count leading whitespace
                indent_count = len(line) - len(stripped)
                # Convert to language-specific indentation
                if language == 'python':
                    # Python uses 4 spaces
                    new_indent = '    ' * (indent_count // 4)
                elif language in ['javascript', 'typescript']:
                    # JS/TS typically use 2 spaces
                    new_indent = '  ' * (indent_count // 2)
                else:
                    # Default to 4 spaces
                    new_indent = '    ' * (indent_count // 4)
                
                formatted_lines.append(new_indent + stripped)
            else:
                formatted_lines.append('')
        
        return '\n'.join(formatted_lines)
    
    def _generate_file_header(self, file_path: Path, language: str) -> str:
        """Generate a file header comment."""
        if language not in self.language_configs:
            return ''
        
        config = self.language_configs[language]
        comment_style = config['comment_style']
        
        header_lines = [
            f"{comment_style} File: {file_path.name}",
            f"{comment_style} Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"{comment_style} Description: Auto-generated file",
            ""
        ]
        
        return '\n'.join(header_lines)
    
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
        
        return extension_map.get(extension, 'text')
    
    def _find_line_number(self, content: str, text: str) -> int:
        """Find the line number where text appears."""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if text in line:
                return i
        return -1
    
    def _validate_content(self, content: str, language: str) -> Dict[str, Any]:
        """Validate content for basic syntax issues."""
        validation = {
            'valid': True,
            'issues': []
        }
        
        if language == 'python':
            validation = self._validate_python_content(content)
        elif language in ['javascript', 'typescript']:
            validation = self._validate_js_content(content)
        elif language == 'json':
            validation = self._validate_json_content(content)
        
        return validation
    
    def _validate_python_content(self, content: str) -> Dict[str, Any]:
        """Validate Python content."""
        validation = {
            'valid': True,
            'issues': []
        }
        
        try:
            # Try to compile the Python code
            compile(content, '<string>', 'exec')
        except SyntaxError as e:
            validation['valid'] = False
            validation['issues'].append(f"Syntax error: {e}")
        except Exception as e:
            validation['valid'] = False
            validation['issues'].append(f"Compilation error: {e}")
        
        # Check for basic style issues
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for tabs (PEP 8 recommends spaces)
            if '\t' in line:
                validation['issues'].append(f"Line {i}: Contains tabs (use spaces)")
            
            # Check line length (PEP 8 recommends max 79 characters)
            if len(line) > 100:  # Being lenient
                validation['issues'].append(f"Line {i}: Line too long ({len(line)} characters)")
        
        return validation
    
    def _validate_js_content(self, content: str) -> Dict[str, Any]:
        """Validate JavaScript/TypeScript content."""
        validation = {
            'valid': True,
            'issues': []
        }
        
        # Basic syntax checks
        lines = content.split('\n')
        brace_count = 0
        paren_count = 0
        bracket_count = 0
        
        for i, line in enumerate(lines, 1):
            # Count braces, parentheses, and brackets
            brace_count += line.count('{') - line.count('}')
            paren_count += line.count('(') - line.count(')')
            bracket_count += line.count('[') - line.count(']')
            
            # Check for common issues
            if line.strip().endswith(',}'):
                validation['issues'].append(f"Line {i}: Trailing comma before closing brace")
        
        # Check for unmatched braces/parentheses
        if brace_count != 0:
            validation['valid'] = False
            validation['issues'].append("Unmatched braces")
        
        if paren_count != 0:
            validation['valid'] = False
            validation['issues'].append("Unmatched parentheses")
        
        if bracket_count != 0:
            validation['valid'] = False
            validation['issues'].append("Unmatched brackets")
        
        return validation
    
    def _validate_json_content(self, content: str) -> Dict[str, Any]:
        """Validate JSON content."""
        validation = {
            'valid': True,
            'issues': []
        }
        
        try:
            json.loads(content)
        except json.JSONDecodeError as e:
            validation['valid'] = False
            validation['issues'].append(f"JSON syntax error: {e}")
        
        return validation
    
    def refactor_code(self, file_path: Path, refactor_type: str, 
                     target: Optional[str] = None) -> Dict[str, Any]:
        """Refactor code in a file."""
        result = {
            'operation': ModificationType.REFACTOR.value,
            'file_path': str(file_path),
            'refactor_type': refactor_type,
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'message': '',
            'changes': []
        }
        
        try:
            if not FileUtils.file_exists(file_path):
                result['message'] = f"File {file_path} does not exist"
                return result
            
            # Create backup
            if self.backup_enabled:
                backup_path = FileUtils.backup_file(file_path)
                result['backup_path'] = str(backup_path)
            
            content = FileUtils.read_file(file_path)
            language = self._detect_language(file_path)
            
            # Apply refactoring based on type
            if refactor_type == 'extract_function':
                refactored_content = self._extract_function(content, target, language)
            elif refactor_type == 'rename_variable':
                refactored_content = self._rename_variable(content, target, language)
            elif refactor_type == 'optimize_imports':
                refactored_content = self._optimize_imports(content, language)
            elif refactor_type == 'format_code':
                refactored_content = self._format_code(content, language)
            else:
                result['message'] = f"Unknown refactor type: {refactor_type}"
                return result
            
            # Write refactored content
            FileUtils.write_file(file_path, refactored_content)
            
            # Record the change
            change = {
                'type': ModificationType.REFACTOR.value,
                'refactor_type': refactor_type,
                'file_path': str(file_path),
                'timestamp': datetime.now().isoformat()
            }
            
            self.modification_history.append(change)
            
            result['success'] = True
            result['message'] = f"Successfully applied {refactor_type} refactoring"
            result['changes'] = [change]
            
            return result
        
        except Exception as e:
            result['message'] = f"Refactoring failed: {e}"
            return result
    
    def _extract_function(self, content: str, target: str, language: str) -> str:
        """Extract code into a new function."""
        # This is a simplified implementation
        # In practice, this would require more sophisticated AST manipulation
        
        if not target:
            return content
        
        # For now, just add a comment indicating where extraction would happen
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if target in line:
                lines.insert(i, f"# TODO: Extract function for: {target}")
                break
        
        return '\n'.join(lines)
    
    def _rename_variable(self, content: str, target: str, language: str) -> str:
        """Rename a variable throughout the code."""
        if not target or '=' not in target:
            return content
        
        old_name, new_name = target.split('=', 1)
        old_name = old_name.strip()
        new_name = new_name.strip()
        
        # Simple word boundary replacement
        import re
        pattern = r'\b' + re.escape(old_name) + r'\b'
        return re.sub(pattern, new_name, content)
    
    def _optimize_imports(self, content: str, language: str) -> str:
        """Optimize import statements."""
        if language != 'python':
            return content
        
        lines = content.split('\n')
        import_lines = []
        other_lines = []
        
        for line in lines:
            if line.strip().startswith(('import ', 'from ')):
                import_lines.append(line)
            else:
                other_lines.append(line)
        
        # Sort imports
        import_lines.sort()
        
        # Remove duplicates
        unique_imports = []
        seen = set()
        for imp in import_lines:
            if imp not in seen:
                unique_imports.append(imp)
                seen.add(imp)
        
        # Combine back
        if unique_imports and other_lines:
            return '\n'.join(unique_imports + [''] + other_lines)
        else:
            return '\n'.join(unique_imports + other_lines)
    
    def _format_code(self, content: str, language: str) -> str:
        """Format code according to language conventions."""
        return self._format_content(content, language)
    
    def get_modification_history(self, file_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Get modification history, optionally filtered by file."""
        if file_path:
            return [mod for mod in self.modification_history 
                   if mod.get('file_path') == str(file_path)]
        return self.modification_history.copy()
    
    def undo_last_modification(self, file_path: Path) -> Dict[str, Any]:
        """Undo the last modification to a file."""
        result = {
            'operation': 'undo',
            'file_path': str(file_path),
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'message': ''
        }
        
        # Find the most recent modification for this file
        file_modifications = [mod for mod in self.modification_history 
                            if mod.get('file_path') == str(file_path)]
        
        if not file_modifications:
            result['message'] = f"No modifications found for {file_path}"
            return result
        
        last_modification = file_modifications[-1]
        
        # Look for backup file
        backup_dir = file_path.parent / "backups"
        if backup_dir.exists():
            backup_files = list(backup_dir.glob(f"{file_path.stem}_*{file_path.suffix}"))
            if backup_files:
                # Get the most recent backup
                latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
                
                try:
                    # Restore from backup
                    FileUtils.copy_file(latest_backup, file_path)
                    
                    # Remove the last modification from history
                    self.modification_history.remove(last_modification)
                    
                    result['success'] = True
                    result['message'] = f"Successfully undid last modification to {file_path}"
                    
                except Exception as e:
                    result['message'] = f"Failed to restore from backup: {e}"
            else:
                result['message'] = f"No backup files found for {file_path}"
        else:
            result['message'] = f"No backup directory found for {file_path}"
        
        return result
    
    def generate_modification_summary(self, modifications: List[Dict[str, Any]]) -> str:
        """Generate a human-readable summary of modifications."""
        if not modifications:
            return "No modifications performed."
        
        summary_parts = [
            f"Modification Summary ({len(modifications)} changes):",
            ""
        ]
        
        # Group by file
        files = {}
        for mod in modifications:
            file_path = mod.get('file_path', 'unknown')
            if file_path not in files:
                files[file_path] = []
            files[file_path].append(mod)
        
        for file_path, file_mods in files.items():
            summary_parts.append(f"File: {file_path}")
            
            for mod in file_mods:
                mod_type = mod.get('type', 'unknown')
                timestamp = mod.get('timestamp', '')
                
                if mod_type == 'create':
                    summary_parts.append(f"  - Created file ({timestamp})")
                elif mod_type == 'replace':
                    old_text = mod.get('old_text', '')[:30]
                    summary_parts.append(f"  - Replaced text: {old_text}... ({timestamp})")
                elif mod_type == 'insert':
                    line_num = mod.get('line_number', 'unknown')
                    summary_parts.append(f"  - Inserted text at line {line_num} ({timestamp})")
                elif mod_type == 'delete':
                    line_num = mod.get('line_number', 'unknown')
                    summary_parts.append(f"  - Deleted text at line {line_num} ({timestamp})")
                else:
                    summary_parts.append(f"  - {mod_type.title()} modification ({timestamp})")
            
            summary_parts.append("")
        
        return '\n'.join(summary_parts)