"""
Rational Inequality Solver Package

A dual-approach symbolic mathematics system for solving rational inequalities using SymPy.
The architecture provides two complementary solving strategies with a unified inequality treatment.

Main Components:
- case_system: Hierarchical case management infrastructure
- eliminator: Core 4-step variable elimination engine  
- latex_generator: Professional LaTeX document generation
- solver: Traditional single-variable case-by-case solver
- input_processor: Input validation and standardization
- sign_analyzer: Optional optimization for impossible case elimination
- demo: Demonstration and testing functions
- main: Clean entry point

Usage:
    from eliminator import HierarchicalCaseEliminator
    
    inequalities = [("x1 + x2", "<=", "a"), ("x1", ">=", "b")]
    variables_to_eliminate = ['x1', 'x2']
    
    eliminator = HierarchicalCaseEliminator()
    final_cases = eliminator.eliminate_variables_hierarchical(inequalities, variables_to_eliminate)

Author: Simplified Rational Inequality Solver Team
Version: Pure Inequality System - No Constraint/Inequality Separation
"""

__version__ = "2.0.0"
__author__ = "Simplified Rational Inequality Solver Team"

# Main components
from .case_system import CaseNamingSystem, HierarchicalCase
from .eliminator import HierarchicalCaseEliminator
from .latex_generator import HierarchicalLatexGenerator
from .demo import demonstrate_enhanced_variable_elimination

# Supporting components
from .input_processor import process_inequalities
from .sign_analyzer import create_default_analyzer
from .solver import solve_rational_ineq_full

__all__ = [
    'CaseNamingSystem',
    'HierarchicalCase', 
    'HierarchicalCaseEliminator',
    'HierarchicalLatexGenerator',
    'demonstrate_enhanced_variable_elimination',
    'process_inequalities',
    'create_default_analyzer',
    'solve_rational_ineq_full'
]
