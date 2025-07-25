"""
Enhanced example library with better organization.
"""
from typing import Dict, List, Tuple, Any
from sympy import symbols

from ..core.inequality_system import InequalitySystem


class ExampleLibrary:
    """Library of example inequality systems for testing and demonstration."""
    
    def __init__(self):
        """Initialize example library."""
        self._examples = self._build_example_catalog()
    
    def _build_example_catalog(self) -> Dict[str, Dict[str, Any]]:
        """Build the catalog of examples."""
        x, a, b, c, d, e, f, g = symbols('x a b c d e f g')
        
        return {
            'quadratic_simple': {
                'inequalities': [
                    (x**2 - 4, ">=", 0),
                    (x + 1, ">", 0),
                ],
                'description': "Simple quadratic inequality system",
                'difficulty': 'beginner',
                'expected_cases': 2,
            },
            
            'rational_basic': {
                'inequalities': [
                    ((x - 1)/(x + 2), "<=", 0),
                    (x, "!=", -2),
                ],
                'description': "Basic rational function with singularity",
                'difficulty': 'beginner',
                'expected_cases': 2,
            },
            
            'polynomial_cubic': {
                'inequalities': [
                    (x**3 - x, ">", 0),
                    (x**2 - 9, "<=", 0),
                ],
                'description': "Cubic polynomial with quadratic constraint",
                'difficulty': 'intermediate',
                'expected_cases': 3,
            },
            
            'parametric_linear': {
                'inequalities': [
                    (a*x + b, ">", 0),
                    (x**2 - a, "<=", b),
                    (a, ">", 0),
                ],
                'description': "Linear in x with parameter constraints",
                'difficulty': 'intermediate',
                'expected_cases': 4,
            },
            
            'complex_rational': {
                'inequalities': [
                    ((a*x - c + b - 1)/(a*b*d) - b/a + 1/a + (b*d*c)/a - 
                     (x - e*f*c + (b - 1 - b*d*c)*(e*f + g*x)) / (g*c + 1 - c*f*a - g*x), "<="),
                    ((x + 1)*(x - 2)/(x + 3), ">="),
                    (a + b, "<=", c),
                ],
                'description': "Complex rational inequality with multiple parameters",
                'difficulty': 'advanced',
                'expected_cases': 8,
            },
            
            'mixed_types': {
                'inequalities': [
                    (x**2 - 2*x - 3, ">=", 0),  # Quadratic
                    ((x - 1)/(x + 1), "<", 1),   # Rational
                    (x, ">", -5),                # Linear constraint
                ],
                'description': "Mixed polynomial and rational inequalities",
                'difficulty': 'intermediate',
                'expected_cases': 4,
            },
            
            'trigonometric_bounds': {
                'inequalities': [
                    (x**2 - 1, "<=", 0),
                    (x, ">=", -1),
                    (x, "<=", 1),
                ],
                'description': "Bounded domain example",
                'difficulty': 'beginner',
                'expected_cases': 1,
            },
            
            'absolute_value': {
                'inequalities': [
                    (x**2 - 4, ">=", 0),
                    (-x**2 + 6*x - 5, ">=", 0),
                ],
                'description': "System resembling absolute value constraints",
                'difficulty': 'intermediate',
                'expected_cases': 3,
            },
            
            'degenerate_cases': {
                'inequalities': [
                    (0*x + 1, ">", 0),  # Always true
                    (x**2, ">=", 0),    # Always true for real x
                    (a, ">", 0),        # Parameter constraint
                ],
                'description': "Example with degenerate/trivial cases",
                'difficulty': 'beginner',
                'expected_cases': 1,
            },
            
            'stress_test': {
                'inequalities': [
                    (x**4 - 5*x**2 + 4, "<=", 0),
                    ((x**2 - 1)/(x**2 - 4), ">=", 0),
                    (x**3 - x, "!=", 0),
                    (a*x + b, ">", c),
                    (a**2 + b**2, ">", 0),
                ],
                'description': "Complex system for stress testing",
                'difficulty': 'expert',
                'expected_cases': 16,
            }
        }
    
    def get_example(self, name: str) -> InequalitySystem:
        """
        Get an example inequality system by name.
        
        Args:
            name: Name of the example
            
        Returns:
            InequalitySystem instance
            
        Raises:
            KeyError: If example name not found
        """
        if name not in self._examples:
            available = list(self._examples.keys())
            raise KeyError(f"Example '{name}' not found. Available: {available}")
        
        example_data = self._examples[name]
        return InequalitySystem(example_data['inequalities'])
    
    def get_example_data(self, name: str) -> Dict[str, Any]:
        """
        Get complete example data including metadata.
        
        Args:
            name: Name of the example
            
        Returns:
            Dictionary with example data and metadata
        """
        if name not in self._examples:
            available = list(self._examples.keys())
            raise KeyError(f"Example '{name}' not found. Available: {available}")
        
        return self._examples[name].copy()
    
    def list_examples(self) -> List[str]:
        """Get list of available example names."""
        return list(self._examples.keys())
    
    def list_by_difficulty(self, difficulty: str) -> List[str]:
        """
        Get examples by difficulty level.
        
        Args:
            difficulty: 'beginner', 'intermediate', 'advanced', or 'expert'
            
        Returns:
            List of example names matching the difficulty
        """
        return [
            name for name, data in self._examples.items()
            if data.get('difficulty') == difficulty
        ]
    
    def get_example_info(self) -> str:
        """Get formatted information about all examples."""
        info_lines = []
        info_lines.append("Available Examples:")
        info_lines.append("-" * 50)
        
        # Group by difficulty
        difficulties = ['beginner', 'intermediate', 'advanced', 'expert']
        
        for difficulty in difficulties:
            examples_in_difficulty = self.list_by_difficulty(difficulty)
            if examples_in_difficulty:
                info_lines.append(f"\\n{difficulty.upper()}:")
                for name in examples_in_difficulty:
                    data = self._examples[name]
                    description = data.get('description', 'No description')
                    expected_cases = data.get('expected_cases', '?')
                    num_inequalities = len(data['inequalities'])
                    
                    info_lines.append(
                        f"  {name:20}: {description} "
                        f"({num_inequalities} inequalities, ~{expected_cases} cases)"
                    )
        
        info_lines.append("\\nUsage: get_example('example_name')")
        return "\\n".join(info_lines)
    
    def validate_examples(self) -> Dict[str, bool]:
        """
        Validate all examples can be created successfully.
        
        Returns:
            Dictionary mapping example names to validation status
        """
        validation_results = {}
        
        for name in self._examples:
            try:
                system = self.get_example(name)
                system.validate()
                validation_results[name] = True
            except Exception as e:
                print(f"Validation failed for '{name}': {e}")
                validation_results[name] = False
        
        return validation_results


# Global example library instance
EXAMPLE_LIBRARY = ExampleLibrary()


# Convenience functions for backward compatibility
def get_example(name: str) -> InequalitySystem:
    """Get an example inequality system."""
    return EXAMPLE_LIBRARY.get_example(name)


def list_examples() -> List[str]:
    """List available examples."""
    return EXAMPLE_LIBRARY.list_examples()


def print_example_info():
    """Print information about available examples."""
    print(EXAMPLE_LIBRARY.get_example_info())


# Individual example functions for backward compatibility
def get_complex_example() -> List[Tuple]:
    """Get the complex example."""
    return EXAMPLE_LIBRARY.get_example_data('complex_rational')['inequalities']


def get_simple_quadratic_example() -> List[Tuple]:
    """Get simple quadratic example."""
    return EXAMPLE_LIBRARY.get_example_data('quadratic_simple')['inequalities']


def get_rational_function_example() -> List[Tuple]:
    """Get rational function example."""
    return EXAMPLE_LIBRARY.get_example_data('rational_basic')['inequalities']


def get_polynomial_example() -> List[Tuple]:
    """Get polynomial example."""
    return EXAMPLE_LIBRARY.get_example_data('polynomial_cubic')['inequalities']


def get_mixed_parameters_example() -> List[Tuple]:
    """Get mixed parameters example."""
    return EXAMPLE_LIBRARY.get_example_data('parametric_linear')['inequalities']


def get_all_examples() -> Dict[str, List[Tuple]]:
    """Get all examples in the old format."""
    return {
        'complex': get_complex_example(),
        'quadratic': get_simple_quadratic_example(),
        'rational': get_rational_function_example(),
        'polynomial': get_polynomial_example(),
        'mixed_params': get_mixed_parameters_example(),
    }
