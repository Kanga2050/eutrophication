"""
Main interface for the Enhanced Variable Elimination Solver.

This module provides the primary interface for solving rational inequality systems
with sequential variable elimination.
"""
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.variable_eliminator import VariableEliminationSolver


def solve_with_elimination(inequalities, variables_to_eliminate, 
                          use_sign_analysis=True, save_latex=True, 
                          output_filename=None):
    """
    Solve a system of rational inequalities by eliminating variables sequentially.
    
    Args:
        inequalities: List of inequalities in supported formats:
                     - String: "x**2 - 4 >= 0"
                     - Tuple: (lhs, op, rhs) or (expr, op)
        variables_to_eliminate: List of variable names ['x1', 'x2', 'x3', ...]
        use_sign_analysis: Whether to use sign analysis optimization
        save_latex: Whether to save LaTeX output to file
        output_filename: Custom filename for output (optional)
        
    Returns:
        dict: Complete solution with steps and final inequalities
    """
    print("=" * 80)
    print("ENHANCED VARIABLE ELIMINATION SOLVER")
    print("=" * 80)
    print(f"Input: {len(inequalities)} inequalities")
    print(f"Variables to eliminate: {variables_to_eliminate}")
    print(f"Sign analysis: {'Enabled' if use_sign_analysis else 'Disabled'}")
    print()
    
    # Initialize solver
    solver = VariableEliminationSolver(use_sign_analysis=use_sign_analysis)
    
    # Solve the system
    result = solver.solve_with_variable_elimination(inequalities, variables_to_eliminate)
    
    # Generate LaTeX report
    if save_latex:
        latex_content = solver.generate_latex_report()
        
        # Generate filename if not provided
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"variable_elimination_{timestamp}"
        
        # Save to standard output folder
        output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(output_dir, exist_ok=True)
        
        latex_file = os.path.join(output_dir, f"{output_filename}.tex")
        with open(latex_file, 'w') as f:
            f.write(latex_content)
        
        print(f"LaTeX report saved to: {latex_file}")
        
        # Save complete LaTeX report to output_final folder
        output_final_dir = os.path.join(os.path.dirname(__file__), "output_final")
        os.makedirs(output_final_dir, exist_ok=True)
        
        final_latex_file = os.path.join(output_final_dir, f"{output_filename}_complete.tex")
        with open(final_latex_file, 'w') as f:
            f.write(latex_content)
        
        print(f"Complete LaTeX report saved to: {final_latex_file}")
        print()
        
        # Also save raw text summary
        text_file = os.path.join(output_dir, f"{output_filename}_summary.txt")
        with open(text_file, 'w') as f:
            f.write(generate_text_summary(result))
        
        print(f"Text summary saved to: {text_file}")
        print()
    
    # Print summary
    print_solution_summary(result)
    
    return result


def print_solution_summary(result):
    """Print a summary of the solution to console."""
    print("SOLUTION SUMMARY")
    print("-" * 40)
    print(f"Total elimination steps: {result['total_steps']}")
    print(f"Final number of inequalities: {len(result['final_inequalities'])}")
    print()
    
    for step in result['steps']:
        if step['step_number'] == 0:
            print(f"Step {step['step_number']}: {step['description']}")
            print(f"  Initial inequalities: {len(step['input_inequalities'])}")
        else:
            print(f"Step {step['step_number']}: {step['description']}")
            print(f"  Variable eliminated: {step['variable_eliminated']}")
            print(f"  Input inequalities: {len(step['input_inequalities'])}")
            print(f"  Output inequalities: {len(step['output_inequalities'])}")
            
            min_max = step['min_max_expressions']
            print(f"  Lower bounds found: {len(min_max['lower_bounds'])}")
            print(f"  Upper bounds found: {len(min_max['upper_bounds'])}")
        print()


def generate_text_summary(result):
    """Generate a text summary of the solution."""
    summary = []
    summary.append("VARIABLE ELIMINATION SOLVER - SUMMARY REPORT")
    summary.append("=" * 60)
    summary.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append(f"Total steps: {result['total_steps']}")
    summary.append(f"Final inequalities: {len(result['final_inequalities'])}")
    summary.append("")
    
    for step in result['steps']:
        summary.append(f"STEP {step['step_number']}: {step['description']}")
        summary.append("-" * 40)
        
        if step['step_number'] == 0:
            summary.append("Initial system:")
            for lhs, op, rhs in step['input_inequalities']:
                summary.append(f"  {lhs} {op} {rhs}")
        else:
            summary.append(f"Variable eliminated: {step['variable_eliminated']}")
            summary.append("")
            
            summary.append("Input inequalities:")
            for lhs, op, rhs in step['input_inequalities']:
                summary.append(f"  {lhs} {op} {rhs}")
            summary.append("")
            
            min_max = step['min_max_expressions']
            if min_max['lower_bounds']:
                summary.append("Lower bounds:")
                for bound in min_max['lower_bounds']:
                    summary.append(f"  {step['variable_eliminated']} > {bound['expression']}")
                summary.append("")
            
            if min_max['upper_bounds']:
                summary.append("Upper bounds:")
                for bound in min_max['upper_bounds']:
                    summary.append(f"  {step['variable_eliminated']} < {bound['expression']}")
                summary.append("")
            
            summary.append("Output inequalities:")
            for lhs, op, rhs in step['output_inequalities']:
                summary.append(f"  {lhs} {op} {rhs}")
        
        summary.append("")
    
    summary.append("FINAL SYSTEM:")
    summary.append("-" * 40)
    for lhs, op, rhs in result['final_inequalities']:
        summary.append(f"  {lhs} {op} {rhs}")
    
    return "\n".join(summary)


if __name__ == "__main__":
    # Example usage
    from sympy import symbols
    
    # Define test inequalities
    test_inequalities = [
        "x1**2 + x2 - 4 >= 0",
        "x1 + 2*x2 - 1 <= 0", 
        "x2 - x3 + 1 > 0",
        "a + b <= c"  # Constraint not involving variables to eliminate
    ]
    
    variables = ['x1', 'x2', 'x3']
    
    print("Running example with variable elimination...")
    result = solve_with_elimination(test_inequalities, variables)
