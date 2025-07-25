"""
Enhanced Variable Elimination Solver for Rational Inequalities.

This package implements a sequential variable elimination approach for solving
systems of rational inequalities. Variables are eliminated one by one using
min/max decomposition, which can handle complex constraint systems at the cost
of potentially generating many more inequality cases.

Main Components:
- VariableEliminationSolver: Core solver class
- solve_with_elimination: High-level interface function
- LaTeX report generation with step-by-step documentation

Example Usage:
    from enhanced_solver import solve_with_elimination
    
    inequalities = [
        "x1**2 + x2 - 4 >= 0",
        "x1 + 2*x2 <= 1", 
        "x2 - x3 > 0"
    ]
    
    variables = ['x1', 'x2', 'x3']
    
    result = solve_with_elimination(inequalities, variables)
"""

from .enhanced_solver import solve_with_elimination
from .core.variable_eliminator import VariableEliminationSolver

__version__ = "1.0.0"
__author__ = "Enhanced Rational Inequality Solver"

__all__ = [
    'solve_with_elimination',
    'VariableEliminationSolver'
]
