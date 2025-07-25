"""
Main integration script for the Enhanced Variable Elimination Solver.

This script provides the main interface for running the enhanced solver
with various examples and configurations.
"""
import sys
import os
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enhanced_solver import solve_with_elimination


def main():
    """Main function with example usage."""
    
    print("Enhanced Variable Elimination Solver")
    print("=" * 50)
    print("Systematic elimination of variables x1, x2, ..., xn from rational inequalities")
    print()
    
    # Example system as requested by the user
    print("EXAMPLE: Multi-variable rational inequality system")
    print("-" * 50)
    
    # Define a comprehensive example system
    inequalities = [
        # Complex rational inequality with multiple variables
        "(x1 + 1)/(x1 - 1) + x2 >= 0",
        
        # Quadratic constraint
        "x1**2 + x2**2 - 4 <= 0",
        
        # Linear constraints with multiple variables
        "x1 + 2*x2 + x3 >= 1",
        "x2 - x3 <= 2",
        "x1 - x3 >= -1",
        
        # Parameter constraints (will be preserved)
        "a + b <= c",
        "d*e >= f",
        
        # Mixed constraint
        "x1 + a*x2 >= b*x3 + c"
    ]
    
    # Variables to eliminate in order
    variables_to_eliminate = ['x1', 'x2', 'x3']
    
    print("Input System:")
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    
    print(f"\nVariables to eliminate: {variables_to_eliminate}")
    print()
    
    # Solve with enhanced elimination
    print("Running enhanced variable elimination...")
    print("This will show 4 steps for each variable:")
    print("  1. Original inequalities")
    print("  2. Min/max expressions with variable")
    print("  3. Min/max expressions without variable")
    print("  4. Final split inequalities")
    print()
    
    # Generate timestamp for output files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        result = solve_with_elimination(
            inequalities=inequalities,
            variables_to_eliminate=variables_to_eliminate,
            use_sign_analysis=True,
            save_latex=True,
            output_filename=f"main_example_{timestamp}"
        )
        
        print("\n" + "="*60)
        print("RESULTS SUMMARY")
        print("="*60)
        
        print(f"Total elimination steps: {result['total_steps']}")
        print(f"Final inequalities: {len(result['final_inequalities'])}")
        print()
        
        if result['final_inequalities']:
            print("Final constraint system (no x1, x2, x3):")
            for i, (lhs, op, rhs) in enumerate(result['final_inequalities'], 1):
                print(f"  {i}. {lhs} {op} {rhs}")
        else:
            print("All variables eliminated - system reduced to feasibility check")
        
        print()
        print("Key Benefits of This Approach:")
        print("• Systematic variable elimination for dimensional reduction")
        print("• Complete documentation of each elimination step")
        print("• Preservation of parameter constraints")
        print("• Useful for optimization and constraint analysis")
        print("• Handles rational, polynomial, and linear inequalities")
        
        return True
        
    except Exception as e:
        print(f"Error during solving: {e}")
        print("This may indicate complex rational expressions that need manual analysis")
        return False


def run_comparison_with_original():
    """Compare with the original solver approach."""
    
    print("\n" + "="*60)
    print("COMPARISON WITH ORIGINAL SOLVER")
    print("="*60)
    
    # Simple system for comparison
    simple_system = [
        "x + y >= 0",
        "x - y <= 1",
        "a + b <= c"
    ]
    
    print("Simple system for comparison:")
    for ineq in simple_system:
        print(f"  {ineq}")
    print()
    
    print("Original approach: Solve for x, get min/max expressions")
    print("Enhanced approach: Eliminate x AND y sequentially")
    print()
    
    # Run enhanced elimination
    result = solve_with_elimination(
        simple_system, 
        ['x', 'y'], 
        save_latex=False
    )
    
    print("Enhanced approach results:")
    print(f"  Steps: {result['total_steps']}")
    print(f"  Final inequalities: {len(result['final_inequalities'])}")
    if result['final_inequalities']:
        for lhs, op, rhs in result['final_inequalities']:
            print(f"    {lhs} {op} {rhs}")
    else:
        print("    All variables eliminated")


def demonstrate_step_by_step():
    """Show detailed step-by-step process."""
    
    print("\n" + "="*60)
    print("DETAILED STEP-BY-STEP DEMONSTRATION")
    print("="*60)
    
    # Very simple system to show process clearly
    demo_system = [
        "x1 >= 0",
        "x1 <= 2", 
        "x1 + x2 >= 1",
        "x2 <= 3"
    ]
    
    print("Demo system:")
    for ineq in demo_system:
        print(f"  {ineq}")
    print()
    
    result = solve_with_elimination(demo_system, ['x1'], save_latex=False)
    
    # Show the detailed breakdown
    step = result['steps'][1]  # First elimination step
    
    print("STEP-BY-STEP BREAKDOWN for x1 elimination:")
    print()
    
    print("1. ORIGINAL INEQUALITIES:")
    for lhs, op, rhs in step['input_inequalities']:
        print(f"   {lhs} {op} {rhs}")
    print()
    
    print("2. MIN/MAX WITH VARIABLE:")
    min_max = step['min_max_expressions']
    for bound in min_max['lower_bounds']:
        print(f"   x1 > {bound['expression']}")
    for bound in min_max['upper_bounds']:
        print(f"   x1 < {bound['expression']}")
    print()
    
    print("3. MIN/MAX WITHOUT VARIABLE:")
    eliminated = step['eliminated_expressions']
    if eliminated['max_expression']:
        print(f"   max(lower bounds) = {eliminated['max_expression']}")
    if eliminated['min_expression']:
        print(f"   min(upper bounds) = {eliminated['min_expression']}")
    print()
    
    print("4. FINAL SPLIT INEQUALITIES:")
    for lhs, op, rhs in step['output_inequalities']:
        print(f"   {lhs} {op} {rhs}")


if __name__ == "__main__":
    success = main()
    
    if success:
        run_comparison_with_original()
        demonstrate_step_by_step()
        
        print("\n" + "="*60)
        print("ENHANCED SOLVER COMPLETE")
        print("="*60)
        print()
        print("Generated files:")
        print("• LaTeX report with complete mathematical derivations")
        print("• Text summary with step-by-step analysis")
        print("• All files saved to enhanced_solver/output/")
        print()
        print("To run more examples:")
        print("  python demo.py              # Multiple demonstrations")
        print("  python simple_example.py    # Clear 4-step breakdown")
        print("  python tests/test_enhanced_solver.py  # Full test suite")
        
    else:
        print("\n" + "="*60)
        print("SOLVER ENCOUNTERED ISSUES")
        print("="*60)
        print("Try running simpler examples:")
        print("  python simple_example.py")
        print("  python demo.py")
