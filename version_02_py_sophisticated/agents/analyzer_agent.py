"""
Analyzer Agent for code analysis and understanding.
"""

from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import json
from datetime import datetime

from ..utils.file_utils import FileUtils
from ..utils.ai_utils import AIUtils


class AnalyzerAgent:
    """Agent specialized in analyzing code, projects, and requirements."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the analyzer agent."""
        self.config = config
        self.analysis_cache = {}
        self.supported_languages = {
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
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.dart': 'dart',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sql': 'sql',
            '.sh': 'bash',
            '.ps1': 'powershell'
        }
    
    def analyze_project_structure(self, project_path: Path) -> Dict[str, Any]:
        """Analyze the overall project structure."""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'project_path': str(project_path),
            'structure': {},
            'file_count': 0,
            'directory_count': 0,
            'languages': {},
            'file_types': {},
            'size_analysis': {},
            'complexity_indicators': {}
        }
        
        try:
            # Walk through the project directory
            for item in project_path.rglob('*'):
                if item.is_file():
                    analysis['file_count'] += 1
                    self._analyze_file_for_structure(item, project_path, analysis)
                elif item.is_dir():
                    analysis['directory_count'] += 1
            
            # Calculate complexity indicators
            analysis['complexity_indicators'] = self._calculate_complexity_indicators(analysis)
            
            return analysis
        
        except Exception as e:
            return {
                'error': f"Failed to analyze project structure: {e}",
                'timestamp': datetime.now().isoformat()
            }
    
    def _analyze_file_for_structure(self, file_path: Path, project_root: Path, analysis: Dict[str, Any]):
        """Analyze a single file for structure analysis."""
        try:
            # Get relative path
            rel_path = file_path.relative_to(project_root)
            
            # Get file extension and type
            extension = file_path.suffix.lower()
            file_size = FileUtils.get_file_size(file_path)
            
            # Update file types count
            if extension:
                analysis['file_types'][extension] = analysis['file_types'].get(extension, 0) + 1
            
            # Update language count
            if extension in self.supported_languages:
                language = self.supported_languages[extension]
                analysis['languages'][language] = analysis['languages'].get(language, 0) + 1
            
            # Update size analysis
            size_category = self._categorize_file_size(file_size)
            analysis['size_analysis'][size_category] = analysis['size_analysis'].get(size_category, 0) + 1
            
            # Store file info in structure
            dir_parts = list(rel_path.parent.parts)
            current_level = analysis['structure']
            
            for part in dir_parts:
                if part not in current_level:
                    current_level[part] = {'files': [], 'directories': {}}
                current_level = current_level[part]['directories']
            
            # Add file to the appropriate directory level
            if dir_parts:
                parent_dir = analysis['structure']
                for part in dir_parts[:-1]:
                    parent_dir = parent_dir[part]['directories']
                parent_dir[dir_parts[-1]]['files'].append({
                    'name': file_path.name,
                    'size': file_size,
                    'extension': extension,
                    'language': self.supported_languages.get(extension, 'unknown')
                })
            else:
                # File in root directory
                if 'root_files' not in analysis['structure']:
                    analysis['structure']['root_files'] = []
                analysis['structure']['root_files'].append({
                    'name': file_path.name,
                    'size': file_size,
                    'extension': extension,
                    'language': self.supported_languages.get(extension, 'unknown')
                })
        
        except Exception as e:
            # Log error but continue analysis
            pass
    
    def _categorize_file_size(self, size: int) -> str:
        """Categorize file size."""
        if size < 1024:  # < 1KB
            return 'tiny'
        elif size < 10240:  # < 10KB
            return 'small'
        elif size < 102400:  # < 100KB
            return 'medium'
        elif size < 1048576:  # < 1MB
            return 'large'
        else:
            return 'very_large'
    
    def _calculate_complexity_indicators(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate project complexity indicators."""
        indicators = {
            'language_diversity': len(analysis['languages']),
            'file_diversity': len(analysis['file_types']),
            'average_files_per_directory': 0,
            'depth_estimate': 0,
            'complexity_score': 0
        }
        
        # Calculate average files per directory
        if analysis['directory_count'] > 0:
            indicators['average_files_per_directory'] = analysis['file_count'] / analysis['directory_count']
        
        # Estimate project depth (simplified)
        indicators['depth_estimate'] = min(analysis['directory_count'] // 5, 10)
        
        # Calculate complexity score (0-100)
        complexity_score = 0
        complexity_score += min(indicators['language_diversity'] * 10, 30)  # Max 30 for languages
        complexity_score += min(analysis['file_count'] // 10, 40)  # Max 40 for file count
        complexity_score += min(indicators['depth_estimate'] * 3, 30)  # Max 30 for depth
        
        indicators['complexity_score'] = min(complexity_score, 100)
        
        return indicators
    
    def analyze_code_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a specific code file."""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'file_path': str(file_path),
            'language': 'unknown',
            'metrics': {},
            'structure': {},
            'issues': [],
            'suggestions': []
        }
        
        try:
            # Determine language
            extension = file_path.suffix.lower()
            analysis['language'] = self.supported_languages.get(extension, 'unknown')
            
            if not FileUtils.is_text_file(file_path):
                analysis['issues'].append("File is not a text file")
                return analysis
            
            # Read file content
            content = FileUtils.read_file(file_path)
            lines = content.split('\n')
            
            # Basic metrics
            analysis['metrics'] = {
                'lines_total': len(lines),
                'lines_code': self._count_code_lines(lines, analysis['language']),
                'lines_comment': self._count_comment_lines(lines, analysis['language']),
                'lines_blank': self._count_blank_lines(lines),
                'characters': len(content),
                'file_size': FileUtils.get_file_size(file_path)
            }
            
            # Language-specific analysis
            if analysis['language'] == 'python':
                analysis['structure'] = self._analyze_python_structure(content)
            elif analysis['language'] in ['javascript', 'typescript']:
                analysis['structure'] = self._analyze_js_structure(content)
            else:
                analysis['structure'] = self._analyze_generic_structure(content)
            
            # Generate suggestions
            analysis['suggestions'] = self._generate_code_suggestions(analysis)
            
            return analysis
        
        except Exception as e:
            analysis['issues'].append(f"Analysis failed: {e}")
            return analysis
    
    def _count_code_lines(self, lines: List[str], language: str) -> int:
        """Count lines of code (excluding comments and blank lines)."""
        code_lines = 0
        comment_patterns = {
            'python': ['#'],
            'javascript': ['//', '/*', '*/', '/**'],
            'typescript': ['//', '/*', '*/', '/**'],
            'java': ['//', '/*', '*/', '/**'],
            'cpp': ['//', '/*', '*/', '/**'],
            'c': ['//', '/*', '*/', '/**'],
            'csharp': ['//', '/*', '*/', '/**'],
            'go': ['//', '/*', '*/', '/**'],
            'rust': ['//', '/*', '*/', '/**'],
            'css': ['/*', '*/'],
            'html': ['<!--', '-->'],
            'sql': ['--', '/*', '*/'],
            'bash': ['#'],
            'powershell': ['#']
        }
        
        comment_chars = comment_patterns.get(language, ['#', '//', '/*'])
        
        for line in lines:
            stripped = line.strip()
            if stripped and not any(stripped.startswith(char) for char in comment_chars):
                code_lines += 1
        
        return code_lines
    
    def _count_comment_lines(self, lines: List[str], language: str) -> int:
        """Count comment lines."""
        comment_lines = 0
        comment_patterns = {
            'python': ['#'],
            'javascript': ['//', '/*', '*/', '/**', '*'],
            'typescript': ['//', '/*', '*/', '/**', '*'],
            'java': ['//', '/*', '*/', '/**', '*'],
            'cpp': ['//', '/*', '*/', '/**', '*'],
            'c': ['//', '/*', '*/', '/**', '*'],
            'csharp': ['//', '/*', '*/', '/**', '*'],
            'go': ['//', '/*', '*/', '/**', '*'],
            'rust': ['//', '/*', '*/', '/**', '*'],
            'css': ['/*', '*/', '*'],
            'html': ['<!--', '-->', '*'],
            'sql': ['--', '/*', '*/', '*'],
            'bash': ['#'],
            'powershell': ['#']
        }
        
        comment_chars = comment_patterns.get(language, ['#', '//', '/*', '*'])
        
        for line in lines:
            stripped = line.strip()
            if any(stripped.startswith(char) for char in comment_chars):
                comment_lines += 1
        
        return comment_lines
    
    def _count_blank_lines(self, lines: List[str]) -> int:
        """Count blank lines."""
        return sum(1 for line in lines if not line.strip())
    
    def _analyze_python_structure(self, content: str) -> Dict[str, Any]:
        """Analyze Python file structure."""
        structure = {
            'imports': [],
            'classes': [],
            'functions': [],
            'variables': [],
            'complexity_estimate': 0
        }
        
        lines = content.split('\n')
        current_class = None
        indent_level = 0
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Count indentation
            indent = len(line) - len(line.lstrip())
            
            # Imports
            if stripped.startswith(('import ', 'from ')):
                structure['imports'].append({
                    'line': line_num,
                    'statement': stripped
                })
            
            # Class definitions
            elif stripped.startswith('class '):
                class_name = stripped.split('(')[0].replace('class ', '').strip(':')
                current_class = {
                    'name': class_name,
                    'line': line_num,
                    'methods': [],
                    'indent': indent
                }
                structure['classes'].append(current_class)
            
            # Function/method definitions
            elif stripped.startswith('def '):
                func_name = stripped.split('(')[0].replace('def ', '')
                func_info = {
                    'name': func_name,
                    'line': line_num,
                    'indent': indent
                }
                
                if current_class and indent > current_class['indent']:
                    current_class['methods'].append(func_info)
                else:
                    structure['functions'].append(func_info)
                    current_class = None  # Reset current class if we're at module level
            
            # Variable assignments (simple detection)
            elif '=' in stripped and not stripped.startswith(('#', '"', "'")):
                var_name = stripped.split('=')[0].strip()
                if var_name.isidentifier():
                    structure['variables'].append({
                        'name': var_name,
                        'line': line_num
                    })
        
        # Estimate complexity
        structure['complexity_estimate'] = (
            len(structure['classes']) * 3 +
            len(structure['functions']) * 2 +
            sum(len(cls['methods']) for cls in structure['classes']) * 2
        )
        
        return structure
    
    def _analyze_js_structure(self, content: str) -> Dict[str, Any]:
        """Analyze JavaScript/TypeScript file structure."""
        structure = {
            'imports': [],
            'exports': [],
            'functions': [],
            'classes': [],
            'variables': [],
            'complexity_estimate': 0
        }
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Imports
            if stripped.startswith(('import ', 'const ', 'let ', 'var ')) and 'require(' in stripped:
                structure['imports'].append({
                    'line': line_num,
                    'statement': stripped
                })
            elif stripped.startswith('import '):
                structure['imports'].append({
                    'line': line_num,
                    'statement': stripped
                })
            
            # Exports
            elif stripped.startswith('export '):
                structure['exports'].append({
                    'line': line_num,
                    'statement': stripped
                })
            
            # Function definitions
            elif 'function ' in stripped or '=>' in stripped:
                structure['functions'].append({
                    'line': line_num,
                    'statement': stripped[:50] + '...' if len(stripped) > 50 else stripped
                })
            
            # Class definitions
            elif stripped.startswith('class '):
                class_name = stripped.split('{')[0].replace('class ', '').strip()
                structure['classes'].append({
                    'name': class_name,
                    'line': line_num
                })
            
            # Variable declarations
            elif stripped.startswith(('const ', 'let ', 'var ')):
                var_name = stripped.split('=')[0].strip()
                for keyword in ['const ', 'let ', 'var ']:
                    var_name = var_name.replace(keyword, '')
                structure['variables'].append({
                    'name': var_name,
                    'line': line_num
                })
        
        # Estimate complexity
        structure['complexity_estimate'] = (
            len(structure['functions']) * 2 +
            len(structure['classes']) * 3 +
            len(structure['exports']) * 1
        )
        
        return structure
    
    def _analyze_generic_structure(self, content: str) -> Dict[str, Any]:
        """Generic structure analysis for unsupported languages."""
        structure = {
            'lines_analyzed': len(content.split('\n')),
            'estimated_functions': 0,
            'estimated_classes': 0,
            'complexity_estimate': 0
        }
        
        lines = content.split('\n')
        
        # Simple heuristics for function/class detection
        function_keywords = ['function', 'def ', 'func ', 'sub ', 'procedure', 'method']
        class_keywords = ['class ', 'struct ', 'interface ', 'type ']
        
        for line in lines:
            stripped = line.strip().lower()
            
            if any(keyword in stripped for keyword in function_keywords):
                structure['estimated_functions'] += 1
            
            if any(keyword in stripped for keyword in class_keywords):
                structure['estimated_classes'] += 1
        
        structure['complexity_estimate'] = (
            structure['estimated_functions'] * 2 +
            structure['estimated_classes'] * 3
        )
        
        return structure
    
    def _generate_code_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate suggestions based on code analysis."""
        suggestions = []
        metrics = analysis.get('metrics', {})
        
        # File size suggestions
        if metrics.get('lines_total', 0) > 500:
            suggestions.append("Consider breaking this large file into smaller modules")
        
        # Comment ratio suggestions
        code_lines = metrics.get('lines_code', 1)
        comment_lines = metrics.get('lines_comment', 0)
        comment_ratio = comment_lines / code_lines if code_lines > 0 else 0
        
        if comment_ratio < 0.1:
            suggestions.append("Consider adding more comments to improve code documentation")
        elif comment_ratio > 0.5:
            suggestions.append("High comment ratio - ensure comments are necessary and up-to-date")
        
        # Complexity suggestions
        structure = analysis.get('structure', {})
        complexity = structure.get('complexity_estimate', 0)
        
        if complexity > 20:
            suggestions.append("High complexity detected - consider refactoring into smaller components")
        
        # Language-specific suggestions
        if analysis['language'] == 'python':
            if len(structure.get('imports', [])) > 20:
                suggestions.append("Many imports detected - consider organizing imports or reducing dependencies")
        
        return suggestions
    
    def analyze_requirements(self, requirements_text: str) -> Dict[str, Any]:
        """Analyze requirements or task descriptions."""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'word_count': len(requirements_text.split()),
            'character_count': len(requirements_text),
            'complexity_indicators': {},
            'extracted_entities': {},
            'suggestions': []
        }
        
        # Basic complexity analysis
        sentences = requirements_text.split('.')
        analysis['complexity_indicators'] = {
            'sentence_count': len(sentences),
            'average_sentence_length': analysis['word_count'] / len(sentences) if sentences else 0,
            'technical_terms': self._count_technical_terms(requirements_text),
            'action_words': self._count_action_words(requirements_text)
        }
        
        # Extract entities (simplified)
        analysis['extracted_entities'] = {
            'technologies': self._extract_technologies(requirements_text),
            'file_types': self._extract_file_types(requirements_text),
            'actions': self._extract_actions(requirements_text)
        }
        
        # Generate suggestions
        analysis['suggestions'] = self._generate_requirements_suggestions(analysis)
        
        return analysis
    
    def _count_technical_terms(self, text: str) -> int:
        """Count technical terms in text."""
        technical_terms = [
            'api', 'database', 'server', 'client', 'framework', 'library',
            'function', 'class', 'method', 'variable', 'algorithm', 'data',
            'interface', 'component', 'module', 'service', 'endpoint',
            'authentication', 'authorization', 'security', 'performance',
            'optimization', 'testing', 'deployment', 'configuration'
        ]
        
        text_lower = text.lower()
        return sum(1 for term in technical_terms if term in text_lower)
    
    def _count_action_words(self, text: str) -> int:
        """Count action words in text."""
        action_words = [
            'create', 'build', 'develop', 'implement', 'design', 'add',
            'remove', 'update', 'modify', 'fix', 'optimize', 'test',
            'deploy', 'configure', 'setup', 'install', 'integrate',
            'refactor', 'improve', 'enhance', 'validate', 'verify'
        ]
        
        text_lower = text.lower()
        return sum(1 for word in action_words if word in text_lower)
    
    def _extract_technologies(self, text: str) -> List[str]:
        """Extract technology names from text."""
        technologies = [
            'python', 'javascript', 'typescript', 'java', 'cpp', 'c++',
            'react', 'vue', 'angular', 'node', 'express', 'django',
            'flask', 'spring', 'laravel', 'rails', 'asp.net',
            'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp',
            'git', 'github', 'gitlab', 'jenkins', 'travis'
        ]
        
        text_lower = text.lower()
        found_technologies = []
        
        for tech in technologies:
            if tech in text_lower:
                found_technologies.append(tech)
        
        return found_technologies
    
    def _extract_file_types(self, text: str) -> List[str]:
        """Extract file types mentioned in text."""
        import re
        
        # Look for file extensions
        file_pattern = r'\.\w{2,4}\b'
        matches = re.findall(file_pattern, text.lower())
        
        return list(set(matches))
    
    def _extract_actions(self, text: str) -> List[str]:
        """Extract action items from text."""
        import re
        
        # Look for imperative sentences or action phrases
        action_patterns = [
            r'\b(create|build|develop|implement|design|add|remove|update|modify|fix)\s+\w+',
            r'\b(should|must|need to|have to)\s+\w+',
            r'\b(will|shall)\s+\w+'
        ]
        
        actions = []
        for pattern in action_patterns:
            matches = re.findall(pattern, text.lower())
            actions.extend(matches)
        
        return actions
    
    def _generate_requirements_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate suggestions for requirements improvement."""
        suggestions = []
        
        complexity = analysis['complexity_indicators']
        
        if complexity['sentence_count'] < 3:
            suggestions.append("Requirements seem brief - consider adding more detail")
        
        if complexity['technical_terms'] < 2:
            suggestions.append("Consider specifying technical requirements more clearly")
        
        if complexity['action_words'] < 1:
            suggestions.append("Add clear action items or deliverables")
        
        entities = analysis['extracted_entities']
        
        if not entities['technologies']:
            suggestions.append("Specify the technologies or frameworks to be used")
        
        if not entities['actions']:
            suggestions.append("Define clear actions or tasks to be completed")
        
        return suggestions
    
    def get_analysis_summary(self, analysis_type: str, analysis_data: Dict[str, Any]) -> str:
        """Generate a human-readable summary of analysis results."""
        if analysis_type == "project_structure":
            return self._summarize_project_analysis(analysis_data)
        elif analysis_type == "code_file":
            return self._summarize_code_analysis(analysis_data)
        elif analysis_type == "requirements":
            return self._summarize_requirements_analysis(analysis_data)
        else:
            return "Unknown analysis type"
    
    def _summarize_project_analysis(self, analysis: Dict[str, Any]) -> str:
        """Summarize project structure analysis."""
        summary_parts = [
            f"Project Analysis Summary:",
            f"- Files: {analysis.get('file_count', 0)}",
            f"- Directories: {analysis.get('directory_count', 0)}",
            f"- Languages: {', '.join(analysis.get('languages', {}).keys())}",
            f"- Complexity Score: {analysis.get('complexity_indicators', {}).get('complexity_score', 0)}/100"
        ]
        
        return '\n'.join(summary_parts)
    
    def _summarize_code_analysis(self, analysis: Dict[str, Any]) -> str:
        """Summarize code file analysis."""
        metrics = analysis.get('metrics', {})
        structure = analysis.get('structure', {})
        
        summary_parts = [
            f"Code Analysis Summary:",
            f"- Language: {analysis.get('language', 'unknown')}",
            f"- Lines of Code: {metrics.get('lines_code', 0)}",
            f"- Comments: {metrics.get('lines_comment', 0)}",
            f"- Complexity: {structure.get('complexity_estimate', 0)}"
        ]
        
        if analysis.get('suggestions'):
            summary_parts.append(f"- Suggestions: {len(analysis['suggestions'])}")
        
        return '\n'.join(summary_parts)
    
    def _summarize_requirements_analysis(self, analysis: Dict[str, Any]) -> str:
        """Summarize requirements analysis."""
        complexity = analysis.get('complexity_indicators', {})
        entities = analysis.get('extracted_entities', {})
        
        summary_parts = [
            f"Requirements Analysis Summary:",
            f"- Word Count: {analysis.get('word_count', 0)}",
            f"- Technical Terms: {complexity.get('technical_terms', 0)}",
            f"- Technologies: {', '.join(entities.get('technologies', []))}",
            f"- Suggestions: {len(analysis.get('suggestions', []))}"
        ]
        
        return '\n'.join(summary_parts)