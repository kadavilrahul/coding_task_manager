"""
Code template generator for various programming patterns and structures.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from ..utils.file_utils import FileUtils


class TemplateType(Enum):
    """Types of code templates."""
    CLASS = "class"
    FUNCTION = "function"
    MODULE = "module"
    API_ENDPOINT = "api_endpoint"
    TEST_CASE = "test_case"
    CONFIG = "config"
    SCRIPT = "script"
    INTERFACE = "interface"


class LanguageType(Enum):
    """Supported programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CSHARP = "csharp"
    GO = "go"


@dataclass
class TemplateParameter:
    """Template parameter specification."""
    name: str
    type: str
    description: str
    default_value: Optional[str] = None
    required: bool = True


@dataclass
class CodeTemplate:
    """Code template definition."""
    name: str
    type: TemplateType
    language: LanguageType
    description: str
    parameters: List[TemplateParameter]
    template_content: str
    dependencies: List[str]
    examples: List[str]


class CodeTemplateGenerator:
    """Generate code templates for various programming patterns."""
    
    def __init__(self):
        """Initialize the code template generator."""
        self.templates = {}
        self._load_default_templates()
    
    def generate_code(self, template_name: str, parameters: Dict[str, Any]) -> str:
        """Generate code from a template with given parameters."""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = self.templates[template_name]
        
        # Validate required parameters
        self._validate_parameters(template, parameters)
        
        # Generate code
        code = self._render_template(template, parameters)
        
        # Add header comment
        header = self._generate_header_comment(template, parameters)
        
        return f"{header}\n\n{code}"
    
    def _validate_parameters(self, template: CodeTemplate, parameters: Dict[str, Any]):
        """Validate that all required parameters are provided."""
        for param in template.parameters:
            if param.required and param.name not in parameters:
                raise ValueError(f"Required parameter '{param.name}' not provided")
    
    def _render_template(self, template: CodeTemplate, parameters: Dict[str, Any]) -> str:
        """Render template with parameters."""
        content = template.template_content
        
        # Replace parameter placeholders
        for param in template.parameters:
            value = parameters.get(param.name, param.default_value)
            if value is not None:
                placeholder = f"{{{param.name}}}"
                content = content.replace(placeholder, str(value))
        
        return content
    
    def _generate_header_comment(self, template: CodeTemplate, parameters: Dict[str, Any]) -> str:
        """Generate header comment for the generated code."""
        if template.language == LanguageType.PYTHON:
            return f'"""\n{template.description}\n\nGenerated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\nTemplate: {template.name}\n"""'
        elif template.language in [LanguageType.JAVASCRIPT, LanguageType.TYPESCRIPT]:
            return f'/**\n * {template.description}\n * \n * Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n * Template: {template.name}\n */'
        elif template.language == LanguageType.JAVA:
            return f'/**\n * {template.description}\n * \n * Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n * Template: {template.name}\n */'
        else:
            return f'// {template.description}\n// Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n// Template: {template.name}'
    
    def _load_default_templates(self):
        """Load default code templates."""
        # Python class template
        self.templates["python_class"] = CodeTemplate(
            name="python_class",
            type=TemplateType.CLASS,
            language=LanguageType.PYTHON,
            description="Python class template with common patterns",
            parameters=[
                TemplateParameter("class_name", "str", "Name of the class", required=True),
                TemplateParameter("base_class", "str", "Base class to inherit from", default_value="", required=False),
                TemplateParameter("docstring", "str", "Class docstring", default_value="Class description.", required=False),
                TemplateParameter("init_params", "str", "Constructor parameters", default_value="", required=False),
                TemplateParameter("methods", "str", "Additional methods", default_value="", required=False)
            ],
            template_content=self._get_python_class_template(),
            dependencies=["typing"],
            examples=["Basic class", "Class with inheritance", "Data class"]
        )
        
        # Python function template
        self.templates["python_function"] = CodeTemplate(
            name="python_function",
            type=TemplateType.FUNCTION,
            language=LanguageType.PYTHON,
            description="Python function template with type hints and documentation",
            parameters=[
                TemplateParameter("function_name", "str", "Name of the function", required=True),
                TemplateParameter("parameters", "str", "Function parameters with type hints", default_value="", required=False),
                TemplateParameter("return_type", "str", "Return type annotation", default_value="None", required=False),
                TemplateParameter("docstring", "str", "Function docstring", default_value="Function description.", required=False),
                TemplateParameter("body", "str", "Function body", default_value="pass", required=False)
            ],
            template_content=self._get_python_function_template(),
            dependencies=["typing"],
            examples=["Simple function", "Function with parameters", "Async function"]
        )
        
        # Python API endpoint template
        self.templates["python_api_endpoint"] = CodeTemplate(
            name="python_api_endpoint",
            type=TemplateType.API_ENDPOINT,
            language=LanguageType.PYTHON,
            description="FastAPI endpoint template",
            parameters=[
                TemplateParameter("endpoint_name", "str", "Name of the endpoint", required=True),
                TemplateParameter("http_method", "str", "HTTP method (GET, POST, etc.)", default_value="GET", required=False),
                TemplateParameter("path", "str", "URL path", required=True),
                TemplateParameter("request_model", "str", "Request model class", default_value="", required=False),
                TemplateParameter("response_model", "str", "Response model class", default_value="", required=False),
                TemplateParameter("description", "str", "Endpoint description", default_value="API endpoint", required=False)
            ],
            template_content=self._get_python_api_template(),
            dependencies=["fastapi", "pydantic"],
            examples=["GET endpoint", "POST endpoint", "Endpoint with validation"]
        )
        
        # Python test case template
        self.templates["python_test"] = CodeTemplate(
            name="python_test",
            type=TemplateType.TEST_CASE,
            language=LanguageType.PYTHON,
            description="Python unittest template",
            parameters=[
                TemplateParameter("test_class", "str", "Test class name", required=True),
                TemplateParameter("target_class", "str", "Class being tested", required=True),
                TemplateParameter("test_methods", "str", "Test methods", default_value="", required=False)
            ],
            template_content=self._get_python_test_template(),
            dependencies=["unittest", "pytest"],
            examples=["Unit test", "Integration test", "Mock test"]
        )
        
        # JavaScript class template
        self.templates["javascript_class"] = CodeTemplate(
            name="javascript_class",
            type=TemplateType.CLASS,
            language=LanguageType.JAVASCRIPT,
            description="JavaScript ES6 class template",
            parameters=[
                TemplateParameter("class_name", "str", "Name of the class", required=True),
                TemplateParameter("constructor_params", "str", "Constructor parameters", default_value="", required=False),
                TemplateParameter("methods", "str", "Class methods", default_value="", required=False)
            ],
            template_content=self._get_javascript_class_template(),
            dependencies=[],
            examples=["Basic class", "Class with methods", "Class with inheritance"]
        )
    
    def _get_python_class_template(self) -> str:
        """Get Python class template."""
        return '''from typing import Any, Dict, List, Optional


class {class_name}{base_class}:
    """{docstring}"""
    
    def __init__(self{init_params}):
        """Initialize the {class_name}."""
        {init_body}
    
    def __str__(self) -> str:
        """String representation of the {class_name}."""
        return f"{class_name}()"
    
    def __repr__(self) -> str:
        """Developer representation of the {class_name}."""
        return self.__str__()
    
{methods}'''
    
    def _get_python_function_template(self) -> str:
        """Get Python function template."""
        return '''def {function_name}({parameters}) -> {return_type}:
    """{docstring}
    
    Args:
        {args_doc}
    
    Returns:
        {return_doc}
    
    Raises:
        {raises_doc}
    """
    {body}'''
    
    def _get_python_api_template(self) -> str:
        """Get Python API endpoint template."""
        return '''from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

router = APIRouter()


{request_model}


{response_model}


@router.{http_method_lower}("{path}")
async def {endpoint_name}({endpoint_params}) -> {response_type}:
    """{description}
    
    Args:
        {args_doc}
    
    Returns:
        {return_doc}
    
    Raises:
        HTTPException: If operation fails
    """
    try:
        # Implementation here
        {implementation}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))'''
    
    def _get_python_test_template(self) -> str:
        """Get Python test template."""
        return '''import unittest
from unittest.mock import Mock, patch, MagicMock
import pytest

from {module_path} import {target_class}


class {test_class}(unittest.TestCase):
    """Test cases for {target_class}."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.{target_instance} = {target_class}()
    
    def tearDown(self):
        """Clean up after each test method."""
        pass
    
    def test_{test_method_name}(self):
        """Test {test_description}."""
        # Arrange
        {arrange_code}
        
        # Act
        {act_code}
        
        # Assert
        {assert_code}
    
{test_methods}


if __name__ == '__main__':
    unittest.main()'''
    
    def _get_javascript_class_template(self) -> str:
        """Get JavaScript class template."""
        return '''class {class_name} {{
    /**
     * Create a new {class_name}.
     * @param {{{constructor_param_types}}} {constructor_params}
     */
    constructor({constructor_params}) {{
        {constructor_body}
    }}
    
    /**
     * String representation of the {class_name}.
     * @returns {{string}} String representation
     */
    toString() {{
        return `{class_name}()`;
    }}
    
{methods}
}}

export default {class_name};'''
    
    def generate_module_template(self, module_name: str, language: LanguageType, 
                               components: List[str]) -> str:
        """Generate a complete module template."""
        if language == LanguageType.PYTHON:
            return self._generate_python_module(module_name, components)
        elif language == LanguageType.JAVASCRIPT:
            return self._generate_javascript_module(module_name, components)
        else:
            raise ValueError(f"Unsupported language: {language}")
    
    def _generate_python_module(self, module_name: str, components: List[str]) -> str:
        """Generate Python module template."""
        header = f'"""\n{module_name.replace("_", " ").title()} module.\n\nGenerated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n"""'
        
        imports = [
            "from typing import Any, Dict, List, Optional, Union",
            "from pathlib import Path",
            "from dataclasses import dataclass",
            "from enum import Enum"
        ]
        
        content = [header, ""]
        content.extend(imports)
        content.extend(["", ""])
        
        # Add components
        for component in components:
            if component == "class":
                content.extend([
                    f"class {module_name.title().replace('_', '')}:",
                    f'    """Main class for {module_name} module."""',
                    "",
                    "    def __init__(self):",
                    f'        """Initialize the {module_name.title().replace("_", "")}."""',
                    "        pass",
                    "",
                    ""
                ])
            elif component == "function":
                content.extend([
                    f"def {module_name}_function() -> None:",
                    f'    """Main function for {module_name} module."""',
                    "    pass",
                    "",
                    ""
                ])
        
        # Add __all__ export
        exports = [comp.replace("class", module_name.title().replace('_', '')) 
                  for comp in components if comp == "class"]
        exports.extend([f"{module_name}_function" for comp in components if comp == "function"])
        
        if exports:
            content.extend([
                "__all__ = [",
                *[f"    '{export}'," for export in exports],
                "]"
            ])
        
        return '\n'.join(content)
    
    def _generate_javascript_module(self, module_name: str, components: List[str]) -> str:
        """Generate JavaScript module template."""
        header = f"/**\n * {module_name.replace('_', ' ').title()} module.\n * \n * Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n */"
        
        content = [header, ""]
        
        # Add components
        exports = []
        for component in components:
            if component == "class":
                class_name = module_name.title().replace('_', '')
                content.extend([
                    f"class {class_name} {{",
                    f"    /**",
                    f"     * Create a new {class_name}.",
                    f"     */",
                    "    constructor() {",
                    "        // Initialize here",
                    "    }",
                    "}",
                    ""
                ])
                exports.append(class_name)
            elif component == "function":
                func_name = f"{module_name}Function"
                content.extend([
                    f"/**",
                    f" * Main function for {module_name} module.",
                    f" * @returns {{void}}",
                    f" */",
                    f"function {func_name}() {{",
                    "    // Implementation here",
                    "}",
                    ""
                ])
                exports.append(func_name)
        
        # Add exports
        if exports:
            content.extend([
                "export {",
                *[f"    {export}," for export in exports],
                "};"
            ])
        
        return '\n'.join(content)
    
    def generate_config_template(self, config_type: str, language: LanguageType) -> str:
        """Generate configuration file template."""
        if language == LanguageType.PYTHON:
            if config_type == "settings":
                return self._get_python_settings_template()
            elif config_type == "logging":
                return self._get_python_logging_template()
        
        return ""
    
    def _get_python_settings_template(self) -> str:
        """Get Python settings configuration template."""
        return '''"""
Application settings configuration.
"""

import os
from typing import Any, Dict, List, Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings."""
    
    # Application settings
    app_name: str = Field(default="My Application", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Database settings
    database_url: str = Field(default="sqlite:///./app.db", env="DATABASE_URL")
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")
    
    # API settings
    api_host: str = Field(default="localhost", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_prefix: str = Field(default="/api/v1", env="API_PREFIX")
    
    # Security settings
    secret_key: str = Field(default="your-secret-key", env="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Logging settings
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Optional[str] = Field(default=None, env="LOG_FILE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()'''
    
    def _get_python_logging_template(self) -> str:
        """Get Python logging configuration template."""
        return '''"""
Logging configuration.
"""

import logging
import logging.config
from typing import Dict, Any


LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "app.log",
            "mode": "a"
        }
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False
        }
    }
}


def setup_logging(config: Dict[str, Any] = None) -> None:
    """Setup logging configuration."""
    if config is None:
        config = LOGGING_CONFIG
    
    logging.config.dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)'''
    
    def list_templates(self, template_type: Optional[TemplateType] = None, 
                      language: Optional[LanguageType] = None) -> List[str]:
        """List available templates."""
        templates = []
        
        for name, template in self.templates.items():
            if template_type and template.type != template_type:
                continue
            if language and template.language != language:
                continue
            templates.append(name)
        
        return sorted(templates)
    
    def get_template_info(self, template_name: str) -> Optional[CodeTemplate]:
        """Get information about a specific template."""
        return self.templates.get(template_name)
    
    def add_custom_template(self, template: CodeTemplate) -> None:
        """Add a custom template."""
        self.templates[template.name] = template
    
    def save_template(self, template_name: str, file_path: Path) -> None:
        """Save a template to a file."""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = self.templates[template_name]
        content = {
            "name": template.name,
            "type": template.type.value,
            "language": template.language.value,
            "description": template.description,
            "parameters": [
                {
                    "name": p.name,
                    "type": p.type,
                    "description": p.description,
                    "default_value": p.default_value,
                    "required": p.required
                }
                for p in template.parameters
            ],
            "template_content": template.template_content,
            "dependencies": template.dependencies,
            "examples": template.examples
        }
        
        FileUtils.write_json(file_path, content)
    
    def load_template(self, file_path: Path) -> None:
        """Load a template from a file."""
        if not FileUtils.file_exists(file_path):
            raise FileNotFoundError(f"Template file not found: {file_path}")
        
        data = FileUtils.read_json(file_path)
        
        parameters = [
            TemplateParameter(
                name=p["name"],
                type=p["type"],
                description=p["description"],
                default_value=p.get("default_value"),
                required=p.get("required", True)
            )
            for p in data["parameters"]
        ]
        
        template = CodeTemplate(
            name=data["name"],
            type=TemplateType(data["type"]),
            language=LanguageType(data["language"]),
            description=data["description"],
            parameters=parameters,
            template_content=data["template_content"],
            dependencies=data.get("dependencies", []),
            examples=data.get("examples", [])
        )
        
        self.templates[template.name] = template