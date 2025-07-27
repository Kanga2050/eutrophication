"""
Manual Verification Test Case

Let's design a simple system that we can solve by hand and compare with our solver.

Test System:
1. x1 + x2 <= 3
2. x1 - x2 >= 1  
3. x1/(x2 + 2) >= 0

Goal: Eliminate x1

Manual Solution:
================

Step 1: Isolate x1 from each inequality

From inequality 1: x1 + x2 <= 3
   => x1 <= 3 - x2

From inequality 2: x1 - x2 >= 1
   => x1 >= x2 + 1

From inequality 3: x1/(x2 + 2) >= 0
   Case analysis needed:
   - If x2 + 2 > 0 (i.e., x2 > -2): then x1 >= 0
   - If x2 + 2 < 0 (i.e., x2 < -2): then x1 <= 0
   - If x2 + 2 = 0 (i.e., x2 = -2): undefined, so x2 ≠ -2

Step 2: Combine bounds
For x2 > -2: we have x2 + 1 <= x1 <= min(3 - x2, +∞) and x1 >= 0
   So: max(x2 + 1, 0) <= x1 <= 3 - x2

For x2 < -2: we have x2 + 1 <= x1 <= min(3 - x2, 0)
   So: x2 + 1 <= x1 <= 0

Step 3: Create elimination constraints
For x2 > -2: max(x2 + 1, 0) <= 3 - x2
For x2 < -2: x2 + 1 <= 0

Let's work these out:

Case 1: x2 > -2
   If x2 + 1 >= 0 (i.e., x2 >= -1): then x2 + 1 <= 3 - x2 => 2*x2 <= 2 => x2 <= 1
   If x2 + 1 < 0 (i.e., -2 < x2 < -1): then 0 <= 3 - x2 => x2 <= 3

   So for x2 > -2: we get x2 <= 1

Case 2: x2 < -2
   x2 + 1 <= 0 => x2 <= -1
   
   Combined with x2 < -2, we get x2 < -2

Final Result: 
- x2 < -2, or
- -2 < x2 <= 1

Actually, let's simplify this. The constraint x2 ≠ -2 combined with x2 <= 1 gives us:
x2 <= 1 and x2 ≠ -2

Let's test this with our solver!
"""

from variable_eliminator import solve_with_variable_elimination

def test_manual_case():
    """Test case that we can verify manually."""
    
    print("=" * 80)
    print("MANUAL VERIFICATION TEST")
    print("=" * 80)
    
    # Define our test system
    inequalities = [
        'x1 + x2 <= 3',     # Upper bound: x1 <= 3 - x2
        'x1 - x2 >= 1',     # Lower bound: x1 >= x2 + 1  
        'x1/(x2 + 2) >= 0'  # Case splitting needed
    ]
    
    print("Test System:")
    for i, ineq in enumerate(inequalities, 1):
        print(f"  {i}. {ineq}")
    print()
    
    print("Manual Analysis:")
    print("From x1 + x2 <= 3: x1 <= 3 - x2")
    print("From x1 - x2 >= 1: x1 >= x2 + 1")
    print("From x1/(x2 + 2) >= 0:")
    print("  Case 1: x2 > -2 => x1 >= 0")
    print("  Case 2: x2 < -2 => x1 <= 0")
    print("  (x2 = -2 makes denominator zero, excluded)")
    print()
    
    print("Expected elimination constraints:")
    print("  Case 1 (x2 > -2): max(x2 + 1, 0) <= 3 - x2")
    print("  Case 2 (x2 < -2): x2 + 1 <= 0")
    print()
    
    # Run our solver
    result = solve_with_variable_elimination(
        inequalities, 
        ['x1'], 
        use_sign_analysis=True,
        save_latex=True,
        output_filename='manual_verification_test'
    )
    
    print("\n" + "=" * 80)
    print("COMPARISON WITH SOLVER OUTPUT")
    print("=" * 80)
    
    # Show the step details
    step_1 = result['steps'][1]  # x1 elimination step
    min_max = step_1['min_max_expressions']
    
    print("Solver found bounds:")
    print(f"  Lower bounds: {len(min_max['lower_bounds'])}")
    for bound in min_max['lower_bounds']:
        print(f"    {bound['case_label']}: x1 > {bound['expression']}")
    
    print(f"  Upper bounds: {len(min_max['upper_bounds'])}")
    for bound in min_max['upper_bounds']:
        print(f"    {bound['case_label']}: x1 < {bound['expression']}")
    
    print("\nFinal inequalities after elimination:")
    for lhs, op, rhs in result['final_inequalities']:
        print(f"  {lhs} {op} {rhs}")
    
    return result

if __name__ == "__main__":
    test_manual_case()
