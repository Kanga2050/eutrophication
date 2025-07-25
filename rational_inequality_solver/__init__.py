"""
Rational Inequality Solver Package

A modular Python package for solving rational inequalities symbolically with LaTeX output formatting.

Main Components:
- Core solver engine with sign analysis optimization
- Flexible input processing supporting multiple formats
- Case-based output generation with LaTeX formatting
- Comprehensive example library
- Extensible processor architecture

Usage:
    from rational_inequality_solver import solve_inequality_system
    from rational_inequality_solver.examples import get_example
    
    # Quick solve
    results = solve_inequality_system(inequalities, variable='x')
    
    # With examples
    example_ineqs = get_example('quadratic')
    results = solve_inequality_system(example_ineqs)
"""

__version__ = "2.0.0"
__author__ = "Rational Inequality Solver Team"

# Main API imports
from .core.solver_engine import SolverEngine
from .core.inequality_system import InequalitySystem
from .processors.input_processor import InputProcessor
from .processors.case_processor import CaseProcessor
from .output.latex_formatter import LaTeXFormatter
from .output.console_formatter import ConsoleFormatter

# Convenience functions
def solve_inequality_system(inequalities, variable='x', **kwargs):
    """
    Convenient function to solve a system of rational inequalities.
    
    Args:
        inequalities: List of inequalities in various formats
        variable: Variable symbol name (default: 'x')
        **kwargs: Additional solver options
        
    Returns:
        Formatted solution results
    """
    system = InequalitySystem(inequalities, variable)
    engine = SolverEngine(**kwargs)
    return engine.solve(system)

# Package-level configuration
DEFAULT_CONFIG = {
    'use_sign_analysis': True,
    'latex_output': True,
    'console_output': True,
    'save_to_file': True,
    'output_directory': 'output'
}

__all__ = [
    'solve_inequality_system',
    'SolverEngine',
    'InequalitySystem', 
    'InputProcessor',
    'CaseProcessor',
    'LaTeXFormatter',
    'ConsoleFormatter',
    'DEFAULT_CONFIG'
]
