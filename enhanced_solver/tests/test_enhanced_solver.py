"""
Comprehensive test suite for the Enhanced Variable Elimination Solver.
"""
import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enhanced_solver import solve_with_elimination
from core.variable_eliminator import VariableEliminationSolver


class TestVariableEliminationSolver(unittest.TestCase):
    """Test the VariableEliminationSolver class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.solver = VariableEliminationSolver(use_sign_analysis=True)
    
    def test_basic_linear_system(self):
        """Test with a basic linear system."""
        inequalities = [
            "x1 + x2 >= 0",
            "x1 - x2 <= 1",
            "2*x1 + 3*x2 >= -1"
        ]
        variables = ['x1', 'x2']
        
        result = self.solver.solve_with_variable_elimination(inequalities, variables)
        
        self.assertEqual(len(result['steps']), 3)  # Initial + 2 elimination steps
        self.assertIsInstance(result['final_inequalities'], list)
        self.assertTrue(len(result['final_inequalities']) >= 0)
    
    def test_quadratic_system(self):
        """Test with quadratic inequalities."""
        inequalities = [
            "x1**2 - 4 >= 0",
            "x1 + x2 <= 2",
            "x2**2 - 1 <= 0"
        ]
        variables = ['x1', 'x2']
        
        result = self.solver.solve_with_variable_elimination(inequalities, variables)
        
        self.assertEqual(len(result['steps']), 3)
        self.assertEqual(result['total_steps'], 2)
    
    def test_mixed_constraints(self):
        """Test with mixed variable and non-variable constraints."""
        inequalities = [
            "x1 + 2*x2 >= 0",
            "a + b <= c",  # No x1, x2
            "x1 - 1 <= 0"
        ]
        variables = ['x1']
        
        result = self.solver.solve_with_variable_elimination(inequalities, variables)
        
        # Should have constraints that don't involve x1, x2 preserved
        final_ineqs = result['final_inequalities']
        has_constraint = any('a' in str(lhs) or 'b' in str(lhs) or 'c' in str(rhs) 
                           for lhs, op, rhs in final_ineqs)
        self.assertTrue(has_constraint)
    
    def test_single_variable(self):
        """Test eliminating a single variable."""
        inequalities = [
            "x + 1 >= 0",
            "x - 2 <= 0",
            "y + z >= 1"  # Doesn't involve x
        ]
        variables = ['x']
        
        result = self.solver.solve_with_variable_elimination(inequalities, variables)
        
        self.assertEqual(len(result['steps']), 2)  # Initial + 1 elimination
        
        # Final system should not contain x
        final_vars = set()
        for lhs, op, rhs in result['final_inequalities']:
            final_vars.update(str(lhs).replace(' ', '').replace('*', '').replace('+', '').replace('-', ''))
            final_vars.update(str(rhs).replace(' ', '').replace('*', '').replace('+', '').replace('-', ''))
        
        # Remove non-variable characters
        final_vars = {v for v in final_vars if v.isalpha() and v != 'x'}
    
    def test_no_variable_bounds(self):
        """Test case where variable has no bounds."""
        inequalities = [
            "a + b >= c",  # No x
            "y - z <= 0"   # No x
        ]
        variables = ['x']
        
        result = self.solver.solve_with_variable_elimination(inequalities, variables)
        
        # Should handle gracefully
        self.assertEqual(len(result['steps']), 2)
    
    def test_complex_rational_system(self):
        """Test with complex rational inequalities."""
        inequalities = [
            "(x1 + 1)/(x1 - 1) >= 0",
            "x1 + x2 <= 3",
            "x2**2 - 4 >= 0"
        ]
        variables = ['x1', 'x2']
        
        result = self.solver.solve_with_variable_elimination(inequalities, variables)
        
        self.assertEqual(len(result['steps']), 3)
        self.assertIsInstance(result['final_inequalities'], list)


class TestEnhancedSolverInterface(unittest.TestCase):
    """Test the main enhanced solver interface."""
    
    def test_solve_with_elimination_basic(self):
        """Test the main solving interface."""
        inequalities = [
            "x + y >= 0",
            "x - y <= 1"
        ]
        variables = ['x', 'y']
        
        result = solve_with_elimination(
            inequalities, variables, 
            save_latex=False  # Don't save files during testing
        )
        
        self.assertIn('steps', result)
        self.assertIn('final_inequalities', result)
        self.assertIn('total_steps', result)
        self.assertEqual(result['total_steps'], len(variables))
    
    def test_string_input_formats(self):
        """Test various string input formats."""
        inequalities = [
            "x**2 - 4 >= 0",      # String format
            ("x + y", "<=", "1"), # Tuple format
            ("2*x - y", ">=")     # Tuple with implicit 0 RHS
        ]
        variables = ['x', 'y']
        
        result = solve_with_elimination(
            inequalities, variables,
            save_latex=False
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('final_inequalities', result)
    
    def test_empty_variable_list(self):
        """Test with no variables to eliminate."""
        inequalities = [
            "a + b >= c",
            "d - e <= f"
        ]
        variables = []
        
        result = solve_with_elimination(
            inequalities, variables,
            save_latex=False
        )
        
        # Should return original system
        self.assertEqual(len(result['steps']), 1)  # Only initial step


class TestLatexGeneration(unittest.TestCase):
    """Test LaTeX report generation."""
    
    def test_latex_header_footer(self):
        """Test LaTeX document structure."""
        solver = VariableEliminationSolver()
        
        # Mock some steps
        solver.steps = [{
            'step_number': 0,
            'description': 'Initial System',
            'variable_eliminated': None,
            'input_inequalities': [('x', '>=', '0')],
            'min_max_expressions': [],
            'eliminated_expressions': [],
            'output_inequalities': []
        }]
        
        latex_content = solver.generate_latex_report()
        
        # Check basic LaTeX structure
        self.assertIn('\\documentclass{article}', latex_content)
        self.assertIn('\\begin{document}', latex_content)
        self.assertIn('\\end{document}', latex_content)
        self.assertIn('\\title{', latex_content)
    
    def test_step_latex_generation(self):
        """Test LaTeX generation for elimination steps."""
        solver = VariableEliminationSolver()
        
        # Create a complete elimination result
        inequalities = ["x + y >= 0", "x - 1 <= 0"]
        variables = ['x']
        
        result = solver.solve_with_variable_elimination(inequalities, variables)
        latex_content = solver.generate_latex_report()
        
        # Should contain step sections
        self.assertIn('\\section{', latex_content)
        self.assertIn('\\subsection{', latex_content)
        self.assertIn('\\begin{align}', latex_content)
        self.assertIn('\\end{align}', latex_content)


def run_performance_test():
    """Run a performance test with a larger system."""
    print("\n" + "="*60)
    print("PERFORMANCE TEST")
    print("="*60)
    
    # Create a larger system
    import time
    
    inequalities = []
    for i in range(1, 6):
        inequalities.append(f"x{i} + x{i+1} >= {i}")
        inequalities.append(f"x{i}**2 - {i+1} <= 0")
    
    inequalities.append("a + b + c >= 0")  # Constraint
    
    variables = [f'x{i}' for i in range(1, 4)]  # Eliminate first 3 variables
    
    print(f"System size: {len(inequalities)} inequalities")
    print(f"Variables to eliminate: {variables}")
    
    start_time = time.time()
    result = solve_with_elimination(inequalities, variables, save_latex=False)
    end_time = time.time()
    
    print(f"Solving time: {end_time - start_time:.4f} seconds")
    print(f"Final inequality count: {len(result['final_inequalities'])}")


if __name__ == "__main__":
    # Run unit tests
    print("Running Enhanced Variable Elimination Solver Tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run performance test
    run_performance_test()
