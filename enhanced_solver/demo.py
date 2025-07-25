"""
Demo script for the Enhanced Variable Elimination Solver.

This script demonstrates the capabilities of the sequential variable elimination approach
with several examples of increasing complexity.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enhanced_solver import solve_with_elimination


def demo_linear_system():
    """Demonstrate elimination on a simple linear system."""
    print("DEMO 1: Linear System")
    print("-" * 40)
    
    inequalities = [
        "x1 + x2 >= 0",
        "x1 - x2 <= 1", 
        "2*x1 + x2 >= -1"
    ]
    
    variables = ['x1', 'x2']
    
    print("Input system:")
    for ineq in inequalities:
        print(f"  {ineq}")
    print(f"Variables to eliminate: {variables}")
    print()
    
    result = solve_with_elimination(inequalities, variables, save_latex=False)
    
    print(f"Result: {len(result['final_inequalities'])} final inequalities")
    print("Final system:")
    for lhs, op, rhs in result['final_inequalities']:
        print(f"  {lhs} {op} {rhs}")
    print()


def demo_quadratic_system():
    """Demonstrate elimination on a system with quadratic inequalities."""
    print("DEMO 2: Quadratic System")
    print("-" * 40)
    
    inequalities = [
        "x1**2 - 4 >= 0",
        "x1 + x2 <= 2", 
        "x2 - 1 >= 0",
        "a + b <= c"  # Constraint not involving x1, x2
    ]
    
    variables = ['x1', 'x2']
    
    print("Input system:")
    for ineq in inequalities:
        print(f"  {ineq}")
    print(f"Variables to eliminate: {variables}")
    print()
    
    result = solve_with_elimination(inequalities, variables, save_latex=False)
    
    print(f"Result: {len(result['final_inequalities'])} final inequalities")
    print("Final system (constraints only):")
    for lhs, op, rhs in result['final_inequalities']:
        print(f"  {lhs} {op} {rhs}")
    print()


def demo_rational_system():
    """Demonstrate elimination on a system with rational inequalities."""
    print("DEMO 3: Rational System")
    print("-" * 40)
    
    inequalities = [
        "(x + 1)/(x - 1) >= 0",
        "x + y <= 3",
        "y**2 - 4 <= 0"
    ]
    
    variables = ['x', 'y']
    
    print("Input system:")
    for ineq in inequalities:
        print(f"  {ineq}")
    print(f"Variables to eliminate: {variables}")
    print()
    
    try:
        result = solve_with_elimination(inequalities, variables, save_latex=False)
        
        print(f"Result: {len(result['final_inequalities'])} final inequalities")
        print("Final system:")
        for lhs, op, rhs in result['final_inequalities']:
            print(f"  {lhs} {op} {rhs}")
    except Exception as e:
        print(f"Error in rational system demo: {e}")
        print("This demonstrates the complexity of rational inequality elimination.")
    
    print()


def demo_single_variable():
    """Demonstrate elimination of a single variable."""
    print("DEMO 4: Single Variable Elimination")
    print("-" * 40)
    
    inequalities = [
        "x >= -1",
        "x <= 2",
        "x + y >= 0",
        "y - z <= 1",
        "a + b >= c"  # Constraint
    ]
    
    variables = ['x']  # Only eliminate x
    
    print("Input system:")
    for ineq in inequalities:
        print(f"  {ineq}")
    print(f"Variables to eliminate: {variables}")
    print()
    
    result = solve_with_elimination(inequalities, variables, save_latex=False)
    
    print(f"Result: {len(result['final_inequalities'])} final inequalities")
    print("Final system (no x variables):")
    for lhs, op, rhs in result['final_inequalities']:
        print(f"  {lhs} {op} {rhs}")
    print()


def demo_complex_system_with_latex():
    """Demonstrate a complex system and generate LaTeX output."""
    print("DEMO 5: Complex System with LaTeX Output")
    print("-" * 40)
    
    inequalities = [
        "x1**2 + x2 - 4 >= 0",
        "x1 + 2*x2 - 1 <= 0",
        "x2 - x3 + 1 > 0",
        "x3**2 - x1 <= 2",
        "a*x1 + b*x2 >= c",  # Parametric constraint
        "d + e <= f"  # Pure constraint
    ]
    
    variables = ['x1', 'x2', 'x3']
    
    print("Input system:")
    for ineq in inequalities:
        print(f"  {ineq}")
    print(f"Variables to eliminate: {variables}")
    print()
    
    print("Solving and generating LaTeX report...")
    
    result = solve_with_elimination(
        inequalities, variables, 
        save_latex=True,
        output_filename="complex_demo"
    )
    
    print(f"Result: {len(result['final_inequalities'])} final inequalities")
    print("LaTeX report generated!")
    print()


def run_all_demos():
    """Run all demonstration examples."""
    print("=" * 80)
    print("ENHANCED VARIABLE ELIMINATION SOLVER - DEMONSTRATION")
    print("=" * 80)
    print()
    
    demo_linear_system()
    demo_quadratic_system()
    demo_rational_system()
    demo_single_variable()
    demo_complex_system_with_latex()
    
    print("=" * 80)
    print("DEMONSTRATIONS COMPLETE")
    print("=" * 80)
    print()
    print("Key observations:")
    print("1. Linear systems generally have fewer final inequalities")
    print("2. Quadratic systems can produce many more constraints")
    print("3. Rational systems may have complex case analysis")
    print("4. The number of final inequalities grows with system complexity")
    print("5. Non-variable constraints are preserved throughout")


if __name__ == "__main__":
    run_all_demos()
