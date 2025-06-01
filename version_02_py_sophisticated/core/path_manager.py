"""
Dynamic path management for cross-platform compatibility.
Handles all path-related operations without hardcoded paths.
"""

import os
from pathlib import Path
from typing import Optional, List, Union


class PathManager:
    """Manages all path operations dynamically."""
    
    def __init__(self, project_root: Optional[Union[str, Path]] = None):
        """Initialize path manager with optional project root."""
        self._project_root = self._find_project_root(project_root)
        self._task_file = "tasks.txt"
        self._config_file = ".task-config.json"
        self._ai_context_file = ".ai-context.json"
    
    def _find_project_root(self, provided_root: Optional[Union[str, Path]] = None) -> Path:
        """Find the project root directory."""
        if provided_root:
            return Path(provided_root).resolve()
        
        # Start from current directory
        current = Path.cwd()
        
        # Look for common project indicators
        indicators = [
            '.git',
            '.task-config.json',
            'package.json',
            'requirements.txt',
            'pyproject.toml',
            'Cargo.toml',
            'pom.xml'
        ]
        
        # Search up the directory tree
        for parent in [current] + list(current.parents):
            for indicator in indicators:
                if (parent / indicator).exists():
                    return parent
        
        # Default to current directory
        return current
    
    def get_project_root(self) -> Path:
        """Get the project root directory."""
        return self._project_root
    
    def get_task_file_path(self) -> Path:
        """Get the path to the tasks file."""
        return self._project_root / self._task_file
    
    def get_config_file_path(self) -> Path:
        """Get the path to the configuration file."""
        return self._project_root / self._config_file
    
    def get_ai_context_file_path(self) -> Path:
        """Get the path to the AI context file."""
        return self._project_root / self._ai_context_file
    
    def get_templates_dir(self) -> Path:
        """Get the templates directory path."""
        return Path(__file__).parent.parent / "templates"
    
    def get_docs_dir(self) -> Path:
        """Get the documentation directory path."""
        return self._project_root / "docs"
    
    def get_prompts_dir(self) -> Path:
        """Get the prompts directory path."""
        return self._project_root / "prompts"
    
    def get_task_manager_dir(self) -> Path:
        """Get the task manager internal directory."""
        return self._project_root / ".task-manager"
    
    def resolve_path(self, path: Union[str, Path], relative_to_project: bool = True) -> Path:
        """Resolve a path relative to project root or as absolute."""
        path_obj = Path(path)
        
        if path_obj.is_absolute():
            return path_obj
        
        if relative_to_project:
            return self._project_root / path_obj
        else:
            return path_obj.resolve()
    
    def find_files(self, pattern: str, directories: Optional[List[str]] = None) -> List[Path]:
        """Find files matching a pattern in specified directories."""
        if directories is None:
            directories = ["."]
        
        found_files = []
        
        for directory in directories:
            dir_path = self.resolve_path(directory)
            if dir_path.exists() and dir_path.is_dir():
                found_files.extend(dir_path.rglob(pattern))
        
        return found_files
    
    def get_source_files(self, extensions: Optional[List[str]] = None) -> List[Path]:
        """Get all source files in the project."""
        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.tsx', '.java', '.cpp', '.c', '.cs', '.go', '.rb', '.php']
        
        source_files = []
        
        # Common source directories
        source_dirs = ['src', 'lib', 'app', 'components', 'modules', 'packages']
        
        # Also check project root
        search_dirs = ['.'] + source_dirs
        
        for ext in extensions:
            pattern = f"*{ext}"
            source_files.extend(self.find_files(pattern, search_dirs))
        
        # Filter out common ignore patterns
        ignore_patterns = [
            '__pycache__',
            'node_modules',
            '.git',
            'venv',
            'env',
            'build',
            'dist',
            '.pytest_cache'
        ]
        
        filtered_files = []
        for file_path in source_files:
            if not any(ignore in str(file_path) for ignore in ignore_patterns):
                filtered_files.append(file_path)
        
        return filtered_files
    
    def get_test_files(self) -> List[Path]:
        """Get all test files in the project."""
        test_patterns = ['test_*.py', '*_test.py', '*.test.js', '*.spec.js']
        test_dirs = ['tests', 'test', '__tests__', 'spec']
        
        test_files = []
        for pattern in test_patterns:
            test_files.extend(self.find_files(pattern, test_dirs))
        
        return test_files
    
    def get_config_files(self) -> List[Path]:
        """Get all configuration files in the project."""
        config_patterns = [
            'package.json',
            'requirements.txt',
            'pyproject.toml',
            'setup.py',
            'Cargo.toml',
            'pom.xml',
            '*.config.js',
            '*.config.json',
            '.env*',
            'Dockerfile',
            'docker-compose.yml'
        ]
        
        config_files = []
        for pattern in config_patterns:
            config_files.extend(self.find_files(pattern, ['.']))
        
        return config_files
    
    def create_directory(self, path: Union[str, Path], relative_to_project: bool = True) -> Path:
        """Create a directory if it doesn't exist."""
        dir_path = self.resolve_path(path, relative_to_project)
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path
    
    def ensure_file_directory(self, file_path: Union[str, Path], relative_to_project: bool = True) -> Path:
        """Ensure the directory for a file exists."""
        resolved_path = self.resolve_path(file_path, relative_to_project)
        resolved_path.parent.mkdir(parents=True, exist_ok=True)
        return resolved_path
    
    def is_project_file(self, file_path: Union[str, Path]) -> bool:
        """Check if a file is within the project directory."""
        try:
            resolved_path = self.resolve_path(file_path, relative_to_project=False)
            return self._project_root in resolved_path.parents or resolved_path == self._project_root
        except (ValueError, OSError):
            return False
    
    def get_relative_path(self, file_path: Union[str, Path]) -> Path:
        """Get path relative to project root."""
        resolved_path = self.resolve_path(file_path, relative_to_project=False)
        try:
            return resolved_path.relative_to(self._project_root)
        except ValueError:
            # File is outside project root
            return resolved_path
    
    def backup_file(self, file_path: Union[str, Path]) -> Path:
        """Create a backup of a file."""
        original_path = self.resolve_path(file_path)
        backup_dir = self.get_task_manager_dir() / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Create backup filename with timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{original_path.stem}_{timestamp}{original_path.suffix}"
        backup_path = backup_dir / backup_name
        
        if original_path.exists():
            import shutil
            shutil.copy2(original_path, backup_path)
        
        return backup_path
    
    def __str__(self) -> str:
        """String representation of the path manager."""
        return f"PathManager(project_root={self._project_root})"
    
    def __repr__(self) -> str:
        """Detailed representation of the path manager."""
        return f"PathManager(project_root='{self._project_root}', task_file='{self._task_file}')"