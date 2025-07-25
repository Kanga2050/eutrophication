"""
Simple example demonstrating the 4-step variable elimination process.

This script shows exactly what the user requested:
1. Original inequalities
2. Min/max expressions with the variable  
3. Min/max expressions without the variable
4. Final split inequalities

We'll use a simple system to clearly show each step.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enhanced_solver import solve_with_elimination


def demonstrate_four_steps():
    """Demonstrate the exact 4-step process requested by the user."""
    
    print("=" * 80)
    print("DEMONSTRATION: 4-Step Variable Elimination Process")
    print("=" * 80)
    print()
    
    # Simple system to clearly show the process
    inequalities = [
        "x1 + x2 >= 0",      # Linear constraint
        "x1 - 2 <= 0",       # Upper bound for x1
        "x1 + 1 >= 0",       # Lower bound for x1  
        "x2 - x3 <= 1",      # Constraint involving x2, x3
        "a + b <= c"         # Parameter constraint (preserved)
    ]
    
    print("INITIAL SYSTEM:")
    print("-" * 40)
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    print()
    
    # We'll eliminate x1 first to show the 4 steps clearly
    variables = ['x1']
    
    print("ELIMINATING VARIABLE: x1")
    print("-" * 40)
    print()
    
    # Use the enhanced solver but also manually demonstrate each step
    result = solve_with_elimination(inequalities, variables, save_latex=False)
    
    print("\n" + "="*60)
    print("DETAILED 4-STEP BREAKDOWN")
    print("="*60)
    
    # Get the elimination step for x1
    x1_step = result['steps'][1]  # Step 0 is initial, step 1 is x1 elimination
    
    print("\nSTEP 1: ORIGINAL INEQUALITIES INVOLVING x1")
    print("-" * 50)
    print("These are the inequalities that contain the variable x1:")
    for lhs, op, rhs in x1_step['input_inequalities']:
        if 'x1' in str(lhs) or 'x1' in str(rhs):
            print(f"  {lhs} {op} {rhs}")
    print()
    
    print("STEP 2: MIN/MAX EXPRESSIONS WITH x1")
    print("-" * 50)
    min_max = x1_step['min_max_expressions']
    
    if min_max['lower_bounds']:
        print("Lower bounds (x1 > these expressions):")
        for bound in min_max['lower_bounds']:
            print(f"  x1 > {bound['expression']}")
        print()
    
    if min_max['upper_bounds']:
        print("Upper bounds (x1 < these expressions):")
        for bound in min_max['upper_bounds']:
            print(f"  x1 < {bound['expression']}")
        print()
    
    print("STEP 3: MIN/MAX EXPRESSIONS WITHOUT x1")
    print("-" * 50)
    eliminated = x1_step['eliminated_expressions']
    
    if eliminated['max_expression'] is not None:
        print(f"Maximum of lower bounds: max = {eliminated['max_expression']}")
    else:
        print("No lower bounds found")
        
    if eliminated['min_expression'] is not None:
        print(f"Minimum of upper bounds: min = {eliminated['min_expression']}")
    else:
        print("No upper bounds found")
    print()
    
    print("STEP 4: FINAL SPLIT INEQUALITIES")
    print("-" * 50)
    print("New inequalities created from min/max combinations:")
    for i, (lhs, op, rhs) in enumerate(x1_step['output_inequalities'], 1):
        print(f"  {i}. {lhs} {op} {rhs}")
    print()
    
    print("SUMMARY:")
    print("-" * 50)
    print(f"Original inequalities: {len(x1_step['input_inequalities'])}")
    print(f"Lower bounds found: {len(min_max['lower_bounds'])}")
    print(f"Upper bounds found: {len(min_max['upper_bounds'])}")
    print(f"Final inequalities: {len(x1_step['output_inequalities'])}")
    print()
    
    print("EXPLANATION:")
    print("-" * 50)
    print("• Variable x1 was isolated from inequalities involving it")
    print("• This created lower bounds (x1 >) and upper bounds (x1 <)")
    print("• The max of lower bounds and min of upper bounds were computed")
    print("• For feasibility, we need: max(lower) <= min(upper)")
    print("• Each combination of max terms with min terms creates new constraints")
    print("• Constraints not involving x1 are preserved unchanged")


def demonstrate_multi_variable():
    """Show the process for multiple variables."""
    
    print("\n\n" + "=" * 80)
    print("DEMONSTRATION: Multi-Variable Elimination (x1, x2)")
    print("=" * 80)
    print()
    
    inequalities = [
        "x1 + x2 >= 0",
        "x1 - x2 <= 1", 
        "2*x1 + x2 >= -1",
        "x2 <= 3"
    ]
    
    variables = ['x1', 'x2']
    
    print("SYSTEM TO SOLVE:")
    for ineq in inequalities:
        print(f"  {ineq}")
    print()
    
    result = solve_with_elimination(inequalities, variables, save_latex=False)
    
    print("ELIMINATION SEQUENCE:")
    print("-" * 40)
    
    for step in result['steps']:
        if step['step_number'] == 0:
            print(f"Step {step['step_number']}: {step['description']}")
            print(f"  Starting with {len(step['input_inequalities'])} inequalities")
        else:
            print(f"Step {step['step_number']}: Eliminate {step['variable_eliminated']}")
            print(f"  Input: {len(step['input_inequalities'])} inequalities")
            print(f"  Output: {len(step['output_inequalities'])} inequalities")
            
            min_max = step['min_max_expressions']
            print(f"  Found {len(min_max['lower_bounds'])} lower + {len(min_max['upper_bounds'])} upper bounds")
        print()
    
    print("FINAL RESULT:")
    print("-" * 40)
    if result['final_inequalities']:
        print("Remaining constraints (no x1, x2):")
        for lhs, op, rhs in result['final_inequalities']:
            print(f"  {lhs} {op} {rhs}")
    else:
        print("All variables eliminated - system is either always feasible or infeasible")
    print()
    
    print("INTERPRETATION:")
    print("-" * 40)
    print("• This shows the complete elimination of x1 and x2")
    print("• Each step potentially increases the number of constraints")
    print("• Final system contains only parameter/constant constraints")
    print("• This is useful for parameter analysis and optimization")


if __name__ == "__main__":
    demonstrate_four_steps()
    demonstrate_multi_variable()
    
    print("\n" + "=" * 80)
    print("For complete LaTeX documentation, run:")
    print("  python enhanced_solver.py")
    print("or")  
    print("  python demo.py")
    print("=" * 80)
