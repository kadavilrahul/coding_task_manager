"""
Smart line identification for precise code modifications.
"""

import re
from typing import Dict, Any, List, Optional, Tuple, Set
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from ..utils.file_utils import FileUtils


class MatchType(Enum):
    """Types of line matching."""
    EXACT = "exact"
    FUZZY = "fuzzy"
    PATTERN = "pattern"
    CONTEXT = "context"
    SEMANTIC = "semantic"


@dataclass
class LineMatch:
    """Represents a line match result."""
    line_number: int
    content: str
    match_type: MatchType
    confidence: float
    context_before: List[str]
    context_after: List[str]


@dataclass
class IdentificationResult:
    """Result of line identification."""
    matches: List[LineMatch]
    best_match: Optional[LineMatch]
    total_lines: int
    search_query: str
    success: bool


class LineIdentifier:
    """Smart line identification for code modifications."""
    
    def __init__(self):
        """Initialize the line identifier."""
        self.context_size = 3  # Number of lines before/after for context
        self.fuzzy_threshold = 0.7  # Minimum similarity for fuzzy matching
        
        # Common code patterns
        self.code_patterns = {
            'function_def': r'^\s*def\s+(\w+)\s*\(',
            'class_def': r'^\s*class\s+(\w+)\s*[\(:]',
            'import': r'^\s*(?:from\s+\w+\s+)?import\s+',
            'assignment': r'^\s*(\w+)\s*=',
            'if_statement': r'^\s*if\s+',
            'for_loop': r'^\s*for\s+',
            'while_loop': r'^\s*while\s+',
            'try_block': r'^\s*try\s*:',
            'except_block': r'^\s*except\s+',
            'comment': r'^\s*#',
            'docstring': r'^\s*["\']{{3}}'
        }
    
    def identify_line(self, file_path: Path, search_query: str, 
                     match_types: Optional[List[MatchType]] = None,
                     context_lines: int = 3) -> IdentificationResult:
        """Identify lines in a file based on search query."""
        if not FileUtils.file_exists(file_path):
            return IdentificationResult(
                matches=[],
                best_match=None,
                total_lines=0,
                search_query=search_query,
                success=False
            )
        
        content = FileUtils.read_file(file_path)
        lines = content.split('\n')
        
        if match_types is None:
            match_types = [MatchType.EXACT, MatchType.FUZZY, MatchType.PATTERN, MatchType.CONTEXT]
        
        self.context_size = context_lines
        matches = []
        
        # Try different matching strategies
        for match_type in match_types:
            if match_type == MatchType.EXACT:
                matches.extend(self._exact_match(lines, search_query))
            elif match_type == MatchType.FUZZY:
                matches.extend(self._fuzzy_match(lines, search_query))
            elif match_type == MatchType.PATTERN:
                matches.extend(self._pattern_match(lines, search_query))
            elif match_type == MatchType.CONTEXT:
                matches.extend(self._context_match(lines, search_query))
            elif match_type == MatchType.SEMANTIC:
                matches.extend(self._semantic_match(lines, search_query))
        
        # Remove duplicates and sort by confidence
        unique_matches = self._deduplicate_matches(matches)
        unique_matches.sort(key=lambda x: x.confidence, reverse=True)
        
        # Find best match
        best_match = unique_matches[0] if unique_matches else None
        
        return IdentificationResult(
            matches=unique_matches,
            best_match=best_match,
            total_lines=len(lines),
            search_query=search_query,
            success=len(unique_matches) > 0
        )
    
    def identify_function(self, file_path: Path, function_name: str) -> IdentificationResult:
        """Identify a specific function in the file."""
        pattern = rf'^\s*def\s+{re.escape(function_name)}\s*\('
        return self.identify_line(file_path, pattern, [MatchType.PATTERN])
    
    def identify_class(self, file_path: Path, class_name: str) -> IdentificationResult:
        """Identify a specific class in the file."""
        pattern = rf'^\s*class\s+{re.escape(class_name)}\s*[\(:]'
        return self.identify_line(file_path, pattern, [MatchType.PATTERN])
    
    def identify_import(self, file_path: Path, module_name: str) -> IdentificationResult:
        """Identify import statements for a specific module."""
        patterns = [
            rf'^\s*import\s+{re.escape(module_name)}',
            rf'^\s*from\s+{re.escape(module_name)}\s+import',
            rf'^\s*import\s+.*{re.escape(module_name)}'
        ]
        
        matches = []
        for pattern in patterns:
            result = self.identify_line(file_path, pattern, [MatchType.PATTERN])
            matches.extend(result.matches)
        
        unique_matches = self._deduplicate_matches(matches)
        unique_matches.sort(key=lambda x: x.confidence, reverse=True)
        
        return IdentificationResult(
            matches=unique_matches,
            best_match=unique_matches[0] if unique_matches else None,
            total_lines=0,  # Will be set properly in identify_line
            search_query=f"import {module_name}",
            success=len(unique_matches) > 0
        )
    
    def identify_variable_assignment(self, file_path: Path, variable_name: str) -> IdentificationResult:
        """Identify variable assignment lines."""
        pattern = rf'^\s*{re.escape(variable_name)}\s*='
        return self.identify_line(file_path, pattern, [MatchType.PATTERN])
    
    def identify_code_block(self, file_path: Path, start_pattern: str, 
                           end_pattern: Optional[str] = None) -> Dict[str, Any]:
        """Identify a code block between start and end patterns."""
        if not FileUtils.file_exists(file_path):
            return {'success': False, 'error': 'File not found'}
        
        content = FileUtils.read_file(file_path)
        lines = content.split('\n')
        
        # Find start line
        start_result = self.identify_line(file_path, start_pattern, [MatchType.PATTERN, MatchType.FUZZY])
        if not start_result.success:
            return {'success': False, 'error': 'Start pattern not found'}
        
        start_line = start_result.best_match.line_number
        
        if end_pattern:
            # Find end line
            end_result = self.identify_line(file_path, end_pattern, [MatchType.PATTERN, MatchType.FUZZY])
            if not end_result.success:
                return {'success': False, 'error': 'End pattern not found'}
            
            end_line = end_result.best_match.line_number
            if end_line <= start_line:
                return {'success': False, 'error': 'End line must be after start line'}
        else:
            # Auto-detect end based on indentation
            end_line = self._find_block_end(lines, start_line)
        
        block_lines = lines[start_line:end_line + 1]
        
        return {
            'success': True,
            'start_line': start_line,
            'end_line': end_line,
            'block_content': '\n'.join(block_lines),
            'line_count': len(block_lines)
        }
    
    def _exact_match(self, lines: List[str], search_query: str) -> List[LineMatch]:
        """Find exact matches."""
        matches = []
        
        for i, line in enumerate(lines):
            if search_query in line:
                matches.append(LineMatch(
                    line_number=i,
                    content=line,
                    match_type=MatchType.EXACT,
                    confidence=1.0,
                    context_before=self._get_context_before(lines, i),
                    context_after=self._get_context_after(lines, i)
                ))
        
        return matches
    
    def _fuzzy_match(self, lines: List[str], search_query: str) -> List[LineMatch]:
        """Find fuzzy matches using similarity."""
        matches = []
        
        for i, line in enumerate(lines):
            similarity = self._calculate_similarity(search_query, line)
            if similarity >= self.fuzzy_threshold:
                matches.append(LineMatch(
                    line_number=i,
                    content=line,
                    match_type=MatchType.FUZZY,
                    confidence=similarity,
                    context_before=self._get_context_before(lines, i),
                    context_after=self._get_context_after(lines, i)
                ))
        
        return matches
    
    def _pattern_match(self, lines: List[str], search_query: str) -> List[LineMatch]:
        """Find pattern matches using regex."""
        matches = []
        
        try:
            pattern = re.compile(search_query, re.IGNORECASE)
            
            for i, line in enumerate(lines):
                if pattern.search(line):
                    matches.append(LineMatch(
                        line_number=i,
                        content=line,
                        match_type=MatchType.PATTERN,
                        confidence=0.9,  # High confidence for pattern matches
                        context_before=self._get_context_before(lines, i),
                        context_after=self._get_context_after(lines, i)
                    ))
        
        except re.error:
            # Invalid regex pattern, fall back to exact match
            return self._exact_match(lines, search_query)
        
        return matches
    
    def _context_match(self, lines: List[str], search_query: str) -> List[LineMatch]:
        """Find matches based on context (surrounding lines)."""
        matches = []
        query_words = set(search_query.lower().split())
        
        for i, line in enumerate(lines):
            # Get context window
            context_start = max(0, i - self.context_size)
            context_end = min(len(lines), i + self.context_size + 1)
            context_lines = lines[context_start:context_end]
            
            # Calculate context similarity
            context_text = ' '.join(context_lines).lower()
            context_words = set(context_text.split())
            
            # Calculate overlap
            overlap = len(query_words.intersection(context_words))
            similarity = overlap / len(query_words) if query_words else 0
            
            if similarity >= 0.5:  # At least 50% word overlap
                matches.append(LineMatch(
                    line_number=i,
                    content=line,
                    match_type=MatchType.CONTEXT,
                    confidence=similarity,
                    context_before=self._get_context_before(lines, i),
                    context_after=self._get_context_after(lines, i)
                ))
        
        return matches
    
    def _semantic_match(self, lines: List[str], search_query: str) -> List[LineMatch]:
        """Find semantic matches based on code structure."""
        matches = []
        
        # Identify query type
        query_type = self._identify_query_type(search_query)
        
        for i, line in enumerate(lines):
            line_type = self._identify_line_type(line)
            
            # Match based on semantic similarity
            if query_type == line_type:
                confidence = 0.8
                
                # Additional scoring based on content similarity
                content_similarity = self._calculate_similarity(search_query, line)
                confidence = max(confidence, content_similarity)
                
                matches.append(LineMatch(
                    line_number=i,
                    content=line,
                    match_type=MatchType.SEMANTIC,
                    confidence=confidence,
                    context_before=self._get_context_before(lines, i),
                    context_after=self._get_context_after(lines, i)
                ))
        
        return matches
    
    def _identify_query_type(self, query: str) -> str:
        """Identify the type of code construct in the query."""
        for pattern_name, pattern in self.code_patterns.items():
            if re.search(pattern, query, re.IGNORECASE):
                return pattern_name
        return 'unknown'
    
    def _identify_line_type(self, line: str) -> str:
        """Identify the type of code construct in a line."""
        for pattern_name, pattern in self.code_patterns.items():
            if re.search(pattern, line):
                return pattern_name
        return 'unknown'
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two strings."""
        # Simple Jaccard similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _get_context_before(self, lines: List[str], line_number: int) -> List[str]:
        """Get context lines before the specified line."""
        start = max(0, line_number - self.context_size)
        return lines[start:line_number]
    
    def _get_context_after(self, lines: List[str], line_number: int) -> List[str]:
        """Get context lines after the specified line."""
        end = min(len(lines), line_number + self.context_size + 1)
        return lines[line_number + 1:end]
    
    def _deduplicate_matches(self, matches: List[LineMatch]) -> List[LineMatch]:
        """Remove duplicate matches (same line number)."""
        seen_lines = set()
        unique_matches = []
        
        for match in matches:
            if match.line_number not in seen_lines:
                seen_lines.add(match.line_number)
                unique_matches.append(match)
            else:
                # Keep the match with higher confidence
                existing_match = next(m for m in unique_matches if m.line_number == match.line_number)
                if match.confidence > existing_match.confidence:
                    unique_matches.remove(existing_match)
                    unique_matches.append(match)
        
        return unique_matches
    
    def _find_block_end(self, lines: List[str], start_line: int) -> int:
        """Find the end of a code block based on indentation."""
        if start_line >= len(lines):
            return start_line
        
        start_indent = self._get_indentation_level(lines[start_line])
        
        for i in range(start_line + 1, len(lines)):
            line = lines[i]
            
            # Skip empty lines
            if not line.strip():
                continue
            
            current_indent = self._get_indentation_level(line)
            
            # If we find a line with same or less indentation, we've found the end
            if current_indent <= start_indent:
                return i - 1
        
        # If we reach the end of file, return the last line
        return len(lines) - 1
    
    def _get_indentation_level(self, line: str) -> int:
        """Get the indentation level of a line."""
        return len(line) - len(line.lstrip())
    
    def find_insertion_point(self, file_path: Path, target_type: str, 
                           target_name: Optional[str] = None) -> Dict[str, Any]:
        """Find the best insertion point for new code."""
        if not FileUtils.file_exists(file_path):
            return {'success': False, 'error': 'File not found'}
        
        content = FileUtils.read_file(file_path)
        lines = content.split('\n')
        
        if target_type == 'function':
            return self._find_function_insertion_point(lines, target_name)
        elif target_type == 'class':
            return self._find_class_insertion_point(lines, target_name)
        elif target_type == 'import':
            return self._find_import_insertion_point(lines)
        elif target_type == 'end_of_file':
            return {'success': True, 'line_number': len(lines), 'context': 'end_of_file'}
        else:
            return {'success': False, 'error': f'Unknown target type: {target_type}'}
    
    def _find_function_insertion_point(self, lines: List[str], function_name: Optional[str]) -> Dict[str, Any]:
        """Find the best place to insert a new function."""
        # Look for existing functions
        function_lines = []
        for i, line in enumerate(lines):
            if re.match(r'^\s*def\s+\w+', line):
                function_lines.append(i)
        
        if not function_lines:
            # No functions found, insert after imports
            import_end = self._find_import_section_end(lines)
            return {
                'success': True,
                'line_number': import_end + 2,  # Leave a blank line
                'context': 'after_imports'
            }
        
        # Insert after the last function
        last_function_start = function_lines[-1]
        last_function_end = self._find_block_end(lines, last_function_start)
        
        return {
            'success': True,
            'line_number': last_function_end + 2,  # Leave a blank line
            'context': 'after_last_function'
        }
    
    def _find_class_insertion_point(self, lines: List[str], class_name: Optional[str]) -> Dict[str, Any]:
        """Find the best place to insert a new class."""
        # Look for existing classes
        class_lines = []
        for i, line in enumerate(lines):
            if re.match(r'^\s*class\s+\w+', line):
                class_lines.append(i)
        
        if not class_lines:
            # No classes found, insert after imports and functions
            function_end = self._find_last_function_end(lines)
            if function_end >= 0:
                return {
                    'success': True,
                    'line_number': function_end + 2,
                    'context': 'after_functions'
                }
            else:
                import_end = self._find_import_section_end(lines)
                return {
                    'success': True,
                    'line_number': import_end + 2,
                    'context': 'after_imports'
                }
        
        # Insert after the last class
        last_class_start = class_lines[-1]
        last_class_end = self._find_block_end(lines, last_class_start)
        
        return {
            'success': True,
            'line_number': last_class_end + 2,
            'context': 'after_last_class'
        }
    
    def _find_import_insertion_point(self, lines: List[str]) -> Dict[str, Any]:
        """Find the best place to insert a new import."""
        import_end = self._find_import_section_end(lines)
        
        return {
            'success': True,
            'line_number': import_end,
            'context': 'with_imports'
        }
    
    def _find_import_section_end(self, lines: List[str]) -> int:
        """Find the end of the import section."""
        last_import_line = -1
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if (stripped.startswith('import ') or 
                stripped.startswith('from ') or
                stripped.startswith('#') and 'import' in stripped.lower() or
                not stripped):  # Empty lines in import section
                last_import_line = i
            elif stripped and not stripped.startswith('#'):
                # Found non-import, non-comment line
                break
        
        return last_import_line + 1
    
    def _find_last_function_end(self, lines: List[str]) -> int:
        """Find the end of the last function in the file."""
        function_lines = []
        for i, line in enumerate(lines):
            if re.match(r'^\s*def\s+\w+', line):
                function_lines.append(i)
        
        if not function_lines:
            return -1
        
        last_function_start = function_lines[-1]
        return self._find_block_end(lines, last_function_start)