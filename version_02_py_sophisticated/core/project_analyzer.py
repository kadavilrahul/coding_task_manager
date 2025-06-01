"""
Project analysis and discovery functionality.
Automatically detects project type, structure, and characteristics.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from collections import Counter
from .path_manager import PathManager


class ProjectAnalyzer:
    """Analyzes project structure and characteristics."""
    
    def __init__(self, path_manager: PathManager):
        """Initialize project analyzer."""
        self.path_manager = path_manager
        self.project_root = path_manager.get_project_root()
    
    def analyze_current_directory(self) -> Dict[str, Any]:
        """Analyze the current project directory."""
        analysis = {
            'project_name': self.project_root.name,
            'project_type': self._detect_project_type(),
            'tech_stack': self._detect_tech_stack(),
            'architecture': self._detect_architecture(),
            'source_dirs': self._find_source_directories(),
            'test_dirs': self._find_test_directories(),
            'config_files': self._find_config_files(),
            'dependencies': self._analyze_dependencies(),
            'file_stats': self._get_file_statistics(),
            'complexity_estimate': self._estimate_complexity(),
            'ai_readiness': self._assess_ai_readiness()
        }
        
        return analysis
    
    def _detect_project_type(self) -> str:
        """Detect the type of project based on files and structure."""
        indicators = {
            'web-app': [
                'package.json', 'index.html', 'src/index.js', 'public/',
                'webpack.config.js', 'vite.config.js', 'next.config.js'
            ],
            'mobile-app': [
                'package.json', 'App.js', 'App.tsx', 'android/', 'ios/',
                'react-native.config.js', 'metro.config.js'
            ],
            'api': [
                'app.py', 'main.py', 'server.py', 'api/', 'routes/',
                'requirements.txt', 'Pipfile', 'fastapi', 'flask'
            ],
            'library': [
                'setup.py', 'pyproject.toml', '__init__.py', 'lib/',
                'Cargo.toml', 'package.json'
            ],
            'microservice': [
                'Dockerfile', 'docker-compose.yml', 'k8s/', 'helm/',
                'service.py', 'microservice'
            ],
            'desktop-app': [
                'main.py', 'app.py', 'tkinter', 'PyQt', 'electron',
                'main.js', 'package.json'
            ],
            'data-science': [
                'notebook.ipynb', 'data/', 'models/', 'requirements.txt',
                'jupyter', 'pandas', 'numpy', 'sklearn'
            ],
            'game': [
                'main.py', 'game.py', 'pygame', 'unity', 'godot',
                'Assets/', 'Scripts/'
            ]
        }
        
        scores = {}
        
        for project_type, type_indicators in indicators.items():
            score = 0
            for indicator in type_indicators:
                if self._check_indicator(indicator):
                    score += 1
            scores[project_type] = score
        
        # Return the type with highest score, or 'unknown' if no clear match
        if scores:
            best_type = max(scores, key=scores.get)
            if scores[best_type] > 0:
                return best_type
        
        return 'unknown'
    
    def _check_indicator(self, indicator: str) -> bool:
        """Check if a project indicator exists."""
        # Check for files
        if '.' in indicator and not indicator.endswith('/'):
            return (self.project_root / indicator).exists()
        
        # Check for directories
        if indicator.endswith('/'):
            return (self.project_root / indicator.rstrip('/')).is_dir()
        
        # Check for content in files (like dependencies)
        return self._check_content_indicator(indicator)
    
    def _check_content_indicator(self, indicator: str) -> bool:
        """Check if indicator appears in project files."""
        search_files = [
            'package.json', 'requirements.txt', 'Pipfile', 'pyproject.toml',
            'Cargo.toml', 'pom.xml', 'build.gradle'
        ]
        
        for file_name in search_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    if indicator.lower() in content.lower():
                        return True
                except (UnicodeDecodeError, OSError):
                    continue
        
        return False
    
    def _detect_tech_stack(self) -> List[str]:
        """Detect technologies used in the project."""
        tech_stack = set()
        
        # Language detection based on file extensions
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript',
            '.jsx': 'JavaScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.dart': 'Dart',
            '.html': 'HTML',
            '.css': 'CSS',
            '.scss': 'SASS',
            '.less': 'LESS'
        }
        
        # Count file extensions
        source_files = self.path_manager.get_source_files()
        for file_path in source_files:
            ext = file_path.suffix.lower()
            if ext in language_map:
                tech_stack.add(language_map[ext])
        
        # Framework/library detection
        frameworks = self._detect_frameworks()
        tech_stack.update(frameworks)
        
        return sorted(list(tech_stack))
    
    def _detect_frameworks(self) -> List[str]:
        """Detect frameworks and libraries used."""
        frameworks = []
        
        # Check package.json for JavaScript frameworks
        package_json = self.project_root / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                
                framework_map = {
                    'react': 'React',
                    'vue': 'Vue.js',
                    'angular': 'Angular',
                    'svelte': 'Svelte',
                    'next': 'Next.js',
                    'nuxt': 'Nuxt.js',
                    'express': 'Express.js',
                    'fastify': 'Fastify',
                    'nest': 'NestJS',
                    'electron': 'Electron'
                }
                
                for dep in deps:
                    for key, framework in framework_map.items():
                        if key in dep.lower():
                            frameworks.append(framework)
                            break
            
            except (json.JSONDecodeError, OSError):
                pass
        
        # Check requirements.txt for Python frameworks
        requirements_txt = self.project_root / 'requirements.txt'
        if requirements_txt.exists():
            try:
                content = requirements_txt.read_text(encoding='utf-8')
                
                python_frameworks = {
                    'django': 'Django',
                    'flask': 'Flask',
                    'fastapi': 'FastAPI',
                    'tornado': 'Tornado',
                    'pyramid': 'Pyramid',
                    'bottle': 'Bottle',
                    'streamlit': 'Streamlit',
                    'dash': 'Dash',
                    'pandas': 'Pandas',
                    'numpy': 'NumPy',
                    'tensorflow': 'TensorFlow',
                    'pytorch': 'PyTorch',
                    'scikit-learn': 'Scikit-learn'
                }
                
                for package, framework in python_frameworks.items():
                    if package in content.lower():
                        frameworks.append(framework)
            
            except OSError:
                pass
        
        return frameworks
    
    def _detect_architecture(self) -> str:
        """Detect the project architecture pattern."""
        # Check for common architecture patterns
        patterns = {
            'MVC': ['models/', 'views/', 'controllers/', 'model.py', 'view.py', 'controller.py'],
            'MVP': ['models/', 'views/', 'presenters/', 'presenter.py'],
            'MVVM': ['models/', 'views/', 'viewmodels/', 'viewmodel.py'],
            'Component-based': ['components/', 'Component.js', 'Component.tsx'],
            'Microservices': ['services/', 'service.py', 'docker-compose.yml'],
            'Layered': ['layers/', 'business/', 'data/', 'presentation/'],
            'Clean Architecture': ['domain/', 'infrastructure/', 'application/', 'presentation/'],
            'Hexagonal': ['adapters/', 'ports/', 'domain/'],
            'Event-driven': ['events/', 'handlers/', 'event.py'],
            'REST': ['api/', 'routes/', 'endpoints/'],
            'GraphQL': ['schema/', 'resolvers/', 'graphql']
        }
        
        scores = {}
        for pattern, indicators in patterns.items():
            score = sum(1 for indicator in indicators if self._check_indicator(indicator))
            if score > 0:
                scores[pattern] = score
        
        if scores:
            return max(scores, key=scores.get)
        
        return 'unknown'
    
    def _find_source_directories(self) -> List[str]:
        """Find source code directories."""
        common_source_dirs = [
            'src', 'lib', 'app', 'source', 'code', 'components',
            'modules', 'packages', 'services', 'api', 'core'
        ]
        
        found_dirs = []
        for dir_name in common_source_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.is_dir() and self._has_source_files(dir_path):
                found_dirs.append(dir_name)
        
        # If no common directories found, check if root has source files
        if not found_dirs and self._has_source_files(self.project_root):
            found_dirs.append('.')
        
        return found_dirs or ['src']  # Default to 'src' if nothing found
    
    def _find_test_directories(self) -> List[str]:
        """Find test directories."""
        common_test_dirs = [
            'tests', 'test', '__tests__', 'spec', 'testing',
            'test_suite', 'unit_tests', 'integration_tests'
        ]
        
        found_dirs = []
        for dir_name in common_test_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.is_dir():
                found_dirs.append(dir_name)
        
        return found_dirs or ['tests']  # Default to 'tests'
    
    def _find_config_files(self) -> List[str]:
        """Find configuration files."""
        config_files = []
        
        for file_path in self.path_manager.get_config_files():
            relative_path = self.path_manager.get_relative_path(file_path)
            config_files.append(str(relative_path))
        
        return config_files
    
    def _has_source_files(self, directory: Path) -> bool:
        """Check if directory contains source files."""
        source_extensions = {'.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.cpp', '.c', '.cs', '.go', '.rs'}
        
        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in source_extensions:
                return True
        
        return False
    
    def _analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze project dependencies."""
        dependencies = {
            'package_managers': [],
            'dependency_files': [],
            'total_dependencies': 0,
            'outdated_dependencies': []
        }
        
        # Check for different package managers
        package_files = {
            'package.json': 'npm/yarn',
            'requirements.txt': 'pip',
            'Pipfile': 'pipenv',
            'pyproject.toml': 'poetry/pip',
            'Cargo.toml': 'cargo',
            'pom.xml': 'maven',
            'build.gradle': 'gradle',
            'composer.json': 'composer'
        }
        
        for file_name, manager in package_files.items():
            file_path = self.project_root / file_name
            if file_path.exists():
                dependencies['package_managers'].append(manager)
                dependencies['dependency_files'].append(file_name)
                
                # Count dependencies
                dep_count = self._count_dependencies(file_path)
                dependencies['total_dependencies'] += dep_count
        
        return dependencies
    
    def _count_dependencies(self, file_path: Path) -> int:
        """Count dependencies in a dependency file."""
        try:
            if file_path.name == 'package.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                deps = data.get('dependencies', {})
                dev_deps = data.get('devDependencies', {})
                return len(deps) + len(dev_deps)
            
            elif file_path.name in ['requirements.txt', 'Pipfile']:
                content = file_path.read_text(encoding='utf-8')
                lines = [line.strip() for line in content.split('\n')]
                return len([line for line in lines if line and not line.startswith('#')])
            
            # Add more dependency file parsers as needed
            
        except (json.JSONDecodeError, OSError, UnicodeDecodeError):
            pass
        
        return 0
    
    def _get_file_statistics(self) -> Dict[str, Any]:
        """Get file statistics for the project."""
        stats = {
            'total_files': 0,
            'source_files': 0,
            'test_files': 0,
            'config_files': 0,
            'documentation_files': 0,
            'lines_of_code': 0,
            'file_types': {}
        }
        
        # Count different types of files
        all_files = list(self.project_root.rglob('*'))
        
        for file_path in all_files:
            if file_path.is_file() and not self._should_ignore_file(file_path):
                stats['total_files'] += 1
                
                ext = file_path.suffix.lower()
                stats['file_types'][ext] = stats['file_types'].get(ext, 0) + 1
                
                # Categorize files
                if self._is_source_file(file_path):
                    stats['source_files'] += 1
                    stats['lines_of_code'] += self._count_lines(file_path)
                elif self._is_test_file(file_path):
                    stats['test_files'] += 1
                elif self._is_config_file(file_path):
                    stats['config_files'] += 1
                elif self._is_documentation_file(file_path):
                    stats['documentation_files'] += 1
        
        return stats
    
    def _should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored in analysis."""
        ignore_patterns = [
            '__pycache__', '.git', 'node_modules', 'venv', 'env',
            '.pytest_cache', 'build', 'dist', '.DS_Store'
        ]
        
        path_str = str(file_path)
        return any(pattern in path_str for pattern in ignore_patterns)
    
    def _is_source_file(self, file_path: Path) -> bool:
        """Check if file is a source code file."""
        source_extensions = {'.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.cpp', '.c', '.cs', '.go', '.rs', '.rb', '.php'}
        return file_path.suffix.lower() in source_extensions
    
    def _is_test_file(self, file_path: Path) -> bool:
        """Check if file is a test file."""
        name = file_path.name.lower()
        return ('test' in name or 'spec' in name) and self._is_source_file(file_path)
    
    def _is_config_file(self, file_path: Path) -> bool:
        """Check if file is a configuration file."""
        config_names = {
            'package.json', 'requirements.txt', 'pyproject.toml', 'setup.py',
            'Cargo.toml', 'pom.xml', 'build.gradle', 'Dockerfile',
            'docker-compose.yml', '.env', '.gitignore'
        }
        config_extensions = {'.config.js', '.config.json', '.yml', '.yaml', '.toml', '.ini'}
        
        return (file_path.name in config_names or 
                any(file_path.name.endswith(ext) for ext in config_extensions))
    
    def _is_documentation_file(self, file_path: Path) -> bool:
        """Check if file is documentation."""
        doc_extensions = {'.md', '.rst', '.txt', '.adoc'}
        doc_names = {'readme', 'changelog', 'license', 'contributing', 'docs'}
        
        return (file_path.suffix.lower() in doc_extensions or
                any(name in file_path.name.lower() for name in doc_names))
    
    def _count_lines(self, file_path: Path) -> int:
        """Count lines in a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return sum(1 for line in f if line.strip())
        except (UnicodeDecodeError, OSError):
            return 0
    
    def _estimate_complexity(self) -> str:
        """Estimate project complexity."""
        stats = self._get_file_statistics()
        
        lines_of_code = stats['lines_of_code']
        source_files = stats['source_files']
        
        if lines_of_code < 1000 and source_files < 10:
            return 'Simple'
        elif lines_of_code < 10000 and source_files < 50:
            return 'Medium'
        elif lines_of_code < 50000 and source_files < 200:
            return 'Complex'
        else:
            return 'Very Complex'
    
    def _assess_ai_readiness(self) -> Dict[str, Any]:
        """Assess how ready the project is for AI assistance."""
        readiness = {
            'score': 0,
            'max_score': 10,
            'recommendations': []
        }
        
        # Check for documentation
        if any(self._is_documentation_file(Path(f)) for f in self._find_config_files()):
            readiness['score'] += 2
        else:
            readiness['recommendations'].append('Add README.md and documentation')
        
        # Check for clear project structure
        source_dirs = self._find_source_directories()
        if len(source_dirs) > 0 and 'src' in source_dirs:
            readiness['score'] += 2
        else:
            readiness['recommendations'].append('Organize code in clear directory structure')
        
        # Check for tests
        test_dirs = self._find_test_directories()
        if any((self.project_root / test_dir).exists() for test_dir in test_dirs):
            readiness['score'] += 2
        else:
            readiness['recommendations'].append('Add test files and test directory')
        
        # Check for configuration files
        if self._find_config_files():
            readiness['score'] += 2
        else:
            readiness['recommendations'].append('Add configuration files (package.json, requirements.txt, etc.)')
        
        # Check for reasonable complexity
        complexity = self._estimate_complexity()
        if complexity in ['Simple', 'Medium']:
            readiness['score'] += 2
        else:
            readiness['recommendations'].append('Consider breaking down complex project into smaller modules')
        
        readiness['level'] = self._get_readiness_level(readiness['score'])
        
        return readiness
    
    def _get_readiness_level(self, score: int) -> str:
        """Get readiness level based on score."""
        if score >= 8:
            return 'Excellent'
        elif score >= 6:
            return 'Good'
        elif score >= 4:
            return 'Fair'
        else:
            return 'Needs Improvement'
    
    def generate_analysis_report(self) -> str:
        """Generate a comprehensive analysis report."""
        analysis = self.analyze_current_directory()
        
        report = f"""
# Project Analysis Report

## Project Overview
- **Name**: {analysis['project_name']}
- **Type**: {analysis['project_type']}
- **Architecture**: {analysis['architecture']}
- **Complexity**: {analysis['complexity_estimate']}

## Technology Stack
{', '.join(analysis['tech_stack']) if analysis['tech_stack'] else 'Not detected'}

## Project Structure
- **Source Directories**: {', '.join(analysis['source_dirs'])}
- **Test Directories**: {', '.join(analysis['test_dirs'])}
- **Configuration Files**: {len(analysis['config_files'])} files

## File Statistics
- **Total Files**: {analysis['file_stats']['total_files']}
- **Source Files**: {analysis['file_stats']['source_files']}
- **Test Files**: {analysis['file_stats']['test_files']}
- **Lines of Code**: {analysis['file_stats']['lines_of_code']}

## Dependencies
- **Package Managers**: {', '.join(analysis['dependencies']['package_managers'])}
- **Total Dependencies**: {analysis['dependencies']['total_dependencies']}

## AI Readiness Assessment
- **Score**: {analysis['ai_readiness']['score']}/{analysis['ai_readiness']['max_score']}
- **Level**: {analysis['ai_readiness']['level']}

### Recommendations:
{chr(10).join(f"- {rec}" for rec in analysis['ai_readiness']['recommendations'])}

---
*Report generated by AI-Enhanced Task Management System*
"""
        
        return report.strip()