"""
Configuration management for the task management system.
Handles loading, saving, and validating configuration files.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from .path_manager import PathManager


@dataclass
class AISettings:
    """AI configuration settings."""
    model: str = "gemini-pro"
    max_tokens: int = 4096
    temperature: float = 0.7
    api_key: Optional[str] = None
    endpoint: Optional[str] = None


@dataclass
class AgentSettings:
    """Agent configuration settings."""
    enabled: bool = True
    max_retries: int = 3
    timeout: int = 30
    custom_prompts: Optional[Dict[str, str]] = None


@dataclass
class ProjectConfig:
    """Main project configuration."""
    project_name: str = "Unknown Project"
    project_type: str = "web-app"
    description: str = ""
    version: str = "1.0.0"
    tech_stack: List[str] = None
    architecture: str = "unknown"
    source_dirs: List[str] = None
    test_dirs: List[str] = None
    ignore_patterns: List[str] = None
    coding_standards: str = "PEP8"
    testing_framework: str = "pytest"
    ai_settings: AISettings = None
    agents: Dict[str, AgentSettings] = None
    
    def __post_init__(self):
        """Initialize default values after creation."""
        if self.tech_stack is None:
            self.tech_stack = []
        if self.source_dirs is None:
            self.source_dirs = ["src", "lib"]
        if self.test_dirs is None:
            self.test_dirs = ["tests", "test"]
        if self.ignore_patterns is None:
            self.ignore_patterns = [
                "node_modules", "__pycache__", ".git", "venv", "env",
                "build", "dist", ".pytest_cache", "*.pyc", "*.pyo"
            ]
        if self.ai_settings is None:
            self.ai_settings = AISettings()
        if self.agents is None:
            self.agents = {
                "analyzer": AgentSettings(),
                "planner": AgentSettings(),
                "modifier": AgentSettings(),
                "validator": AgentSettings()
            }


class ConfigManager:
    """Manages project configuration."""
    
    def __init__(self, path_manager: PathManager):
        """Initialize configuration manager."""
        self.path_manager = path_manager
        self._config: Optional[ProjectConfig] = None
        self._config_file = path_manager.get_config_file_path()
    
    def load_config(self) -> ProjectConfig:
        """Load configuration from file."""
        if self._config is not None:
            return self._config
        
        if not self._config_file.exists():
            self._config = self.create_default_config()
            self.save_config()
            return self._config
        
        try:
            with open(self._config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Convert nested dictionaries to dataclasses
            if 'ai_settings' in config_data:
                config_data['ai_settings'] = AISettings(**config_data['ai_settings'])
            
            if 'agents' in config_data:
                agents = {}
                for agent_name, agent_data in config_data['agents'].items():
                    agents[agent_name] = AgentSettings(**agent_data)
                config_data['agents'] = agents
            
            self._config = ProjectConfig(**config_data)
            return self._config
            
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            print(f"Warning: Error loading config file: {e}")
            print("Creating default configuration...")
            self._config = self.create_default_config()
            self.save_config()
            return self._config
    
    def save_config(self, config: Optional[ProjectConfig] = None) -> None:
        """Save configuration to file."""
        if config is None:
            config = self._config
        
        if config is None:
            raise ValueError("No configuration to save")
        
        # Ensure directory exists
        self.path_manager.ensure_file_directory(self._config_file)
        
        # Convert dataclasses to dictionaries
        config_dict = asdict(config)
        
        try:
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            self._config = config
            
        except (OSError, json.JSONEncodeError) as e:
            raise RuntimeError(f"Failed to save configuration: {e}")
    
    def create_default_config(self, project_type: Optional[str] = None) -> ProjectConfig:
        """Create default configuration."""
        project_root = self.path_manager.get_project_root()
        
        config = ProjectConfig(
            project_name=project_root.name,
            project_type=project_type or "web-app",
            description=f"Project in {project_root}",
        )
        
        # Customize based on project type
        if project_type:
            config = self._customize_config_for_type(config, project_type)
        
        return config
    
    def _customize_config_for_type(self, config: ProjectConfig, project_type: str) -> ProjectConfig:
        """Customize configuration based on project type."""
        type_configs = {
            "web-app": {
                "tech_stack": ["HTML", "CSS", "JavaScript"],
                "source_dirs": ["src", "public", "components"],
                "architecture": "MVC"
            },
            "mobile-app": {
                "tech_stack": ["React Native", "JavaScript"],
                "source_dirs": ["src", "components", "screens"],
                "architecture": "Component-based"
            },
            "api": {
                "tech_stack": ["Python", "Flask/FastAPI"],
                "source_dirs": ["src", "api", "models"],
                "architecture": "REST/GraphQL"
            },
            "library": {
                "tech_stack": ["Python"],
                "source_dirs": ["src", "lib"],
                "architecture": "Modular"
            },
            "microservice": {
                "tech_stack": ["Python", "Docker"],
                "source_dirs": ["src", "services"],
                "architecture": "Microservices"
            }
        }
        
        if project_type in type_configs:
            type_config = type_configs[project_type]
            config.tech_stack = type_config.get("tech_stack", config.tech_stack)
            config.source_dirs = type_config.get("source_dirs", config.source_dirs)
            config.architecture = type_config.get("architecture", config.architecture)
        
        return config
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """Update configuration with new values."""
        config = self.load_config()
        
        for key, value in updates.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        self.save_config(config)
    
    def get_config(self) -> ProjectConfig:
        """Get current configuration."""
        return self.load_config()
    
    def get_ai_settings(self) -> AISettings:
        """Get AI settings."""
        config = self.load_config()
        return config.ai_settings
    
    def get_agent_settings(self, agent_name: str) -> AgentSettings:
        """Get settings for a specific agent."""
        config = self.load_config()
        return config.agents.get(agent_name, AgentSettings())
    
    def is_agent_enabled(self, agent_name: str) -> bool:
        """Check if an agent is enabled."""
        agent_settings = self.get_agent_settings(agent_name)
        return agent_settings.enabled
    
    def get_source_directories(self) -> List[Path]:
        """Get source directories as Path objects."""
        config = self.load_config()
        return [self.path_manager.resolve_path(dir_name) for dir_name in config.source_dirs]
    
    def get_test_directories(self) -> List[Path]:
        """Get test directories as Path objects."""
        config = self.load_config()
        return [self.path_manager.resolve_path(dir_name) for dir_name in config.test_dirs]
    
    def should_ignore_path(self, path: Path) -> bool:
        """Check if a path should be ignored based on ignore patterns."""
        config = self.load_config()
        path_str = str(path)
        
        for pattern in config.ignore_patterns:
            if pattern in path_str:
                return True
        
        return False
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return list of issues."""
        issues = []
        config = self.load_config()
        
        # Check required fields
        if not config.project_name:
            issues.append("Project name is required")
        
        if not config.project_type:
            issues.append("Project type is required")
        
        # Check directories exist
        for dir_name in config.source_dirs:
            dir_path = self.path_manager.resolve_path(dir_name)
            if not dir_path.exists():
                issues.append(f"Source directory does not exist: {dir_name}")
        
        # Check AI settings
        if config.ai_settings.max_tokens <= 0:
            issues.append("AI max_tokens must be positive")
        
        if not (0.0 <= config.ai_settings.temperature <= 2.0):
            issues.append("AI temperature must be between 0.0 and 2.0")
        
        return issues
    
    def reset_config(self, project_type: Optional[str] = None) -> None:
        """Reset configuration to defaults."""
        self._config = self.create_default_config(project_type)
        self.save_config()
    
    def export_config(self, export_path: Path) -> None:
        """Export configuration to a file."""
        config = self.load_config()
        config_dict = asdict(config)
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
    
    def import_config(self, import_path: Path) -> None:
        """Import configuration from a file."""
        with open(import_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        # Convert to ProjectConfig
        if 'ai_settings' in config_data:
            config_data['ai_settings'] = AISettings(**config_data['ai_settings'])
        
        if 'agents' in config_data:
            agents = {}
            for agent_name, agent_data in config_data['agents'].items():
                agents[agent_name] = AgentSettings(**agent_data)
            config_data['agents'] = agents
        
        config = ProjectConfig(**config_data)
        self.save_config(config)
    
    def __str__(self) -> str:
        """String representation."""
        config = self.load_config()
        return f"ConfigManager(project={config.project_name}, type={config.project_type})"